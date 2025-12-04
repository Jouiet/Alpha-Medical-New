#!/usr/bin/env python3
"""
Fix 19 misplaced products in Alpha Medical Shopify collections
Based on forensic audit results from 2025-12-01
"""

import requests
import time
import json
from typing import List, Dict, Optional

# Shopify credentials
SHOP_URL = "https://azffej-as.myshopify.com"
ACCESS_TOKEN = "***REMOVED***"
API_VERSION = "2024-10"

# Headers for API requests
headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Collection IDs (verified)
COLLECTIONS = {
    "Pain Relief & Recovery": 295060439117,
    "Posture & Support": 295060471885,
    "Therapy & Wellness": 295060504653,
    "Complete Care Kits": 295163035725,
    "Medical Equipment Bundles": 296239169613,
    "New Arrivals": 295064764493,
    "Bestsellers": 295064666189
}

# Products to fix - organized by target collection
FIXES_NEEDED = {
    "GROUP 1: Neck Support → Pain Relief & Recovery": {
        "target_collection_id": COLLECTIONS["Pain Relief & Recovery"],
        "target_collection_name": "Pain Relief & Recovery",
        "products": [
            {"id": 7585886961741, "current": ["Posture & Support"]},
            {"id": 7585887027277, "current": ["Posture & Support"]},
            {"id": 7586409480269, "current": ["Therapy & Wellness"]},
            {"id": 7585887223885, "current": ["Posture & Support"]},
            {"id": 7586409873485, "current": ["New Arrivals", "Therapy & Wellness"]},
            {"id": 7586410233933, "current": ["Therapy & Wellness"]},
            {"id": 7585939849293, "current": ["Posture & Support"]},
            {"id": 7585939488845, "current": ["Posture & Support"]}
        ]
    },
    "GROUP 2: Therapeutic Devices → Therapy & Wellness": {
        "target_collection_id": COLLECTIONS["Therapy & Wellness"],
        "target_collection_name": "Therapy & Wellness",
        "products": [
            {"id": 7586399191117, "current": ["New Arrivals", "Pain Relief & Recovery"]},
            {"id": 7586408857677, "current": ["Pain Relief & Recovery", "New Arrivals"]},
            {"id": 7586409054285, "current": ["Pain Relief & Recovery"]},
            {"id": 7586409087053, "current": ["New Arrivals"]},
            {"id": 7586409906253, "current": ["Pain Relief & Recovery", "New Arrivals"]},
            {"id": 7585887256653, "current": ["Pain Relief & Recovery"]},
            {"id": 7585887158349, "current": ["Pain Relief & Recovery", "New Arrivals"]},
            {"id": 7586409218125, "current": ["New Arrivals", "Pain Relief & Recovery"]},
            {"id": 7586410266701, "current": ["Bestsellers", "Pain Relief & Recovery"]},
            {"id": 7586408988749, "current": ["New Arrivals", "Posture & Support"]},
            {"id": 7586410758221, "current": ["Pain Relief & Recovery", "Bestsellers"]}
        ]
    }
}

# Collections to preserve (promotional)
PROMOTIONAL_COLLECTIONS = ["New Arrivals", "Bestsellers"]

# Collections that are category-based (only one should be assigned)
CATEGORY_COLLECTIONS = ["Pain Relief & Recovery", "Posture & Support", "Therapy & Wellness"]


def get_product_collects(product_id: int) -> List[Dict]:
    """Get all collects for a specific product"""
    url = f"{SHOP_URL}/admin/api/{API_VERSION}/collects.json?product_id={product_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('collects', [])
    except Exception as e:
        print(f"  ⚠️ Error getting collects for product {product_id}: {e}")
        return []


def delete_collect(collect_id: int) -> bool:
    """Delete a specific collect"""
    url = f"{SHOP_URL}/admin/api/{API_VERSION}/collects/{collect_id}.json"

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code == 404:
            print(f"    ℹ️ Collect {collect_id} already removed")
            return True
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"    ❌ Error deleting collect {collect_id}: {e}")
        return False


