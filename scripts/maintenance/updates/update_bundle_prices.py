#!/usr/bin/env python3
"""
UPDATE BUNDLE VARIANT PRICES - Alpha Medical
Fix prices for all created bundle products using productVariantsBulkUpdate

Uses latest Shopify API 2025-10 with correct mutation
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

# Use latest API version
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
        for error in data["errors"]:
            print(f"❌ GraphQL Error: {error.get('message')}")
        return None
    return data

print("="*80)
print("ALPHA MEDICAL - UPDATE BUNDLE VARIANT PRICES")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"API Version: {API_VERSION}")
print("="*80)

# ============================================================================
# 1. LOAD CREATED BUNDLES AND PLANS
# ============================================================================
print("\n1. Loading bundle data...\n")

try:
    with open('bundle_products_created.json', 'r') as f:
        created_data = json.load(f)
    with open('optimal_bundles_plan.json', 'r') as f:
        plans_data = json.load(f)
except Exception as e:
    print(f"❌ Failed to load data: {e}")
    exit(1)

created_bundles = created_data["created_bundles"]
bundles_plans = {b["name"]: b for b in plans_data["bundles"]}

print(f"✅ Loaded {len(created_bundles)} created bundles")

# ============================================================================
# 2. GET CURRENT VARIANT IDS AND PRICES
# ============================================================================
print("\n" + "="*80)
print("2. FETCHING CURRENT VARIANT DATA")
print("="*80)

query_product = """
query getProduct($id: ID!) {
  product(id: $id) {
    id
    title
    variants(first: 1) {
      edges {
        node {
          id
          price
        }
      }
    }
  }
}
"""

bundle_variants = []

for bundle in created_bundles:
    result = graphql_query(query_product, {"id": bundle["id"]})

    if not result:
        print(f"❌ Failed to fetch: {bundle['name']}")
        continue

    product = result["data"]["product"]
    variant = product["variants"]["edges"][0]["node"]

    # Find corresponding plan
    plan_name = bundle["name"].replace(" - Complete Care Kit", "")
    plan = bundles_plans.get(plan_name)

    if not plan:
        print(f"⚠️  No plan found for: {bundle['name']}")
        continue

    current_price = float(variant["price"])
    target_price = round(plan["bundle_price"], 2)

    print(f"\n{bundle['name'][:60]}...")
    print(f"   Current: ${current_price:.2f}")
    print(f"   Target:  ${target_price:.2f}")
    print(f"   Status:  {'✅ OK' if abs(current_price - target_price) < 0.01 else '⚠️  NEEDS UPDATE'}")

    bundle_variants.append({
        "product_id": bundle["id"],
        "variant_id": variant["id"],
        "name": bundle["name"],
        "current_price": current_price,
        "target_price": target_price,
        "needs_update": abs(current_price - target_price) >= 0.01
    })

# ============================================================================
# 3. UPDATE VARIANT PRICES
# ============================================================================
print("\n" + "="*80)
print("3. UPDATING VARIANT PRICES")
print("="*80)

mutation_bulk_update = """
mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    product {
      id
      title
    }
    productVariants {
      id
      price
    }
    userErrors {
      field
      message
    }
  }
}
"""

updated_count = 0
failed_count = 0

for bv in bundle_variants:
    if not bv["needs_update"]:
        print(f"\n✅ {bv['name'][:60]}... (already correct price)")
        continue

    print(f"\n⏳ Updating: {bv['name'][:60]}...")
    print(f"   {bv['current_price']:.2f} → ${bv['target_price']:.2f}")

    variables = {
        "productId": bv["product_id"],
        "variants": [
            {
                "id": bv["variant_id"],
                "price": str(bv["target_price"])
            }
        ]
    }

    result = graphql_query(mutation_bulk_update, variables)

    if not result:
        print(f"   ❌ FAILED - GraphQL error")
        failed_count += 1
        continue

    update_result = result["data"]["productVariantsBulkUpdate"]
    user_errors = update_result.get("userErrors", [])

    if user_errors:
        print(f"   ❌ FAILED - User errors:")
        for error in user_errors:
            print(f"      {error['field']}: {error['message']}")
        failed_count += 1
        continue

    updated_variant = update_result["productVariants"][0]
    print(f"   ✅ SUCCESS - New price: ${updated_variant['price']}")
    updated_count += 1

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)
print(f"\n✅ Updated: {updated_count} bundles")
if failed_count > 0:
    print(f"❌ Failed: {failed_count} bundles")
print(f"✅ Total processed: {len(bundle_variants)} bundles")

print("\n🎯 VERIFICATION:")
print("Visit: https://www.alphamedical.shop/collections/complete-care-kits")
print("Check all bundle prices are correct (15% discount)")

print("\n" + "="*80)
