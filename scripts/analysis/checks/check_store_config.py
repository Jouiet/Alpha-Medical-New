#!/usr/bin/env python3
"""
CHECK STORE CONFIGURATION - Debug title issue
"""

import requests

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

# Get shop details
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/shop.json"
headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN
}

response = requests.get(url, headers=headers)
shop_data = response.json()

shop = shop_data.get("shop", {})

print("="*80)
print("STORE CONFIGURATION")
print("="*80)
print(f"\nShop Name: {shop.get('name')}")
print(f"Primary Domain: {shop.get('domain')}")
print(f"Custom Domain: {shop.get('myshopify_domain')}")
print(f"Email: {shop.get('email')}")

# Check if there's a meta title set
print(f"\n📋 SEO Settings:")
print(f"   Homepage Title: {shop.get('meta_title', 'NOT SET')}")
print(f"   Homepage Description: {shop.get('meta_description', 'NOT SET')[:100] if shop.get('meta_description') else 'NOT SET'}...")

print("\n" + "="*80)
