#!/usr/bin/env python3
"""
Deploy Session 69 schema markup files to Shopify theme
Uploads: 2 new snippets + 3 modified sections/templates
"""

import os
import requests
from pathlib import Path

# Load credentials
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN', '***REMOVED***')
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN', 'azffej-as.myshopify.com')
THEME_ID = '140069830733'

# API endpoint
BASE_URL = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10/themes/{THEME_ID}/assets.json'

# Headers
HEADERS = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

# Files to deploy (path relative to repo root)
FILES_TO_DEPLOY = [
    'snippets/schema-author-person.liquid',
    'snippets/schema-organization.liquid',
    'sections/main-article.liquid',
    'sections/main-collection-banner.liquid',
    'templates/page.about-us.liquid'
]

def upload_file(file_path):
    """Upload a single file to Shopify theme"""

    # Read file content
    full_path = Path(file_path)
    if not full_path.exists():
        print(f"❌ File not found: {file_path}")
        return False

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Prepare payload
    payload = {
        'asset': {
            'key': file_path,
            'value': content
        }
    }

    # Upload to Shopify
    print(f"📤 Uploading: {file_path}...", end=" ")

    try:
        response = requests.put(BASE_URL, json=payload, headers=HEADERS)

        if response.status_code == 200:
            print("✅ Success")
            return True
        else:
            print(f"❌ Failed (HTTP {response.status_code})")
            print(f"   Response: {response.text[:200]}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("SCHEMA MARKUP DEPLOYMENT - SESSION 69")
    print("=" * 60)
    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print(f"Theme ID: {THEME_ID}")
    print(f"Files to deploy: {len(FILES_TO_DEPLOY)}")
    print()

    results = []

    for file_path in FILES_TO_DEPLOY:
        success = upload_file(file_path)
        results.append((file_path, success))

    print()
    print("=" * 60)
    print("DEPLOYMENT SUMMARY")
    print("=" * 60)

    successful = sum(1 for _, success in results if success)
    failed = len(results) - successful

    print(f"✅ Successful: {successful}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")

    if failed > 0:
        print("\nFailed files:")
        for file_path, success in results:
            if not success:
                print(f"  - {file_path}")

    print()

    if successful == len(results):
        print("🎉 All schema markup files deployed successfully!")
        print()
        print("Next steps:")
        print("1. Wait 2-3 minutes for Shopify CDN cache to clear")
        print("2. Visit https://alphamedical.shop/collections/knee-braces-supports")
        print("3. Verify CollectionPage + ItemList schema in page source")
        print("4. Test with Google Rich Results Test")
        return 0
    else:
        print("⚠️ Some files failed to deploy. Check errors above.")
        return 1

if __name__ == '__main__':
    exit(main())
