#!/usr/bin/env python3
"""
Verify Products & Metafields via Admin API
Uses working credentials from .env.admin
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

# Query products with metafields
query = """
{
  products(first: 100, query: "status:active") {
    edges {
      node {
        id
        title
        status
        tags
        metafields(first: 10, namespace: "custom") {
          edges {
            node {
              key
              value
              namespace
            }
          }
        }
      }
    }
    pageInfo {
      hasNextPage
    }
  }
}
"""

try:
    response = requests.post(url, json={"query": query}, headers=headers, timeout=30)

    if response.status_code != 200:
        print(f"❌ HTTP {response.status_code}: {response.text[:300]}")
        exit(1)

    data = response.json()

    if 'errors' in data:
        print(f"❌ GraphQL errors: {data['errors']}")
        exit(1)

    products = data.get('data', {}).get('products', {}).get('edges', [])

    print(f"✅ Admin API Query: SUCCESS")
    print(f"   Active products: {len(products)}")

    # Count metafields
    with_metafields = 0
    without_metafields = 0
    total_metafields = 0

    for product in products:
        node = product['node']
        metafields = node.get('metafields', {}).get('edges', [])

        if metafields:
            with_metafields += 1
            total_metafields += len(metafields)
        else:
            without_metafields += 1

    print(f"   With metafields: {with_metafields} ({with_metafields*100//len(products)}%)")
    print(f"   Without metafields: {without_metafields}")
    print(f"   Total metafields: {total_metafields}")

    # Sample metafields
    if total_metafields > 0:
        print("\n📋 Sample metafields:")
        for product in products[:3]:
            node = product['node']
            metafields = node.get('metafields', {}).get('edges', [])
            if metafields:
                print(f"\n   {node['title'][:50]}:")
                for mf in metafields[:3]:
                    mf_node = mf['node']
                    print(f"      - {mf_node['key']}: {str(mf_node['value'])[:50]}")

    # Check for French keywords in tags
    french_keywords = ['santé', 'douleur', 'articulation', 'soulagement', 'thérapie']
    products_with_french = []

    for product in products:
        node = product['node']
        tags = ' '.join(node.get('tags', [])).lower()
        for keyword in french_keywords:
            if keyword in tags:
                products_with_french.append(node['title'])
                break

    if products_with_french:
        print(f"\n⚠️  {len(products_with_french)} products with French keywords in tags:")
        for title in products_with_french[:5]:
            print(f"   - {title}")
    else:
        print("\n✅ No French keywords detected in tags")

    exit(0)

except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
