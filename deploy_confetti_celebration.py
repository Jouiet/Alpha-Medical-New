#!/usr/bin/env python3
"""
Deploy Free Shipping Confetti Celebration to Shopify
Uploads updated snippets/free-shipping-progress-bar.liquid with confetti system
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
    print("CONFETTI CELEBRATION DEPLOYMENT - Option A: Non-blocking")
    print("=" * 80)
    print()

    # File to upload
    file_path = '/Users/mac/Desktop/Alpha-Medical/snippets/free-shipping-progress-bar.liquid'
    theme_key = 'snippets/free-shipping-progress-bar.liquid'

    # Upload
    success = upload_file(file_path, theme_key)

    print()
    print("=" * 80)
    if success:
        print("✅ DEPLOYMENT SUCCESSFUL")
        print()
        print("🎉 CONFETTI CELEBRATION SYSTEM FEATURES:")
        print()
        print("TRIGGER:")
        print("- Activates when cart reaches $150 (free shipping threshold)")
        print("- Triggers on page load if already qualified")
        print("- Triggers when adding item that crosses threshold")
        print()
        print("ANIMATION:")
        print("- 50 confetti pieces (squares, circles, triangles)")
        print("- 8 brand colors (Alpha Medical blue + celebration palette)")
        print("- 2-3.5s fall duration with random drift & rotation")
        print("- Staggered launch (0-300ms delays)")
        print()
        print("NON-BLOCKING DESIGN:")
        print("- position: fixed (overlay)")
        print("- pointer-events: none (clicks pass through)")
        print("- z-index: 9999 (above all content)")
        print("- Auto-cleanup after 4 seconds")
        print()
        print("SMART BEHAVIOR:")
        print("- Only celebrates once per 10 seconds (prevents spam)")
        print("- sessionStorage tracking (no repeated celebrations)")
        print("- Works on cart drawer AND cart page")
        print()
        print("PERFORMANCE:")
        print("- Pure CSS/JS (no external dependencies)")
        print("- ~100 lines of code (lightweight)")
        print("- Hardware-accelerated animations")
        print("- Mobile optimized")
        print()
        print("TEST IT:")
        print("1. Add products totaling $150+ to cart")
        print("2. Watch confetti celebration! 🎊")
        print("3. Verify clicks work during animation (non-blocking)")
    else:
        print("❌ DEPLOYMENT FAILED")
    print("=" * 80)

if __name__ == '__main__':
    main()
