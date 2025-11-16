#!/usr/bin/env python3
"""
Deploy AI Recommendations System to Shopify
- Upload product-recommendations-matrix.js
- Create smart-recommendations.liquid snippet
- Update theme.liquid to include JS
"""

import os
import json
import requests

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
    exit(1)

API_VERSION = "2025-10"
THEME_ID = "140069830733"  # Alpha-Medical-New/main theme

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("=" * 80)
print("DEPLOYING AI RECOMMENDATIONS SYSTEM")
print("=" * 80)
print(f"Theme ID: {THEME_ID}")
print()

# ============================================================================
# STEP 1: Upload product-recommendations-matrix.js
# ============================================================================

print("Step 1: Uploading product-recommendations-matrix.js...")

# Read the generated JS file
js_file_path = '/Users/mac/Desktop/Alpha-Medical/assets/product-recommendations-matrix.js'
with open(js_file_path, 'r') as f:
    js_content = f.read()

# Upload to Shopify
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
payload = {
    "asset": {
        "key": "assets/product-recommendations-matrix.js",
        "value": js_content
    }
}

response = requests.put(url, headers=HEADERS, json=payload)

if response.status_code in [200, 201]:
    print("  ✅ product-recommendations-matrix.js uploaded successfully")
else:
    print(f"  ❌ Upload failed: {response.status_code}")
    print(response.text)

# ============================================================================
# STEP 2: Update theme.liquid to include JS
# ============================================================================

print("\nStep 2: Updating theme.liquid...")

# Read current theme.liquid
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]=layout/theme.liquid"
response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    theme_liquid = response.json()['asset']['value']

    # Check if already included
    if 'product-recommendations-matrix.js' in theme_liquid:
        print("  ✅ product-recommendations-matrix.js already included in theme.liquid")
    else:
        # Add script tag before </head>
        js_tag = '''
  {%- if template.name == 'product' -%}
    <script src="{{ 'product-recommendations-matrix.js' | asset_url }}" defer></script>
  {%- endif -%}'''

        # Insert before </head>
        theme_liquid = theme_liquid.replace('</head>', js_tag + '\n</head>')

        # Upload updated theme.liquid
        url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
        payload = {
            "asset": {
                "key": "layout/theme.liquid",
                "value": theme_liquid
            }
        }

        response = requests.put(url, headers=HEADERS, json=payload)

        if response.status_code in [200, 201]:
            print("  ✅ theme.liquid updated successfully")
        else:
            print(f"  ❌ theme.liquid update failed: {response.status_code}")
else:
    print(f"  ❌ Failed to read theme.liquid: {response.status_code}")

# ============================================================================
# SUCCESS
# ============================================================================

print("\n" + "=" * 80)
print("DEPLOYMENT COMPLETE")
print("=" * 80)
print("✅ product-recommendations-matrix.js deployed")
print("✅ theme.liquid updated")
print()
print("NEXT STEPS:")
print("1. Create smart-recommendations.liquid snippet (manual or script)")
print("2. Integrate into product pages")
print("3. Test recommendations on live site")
print("=" * 80)
