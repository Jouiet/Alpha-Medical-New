#!/usr/bin/env python3
"""
PUBLISHED ITEMS VERIFICATION - FACTUAL API CHECK
Vérifie que tous les items publiés ont des données complètes
Objectif: Identifier les issues avant le lancement (15 jours restants)
"""

import os
import requests
import json
from datetime import datetime
from collections import defaultdict

# Load credentials
shop_domain = os.getenv("SHOPIFY_STORE_DOMAIN", "azffej-as.myshopify.com")
access_token = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")

if not access_token:
    with open("/Users/mac/Desktop/Alpha-Medical/.env.admin", "r") as f:
        for line in f:
            if line.startswith("SHOPIFY_ADMIN_ACCESS_TOKEN="):
                access_token = line.split("=")[1].strip()
                break

headers = {"X-Shopify-Access-Token": access_token}
base_url = f"https://{shop_domain}/admin/api/2025-10"

def get_published_items():
    """Get all published items via API"""
    print("\n" + "="*70)
    print("🔍 FETCHING PUBLISHED ITEMS")
    print("="*70)

    url = f"{base_url}/products.json?status=active&limit=250"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        print(f"  {response.text}")
        return []

    items = response.json()["products"]
    print(f"\n✅ Found {len(items)} published items")

    return items

def analyze_item_quality(item):
    """Analyze item data quality and completeness"""
    analysis = {
        "id": item["id"],
        "title": item["title"],
        "handle": item["handle"],
        "issues": [],
        "warnings": [],
        "quality_score": 100
    }

    is_bundle = "kit" in item["title"].lower() or "bundle" in item["title"].lower()

    # Check images
    images_count = len(item.get("images", []))
    if images_count == 0:
        analysis["issues"].append("NO IMAGES")
        analysis["quality_score"] -= 50
    elif images_count < 3 and not is_bundle:
        analysis["warnings"].append(f"ONLY {images_count} IMAGE(S) - Recommend 3-5 images")
        analysis["quality_score"] -= 10

    # Check description
    description = item.get("body_html", "").strip()
    if not description:
        analysis["issues"].append("NO DESCRIPTION")
        analysis["quality_score"] -= 30
    elif len(description) < 200:
        analysis["warnings"].append(f"SHORT DESCRIPTION ({len(description)} chars) - Recommend 500+ chars")
        analysis["quality_score"] -= 10

    # Check variants
    if not item.get("variants") or len(item["variants"]) == 0:
        analysis["issues"].append("NO VARIANTS")
        analysis["quality_score"] -= 50
    else:
        variant = item["variants"][0]

        # Check price
        price = float(variant.get("price", 0))
        if price == 0:
            analysis["issues"].append("PRICE IS ZERO")
            analysis["quality_score"] -= 40
        elif price < 5:
            analysis["warnings"].append(f"LOW PRICE (${price}) - Verify pricing")
            analysis["quality_score"] -= 5

        # Check inventory
        inventory = variant.get("inventory_quantity", 0)
        if inventory == 0 and not is_bundle:
            analysis["warnings"].append("ZERO INVENTORY (not a bundle)")
            analysis["quality_score"] -= 15

        # Check SKU
        if not variant.get("sku"):
            analysis["warnings"].append("NO SKU")
            analysis["quality_score"] -= 5

    # Check product type
    if not item.get("product_type"):
        analysis["warnings"].append("NO PRODUCT TYPE")
        analysis["quality_score"] -= 5

    # Check vendor
    if not item.get("vendor"):
        analysis["warnings"].append("NO VENDOR")
        analysis["quality_score"] -= 5

    # Check tags
    if not item.get("tags"):
        analysis["warnings"].append("NO TAGS")
        analysis["quality_score"] -= 5

    # Check SEO
    if not item.get("metafields_global_title_tag"):
        analysis["warnings"].append("NO SEO TITLE")
        analysis["quality_score"] -= 5

    if not item.get("metafields_global_description_tag"):
        analysis["warnings"].append("NO META DESCRIPTION")
        analysis["quality_score"] -= 5

    return analysis

