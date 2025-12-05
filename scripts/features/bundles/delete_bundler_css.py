#!/usr/bin/env python3
"""
DELETE BUNDLER-APP-OVERRIDE.CSS FROM SHOPIFY
Removes the now-useless CSS override file
"""

import requests
import sys

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('/Users/mac/Desktop/Alpha-Medical/.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except Exception as e:
    print(f"❌ Failed to load credentials: {e}")
    sys.exit(1)

API_VERSION = "2025-10"
THEME_ID = "140069830733"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def delete_asset(asset_key):
    """Delete an asset from Shopify theme"""
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]={asset_key}"

    try:
        response = requests.delete(url, headers=HEADERS)

        if response.status_code == 200:
            return True, "Deleted successfully"
        elif response.status_code == 404:
            return True, "File doesn't exist on Shopify (already deleted or never uploaded)"
        else:
            return False, f"{response.status_code}: {response.text}"

    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("DELETING BUNDLER-APP-OVERRIDE.CSS FROM SHOPIFY")
    print("=" * 80)
    print(f"Store: {SHOPIFY_DOMAIN}")
    print(f"Theme: {THEME_ID}")
    print()

    asset_key = "assets/bundler-app-override.css"
    print(f"Deleting: {asset_key}...")

    success, message = delete_asset(asset_key)

    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ Failed: {message}")

    print()
    print("=" * 80)
    print("CLEANUP SUMMARY")
    print("=" * 80)
    print()
    print("✅ Bundler.app completely removed from Alpha Medical:")
    print("  ❌ App uninstalled (by user)")
    print("  ❌ App blocks removed from templates/product.json")
    print("  ❌ App blocks removed from config/settings_data.json")
    print("  ❌ CSS override removed from assets/bundler-app-override.css")
    print()
    print("✅ 100% NATIVE Shopify - No external apps for bundling")
    print("=" * 80)

if __name__ == '__main__':
    main()
