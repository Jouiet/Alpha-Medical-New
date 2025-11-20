#!/usr/bin/env python3
"""
FIX PRODUCT_TYPE COHERENCE ISSUE
Date: 2025-11-20

ISSUE DETECTED:
"Adjustable Hunchback Orthotic Brace Back Waist Posture Corrector"
Currently: "Neck Support"
Should be: "Back & Posture Support"

This is a BACK brace, not a neck brace.
"""

import os
import requests
import json

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

SHOP = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

print("=" * 80)
print("FIX PRODUCT_TYPE COHERENCE ISSUE")
print("=" * 80)

# Find the product
print("Searching for 'Adjustable Hunchback Orthotic Brace'...\n")

response = requests.get(f"{REST_URL}/products.json?limit=250", headers=HEADERS)
if response.status_code != 200:
    print(f"❌ API Error: {response.status_code}")
    exit(1)

products = response.json().get('products', [])

# Find the specific product
target = None
for p in products:
    if 'hunchback' in p.get('title', '').lower():
        target = p
        break

if not target:
    print("❌ Product not found")
    exit(1)

print(f"✅ Found product:")
print(f"   ID: {target['id']}")
print(f"   Title: {target['title']}")
print(f"   Current product_type: '{target['product_type']}'")
print(f"   Should be: 'Back & Posture Support'\n")

# Update product_type
print("Updating product_type...\n")

update_data = {
    "product": {
        "id": target['id'],
        "product_type": "Back & Posture Support"
    }
}

update_response = requests.put(
    f"{REST_URL}/products/{target['id']}.json",
    headers=HEADERS,
    json=update_data
)

if update_response.status_code in [200, 201]:
    print("✅ SUCCESS: Product updated")
    updated_product = update_response.json().get('product', {})
    print(f"   New product_type: '{updated_product.get('product_type')}'")
    print()
    print("=" * 80)
    print("CORRECTION COMPLETE")
    print("=" * 80)
    print("Next: Re-run verify_product_type_fix.py to confirm 100% coherence")
    print()
else:
    print(f"❌ Update failed: {update_response.status_code}")
    print(f"Response: {update_response.text}")
    exit(1)
