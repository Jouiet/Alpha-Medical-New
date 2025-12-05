#!/usr/bin/env python3
"""
Verify ALL metafields across ALL namespaces
Investigate discrepancy: audit says 100%, API shows 8%
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_URL = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

url = f"https://{SHOP_URL}/admin/api/2024-10/graphql.json"
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# Query ALL metafields (no namespace filter)
query = """
{
  products(first: 100, query: "status:active") {
    edges {
      node {
        id
        title
        status
        metafields(first: 50) {
          edges {
            node {
              key
              value
              namespace
              type
            }
          }
        }
      }
    }
  }
}
"""

try:
    response = requests.post(url, json={"query": query}, headers=headers, timeout=30)

    if response.status_code != 200:
        print(f"❌ HTTP {response.status_code}")
        exit(1)

    data = response.json()

    if 'errors' in data:
        print(f"❌ GraphQL errors: {data['errors']}")
        exit(1)

    products = data.get('data', {}).get('products', {}).get('edges', [])

    print(f"✅ Querying ALL metafields (all namespaces)")
    print(f"   Active products: {len(products)}\n")

    # Analyze metafields by namespace
    namespace_counts = {}
    products_with_metafields = 0
    products_without_metafields = 0

    for product in products:
        node = product['node']
        metafields = node.get('metafields', {}).get('edges', [])

        if metafields:
            products_with_metafields += 1
            for mf in metafields:
                mf_node = mf['node']
                ns = mf_node['namespace']
                namespace_counts[ns] = namespace_counts.get(ns, 0) + 1
        else:
            products_without_metafields += 1

    print(f"📊 RESULTS:")
    print(f"   Products with metafields: {products_with_metafields}/{len(products)} ({products_with_metafields*100//len(products)}%)")
    print(f"   Products without metafields: {products_without_metafields}/{len(products)}")

    if namespace_counts:
        print(f"\n📋 Metafields by namespace:")
        for ns, count in sorted(namespace_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {ns}: {count} metafields")

    # Show sample products WITH metafields
    print(f"\n✅ Sample products WITH metafields:")
    count = 0
    for product in products:
        node = product['node']
        metafields = node.get('metafields', {}).get('edges', [])
        if metafields and count < 3:
            print(f"\n   {node['title'][:60]}")
            for mf in metafields[:5]:
                mf_node = mf['node']
                value_preview = str(mf_node['value'])[:60].replace('\n', ' ')
                print(f"      {mf_node['namespace']}.{mf_node['key']}: {value_preview}")
            count += 1

    # Show sample products WITHOUT metafields
    print(f"\n❌ Sample products WITHOUT metafields:")
    count = 0
    for product in products:
        node = product['node']
        metafields = node.get('metafields', {}).get('edges', [])
        if not metafields and count < 5:
            print(f"   - {node['title']}")
            count += 1

    exit(0)

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