def create_collect(product_id: int, collection_id: int) -> bool:
    """Create a new collect (add product to collection)"""
    url = f"{SHOP_URL}/admin/api/{API_VERSION}/collects.json"

    data = {
        "collect": {
            "product_id": product_id,
            "collection_id": collection_id
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 422:
            # Already exists - that's okay
            return True
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"    ❌ Error creating collect: {e}")
        return False


def get_collection_name(collection_id: int) -> str:
    """Get collection name from ID"""
    for name, cid in COLLECTIONS.items():
        if cid == collection_id:
            return name
    return f"Unknown ({collection_id})"


def fix_product_collections(product_id: int, target_collection_id: int, target_name: str, current_collections: List[str]) -> Dict:
    """Fix collections for a single product"""
    result = {
        "product_id": product_id,
        "success": False,
        "changes": [],
        "errors": []
    }

    print(f"\n  Product {product_id}:")
    print(f"    Current: {', '.join(current_collections)}")
    print(f"    Target: {target_name}")

    # Step 1: Get current collects
    collects = get_product_collects(product_id)
    time.sleep(0.5)  # Rate limiting

    if not collects:
        print(f"    ⚠️ No collects found")

    # Map collection IDs to names for easier processing
    collect_map = {}
    for collect in collects:
        collection_name = get_collection_name(collect['collection_id'])
        collect_map[collect['id']] = {
            'collection_id': collect['collection_id'],
            'collection_name': collection_name
        }

    # Step 2: Identify collects to delete (wrong category collections)
    collects_to_delete = []
    already_in_target = False

    for collect_id, info in collect_map.items():
        collection_name = info['collection_name']

        # Check if already in target collection
        if info['collection_id'] == target_collection_id:
            already_in_target = True
            print(f"    ✓ Already in {target_name}")
            continue

        # Delete if it's a wrong category collection
        if collection_name in CATEGORY_COLLECTIONS:
            collects_to_delete.append((collect_id, collection_name))

    # Step 3: Delete incorrect collects
    for collect_id, collection_name in collects_to_delete:
        print(f"    Removing from: {collection_name}")
        if delete_collect(collect_id):
            result["changes"].append(f"Removed from {collection_name}")
            time.sleep(0.5)  # Rate limiting
        else:
            result["errors"].append(f"Failed to remove from {collection_name}")

    # Step 4: Add to correct collection if not already there
    if not already_in_target:
        print(f"    Adding to: {target_name}")
        if create_collect(product_id, target_collection_id):
            result["changes"].append(f"Added to {target_name}")
            time.sleep(0.5)  # Rate limiting
        else:
            result["errors"].append(f"Failed to add to {target_name}")

    # Step 5: Verify final state
    final_collects = get_product_collects(product_id)
    time.sleep(0.5)  # Rate limiting

    final_collections = [get_collection_name(c['collection_id']) for c in final_collects]
    print(f"    Final: {', '.join(final_collections)}")

    # Check if product is now in correct collection
    if target_collection_id in [c['collection_id'] for c in final_collects]:
        # Check if no other category collections are assigned
        other_category_collections = [c for c in final_collections
                                     if c in CATEGORY_COLLECTIONS and c != target_name]
        if not other_category_collections:
            result["success"] = True
            print(f"    ✅ Successfully fixed!")
        else:
            result["errors"].append(f"Still in wrong category collections: {other_category_collections}")
            print(f"    ⚠️ Partially fixed - still in: {other_category_collections}")
    else:
        result["errors"].append("Not in target collection after fix")
        print(f"    ❌ Failed - not in target collection")

    return result


def main():
    """Main execution"""
    print("=" * 80)
    print("ALPHA MEDICAL COLLECTION FIX SCRIPT")
    print("Fixing 19 products with incorrect collection assignments")
    print("=" * 80)

    total_products = 0
    successful_fixes = 0
    all_results = {}

    # Process each group
    for group_name, group_data in FIXES_NEEDED.items():
        print(f"\n{group_name}")
        print("-" * 60)

        target_collection_id = group_data["target_collection_id"]
        target_collection_name = group_data["target_collection_name"]
        group_results = []

        for product in group_data["products"]:
            product_id = product["id"]
            current_collections = product["current"]

            result = fix_product_collections(
                product_id,
                target_collection_id,
                target_collection_name,
                current_collections
            )

            group_results.append(result)
            total_products += 1
            if result["success"]:
                successful_fixes += 1

        all_results[group_name] = group_results

    # Print summary
    print("\n" + "=" * 80)
    print("FINAL REPORT")
    print("=" * 80)

    if successful_fixes == total_products:
        print(f"✅ SCRIPT RESULT: SUCCESS")
    else:
        print(f"⚠️ SCRIPT RESULT: PARTIAL SUCCESS")

    print(f"Products Fixed: {successful_fixes}/{total_products}")

    # Detailed results by group
    for group_name, results in all_results.items():
        print(f"\n{group_name}:")
        for result in results:
            status = "✅" if result["success"] else "❌"
            product_id = result["product_id"]
            changes = ", ".join(result["changes"]) if result["changes"] else "No changes"
            print(f"  Product {product_id}: {status} {changes}")
            if result["errors"]:
                for error in result["errors"]:
                    print(f"    ⚠️ {error}")

    print("\n" + "=" * 80)
    print(f"Final Verification: {successful_fixes} of {total_products} products now in correct collections")

    if successful_fixes < total_products:
        print(f"\n⚠️ {total_products - successful_fixes} products still need manual review")
    else:
        print("\n✅ All 19 products successfully fixed!")

    print("=" * 80)


if __name__ == "__main__":
    main()