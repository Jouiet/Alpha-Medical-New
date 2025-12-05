#!/usr/bin/env python3
"""
BUNDLE BUILDER COMBINED - Deployment Script
Déploie la version unifiée avec recherche ET URL input
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
print("BUNDLE BUILDER COMBINED - DEPLOYMENT")
print("Recherche de produits + Input URL")
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
# STEP 2: Upload sections/bundle-builder-combined.liquid
# ============================================================================
print("\n2. Uploading sections/bundle-builder-combined.liquid...")

with open('sections/bundle-builder-combined.liquid', 'r') as f:
    section_content = f.read()

section_data = {
    "asset": {
        "key": "sections/bundle-builder-combined.liquid",
        "value": section_content
    }
}

section_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", section_data)
if section_result:
    print(f"✅ sections/bundle-builder-combined.liquid uploaded ({len(section_content)} chars)")
else:
    print("❌ Failed to upload section")
    exit(1)

# ============================================================================
# STEP 3: Upload assets/bundle-builder-combined.css
# ============================================================================
print("\n3. Uploading assets/bundle-builder-combined.css...")

with open('assets/bundle-builder-combined.css', 'r') as f:
    css_content = f.read()

css_data = {
    "asset": {
        "key": "assets/bundle-builder-combined.css",
        "value": css_content
    }
}

css_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", css_data)
if css_result:
    print(f"✅ assets/bundle-builder-combined.css uploaded ({len(css_content)} chars)")
else:
    print("❌ Failed to upload CSS")
    exit(1)

# ============================================================================
# STEP 4: Upload assets/bundle-builder-combined.js
# ============================================================================
print("\n4. Uploading assets/bundle-builder-combined.js...")

with open('assets/bundle-builder-combined.js', 'r') as f:
    js_content = f.read()

js_data = {
    "asset": {
        "key": "assets/bundle-builder-combined.js",
        "value": js_content
    }
}

js_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", js_data)
if js_result:
    print(f"✅ assets/bundle-builder-combined.js uploaded ({len(js_content)} chars)")
else:
    print("❌ Failed to upload JavaScript")
    exit(1)

# ============================================================================
# STEP 5: Upload templates/page.bundle-creator.json
# ============================================================================
print("\n5. Uploading templates/page.bundle-creator.json...")

with open('templates/page.bundle-creator.json', 'r') as f:
    template_content = f.read()

template_data = {
    "asset": {
        "key": "templates/page.bundle-creator.json",
        "value": template_content
    }
}

template_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", template_data)
if template_result:
    print(f"✅ templates/page.bundle-creator.json uploaded")
else:
    print("❌ Failed to upload page template")
    exit(1)

# ============================================================================
# STEP 6: Upload snippets/bundle-creator-cta.liquid
# ============================================================================
print("\n6. Uploading snippets/bundle-creator-cta.liquid...")

with open('snippets/bundle-creator-cta.liquid', 'r') as f:
    snippet_content = f.read()

snippet_data = {
    "asset": {
        "key": "snippets/bundle-creator-cta.liquid",
        "value": snippet_content
    }
}

snippet_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", snippet_data)
if snippet_result:
    print(f"✅ snippets/bundle-creator-cta.liquid uploaded ({len(snippet_content)} chars)")
else:
    print("❌ Failed to upload snippet")
    exit(1)

# ============================================================================
# STEP 7: Create /pages/bundle-creator Page
# ============================================================================
print("\n7. Creating page /pages/bundle-creator...")

# Check if page already exists
existing_pages = rest_request("GET", "/pages.json?handle=bundle-creator")
if existing_pages and existing_pages.get('pages'):
    page = existing_pages['pages'][0]
    print(f"⚠️  Page already exists: {page['title']} (ID: {page['id']})")
    print(f"   Updating template suffix...")

    # Update existing page to use bundle-creator template
    update_data = {
        "page": {
            "id": page['id'],
            "template_suffix": "bundle-creator"
        }
    }
    update_result = rest_request("PUT", f"/pages/{page['id']}.json", update_data)
    if update_result:
        print(f"✅ Page template updated to 'bundle-creator'")
        print(f"   URL: https://www.alphamedical.shop/pages/{page['handle']}")
    else:
        print("❌ Failed to update page template")
else:
    # Create new page
    page_data = {
        "page": {
            "title": "Create Your Bundle",
            "handle": "bundle-creator",
            "body_html": """<div style="text-align: center; padding: 40px 20px;">
<h2>Build Your Perfect Bundle</h2>
<p style="font-size: 1.1rem; color: #666; max-width: 600px; margin: 20px auto;">
Select 3-4 products and get 35% OFF instantly!
</p>
<p><strong>Two Easy Methods:</strong></p>
<ol style="text-align: left; max-width: 500px; margin: 20px auto; line-height: 1.8;">
<li><strong>Search Products:</strong> Browse and select from our catalog</li>
<li><strong>Paste URLs:</strong> Copy product links directly</li>
</ol>
<p style="margin-top: 30px; color: #4A90E2; font-weight: 600;">
When 10+ customers request the same bundle, we create it!
</p>
</div>""",
            "published": True,
            "template_suffix": "bundle-creator"
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
# STEP 8: Add CSS/JS to theme.liquid
# ============================================================================
print("\n8. Updating layout/theme.liquid...")

# Read current theme.liquid
theme_liquid_response = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=layout/theme.liquid")

if theme_liquid_response and 'asset' in theme_liquid_response:
    theme_content = theme_liquid_response['asset']['value']

    # Check if already added
    if 'bundle-builder-combined.css' in theme_content:
        print("⚠️  CSS already linked in theme.liquid")
    else:
        # Add before </head>
        theme_content = theme_content.replace(
            '</head>',
            """    {%- comment -%} Bundle Builder Combined Assets {%- endcomment -%}
    {{ 'bundle-builder-combined.css' | asset_url | stylesheet_tag }}
    {{ 'bundle-builder-combined.js' | asset_url | script_tag }}
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
print("   1. sections/bundle-builder-combined.liquid → Theme uploaded")
print("   2. assets/bundle-builder-combined.css → Theme uploaded")
print("   3. assets/bundle-builder-combined.js → Theme uploaded")
print("   4. templates/page.bundle-creator.json → Theme uploaded")
print("   5. snippets/bundle-creator-cta.liquid → Theme uploaded")
print("   6. /pages/bundle-creator → Page created/updated")
print("   7. layout/theme.liquid → CSS/JS links added")
print()
print("🎯 FEATURES:")
print("   ✅ Méthode 1: Recherche de produits (search)")
print("   ✅ Méthode 2: Input URL (copier/coller)")
print("   ✅ Instructions UX claires pour les deux méthodes")
print("   ✅ Validation en temps réel")
print("   ✅ Calcul automatique 35% discount")
print("   ✅ Limite $500 enforced")
print()
print("📋 NEXT STEPS:")
print("   1. Visitez: https://www.alphamedical.shop/pages/bundle-creator")
print("   2. Testez les deux méthodes (search + URL)")
print("   3. Ajoutez le CTA banner sur homepage:")
print("      {% render 'bundle-creator-cta' %}")
print()
print("🔗 CTA BANNER:")
print("   - Snippet créé: snippets/bundle-creator-cta.liquid")
print("   - Design: Gradient animé avec badge 35% OFF")
print("   - Lien: Pointe vers /pages/bundle-creator")
print("   - Utilisation: Ajoutez sur homepage ou autres pages")
print()
print("="*80)
print("DEPLOYMENT COMPLETE ✅")
print("="*80)
