#!/usr/bin/env python3
"""
Deploy theme.liquid to Shopify with popup renders
"""

import requests
import sys

# Load Shopify credentials from .env.admin (gitignored)
SHOPIFY_STORE = None
SHOPIFY_ACCESS_TOKEN = None

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_ACCESS_TOKEN = line.split('=', 1)[1].strip()
            elif line.startswith('SHOPIFY_STORE_DOMAIN='):
                SHOPIFY_STORE = line.split('=', 1)[1].strip()
except FileNotFoundError:
    print("❌ ERROR: .env.admin not found. Create it with:")
    print("   SHOPIFY_ADMIN_ACCESS_TOKEN=your_token")
    print("   SHOPIFY_STORE_DOMAIN=your_store.myshopify.com")
    sys.exit(1)

if not SHOPIFY_STORE or not SHOPIFY_ACCESS_TOKEN:
    print("❌ ERROR: Missing credentials in .env.admin")
    sys.exit(1)

THEME_ID = "140069830733"
API_VERSION = "2025-10"

BASE_URL = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def main():
    print("=" * 60)
    print("DEPLOYING theme.liquid TO SHOPIFY")
    print("=" * 60)

    # Read local theme.liquid
    with open('layout/theme.liquid', 'r', encoding='utf-8') as f:
        content = f.read()

    # Verify popup renders are present
    if 'welcome-popup' in content and 'exit-intent-popup' in content:
        print("✅ Popup renders found in local theme.liquid")
    else:
        print("❌ WARNING: Popup renders NOT found in local theme.liquid")
        return 1

    # Upload to Shopify
    payload = {
        "asset": {
            "key": "layout/theme.liquid",
            "value": content
        }
    }

    print(f"\n📤 Uploading theme.liquid ({len(content)} bytes)...")

    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    response = requests.put(url, headers=HEADERS, json=payload)

    if response.status_code in [200, 201]:
        asset_data = response.json().get('asset', {})
        print(f"✅ SUCCESS: theme.liquid deployed")
        print(f"   Size: {asset_data.get('size', 0)} bytes")
        print(f"   Updated: {asset_data.get('updated_at', 'N/A')}")
        print(f"\n🎉 Deployment complete!")
        print(f"   Email popups should now be LIVE at https://alphamedical.shop")
        return 0
    else:
        print(f"❌ FAILED: {response.status_code}")
        print(f"   Error: {response.text}")
        return 1

if __name__ == "__main__":
    exit(main())
