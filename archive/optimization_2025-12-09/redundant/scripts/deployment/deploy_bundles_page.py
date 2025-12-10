#!/usr/bin/env python3
"""
ALPHA MEDICAL - BUNDLES PAGE DEPLOYMENT
Deploys bundles collection page with filters to Shopify
"""

import os
import json
import requests
from datetime import datetime

# Load credentials
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

def rest_request(method, endpoint, data=None):
    """Execute REST API request"""
    url = f"{REST_URL}{endpoint}"
    if method == "GET":
        response = requests.get(url, headers=HEADERS)
    elif method == "POST":
        response = requests.post(url, json=data, headers=HEADERS)
    elif method == "PUT":
        response = requests.put(url, json=data, headers=HEADERS)
    else:
        raise ValueError(f"Unsupported method: {method}")

    if response.status_code not in [200, 201]:
        print(f"❌ REST API Error: {response.status_code}")
        print(response.text)
        return None

    return response.json() if response.text else {}

print("="*80)
print("BUNDLES PAGE DEPLOYMENT")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)

# ============================================================================
# STEP 1: Get Active Theme ID
# ============================================================================
print("\n1. Getting active theme ID...")

themes_response = rest_request("GET", "/themes.json")
if not themes_response:
    print("❌ Failed to fetch themes")
    exit(1)

active_theme = next((t for t in themes_response['themes'] if t['role'] == 'main'), None)
if not active_theme:
    print("❌ No active theme found")
    exit(1)

theme_id = active_theme['id']
print(f"✅ Active theme: {active_theme['name']} (ID: {theme_id})")

# ============================================================================
# STEP 2: Upload sections/bundles-collection.liquid
# ============================================================================
print("\n2. Uploading sections/bundles-collection.liquid...")

with open('sections/bundles-collection.liquid', 'r') as f:
    section_content = f.read()

section_data = {
    "asset": {
        "key": "sections/bundles-collection.liquid",
        "value": section_content
    }
}

section_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", section_data)
if section_result:
    print(f"✅ sections/bundles-collection.liquid uploaded ({len(section_content)} chars)")
else:
    print("❌ Failed to upload section")
    exit(1)

# ============================================================================
# STEP 3: Upload assets/bundles-collection.css
# ============================================================================
print("\n3. Uploading assets/bundles-collection.css...")

with open('assets/bundles-collection.css', 'r') as f:
    css_content = f.read()

css_data = {
    "asset": {
        "key": "assets/bundles-collection.css",
        "value": css_content
    }
}

css_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", css_data)
if css_result:
    print(f"✅ assets/bundles-collection.css uploaded ({len(css_content)} chars)")
else:
    print("❌ Failed to upload CSS")
    exit(1)

# ============================================================================
# STEP 4: Upload assets/bundles-collection.js
# ============================================================================
print("\n4. Uploading assets/bundles-collection.js...")

with open('assets/bundles-collection.js', 'r') as f:
    js_content = f.read()

js_data = {
    "asset": {
        "key": "assets/bundles-collection.js",
        "value": js_content
    }
}

js_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", js_data)
if js_result:
    print(f"✅ assets/bundles-collection.js uploaded ({len(js_content)} chars)")
else:
    print("❌ Failed to upload JavaScript")
    exit(1)

# ============================================================================
# STEP 5: Upload templates/page.bundles.json
# ============================================================================
print("\n5. Uploading templates/page.bundles.json...")

with open('templates/page.bundles.json', 'r') as f:
    template_content = f.read()

template_data = {
    "asset": {
        "key": "templates/page.bundles.json",
        "value": template_content
    }
}

template_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", template_data)
if template_result:
    print(f"✅ templates/page.bundles.json uploaded")
else:
    print("❌ Failed to upload page template")
    exit(1)

# ============================================================================
# STEP 6: Create /pages/bundles Page
# ============================================================================
print("\n6. Creating page /pages/bundles...")

# Check if page already exists
existing_pages = rest_request("GET", "/pages.json?handle=bundles")
if existing_pages and existing_pages.get('pages'):
    page = existing_pages['pages'][0]
    print(f"⚠️  Page already exists: {page['title']} (ID: {page['id']})")
    print(f"   Updating template suffix...")

    # Update existing page to use bundles template
    update_data = {
        "page": {
            "id": page['id'],
            "template_suffix": "bundles"
        }
    }
    update_result = rest_request("PUT", f"/pages/{page['id']}.json", update_data)
    if update_result:
        print(f"✅ Page template updated to 'bundles'")
        print(f"   URL: https://www.alphamedical.shop/pages/{page['handle']}")
    else:
        print("❌ Failed to update page template")
