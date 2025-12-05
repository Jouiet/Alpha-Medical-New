#!/usr/bin/env python3
"""
AUDIT FORENSIQUE - VERIFICATION PRODUCT_TYPE FIX
Date: 2025-11-20
Purpose: Verify FACTUALLY that all 96 products now have product_type field

METHODOLOGY:
1. Fetch ALL products from Shopify Admin API (fresh data)
2. Check EACH product individually for product_type field
3. Report violations (missing or empty product_type)
4. Product-by-product listing for manual verification

NO BLIND TRUST - FACTUAL VERIFICATION ONLY
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
    print("❌ Failed to load credentials from .env.admin")
    exit(1)

SHOP = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

print("=" * 80)
print("AUDIT FORENSIQUE - VERIFICATION PRODUCT_TYPE FIX")
print("=" * 80)
print(f"Store: {SHOP}")
print(f"Date: 2025-11-20\n")

# Fetch ALL products (fresh from API - no caching)
print("=" * 80)
print("FETCHING FRESH DATA FROM SHOPIFY ADMIN API")
print("=" * 80)

all_products = []
url = f"{REST_URL}/products.json?limit=250"

while url:
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        exit(1)

    data = response.json()
    products = data.get("products", [])
    all_products.extend(products)

    # Check for pagination
    link_header = response.headers.get("Link", "")
    if 'rel="next"' in link_header:
        next_url = link_header.split('>; rel="next"')[0].split('<')[1] if '<' in link_header else None
        url = next_url if next_url else None
    else:
        url = None

print(f"✅ Fetched {len(all_products)} products from API\n")

# Audit each product
print("=" * 80)
print("AUDITING PRODUCT_TYPE FIELD (PRODUCT BY PRODUCT)")
print("=" * 80)

violations = []
valid_products = []

for i, product in enumerate(all_products, 1):
    product_id = product.get('id')
    handle = product.get('handle')
    title = product.get('title', '')
    product_type = product.get('product_type', '')

    # Check if product_type is missing or empty
    if not product_type or product_type.strip() == '':
        violations.append({
            "id": product_id,
            "handle": handle,
            "title": title[:60],
            "product_type": product_type
        })
        print(f"{i:3}. ❌ VIOLATION | {title[:60]}")
        print(f"     Handle: {handle}")
        print(f"     Product Type: '{product_type}' (EMPTY/MISSING)\n")
    else:
        valid_products.append({
            "id": product_id,
            "handle": handle,
            "title": title[:60],
            "product_type": product_type
        })

# Print valid products summary
if valid_products:
    print("\n" + "=" * 80)
    print("VALID PRODUCTS (PRODUCT-BY-PRODUCT VERIFICATION)")
    print("=" * 80)

    for i, p in enumerate(valid_products, 1):
        print(f"{i:3}. ✅ Valid ({p['product_type']:<30}) | {p['title']}")

print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print(f"Total products: {len(all_products)}")
print(f"✅ Valid (with product_type): {len(valid_products)}")
print(f"❌ Violations (missing/empty): {len(violations)}\n")

# Save results
results = {
    "timestamp": "2025-11-20",
    "store": SHOP,
    "total_products": len(all_products),
    "valid_count": len(valid_products),
    "violation_count": len(violations),
    "violations": violations,
    "valid_products": valid_products
}

with open("product_type_verification_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"📄 Full results saved to: product_type_verification_results.json\n")

# Verdict
if len(violations) == 0:
    print("=" * 80)
    print("🎉 100% SUCCESS: ALL PRODUCTS HAVE PRODUCT_TYPE!")
    print("=" * 80)
    print(f"✅ {len(all_products)}/{len(all_products)} products verified")
    print()
    exit(0)
else:
    print("=" * 80)
    print("❌ VIOLATIONS FOUND - FIX REQUIRED")
    print("=" * 80)
    print(f"❌ {len(violations)} products still missing product_type")
    print()
    print("NEXT STEPS:")
    print("1. Review violations in product_type_verification_results.json")
    print("2. Re-run fix_missing_product_types.py for failed products")
    print("3. Re-run this verification script")
    print()
    exit(1)
