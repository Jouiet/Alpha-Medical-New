#!/usr/bin/env python3
"""
DEPLOY DYNAMIC MERCHANDISING SYSTEM
Date: 2025-11-19
Purpose: Deploy complete dynamic merchandising system to Shopify

DEPLOYMENT:
1. Upload product_matrix_complete.json → assets/
2. Upload dynamic-merchandising.js → assets/
3. Upload product-matrix-loader.liquid → snippets/
4. Update layout/theme.liquid → add script references
5. Verification

FILES:
- product_matrix_complete.json (96 products, 6D scores)
- assets/dynamic-merchandising.js (rotation logic)
- snippets/product-matrix-loader.liquid (data loader)
- layout/theme.liquid (integration)
"""

import os
import requests
import json

# Load credentials from .env.admin
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials from .env.admin")
    exit(1)

SHOP = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
THEME_ID = "140069830733"  # Alpha-Medical-New/main
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

print("=" * 80)
print("DEPLOY DYNAMIC MERCHANDISING SYSTEM")
print("=" * 80)
print(f"Store: {SHOP}")
print(f"Theme: {THEME_ID}")
print(f"API Version: {API_VERSION}\n")

# =========================================================================
# STEP 1: Upload product_matrix_complete.json to assets
# =========================================================================

print("=" * 80)
print("STEP 1: Upload product_matrix_complete.json")
print("=" * 80)

try:
    with open("product_matrix_complete.json", "r") as f:
        matrix_content = f.read()

    print(f"✅ Read product_matrix_complete.json ({len(matrix_content)} bytes)")

    # Upload to assets
    asset_data = {
        "asset": {
            "key": "assets/product_matrix_complete.json",
            "value": matrix_content
        }
    }

    response = requests.put(
        f"{REST_URL}/themes/{THEME_ID}/assets.json",
        headers=HEADERS,
        json=asset_data
    )

    if response.status_code in [200, 201]:
        print("✅ Uploaded to assets/product_matrix_complete.json\n")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"Response: {response.text[:200]}\n")

except Exception as e:
    print(f"❌ Error: {e}\n")

# =========================================================================
# STEP 2: Upload dynamic-merchandising.js to assets
# =========================================================================

print("=" * 80)
print("STEP 2: Upload dynamic-merchandising.js")
print("=" * 80)

try:
    with open("assets/dynamic-merchandising.js", "r") as f:
        js_content = f.read()

    print(f"✅ Read dynamic-merchandising.js ({len(js_content)} bytes)")

    asset_data = {
        "asset": {
            "key": "assets/dynamic-merchandising.js",
            "value": js_content
        }
    }

    response = requests.put(
        f"{REST_URL}/themes/{THEME_ID}/assets.json",
        headers=HEADERS,
        json=asset_data
    )

    if response.status_code in [200, 201]:
        print("✅ Uploaded to assets/dynamic-merchandising.js\n")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"Response: {response.text[:200]}\n")

except Exception as e:
    print(f"❌ Error: {e}\n")

# =========================================================================
# STEP 3: Upload product-matrix-loader.liquid to snippets
# =========================================================================

print("=" * 80)
print("STEP 3: Upload product-matrix-loader.liquid")
print("=" * 80)

try:
    with open("snippets/product-matrix-loader.liquid", "r") as f:
        snippet_content = f.read()

    print(f"✅ Read product-matrix-loader.liquid ({len(snippet_content)} bytes)")

    asset_data = {
        "asset": {
            "key": "snippets/product-matrix-loader.liquid",
            "value": snippet_content
        }
    }

    response = requests.put(
        f"{REST_URL}/themes/{THEME_ID}/assets.json",
        headers=HEADERS,
        json=asset_data
    )

    if response.status_code in [200, 201]:
        print("✅ Uploaded to snippets/product-matrix-loader.liquid\n")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(f"Response: {response.text[:200]}\n")

except Exception as e:
    print(f"❌ Error: {e}\n")

