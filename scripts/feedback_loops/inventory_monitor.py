#!/usr/bin/env python3
"""
FEEDBACK LOOP #2: Inventory Monitoring Script
Purpose: Monitor inventory levels, detect issues, prevent revenue loss
Stack: Shopify Admin API

Usage:
    python3 scripts/feedback_loops/inventory_monitor.py

Environment Variables Required:
    SHOPIFY_ADMIN_ACCESS_TOKEN - From .env.admin

Alerts Generated:
    - Zero inventory on active products
    - Low inventory (< 10 units)
    - Bundles with inventory issues
    - Draft products that should be active

Exit Codes:
    0 - All inventory healthy
    1 - Warnings detected (low inventory)
    2 - Critical issues (zero inventory on active products)
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Configuration
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
REPORTS_DIR = Path(__file__).parent / "reports"
LOW_INVENTORY_THRESHOLD = 10
BUNDLE_INVENTORY_MIN = 100

def load_env():
    """Load environment variables from .env.admin"""
    env_file = Path(__file__).parent.parent.parent / ".env.admin"
    env_vars = {}
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def get_all_products(headers):
    """Fetch all products from Shopify"""
    base_url = f"https://{SHOPIFY_DOMAIN}/admin/api/2025-01"
    products = []
    url = f"{base_url}/products.json?limit=250"

    while url:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200:
            print(f"  ❌ API Error: {r.status_code}")
            break

        data = r.json()
        products.extend(data.get("products", []))

        # Check for pagination
        link_header = r.headers.get("Link", "")
        if 'rel="next"' in link_header:
            # Extract next URL
            for part in link_header.split(","):
                if 'rel="next"' in part:
                    url = part.split(";")[0].strip("<>").strip()
                    break
        else:
            url = None

    return products

def analyze_inventory(products):
    """Analyze inventory and categorize issues"""
    print("\n--- INVENTORY ANALYSIS ---")

    issues = {
        "critical": [],      # Zero inventory on active products
        "warnings": [],      # Low inventory
        "bundles": [],       # Bundle-specific issues
        "draft_review": [],  # Draft products to review
    }

    stats = {
        "total_products": len(products),
        "active": 0,
        "draft": 0,
        "archived": 0,
        "bundles": 0,
        "zero_inventory": 0,
        "low_inventory": 0,
        "healthy": 0,
        # NEW: Track untracked products (dropshipped via DSers)
        "tracked_products": 0,      # Products with inventory_management="shopify"
        "untracked_products": 0,    # Products without Shopify tracking (dropship)
        "total_variants": 0,
        "tracked_variants": 0,
        "untracked_variants": 0,
    }

    for product in products:
        product_id = product.get("id")
        title = product.get("title", "Unknown")
        status = product.get("status", "unknown")
        tags = product.get("tags", "").lower()
        variants = product.get("variants", [])

        # Count by status
        if status == "active":
            stats["active"] += 1
        elif status == "draft":
            stats["draft"] += 1
        elif status == "archived":
            stats["archived"] += 1

        # Check if bundle
        is_bundle = "bundle" in title.lower() or "bundle" in tags or "kit" in title.lower()
        if is_bundle:
            stats["bundles"] += 1

        # Track if this product has ANY Shopify-tracked variants
        product_has_tracking = False

        # Analyze each variant
        for variant in variants:
            inventory_management = variant.get("inventory_management")
            inventory_quantity = variant.get("inventory_quantity", 0)
            variant_title = variant.get("title", "Default")
            stats["total_variants"] += 1

            # Track variants by management type
            if inventory_management == "shopify":
                stats["tracked_variants"] += 1
                product_has_tracking = True
            else:
                stats["untracked_variants"] += 1
                continue  # Skip untracked variants for inventory analysis

            # Check for issues
            if status == "active":
                if inventory_quantity <= 0:
                    stats["zero_inventory"] += 1
                    issue = {
                        "product_id": product_id,
                        "title": title,
                        "variant": variant_title,
                        "inventory": inventory_quantity,
                        "is_bundle": is_bundle,
                    }

                    if is_bundle:
                        issues["bundles"].append(issue)
                    else:
                        issues["critical"].append(issue)

                elif inventory_quantity < LOW_INVENTORY_THRESHOLD:
                    stats["low_inventory"] += 1
                    issues["warnings"].append({
                        "product_id": product_id,
                        "title": title,
                        "variant": variant_title,
                        "inventory": inventory_quantity,
                    })
                else:
                    stats["healthy"] += 1

            elif status == "draft":
                # Check if draft products should be active
                if inventory_quantity > 50:
                    issues["draft_review"].append({
                        "product_id": product_id,
                        "title": title,
                        "inventory": inventory_quantity,
                        "suggestion": "Has inventory, consider activating",
                    })

        # Count tracked vs untracked products
        if product_has_tracking:
            stats["tracked_products"] += 1
        else:
            stats["untracked_products"] += 1

    return issues, stats

def print_issues(issues, stats):
    """Print formatted issues report"""

    print(f"\n📊 INVENTORY STATISTICS:")
    print(f"  Total Products: {stats['total_products']}")
    print(f"  Active: {stats['active']} | Draft: {stats['draft']} | Archived: {stats['archived']}")
    print(f"  Bundles: {stats['bundles']}")

    # NEW: Clear tracking breakdown
    print(f"\n📦 INVENTORY TRACKING:")
    print(f"  Shopify-Tracked Products: {stats['tracked_products']} (inventory_management=shopify)")
    print(f"  Dropship Products (DSers): {stats['untracked_products']} (no Shopify tracking)")
    print(f"  Total Variants: {stats['total_variants']} ({stats['tracked_variants']} tracked, {stats['untracked_variants']} untracked)")

    # Tracked inventory health
    print(f"\n🏥 TRACKED INVENTORY HEALTH:")
    print(f"  Healthy (>10 units): {stats['healthy']}")
    print(f"  Low (<10 units): {stats['low_inventory']}")
    print(f"  Zero (0 units): {stats['zero_inventory']}")

    # Critical issues
    if issues["critical"]:
        print(f"\n🔴 CRITICAL - Zero Inventory Active Products ({len(issues['critical'])}):")
        for item in issues["critical"][:10]:  # Show max 10
            print(f"  ❌ [{item['product_id']}] {item['title'][:40]}... | Qty: {item['inventory']}")
        if len(issues["critical"]) > 10:
            print(f"  ... and {len(issues['critical']) - 10} more")
    else:
        print(f"\n✅ No critical inventory issues")

    # Bundle issues
    if issues["bundles"]:
        print(f"\n🟠 BUNDLE INVENTORY ISSUES ({len(issues['bundles'])}):")
        for item in issues["bundles"]:
            print(f"  ⚠️ [{item['product_id']}] {item['title'][:40]}... | Qty: {item['inventory']}")
    else:
        print(f"\n✅ All bundles have inventory")

    # Warnings
    if issues["warnings"]:
        print(f"\n🟡 LOW INVENTORY WARNINGS ({len(issues['warnings'])}):")
        for item in issues["warnings"][:5]:  # Show max 5
            print(f"  ⚠️ {item['title'][:40]}... | Qty: {item['inventory']}")
        if len(issues["warnings"]) > 5:
            print(f"  ... and {len(issues['warnings']) - 5} more")
    else:
        print(f"\n✅ No low inventory warnings")

    # Draft review
    if issues["draft_review"]:
        print(f"\n📝 DRAFT PRODUCTS TO REVIEW ({len(issues['draft_review'])}):")
        for item in issues["draft_review"][:3]:
            print(f"  📦 {item['title'][:40]}... | Qty: {item['inventory']} - {item['suggestion']}")

def generate_report(issues, stats):
    """Generate and save inventory report"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    report = {
        "timestamp": datetime.now().isoformat(),
        "store": SHOPIFY_DOMAIN,
        "statistics": stats,
        "issues": {
            "critical_count": len(issues["critical"]),
            "warning_count": len(issues["warnings"]),
            "bundle_issues_count": len(issues["bundles"]),
            "draft_review_count": len(issues["draft_review"]),
            "critical": issues["critical"],
            "bundles": issues["bundles"],
            "warnings": issues["warnings"][:20],  # Limit to 20
            "draft_review": issues["draft_review"],
        },
        "summary": {
            "status": "CRITICAL" if issues["critical"] or issues["bundles"] else ("WARNING" if issues["warnings"] else "HEALTHY"),
            "action_required": bool(issues["critical"] or issues["bundles"]),
        }
    }

    report_file = REPORTS_DIR / f"inventory_report_{timestamp}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 Report saved: {report_file}")

    return report

