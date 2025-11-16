#!/usr/bin/env python3
"""
Deploy optimized sticky add-to-cart widget to Shopify
- Width reduced by 1.3 (23% narrower)
- UX optimized by 1.2 (20% larger buttons, padding, icons)
"""

import os
import requests

# Load credentials from .env.admin
SHOP_URL = 'azffej-as.myshopify.com'
THEME_ID = '140069830733'  # Alpha-Medical-New/main

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                ACCESS_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ ERROR: Failed to load credentials from .env.admin")
    exit(1)

if not ACCESS_TOKEN:
    print("❌ ERROR: SHOPIFY_ADMIN_ACCESS_TOKEN not found in .env.admin")
    exit(1)

headers = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

base_url = f'https://{SHOP_URL}/admin/api/2024-01/themes/{THEME_ID}/assets.json'

def upload_snippet():
    """Upload optimized sticky-add-to-cart.liquid snippet"""

    snippet_path = '/Users/mac/Desktop/Alpha-Medical/snippets/sticky-add-to-cart.liquid'

    if not os.path.exists(snippet_path):
        print(f"❌ Snippet not found: {snippet_path}")
        return False

    with open(snippet_path, 'r', encoding='utf-8') as f:
        content = f.read()

    payload = {
        'asset': {
            'key': 'snippets/sticky-add-to-cart.liquid',
            'value': content
        }
    }

    print(f"📤 Uploading snippets/sticky-add-to-cart.liquid...")
    response = requests.put(base_url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        print(f"✅ Uploaded: snippets/sticky-add-to-cart.liquid ({len(content)} bytes)")
        return True
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 60)
    print("STICKY WIDGET OPTIMIZATION DEPLOYMENT")
    print("=" * 60)
    print(f"Shop: {SHOP_URL}")
    print(f"Theme: {THEME_ID}")
    print("")
    print("CHANGES:")
    print("  • Width reduced by 1.43 (original ÷1.3, then -10%):")
    print("    - Desktop: 380px → 263px (-31%)")
    print("    - Tablet: 340px → 236px (-31%)")
    print("    - Mobile: 300px → 208px (-31%)")
    print("")
    print("  • UX optimized by 1.2 (conversion focus):")
    print("    - Buttons: +20% larger (better tap targets)")
    print("    - Padding: +20% spacious (easier to read)")
    print("    - Icons: +22% bigger (18px → 22px)")
    print("    - Price: +21% (14px → 17px)")
    print("    - Button font: +23% (13px → 16px)")
    print("")

    success = upload_snippet()

    print("")
    print("=" * 60)
    if success:
        print("✅ DEPLOYMENT SUCCESSFUL")
        print("")
        print("VERIFICATION:")
        print("  1. Visit any product page:")
        print("     https://www.alphamedical.shop/products/[any-product]")
        print("  2. Scroll down until main add-to-cart is out of view")
        print("  3. Sticky widget should appear on right side")
        print("  4. Verify widget is narrower and buttons are larger")
        print("")
        print("KEY IMPROVEMENTS:")
        print("  ✅ Reduced visual clutter (23% narrower)")
        print("  ✅ Better mobile UX (larger touch targets)")
        print("  ✅ Improved conversion (more prominent CTA)")
        print("  ✅ Enhanced readability (larger text)")
    else:
        print("❌ DEPLOYMENT FAILED")
        print("")
        print("TROUBLESHOOTING:")
        print("  1. Check .env file has SHOPIFY_ADMIN_ACCESS_TOKEN")
        print("  2. Verify theme ID is correct: 140069830733")
        print("  3. Check API access token permissions")
    print("=" * 60)

if __name__ == '__main__':
    main()