# =========================================================================
# STEP 4: Update layout/theme.liquid
# =========================================================================

print("=" * 80)
print("STEP 4: Update layout/theme.liquid")
print("=" * 80)

try:
    # Fetch current theme.liquid
    response = requests.get(
        f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]=layout/theme.liquid",
        headers=HEADERS
    )

    if response.status_code != 200:
        print(f"❌ Failed to fetch theme.liquid: {response.status_code}")
        exit(1)

    current_theme = response.json().get('asset', {}).get('value', '')
    print(f"✅ Fetched current theme.liquid ({len(current_theme)} bytes)")

    # Check if already integrated
    if 'product-matrix-loader' in current_theme and 'dynamic-merchandising.js' in current_theme:
        print("✅ Dynamic merchandising already integrated in theme.liquid")
        print("   Skipping update (no changes needed)\n")
    else:
        # Add integration before </head>
        integration_code = """
  {%- comment -%} DYNAMIC MERCHANDISING SYSTEM - Auto-added 2025-11-19 {%- endcomment -%}
  {% render 'product-matrix-loader' %}
  <script src="{{ 'dynamic-merchandising.js' | asset_url }}" defer></script>
"""

        if '</head>' in current_theme:
            updated_theme = current_theme.replace('</head>', integration_code + '</head>')

            # Upload updated theme.liquid
            asset_data = {
                "asset": {
                    "key": "layout/theme.liquid",
                    "value": updated_theme
                }
            }

            response = requests.put(
                f"{REST_URL}/themes/{THEME_ID}/assets.json",
                headers=HEADERS,
                json=asset_data
            )

            if response.status_code in [200, 201]:
                print("✅ Updated layout/theme.liquid with dynamic merchandising integration\n")
            else:
                print(f"❌ Update failed: {response.status_code}")
                print(f"Response: {response.text[:200]}\n")
        else:
            print("⚠️  Could not find </head> tag in theme.liquid")
            print("   Manual integration required\n")

except Exception as e:
    print(f"❌ Error: {e}\n")

# =========================================================================
# STEP 5: Verification
# =========================================================================

print("=" * 80)
print("VERIFICATION")
print("=" * 80)

verification_keys = [
    "assets/product_matrix_complete.json",
    "assets/dynamic-merchandising.js",
    "snippets/product-matrix-loader.liquid",
    "layout/theme.liquid"
]

verified = []
failed = []

for key in verification_keys:
    response = requests.get(
        f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]={key}",
        headers=HEADERS
    )

    if response.status_code == 200:
        asset = response.json().get('asset', {})
        size = len(asset.get('value', ''))
        print(f"✅ {key} ({size} bytes)")
        verified.append(key)
    else:
        print(f"❌ {key} (NOT FOUND)")
        failed.append(key)

print()

# =========================================================================
# SUMMARY
# =========================================================================

print("=" * 80)
print("DEPLOYMENT SUMMARY")
print("=" * 80)
print(f"✅ Verified: {len(verified)}/{len(verification_keys)} files")
print(f"❌ Failed: {len(failed)}/{len(verification_keys)} files\n")

if len(failed) > 0:
    print("⚠️  DEPLOYMENT INCOMPLETE - Fix issues above\n")
    exit(1)
else:
    print("🎉 DEPLOYMENT COMPLETE!")
    print()
    print("SYSTEM ENABLED:")
    print("- Product matrix: 96 products with 6D scoring")
    print("- Dynamic rotation: Monthly + demographic-based")
    print("- Target sections: featured-collection, bundle-products-showcase, related-products")
    print("- NOT affected: Hero slideshow (owner-managed)")
    print()
    print("NEXT STEPS:")
    print("1. Test on homepage: https://www.alphamedical.shop")
    print("2. Open browser console: Check for '[DynMerch]' logs")
    print("3. Verify product order changes based on current month")
    print("4. Test demographic inference: View products and see rotation adjust")
    print()
    exit(0)
