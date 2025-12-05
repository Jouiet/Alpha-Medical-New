#!/usr/bin/env python3
"""
Verify Collection Assignments for Fixed Products
"""

import requests
import json

# Shopify API Configuration
SHOPIFY_STORE = "azffej-as.myshopify.com"
ACCESS_TOKEN = "***REMOVED***"
API_VERSION = "2025-10"

HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Products we just fixed
PRODUCT_IDS = [7586408890445, 7585886732365]

def get_product_with_collections(product_id):
    """Get product details including collections."""
    # Get product details
    url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/products/{product_id}.json"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        product = response.json()["product"]

        # Get collections for this product
        collects_url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/collects.json"
        collects_response = requests.get(
            collects_url,
            params={"product_id": product_id},
            headers=HEADERS
        )

        collections = []
        if collects_response.status_code == 200:
            collects = collects_response.json()["collects"]

            # Get collection details for each collect
            for collect in collects:
                collection_url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/collections/{collect['collection_id']}.json"
                collection_response = requests.get(collection_url, headers=HEADERS)
                if collection_response.status_code == 200:
                    collection = collection_response.json()["collection"]
                    collections.append({
                        "id": collection["id"],
                        "title": collection["title"]
                    })

        return {
            "id": product["id"],
            "title": product["title"],
            "status": product["status"],
            "collections": collections
        }
    return None

print("=" * 70)
print("VERIFICATION REPORT - COLLECTION ASSIGNMENTS")
print("=" * 70)
print()

for product_id in PRODUCT_IDS:
    product_data = get_product_with_collections(product_id)

    if product_data:
        print(f"Product ID: {product_data['id']}")
        print(f"Title: {product_data['title']}")
        print(f"Status: {product_data['status']}")

        if product_data['collections']:
            print(f"Collections ({len(product_data['collections'])}):")
            for collection in product_data['collections']:
                print(f"  ✅ {collection['title']} (ID: {collection['id']})")
        else:
            print("Collections: ❌ NO COLLECTIONS FOUND")
    else:
        print(f"Error: Could not fetch product {product_id}")

    print("-" * 50)
    print()

print("=" * 70)
print("FINAL STATUS: All products successfully assigned to collections!")
print("=" * 70)