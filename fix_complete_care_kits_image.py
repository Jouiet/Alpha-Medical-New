#!/usr/bin/env python3
"""
Fix Complete Care Kits Collection Image
Try multiple products until we find one with an image
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2024-10'
BASE_URL = f'https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}'

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

def api_request(endpoint, method='GET', data=None):
    url = f'{BASE_URL}{endpoint}'
    try:
        response = requests.request(method, url, headers=HEADERS, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e)}

print("=" * 80)
print("FIX COMPLETE CARE KITS COLLECTION IMAGE")
print("=" * 80)

# Collection ID from previous script
collection_id = 295163035725

# Get ALL products in collection
collects_result = api_request(f'/collects.json?collection_id={collection_id}&limit=250')

if 'collects' not in collects_result:
    print("❌ Failed to fetch collects")
    exit(1)

collects = collects_result['collects']
print(f"Products in collection: {len(collects)}")

# Try each product until we find one with an image
found_image = False

for i, collect in enumerate(collects, 1):
    product_id = collect['product_id']
    print(f"\n{i}. Checking product ID: {product_id}")

    product_result = api_request(f'/products/{product_id}.json')

    if 'product' not in product_result:
        print(f"   ❌ Failed to fetch product")
        continue

    product = product_result['product']
    print(f"   Title: {product['title']}")

    if product.get('images') and len(product['images']) > 0:
        image_src = product['images'][0]['src']
        print(f"   ✅ Found image: {image_src}")

        # Update collection
        update_data = {
            'custom_collection': {
                'id': collection_id,
                'image': {
                    'src': image_src
                }
            }
        }

        update_result = api_request(
            f'/custom_collections/{collection_id}.json',
            method='PUT',
            data=update_data
        )

        if 'custom_collection' in update_result:
            print(f"\n✅ SUCCESS: Complete Care Kits collection image updated!")
            found_image = True
            break
        else:
            print(f"   ❌ Failed to update collection")
    else:
        print(f"   ⚠️  No images")

if not found_image:
    print(f"\n❌ No products with images found in this collection")

# Verify
print(f"\n{'='*80}")
print("FINAL VERIFICATION")
print(f"{'='*80}")

collections_result = api_request('/custom_collections.json')
collections = collections_result.get('custom_collections', [])
collections_no_images = [c for c in collections if not c.get('image')]

print(f"Collections without images: {len(collections_no_images)}")

if len(collections_no_images) == 0:
    print("✅ ALL COLLECTIONS NOW HAVE IMAGES!")
else:
    for c in collections_no_images:
        print(f"  - {c['title']}")

print("=" * 80)