def main():
    print("=" * 60)
    print("FEEDBACK LOOP #2: INVENTORY MONITORING")
    print(f"Store: {SHOPIFY_DOMAIN}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Load environment
    env_vars = load_env()
    token = env_vars.get("SHOPIFY_ADMIN_ACCESS_TOKEN", "")

    if not token:
        print("❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found in .env.admin")
        return 2

    headers = {"X-Shopify-Access-Token": token, "Content-Type": "application/json"}

    # Fetch products
    print("\n📦 Fetching products...")
    products = get_all_products(headers)
    print(f"  ✅ Fetched {len(products)} products")

    # Analyze inventory
    issues, stats = analyze_inventory(products)

    # Print formatted report
    print_issues(issues, stats)

    # Generate JSON report
    report = generate_report(issues, stats)

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Status: {report['summary']['status']}")
    print(f"  Action Required: {'YES' if report['summary']['action_required'] else 'NO'}")

    # Exit code
    if report["summary"]["status"] == "CRITICAL":
        print("\n❌ CRITICAL inventory issues - immediate action required")
        return 2
    elif report["summary"]["status"] == "WARNING":
        print("\n⚠️ Inventory warnings - review recommended")
        return 1
    else:
        print("\n✅ Inventory healthy")
        return 0

if __name__ == "__main__":
    sys.exit(main())
