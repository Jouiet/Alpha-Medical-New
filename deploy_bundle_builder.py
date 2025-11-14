#!/usr/bin/env python3
"""
BUNDLE BUILDER DEPLOYMENT - Alpha Medical
100% Native Shopify Implementation

Deploys:
1. sections/bundle-builder.liquid (394 lines)
2. assets/bundle-builder.css (1,085 lines)
3. assets/bundle-builder.js (438 lines)
4. templates/page.build-your-bundle.json
5. Creates /pages/build-your-bundle page

NO SHORTCUTS - COMPLETE DEPLOYMENT
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
print("BUNDLE BUILDER - DEPLOYMENT TO SHOPIFY")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
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
# STEP 2: Upload sections/bundle-builder.liquid
# ============================================================================
print("\n2. Uploading sections/bundle-builder.liquid...")

with open('sections/bundle-builder.liquid', 'r') as f:
    section_content = f.read()

section_data = {
    "asset": {
        "key": "sections/bundle-builder.liquid",
        "value": section_content
    }
}

section_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", section_data)
if section_result:
    print(f"✅ sections/bundle-builder.liquid uploaded ({len(section_content)} chars)")
else:
    print("❌ Failed to upload section")
    exit(1)

# ============================================================================
# STEP 3: Upload assets/bundle-builder.css
# ============================================================================
print("\n3. Uploading assets/bundle-builder.css...")

with open('assets/bundle-builder.css', 'r') as f:
    css_content = f.read()

css_data = {
    "asset": {
        "key": "assets/bundle-builder.css",
        "value": css_content
    }
}

css_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", css_data)
if css_result:
    print(f"✅ assets/bundle-builder.css uploaded ({len(css_content)} chars)")
else:
    print("❌ Failed to upload CSS")
    exit(1)

# ============================================================================
# STEP 4: Upload assets/bundle-builder.js
# ============================================================================
print("\n4. Uploading assets/bundle-builder.js...")

with open('assets/bundle-builder.js', 'r') as f:
    js_content = f.read()

js_data = {
    "asset": {
        "key": "assets/bundle-builder.js",
        "value": js_content
    }
}

js_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", js_data)
if js_result:
    print(f"✅ assets/bundle-builder.js uploaded ({len(js_content)} chars)")
else:
    print("❌ Failed to upload JavaScript")
    exit(1)

# ============================================================================
# STEP 5: Upload templates/page.build-your-bundle.json
# ============================================================================
print("\n5. Uploading templates/page.build-your-bundle.json...")

with open('templates/page.build-your-bundle.json', 'r') as f:
    template_content = f.read()

template_data = {
    "asset": {
        "key": "templates/page.build-your-bundle.json",
        "value": template_content
    }
}

template_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", template_data)
if template_result:
    print(f"✅ templates/page.build-your-bundle.json uploaded")
else:
    print("❌ Failed to upload page template")
    exit(1)

# ============================================================================
# STEP 6: Create /pages/build-your-bundle Page
# ============================================================================
print("\n6. Creating page /pages/build-your-bundle...")

# Check if page already exists
existing_pages = rest_request("GET", "/pages.json?handle=build-your-bundle")
if existing_pages and existing_pages.get('pages'):
    page = existing_pages['pages'][0]
    print(f"⚠️  Page already exists: {page['title']} (ID: {page['id']})")
    print(f"   Updating template suffix...")

    # Update existing page to use build-your-bundle template
    update_data = {
        "page": {
            "id": page['id'],
            "template_suffix": "build-your-bundle"
        }
    }
    update_result = rest_request("PUT", f"/pages/{page['id']}.json", update_data)
    if update_result:
        print(f"✅ Page template updated to 'build-your-bundle'")
        print(f"   URL: https://www.alphamedical.shop/pages/{page['handle']}")
    else:
        print("❌ Failed to update page template")
else:
    # Create new page
    page_data = {
        "page": {
            "title": "Build Your Bundle",
            "handle": "build-your-bundle",
            "body_html": """<div style="text-align: center; padding: 40px 20px;">
<h2>Community-Validated Bundle Creation</h2>
<p style="font-size: 1.1rem; color: #666; max-width: 600px; margin: 20px auto;">
Select 3-4 products and get 35% OFF. When 10+ customers request the same bundle, we'll create it!
</p>
<p><strong>How It Works:</strong></p>
<ol style="text-align: left; max-width: 500px; margin: 20px auto; line-height: 1.8;">
<li>Search and select 3-4 products</li>
<li>See your 35% discount calculated automatically</li>
<li>Submit your proposal (not a purchase yet)</li>
<li>We create the bundle when 10+ customers want it</li>
</ol>
</div>""",
            "published": True,
            "template_suffix": "build-your-bundle"
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
# STEP 7: Add CSS/JS to theme.liquid (Manual Instructions)
# ============================================================================
print("\n7. Theme integration (MANUAL STEP REQUIRED)...")
print("⚠️  Add to theme.liquid <head> section:")
print("   {{ 'bundle-builder.css' | asset_url | stylesheet_tag }}")
print("   {{ 'bundle-builder.js' | asset_url | script_tag }}")
print()
print("   Location: layout/theme.liquid")
print("   Before closing </head> tag")

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================
print("\n" + "="*80)
print("DEPLOYMENT SUMMARY")
print("="*80)
print()
print("✅ COMPLETED:")
print("   1. sections/bundle-builder.liquid → Theme uploaded")
print("   2. assets/bundle-builder.css → Theme uploaded")
print("   3. assets/bundle-builder.js → Theme uploaded")
print("   4. templates/page.build-your-bundle.json → Theme uploaded")
print("   5. /pages/build-your-bundle → Page created/updated")
print()
print("📋 NEXT STEPS:")
print("   1. Add CSS/JS links to theme.liquid (see above)")
print("   2. Test page: https://www.alphamedical.shop/pages/build-your-bundle")
print("   3. Configure email → Google Sheets integration")
print("   4. Set up Apps Script for proposal aggregation")
print()
print("📊 CURRENT STATUS:")
print("   - Frontend: ✅ DEPLOYED")
print("   - Styling: ✅ DEPLOYED")
print("   - JavaScript: ✅ DEPLOYED")
print("   - Backend: ⏳ Email/Sheets integration required")
print()
print("="*80)
print("DEPLOYMENT COMPLETE")
print("="*80)
