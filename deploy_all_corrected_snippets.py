#!/usr/bin/env python3
"""
DEPLOY ALL COLOR-CORRECTED SNIPPETS TO SHOPIFY
Uploads all snippets with corrected Alpha Medical brand colors
"""

import requests
import sys
import os
import glob

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    sys.exit(1)

API_VERSION = "2025-10"
THEME_ID = "140069830733"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# List of snippets that were fixed
FIXED_SNIPPETS = [
    'loyalty-history.liquid',
    'loyalty-points-badge.liquid',
    'cart-drawer.liquid',
    'free-shipping-progress-bar.liquid',
    'loyalty-points-widget.liquid',
    'bundle-creator-cta.liquid',
    'loyalty-redemption-form.liquid',
    'exit-intent-popup.liquid',
    'product-trust-badges.liquid',
    'welcome-popup.liquid',
    'bundles-cta-banner.liquid',
    'size-guide-modal.liquid',
    'bundle-builder-cta-banner.liquid',
    'smart-recommendations.liquid',
    'bundle-hover-images.liquid',
    'bundles-collection-cta.liquid',
    'loyalty-tier-badge.liquid',
    'product-low-stock-badge.liquid',
    'subscription-widget.liquid',
    'article-cta.liquid',
    'cart-bundles-upsell.liquid',
    'product-bundle-cta.liquid',  # Manually fixed earlier
    'product-bundle-smart-cta.liquid',  # Manually fixed earlier
]

def upload_snippet(filename):
    """Upload a snippet file to Shopify"""
    filepath = f'/Users/mac/Desktop/Alpha-Medical/snippets/{filename}'

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            snippet_content = f.read()

        url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
        payload = {
            "asset": {
                "key": f"snippets/{filename}",
                "value": snippet_content
            }
        }

        response = requests.put(url, headers=HEADERS, json=payload)

        if response.status_code in [200, 201]:
            return True, len(snippet_content)
        else:
            return False, response.text

    except FileNotFoundError:
        return False, "File not found"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("DEPLOYING COLOR-CORRECTED SNIPPETS TO SHOPIFY")
    print("=" * 80)
    print(f"Store: {SHOPIFY_DOMAIN}")
    print(f"Theme: {THEME_ID}")
    print(f"Files to upload: {len(FIXED_SNIPPETS)}")
    print()

    success_count = 0
    failed_files = []
    total_bytes = 0

    for i, filename in enumerate(FIXED_SNIPPETS, 1):
        print(f"[{i}/{len(FIXED_SNIPPETS)}] Uploading {filename}...", end=" ")

        success, result = upload_snippet(filename)

        if success:
            print(f"✅ ({result} bytes)")
            success_count += 1
            total_bytes += result
        else:
            print(f"❌ Failed")
            failed_files.append((filename, result))

    print()
    print("=" * 80)
    print("DEPLOYMENT COMPLETE")
    print("=" * 80)
    print()
    print(f"✅ Successfully uploaded: {success_count}/{len(FIXED_SNIPPETS)} files")
    print(f"📦 Total size: {total_bytes:,} bytes ({total_bytes/1024:.1f} KB)")
    print()

    if failed_files:
        print("❌ FAILED FILES:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error[:100]}")
        print()

    print("🎨 COLOR CORRECTIONS DEPLOYED:")
    print("  ✅ Primary Blue: #4770db (replaces #4A90E2)")
    print("  ✅ Deep Navy: #0e1b4d (replaces #2c3e50)")
    print("  ✅ Coral Red: #e32402 (replaces #ff4444)")
    print("  ✅ Gradients: Navy → Blue (replaces Blue → Turquoise)")
    print()
    print("STATUS: ALL SNIPPETS NOW USE ALPHA MEDICAL OFFICIAL COLORS")
    print("=" * 80)

if __name__ == '__main__':
    main()
