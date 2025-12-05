#!/usr/bin/env python3
"""Verify schema markup deployment on Shopify theme"""

import requests
import json

SHOPIFY_ADMIN_ACCESS_TOKEN = '***REMOVED***'
SHOPIFY_STORE_DOMAIN = 'azffej-as.myshopify.com'
THEME_ID = '140069830733'

headers = {'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN}

print("=" * 70)
print("SCHEMA MARKUP DEPLOYMENT VERIFICATION")
print("=" * 70)
print()

# Check if main-collection-banner.liquid exists and contains schema
print("1. Checking sections/main-collection-banner.liquid...")
url = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10/themes/{THEME_ID}/assets.json'
params = {'asset[key]': 'sections/main-collection-banner.liquid'}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    asset = response.json().get('asset', {})
    content = asset.get('value', '')

    has_collection_page = '"@type": "CollectionPage"' in content
    has_item_list = '"@type": "ItemList"' in content

    print(f"   ✅ File exists ({len(content)} chars)")
    print(f"   {'✅' if has_collection_page else '❌'} Contains CollectionPage schema")
    print(f"   {'✅' if has_item_list else '❌'} Contains ItemList schema")
else:
    print(f"   ❌ Error fetching file: HTTP {response.status_code}")

print()

# Check collection template configuration
print("2. Checking templates/collection.json...")
params = {'asset[key]': 'templates/collection.json'}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    asset = response.json().get('asset', {})
    template_json = json.loads(asset.get('value', '{}'))
    sections = template_json.get('sections', {})

    print(f"   ✅ Template exists")
    print(f"   Sections defined: {len(sections)}")

    # Check if main-collection-banner is in the template
    banner_section = None
    for key, section in sections.items():
        if section.get('type') == 'main-collection-banner':
            banner_section = key
            break

    if banner_section:
        print(f"   ✅ main-collection-banner section found (key: {banner_section})")
    else:
        print(f"   ❌ main-collection-banner section NOT in template")
        print(f"   Sections in template:")
        for key, section in list(sections.items())[:5]:
            print(f"      - {key}: {section.get('type', 'unknown')}")
else:
    print(f"   ❌ Error fetching template: HTTP {response.status_code}")

print()
print("=" * 70)
print("CONCLUSION")
print("=" * 70)

if has_collection_page and has_item_list and banner_section:
    print("✅ Schema markup deployed successfully!")
    print()
    print("If schema not visible on live site, possible causes:")
    print("1. CDN cache (wait 5-10 more minutes)")
    print("2. Collection using different template (check Shopify admin)")
    print("3. Browser cache (hard refresh: Cmd+Shift+R)")
else:
    print("⚠️ Deployment issues detected - see details above")
