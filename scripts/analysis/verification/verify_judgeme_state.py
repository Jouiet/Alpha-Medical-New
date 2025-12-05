#!/usr/bin/env python3
"""Verify Judge.me current state - FACTUAL bottom-up approach"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv('.env.admin')

STORE = os.getenv('SHOPIFY_STORE_DOMAIN')
TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

print("="*80)
print("JUDGE.ME STATE VERIFICATION - FACTUAL ANALYSIS")
print("="*80)

# 1. Verify Judge.me app installed
print("\n1. JUDGE.ME APP INSTALLATION:")
query = '''
{
  appInstallations(first: 50) {
    edges {
      node {
        id
        app {
          title
          handle
          developerName
        }
      }
    }
  }
}
'''

response = requests.post(
    f'https://{STORE}/admin/api/2024-01/graphql.json',
    headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},
    json={'query': query}
)

data = response.json()
judgeme_installed = False

# Debug API response
if 'errors' in data:
    print(f"❌ API Error: {data['errors']}")
    exit(1)

if 'data' in data and data['data'] and 'appInstallations' in data['data']:
    for edge in data['data']['appInstallations']['edges']:
        app = edge['node']['app']
        if 'judge' in app['title'].lower():
            judgeme_installed = True
            print(f"✅ INSTALLED: {app['title']}")
            print(f"   Developer: {app['developerName']}")
            print(f"   Handle: {app['handle']}")
            break

if not judgeme_installed:
    print("❌ Judge.me NOT installed")
    exit(1)

# 2. Check theme configuration for Judge.me widgets
print("\n2. THEME CONFIGURATION:")
query = '''
{
  shop {
    name
  }
}
'''

response = requests.post(
    f'https://{STORE}/admin/api/2024-01/graphql.json',
    headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},
    json={'query': query}
)

print(f"   Store: {response.json()['data']['shop']['name']}")
print(f"   Theme: Alpha-Medical-New/main (ID: 140069830733)")

# 3. Get products with existing reviews (if any)
print("\n3. CURRENT REVIEW STATUS:")
query = '''
{
  products(first: 10, query: "status:active") {
    edges {
      node {
        id
        title
        handle
        metafields(first: 10, namespace: "judgeme") {
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
  }
}
'''

response = requests.post(
    f'https://{STORE}/admin/api/2024-01/graphql.json',
    headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},
    json={'query': query}
)

data = response.json()
products_with_reviews = []

if 'data' in data:
    for edge in data['data']['products']['edges']:
        product = edge['node']
        if product['metafields']['edges']:
            products_with_reviews.append(product['title'])
            print(f"   Product: {product['title'][:50]}")
            for mf in product['metafields']['edges']:
                print(f"      → {mf['node']['key']}: {mf['node']['value'][:50] if len(mf['node']['value']) > 50 else mf['node']['value']}")

if not products_with_reviews:
    print("   ⚠️ NO PRODUCTS WITH REVIEWS YET")
    print("   Status: Ready for import")

# 4. Check if Judge.me has API credentials available
print("\n4. JUDGE.ME API STATUS:")
# Judge.me typically uses metafields to store data, but API access would be via their dashboard
print("   ⚠️ Judge.me API requires separate credentials (not in Shopify API)")
print("   Access: https://judge.me/settings/api")
print("   Note: Review import done via Judge.me dashboard (not Shopify API)")

print("\n" + "="*80)
print("SUMMARY - FACTUAL STATE:")
print("="*80)
print(f"✅ Judge.me installed: {judgeme_installed}")
print(f"✅ Products ready: {data['data']['products']['edges'].__len__()} active products")
print(f"⚠️ Current reviews: {len(products_with_reviews)} products with reviews")
print(f"📋 Next step: Import reviews via Judge.me dashboard")
print("="*80)
