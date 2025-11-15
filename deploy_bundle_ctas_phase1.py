"""
Deploy Bundle CTAs Phase 1 to Shopify
Uploads all bundle CTA files and modified templates
Alpha Medical Care - 2025
"""

import os
import json
import requests

# Load credentials from .env.admin
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials from .env.admin")
    exit(1)

API_VERSION = "2025-10"
THEME_ID = '140069830733'  # Alpha-Medical-New/main theme

# API endpoint
BASE_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"

headers = {
    'X-Shopify-Access-Token': SHOPIFY_TOKEN,
    'Content-Type': 'application/json'
}

def upload_asset(asset_key, file_path):
    """Upload a single asset to Shopify theme"""
    print(f"\n📤 Uploading {asset_key}...")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        payload = {
            "asset": {
                "key": asset_key,
                "value": content
            }
        }

        response = requests.put(BASE_URL, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            print(f"✅ {asset_key} uploaded successfully")
            return True
        else:
            print(f"❌ Error uploading {asset_key}: {response.status_code}")
            print(f"   Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Exception uploading {asset_key}: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("BUNDLE CTAs PHASE 1 - SHOPIFY DEPLOYMENT")
    print("=" * 60)

    # Define files to upload
    files_to_upload = [
        # New files
        ("assets/bundle-product-mapping.js", "assets/bundle-product-mapping.js"),
        ("snippets/product-bundle-smart-cta.liquid", "snippets/product-bundle-smart-cta.liquid"),
        ("snippets/cart-bundles-upsell.liquid", "snippets/cart-bundles-upsell.liquid"),

        # Modified templates/sections
        ("templates/product.json", "templates/product.json"),
        ("sections/main-cart-footer.liquid", "sections/main-cart-footer.liquid"),
        ("snippets/cart-drawer.liquid", "snippets/cart-drawer.liquid"),
    ]

    results = []
    for asset_key, file_path in files_to_upload:
        success = upload_asset(asset_key, file_path)
        results.append((asset_key, success))

    # Summary
    print("\n" + "=" * 60)
    print("DEPLOYMENT SUMMARY")
    print("=" * 60)

    successful = [name for name, success in results if success]
    failed = [name for name, success in results if not success]

    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    for name in successful:
        print(f"   - {name}")

    if failed:
        print(f"\n❌ Failed: {len(failed)}/{len(results)}")
        for name in failed:
            print(f"   - {name}")
    else:
        print("\n🎉 ALL FILES DEPLOYED SUCCESSFULLY!")
        print("\n📍 NEXT STEPS:")
        print("   1. Test product pages: Visit any product with bundles")
        print("   2. Test cart page: Add items and check cart upsell")
        print("   3. Test cart drawer: Open cart drawer and verify CTA")
        print("   4. Verify GA4 tracking events in browser console")
        print("\n🔗 URLS TO TEST:")
        print("   - Product: https://www.alphamedical.shop/products/posture-corrector")
        print("   - Cart: https://www.alphamedical.shop/cart")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
