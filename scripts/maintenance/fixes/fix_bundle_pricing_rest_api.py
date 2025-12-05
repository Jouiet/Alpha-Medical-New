#!/usr/bin/env python3
"""
FIX BUNDLE PRICING TO 35% - REST API - Alpha Medical Care
Update all bundle prices to 35% of compare_at_price (65% discount)

REQUIREMENT: "Bundles 35% du prix fournisseur (35% du chiffre compare at price)"
METHOD: REST API (more reliable for variant updates)
"""

import requests
import json
from datetime import datetime

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
REST_HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("=" * 80)
print("FIX BUNDLE PRICING TO 35% (REST API) - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# Load bundles
with open('bundle_products_created.json', 'r') as f:
    bundles_created = json.load(f)

with open('optimal_bundles_plan.json', 'r') as f:
    bundles_plan = json.load(f)

# Map bundle names to plans
plans_map = {b['name']: b for b in bundles_plan['bundles']}

print(f"\nProcessing {len(bundles_created['created_bundles'])} bundles...")
print(f"Target: 35% of compare_at_price (65% discount)\n")

updated_count = 0
failed_count = 0

for bundle_created in bundles_created['created_bundles']:
    bundle_name = bundle_created['name']
    bundle_id_gid = bundle_created['id']

    # Extract numeric ID from GID
    product_id = bundle_id_gid.split('/')[-1]

    # Find plan
    plan = plans_map.get(bundle_name)
    if not plan:
        print(f"\n⚠️  No plan found for: {bundle_name}")
        continue

    # Calculate new price (35% of total)
    total_price = plan['total_price']
    new_bundle_price = round(total_price * 0.35, 2)  # 35% of total
    old_bundle_price = plan['bundle_price']

    print(f"\n{'='*80}")
    print(f"Bundle: {bundle_name}")
    print(f"{'='*80}")
    print(f"   Product ID: {product_id}")
    print(f"   Compare At Price (Total): ${total_price:.2f}")
    print(f"   OLD Price: ${old_bundle_price:.2f} (85% of total, 15% discount)")
    print(f"   NEW Price: ${new_bundle_price:.2f} (35% of total, 65% discount)")
    print(f"   Price Reduction: ${old_bundle_price - new_bundle_price:.2f}")

    # Fetch product variants via REST
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/products/{product_id}/variants.json"
    response = requests.get(url, headers=REST_HEADERS)

    if response.status_code != 200:
        print(f"   ❌ Failed to fetch variants: {response.status_code}")
        print(f"      Response: {response.text[:200]}")
        failed_count += 1
        continue

    variants = response.json().get('variants', [])

    if not variants:
        print(f"   ❌ No variants found")
        failed_count += 1
        continue

    # Get first variant (bundles have 1 variant)
    variant = variants[0]
    variant_id = variant['id']
    current_price = float(variant['price'])
    current_compare_at = variant.get('compare_at_price')

    print(f"\n   Variant ID: {variant_id}")
    print(f"   Current Price: ${current_price}")
    print(f"   Current Compare At: ${current_compare_at if current_compare_at else 'None'}")

    # Update variant via REST
    update_url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/variants/{variant_id}.json"
    update_payload = {
        "variant": {
            "id": variant_id,
            "price": str(new_bundle_price),
            "compare_at_price": str(total_price)
        }
    }

    print(f"\n   Updating variant via REST API...")
    print(f"      New Price: ${new_bundle_price}")
    print(f"      New Compare At: ${total_price:.2f}")

    update_response = requests.put(update_url, json=update_payload, headers=REST_HEADERS)

    if update_response.status_code == 200:
        updated_variant = update_response.json()['variant']
        print(f"   ✅ SUCCESS")
        print(f"      Final Price: ${updated_variant['price']}")
        print(f"      Final Compare At: ${updated_variant['compare_at_price']}")
        updated_count += 1
    else:
        print(f"   ❌ Update failed: {update_response.status_code}")
        print(f"      Response: {update_response.text[:300]}")
        failed_count += 1

# Summary
print("\n" + "=" * 80)
print("FINAL SUMMARY")
print("=" * 80)
print(f"\n✅ Successfully updated: {updated_count}/{len(bundles_created['created_bundles'])} bundles")
if failed_count > 0:
    print(f"❌ Failed: {failed_count} bundles")

# Calculate revenue impact
if updated_count > 0:
    old_total = sum([p['bundle_price'] for p in bundles_plan['bundles']])
    new_total = sum([p['total_price'] * 0.35 for p in bundles_plan['bundles']])

    print(f"\n📊 FINANCIAL IMPACT:")
    print(f"   OLD Total Bundle Revenue: ${old_total:.2f} (85% pricing)")
    print(f"   NEW Total Bundle Revenue: ${new_total:.2f} (35% pricing)")
    print(f"   Revenue Change: ${new_total - old_total:.2f} ({((new_total - old_total)/old_total)*100:.1f}%)")

print(f"\n🎯 COMPLIANCE STATUS:")
if updated_count == len(bundles_created['created_bundles']):
    print(f"   ✅ ALL BUNDLES NOW COMPLIANT WITH 35% PRICING REQUIREMENT")
    print(f"   ✅ All bundles now show 65% discount from compare_at_price")
else:
    print(f"   ⚠️  {len(bundles_created['created_bundles']) - updated_count} bundles still need correction")

print(f"\n📋 VERIFICATION:")
print(f"   URL: https://www.alphamedical.shop/collections/complete-care-kits")
print(f"   Expected: All bundles show 65% OFF badges")
print(f"   Expected: Bundle prices = 35% of compare_at_price")

print("\n" + "=" * 80)
