#!/usr/bin/env python3
"""
Push llms.txt template to Shopify via Admin API
Uses Asset API to upload template file directly
"""

import os
import json
import requests
import base64

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except FileNotFoundError:
    SHOPIFY_TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

if not SHOPIFY_TOKEN:
    print("❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found")
    exit(1)

API_VERSION = "2025-10"
THEME_ID = "140069830733"  # Alpha-Medical-New/main (current live theme)
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("="*80)
print("PUSHING LLMS.TXT TEMPLATE TO SHOPIFY")
print("="*80)

# Read template file
template_path = "templates/page.llms-txt.liquid"

try:
    with open(template_path, 'r') as f:
        template_content = f.read()
    print(f"\n✅ Read template: {template_path}")
    print(f"   File size: {len(template_content)} chars")
except FileNotFoundError:
    print(f"\n❌ Template file not found: {template_path}")
    exit(1)

# Upload asset via REST API
asset_key = "templates/page.llms-txt.liquid"

payload = {
    "asset": {
        "key": asset_key,
        "value": template_content
    }
}

print(f"\n📤 Uploading to Shopify...")
print(f"   Theme ID: {THEME_ID}")
print(f"   Asset Key: {asset_key}")

response = requests.put(REST_URL, json=payload, headers=HEADERS)

if response.status_code == 200:
    asset = response.json()["asset"]
    print(f"\n✅ SUCCESS - Template uploaded!")
    print(f"   Key: {asset['key']}")
    print(f"   Size: {asset.get('size', 'N/A')} bytes")
    print(f"   Public URL: {asset.get('public_url', 'N/A')}")
    print(f"\n📝 Page now accessible at:")
    print(f"   https://www.alphamedical.shop/pages/llms-txt")
elif response.status_code == 422:
    errors = response.json().get("errors", {})
    print(f"\n❌ Validation Error:")
    print(f"   {json.dumps(errors, indent=2)}")
    exit(1)
else:
    print(f"\n❌ Upload Failed (HTTP {response.status_code}):")
    print(f"   {response.text[:500]}")
    exit(1)

print("\n" + "="*80)
print("VERIFICATION")
print("="*80)

# Verify page is accessible
print("\n🔍 Testing page accessibility...")

page_url = "https://www.alphamedical.shop/pages/llms-txt"
response = requests.get(page_url, timeout=10)

if response.status_code == 200:
    content = response.text
    # Check for llms.txt markers
    if "Alpha Medical Care" in content and ("llms.txt" in content.lower() or "LLM" in content):
        print(f"✅ Page is live and rendering correctly!")
        print(f"   URL: {page_url}")
        print(f"   Content length: {len(content)} chars")
        print(f"   Contains: 'Alpha Medical Care' ✓")
    else:
        print(f"⚠️  Page is accessible but may not be using custom template")
        print(f"   URL: {page_url}")
        print(f"   Verify manually that template renders correctly")
elif response.status_code == 404:
    print(f"❌ Page not found: {page_url}")
    print(f"   - Page may need to be published in Shopify Admin")
    print(f"   - Go to: https://admin.shopify.com/store/azffej-as/pages")
else:
    print(f"⚠️  HTTP {response.status_code}: {page_url}")

print("\n" + "="*80)
print("DONE")
print("="*80)
