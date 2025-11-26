#!/usr/bin/env python3
"""
Deploy Email Capture Popups to Shopify
Uploads welcome-popup.liquid and exit-intent-popup.liquid to live theme
"""

import os
import requests
import json
import sys

# Load Shopify credentials from .env.admin (gitignored)
SHOPIFY_STORE = None
SHOPIFY_ACCESS_TOKEN = None

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_ACCESS_TOKEN = line.split('=', 1)[1].strip()
            elif line.startswith('SHOPIFY_STORE_DOMAIN='):
                SHOPIFY_STORE = line.split('=', 1)[1].strip()
except FileNotFoundError:
    print("❌ ERROR: .env.admin not found. Create it with:")
    print("   SHOPIFY_ADMIN_ACCESS_TOKEN=your_token")
    print("   SHOPIFY_STORE_DOMAIN=your_store.myshopify.com")
    sys.exit(1)

if not SHOPIFY_STORE or not SHOPIFY_ACCESS_TOKEN:
    print("❌ ERROR: Missing credentials in .env.admin")
    sys.exit(1)

THEME_ID = "140069830733"
API_VERSION = "2024-10"

BASE_URL = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def upload_asset(asset_key, file_path):
    """Upload a single asset to Shopify theme"""
    print(f"\n📤 Uploading {asset_key}...")

    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Prepare API payload
    payload = {
        "asset": {
            "key": asset_key,
            "value": content
        }
    }

    # Upload to Shopify
    url = f"{BASE_URL}/themes/{THEME_ID}/assets.json"
    response = requests.put(url, headers=HEADERS, json=payload)

    if response.status_code in [200, 201]:
        print(f"   ✅ SUCCESS: {asset_key} uploaded")
        asset_data = response.json().get('asset', {})
        print(f"   Size: {asset_data.get('size', 0)} bytes")
        print(f"   Updated: {asset_data.get('updated_at', 'N/A')}")
        return True
    else:
        print(f"   ❌ FAILED: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def main():
    print("=" * 60)
    print("SHOPIFY EMAIL POPUP DEPLOYMENT")
    print("=" * 60)
    print(f"Store: {SHOPIFY_STORE}")
    print(f"Theme ID: {THEME_ID}")

    # Files to upload
    files = [
        ("snippets/welcome-popup.liquid", "snippets/welcome-popup.liquid"),
        ("snippets/exit-intent-popup.liquid", "snippets/exit-intent-popup.liquid")
    ]

    results = []
    for asset_key, file_path in files:
        success = upload_asset(asset_key, file_path)
        results.append((asset_key, success))

    # Summary
    print("\n" + "=" * 60)
    print("DEPLOYMENT SUMMARY")
    print("=" * 60)

    for asset_key, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {asset_key}")

    total = len(results)
    successful = sum(1 for _, success in results if success)

    print(f"\nTotal: {successful}/{total} files deployed successfully")

    if successful == total:
        print("\n🎉 All popups deployed! Lead Capture should now be active.")
        print("   Verify at: https://alphamedical.shop")
        print("   Welcome popup: Shows after 10 seconds on first visit")
        print("   Exit intent popup: Shows on mouse leave (desktop) or 50% scroll (mobile)")
    else:
        print(f"\n⚠️  {total - successful} file(s) failed to deploy")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
