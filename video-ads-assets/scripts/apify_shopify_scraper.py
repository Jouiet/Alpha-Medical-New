#!/usr/bin/env python3
"""
APIFY SHOPIFY SCRAPER - Alpha Medical
Automates product scraping from Shopify store and asset organization

Features:
- Scrapes all products from alphamedical.shop via Apify
- Downloads product images automatically
- Organizes images into proper folder structure
- Fills metadata templates with scraped data
- Supports TOP 3 priority products or all products

Usage:
    python3 apify_shopify_scraper.py --scrape-all
    python3 apify_shopify_scraper.py --scrape-top3
    python3 apify_shopify_scraper.py --scrape-product tourmaline-knee-pads

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
from urllib.parse import urlparse, unquote
from datetime import datetime


# Configuration
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
if not APIFY_API_TOKEN:
    raise ValueError("APIFY_API_TOKEN environment variable not set. Add it to .env file")
APIFY_API_BASE = "https://api.apify.com/v2"
SHOPIFY_STORE_URL = "https://alphamedical.shop"

# Apify Actor IDs for Shopify scraping
SHOPIFY_ACTORS = {
    "products_scraper": "dhrumil/shopify-products-scraper",  # Recommended: $1/1000 products
    "extractor": "jupri/shopify-scraper",                    # Alternative
    "general": "autofacts/shopify"                           # Alternative
}

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
PRODUCTS_DIR = SCRIPT_DIR.parent / "products"
BASE_DIR = SCRIPT_DIR.parent.parent

# TOP 3 priority products (from TOP_10_HERO_PRODUCTS_MAPPING.md)
TOP_3_PRODUCTS = [
    "tourmaline-magnetic-knee-pads-self-heating-support",  # Rank #2, Score 0.923
    "magnetic-posture-corrector",                          # Rank #1, Score 0.934 (need to find exact handle)
    "lower-back-brace"                                      # Rank #6, Score 0.870 (need to find exact handle)
]


class ApifyShopifyScraper:
    """Scrape Shopify store products using Apify API"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def scrape_products(self, store_url: str, max_products: Optional[int] = None) -> Dict:
        """
        Scrape products from Shopify store using Apify actor

        Args:
            store_url: Shopify store URL (e.g., https://alphamedical.shop)
            max_products: Optional limit on number of products to scrape

        Returns:
            Dict containing run_id and status
        """

        actor_id = SHOPIFY_ACTORS["products_scraper"]
        run_url = f"{APIFY_API_BASE}/acts/{actor_id}/runs"

        # Actor input configuration
        actor_input = {
            "startUrls": [{"url": f"{store_url}/collections/all"}],
            "maxItems": max_products if max_products else 1000,
            "proxyConfiguration": {"useApifyProxy": True},
            "extendOutputFunction": "",
            "customMapFunction": ""
        }

        print(f"🚀 Starting Apify actor: {actor_id}")
        print(f"   Store: {store_url}")
        print(f"   Max products: {max_products if max_products else 'All'}")

        response = self.session.post(run_url, json=actor_input)

        if response.status_code != 201:
            print(f"❌ Failed to start actor: {response.status_code}")
            print(f"   Response: {response.text}")
            return None

        run_data = response.json()
        run_id = run_data['data']['id']

        print(f"✅ Actor run started: {run_id}")
        print(f"   Status: {run_data['data']['status']}")

        return run_data['data']

    def wait_for_run(self, run_id: str, timeout: int = 600) -> Dict:
        """
        Wait for Apify actor run to complete

        Args:
            run_id: Actor run ID
            timeout: Maximum wait time in seconds (default 10 min)

        Returns:
            Run data when completed
        """

        status_url = f"{APIFY_API_BASE}/actor-runs/{run_id}"
        start_time = time.time()

        print(f"\n⏳ Waiting for actor run to complete...")
        print(f"   Run ID: {run_id}")

        while True:
            if time.time() - start_time > timeout:
                print(f"❌ Timeout after {timeout} seconds")
                return None

            response = self.session.get(status_url)
            if response.status_code != 200:
                print(f"❌ Failed to get run status: {response.status_code}")
                return None

            run_data = response.json()['data']
            status = run_data['status']

            if status == 'SUCCEEDED':
                print(f"✅ Actor run completed successfully!")
                print(f"   Duration: {run_data.get('stats', {}).get('durationMillis', 0) / 1000:.2f} seconds")
                return run_data

            elif status == 'FAILED':
                print(f"❌ Actor run failed")
                print(f"   Error: {run_data.get('statusMessage', 'Unknown error')}")
                return None

            elif status in ['RUNNING', 'READY']:
                elapsed = int(time.time() - start_time)
                print(f"   Status: {status} ({elapsed}s elapsed)", end='\r')
                time.sleep(5)  # Check every 5 seconds

            else:
                print(f"⚠️  Unexpected status: {status}")
                time.sleep(5)

    def get_dataset_items(self, dataset_id: str) -> List[Dict]:
        """
        Retrieve scraped data from Apify dataset

        Args:
            dataset_id: Dataset ID from completed run

        Returns:
            List of product dictionaries
        """

        dataset_url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items"

        print(f"\n📥 Downloading dataset: {dataset_id}")

        response = self.session.get(dataset_url)

        if response.status_code != 200:
            print(f"❌ Failed to get dataset: {response.status_code}")
            return []

        products = response.json()
        print(f"✅ Downloaded {len(products)} products")

        return products

    def save_products_json(self, products: List[Dict], filepath: Path):
        """Save scraped products to JSON file"""

        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved products to: {filepath}")


