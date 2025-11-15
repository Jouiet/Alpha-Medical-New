#!/usr/bin/env python3
"""
Add SEO Metafields to Bundles
Fixes: 15 bundles without metafields (84.7% → 100% coverage)
"""

import os
import json
import requests

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
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query):
    """Execute GraphQL query/mutation"""
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ GraphQL Error: {response.status_code}")
        print(response.text)
        return None
    return response.json()

print("=" * 70)
print("ADDING SEO METAFIELDS TO BUNDLES")
print("=" * 70)

# Get all active products without metafields
query = """
{
  products(first: 250, query: "status:active") {
    edges {
      node {
        id
        title
        handle
        tags
        metafields(first: 5) {
          edges {
            node {
              namespace
              key
            }
          }
        }
      }
    }
  }
}
"""

data = graphql_query(query)
if not data or 'data' not in data:
    print("❌ Failed to fetch products")
    exit(1)

products = data['data']['products']['edges']

# Find products without metafields
products_without_metafields = []
for edge in products:
    product = edge['node']
    metafields = product['metafields']['edges']
    if len(metafields) == 0:
        products_without_metafields.append(product)

print(f"\n📊 Found {len(products_without_metafields)} products without metafields")

if len(products_without_metafields) == 0:
    print("✅ All products already have metafields!")
    exit(0)

# Add basic SEO metafields to each product
success_count = 0
fail_count = 0

for product in products_without_metafields:
    product_id = product['id']
    title = product['title']
    tags = product['tags']

    print(f"\n📦 Processing: {title}")

    # Create basic SEO metafield (keywords based on tags)
    keywords = ', '.join([tag for tag in tags if len(tag) > 2])[:500]  # Max 500 chars

    # Mutation to add metafield
    mutation = f"""
    mutation {{
      productUpdate(input: {{
        id: "{product_id}"
        metafields: [
          {{
            namespace: "custom"
            key: "seo_keywords"
            type: "single_line_text_field"
            value: "{keywords if keywords else title}"
          }}
        ]
      }}) {{
        product {{
          id
          title
        }}
        userErrors {{
          field
          message
        }}
      }}
    }}
    """

    result = graphql_query(mutation)

    if result and 'data' in result:
        user_errors = result['data']['productUpdate']['userErrors']
        if len(user_errors) == 0:
            print(f"   ✅ Metafield added")
            success_count += 1
        else:
            print(f"   ❌ Error: {user_errors}")
            fail_count += 1
    else:
        print(f"   ❌ Mutation failed")
        fail_count += 1

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"✅ Success: {success_count}/{len(products_without_metafields)}")
print(f"❌ Failed: {fail_count}/{len(products_without_metafields)}")

if success_count == len(products_without_metafields):
    print("\n🎉 ALL PRODUCTS NOW HAVE METAFIELDS!")
    print("   Metafield coverage: 100%")
else:
    print(f"\n⚠️  {fail_count} products still without metafields")

print("=" * 70)
