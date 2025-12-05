#!/usr/bin/env python3
"""
DEPLOYMENT - BUNDLES CTA BANNER
Uploads bundles-cta-banner.liquid snippet to Shopify theme
"""

import os
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
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def rest_request(method, endpoint, data=None):
    """Execute REST API request"""
    url = f"{REST_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=30)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data, timeout=30)

        if response.status_code not in [200, 201]:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None

        return response.json() if response.text else {}
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

print("=" * 80)
print("DEPLOYMENT - BUNDLES CTA BANNER")
print("=" * 80)

# Get main theme
print("\n1. Getting main theme...")
themes_response = rest_request("GET", "/themes.json")
if not themes_response or 'themes' not in themes_response:
    print("❌ Failed to get themes")
    exit(1)

main_theme = next((t for t in themes_response['themes'] if t['role'] == 'main'), None)
if not main_theme:
    print("❌ Main theme not found")
    exit(1)

theme_id = main_theme['id']
print(f"✅ Found theme: {main_theme['name']} (ID: {theme_id})")

# Read snippet file
print("\n2. Reading snippet file...")
snippet_path = "snippets/bundles-cta-banner.liquid"

try:
    with open(snippet_path, 'r', encoding='utf-8') as f:
        snippet_content = f.read()
    print(f"✅ Read snippet: {len(snippet_content)} characters")
except Exception as e:
    print(f"❌ Failed to read snippet: {e}")
    exit(1)

# Upload snippet to theme
print("\n3. Uploading snippet to theme...")
asset_data = {
    "asset": {
        "key": snippet_path,
        "value": snippet_content
    }
}

upload_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", asset_data)
if upload_result and 'asset' in upload_result:
    print(f"✅ Uploaded: {snippet_path}")
else:
    print(f"❌ Failed to upload snippet")
    exit(1)

print("\n" + "=" * 80)
print("DEPLOYMENT COMPLETE")
print("=" * 80)

print("\n✅ Snippet uploaded: snippets/bundles-cta-banner.liquid")
print("\n📋 NEXT STEPS (Manual):")
print("\n1. Add snippet to homepage:")
print("   - Admin Shopify → Online Store → Themes → Customize")
print("   - Go to Homepage")
print("   - Click 'Add section' or find a suitable location")
print("   - Add 'Custom Liquid' section")
print("   - Insert: {% render 'bundles-cta-banner' %}")
print("   - Save")

print("\n2. Recommended placement:")
print("   - Below hero section")
print("   - Before product collections")
print("   - Mid-page (between sections)")

print("\n3. Test:")
print("   - Visit https://www.alphamedical.shop")
print("   - Verify banner appears")
print("   - Test both CTAs:")
print("     • 'Shop Now' → /pages/bundles")
print("     • 'Build Now' → /pages/bundle-creator")

print("\n" + "=" * 80)
