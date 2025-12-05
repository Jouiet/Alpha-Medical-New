#!/usr/bin/env python3
"""
Deploy theme assets to Shopify via Admin REST API
Uploads: CSS, JS, and modified theme.liquid
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment
load_dotenv('.env.admin')

# Configuration
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = "2025-10"

def get_active_theme():
    """Get the active theme ID"""
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/themes.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        print(f"❌ Error fetching themes: {response.status_code}")
        print(response.text)
        return None

    themes = response.json().get('themes', [])
    active_theme = next((t for t in themes if t['role'] == 'main'), None)

    if active_theme:
        print(f"✅ Active theme: {active_theme['name']} (ID: {active_theme['id']})")
        return active_theme['id']

    return None

def upload_asset(theme_id, key, value, content_type='text/plain'):
    """Upload an asset to the theme"""
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "asset": {
            "key": key,
            "value": value
        }
    }

    response = requests.put(url, headers=headers, json=payload, timeout=30)

    if response.status_code in [200, 201]:
        size = len(value.encode('utf-8'))
        print(f"  ✅ Uploaded: {key} ({size:,} bytes)")
        return True
    else:
        print(f"  ❌ Failed: {key} (Status: {response.status_code})")
        print(f"     Error: {response.text}")
        return False

def main():
    """Deploy all theme assets"""
    print("=" * 70)
    print("THEME ASSETS DEPLOYMENT")
    print("=" * 70)
    print()

    # Get active theme
    print("1. Fetching active theme...")
    theme_id = get_active_theme()
    if not theme_id:
        print("❌ No active theme found")
        return False
    print()

    # Assets to upload
    assets = [
        {
            'file': 'assets/confetti-celebration.css',
            'key': 'assets/confetti-celebration.css',
            'name': 'Confetti CSS'
        },
        {
            'file': 'assets/confetti-celebration.js',
            'key': 'assets/confetti-celebration.js',
            'name': 'Confetti JavaScript'
        },
        {
            'file': 'layout/theme.liquid',
            'key': 'layout/theme.liquid',
            'name': 'Theme Layout'
        },
        {
            'file': 'assets/bundle-builder-combined.js',
            'key': 'assets/bundle-builder-combined.js',
            'name': 'Bundle Builder Combined'
        },
        {
            'file': 'assets/bundles-collection.js',
            'key': 'assets/bundles-collection.js',
            'name': 'Bundles Collection'
        },
        {
            'file': 'assets/bundle-builder.js',
            'key': 'assets/bundle-builder.js',
            'name': 'Bundle Builder'
        },
        {
            'file': 'assets/dynamic-merchandising.js',
            'key': 'assets/dynamic-merchandising.js',
            'name': 'Dynamic Merchandising'
        },
        {
            'file': 'assets/product-info.js',
            'key': 'assets/product-info.js',
            'name': 'Product Info'
        },
        {
            'file': 'assets/recently-viewed.js',
            'key': 'assets/recently-viewed.js',
            'name': 'Recently Viewed'
        }
    ]

    # Upload assets
    print("2. Uploading assets...")
    print()

    success_count = 0
    fail_count = 0

    for asset in assets:
        file_path = asset['file']

        if not os.path.exists(file_path):
            print(f"  ⚠️  Skipped: {asset['name']} (file not found: {file_path})")
            continue

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Upload
        print(f"  Uploading: {asset['name']}...")
        if upload_asset(theme_id, asset['key'], content):
            success_count += 1
        else:
            fail_count += 1

    print()
    print("=" * 70)
    print("DEPLOYMENT RESULTS")
    print("=" * 70)
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"📦 Total: {success_count + fail_count}")
    print()

    if fail_count == 0:
        print("🎉 All assets deployed successfully!")
        print()
        print("Next steps:")
        print("1. Verify changes on live site: https://www.alphamedical.shop")
        print("2. Test confetti celebration animation")
        print("3. Check browser console (should have 0 console.log)")
        print("4. Test Core Web Vitals with new assets")
    else:
        print("⚠️  Some assets failed to deploy. Check errors above.")

    print()
    return fail_count == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
