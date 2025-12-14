#!/usr/bin/env python3
"""
Upload bundle-builder-combined.liquid with CSS fix
"""
import os
import base64
import requests
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

def upload_liquid():
    file_path = 'sections/bundle-builder-combined.liquid'
    key = 'sections/bundle-builder-combined.liquid'
    
    print(f"📤 Uploading: {key}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
        print(f"❌ FAILED: {response.status_code}")
        print(f"   {response.text}")
        return False

if __name__ == '__main__':
    print("="*60)
    print("CRITICAL FIX: Upload Liquid with CSS reference")
    print("="*60)
    upload_liquid()
    print("="*60)
    print("✅ DONE - CSS will now load on page!")
    print("🌐 Test: alphamedical.shop/pages/bundle-creator")
    print("="*60)
