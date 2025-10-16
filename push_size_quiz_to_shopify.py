#!/usr/bin/env python3
"""
Push Size Quiz files to Shopify live theme via Admin API
Uses Asset API to upload theme files programmatically
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
THEME_ID = "140069830733"  # Alpha-Medical-New/main (live theme)

REST_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10"

headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN
}

def upload_asset(theme_id, key, value):
    """Upload a theme asset via Admin API"""
    url = f"{REST_URL}/themes/{theme_id}/assets.json"

    data = {
        "asset": {
            "key": key,
            "value": value
        }
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        print(f"✅ Uploaded: {key}")
        return True
    else:
        print(f"❌ Error uploading {key}: {response.status_code}")
        print(response.json())
        return False

def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("=" * 80)
    print("PUSHING SIZE QUIZ TO SHOPIFY LIVE THEME")
    print("=" * 80)
    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print(f"Theme ID: {THEME_ID} (Alpha-Medical-New/main - LIVE)")
    print()

    files_to_upload = [
        {
            "path": "/Users/mac/Desktop/Alpha-Medical/snippets/size-quiz.liquid",
            "key": "snippets/size-quiz.liquid"
        },
        {
            "path": "/Users/mac/Desktop/Alpha-Medical/templates/page.size-quiz.liquid",
            "key": "templates/page.size-quiz.liquid"
        }
    ]

    success_count = 0

    for file_info in files_to_upload:
        print(f"\n📤 Uploading: {file_info['key']}")
        print(f"   Local path: {file_info['path']}")

        # Read file content
        try:
            content = read_file(file_info['path'])
            file_size = len(content)
            print(f"   File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
            continue

        # Upload to Shopify
        if upload_asset(THEME_ID, file_info['key'], content):
            success_count += 1
        else:
            print(f"   ❌ Upload failed")

    print("\n" + "=" * 80)
    print(f"UPLOAD COMPLETE: {success_count}/{len(files_to_upload)} files uploaded successfully")
    print("=" * 80)

    if success_count == len(files_to_upload):
        print("\n✅ SIZE QUIZ IS NOW LIVE ON PRODUCTION!")
        print(f"   View at: https://{SHOPIFY_STORE_DOMAIN}/pages/size-quiz")
        return True
    else:
        print(f"\n⚠️ {len(files_to_upload) - success_count} files failed to upload")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