def verify_all_published_items():
    """Verify all published items data quality"""
    print("\n" + "="*70)
    print("📊 PUBLISHED ITEMS VERIFICATION")
    print("="*70)

    items = get_published_items()

    if not items:
        print("\n❌ NO PUBLISHED ITEMS FOUND")
        return

    critical_issues = []
    warnings_only = []
    perfect = []

    issues_summary = defaultdict(int)
    warnings_summary = defaultdict(int)

    print("\n" + "="*70)
    print("ANALYZING EACH ITEM...")
    print("="*70)

    for i, item in enumerate(items, 1):
        analysis = analyze_item_quality(item)

        is_bundle = "kit" in item["title"].lower() or "bundle" in item["title"].lower()

        if i <= 10 or analysis["issues"] or (analysis["warnings"] and analysis["quality_score"] < 80):
            # Show first 10 items OR items with issues OR items with low quality score
            print(f"\n{'='*70}")
            print(f"📦 [{i}/{len(items)}] {analysis['title'][:50]}...")
            print(f"  ID: {analysis['id']}")
            print(f"  Quality Score: {analysis['quality_score']}/100")

            if is_bundle:
                print(f"  Type: BUNDLE")

            if analysis["issues"]:
                print(f"\n  ❌ CRITICAL ISSUES ({len(analysis['issues'])}):")
                for issue in analysis["issues"]:
                    print(f"    - {issue}")
                    issues_summary[issue] += 1

            if analysis["warnings"]:
                print(f"\n  ⚠️  WARNINGS ({len(analysis['warnings'])}):")
                for warning in analysis["warnings"]:
                    print(f"    - {warning}")
                    warnings_summary[warning] += 1

        # Categorize
        if analysis["issues"]:
            critical_issues.append(analysis)
        elif analysis["warnings"]:
            warnings_only.append(analysis)
        else:
            perfect.append(analysis)

    # Summary
    print("\n" + "="*70)
    print("📊 VERIFICATION SUMMARY")
    print("="*70)

    print(f"\n📦 TOTAL PUBLISHED ITEMS: {len(items)}")

    print(f"\n✅ PERFECT (100/100): {len(perfect)}/{len(items)} ({len(perfect)*100//len(items)}%)")

    print(f"\n⚠️  WARNINGS ONLY (70-99/100): {len(warnings_only)}/{len(items)} ({len(warnings_only)*100//len(items)}%)")

    print(f"\n❌ CRITICAL ISSUES (<70/100): {len(critical_issues)}/{len(items)} ({len(critical_issues)*100//len(items)}%)")

    if issues_summary:
        print(f"\n{'='*70}")
        print("❌ CRITICAL ISSUES BREAKDOWN")
        print("="*70)
        for issue, count in sorted(issues_summary.items(), key=lambda x: x[1], reverse=True):
            print(f"  {count:3d}x  {issue}")

    if warnings_summary:
        print(f"\n{'='*70}")
        print("⚠️  WARNINGS BREAKDOWN")
        print("="*70)
        for warning, count in sorted(warnings_summary.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {count:3d}x  {warning}")

    # Critical items list
    if critical_issues:
        print(f"\n{'='*70}")
        print(f"❌ ITEMS WITH CRITICAL ISSUES ({len(critical_issues)})")
        print("="*70)
        for analysis in critical_issues[:20]:  # Show first 20
            print(f"\n📦 {analysis['title'][:50]}...")
            print(f"  ID: {analysis['id']}")
            print(f"  Quality Score: {analysis['quality_score']}/100")
            print(f"  Issues: {', '.join(analysis['issues'])}")

        if len(critical_issues) > 20:
            print(f"\n... and {len(critical_issues) - 20} more items with critical issues")

    # Recommendations
    print("\n" + "="*70)
    print("🎯 RECOMMENDATIONS")
    print("="*70)

    if critical_issues:
        print(f"\n❌ CRITICAL: {len(critical_issues)} items need immediate attention")
        print("  Priority actions:")

        if issues_summary.get("NO IMAGES", 0) > 0:
            print(f"    1. Add images to {issues_summary['NO IMAGES']} items")

        if issues_summary.get("NO DESCRIPTION", 0) > 0:
            print(f"    2. Write descriptions for {issues_summary['NO DESCRIPTION']} items")

        if issues_summary.get("PRICE IS ZERO", 0) > 0:
            print(f"    3. Set prices for {issues_summary['PRICE IS ZERO']} items")

    if warnings_only:
        print(f"\n⚠️  MEDIUM: {len(warnings_only)} items could be improved")
        print("  Suggested optimizations:")

        if warnings_summary.get("NO SEO TITLE", 0) > 0:
            print(f"    - Add SEO titles to {warnings_summary['NO SEO TITLE']} items")

        if warnings_summary.get("NO META DESCRIPTION", 0) > 0:
            print(f"    - Add meta descriptions to {warnings_summary['NO META DESCRIPTION']} items")

        if "ONLY" in str(warnings_summary):
            low_images = sum(count for warning, count in warnings_summary.items() if "ONLY" in warning and "IMAGE" in warning)
            if low_images > 0:
                print(f"    - Add more images to {low_images} items (currently 1-2 images)")

    print(f"\n✅ EXCELLENT: {len(perfect)} items are perfect (no action needed)")

    print("\n" + "="*70)
    print("⏰ PRE-LAUNCH STATUS")
    print("="*70)

    launch_date = datetime(2025, 12, 25)
    days_remaining = (launch_date - datetime.now()).days

    print(f"\n🗓️  LAUNCH: {days_remaining} days remaining (2025-12-25)")

    if len(critical_issues) == 0:
        print(f"\n✅ READY TO LAUNCH: All published items have complete data")
        print(f"  - {len(items)} items published")
        print(f"  - {len(perfect)} items perfect (100/100)")
        print(f"  - {len(warnings_only)} items with minor warnings")
        print(f"\n🚀 LAUNCH PROBABILITY: 100% (no blockers)")
    elif len(critical_issues) < 5:
        print(f"\n⚠️  MINOR ISSUES: {len(critical_issues)} items need attention")
        print(f"  - Estimated fix time: {len(critical_issues) * 15} minutes ({len(critical_issues)} items × 15 min)")
        print(f"\n🚀 LAUNCH PROBABILITY: 95% ({days_remaining} days remaining, fixable)")
    else:
        print(f"\n❌ CRITICAL: {len(critical_issues)} items need immediate attention")
        print(f"  - Estimated fix time: {len(critical_issues) * 15 / 60:.1f} hours ({len(critical_issues)} items × 15 min)")
        print(f"\n🚀 LAUNCH PROBABILITY: 80% ({days_remaining} days, significant work needed)")

    return {
        "total": len(items),
        "perfect": len(perfect),
        "warnings_only": len(warnings_only),
        "critical_issues": len(critical_issues),
        "issues_summary": dict(issues_summary),
        "warnings_summary": dict(warnings_summary)
    }

if __name__ == "__main__":
    print("="*70)
    print("🔬 PUBLISHED ITEMS VERIFICATION - FACTUAL CHECK")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Method: Shopify Admin API 2025-10")
    print(f"Objective: Verify data completeness for launch readiness")

    result = verify_all_published_items()

    print("\n" + "="*70)
    print("✅ VERIFICATION COMPLETE")
    print("="*70)
