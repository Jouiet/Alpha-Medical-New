#!/usr/bin/env python3
"""
UNPUBLISH BUNDLES WITHOUT IMAGES - PRE-LAUNCH FIX
Dépublie les bundles sans images pour éviter une mauvaise expérience client
Principe: Mieux pas de bundle que bundle sans image
"""

import os
import requests
import json

shop_domain = "azffej-as.myshopify.com"
access_token = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")

if not access_token:
    with open("/Users/mac/Desktop/Alpha-Medical/.env.admin", "r") as f:
        for line in f:
            if line.startswith("SHOPIFY_ADMIN_ACCESS_TOKEN="):
                access_token = line.split("=")[1].strip()
                break

headers = {"X-Shopify-Access-Token": access_token}
base_url = f"https://{shop_domain}/admin/api/2025-10"

def find_bundles_without_images():
    """Find published bundles without images"""
    url = f"{base_url}/products.json?limit=250"
    response = requests.get(url, headers=headers)
    products = response.json()["products"]

    bundles_no_images = []

    for product in products:
        if product["status"] == "active":
            is_bundle = "kit" in product["title"].lower() or "bundle" in product["title"].lower()
            has_images = len(product.get("images", [])) > 0

            if is_bundle and not has_images:
                bundles_no_images.append({
                    "id": product["id"],
                    "title": product["title"],
                    "handle": product["handle"]
                })

    return bundles_no_images

def unpublish_product(product_id, product_title):
    """Unpublish a product by setting status to draft"""
    url = f"{base_url}/products/{product_id}.json"

    payload = {
        "product": {
            "id": product_id,
            "status": "draft"
        }
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"  ✅ UNPUBLISHED: {product_title}")
        return True
    else:
        print(f"  ❌ FAILED: {product_title} - {response.status_code}")
        print(f"     Error: {response.text}")
        return False

def main():
    print("="*70)
    print("🔧 UNPUBLISH BUNDLES WITHOUT IMAGES")
    print("="*70)
    print("\nRationale: Bundles without images = BAD customer experience")
    print("Action: Set status to 'draft' until images are added")
    print("\nSearching for bundles without images...")

    bundles = find_bundles_without_images()

    if not bundles:
        print("\n✅ NO BUNDLES WITHOUT IMAGES FOUND")
        print("All published bundles have images!")
        return

    print(f"\n⚠️  FOUND {len(bundles)} PUBLISHED BUNDLES WITHOUT IMAGES:")
    for bundle in bundles:
        print(f"  - {bundle['title']} (ID: {bundle['id']})")

    print(f"\n🎯 ACTION: Unpublishing {len(bundles)} bundles...")

    success_count = 0
    for bundle in bundles:
        if unpublish_product(bundle['id'], bundle['title']):
            success_count += 1

    print(f"\n" + "="*70)
    print(f"📊 RESULTS:")
    print(f"  - Successfully unpublished: {success_count}/{len(bundles)}")
    print(f"  - Failed: {len(bundles) - success_count}/{len(bundles)}")

    if success_count == len(bundles):
        print(f"\n✅ ALL BUNDLES WITHOUT IMAGES UNPUBLISHED")
        print(f"\n🎯 NEXT STEPS:")
        print(f"  1. Create bundle images (Canva/Photoshop)")
        print(f"  2. Upload images to each bundle product")
        print(f"  3. Re-publish bundles")
    else:
        print(f"\n⚠️  SOME BUNDLES FAILED TO UNPUBLISH")
        print(f"  - Review error messages above")
        print(f"  - Retry or unpublish manually in Shopify Admin")

    print("="*70)

if __name__ == "__main__":
    main()
