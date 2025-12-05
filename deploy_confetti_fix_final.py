#!/usr/bin/env python3
"""
Deploy Confetti Fix - Script moved to theme.liquid for AJAX compatibility
Uploads:
1. layout/theme.liquid - Contains confetti script (executes on page load)
2. snippets/free-shipping-progress-bar.liquid - Script removed (HTML/CSS only)
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
API_VERSION = '2025-10'

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
    print(f"📤 Uploading {theme_key}...")

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
    print("CONFETTI FIX DEPLOYMENT - ROOT CAUSE RESOLVED")
    print("=" * 80)
    print()
    print("🚨 ROOT CAUSE:")
    print("  Scripts inline dans snippets ne se ré-exécutent PAS lors AJAX cart updates")
    print()
    print("✅ SOLUTION:")
    print("  Script déplacé vers layout/theme.liquid (exécuté 1x au page load)")
    print("  MutationObserver détecte data-confetti-trigger via DOM changes")
    print()
    print("=" * 80)
    print()

    # Files to upload
    files = [
        ('/Users/mac/Desktop/Alpha-Medical/layout/theme.liquid', 'layout/theme.liquid'),
        ('/Users/mac/Desktop/Alpha-Medical/snippets/free-shipping-progress-bar.liquid', 'snippets/free-shipping-progress-bar.liquid')
    ]

    success_count = 0
    for file_path, theme_key in files:
        if upload_file(file_path, theme_key):
            success_count += 1

    print()
    print("=" * 80)
    if success_count == len(files):
        print("✅ DEPLOYMENT SUCCESSFUL - ALL FILES UPLOADED")
        print()
        print("🎯 WHAT CHANGED:")
        print()
        print("layout/theme.liquid (lines 392-533):")
        print("  + Confetti script (140 lines)")
        print("  + Executes ONCE at page load")
        print("  + MutationObserver active for AJAX cart updates")
        print("  + Global function: window.triggerFreeShippingConfetti()")
        print()
        print("snippets/free-shipping-progress-bar.liquid:")
        print("  - Script removed (was causing AJAX incompatibility)")
        print("  + CSS retained (confetti animations)")
        print("  + HTML with data-confetti-trigger='true' retained")
        print()
        print("=" * 80)
        print("🧪 TESTING INSTRUCTIONS:")
        print("=" * 80)
        print()
        print("1. Open Console (F12 → Console tab)")
        print("2. Clear sessionStorage:")
        print("   → sessionStorage.clear()")
        print()
        print("3. Add products totaling $150+ to cart")
        print()
        print("4. Expected console logs:")
        print("   ✅ Confetti system initialized")
        print("   👀 MutationObserver started")
        print("   🛒 cart:updated event detected")
        print("   🎯 Confetti trigger found!")
        print("   ✅ Confetti triggered!")
        print("   📦 Confetti container created")
        print("   🎉 50 confetti pieces launched!")
        print()
        print("5. Expected visual:")
        print("   🎊 50 confetti pieces falling from top")
        print("   ⏱️  2-3.5s animation duration")
        print("   🧹 Auto-cleanup after 4s")
        print()
        print("6. If still not working:")
        print("   → Check Console for errors (red text)")
        print("   → Verify data-confetti-trigger='true' exists:")
        print("     document.querySelector('[data-confetti-trigger=\"true\"]')")
        print("   → Manual trigger test:")
        print("     window.triggerFreeShippingConfetti()")
        print()
        print("=" * 80)
        print("STATUS: ✅ READY FOR TESTING")
        print("=" * 80)
    else:
        print("❌ DEPLOYMENT FAILED - SOME FILES NOT UPLOADED")
        print(f"Success: {success_count}/{len(files)}")
    print()

if __name__ == '__main__':
    main()
