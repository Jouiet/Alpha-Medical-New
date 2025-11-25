#!/usr/bin/env python3
"""
Check theme.liquid for tracking pixels (Facebook, TikTok, GA4, GTM)
Uses Shopify Admin API to download theme files and search for pixel codes
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_THEME_ID = os.getenv('SHOPIFY_THEME_ID', '140069830733')
API_VERSION = '2024-10'

BASE_URL = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}'
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN
}

def get_theme_asset(asset_key):
    """Get a theme asset content"""
    url = f'{BASE_URL}/themes/{SHOPIFY_THEME_ID}/assets.json?asset[key]={asset_key}'
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json().get('asset', {})
    except Exception as e:
        return {'error': str(e)}

def search_pixel_codes(content, pixel_type):
    """Search for pixel tracking codes in content"""
    if not content:
        return []

    patterns = {
        'facebook': [
            'fbq(',
            'facebook.com/tr',
            '_fbp',
            'FB_PIXEL',
            'facebook-pixel'
        ],
        'tiktok': [
            'ttq.',
            'analytics.tiktok.com',
            'TikTokPixel',
            'tiktok-pixel'
        ],
        'ga4': [
            'gtag(',
            'G-',
            'google-analytics.com/analytics.js',
            'googletagmanager.com/gtag'
        ],
        'gtm': [
            'GTM-',
            'googletagmanager.com/gtm.js',
            'dataLayer'
        ]
    }

    found = []
    for pattern in patterns.get(pixel_type, []):
        if pattern.lower() in content.lower():
            # Find the line with the pattern
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if pattern.lower() in line.lower():
                    found.append({
                        'pattern': pattern,
                        'line_number': i,
                        'line_content': line.strip()[:100]  # First 100 chars
                    })

    return found

def main():
    print("="*80)
    print("THEME PIXEL TRACKING VERIFICATION")
    print("="*80)
    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print(f"Theme ID: {SHOPIFY_THEME_ID}")
    print()

    # Files to check
    files_to_check = [
        'layout/theme.liquid',
        'layout/checkout.liquid',
        'snippets/head-tag.liquid',
        'snippets/footer.liquid'
    ]

    results = {
        'facebook': {'found': False, 'files': [], 'details': []},
        'tiktok': {'found': False, 'files': [], 'details': []},
        'ga4': {'found': False, 'files': [], 'details': []},
        'gtm': {'found': False, 'files': [], 'details': []}
    }

    for file_path in files_to_check:
        print(f"\n{'='*80}")
        print(f"Checking: {file_path}")
        print(f"{'='*80}")

        asset = get_theme_asset(file_path)

        if 'error' in asset:
            print(f"❌ Error: {asset['error']}")
            continue

        if 'value' not in asset:
            print(f"⚠️  File not found or empty")
            continue

        content = asset.get('value', '')
        print(f"✅ File found ({len(content)} characters)")

        # Check each pixel type
        for pixel_type in ['facebook', 'tiktok', 'ga4', 'gtm']:
            matches = search_pixel_codes(content, pixel_type)
            if matches:
                results[pixel_type]['found'] = True
                results[pixel_type]['files'].append(file_path)
                results[pixel_type]['details'].extend(matches)

                print(f"\n  🔍 {pixel_type.upper()} Pixel:")
                for match in matches:
                    print(f"    ✅ Pattern '{match['pattern']}' found at line {match['line_number']}")
                    print(f"       Preview: {match['line_content']}")

    # Summary
    print("\n" + "="*80)
    print("PIXEL TRACKING SUMMARY")
    print("="*80)

    for pixel_type, data in results.items():
        status = "✅ FOUND" if data['found'] else "❌ NOT FOUND"
        print(f"\n{pixel_type.upper()} Pixel: {status}")

        if data['found']:
            print(f"  Files: {', '.join(set(data['files']))}")
            print(f"  Total matches: {len(data['details'])}")

            # Try to extract pixel ID
            if pixel_type == 'facebook':
                for detail in data['details']:
                    if 'fbq(' in detail['line_content'] or 'FB_PIXEL' in detail['line_content']:
                        print(f"  Code preview: {detail['line_content'][:80]}...")
                        break

            elif pixel_type == 'tiktok':
                for detail in data['details']:
                    if 'ttq.' in detail['line_content']:
                        print(f"  Code preview: {detail['line_content'][:80]}...")
                        break

            elif pixel_type == 'ga4':
                for detail in data['details']:
                    if 'G-' in detail['line_content']:
                        print(f"  Code preview: {detail['line_content'][:80]}...")
                        break

            elif pixel_type == 'gtm':
                for detail in data['details']:
                    if 'GTM-' in detail['line_content']:
                        print(f"  Code preview: {detail['line_content'][:80]}...")
                        break

    # Final verdict
    print("\n" + "="*80)
    print("VERDICT")
    print("="*80)

    all_found = all(data['found'] for data in results.values())
    some_found = any(data['found'] for data in results.values())

    if all_found:
        print("✅ ALL TRACKING PIXELS VERIFIED - Full tracking setup")
    elif some_found:
        print("⚠️  PARTIAL TRACKING - Some pixels found, some missing")
        missing = [name.upper() for name, data in results.items() if not data['found']]
        print(f"   Missing: {', '.join(missing)}")
    else:
        print("❌ NO TRACKING PIXELS FOUND - No analytics configured")

    print("\n" + "="*80)

    # Return results for further processing
    return results

if __name__ == '__main__':
    results = main()
