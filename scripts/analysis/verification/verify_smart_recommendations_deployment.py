#!/usr/bin/env python3
"""
VERIFICATION: smart-recommendations.liquid Deployment Status
Date: 2025-11-20
Purpose: Verify if snippet is deployed to Shopify theme
"""

import os
import requests

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

SHOP = "azffej-as.myshopify.com"
THEME_ID = "140069830733"  # Alpha-Medical-New/main
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN}

print("=" * 80)
print("VERIFICATION: smart-recommendations.liquid Deployment")
print("=" * 80)
print(f"Theme ID: {THEME_ID}\n")

# Check if snippet exists on Shopify
print("Checking if snippets/smart-recommendations.liquid exists on Shopify...\n")

response = requests.get(
    f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]=snippets/smart-recommendations.liquid",
    headers=HEADERS
)

if response.status_code == 200:
    asset = response.json().get('asset', {})
    if asset:
        size = len(asset.get('value', ''))
        print(f"✅ DEPLOYED: snippets/smart-recommendations.liquid")
        print(f"   Size: {size} bytes")
        print(f"   Status: LIVE on theme {THEME_ID}\n")
        exit(0)
    else:
        print("❌ NOT FOUND: snippets/smart-recommendations.liquid")
        print("   Status: NOT deployed to Shopify\n")
        print("ACTION REQUIRED: Deploy snippet using deployment script")
        exit(1)
else:
    print(f"❌ API Error: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    exit(1)
