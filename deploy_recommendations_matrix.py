#!/usr/bin/env python3
"""
Deploy Product Recommendations Matrix to Shopify Theme Assets
Part of: TOP5_PERCENT_NATIVE_IMPLEMENTATION_PLAN.md - Priority 1

Uploads assets/product-recommendations-matrix.js to Shopify theme via Asset API
"""

import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.admin')

# Shopify API Configuration
SHOPIFY_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_THEME_ID = os.getenv('SHOPIFY_THEME_ID', '140069830733')
API_VERSION = '2024-10'
BASE_URL = f'https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}'

# Authentication headers
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

def read_local_file(file_path):
    """Read local JS file content"""
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    file_size = os.path.getsize(file_path)
    print(f"✅ Read local file: {file_path} ({file_size:,} bytes)")
    return content

def upload_asset_to_theme(asset_key, asset_value):
    """Upload asset to Shopify theme via Asset API"""
    print(f"\n📤 Uploading asset: {asset_key}")

    url = f'{BASE_URL}/themes/{SHOPIFY_THEME_ID}/assets.json'

    payload = {
        'asset': {
            'key': asset_key,
            'value': asset_value
        }
    }

    try:
        response = requests.put(url, headers=HEADERS, json=payload, timeout=60)
        response.raise_for_status()

        result = response.json()
        asset_info = result.get('asset', {})

        print(f"✅ Upload successful!")
        print(f"   Key: {asset_info.get('key')}")
        print(f"   Size: {asset_info.get('size', 0):,} bytes")
        print(f"   Theme ID: {asset_info.get('theme_id')}")
        print(f"   Public URL: {asset_info.get('public_url', 'N/A')}")

        return True

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Response: {response.text}")
        return False
    except Exception as e:
        print(f"❌ Error uploading asset: {e}")
        return False

def verify_asset_deployed(asset_key):
    """Verify asset exists in theme"""
    print(f"\n🔍 Verifying asset deployment: {asset_key}")

    url = f'{BASE_URL}/themes/{SHOPIFY_THEME_ID}/assets.json'
    params = {'asset[key]': asset_key}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        response.raise_for_status()

        result = response.json()
        asset_info = result.get('asset', {})

        if asset_info:
            print(f"✅ Asset verified in theme!")
            print(f"   Key: {asset_info.get('key')}")
            print(f"   Size: {asset_info.get('size', 0):,} bytes")
            print(f"   Created: {asset_info.get('created_at', 'N/A')}")
            print(f"   Updated: {asset_info.get('updated_at', 'N/A')}")
            return True
        else:
            print(f"❌ Asset not found in theme")
            return False

    except Exception as e:
        print(f"❌ Error verifying asset: {e}")
        return False

def main():
    print("=" * 80)
    print("DEPLOY AI RECOMMENDATIONS MATRIX TO SHOPIFY THEME")
    print("=" * 80)
    print(f"Theme ID: {SHOPIFY_THEME_ID}")
    print(f"Store: {SHOPIFY_DOMAIN}")
    print("=" * 80)

    # Step 1: Read local file
    local_file_path = '/Users/mac/Desktop/Alpha-Medical/assets/product-recommendations-matrix.js'
    content = read_local_file(local_file_path)

    if not content:
        print("\n❌ DEPLOYMENT FAILED: Cannot read local file")
        return False

    # Step 2: Upload to Shopify theme
    asset_key = 'assets/product-recommendations-matrix.js'
    success = upload_asset_to_theme(asset_key, content)

    if not success:
        print("\n❌ DEPLOYMENT FAILED: Upload error")
        return False

    # Step 3: Verify deployment
    verified = verify_asset_deployed(asset_key)

    if not verified:
        print("\n❌ DEPLOYMENT FAILED: Verification failed")
        return False

    # Success
    print("\n" + "=" * 80)
    print("✅ DEPLOYMENT COMPLETE")
    print("=" * 80)
    print("Asset deployed: assets/product-recommendations-matrix.js")
    print("Live URL: https://cdn.shopify.com/s/files/1/0636/8306/0061/files/product-recommendations-matrix.js")
    print("\nNEXT STEPS (Manual):")
    print("1. Create snippets/smart-recommendations.liquid component (15 hours)")
    print("2. Integrate into product pages (15 hours)")
    print("3. Add Shopify Flow email triggers (5 hours)")
    print("4. Create product quiz (15 hours)")
    print("=" * 80)

    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
