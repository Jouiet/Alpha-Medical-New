#!/usr/bin/env python3
"""
DRAFT STATUS VERIFICATION - FACTUAL API CHECK
Vérifie les items en draft pour identifier pourquoi ils sont draft
Principe: Les items draft DOIVENT rester draft (user constraint)
Objectif: Vérifier si c'est intentionnel ou si des données manquent
"""

import os
import requests
import json
from datetime import datetime

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

def get_draft_items():
    """Get all draft items via API"""
    print("\n" + "="*70)
    print("🔍 FETCHING DRAFT ITEMS")
    print("="*70)

    url = f"{base_url}/products.json?status=draft&limit=250"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        print(f"  {response.text}")
        return []

    items = response.json()["products"]
    print(f"\n✅ Found {len(items)} draft items")

    return items

def analyze_completeness(item):
    """Analyze if item has all required data"""
    analysis = {
        "id": item["id"],
        "title": item["title"],
        "handle": item["handle"],
        "created_at": item["created_at"],
        "updated_at": item["updated_at"],
        "status": item["status"],
        "issues": [],
        "warnings": [],
        "ready_to_publish": True
    }

    # Check critical fields
    if not item.get("images") or len(item["images"]) == 0:
        analysis["issues"].append("NO IMAGES")
        analysis["ready_to_publish"] = False

    if not item.get("body_html") or not item["body_html"].strip():
        analysis["issues"].append("NO DESCRIPTION")
        analysis["ready_to_publish"] = False

    if not item.get("variants") or len(item["variants"]) == 0:
        analysis["issues"].append("NO VARIANTS")
        analysis["ready_to_publish"] = False
    else:
        variant = item["variants"][0]

        if not variant.get("price") or float(variant["price"]) == 0:
            analysis["issues"].append("PRICE IS ZERO")
            analysis["ready_to_publish"] = False

        # Check inventory (bundles can have 0 inventory)
        is_bundle = "kit" in item["title"].lower() or "bundle" in item["title"].lower()
        inventory = variant.get("inventory_quantity", 0)

        if inventory == 0 and not is_bundle:
            analysis["warnings"].append("ZERO INVENTORY (not a bundle)")

        if not variant.get("sku"):
            analysis["warnings"].append("NO SKU")

    # Check item type
    if not item.get("product_type"):
        analysis["warnings"].append("NO PRODUCT TYPE")

    # Check vendor
    if not item.get("vendor"):
        analysis["warnings"].append("NO VENDOR")

    # Check tags
    if not item.get("tags"):
        analysis["warnings"].append("NO TAGS")

    return analysis

