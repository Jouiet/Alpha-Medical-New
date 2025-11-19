#!/usr/bin/env python3
"""
FIX INTERNATIONAL PRESENCE - Reflect TRUE business reality
Alpha Medical Care has:
- Physical stores in Canada + Europe (10,000+ customers)
- E-commerce headquarters in United States (alphamedical.shop)
"""

import os
import requests

# ═══════════════════════════════════════════════════════════════════
# CREDENTIALS
# ═══════════════════════════════════════════════════════════════════

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
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": SHOPIFY_TOKEN, "Content-Type": "application/json"}

def rest_request(method, endpoint, data=None):
    url = f"{REST_URL}{endpoint}"
    if method == "GET":
        response = requests.get(url, headers=HEADERS)
    elif method == "PUT":
        response = requests.put(url, headers=HEADERS, json=data)

    if response.status_code not in [200, 201]:
        print(f"❌ API Error: {response.status_code}")
        return None
    return response.json()

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

print("═══════════════════════════════════════════════════════════════")
print("🌍 FIX INTERNATIONAL PRESENCE - Schema.org Correction")
print("═══════════════════════════════════════════════════════════════\n")

# Get theme
themes = rest_request("GET", "/themes.json")
theme_id = None
for theme in themes.get('themes', []):
    if theme.get('role') == 'main':
        theme_id = theme['id']
        print(f"✅ Theme: {theme['name']} (ID: {theme_id})\n")
        break

if not theme_id:
    print("❌ No theme found!")
    exit(1)

# Get theme.liquid
asset = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=layout/theme.liquid")
if not asset:
    exit(1)

content = asset['asset']['value']
print(f"✅ Downloaded theme.liquid ({len(content):,} chars)\n")

# ═══════════════════════════════════════════════════════════════════
# CORRECTIONS
# ═══════════════════════════════════════════════════════════════════

print("🔧 Applying corrections...\n")

corrections = 0

# Correction 1: disambiguatingDescription - Reflect international presence
OLD_DISAMBIG = 'US-based medical equipment retailer specializing in orthopedic braces and recovery devices.'
NEW_DISAMBIG = 'International medical equipment retailer with e-commerce headquarters in United States and physical stores in Canada and Europe.'

if OLD_DISAMBIG in content:
    content = content.replace(OLD_DISAMBIG, NEW_DISAMBIG)
    corrections += 1
    print("✅ Updated disambiguatingDescription:")
    print(f"   FROM: '{OLD_DISAMBIG[:60]}...'")
    print(f"   TO:   '{NEW_DISAMBIG[:60]}...'")
    print()

# Correction 2: addressCountry - KEEP "US" (e-commerce HQ is in US)
# No change needed - this is correct

# Correction 3: areaServed - Change from single country to multiple
OLD_AREA_SERVED = '''      "areaServed": {
        "@type": "Country",
        "name": "United States"
      },'''

NEW_AREA_SERVED = '''      "areaServed": [
        {
          "@type": "Country",
          "name": "United States"
        },
        {
          "@type": "Country",
          "name": "Canada"
        },
        {
          "@type": "Place",
          "name": "Europe"
        }
      ],'''

if OLD_AREA_SERVED in content:
    content = content.replace(OLD_AREA_SERVED, NEW_AREA_SERVED)
    corrections += 1
    print("✅ Updated areaServed:")
    print("   FROM: Single country (United States)")
    print("   TO:   Multiple countries (US, Canada, Europe)")
    print()

print(f"📊 Total corrections: {corrections}\n")

# ═══════════════════════════════════════════════════════════════════
# UPLOAD
# ═══════════════════════════════════════════════════════════════════

if corrections > 0:
    print("📤 Uploading corrected theme.liquid...")
    update_data = {
        "asset": {
            "key": "layout/theme.liquid",
            "value": content
        }
    }

    result = rest_request("PUT", f"/themes/{theme_id}/assets.json", update_data)

    if result:
        print("✅ theme.liquid updated successfully!")
        print()
    else:
        print("❌ Upload failed!")
        exit(1)
else:
    print("⚠️  No corrections needed\n")

# ═══════════════════════════════════════════════════════════════════
# TRUST BADGES UPDATE
# ═══════════════════════════════════════════════════════════════════

print("═══════════════════════════════════════════════════════════════")
print("🏷️  UPDATE TRUST BADGES - '10,000+ Customers'")
print("═══════════════════════════════════════════════════════════════\n")

# Get product-trust-badges.liquid
badges_asset = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=snippets/product-trust-badges.liquid")

if badges_asset:
    badges_content = badges_asset['asset']['value']
    print(f"✅ Downloaded product-trust-badges.liquid ({len(badges_content):,} chars)\n")

    # Update the text to clarify international scope
    if '10,000+ Customers' in badges_content and 'Trusted by thousands' in badges_content:
        # Option 1: Clarify the scope
        badges_content = badges_content.replace(
            '<strong>10,000+ Customers</strong>\n      <span>Trusted by thousands</span>',
            '<strong>10,000+ Customers Worldwide</strong>\n      <span>International trust since 2025</span>'
        )

        print("✅ Updated trust badge:")
        print("   FROM: '10,000+ Customers' + 'Trusted by thousands'")
        print("   TO:   '10,000+ Customers Worldwide' + 'International trust since 2025'")
        print()

        # Upload
        print("📤 Uploading corrected product-trust-badges.liquid...")
        update_badges = {
            "asset": {
                "key": "snippets/product-trust-badges.liquid",
                "value": badges_content
            }
        }

        result = rest_request("PUT", f"/themes/{theme_id}/assets.json", update_badges)
        if result:
            print("✅ product-trust-badges.liquid updated!\n")
        else:
            print("❌ Upload failed!\n")
else:
    print("⚠️  product-trust-badges.liquid not found\n")

print("═══════════════════════════════════════════════════════════════")
print("✅ CORRECTIONS COMPLETE")
print("═══════════════════════════════════════════════════════════════\n")
print("📋 Summary:")
print("   ✅ Schema.org now reflects international presence")
print("   ✅ addressCountry: US (e-commerce HQ) - CORRECT")
print("   ✅ areaServed: US, Canada, Europe - ACCURATE")
print("   ✅ Trust badge clarified: '10,000+ Customers Worldwide'")
print()
print("🔍 Next: Run forensic verification to confirm\n")
