#!/usr/bin/env python3
"""
VERIFICATION: smart-recommendations-section.liquid Deployment
Date: 2025-11-20
Purpose: Verify if section is deployed to Shopify theme
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
THEME_ID = "140069830733"
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN}

print("=" * 80)
print("VERIFICATION: smart-recommendations-section.liquid Deployment")
print("=" * 80)

# Check section
response = requests.get(
    f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]=sections/smart-recommendations-section.liquid",
    headers=HEADERS
)

if response.status_code == 200:
    asset = response.json().get('asset', {})
    if asset:
        size = len(asset.get('value', ''))
        print(f"✅ DEPLOYED: sections/smart-recommendations-section.liquid")
        print(f"   Size: {size} bytes\n")
    else:
        print("❌ NOT FOUND: sections/smart-recommendations-section.liquid")
        print("   ACTION: Need to deploy section\n")
        exit(1)
else:
    print(f"❌ API Error: {response.status_code}")
    exit(1)

# Check if product-recommendations-matrix.js is deployed
print("Checking product-recommendations-matrix.js...\n")

response2 = requests.get(
    f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]=assets/product-recommendations-matrix.js",
    headers=HEADERS
)

if response2.status_code == 200:
    asset2 = response2.json().get('asset', {})
    if asset2:
        size2 = len(asset2.get('value', ''))
        print(f"✅ DEPLOYED: assets/product-recommendations-matrix.js")
        print(f"   Size: {size2} bytes\n")
    else:
        print("❌ NOT FOUND: assets/product-recommendations-matrix.js")
        exit(1)
else:
    print(f"❌ API Error: {response2.status_code}")
    exit(1)

print("=" * 80)
print("CONCLUSION")
print("=" * 80)
print("✅ All AI recommendations files are deployed")
print("⚠️  If recommendations not showing on product pages:")
print("   1. Check CDN cache (wait 5-10 min)")
print("   2. Hard refresh product page (Cmd+Shift+R)")
print("   3. Check browser console for JavaScript errors")
print()