def audit_all_draft_items():
    """Audit all draft items and categorize them"""
    print("\n" + "="*70)
    print("📊 DRAFT ITEMS AUDIT")
    print("="*70)

    items = get_draft_items()

    if not items:
        print("\n✅ NO DRAFT ITEMS FOUND")
        return

    ready_to_publish = []
    needs_work = []
    bundles = []

    print("\n" + "="*70)
    print("ANALYZING EACH ITEM...")
    print("="*70)

    for item in items:
        analysis = analyze_completeness(item)

        is_bundle = "kit" in item["title"].lower() or "bundle" in item["title"].lower()

        print(f"\n{'='*70}")
        print(f"📦 {analysis['title']}")
        print(f"  ID: {analysis['id']}")
        print(f"  Handle: {analysis['handle']}")
        print(f"  Created: {analysis['created_at'][:10]}")
        print(f"  Updated: {analysis['updated_at'][:10]}")

        if is_bundle:
            print(f"  Type: BUNDLE")
            bundles.append(analysis)

        if analysis["issues"]:
            print(f"\n  ❌ ISSUES ({len(analysis['issues'])}):")
            for issue in analysis["issues"]:
                print(f"    - {issue}")
            needs_work.append(analysis)
        else:
            print(f"\n  ✅ NO CRITICAL ISSUES")

        if analysis["warnings"]:
            print(f"\n  ⚠️  WARNINGS ({len(analysis['warnings'])}):")
            for warning in analysis["warnings"]:
                print(f"    - {warning}")

        if analysis["ready_to_publish"]:
            print(f"\n  ✅ READY TO PUBLISH")
            ready_to_publish.append(analysis)
        else:
            print(f"\n  ❌ NOT READY (missing critical data)")

    # Summary
    print("\n" + "="*70)
    print("📊 AUDIT SUMMARY")
    print("="*70)

    print(f"\n📦 TOTAL DRAFT ITEMS: {len(items)}")
    print(f"  - Bundles: {len(bundles)}/{len(items)}")
    print(f"  - Non-bundles: {len(items) - len(bundles)}/{len(items)}")

    print(f"\n✅ READY TO PUBLISH: {len(ready_to_publish)}/{len(items)}")
    if ready_to_publish:
        for analysis in ready_to_publish:
            print(f"  ✓ {analysis['title']}")

    print(f"\n❌ NEEDS WORK: {len(needs_work)}/{len(items)}")
    if needs_work:
        for analysis in needs_work:
            print(f"  ✗ {analysis['title']}")
            for issue in analysis["issues"]:
                print(f"    - {issue}")

    print("\n" + "="*70)
    print("🎯 RECOMMENDATIONS")
    print("="*70)

    if len(bundles) > 0:
        print(f"\n📦 BUNDLES ({len(bundles)}):")
        print(f"  - These were unpublished because they have NO IMAGES")
        print(f"  - Action: Create bundle images (Canva/Photoshop)")
        print(f"  - Then: Upload images and re-publish")

    if len(ready_to_publish) > 0 and len(ready_to_publish) != len(bundles):
        print(f"\n✅ NON-BUNDLE ITEMS READY TO PUBLISH ({len([p for p in ready_to_publish if 'kit' not in p['title'].lower() and 'bundle' not in p['title'].lower()])}):")
        for analysis in ready_to_publish:
            if "kit" not in analysis["title"].lower() and "bundle" not in analysis["title"].lower():
                print(f"  ✓ {analysis['title']}")
        print(f"\n  ⚠️  USER CONSTRAINT: 'les produits draft DOIVENT rester Draft'")
        print(f"  → These items are draft for a reason (user decision)")
        print(f"  → DO NOT auto-publish without explicit user approval")

    if len(needs_work) > 0:
        needs_work_non_bundles = [p for p in needs_work if "kit" not in p["title"].lower() and "bundle" not in p["title"].lower()]
        if needs_work_non_bundles:
            print(f"\n❌ NON-BUNDLE ITEMS NEEDING WORK ({len(needs_work_non_bundles)}):")
            for analysis in needs_work_non_bundles:
                print(f"  ✗ {analysis['title']}")
                for issue in analysis["issues"]:
                    print(f"    - {issue}")

    print("\n" + "="*70)
    print("🚫 USER CONSTRAINT REMINDER")
    print("="*70)
    print("\n⚠️  'les produits draft DOIVENT rester Draft'")
    print("\nIMPLICATIONS:")
    print("  1. Draft items are draft for a REASON (intentional)")
    print("  2. DO NOT auto-publish without explicit user approval")
    print("  3. Audit purpose: VERIFY data completeness, NOT change status")
    print("  4. Bundles exception: Can be re-published after images added")

    return {
        "total": len(items),
        "bundles": len(bundles),
        "ready_to_publish": len(ready_to_publish),
        "needs_work": len(needs_work),
        "items": items
    }

if __name__ == "__main__":
    print("="*70)
    print("🔬 DRAFT STATUS VERIFICATION - FACTUAL CHECK")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Method: Shopify Admin API 2025-10")
    print(f"Constraint: 'les produits draft DOIVENT rester Draft' (user)")

    result = audit_all_draft_items()

    print("\n" + "="*70)
    print("✅ AUDIT COMPLETE")
    print("="*70)
