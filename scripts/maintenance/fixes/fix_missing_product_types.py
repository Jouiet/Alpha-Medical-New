#!/usr/bin/env python3
"""
FIX MISSING PRODUCT_TYPE - Critical for Google Merchant Center
73.3% of products are missing product_type field
"""

import os
import requests
import json

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": SHOPIFY_TOKEN, "Content-Type": "application/json"}

print("═══════════════════════════════════════════════════════════════")
print("🔧 FIX MISSING PRODUCT_TYPE FIELDS")
print("═══════════════════════════════════════════════════════════════\n")

# Fetch products from Shopify Admin API
print("📥 Fetching products from Shopify Admin API...")
products_response = requests.get(f"{REST_URL}/products.json?limit=250", headers=HEADERS)

if products_response.status_code != 200:
    print(f"❌ API Error: {products_response.status_code}")
    exit(1)

products = products_response.json().get('products', [])
print(f"✅ Fetched {len(products)} products\n")

# Find products missing product_type
missing_type = []
for product in products:
    if not product.get('product_type') or product.get('product_type').strip() == '':
        missing_type.append(product)

print(f"❌ Found {len(missing_type)} products without product_type\n")

if len(missing_type) == 0:
    print("✅ All products have product_type - nothing to fix!")
    exit(0)

# Infer product_type from title/tags
def infer_product_type(product):
    """Infer product type from title, tags, and vendor"""
    title = product.get('title', '').lower()
    tags = ' '.join(product.get('tags', [])).lower()
    combined = f"{title} {tags}"

    # Bundles
    if 'bundle' in combined:
        return "Medical Equipment Bundle"

    # Specific categories
    if any(word in combined for word in ['bunion', 'toe separator', 'foot']):
        return "Foot Care & Orthotics"
    elif any(word in combined for word in ['cupping', 'massage', 'therapy']):
        return "Therapeutic Devices"
    elif any(word in combined for word in ['neck', 'cervical', 'pillow']):
        return "Neck Support"
    elif any(word in combined for word in ['knee', 'joint', 'brace']):
        return "Joint Support"
    elif any(word in combined for word in ['back', 'posture', 'lumbar']):
        return "Back & Posture Support"
    elif any(word in combined for word in ['shoulder', 'arm']):
        return "Shoulder & Arm Support"
    elif any(word in combined for word in ['pain relief', 'led', 'red light']):
        return "Pain Relief Devices"
    else:
        # Default fallback
        return "Medical Equipment"

# Update products
print("🔧 Updating products with inferred product_type...\n")
updated_count = 0
failed_count = 0

for product in missing_type:
    product_id = product['id']
    inferred_type = infer_product_type(product)

    print(f"   Product: {product['title'][:50]}")
    print(f"   Inferred type: {inferred_type}")

    # Update via API
    update_data = {
        "product": {
            "id": product_id,
            "product_type": inferred_type
        }
    }

    update_response = requests.put(
        f"{REST_URL}/products/{product_id}.json",
        headers=HEADERS,
        json=update_data
    )

    if update_response.status_code in [200, 201]:
        print(f"   ✅ Updated\n")
        updated_count += 1
    else:
        print(f"   ❌ Failed: {update_response.status_code}")
        print(f"   {update_response.text[:200]}\n")
        failed_count += 1

print("═══════════════════════════════════════════════════════════════")
print("📊 UPDATE SUMMARY")
print("═══════════════════════════════════════════════════════════════\n")

print(f"✅ Updated: {updated_count}/{len(missing_type)}")
print(f"❌ Failed: {failed_count}/{len(missing_type)}")
print()

if updated_count == len(missing_type):
    print("🎉 SUCCESS: All products now have product_type!")
    print("\n🔍 Next: Rerun verification to confirm\n")
    exit(0)
else:
    print(f"⚠️  PARTIAL SUCCESS: {failed_count} products still need manual review\n")
    exit(1)
