#!/usr/bin/env python3
"""
MARKET ANALYSIS SCRAPER - Alpha Medical
Scrapes competitor products and prices from AliExpress and Google Shopping using Apify

Features:
- Scrapes competitor products from AliExpress (suppliers/wholesale)
- Scrapes Google Shopping results (retail competitors)
- Analyzes pricing, features, positioning
- Creates comprehensive market analysis dataset
- Monitors price changes over time

Usage:
    python3 market_analysis_scraper.py --aliexpress "magnetic knee pads"
    python3 market_analysis_scraper.py --google-shopping "tourmaline knee support"
    python3 market_analysis_scraper.py --full-analysis

Environment:
    APIFY_API_TOKEN=<your_apify_token_here>
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict


# Configuration
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
if not APIFY_API_TOKEN:
    raise ValueError("APIFY_API_TOKEN environment variable not set. Add it to .env file")
APIFY_API_BASE = "https://api.apify.com/v2"

# Apify Actor IDs
ACTORS = {
    "aliexpress": "junglee/aliexpress-scraper",  # AliExpress products scraper
    "google_shopping": "canadesk/google-shopping-scraper",  # Google Shopping scraper
    "amazon": "junglee/amazon-crawler"  # Bonus: Amazon scraper if needed
}

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / "data"
REPORTS_DIR = SCRIPT_DIR / "reports"

# TOP 9 Alpha Medical products to analyze competitors for (TOP 3 PER REAL CATEGORY)
#
# FACTUAL ANALYSIS based on alphamedical.shop collections:
# CATEGORY 1: PAIN RELIEF & RECOVERY (50 products on site)
# CATEGORY 2: POSTURE & SUPPORT (15 products on site)
# CATEGORY 3: THERAPY & WELLNESS (13 products on site)

TOP_PRODUCTS_BY_CATEGORY = {
    "pain-relief-recovery": {
        "tourmaline-knee-pads": {
            "name": "Tourmaline Magnetic Knee Pads | Self-Heating Support",
            "hero_rank": 2,
            "score": 0.700,
            "alpha_price": 55,
            "demographic": "Seniors 65+",
            "collection": "/collections/pain-relief-recovery",
            "keywords": [
                "tourmaline magnetic knee pads",
                "self-heating knee brace",
                "magnetic therapy knee support",
                "heated knee pads arthritis"
            ]
        },
        "neck-massage-machine": {
            "name": "Neck Massage Machine | 4-Head Heating Protection",
            "hero_rank": None,
            "score": 0.650,
            "alpha_price": 73,
            "demographic": "Office Workers + Seniors",
            "collection": "/collections/pain-relief-recovery",
            "keywords": [
                "neck massage machine",
                "4 head heating massage",
                "neck pain relief",
                "electric neck massager"
            ]
        },
        "intelligent-massage-gloves": {
            "name": "Intelligent Massage Gloves | Hand Rehabilitation Robot",
            "hero_rank": None,
            "score": 0.600,
            "alpha_price": 123,
            "demographic": "Seniors + Rehabilitation",
            "collection": "/collections/pain-relief-recovery",
            "keywords": [
                "hand rehabilitation gloves",
                "massage gloves robot",
                "hand recovery device",
                "stroke rehabilitation"
            ]
        }
    },
    "posture-support": {
        "magnetic-posture-corrector": {
            "name": "Magnetic Posture Corrector | Shoulder Orthopedic Brace",
            "hero_rank": 1,
            "score": 0.660,
            "alpha_price": 50,
            "demographic": "Office Workers 25-55",
            "collection": "/collections/posture-support",
            "keywords": [
                "magnetic posture corrector",
                "shoulder orthopedic brace",
                "back posture support",
                "magnetic back corrector"
            ]
        },
        "inflatable-neck-collar": {
            "name": "Inflatable Neck Collar | Cervical Traction Pillow",
            "hero_rank": None,
            "score": 0.605,
            "alpha_price": 45,  # Estimate
            "demographic": "Office Workers + Seniors",
            "collection": "/collections/posture-support",
            "keywords": [
                "inflatable neck collar",
                "cervical traction pillow",
                "neck pain relief",
                "cervical stretcher"
            ]
        },
        "neck-traction-device": {
            "name": "Neck Traction Device | Heating Inflatable Cervical",
            "hero_rank": None,
            "score": 0.600,
            "alpha_price": 50,  # Estimate
            "demographic": "Office Workers + Seniors",
            "collection": "/collections/posture-support",
            "keywords": [
                "neck traction device",
                "heating cervical traction",
                "inflatable neck support",
                "cervical pain relief"
            ]
        }
    },
    "therapy-wellness": {
        "led-face-mask-7-color": {
            "name": "7 Color LED Face Mask | Red Light Therapy",
            "hero_rank": None,
            "score": 0.560,
            "alpha_price": 148,
            "demographic": "Beauty/Wellness 25-55",
            "collection": "/collections/therapy-wellness",
            "keywords": [
                "7 color LED face mask",
                "red light therapy",
                "photon light therapy",
                "anti-aging LED mask"
            ]
        },
        "foreverlily-led-mask": {
            "name": "Foreverlily LED Face & Neck Mask | 7 Colors 3D Flexible",
            "hero_rank": None,
            "score": 0.560,
            "alpha_price": 83,
            "demographic": "Beauty/Wellness 25-55",
            "collection": "/collections/therapy-wellness",
            "keywords": [
                "foreverlily LED mask",
                "7 color face neck mask",
                "3D flexible LED therapy",
                "photon beauty mask"
            ]
        },
        "hello-face-red-light-mask": {
            "name": "Hello Face Red Light Therapy Mask | Face & Neck Infrared LED",
            "hero_rank": None,
            "score": 0.560,
            "alpha_price": 107,
            "demographic": "Beauty/Wellness 25-55",
            "collection": "/collections/therapy-wellness",
            "keywords": [
                "hello face red light mask",
                "infrared LED therapy",
                "face neck light therapy",
                "professional LED mask"
            ]
        }
    }
}

# Flatten structure for iteration
TOP_9_PRODUCTS_FLAT = {}
for category, products in TOP_PRODUCTS_BY_CATEGORY.items():
    for product_key, product_data in products.items():
        TOP_9_PRODUCTS_FLAT[product_key] = product_data
        TOP_9_PRODUCTS_FLAT[product_key]["category"] = category


class ApifyMarketScraper:
    """Scrape market data using Apify actors"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def scrape_aliexpress(self, keyword: str, max_items: int = 50) -> List[Dict]:
        """
        Scrape AliExpress for competitor products

        Args:
            keyword: Search keyword (e.g., "magnetic knee pads")
            max_items: Maximum products to scrape

        Returns:
            List of product dictionaries
        """

        actor_id = ACTORS["aliexpress"]
        run_url = f"{APIFY_API_BASE}/acts/{actor_id}/runs"

        actor_input = {
            "search": keyword,
            "maxItems": max_items,
            "minPrice": 0,
            "maxPrice": 200,
            "proxyConfiguration": {"useApifyProxy": True},
            "includeDescription": True,
            "includeImages": True
        }

        print(f"\n🔍 Scraping AliExpress: '{keyword}'")
        print(f"   Max items: {max_items}")

        response = self.session.post(run_url, json=actor_input)

        if response.status_code != 201:
            print(f"❌ Failed to start actor: {response.status_code}")
            return []

        run_data = response.json()['data']
        run_id = run_data['id']

        print(f"   Run ID: {run_id}")

        # Wait for completion
        completed_run = self._wait_for_run(run_id)
        if not completed_run:
            return []

        # Get dataset
        dataset_id = completed_run['defaultDatasetId']
        products = self._get_dataset_items(dataset_id)

        print(f"✅ Scraped {len(products)} products from AliExpress")

        return products

    def scrape_google_shopping(self, keyword: str, max_items: int = 50) -> List[Dict]:
        """
        Scrape Google Shopping for competitor products

        Args:
            keyword: Search keyword
            max_items: Maximum results

        Returns:
            List of product dictionaries
        """

        actor_id = ACTORS["google_shopping"]
        run_url = f"{APIFY_API_BASE}/acts/{actor_id}/runs"

        actor_input = {
            "queries": [keyword],
            "maxItemsPerQuery": max_items,
            "countryCode": "US",  # Can be changed: CA, UK, etc.
            "proxyConfiguration": {"useApifyProxy": True}
        }

        print(f"\n🔍 Scraping Google Shopping: '{keyword}'")
        print(f"   Max items: {max_items}")
        print(f"   Country: US")

        response = self.session.post(run_url, json=actor_input)

        if response.status_code != 201:
            print(f"❌ Failed to start actor: {response.status_code}")
            return []

        run_data = response.json()['data']
        run_id = run_data['id']

        print(f"   Run ID: {run_id}")

        # Wait for completion
        completed_run = self._wait_for_run(run_id)
        if not completed_run:
            return []

        # Get dataset
        dataset_id = completed_run['defaultDatasetId']
        products = self._get_dataset_items(dataset_id)

        print(f"✅ Scraped {len(products)} products from Google Shopping")

        return products

    def _wait_for_run(self, run_id: str, timeout: int = 600) -> Optional[Dict]:
        """Wait for Apify actor run to complete"""

        status_url = f"{APIFY_API_BASE}/actor-runs/{run_id}"
        start_time = time.time()

        print(f"   ⏳ Waiting for completion...", end='')

        while True:
            if time.time() - start_time > timeout:
                print(f" ❌ Timeout after {timeout}s")
                return None

            response = self.session.get(status_url)
            if response.status_code != 200:
                print(f" ❌ Status check failed: {response.status_code}")
                return None

            run_data = response.json()['data']
            status = run_data['status']

            if status == 'SUCCEEDED':
                duration = run_data.get('stats', {}).get('durationMillis', 0) / 1000
                print(f" ✅ ({duration:.1f}s)")
                return run_data

            elif status == 'FAILED':
                print(f" ❌ Run failed")
                return None

            elif status in ['RUNNING', 'READY']:
                elapsed = int(time.time() - start_time)
                print(f"\r   ⏳ Waiting for completion... {elapsed}s", end='')
                time.sleep(5)

            else:
                time.sleep(5)

    def _get_dataset_items(self, dataset_id: str) -> List[Dict]:
        """Retrieve items from Apify dataset"""

        dataset_url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items"
        response = self.session.get(dataset_url)

        if response.status_code != 200:
            return []

        return response.json()


