#!/usr/bin/env python3
"""
Verify that all 19 products are now in the correct collections
"""

import requests
import time
import json

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

# Expected state after fix
EXPECTED_STATE = {
    "Group 1 - Neck Support (Should be in Pain Relief & Recovery)": [
        7585886961741, 7585887027277, 7586409480269, 7585887223885,
        7586409873485, 7586410233933, 7585939849293, 7585939488845
    ],
    "Group 2 - Therapeutic Devices (Should be in Therapy & Wellness)": [
        7586399191117, 7586408857677, 7586409054285, 7586409087053,
        7586409906253, 7585887256653, 7585887158349, 7586409218125,
        7586410266701, 7586408988749, 7586410758221
    ]
}

EXPECTED_COLLECTIONS = {
    "Group 1 - Neck Support (Should be in Pain Relief & Recovery)": "Pain Relief & Recovery",
    "Group 2 - Therapeutic Devices (Should be in Therapy & Wellness)": "Therapy & Wellness"
}


def get_product_info(product_id):
    """Get product title"""
    url = f"{SHOP_URL}/admin/api/{API_VERSION}/products/{product_id}.json"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['product']['title']
    except:
        return "Unknown Product"


def get_product_collections(product_id):
    """Get all collections for a product"""
    url = f"{SHOP_URL}/admin/api/{API_VERSION}/collects.json?product_id={product_id}"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        collects = response.json().get('collects', [])

        collection_names = []
        for collect in collects:
            for name, cid in COLLECTIONS.items():
                if cid == collect['collection_id']:
                    collection_names.append(name)
                    break

        return collection_names
    except Exception as e:
        print(f"Error getting collections for product {product_id}: {e}")
        return []


def main():
    print("=" * 80)
    print("VERIFICATION REPORT - COLLECTION FIXES")
    print("=" * 80)
    print("\nVerifying all 19 products are in correct collections...\n")

    total_verified = 0
    total_correct = 0
    issues = []

    for group_name, product_ids in EXPECTED_STATE.items():
        expected_collection = EXPECTED_COLLECTIONS[group_name]
        print(f"\n{group_name}")
        print("-" * 60)

        for product_id in product_ids:
            time.sleep(0.3)  # Rate limiting
            product_title = get_product_info(product_id)
            collections = get_product_collections(product_id)

            total_verified += 1
            status = "❌"

            if expected_collection in collections:
                # Check that no other category collections are present
                category_collections = [c for c in collections
                                       if c in ["Pain Relief & Recovery", "Posture & Support", "Therapy & Wellness"]]

                if len(category_collections) == 1 and category_collections[0] == expected_collection:
                    status = "✅"
                    total_correct += 1
                else:
                    status = "⚠️"
                    issues.append(f"Product {product_id}: Multiple category collections: {category_collections}")
            else:
                issues.append(f"Product {product_id}: Not in {expected_collection}")

            print(f"{status} {product_id}: {product_title[:50]}")
            print(f"   Collections: {', '.join(collections)}")

    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"\nProducts Verified: {total_verified}")
    print(f"Correctly Placed: {total_correct}/{total_verified}")

    if total_correct == total_verified:
        print("\n✅ SUCCESS: All 19 products are in their correct collections!")
    else:
        print(f"\n⚠️ WARNING: {total_verified - total_correct} products have issues:")
        for issue in issues:
            print(f"  - {issue}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()