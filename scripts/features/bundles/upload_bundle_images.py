#!/usr/bin/env python3
"""
UPLOAD BUNDLE IMAGES TO SHOPIFY

Uploads images for the 10 Complete Care Kit bundles that currently have no images.

Usage:
    1. Create folder: bundle_images/
    2. Put 10 images in that folder with exact names (see BUNDLE_IMAGES_CREATION_GUIDE.md)
    3. Run: python3 upload_bundle_images.py

Requirements:
    pip install requests

Author: Claude Code
Date: 2025-11-28
"""

import os
import json
import base64
import requests
from pathlib import Path

# Load credentials
env_file = Path(__file__).parent / '.env.admin'
SHOPIFY_TOKEN = None
SHOPIFY_DOMAIN = None

with open(env_file, 'r') as f:
    for line in f:
        if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN'):
            SHOPIFY_TOKEN = line.split('=')[1].strip()
        elif line.startswith('SHOPIFY_STORE_DOMAIN'):
            SHOPIFY_DOMAIN = line.split('=')[1].strip()

# Bundle ID mapping (product_id → image filename)
BUNDLE_MAPPING = {
    7620850876493: 'active-athlete-sports-enthusiast',
    7620851105869: 'active-athlete-knee-support-kit',
    7620851171405: 'beauty-wellness-premium-facial-therapy-kit',
    7620851007565: 'beauty-wellness-enthusiast',
    7620851040333: 'comprehensive-therapy-user',
    7620850942029: 'elderly-mobility-support',
    7620851073101: 'foot-care-bunion-relief',
    7620851138637: 'office-worker-back-neck-relief-kit',
    7620850909261: 'office-worker-chronic-pain',
    7620850974797: 'post-injury-post-surgery-recovery'
}

def upload_product_image(product_id, image_path):
    """Upload image to product via Shopify API"""

    # Read image file
    with open(image_path, 'rb') as img_file:
        image_data = base64.b64encode(img_file.read()).decode('utf-8')

    # Determine file extension
    ext = image_path.suffix.lower()
    if ext == '.jpg' or ext == '.jpeg':
        mime_type = 'image/jpeg'
    elif ext == '.png':
        mime_type = 'image/png'
    else:
        print(f'  ⚠️  Unknown image type: {ext}')
        return False

    # Upload via API
    url = f'https://{SHOPIFY_DOMAIN}/admin/api/2024-10/products/{product_id}/images.json'

    headers = {
        'X-Shopify-Access-Token': SHOPIFY_TOKEN,
        'Content-Type': 'application/json'
    }

    payload = {
        'image': {
            'attachment': image_data,
            'filename': image_path.name
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 201:
            result = response.json()
            image_id = result['image']['id']
            print(f'  ✅ Uploaded successfully (Image ID: {image_id})')
            return True
        else:
            print(f'  ❌ Upload failed: {response.status_code}')
            print(f'     Response: {response.text[:200]}')
            return False

    except Exception as e:
        print(f'  ❌ ERROR: {e}')
        return False

def main():
    print('📤 UPLOAD BUNDLE IMAGES TO SHOPIFY')
    print('=' * 80)
    print(f'Store: {SHOPIFY_DOMAIN}')
    print('')

    # Check bundle_images folder exists
    images_folder = Path(__file__).parent / 'bundle_images'

    if not images_folder.exists():
        print('❌ ERROR: bundle_images/ folder not found!')
        print('   Create the folder and add your 10 bundle images first.')
        print('   See: BUNDLE_IMAGES_CREATION_GUIDE.md for details')
        return 1

    # Find images
    print(f'📁 Looking for images in: {images_folder}')
    print('')

    success_count = 0
    failed_count = 0
    missing_count = 0

    for product_id, base_filename in BUNDLE_MAPPING.items():
        # Try different extensions
        image_path = None
        for ext in ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']:
            test_path = images_folder / f'{base_filename}{ext}'
            if test_path.exists():
                image_path = test_path
                break

        if not image_path:
            print(f'❌ MISSING: {base_filename}.[png|jpg]')
            missing_count += 1
            continue

        # Get product title for display
        try:
            headers = {'X-Shopify-Access-Token': SHOPIFY_TOKEN}
            url = f'https://{SHOPIFY_DOMAIN}/admin/api/2024-10/products/{product_id}.json?fields=title'
            response = requests.get(url, headers=headers, timeout=10)
            product_title = response.json()['product']['title'][:50]
        except:
            product_title = f'Product {product_id}'

        print(f'{product_title}')
        print(f'  Image: {image_path.name} ({image_path.stat().st_size / 1024:.1f} KB)')

        # Upload
        if upload_product_image(product_id, image_path):
            success_count += 1
        else:
            failed_count += 1

        print('')

    # Summary
    print('=' * 80)
    print('📊 UPLOAD SUMMARY')
    print(f'  ✅ Uploaded: {success_count}/10')
    print(f'  ❌ Failed: {failed_count}/10')
    print(f'  ⚠️  Missing: {missing_count}/10')
    print('')

    if success_count == 10:
        print('🎉 ALL BUNDLE IMAGES UPLOADED!')
        print('   All 10 Complete Care Kits now have images.')
        print('   Bundles are now FULLY FUNCTIONAL and ready to sell!')
        return 0
    elif success_count > 0:
        print('⚠️  PARTIAL SUCCESS')
        print(f'   {10 - success_count} bundles still need images')
        return 1
    else:
        print('❌ NO IMAGES UPLOADED')
        print('   Check the bundle_images/ folder and image filenames')
        return 1

if __name__ == '__main__':
    exit(main())
