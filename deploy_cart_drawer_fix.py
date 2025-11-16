#!/usr/bin/env python3
"""
Deploy Cart Drawer UX Fix to Shopify
Uploads snippets/cart-drawer.liquid to live theme
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.admin')

# Configuration
SHOP_NAME = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2024-10'

# Theme ID (live theme)
THEME_ID = '140069830733'

# Base URL
BASE_URL = f'https://{SHOP_NAME}/admin/api/{API_VERSION}'

# Headers
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def upload_file(file_path, theme_key):
    """Upload a single file to Shopify theme."""
    print(f"📤 Uploading {file_path} to theme {THEME_ID}...")

    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # API endpoint
    url = f'{BASE_URL}/themes/{THEME_ID}/assets.json'

    # Payload
    payload = {
        'asset': {
            'key': theme_key,
            'value': content
        }
    }

    # Upload
    response = requests.put(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        print(f"✅ Successfully uploaded {theme_key}")
        return True
    else:
        print(f"❌ Failed to upload {theme_key}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def main():
    """Main deployment function."""
    print("=" * 80)
    print("CART DRAWER UX FIX DEPLOYMENT")
    print("=" * 80)
    print()

    # File to upload
    file_path = '/Users/mac/Desktop/Alpha-Medical/snippets/cart-drawer.liquid'
    theme_key = 'snippets/cart-drawer.liquid'

    # Upload
    success = upload_file(file_path, theme_key)

    print()
    print("=" * 80)
    if success:
        print("✅ DEPLOYMENT SUCCESSFUL")
        print()
        print("Changes deployed:")
        print("- Buttons size ÷2 (padding: 0.1875rem 0.375rem, font: 0.625rem)")
        print("- Text size ×1.5 (title: 1.125rem, price: 1.3125rem)")
        print("- Reduced padding and spacing for more compact layout")
        print()
        print("Cart drawer upsells will now take less vertical space,")
        print("making cart items more visible.")
    else:
        print("❌ DEPLOYMENT FAILED")
    print("=" * 80)

if __name__ == '__main__':
    main()
