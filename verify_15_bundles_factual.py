#!/usr/bin/env python3
"""
VERIFICATION FACTUELLE - 15 BUNDLES DANS SHOPIFY
Audit rigoureux pour confirmer que TOUS les 15 bundles existent
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
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def rest_request(method, endpoint):
    """Execute REST API request"""
    url = f"{REST_URL}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}")
            return None
        return response.json() if response.text else {}
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

print("="*80)
print("VERIFICATION FACTUELLE - 15 BUNDLES ALPHA MEDICAL")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# Get collection
print("\n1. Fetching 'Medical Equipment Bundles' collection...")
collections = rest_request("GET", "/custom_collections.json")
bundle_collection = None

if collections and 'custom_collections' in collections:
    for coll in collections['custom_collections']:
        if coll['handle'] == 'medical-equipment-bundles':
            bundle_collection = coll
            print(f"✅ Collection found: {coll['title']} (ID: {coll['id']})")
            break

if not bundle_collection:
    print("❌ Collection NOT FOUND")
    exit(1)

# Get all products in collection
print("\n2. Fetching all products in collection...")
collects = rest_request("GET", f"/collects.json?collection_id={bundle_collection['id']}&limit=250")

if not collects or 'collects' not in collects:
    print("❌ Failed to fetch collects")
    exit(1)

product_ids = [c['product_id'] for c in collects['collects']]
print(f"✅ Found {len(product_ids)} products in collection")

# Get details for each product
print("\n3. Fetching product details...")
bundles = []

for i, product_id in enumerate(product_ids, 1):
    product_data = rest_request("GET", f"/products/{product_id}.json")
    if product_data and 'product' in product_data:
        product = product_data['product']
        variant = product['variants'][0]

        bundles.append({
            "id": product['id'],
            "title": product['title'],
            "handle": product['handle'],
            "price": variant['price'],
            "compare_at_price": variant['compare_at_price'],
            "savings": float(variant['compare_at_price']) - float(variant['price']),
            "discount_pct": ((float(variant['compare_at_price']) - float(variant['price'])) / float(variant['compare_at_price']) * 100),
            "tags": product['tags'],
            "published": product['published_at'] is not None
        })

        print(f"   [{i}/{len(product_ids)}] ✅ {product['title'][:70]}")
    else:
        print(f"   [{i}/{len(product_ids)}] ❌ Failed to fetch product {product_id}")

# FACTUAL VERIFICATION
print("\n" + "="*80)
print("FACTUAL VERIFICATION RESULTS")
print("="*80)

print(f"\n📊 TOTAL BUNDLES: {len(bundles)}/15")

if len(bundles) == 15:
    print("✅ ALL 15 BUNDLES EXIST IN SHOPIFY")
else:
    print(f"❌ MISSING {15 - len(bundles)} BUNDLES")

# Verify 35% discount
print("\n🔍 DISCOUNT VERIFICATION:")
all_35_percent = True
for bundle in bundles:
    if abs(bundle['discount_pct'] - 35.0) > 0.5:  # Allow 0.5% tolerance for rounding
        print(f"   ❌ {bundle['title'][:60]}: {bundle['discount_pct']:.2f}% (NOT 35%)")
        all_35_percent = False

if all_35_percent:
    print("   ✅ All bundles have 35% discount (within tolerance)")
else:
    print("   ❌ Some bundles do NOT have 35% discount")

# Verify published status
print("\n📢 PUBLISHED STATUS:")
unpublished = [b for b in bundles if not b['published']]
if unpublished:
    print(f"   ❌ {len(unpublished)} bundles are UNPUBLISHED:")
    for b in unpublished:
        print(f"      - {b['title']}")
else:
    print("   ✅ All bundles are PUBLISHED")

# Sort by price
bundles_sorted = sorted(bundles, key=lambda x: float(x['price']))

# Display all bundles
print("\n" + "="*80)
print("ALL 15 BUNDLES (sorted by price)")
print("="*80)

for i, bundle in enumerate(bundles_sorted, 1):
    print(f"\n{i}. {bundle['title']}")
    print(f"   ID: {bundle['id']}")
    print(f"   Price: ${bundle['price']} (was ${bundle['compare_at_price']})")
    print(f"   Savings: ${bundle['savings']:.2f} ({bundle['discount_pct']:.1f}%)")
    print(f"   Handle: {bundle['handle']}")
    print(f"   Tags: {bundle['tags'][:80]}...")

# Calculate totals
total_regular = sum(float(b['compare_at_price']) for b in bundles)
total_bundle = sum(float(b['price']) for b in bundles)
total_savings = total_regular - total_bundle

print("\n" + "="*80)
print("FINANCIAL SUMMARY")
print("="*80)
print(f"\nTotal Regular Price: ${total_regular:.2f}")
print(f"Total Bundle Price: ${total_bundle:.2f}")
print(f"Total Savings: ${total_savings:.2f} ({(total_savings/total_regular*100):.1f}%)")
print(f"Average Bundle Price: ${total_bundle/len(bundles):.2f}")

print("\n📋 REVENUE PROJECTIONS:")
print(f"   Monthly (100 bundles): ${(total_bundle/len(bundles))*100:.2f}")
print(f"   Annual (1200 bundles): ${(total_bundle/len(bundles))*1200:.2f}")

# Save results
output_file = "bundles_verification_results.json"
with open(output_file, 'w') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "collection_id": bundle_collection['id'],
        "total_bundles": len(bundles),
        "expected_bundles": 15,
        "verification_passed": len(bundles) == 15 and all_35_percent and not unpublished,
        "total_regular_price": total_regular,
        "total_bundle_price": total_bundle,
        "total_savings": total_savings,
        "bundles": bundles
    }, f, indent=2)

print(f"\n✅ Results saved to: {output_file}")

# Final verdict
print("\n" + "="*80)
print("FINAL VERDICT")
print("="*80)

if len(bundles) == 15 and all_35_percent and not unpublished:
    print("\n✅ ✅ ✅ VERIFICATION PASSED ✅ ✅ ✅")
    print("   - 15/15 bundles exist")
    print("   - All have 35% discount")
    print("   - All are published")
    print("\n🎯 READY FOR PRODUCTION")
else:
    print("\n❌ ❌ ❌ VERIFICATION FAILED ❌ ❌ ❌")
    if len(bundles) != 15:
        print(f"   - Missing {15 - len(bundles)} bundles")
    if not all_35_percent:
        print("   - Discount issues detected")
    if unpublished:
        print(f"   - {len(unpublished)} bundles unpublished")
    print("\n⚠️  REQUIRES ATTENTION")

print("\n" + "="*80)
