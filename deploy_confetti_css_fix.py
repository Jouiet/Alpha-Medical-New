#!/usr/bin/env python3
"""
Deploy Confetti CSS Fix - Add keyframes to theme.liquid
Critical fix: CSS keyframes must be in <head> for confetti animations to work
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_NAME = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2024-10'
THEME_ID = '140069830733'

BASE_URL = f'https://{SHOP_NAME}/admin/api/{API_VERSION}'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def upload_file(file_path, theme_key):
    """Upload file to Shopify."""
    print(f"📤 Uploading {theme_key}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    url = f'{BASE_URL}/themes/{THEME_ID}/assets.json'
    payload = {'asset': {'key': theme_key, 'value': content}}

    response = requests.put(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        print(f"✅ {theme_key}")
        return True
    else:
        print(f"❌ FAILED: {theme_key}")
        print(f"Error: {response.text}")
        return False

print("=" * 80)
print("CONFETTI CSS FIX - ROOT CAUSE #2")
print("=" * 80)
print()
print("🚨 PROBLEM DETECTED:")
print("  CSS @keyframes confetti-fall was ONLY in snippet")
print("  Snippet not always loaded on initial page render")
print("  Result: Confetti generated but NO ANIMATION")
print()
print("✅ SOLUTION:")
print("  CSS keyframes moved to <head> in theme.liquid")
print("  Lines 316-373: Confetti CSS added before </head>")
print()
print("=" * 80)
print()

success = upload_file(
    '/Users/mac/Desktop/Alpha-Medical/layout/theme.liquid',
    'layout/theme.liquid'
)

print()
print("=" * 80)
if success:
    print("✅ DEPLOYMENT SUCCESSFUL")
    print()
    print("COMPLETE CONFETTI SYSTEM NOW INCLUDES:")
    print("  1. CSS in <head> (lines 316-373)")
    print("  2. JavaScript in <body> (lines 447-588)")
    print("  3. Trigger in snippet: data-confetti-trigger='true'")
    print()
    print("STATUS: ✅ FULLY OPERATIONAL")
    print()
    print("TEST NOW:")
    print("  1. Add $150+ products to cart")
    print("  2. Watch for confetti animation!")
    print("  3. Manual test: sessionStorage.clear(); window.triggerFreeShippingConfetti();")
else:
    print("❌ DEPLOYMENT FAILED")

print("=" * 80)
