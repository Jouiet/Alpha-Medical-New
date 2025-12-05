#!/usr/bin/env python3
"""
CHECK: Product Template Integration
Date: 2025-11-20
Purpose: Verify if smart-recommendations snippet is integrated in product template
"""

import os
import requests

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

SHOP = "azffej-as.myshopify.com"
THEME_ID = "140069830733"
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN}

print("=" * 80)
print("CHECK: Product Template Integration")
print("=" * 80)

# Fetch product template
print("Fetching templates/product.json...\n")

response = requests.get(
    f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]=templates/product.json",
    headers=HEADERS
)

if response.status_code != 200:
    print(f"❌ Failed to fetch template: {response.status_code}")
    exit(1)

template = response.json().get('asset', {}).get('value', '')

if not template:
    print("❌ Template is empty or not found")
    exit(1)

print(f"✅ Fetched template ({len(template)} bytes)\n")

# Check if smart-recommendations is integrated
if 'smart-recommendations' in template:
    print("✅ INTEGRATED: smart-recommendations snippet is referenced in template")
    print()

    # Find the exact line
    for i, line in enumerate(template.split('\n'), 1):
        if 'smart-recommendations' in line:
            print(f"   Line {i}: {line.strip()}")
    print()
else:
    print("❌ NOT INTEGRATED: smart-recommendations snippet is NOT referenced")
    print()
    print("ACTION REQUIRED:")
    print("1. Add {% render 'smart-recommendations', product: product %} to product template")
    print("2. Recommended location: After product description, before footer")
    print()

    # Check template structure
    import json
    try:
        template_json = json.loads(template)
        sections = template_json.get('sections', {})
        print("Current template sections:")
        for section_id, section_data in sections.items():
            section_type = section_data.get('type', 'unknown')
            print(f"  - {section_id}: {section_type}")
    except:
        print("⚠️  Could not parse template JSON")

    exit(1)
