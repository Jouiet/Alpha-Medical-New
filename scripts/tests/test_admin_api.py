#!/usr/bin/env python3
"""
Test Shopify Admin API Access
Verifies credentials work before configuring GitHub Secrets
"""

import os
import requests
from dotenv import load_dotenv

# Load .env.admin credentials
load_dotenv('.env.admin')

SHOP_URL = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

if not SHOP_URL or not ACCESS_TOKEN:
    print("❌ Missing credentials in .env.admin")
    exit(1)

# Test Admin API with simple shop query
url = f"https://{SHOP_URL}/admin/api/2024-10/graphql.json"
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

query = """
{
  shop {
    name
    email
    currencyCode
    plan {
      displayName
    }
  }
}
"""

try:
    response = requests.post(url, json={"query": query}, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print(f"❌ GraphQL errors: {data['errors']}")
            exit(1)

        shop = data.get('data', {}).get('shop', {})
        print("✅ Admin API Access: SUCCESS")
        print(f"   Shop: {shop.get('name')}")
        print(f"   Email: {shop.get('email')}")
        print(f"   Currency: {shop.get('currencyCode')}")
        print(f"   Plan: {shop.get('plan', {}).get('displayName')}")
        exit(0)
    else:
        print(f"❌ HTTP {response.status_code}: {response.text}")
        exit(1)

except Exception as e:
    print(f"❌ Connection error: {e}")
    exit(1)
