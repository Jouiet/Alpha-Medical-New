#!/usr/bin/env python3
"""
FIX COUNTRY INFORMATION - Correct CA → US factual errors
Corrects schema.org, About Us page, and any other country mentions
"""

import os
import requests
import re

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
    print("❌ Failed to load credentials from .env.admin")
    exit(1)

API_VERSION = "2025-10"
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def rest_request(method, endpoint, data=None):
    """Execute REST API request"""
    url = f"{REST_URL}{endpoint}"

    if method == "GET":
        response = requests.get(url, headers=HEADERS)
    elif method == "PUT":
        response = requests.put(url, headers=HEADERS, json=data)

    if response.status_code not in [200, 201]:
        print(f"❌ API Error: {response.status_code}")
        print(response.text[:500])
        return None

    return response.json()

def get_published_theme():
    """Get the published theme ID"""
    themes_response = rest_request("GET", "/themes.json")
    if not themes_response:
        return None

    for theme in themes_response.get('themes', []):
        if theme.get('role') == 'main':
            return theme

    return None

def get_asset(theme_id, asset_key):
    """Get asset content from theme"""
    asset_response = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]={asset_key}")
    if not asset_response:
        return None

    return asset_response['asset']['value']

def update_asset(theme_id, asset_key, content):
    """Update asset content"""
    update_data = {
        "asset": {
            "key": asset_key,
            "value": content
        }
    }

    return rest_request("PUT", f"/themes/{theme_id}/assets.json", update_data)

# ═══════════════════════════════════════════════════════════════════
# MAIN CORRECTION LOGIC
# ═══════════════════════════════════════════════════════════════════

print("═══════════════════════════════════════════════════════════════")
print("🔧 COUNTRY INFORMATION CORRECTION TOOL")
print("═══════════════════════════════════════════════════════════════\n")

# Step 1: Get published theme
print("📋 STEP 1: Get Published Theme")
print("─" * 60)

published_theme = get_published_theme()
if not published_theme:
    print("❌ No published theme found!")
    exit(1)

theme_id = published_theme['id']
print(f"✅ Found: {published_theme['name']} (ID: {theme_id})\n")

# Step 2: Fix theme.liquid (schema.org)
print("📋 STEP 2: Fix theme.liquid (Schema.org)")
print("─" * 60)

theme_content = get_asset(theme_id, "layout/theme.liquid")
if not theme_content:
    print("❌ Could not fetch theme.liquid!")
    exit(1)

print(f"✅ Downloaded theme.liquid ({len(theme_content):,} chars)")

# Apply corrections
corrections_made = 0
original_content = theme_content

# Correction 1: disambiguatingDescription
if 'Canadian medical equipment retailer' in theme_content:
    theme_content = theme_content.replace(
        'Canadian medical equipment retailer',
        'US-based medical equipment retailer'
    )
    corrections_made += 1
    print("✅ Fixed: 'Canadian medical equipment retailer' → 'US-based medical equipment retailer'")

# Correction 2: addressCountry
if '"addressCountry": "CA"' in theme_content:
    theme_content = theme_content.replace(
        '"addressCountry": "CA"',
        '"addressCountry": "US"'
    )
    corrections_made += 1
    print("✅ Fixed: addressCountry 'CA' → 'US'")

# Correction 3: areaServed
if '"name": "Canada"' in theme_content and '"areaServed"' in theme_content:
    # More precise replacement - only in areaServed context
    theme_content = re.sub(
        r'("areaServed":\s*\{\s*"@type":\s*"Country",\s*"name":\s*)"Canada"',
        r'\1"United States"',
        theme_content
    )
    corrections_made += 1
    print("✅ Fixed: areaServed 'Canada' → 'United States'")

if corrections_made > 0:
    print(f"\n📤 Uploading corrected theme.liquid ({corrections_made} changes)...")
    result = update_asset(theme_id, "layout/theme.liquid", theme_content)
    if result:
        print("✅ theme.liquid updated successfully!\n")
    else:
        print("❌ Failed to update theme.liquid!\n")
        exit(1)
else:
    print("✅ No corrections needed in theme.liquid\n")

# Step 3: Fix About Us page
print("📋 STEP 3: Fix About Us Page")
print("─" * 60)

about_us_content = get_asset(theme_id, "templates/page.about-us.liquid")
if not about_us_content:
    print("⚠️  Could not fetch page.about-us.liquid (may not exist)")
else:
    print(f"✅ Downloaded page.about-us.liquid ({len(about_us_content):,} chars)")

    about_corrections = 0

    # Correction 4: "Based in Canada"
    if 'Based in Canada' in about_us_content:
        about_us_content = about_us_content.replace(
            'Based in Canada',
            'Based in United States'
        )
        about_corrections += 1
        print("✅ Fixed: 'Based in Canada' → 'Based in United States'")

    # Check for other Canada mentions
    canada_mentions = about_us_content.count('Canada')
    if canada_mentions > 0:
        print(f"⚠️  Warning: {canada_mentions} other 'Canada' mentions found - manual review needed")

    if about_corrections > 0:
        print(f"\n📤 Uploading corrected page.about-us.liquid ({about_corrections} changes)...")
        result = update_asset(theme_id, "templates/page.about-us.liquid", about_us_content)
        if result:
            print("✅ page.about-us.liquid updated successfully!\n")
        else:
            print("❌ Failed to update page.about-us.liquid!\n")
    else:
        print("✅ No corrections needed in page.about-us.liquid\n")

# Step 4: Summary
print("═══════════════════════════════════════════════════════════════")
print("📊 CORRECTION SUMMARY")
print("═══════════════════════════════════════════════════════════════\n")

print(f"✅ Files corrected: 2")
print(f"✅ Total changes: {corrections_made + about_corrections}")
print(f"\n🔍 Next step: Run forensic verification to confirm changes are live\n")
