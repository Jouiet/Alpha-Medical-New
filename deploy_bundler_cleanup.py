#!/usr/bin/env python3
"""
DEPLOY BUNDLER CLEANUP - ALPHA MEDICAL
Uploads cleaned templates/product.json and config/settings_data.json
"""

import requests
import json
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

def upload_file(filepath, asset_key):
    """Upload a file to Shopify theme"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
        payload = {
            "asset": {
                "key": asset_key,
                "value": content
            }
        }

        response = requests.put(url, headers=HEADERS, json=payload)

        if response.status_code in [200, 201]:
            return True, len(content)
        else:
            return False, response.text

    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("DEPLOYING BUNDLER CLEANUP TO SHOPIFY")
    print("=" * 80)
    print(f"Store: {SHOPIFY_DOMAIN}")
    print(f"Theme: {THEME_ID}")
    print()

    files = [
        {
            'path': '/Users/mac/Desktop/Alpha-Medical/templates/product.json',
            'key': 'templates/product.json',
            'description': 'Product template (removed bundler_bundler_target_element_k4Rh48)'
        },
        {
            'path': '/Users/mac/Desktop/Alpha-Medical/config/settings_data.json',
            'key': 'config/settings_data.json',
            'description': 'Theme settings (removed bundler-script-append block)'
        }
    ]

    success_count = 0
    total_bytes = 0

    for i, file_info in enumerate(files, 1):
        print(f"[{i}/{len(files)}] Uploading {file_info['key']}...")
        print(f"  → {file_info['description']}")

        success, result = upload_file(file_info['path'], file_info['key'])

        if success:
            print(f"  ✅ Success ({result} bytes)")
            success_count += 1
            total_bytes += result
        else:
            print(f"  ❌ Failed: {result[:200]}")

        print()

    print("=" * 80)
    print("DEPLOYMENT SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully uploaded: {success_count}/{len(files)} files")
    print(f"📦 Total size: {total_bytes:,} bytes ({total_bytes/1024:.1f} KB)")
    print()

    if success_count == len(files):
        print("🎉 BUNDLER.APP CLEANUP COMPLETE!")
        print()
        print("VERIFICATION:")
        print("1. Visit: https://www.alphamedical.shop/products/[any-product]")
        print("2. Inspect page source (View Page Source)")
        print("3. Search for 'bundler' - should find ZERO app block errors")
        print("4. Confirm no 'Powered by Bundler.app' text appears")
        print()
        print("WHAT WAS REMOVED:")
        print("  ❌ templates/product.json: bundler_bundler_target_element_k4Rh48 block")
        print("  ❌ config/settings_data.json: bundler-script-append block (ID: 5918445685253060206)")
        print()
        print("WHAT REMAINS:")
        print("  ✅ assets/bundler-app-override.css (harmless - just CSS, can delete later)")
        print("  ✅ All NATIVE Shopify functionality intact")
    else:
        print("⚠️  Some files failed to upload. Check errors above.")

    print("=" * 80)

if __name__ == '__main__':
    main()
