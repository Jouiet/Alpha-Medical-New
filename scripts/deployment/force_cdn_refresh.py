#!/usr/bin/env python3
"""
Force Shopify CDN cache purge by re-uploading assets
"""
import os
import base64
import requests
import time
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP = os.getenv('SHOPIFY_STORE_DOMAIN')
TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
THEME_ID = '140069830733'

API_URL = f'https://{SHOP}/admin/api/2024-10/themes/{THEME_ID}/assets.json'
HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type': 'application/json'
}

def force_upload(key, file_path):
    """Upload asset and force CDN refresh"""
    print(f"\n🔄 Force uploading: {key}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add timestamp comment to force new version
    timestamp_comment = f"\n/* Updated: {int(time.time())} */\n"
    if key.endswith('.css'):
        content = timestamp_comment + content
    elif key.endswith('.js'):
        content = f"// Updated: {int(time.time())}\n" + content
    
    encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    payload = {
        'asset': {
            'key': key,
            'attachment': encoded
        }
    }
    
    response = requests.put(API_URL, json=payload, headers=HEADERS)
    
    if response.status_code == 200:
        print(f"✅ UPLOADED: {key}")
        
        # Verify it's accessible
        asset_data = response.json()['asset']
        if 'public_url' in asset_data:
            print(f"   CDN URL: {asset_data['public_url']}")
        
        return True
    else:
        print(f"❌ FAILED: {response.status_code}")
        print(f"   {response.text}")
        return False

def main():
    print("=" * 70)
    print("FORCE CDN CACHE PURGE - Bundle Builder Assets")
    print("=" * 70)
    
    assets = [
        ('assets/bundle-builder-combined.css', 'assets/bundle-builder-combined.css'),
        ('assets/bundle-builder-combined.js', 'assets/bundle-builder-combined.js'),
    ]
    
    for file_path, key in assets:
        if os.path.exists(file_path):
            force_upload(key, file_path)
            time.sleep(2)  # Wait between uploads
        else:
            print(f"❌ NOT FOUND: {file_path}")
    
    print("\n" + "=" * 70)
    print("✅ FORCE UPLOAD COMPLETE")
    print("🌐 Test: https://www.alphamedical.shop/pages/bundle-creator")
    print("💡 Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)")
    print("=" * 70)

if __name__ == '__main__':
    main()
