#!/usr/bin/env python3
"""
ANALYZE TOP 10 HERO PRODUCTS FOR ADS
Date: 2025-11-22
Purpose: Identify top 10 products for Creatify video ads & carousel ads
Criteria: Price, Sales potential, 2025-2026 trends, Demographics match
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime

def load_product_matrix() -> Dict:
    """Load product matrix JSON"""
    with open('product_matrix_complete.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert product_matrix dict to list of products
    products = []
    for handle, product_data in data.get('product_matrix', {}).items():
        product = {
            'handle': handle,
            'title': product_data.get('name', handle),
            'scores': product_data.get('scores', {})
        }
        products.append(product)

    return products

def calculate_hero_score(product: Dict, current_season: str = "winter") -> Tuple[float, Dict]:
    """
    Calculate hero product score based on multiple criteria

    Criteria weights:
    - Price tier (30%): Mid-range products ($40-80) score highest
    - Seasonality (25%): Match current + next season (winter → spring 2025-2026)
    - Demographics (20%): Match FB/IG personas (office workers, seniors, athletes)
    - Trends 2025-2026 (15%): UGC-friendly, visual appeal, problem-solution narrative
    - Sales potential (10%): Overall score from matrix

    Returns:
        Tuple of (total_score, breakdown_dict)
    """
    breakdown = {}
    scores = product.get('scores', {})

    # 1. PRICE TIER SCORE (30% weight)
    # Sweet spot: mid_range products ($40-80) score highest
    price_tier_scores = scores.get('price_tier', {})

    # Weights for each tier (mid_range is optimal for ads)
    tier_weights = {
        'budget': 0.6,      # <$40 - Lower AOV but high volume
        'mid_range': 1.0,   # $40-80 - OPTIMAL
        'premium': 0.75,    # $80-150 - Higher value but lower conversion
        'luxury': 0.5       # >$150 - Lowest conversion for cold ads
    }

    # Calculate weighted price score
    price_score = sum(
        price_tier_scores.get(tier, 0) * weight
        for tier, weight in tier_weights.items()
    ) * 0.30

    # Determine dominant tier for display
    dominant_tier = max(price_tier_scores.items(), key=lambda x: x[1])[0] if price_tier_scores else 'unknown'

    breakdown['price'] = {
        'tier': dominant_tier,
        'score': price_score,
        'weight': '30%',
        'tier_scores': price_tier_scores
    }

    # 2. SEASONALITY SCORE (25% weight)
    # Winter 2025 (now) + Spring 2026 (next)
    seasonality = scores.get('seasonality', {})
    winter_score = seasonality.get('winter', 0.5)
    spring_score = seasonality.get('spring', 0.5)

    # Weight: 60% current season (winter), 40% next season (spring)
    seasonality_score = (winter_score * 0.6 + spring_score * 0.4) * 0.25
    breakdown['seasonality'] = {
        'winter': winter_score,
        'spring': spring_score,
        'combined': seasonality_score,
        'weight': '25%'
    }

    # 3. DEMOGRAPHICS SCORE (20% weight)
    # Match FB/IG personas: office_workers (28%), seniors (27%), athletes (10%)
    demographics = scores.get('demographics', {})

    # Weighted by catalog representation + ad platform fit
    demo_weights = {
        'office_workers_25_55': 0.35,  # 28% catalog + perfect FB/IG match
        'seniors_65plus': 0.35,        # 27% catalog + strong FB match
        'athletes_18_45': 0.20,        # 10% catalog + strong IG match
        'beauty_wellness_25_55': 0.10  # 20% catalog but lower priority (non-orthopedic)
    }

    demo_score = sum(
        demographics.get(demo, 0) * weight
        for demo, weight in demo_weights.items()
    ) * 0.20
    breakdown['demographics'] = {
        'scores': demographics,
        'weighted_score': demo_score,
        'weight': '20%'
    }

    # 4. TRENDS 2025-2026 SCORE (15% weight)
    # UGC-friendly products: visual appeal, clear before/after, problem-solution
    trends_score = 0

    # Check product attributes
    title = product.get('title', '').lower()
    # Extract product_type from pain_type scores (dominant pain type)
    pain_type_scores = scores.get('pain_type', {})
    product_type = max(pain_type_scores.items(), key=lambda x: x[1])[0] if pain_type_scores else ''

    # UGC-friendly attributes
    ugc_keywords = {
        'brace': 0.25,      # Visual, wearable, demo-friendly
        'support': 0.25,    # Clear problem-solution
        'knee': 0.20,       # High demand + visual
        'back': 0.20,       # High demand + relatable
        'posture': 0.20,    # Before/after potential
        'compression': 0.15,# Performance + visual
        'heated': 0.15,     # Winter trend + unique feature
        'magnetic': 0.10,   # Differentiator
        'therapy': 0.10     # Medical authority
    }

    for keyword, score_boost in ugc_keywords.items():
        if keyword in title or keyword in product_type:
            trends_score += score_boost

    trends_score = min(trends_score, 1.0) * 0.15
    breakdown['trends_2025_2026'] = {
        'ugc_friendliness': trends_score,
        'weight': '15%'
    }

    # 5. SALES POTENTIAL (10% weight)
    # Calculate average of all dimension scores
    all_scores = []
    for dimension in scores.values():
        if isinstance(dimension, dict):
            all_scores.extend(dimension.values())

    overall_score = sum(all_scores) / len(all_scores) if all_scores else 0.5
    sales_score = overall_score * 0.10
    breakdown['sales_potential'] = {
        'overall_matrix_score': overall_score,
        'weighted_score': sales_score,
        'weight': '10%'
    }

    # TOTAL HERO SCORE
    total_score = (
        price_score +
        seasonality_score +
        demo_score +
        trends_score +
        sales_score
    )

    return total_score, breakdown

def analyze_top_10(products: List[Dict]) -> List[Dict]:
    """Analyze and rank all products, return top 10"""
    scored_products = []

    for product in products:
        hero_score, breakdown = calculate_hero_score(product, current_season="winter")

        scored_products.append({
            'product': product,
            'hero_score': hero_score,
            'breakdown': breakdown
        })

    # Sort by hero_score descending
    scored_products.sort(key=lambda x: x['hero_score'], reverse=True)

    return scored_products[:10]

def format_top_10_report(top_10: List[Dict]) -> str:
    """Format detailed report for top 10 products"""

    report = []
    report.append("=" * 100)
    report.append("TOP 10 HERO PRODUCTS FOR CREATIFY VIDEO ADS & CAROUSEL ADS")
    report.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("Criteria: Price Tier (30%) + Seasonality Winter/Spring (25%) + Demographics (20%) + UGC Trends (15%) + Sales Potential (10%)")
    report.append("=" * 100)
    report.append("")

    for rank, item in enumerate(top_10, 1):
        product = item['product']
        score = item['hero_score']
        breakdown = item['breakdown']

        report.append(f"\n{'='*100}")
        report.append(f"RANK #{rank} | HERO SCORE: {score:.3f}/1.000")
        report.append(f"{'='*100}")

        # Product Info
        # Determine product type from pain_type scores
        pain_scores = product.get('scores', {}).get('pain_type', {})
        dominant_pain_type = max(pain_scores.items(), key=lambda x: x[1])[0] if pain_scores else 'N/A'

        report.append(f"\n📦 PRODUCT: {product.get('title', 'N/A')}")
        report.append(f"   Handle: {product.get('handle', 'N/A')}")
        report.append(f"   Type: {dominant_pain_type} support")
        report.append(f"   Price Tier: {breakdown['price']['tier'].upper()}")

        # Score Breakdown
        report.append(f"\n📊 SCORE BREAKDOWN:")
        report.append(f"   • Price (30%): {breakdown['price']['score']:.3f} [{breakdown['price']['tier']}]")
        report.append(f"   • Seasonality (25%): {breakdown['seasonality']['combined']:.3f} [Winter: {breakdown['seasonality']['winter']:.2f}, Spring: {breakdown['seasonality']['spring']:.2f}]")
        report.append(f"   • Demographics (20%): {breakdown['demographics']['weighted_score']:.3f}")
        report.append(f"   • UGC Trends 2025 (15%): {breakdown['trends_2025_2026']['ugc_friendliness']:.3f}")
        report.append(f"   • Sales Potential (10%): {breakdown['sales_potential']['weighted_score']:.3f}")

        # Demographics Detail
        demo_scores = breakdown['demographics']['scores']
        report.append(f"\n👥 DEMOGRAPHICS FIT:")
        if demo_scores.get('office_workers_25_55', 0) > 0.5:
            report.append(f"   ✓ Office Workers 25-55: {demo_scores['office_workers_25_55']:.2f} (FB/IG primary)")
        if demo_scores.get('seniors_65plus', 0) > 0.5:
            report.append(f"   ✓ Seniors 65+: {demo_scores['seniors_65plus']:.2f} (FB strong)")
        if demo_scores.get('athletes_18_45', 0) > 0.5:
            report.append(f"   ✓ Athletes 18-45: {demo_scores['athletes_18_45']:.2f} (IG/Reels strong)")
        if demo_scores.get('beauty_wellness_25_55', 0) > 0.5:
            report.append(f"   ✓ Beauty/Wellness 25-55: {demo_scores['beauty_wellness_25_55']:.2f} (IG visual)")

        # Ad Recommendations
        report.append(f"\n🎬 AD FORMAT RECOMMENDATIONS:")

        # Determine best ad type
        demo = breakdown['demographics']['scores']
        price_tier = breakdown['price']['tier']

        ad_types = []
        if demo.get('athletes_18_45', 0) > 0.6 or 'sports' in product.get('title', '').lower():
            ad_types.append("✓ UGC Video (9:16 Reels) - Athlete testimonial")
        if demo.get('seniors_65plus', 0) > 0.6:
            ad_types.append("✓ Video Before/After (1:1 FB Feed) - Senior comfort")
        if demo.get('office_workers_25_55', 0) > 0.6:
            ad_types.append("✓ Carousel (1:1) - Pain → Solution journey")
        if price_tier == 'premium' or price_tier == 'luxury':
            ad_types.append("✓ Demo Video (9:16) - Educational, authority-building")
        if price_tier == 'mid' or price_tier == 'budget':
            ad_types.append("✓ Carousel (5-6 cards) - Features + social proof + offer")

        for ad_type in ad_types[:3]:  # Top 3 recommendations
            report.append(f"   {ad_type}")

        report.append("")

    # Summary section
    report.append(f"\n{'='*100}")
    report.append("SUMMARY & NEXT STEPS")
    report.append(f"{'='*100}\n")

    # Count by pain type category
    categories = {}
    for item in top_10:
        pain_scores = item['product'].get('scores', {}).get('pain_type', {})
        cat = max(pain_scores.items(), key=lambda x: x[1])[0] if pain_scores else 'Other'
        categories[cat] = categories.get(cat, 0) + 1

    report.append("📊 TOP 10 BY PAIN TYPE CATEGORY:")
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        report.append(f"   • {cat.title()} support: {count} products")

    # Price distribution
    price_tiers = {}
    for item in top_10:
        tier = item['breakdown']['price']['tier']
        price_tiers[tier] = price_tiers.get(tier, 0) + 1

    report.append(f"\n💰 PRICE TIER DISTRIBUTION:")
    for tier, count in sorted(price_tiers.items(), key=lambda x: x[1], reverse=True):
        report.append(f"   • {tier.upper()}: {count} products")

    report.append(f"\n✅ RECOMMENDED ACTIONS:")
    report.append("   1. Create 3-5 Creatify video ads for TOP 5 products")
    report.append("   2. Create 2-3 carousel ads for products ranked #6-#10")
    report.append("   3. Prioritize UGC-style videos for products with high athlete/office worker scores")
    report.append("   4. Use Before/After format for products with high senior scores")
    report.append("   5. Test winter-seasonal products NOW (Dec-Feb), prepare spring products for Mar launch")

    return "\n".join(report)

def main():
    """Main analysis"""
    print("Loading product matrix...")
    products = load_product_matrix()

    print(f"Loaded {len(products)} products")

    if not products:
        print("❌ No products found in matrix")
        return

    print("Analyzing and scoring products...")
    top_10 = analyze_top_10(products)

    print(f"✅ Top 10 hero products identified\n")

    # Generate report
    report = format_top_10_report(top_10)

    # Save to file
    output_file = "TOP_10_HERO_PRODUCTS_ANALYSIS.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(report)
    print(f"\n✅ Report saved to: {output_file}")

    # Also save JSON for programmatic use
    json_output = []
    for rank, item in enumerate(top_10, 1):
        pain_scores = item['product'].get('scores', {}).get('pain_type', {})
        product_type = max(pain_scores.items(), key=lambda x: x[1])[0] if pain_scores else 'N/A'

        json_output.append({
            'rank': rank,
            'handle': item['product'].get('handle'),
            'title': item['product'].get('title'),
            'product_type': product_type + ' support',
            'price_tier': item['breakdown']['price']['tier'],
            'hero_score': round(item['hero_score'], 3),
            'breakdown': {
                'price': round(item['breakdown']['price']['score'], 3),
                'seasonality': round(item['breakdown']['seasonality']['combined'], 3),
                'demographics': round(item['breakdown']['demographics']['weighted_score'], 3),
                'ugc_trends': round(item['breakdown']['trends_2025_2026']['ugc_friendliness'], 3),
                'sales_potential': round(item['breakdown']['sales_potential']['weighted_score'], 3)
            }
        })

    with open('top_10_hero_products.json', 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2)

    print(f"✅ JSON data saved to: top_10_hero_products.json")

if __name__ == "__main__":
    main()
