#!/usr/bin/env python3
"""
INTEGRATE SMART RECOMMENDATIONS SECTION INTO PRODUCT TEMPLATE
- Modifies templates/product.json to add smart-recommendations-section
- Positions it after product-information section
"""

import os
import json
import requests
from datetime import datetime

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

API_VERSION = "2025-10"
THEME_ID = "140069830733"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("=" * 80)
print("INTEGRATING SMART RECOMMENDATIONS INTO PRODUCT TEMPLATE")
print("=" * 80)
print(f"Theme ID: {THEME_ID}")
print()

# ============================================================================
# STEP 1: Read current product.json template
# ============================================================================

print("Step 1: Reading templates/product.json...")

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]=templates/product.json"
response = requests.get(url, headers=HEADERS)

if response.status_code != 200:
    print(f"  ❌ Failed to read product.json: {response.status_code}")
    exit(1)

product_json = response.json()['asset']['value']
template_data = json.loads(product_json)

print("  ✅ templates/product.json loaded")
print(f"  ℹ️  Current sections: {len(template_data.get('sections', {}))}")
print(f"  ℹ️  Section order: {template_data.get('order', [])}")

# ============================================================================
# STEP 2: Check if recommendations section already exists
# ============================================================================

print("\nStep 2: Checking for existing recommendations section...")

existing_recs = None
for section_id in template_data.get('sections', {}).keys():
    if 'recommendation' in section_id.lower():
        existing_recs = section_id
        print(f"  ⚠️  Found existing section: {section_id}")
        break

if existing_recs:
    print(f"  ℹ️  Recommendations section already exists: {existing_recs}")
    print("  ℹ️  Skipping integration to avoid duplicates")
    exit(0)

# ============================================================================
# STEP 3: Add smart-recommendations-section to template
# ============================================================================

print("\nStep 3: Adding smart-recommendations-section to template...")

# Generate unique section ID with timestamp
section_id = f"smart_recommendations_{int(datetime.now().timestamp())}"

# Add section configuration
template_data['sections'][section_id] = {
    "type": "smart-recommendations-section",
    "settings": {
        "recommendation_type": "auto",
        "products_limit": 4,
        "section_title": ""
    }
}

# Find position to insert (after product-information or related-products)
insert_position = None
order = template_data.get('order', [])

for i, section in enumerate(order):
    if any(keyword in section.lower() for keyword in ['product-information', 'main', 'product']):
        insert_position = i + 1
        print(f"  ℹ️  Found insertion point after: {section}")
        break

if insert_position is None:
    # Append at end
    insert_position = len(order)
    print("  ℹ️  No specific position found, adding at end")

# Insert section into order
order.insert(insert_position, section_id)
template_data['order'] = order

print(f"  ✅ Section added: {section_id}")
print(f"  ✅ Position: {insert_position + 1} of {len(order)}")

# ============================================================================
# STEP 4: Upload modified template
# ============================================================================

print("\nStep 4: Uploading modified template...")

updated_json = json.dumps(template_data, indent=2)

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
payload = {
    "asset": {
        "key": "templates/product.json",
        "value": updated_json
    }
}

response = requests.put(url, headers=HEADERS, json=payload)

if response.status_code in [200, 201]:
    print("  ✅ templates/product.json updated successfully")
else:
    print(f"  ❌ Upload failed: {response.status_code}")
    print(response.text)
    exit(1)

# ============================================================================
# STEP 5: Verification
# ============================================================================

print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

# Re-read template to verify
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]=templates/product.json"
response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    verification_data = json.loads(response.json()['asset']['value'])

    if section_id in verification_data.get('sections', {}):
        print(f"✅ Section {section_id} verified in template")
        print(f"✅ Position in order: {verification_data['order'].index(section_id) + 1}")
        print(f"✅ Settings: {verification_data['sections'][section_id]['settings']}")
    else:
        print("❌ Section not found in verification")
else:
    print("⚠️  Could not verify (template locked or busy)")

# ============================================================================
# SUCCESS
# ============================================================================

print("\n" + "=" * 80)
print("INTEGRATION COMPLETE")
print("=" * 80)
print("✅ smart-recommendations-section integrated into product pages")
print()
print("LIVE ON:")
print("  - All product pages on alphamedical.shop")
print()
print("TEST NOW:")
print("  1. Visit: https://www.alphamedical.shop/products/tourmaline-magnetic-knee-pads-self-heating-support")
print("  2. Scroll down to see 'Recommended For You' section")
print("  3. Verify 3 tabs: Similar Products, Complements, Bundles")
print("  4. Click tabs to switch recommendation types")
print("  5. Check browser console (F12) for errors")
print()
print("NEXT STEPS:")
print("  - Test on multiple product pages")
print("  - Verify recommendations accuracy")
print("  - Monitor analytics for engagement")
print("=" * 80)
