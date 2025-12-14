#!/usr/bin/env python3
"""
Push bundle builder assets directly to Shopify theme via Admin API
"""
import os
import base64
import requests
from dotenv import load_dotenv

# Load credentials
load_dotenv('.env.admin')

SHOP = os.getenv('SHOPIFY_STORE_DOMAIN')
TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
THEME_ID = '140069830733'

API_URL = f'https://{SHOP}/admin/api/2024-10/themes/{THEME_ID}/assets.json'

HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type': 'application/json'
}

def upload_asset(key, file_path):
    """Upload a single asset to Shopify theme"""
    print(f"\n📤 Uploading: {key}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Base64 encode for binary safety
    encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    payload = {
        'asset': {
            'key': key,
            'attachment': encoded
        }
    }
    
    response = requests.put(API_URL, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"✅ SUCCESS: {key}")
        return True
    else:
        print(f"❌ FAILED: {key}")
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def main():
    print("=" * 60)
    print("SHOPIFY ASSET UPLOAD - BUNDLE BUILDER")
    print("=" * 60)
    print(f"Store: {SHOP}")
    print(f"Theme ID: {THEME_ID}")
    print("=" * 60)
    
    assets = [
        ('assets/bundle-builder-combined.js', 'assets/bundle-builder-combined.js'),
        ('assets/bundle-builder-combined.css', 'assets/bundle-builder-combined.css'),
    ]
    
    results = []
    for file_path, key in assets:
        if os.path.exists(file_path):
            success = upload_asset(key, file_path)
            results.append((key, success))
        else:
            print(f"❌ FILE NOT FOUND: {file_path}")
            results.append((key, False))
    
    print("\n" + "=" * 60)
    print("UPLOAD SUMMARY")
    print("=" * 60)
    for key, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {key}")
    
    all_success = all(success for _, success in results)
    if all_success:
        print("\n🎉 ALL FILES UPLOADED SUCCESSFULLY!")
        print("🌐 Check: https://www.alphamedical.shop/pages/bundle-creator")
    else:
        print("\n⚠️  SOME UPLOADS FAILED - CHECK ERRORS ABOVE")
    
    return 0 if all_success else 1

if __name__ == '__main__':
    exit(main())