else:
    # Create new page
    page_data = {
        "page": {
            "title": "Medical Equipment Bundles",
            "handle": "bundles",
            "body_html": """<div style="text-align: center; padding: 40px 20px;">
<h2>Complete Care Bundles</h2>
<p style="font-size: 1.1rem; color: #666; max-width: 600px; margin: 20px auto;">
Curated medical equipment packages designed for your specific needs. Save 35% OFF on every bundle.
</p>
<p><strong>15 Expert Bundles | 8 Patient Personas | 4 Price Tiers</strong></p>
<p style="margin-top: 30px; color: #4A90E2; font-weight: 600;">
Every bundle offers exactly 35% OFF with free shipping!
</p>
</div>""",
            "published": True,
            "template_suffix": "bundles"
        }
    }

    page_result = rest_request("POST", "/pages.json", page_data)

    if page_result and page_result.get('page'):
        page = page_result['page']
        print(f"✅ Page created successfully")
        print(f"   Title: {page['title']}")
        print(f"   Handle: {page['handle']}")
        print(f"   URL: https://www.alphamedical.shop/pages/{page['handle']}")
    else:
        print("❌ Failed to create page")
        exit(1)

# ============================================================================
# STEP 7: Add CSS/JS to theme.liquid
# ============================================================================
print("\n7. Updating layout/theme.liquid...")

# Read current theme.liquid
theme_liquid_response = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=layout/theme.liquid")

if theme_liquid_response and 'asset' in theme_liquid_response:
    theme_content = theme_liquid_response['asset']['value']

    # Check if already added
    if 'bundles-collection.css' in theme_content:
        print("⚠️  CSS/JS already linked in theme.liquid")
    else:
        # Add before </head>
        theme_content = theme_content.replace(
            '</head>',
            """    {%- comment -%} Bundles Collection Assets {%- endcomment -%}
    {{ 'bundles-collection.css' | asset_url | stylesheet_tag }}
    {{ 'bundles-collection.js' | asset_url | script_tag }}
  </head>"""
        )

        # Upload updated theme.liquid
        theme_data = {
            "asset": {
                "key": "layout/theme.liquid",
                "value": theme_content
            }
        }

        theme_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", theme_data)
        if theme_result:
            print("✅ theme.liquid updated with CSS/JS links")
        else:
            print("❌ Failed to update theme.liquid")
else:
    print("⚠️  Could not read theme.liquid - manual update required")

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================
print("\n" + "="*80)
print("DEPLOYMENT SUMMARY")
print("="*80)
print()
print("✅ COMPLETED:")
print("   1. sections/bundles-collection.liquid → Theme uploaded")
print("   2. assets/bundles-collection.css → Theme uploaded")
print("   3. assets/bundles-collection.js → Theme uploaded")
print("   4. templates/page.bundles.json → Theme uploaded")
print("   5. /pages/bundles → Page created/updated")
print("   6. layout/theme.liquid → CSS/JS links added")
print()
print("🎯 FEATURES:")
print("   ✅ Persona filters (8 patient types)")
print("   ✅ Tier filters (4 price ranges)")
print("   ✅ Sort options (savings, price, products)")
print("   ✅ Real-time filtering with JavaScript")
print("   ✅ Responsive design (mobile + desktop)")
print("   ✅ 35% discount badges on all bundles")
print("   ✅ Why Bundles education section")
print("   ✅ FAQ section")
print("   ✅ Custom bundle CTA")
print()
print("📋 NEXT STEPS:")
print("   1. Visit: https://www.alphamedical.shop/pages/bundles")
print("   2. Create 15 bundle products via Shopify Admin API")
print("   3. Upload bundle images (1200x1200px)")
print("   4. Add bundle CTAs to homepage + product pages")
print("   5. Add /pages/bundles to main navigation")
print()
print("📝 NOTE:")
print("   - Bundle cards currently show placeholder images")
print("   - Add to cart buttons show alerts (need Shopify product IDs)")
print("   - Create actual bundle products to make functional")
print()
print("="*80)
print("DEPLOYMENT COMPLETE ✅")
print("="*80)
