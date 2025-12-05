#!/usr/bin/env python3
"""
Fix Collections Missing Images
Session 52 - Programmatic Fix

Collections without images:
1. Complete Care Kits
2. Medical Equipment Bundles

Solution: Use representative product images from each collection
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.admin')

SHOPIFY_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'
BASE_URL = f'https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}'

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

def api_request(endpoint, method='GET', data=None):
    """Make API request"""
    url = f'{BASE_URL}{endpoint}'
    try:
        response = requests.request(method, url, headers=HEADERS, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e)}

print("=" * 80)
print("FIX COLLECTIONS MISSING IMAGES")
print("=" * 80)

# Step 1: Get all collections
collections_result = api_request('/custom_collections.json')

if 'custom_collections' not in collections_result:
    print("❌ Failed to fetch collections")
    exit(1)

collections = collections_result['custom_collections']
print(f"Total collections: {len(collections)}")

# Step 2: Find collections without images
collections_no_images = [c for c in collections if not c.get('image')]

print(f"\nCollections without images: {len(collections_no_images)}")
for c in collections_no_images:
    print(f"  - {c['title']} (ID: {c['id']})")

# Step 3: For each collection, get products and use first product image
for collection in collections_no_images:
    print(f"\n{'='*80}")
    print(f"Processing: {collection['title']}")
    print(f"{'='*80}")

    # Get collects (products in collection)
    collects_result = api_request(f'/collects.json?collection_id={collection["id"]}&limit=10')

    if 'collects' not in collects_result or not collects_result['collects']:
        print(f"⚠️  No products in collection, skipping")
        continue

    # Get first product
    product_id = collects_result['collects'][0]['product_id']
    product_result = api_request(f'/products/{product_id}.json')

    if 'product' not in product_result:
        print(f"❌ Failed to fetch product {product_id}")
        continue

    product = product_result['product']

    if not product.get('images'):
        print(f"⚠️  Product has no images, skipping")
        continue

    # Use first product image
    image_src = product['images'][0]['src']

    print(f"Using image from product: {product['title']}")
    print(f"Image URL: {image_src}")

    # Update collection with image
    update_data = {
        'custom_collection': {
            'id': collection['id'],
            'image': {
                'src': image_src
            }
        }
    }

    update_result = api_request(
        f'/custom_collections/{collection["id"]}.json',
        method='PUT',
        data=update_data
    )

    if 'custom_collection' in update_result:
        print(f"✅ Collection image updated successfully")
    else:
        print(f"❌ Failed to update collection")
        if 'error' in update_result:
            print(f"   Error: {update_result['error']}")

# Step 4: Verify
print(f"\n{'='*80}")
print("VERIFICATION")
print(f"{'='*80}")

collections_result = api_request('/custom_collections.json')
collections = collections_result.get('custom_collections', [])
collections_no_images = [c for c in collections if not c.get('image')]

print(f"Collections without images (AFTER): {len(collections_no_images)}")

if len(collections_no_images) == 0:
    print("✅ All collections now have images!")
else:
    print("⚠️  Still missing images:")
    for c in collections_no_images:
        print(f"  - {c['title']}")

print("=" * 80)
