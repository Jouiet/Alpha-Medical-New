#!/usr/bin/env python3
"""
FIX BUNDLE PRICING TO 35% - Alpha Medical Care
Update all bundle prices to 35% of compare_at_price (65% discount)

REQUIREMENT: "Bundles 35% du prix fournisseur (35% du chiffre compare at price)"
CURRENT STATE: Bundles at 85% (15% discount) - VIOLATION
TARGET STATE: Bundles at 35% (65% discount) - COMPLIANT
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
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    data = response.json()
    if "errors" in data:
        print(f"   ❌ GraphQL Errors: {data['errors']}")
        return None
    return data

print("=" * 80)
print("FIX BUNDLE PRICING TO 35% - ALPHA MEDICAL CARE")
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
    bundle_id = bundle_created['id']

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
    print(f"   ID: {bundle_id}")
    print(f"   Compare At Price (Total): ${total_price:.2f}")
    print(f"   OLD Price: ${old_bundle_price:.2f} (85% of total, 15% discount)")
    print(f"   NEW Price: ${new_bundle_price:.2f} (35% of total, 65% discount)")
    print(f"   Price Reduction: ${old_bundle_price - new_bundle_price:.2f}")

    # Fetch product variants
    query = """
    query getProduct($id: ID!) {
      product(id: $id) {
        id
        title
        variants(first: 10) {
          edges {
            node {
              id
              price
              compareAtPrice
            }
          }
        }
      }
    }
    """

    result = graphql_query(query, {"id": bundle_id})

    if not result:
        print(f"   ❌ Failed to fetch product variants")
        failed_count += 1
        continue

    product = result['data']['product']
    variants = product['variants']['edges']

    if not variants:
        print(f"   ❌ No variants found")
        failed_count += 1
        continue

    # Get first variant (bundles have 1 variant)
    variant_id = variants[0]['node']['id']
    current_price = float(variants[0]['node']['price'])
    current_compare_at = variants[0]['node']['compareAtPrice']

    print(f"\n   Variant ID: {variant_id}")
    print(f"   Current Variant Price: ${current_price}")
    print(f"   Current Compare At: ${current_compare_at}")

    # Update variant price and compare_at_price
    mutation = """
    mutation productVariantUpdate($input: ProductVariantInput!) {
      productVariantUpdate(input: $input) {
        productVariant {
          id
          price
          compareAtPrice
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "id": variant_id,
            "price": str(new_bundle_price),
            "compareAtPrice": str(total_price)  # Set compare_at to total price
        }
    }

    print(f"\n   Updating variant...")
    print(f"      New Price: ${new_bundle_price}")
    print(f"      New Compare At: ${total_price:.2f}")

    update_result = graphql_query(mutation, variables)

    if not update_result:
        print(f"   ❌ Failed to update variant")
        failed_count += 1
        continue

    update_data = update_result['data']['productVariantUpdate']
    user_errors = update_data.get('userErrors', [])

    if user_errors:
        print(f"   ❌ Update errors:")
        for error in user_errors:
            print(f"      {error['field']}: {error['message']}")
        failed_count += 1
        continue

    updated_variant = update_data['productVariant']
    print(f"   ✅ SUCCESS")
    print(f"      Final Price: ${updated_variant['price']}")
    print(f"      Final Compare At: ${updated_variant['compareAtPrice']}")
    updated_count += 1

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
else:
    print(f"   ⚠️  {len(bundles_created['created_bundles']) - updated_count} bundles still need correction")

print(f"\n📋 VERIFICATION:")
print(f"   URL: https://www.alphamedical.shop/collections/complete-care-kits")
print(f"   Expected: All bundles show 65% OFF badges")
print(f"   Expected: Bundle prices = 35% of compare_at_price")

print("\n" + "=" * 80)
