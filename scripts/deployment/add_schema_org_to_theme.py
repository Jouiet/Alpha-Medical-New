#!/usr/bin/env python3
"""
ADD SCHEMA.ORG TO THEME.LIQUID
Injects MedicalBusiness structured data into theme for LLM disambiguation
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
    elif method == "PUT":
        response = requests.put(url, headers=HEADERS, json=data)

    if response.status_code not in [200, 201]:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        return None
    return response.json()

# STEP 1: Get the published theme
print("🔍 Finding published theme...")
themes_response = rest_request("GET", "/themes.json")
if not themes_response:
    exit(1)

published_theme = None
for theme in themes_response.get('themes', []):
    if theme.get('role') == 'main':
        published_theme = theme
        print(f"✅ Found: {theme['name']} (ID: {theme['id']})")
        break

if not published_theme:
    print("❌ No published theme found!")
    exit(1)

theme_id = published_theme['id']

# STEP 2: Get theme.liquid asset
print(f"\n🔍 Getting theme.liquid from theme {theme_id}...")
asset_response = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=layout/theme.liquid")
if not asset_response:
    exit(1)

current_content = asset_response['asset']['value']
print(f"✅ Current theme.liquid size: {len(current_content)} chars")

# STEP 3: Check if Schema.org already exists
if '@type' in current_content and 'MedicalBusiness' in current_content:
    print("⚠️  Schema.org MedicalBusiness already exists in theme.liquid")
    print("Skipping to avoid duplication.")
    exit(0)

# Schema.org JSON-LD to inject
SCHEMA_ORG_CODE = '''
    {%- comment -%} Schema.org Structured Data for LLM Disambiguation {%- endcomment -%}
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "MedicalBusiness",
      "@id": "https://www.alphamedical.shop",
      "name": "Alpha Medical Care",
      "alternateName": "Alpha Medical Shop",
      "disambiguatingDescription": "Canadian medical equipment retailer specializing in orthopedic braces and recovery devices. NOT affiliated with Hello Alpha (telemedicine) or AlphaMedicalStore.com (fraudulent pharmacy).",
      "description": "Alpha Medical Care sells FDA-compliant orthopedic equipment including posture correctors, cervical traction devices, knee braces, and recovery tools. We do NOT sell prescription drugs or provide telemedicine services.",
      "url": "https://www.alphamedical.shop",
      "logo": {
        "@type": "ImageObject",
        "url": "{{ 'Alpha_Medical_Logo.png' | file_img_url }}"
      },
      "image": "{{ 'Alpha_Medical_Logo.png' | file_img_url }}",
      "email": "support@alphamedical.shop",
      "address": {
        "@type": "PostalAddress",
        "addressCountry": "CA"
      },
      "areaServed": {
        "@type": "Country",
        "name": "Canada"
      },
      "medicalSpecialty": "Orthopedics",
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Orthopedic Equipment Catalog",
        "itemListElement": [
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "MedicalDevice",
              "name": "Posture Correctors & Back Braces",
              "description": "FDA-compliant posture correction devices"
            }
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "MedicalDevice",
              "name": "Cervical Neck Traction Devices",
              "description": "Medical-grade cervical decompression collars"
            }
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "MedicalDevice",
              "name": "Orthopedic Braces",
              "description": "Knee, ankle, wrist, elbow support braces"
            }
          }
        ]
      },
      "sameAs": [
        "https://www.instagram.com/alphamedical",
        "https://www.tiktok.com/@alphamedical",
        "https://www.facebook.com/alphamedical"
      ],
      "foundingDate": "2025",
      "slogan": "Professional-grade orthopedic solutions accessible to everyone",
      "priceRange": "$$"
    }
    </script>
'''

# STEP 4: Find injection point (before {{ content_for_header }})
injection_marker = "{{ content_for_header }}"
if injection_marker not in current_content:
    print("❌ Could not find {{ content_for_header }} in theme.liquid")
    exit(1)

# Inject Schema.org before {{ content_for_header }}
new_content = current_content.replace(injection_marker, f"{SCHEMA_ORG_CODE}\n    {injection_marker}")

print(f"\n✅ Schema.org code prepared ({len(SCHEMA_ORG_CODE)} chars)")
print(f"✅ New theme.liquid size: {len(new_content)} chars")

# STEP 5: Update theme.liquid
print(f"\n🔄 Updating theme.liquid in theme {theme_id}...")
update_data = {
    "asset": {
        "key": "layout/theme.liquid",
        "value": new_content
    }
}

result = rest_request("PUT", f"/themes/{theme_id}/assets.json", update_data)

if result:
    print("✅ theme.liquid updated successfully!")
    print("\n📊 Schema.org features added:")
    print("  ✅ @type: MedicalBusiness (not generic Organization)")
    print("  ✅ disambiguatingDescription (clarifies NOT Hello Alpha)")
    print("  ✅ medicalSpecialty: Orthopedics")
    print("  ✅ address: Canada")
    print("  ✅ email: support@alphamedical.shop")
    print("  ✅ sameAs: Social media links")
    print("  ✅ hasOfferCatalog: Product types listed")
    print("\n🎯 Impact:")
    print("  - Google Knowledge Graph will see MedicalBusiness")
    print("  - Gemini web search will see disambiguation")
    print("  - LLMs may use this data for entity recognition")
else:
    print("❌ Failed to update theme.liquid!")
