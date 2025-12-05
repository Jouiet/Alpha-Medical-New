#!/usr/bin/env python3
"""
PUSH THEME FIXES TO SHOPIFY - Alpha Medical
Upload theme asset changes via Shopify Admin API (REST)

FILES TO PUSH:
1. layout/theme.liquid - Homepage title fix
2. snippets/meta-tags.liquid - Open Graph improvements
3. templates/robots.txt.liquid - AI crawlers activation

NO SHORTCUTS - DIRECT API UPLOAD
"""

import os
import requests
import base64
from datetime import datetime

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

# Load credentials
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

print("="*80)
print("PUSH THEME FIXES TO SHOPIFY - ALPHA MEDICAL")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# ============================================================================
# 1. GET THEME ID (Main published theme)
# ============================================================================
print("\n1. Finding main theme...\n")

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes.json"
headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
themes_data = response.json()

theme_id = None
for theme in themes_data.get("themes", []):
    if theme.get("role") == "main":
        theme_id = theme["id"]
        print(f"✅ Found main theme: {theme['name']} (ID: {theme_id})")
        break

if not theme_id:
    print("❌ No main theme found")
    exit(1)

# ============================================================================
# 2. PUSH THEME ASSETS
# ============================================================================
print("\n" + "="*80)
print("2. PUSHING THEME ASSETS TO SHOPIFY")
print("="*80)

assets_to_push = [
    {
        "key": "layout/theme.liquid",
        "file_path": "/Users/mac/Desktop/Alpha-Medical/layout/theme.liquid",
        "description": "Homepage title fix + meta tags"
    },
    {
        "key": "snippets/meta-tags.liquid",
        "file_path": "/Users/mac/Desktop/Alpha-Medical/snippets/meta-tags.liquid",
        "description": "Open Graph improvements"
    },
    {
        "key": "templates/robots.txt.liquid",
        "file_path": "/Users/mac/Desktop/Alpha-Medical/templates/robots.txt.liquid",
        "description": "AI crawlers activation"
    }
]

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"

pushed_count = 0
failed_count = 0

for asset in assets_to_push:
    print(f"\n⏳ Pushing: {asset['key']}")
    print(f"   Description: {asset['description']}")

    # Check if file exists
    if not os.path.exists(asset['file_path']):
        print(f"   ❌ File not found: {asset['file_path']}")
        failed_count += 1
        continue

    # Read file content
    try:
        with open(asset['file_path'], 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"   ❌ Failed to read file: {e}")
        failed_count += 1
        continue

    # Upload asset via REST API
    payload = {
        "asset": {
            "key": asset['key'],
            "value": content
        }
    }

    try:
        response = requests.put(url, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            pushed_count += 1
            print(f"   ✅ SUCCESS - Asset uploaded")
            print(f"   Size: {len(content):,} bytes")
        else:
            print(f"   ❌ FAILED - Status {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            failed_count += 1

    except Exception as e:
        print(f"   ❌ Exception: {e}")
        failed_count += 1

# ============================================================================
# 3. SUMMARY
# ============================================================================
print("\n" + "="*80)
print("PUSH SUMMARY")
print("="*80)
print(f"\n✅ Successfully pushed: {pushed_count}/{len(assets_to_push)} assets")
if failed_count > 0:
    print(f"❌ Failed: {failed_count} assets")

print("\n🎯 NEXT STEPS:")
print("1. Wait 30-60 seconds for Shopify to propagate changes")
print("2. Re-run comprehensive_seo_validation.py to verify")
print("3. Check homepage: https://www.alphamedical.shop/")

print("\n" + "="*80)