class ProductAssetOrganizer:
    """Organize scraped product images into video-ads-assets structure"""

    def __init__(self, products_dir: Path):
        self.products_dir = products_dir

    def download_image(self, url: str, save_path: Path) -> bool:
        """Download image from URL to local path"""

        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                save_path.parent.mkdir(parents=True, exist_ok=True)

                with open(save_path, 'wb') as f:
                    f.write(response.content)

                return True
            else:
                print(f"   ⚠️  Failed to download: {response.status_code}")
                return False

        except Exception as e:
            print(f"   ❌ Download error: {e}")
            return False

    def extract_product_handle(self, product_data: Dict) -> str:
        """Extract product handle from scraped data"""

        # Try different possible fields
        if 'handle' in product_data:
            return product_data['handle']

        if 'url' in product_data:
            # Extract handle from URL: https://alphamedical.shop/products/handle
            parts = urlparse(product_data['url']).path.split('/')
            if 'products' in parts:
                idx = parts.index('products')
                if idx + 1 < len(parts):
                    return parts[idx + 1]

        if 'title' in product_data:
            # Fallback: slugify title
            return product_data['title'].lower().replace(' ', '-').replace('|', '-')

        return "unknown-product"

    def categorize_image(self, image_url: str, index: int, total: int) -> str:
        """
        Categorize image into hero/lifestyle/feature based on heuristics

        Simple logic:
        - First image: hero
        - Last 2 images: feature close-ups
        - Middle images: lifestyle
        """

        if index == 0:
            return "hero"
        elif index >= total - 2:
            return "feature"
        else:
            return "lifestyle"

    def organize_product(self, product_data: Dict) -> bool:
        """
        Organize single product: create folders, download images, fill metadata

        Args:
            product_data: Scraped product dictionary

        Returns:
            bool: Success status
        """

        handle = self.extract_product_handle(product_data)
        product_dir = self.products_dir / handle

        print(f"\n📦 Organizing product: {handle}")
        print(f"   Title: {product_data.get('title', 'N/A')}")

        # Create folder structure
        folders = {
            "hero": product_dir / "hero-images",
            "lifestyle": product_dir / "lifestyle-images",
            "feature": product_dir / "feature-closeups",
            "metadata": product_dir / "metadata"
        }

        for folder_path in folders.values():
            folder_path.mkdir(parents=True, exist_ok=True)

        print(f"   ✅ Created folder structure")

        # Download images
        images = product_data.get('images', [])
        if isinstance(images, list) and len(images) > 0:
            print(f"   📸 Downloading {len(images)} images...")

            downloaded = {"hero": 0, "lifestyle": 0, "feature": 0}

            for idx, image_url in enumerate(images):
                category = self.categorize_image(image_url, idx, len(images))

                # Generate filename
                filename = f"{handle}_{category}_{idx}.jpg"
                save_path = folders[category] / filename

                print(f"      {idx + 1}/{len(images)}: {category} <- {image_url[:60]}...")

                if self.download_image(image_url, save_path):
                    downloaded[category] += 1

            print(f"   ✅ Downloaded: {downloaded['hero']} hero, {downloaded['lifestyle']} lifestyle, {downloaded['feature']} feature")

        else:
            print(f"   ⚠️  No images found in product data")

        # Create metadata files
        self.create_metadata_files(product_dir, handle, product_data)

        return True

    def create_metadata_files(self, product_dir: Path, handle: str, product_data: Dict):
        """Create metadata files for product"""

        metadata_dir = product_dir / "metadata"

        # shopify-url.txt
        shopify_url = product_data.get('url', f"{SHOPIFY_STORE_URL}/products/{handle}")
        url_file = metadata_dir / "shopify-url.txt"
        url_file.write_text(f"{shopify_url}\n")

        # product-info.txt
        info_file = metadata_dir / "product-info.txt"

        title = product_data.get('title', handle.replace('-', ' ').title())
        price = product_data.get('price', 'N/A')
        description = product_data.get('description', 'N/A')
        variants = product_data.get('variants', [])

        info_template = f"""# PRODUCT METADATA: {title.upper()}

**Created:** {datetime.now().strftime('%Y-%m-%d')}
**Handle:** {handle}
**Shopify URL:** {shopify_url}
**Scraped via:** Apify Shopify Products Scraper

---

## BASIC INFO

**Product Name:** {title}
**Category:** [FILL: Knee Support / Back Support / Posture / etc.]
**Price:** ${price}
**Hero Score:** [FILL: Check TOP_10_HERO_PRODUCTS_ANALYSIS.txt]
**Priority Rank:** [FILL: Check TOP_10_HERO_PRODUCTS_MAPPING.md]

---

## PRODUCT DESCRIPTION (From Shopify)

{description[:500]}...

[FILL: Review and enhance description for video ads]

---

## VARIANTS

{len(variants)} variant(s) available:
{self._format_variants(variants[:3])}

---

## TARGET AUDIENCE

**Primary Demographic:**
- Age: [FILL: e.g., 65+, 25-45, etc.]
- Gender: [FILL: Male/Female/Unisex]
- Persona: [FILL: Seniors/Office Workers/Athletes/etc.]

**Pain Points:**
- [FILL: Primary problem this solves]
- [FILL: Secondary problem]
- [FILL: Tertiary problem]

---

## UNIQUE SELLING POINTS (USPs)

**USP 1:** [FILL: e.g., Self-heating technology]
**USP 2:** [FILL: e.g., Magnetic therapy nodes]
**USP 3:** [FILL: e.g., Medical-grade materials]

**Key Features:**
- [FILL: Feature 1]
- [FILL: Feature 2]
- [FILL: Feature 3]

---

## CERTIFICATIONS & SOCIAL PROOF

**Certifications:**
- [ ] FDA-Registered
- [ ] CE Certified
- [ ] Medical-Grade
- [ ] Other: [FILL]

**Social Proof:**
- Customer Count: [FILL: e.g., 8,000+]
- Star Rating: [FILL: e.g., 4.8/5]
- Review Count: [FILL: e.g., 3,000+]

---

## DISCOUNT CODES

**Active Codes:**
- Code 1: [FILL: e.g., WARMKNEES20 (-20%)]
- Code 2: [FILL: e.g., SENIOR20 (-20%)]
- Code 3: [FILL: e.g., WINTER30 (-30%)]

---

## VIDEO ADS STRATEGY

**Recommended Video Types (Priority Order):**
1. [ ] UGC Testimonial (15 sec) - Best for: [FILL: Demographic reason]
2. [ ] Before/After (12 sec) - Best for: [FILL: Visual transformation]
3. [ ] Product Demo (20 sec) - Best for: [FILL: Technology/features]
4. [ ] Comparison (25 sec) - Best for: [FILL: Premium positioning]
5. [ ] Educational (30 sec) - Best for: [FILL: Authority building]

**Template Selection:**
- Primary: [FILL: ugc/ba/demo/comp/edu]
- Secondary: [FILL: ugc/ba/demo/comp/edu]

**Platform Priority:**
- Platform 1: [FILL: TikTok/IG Reels/FB Feed]
- Platform 2: [FILL]
- Platform 3: [FILL]

---

## ASSETS INVENTORY

**Hero Images:**
{self._list_images(product_dir / "hero-images")}

**Lifestyle Images:**
{self._list_images(product_dir / "lifestyle-images")}

**Feature Close-ups:**
{self._list_images(product_dir / "feature-closeups")}

---

## VIDEOS CREATED

**Video 1:**
- Date: [TBD]
- Type: [TBD]
- Filename: [TBD]
- Status: [TBD]

---

**NEXT STEPS:**
1. Review and enhance scraped description for video ads
2. Fill all [FILL] sections with strategic data
3. Select template and create first video
4. Update this metadata with video filename when created
"""

        info_file.write_text(info_template)

        print(f"   ✅ Created metadata files")

    def _format_variants(self, variants: List[Dict]) -> str:
        """Format variants list for metadata"""
        if not variants:
            return "- No variants available"

        lines = []
        for v in variants:
            title = v.get('title', 'N/A')
            price = v.get('price', 'N/A')
            available = v.get('available', True)
            status = "✅ In stock" if available else "❌ Out of stock"
            lines.append(f"- {title}: ${price} ({status})")

        if len(variants) > 3:
            lines.append(f"- ... and {len(variants) - 3} more variants")

        return '\n'.join(lines)

    def _list_images(self, folder_path: Path) -> str:
        """List images in folder for metadata"""
        if not folder_path.exists():
            return "- [ ] Not yet gathered"

        images = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png"))
        if not images:
            return "- [ ] Not yet gathered"

        lines = [f"- [x] {img.name}" for img in images[:5]]
        if len(images) > 5:
            lines.append(f"- ... and {len(images) - 5} more images")

        return '\n'.join(lines)