class MarketAnalyzer:
    """Analyze competitor data and generate insights"""

    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def analyze_aliexpress_pricing(self, products: List[Dict], alpha_price: float) -> Dict:
        """
        Analyze AliExpress pricing vs Alpha Medical

        Returns pricing insights dictionary
        """

        if not products:
            return {}

        prices = []
        for product in products:
            # AliExpress price extraction (varies by actor output structure)
            price = product.get('price', {})
            if isinstance(price, dict):
                price_value = price.get('min', price.get('value', 0))
            else:
                price_value = float(price) if price else 0

            if price_value > 0:
                prices.append(price_value)

        if not prices:
            return {}

        analysis = {
            "total_products": len(products),
            "products_with_price": len(prices),
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": sum(prices) / len(prices),
            "median_price": sorted(prices)[len(prices) // 2],
            "alpha_price": alpha_price,
            "alpha_vs_min": alpha_price - min(prices),
            "alpha_vs_avg": alpha_price - (sum(prices) / len(prices)),
            "alpha_vs_median": alpha_price - sorted(prices)[len(prices) // 2],
            "price_percentile": sum(1 for p in prices if p < alpha_price) / len(prices) * 100
        }

        return analysis

    def analyze_google_shopping_competitors(self, products: List[Dict], alpha_price: float) -> Dict:
        """Analyze Google Shopping competitors"""

        if not products:
            return {}

        prices = []
        merchants = defaultdict(int)
        ratings = []

        for product in products:
            # Google Shopping price extraction
            price_str = product.get('price', '').replace('$', '').replace(',', '')
            try:
                price_value = float(price_str)
                if price_value > 0:
                    prices.append(price_value)
            except:
                pass

            # Merchant analysis
            merchant = product.get('merchant', {}).get('name', 'Unknown')
            merchants[merchant] += 1

            # Rating analysis
            rating = product.get('rating', 0)
            if rating > 0:
                ratings.append(rating)

        analysis = {
            "total_products": len(products),
            "products_with_price": len(prices),
            "min_price": min(prices) if prices else 0,
            "max_price": max(prices) if prices else 0,
            "avg_price": sum(prices) / len(prices) if prices else 0,
            "median_price": sorted(prices)[len(prices) // 2] if prices else 0,
            "alpha_price": alpha_price,
            "alpha_vs_avg": alpha_price - (sum(prices) / len(prices)) if prices else 0,
            "top_merchants": dict(sorted(merchants.items(), key=lambda x: x[1], reverse=True)[:5]),
            "avg_rating": sum(ratings) / len(ratings) if ratings else 0,
            "products_with_rating": len(ratings)
        }

        return analysis

    def generate_market_report(
        self,
        product_key: str,
        product_info: Dict,
        aliexpress_data: List[Dict],
        google_shopping_data: List[Dict]
    ) -> Dict:
        """Generate comprehensive market analysis report"""

        report = {
            "product": product_info['name'],
            "product_key": product_key,
            "alpha_price": product_info['alpha_price'],
            "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "aliexpress_analysis": self.analyze_aliexpress_pricing(
                aliexpress_data,
                product_info['alpha_price']
            ),
            "google_shopping_analysis": self.analyze_google_shopping_competitors(
                google_shopping_data,
                product_info['alpha_price']
            ),
            "summary": {}
        }

        # Generate summary insights
        ae_analysis = report['aliexpress_analysis']
        gs_analysis = report['google_shopping_analysis']

        summary = {}

        # Pricing positioning
        if ae_analysis:
            summary['aliexpress_positioning'] = (
                f"Alpha Medical price (${product_info['alpha_price']}) is "
                f"{ae_analysis['price_percentile']:.0f}th percentile on AliExpress. "
                f"Average AliExpress price: ${ae_analysis['avg_price']:.2f}"
            )

        if gs_analysis:
            if gs_analysis['avg_price'] > 0:
                summary['google_shopping_positioning'] = (
                    f"Alpha Medical price is "
                    f"${abs(gs_analysis['alpha_vs_avg']):.2f} "
                    f"{'above' if gs_analysis['alpha_vs_avg'] > 0 else 'below'} "
                    f"average Google Shopping price (${gs_analysis['avg_price']:.2f})"
                )
            summary['top_competitors'] = gs_analysis['top_merchants']

        report['summary'] = summary

        return report

    def save_report(self, report: Dict, product_key: str):
        """Save market analysis report to JSON"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"market_analysis_{product_key}_{timestamp}.json"
        filepath = REPORTS_DIR / filename

        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Report saved: {filepath}")

        return filepath

    def print_summary(self, report: Dict):
        """Print market analysis summary to console"""

        print("\n" + "=" * 70)
        print(f"MARKET ANALYSIS REPORT: {report['product']}")
        print("=" * 70)

        print(f"\n📊 Alpha Medical Price: ${report['alpha_price']}")

        # AliExpress summary
        ae = report['aliexpress_analysis']
        if ae:
            print(f"\n🌐 ALIEXPRESS ANALYSIS ({ae['products_with_price']} products)")
            print(f"   Price Range: ${ae['min_price']:.2f} - ${ae['max_price']:.2f}")
            print(f"   Average: ${ae['avg_price']:.2f}")
            print(f"   Median: ${ae['median_price']:.2f}")
            print(f"   Alpha vs Average: ${ae['alpha_vs_avg']:+.2f}")
            print(f"   Position: {ae['price_percentile']:.0f}th percentile")

        # Google Shopping summary
        gs = report['google_shopping_analysis']
        if gs:
            print(f"\n🛍️  GOOGLE SHOPPING ANALYSIS ({gs['products_with_price']} products)")
            print(f"   Price Range: ${gs['min_price']:.2f} - ${gs['max_price']:.2f}")
            print(f"   Average: ${gs['avg_price']:.2f}")
            print(f"   Alpha vs Average: ${gs['alpha_vs_avg']:+.2f}")

            if gs['avg_rating'] > 0:
                print(f"   Average Rating: {gs['avg_rating']:.1f}/5 ({gs['products_with_rating']} products)")

            print(f"\n   🏪 Top Competitors:")
            for merchant, count in list(gs['top_merchants'].items())[:5]:
                print(f"      - {merchant}: {count} products")

        # Insights
        print(f"\n💡 INSIGHTS:")
        for key, insight in report['summary'].items():
            if isinstance(insight, str):
                print(f"   • {insight}")

        print("\n" + "=" * 70)


def full_market_analysis(scraper: ApifyMarketScraper, analyzer: MarketAnalyzer):
    """
    Run full market analysis for TOP 9 Alpha Medical products (TOP 3 per category)

    Scrapes both AliExpress and Google Shopping for each product across 3 categories:
    - NECK/POSTURE SUPPORT (Office Workers 25-55)
    - KNEE SUPPORT (Seniors 65+)
    - LOWER BACK/LUMBAR (Mixed demographics)
    """

    print("=" * 70)
    print("FULL MARKET ANALYSIS - Alpha Medical TOP 9 Products (TOP 3 per Category)")
    print("=" * 70)

    reports = []

    for product_key, product_info in TOP_9_PRODUCTS_FLAT.items():
        print(f"\n{'='*70}")
        print(f"ANALYZING: {product_info['name']}")
        print(f"{'='*70}")

        # Use primary keyword for scraping
        primary_keyword = product_info['keywords'][0]

        # Scrape AliExpress
        aliexpress_data = scraper.scrape_aliexpress(primary_keyword, max_items=30)

        # Save raw AliExpress data
        ae_file = DATA_DIR / f"aliexpress_{product_key}_{datetime.now().strftime('%Y%m%d')}.json"
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(ae_file, 'w', encoding='utf-8') as f:
            json.dump(aliexpress_data, f, indent=2)
        print(f"   💾 Saved raw AliExpress data: {ae_file.name}")

        # Scrape Google Shopping
        google_shopping_data = scraper.scrape_google_shopping(primary_keyword, max_items=30)

        # Save raw Google Shopping data
        gs_file = DATA_DIR / f"google_shopping_{product_key}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(gs_file, 'w', encoding='utf-8') as f:
            json.dump(google_shopping_data, f, indent=2)
        print(f"   💾 Saved raw Google Shopping data: {gs_file.name}")

        # Generate analysis report
        report = analyzer.generate_market_report(
            product_key,
            product_info,
            aliexpress_data,
            google_shopping_data
        )

        # Save and display report
        analyzer.save_report(report, product_key)
        analyzer.print_summary(report)

        reports.append(report)

        # Rate limiting between products
        time.sleep(10)

    # Generate combined summary
    print("\n" + "=" * 70)
    print("📈 MARKET ANALYSIS COMPLETE!")
    print("=" * 70)
    print(f"\n✅ Analyzed {len(reports)} products")
    print(f"📂 Reports saved in: {REPORTS_DIR}")
    print(f"📂 Raw data saved in: {DATA_DIR}")

    return reports


def main():
    """CLI entry point"""

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable commands:")
        print("  --full-analysis           Run complete market analysis for TOP 3 products")
        print("  --aliexpress <keyword>    Scrape AliExpress only")
        print("  --google-shopping <keyword>  Scrape Google Shopping only")
        sys.exit(1)

    command = sys.argv[1]

    scraper = ApifyMarketScraper(APIFY_API_TOKEN)
    analyzer = MarketAnalyzer(DATA_DIR)

    if command == "--full-analysis":
        full_market_analysis(scraper, analyzer)

    elif command == "--aliexpress":
        if len(sys.argv) < 3:
            print("❌ Error: Keyword required")
            print("Usage: python3 market_analysis_scraper.py --aliexpress 'keyword'")
            sys.exit(1)

        keyword = sys.argv[2]
        products = scraper.scrape_aliexpress(keyword, max_items=50)

        # Save data
        filename = f"aliexpress_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = DATA_DIR / filename
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2)

        print(f"\n💾 Saved {len(products)} products to: {filepath}")

    elif command == "--google-shopping":
        if len(sys.argv) < 3:
            print("❌ Error: Keyword required")
            print("Usage: python3 market_analysis_scraper.py --google-shopping 'keyword'")
            sys.exit(1)

        keyword = sys.argv[2]
        products = scraper.scrape_google_shopping(keyword, max_items=50)

        # Save data
        filename = f"google_shopping_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = DATA_DIR / filename
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2)

        print(f"\n💾 Saved {len(products)} products to: {filepath}")

    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
