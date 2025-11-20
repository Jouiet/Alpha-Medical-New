#!/usr/bin/env python3
"""
AUDIT FORENSIQUE POST-FIX - Product_type Verification
Date: 2025-11-20
Purpose: VERIFY (no blind trust) that fix_missing_product_types.py actually worked

METHODOLOGY:
1. Fresh fetch from Shopify API (no cache)
2. Check EVERY product individually
3. Report missing/empty product_type
4. Compare with claimed "78 updated"
5. Exit 0 ONLY if 100% success

NO ASSUMPTIONS - ONLY FACTS
"""

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
HEADERS = {"X-Shopify-Access-Token": TOKEN}

print("=" * 80)
print("AUDIT FORENSIQUE POST-FIX - PRODUCT_TYPE VERIFICATION")
print("=" * 80)
print("Methodology: Fresh API fetch + individual product verification")
print("Success criteria: 96/96 products have product_type (100%)")
print("=" * 80)
print()

# Fetch ALL products (fresh, no cache)
print("📥 Fetching ALL products from Shopify (fresh data)...")
all_products = []
url = f"{REST_URL}/products.json?limit=250"

while url:
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        exit(1)

    data = response.json()
    products = data.get("products", [])
    all_products.extend(products)

    # Pagination
    link_header = response.headers.get("Link", "")
    if 'rel="next"' in link_header:
        next_url = link_header.split('>; rel="next"')[0].split('<')[1]
        url = next_url
    else:
        url = None

print(f"✅ Fetched {len(all_products)} products\n")

# Forensic audit: check EACH product individually
print("=" * 80)
print("FORENSIC AUDIT - INDIVIDUAL PRODUCT VERIFICATION")
print("=" * 80)
print()

missing_product_type = []
empty_product_type = []
valid_product_type = []

for i, product in enumerate(all_products, 1):
    product_id = product.get('id')
    title = product.get('title', 'UNKNOWN')[:50]
    product_type = product.get('product_type')

    # Check if product_type is missing or empty
    if product_type is None:
        missing_product_type.append({
            'id': product_id,
            'title': title,
            'product_type': None
        })
        print(f"❌ [{i}/{len(all_products)}] {title}")
        print(f"   Product ID: {product_id}")
        print(f"   Issue: product_type = None (missing)")
        print()
    elif product_type.strip() == '':
        empty_product_type.append({
            'id': product_id,
            'title': title,
            'product_type': ''
        })
        print(f"❌ [{i}/{len(all_products)}] {title}")
        print(f"   Product ID: {product_id}")
        print(f"   Issue: product_type = '' (empty string)")
        print()
    else:
        valid_product_type.append({
            'id': product_id,
            'title': title,
            'product_type': product_type
        })

# Summary
print("=" * 80)
print("AUDIT RESULTS")
print("=" * 80)
print()

total = len(all_products)
valid = len(valid_product_type)
missing = len(missing_product_type)
empty = len(empty_product_type)
invalid = missing + empty

print(f"Total products: {total}")
print(f"✅ Valid product_type: {valid}/{total} ({valid/total*100:.1f}%)")
print(f"❌ Missing product_type: {missing}/{total}")
print(f"❌ Empty product_type: {empty}/{total}")
print(f"❌ Total invalid: {invalid}/{total}")
print()

# Detailed breakdown
if invalid > 0:
    print("=" * 80)
    print("❌ FAILED PRODUCTS (Detailed)")
    print("=" * 80)
    print()

    if missing_product_type:
        print(f"Missing product_type ({len(missing_product_type)} products):")
        for p in missing_product_type:
            print(f"  - ID {p['id']}: {p['title']}")
        print()

    if empty_product_type:
        print(f"Empty product_type ({len(empty_product_type)} products):")
        for p in empty_product_type:
            print(f"  - ID {p['id']}: {p['title']}")
        print()

    print("=" * 80)
    print("VERIFICATION RESULT: ❌ FAILED")
    print("=" * 80)
    print(f"Script claimed: 78/78 updated")
    print(f"Actual result: {invalid} products still missing product_type")
    print()
    print("ACTION REQUIRED:")
    print("1. Investigate why fix script claimed success but products still missing")
    print("2. Re-run fix script")
    print("3. Re-run this verification script")
    print()

    # Save failed products
    with open('product_type_failed_products.json', 'w') as f:
        json.dump({
            'timestamp': '2025-11-20',
            'total_products': total,
            'valid': valid,
            'missing': missing_product_type,
            'empty': empty_product_type
        }, f, indent=2)

    print("📄 Failed products saved to: product_type_failed_products.json")
    print()

    exit(1)
else:
    print("=" * 80)
    print("✅ VERIFICATION RESULT: 100% SUCCESS")
    print("=" * 80)
    print(f"✅ All {total} products have valid product_type")
    print(f"✅ Script claimed: 78/78 updated")
    print(f"✅ Forensic verification: {valid}/{total} valid (100%)")
    print()
    print("🎉 FACTUAL CONFIRMATION: fix_missing_product_types.py worked correctly")
    print()

    # Save success report
    with open('product_type_verification_success.json', 'w') as f:
        json.dump({
            'timestamp': '2025-11-20',
            'total_products': total,
            'valid_products': valid,
            'success_rate': 100.0,
            'verification_method': 'Fresh API fetch + individual product audit'
        }, f, indent=2)

    print("📄 Success report saved to: product_type_verification_success.json")
    print()

    exit(0)
