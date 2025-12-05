#!/usr/bin/env python3
"""
Fix 3 products missing SEO metafields (title_tag + description_tag)

Products identified in audit:
1. electric-vibration-massager-bunion-corrector-unisex-foot-hallux-valgus-braces...
2. bunion-corrector-toe-separator-bunions-haluksy-separators...
3. effective-bunion-corrector-airbag-traction-foot-hallux-valgus-braces...

NO SUPPOSITIONS - RIGOROUS VERIFICATION
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
    if not SHOPIFY_TOKEN:
        raise ValueError("Token not found")
except Exception as e:
    print(f"❌ Error: {e}")
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
        for error in data["errors"]:
            print(f"❌ {error.get('message')}")
        return None
    return data

print("="*80)
print("FIX MISSING METAFIELDS - 3 BUNION CORRECTOR PRODUCTS")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# Target products handles
target_handles = [
    "electric-vibration-massager-bunion-corrector-unisex-foot-hallux-valgus-braces-adjustable-toe-separator-finger-toe-corrector",
    "bunion-corrector-toe-separator-bunions-haluksy-separators-halux-toe-spreader-finger-straightener-for-toe-hallux-valgus-corrector",
    "effective-bunion-corrector-airbag-traction-foot-hallux-valgus-braces-toe-separator-straightener-orthotics-toe-correction"
]

print(f"\n1. Fetching product details for {len(target_handles)} products...\n")

products_to_fix = []

for handle in target_handles:
    query = """
    query getProduct($handle: String!) {
      productByHandle(handle: $handle) {
        id
        title
        handle
        description
        metafields(first: 20) {
          edges {
            node {
              namespace
              key
              value
            }
          }
        }
      }
    }
    """

    result = graphql_query(query, {"handle": handle})

    if not result or not result.get("data", {}).get("productByHandle"):
        print(f"❌ Product not found: {handle}")
        continue

    product = result["data"]["productByHandle"]

    # Check if already has metafields
    metafields = product["metafields"]["edges"]
    has_title = any(mf["node"]["key"] == "title_tag" for mf in metafields)
    has_desc = any(mf["node"]["key"] == "description_tag" for mf in metafields)

    print(f"Product: {product['title'][:60]}...")
    print(f"   ID: {product['id']}")
    print(f"   Has title_tag: {'✅' if has_title else '❌'}")
    print(f"   Has description_tag: {'✅' if has_desc else '❌'}")

    if not has_title or not has_desc:
        products_to_fix.append(product)
        print(f"   → Will fix")
    else:
        print(f"   → Already has metafields (skipping)")
    print()

if not products_to_fix:
    print("✅ All products already have metafields. Nothing to fix.")
    exit(0)

print(f"\n2. Fixing {len(products_to_fix)} products...\n")

# Mutation to add metafields
mutation = """
mutation productUpdate($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      title
      metafields(first: 20) {
        edges {
          node {
            namespace
            key
            value
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

fixed_count = 0

for product in products_to_fix:
    # Generate SEO title and description from product title and description
    title = product["title"]
    description = product["description"]

    # SEO title: Product title (max 60 chars)
    seo_title = title if len(title) <= 60 else title[:57] + "..."

    # SEO description: First 160 chars of description
    seo_description = description.replace("\n", " ").strip()
    if len(seo_description) > 160:
        seo_description = seo_description[:157] + "..."

    print(f"Updating: {title[:60]}...")
    print(f"   SEO Title ({len(seo_title)} chars): {seo_title}")
    print(f"   SEO Desc ({len(seo_description)} chars): {seo_description[:80]}...")

    variables = {
        "input": {
            "id": product["id"],
            "metafields": [
                {
                    "namespace": "global",
                    "key": "title_tag",
                    "value": seo_title,
                    "type": "single_line_text_field"
                },
                {
                    "namespace": "global",
                    "key": "description_tag",
                    "value": seo_description,
                    "type": "single_line_text_field"
                }
            ]
        }
    }

    result = graphql_query(mutation, variables)

    if not result:
        print(f"   ❌ Failed to update")
        continue

    update_result = result["data"]["productUpdate"]
    user_errors = update_result.get("userErrors", [])

    if user_errors:
        print(f"   ❌ Errors:")
        for error in user_errors:
            print(f"      - {error['field']}: {error['message']}")
        continue

    fixed_count += 1
    print(f"   ✅ SUCCESS")
    print()

print("="*80)
print("SUMMARY")
print("="*80)
print(f"\n✅ Fixed {fixed_count}/{len(products_to_fix)} products")
print(f"\nRe-run audit to verify: python3 audit_all_products_metafields.py")
print("\n" + "="*80)