def scrape_and_organize(
    scraper: ApifyShopifyScraper,
    organizer: ProductAssetOrganizer,
    mode: str = "top3",
    specific_product: Optional[str] = None
) -> bool:
    """
    Main workflow: scrape products and organize assets

    Args:
        scraper: ApifyShopifyScraper instance
        organizer: ProductAssetOrganizer instance
        mode: "all", "top3", or "specific"
        specific_product: Product handle if mode="specific"

    Returns:
        bool: Success status
    """

    print("=" * 60)
    print("APIFY SHOPIFY SCRAPER - Alpha Medical")
    print("=" * 60)
    print(f"Mode: {mode.upper()}")
    print(f"Store: {SHOPIFY_STORE_URL}")
    print("=" * 60)

    # Step 1: Scrape products
    max_products = None if mode == "all" else (3 if mode == "top3" else 100)

    run_data = scraper.scrape_products(SHOPIFY_STORE_URL, max_products=max_products)
    if not run_data:
        return False

    # Step 2: Wait for completion
    run_id = run_data['id']
    completed_run = scraper.wait_for_run(run_id, timeout=600)

    if not completed_run:
        return False

    # Step 3: Download dataset
    dataset_id = completed_run['defaultDatasetId']
    products = scraper.get_dataset_items(dataset_id)

    if not products:
        print("❌ No products found in dataset")
        return False

    # Save raw scraped data
    scraped_data_file = BASE_DIR / "scraped_shopify_products.json"
    scraper.save_products_json(products, scraped_data_file)

    # Step 4: Organize products
    print("\n" + "=" * 60)
    print("ORGANIZING PRODUCT ASSETS")
    print("=" * 60)

    if mode == "specific" and specific_product:
        # Find specific product
        product = next((p for p in products if organizer.extract_product_handle(p) == specific_product), None)
        if product:
            organizer.organize_product(product)
        else:
            print(f"❌ Product not found: {specific_product}")
            return False

    elif mode == "top3":
        # Organize only TOP 3 priority products
        organized_count = 0
        for product in products:
            handle = organizer.extract_product_handle(product)
            if any(priority_handle in handle for priority_handle in TOP_3_PRODUCTS):
                organizer.organize_product(product)
                organized_count += 1
                if organized_count >= 3:
                    break

    else:  # mode == "all"
        for product in products:
            organizer.organize_product(product)

    print("\n" + "=" * 60)
    print("✅ SCRAPING & ORGANIZATION COMPLETE!")
    print("=" * 60)
    print(f"\n📂 Products organized in: {PRODUCTS_DIR}")
    print(f"📄 Raw data saved to: {scraped_data_file}")
    print(f"\n🎬 Next steps:")
    print(f"   1. Review organized assets in products/ folders")
    print(f"   2. Fill [FILL] sections in metadata/product-info.txt")
    print(f"   3. Run: python3 asset_organizer.py --verify-all")
    print(f"   4. Create videos following VIDEO_ADS_CREATION_PLAYBOOK.md")

    return True


def main():
    """CLI entry point"""

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable commands:")
        print("  --scrape-all          Scrape ALL products from store")
        print("  --scrape-top3         Scrape and organize TOP 3 priority products")
        print("  --scrape-product {handle}  Scrape specific product by handle")
        sys.exit(1)

    command = sys.argv[1]

    # Initialize
    scraper = ApifyShopifyScraper(APIFY_API_TOKEN)
    organizer = ProductAssetOrganizer(PRODUCTS_DIR)

    if command == "--scrape-all":
        scrape_and_organize(scraper, organizer, mode="all")

    elif command == "--scrape-top3":
        scrape_and_organize(scraper, organizer, mode="top3")

    elif command == "--scrape-product":
        if len(sys.argv) < 3:
            print("❌ Error: Product handle required")
            print("Usage: python3 apify_shopify_scraper.py --scrape-product {product-handle}")
            sys.exit(1)

        product_handle = sys.argv[2]
        scrape_and_organize(scraper, organizer, mode="specific", specific_product=product_handle)

    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
