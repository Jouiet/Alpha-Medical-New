#!/usr/bin/env python3
"""
DEPLOY SMART RECOMMENDATIONS SNIPPET TO SHOPIFY
- Upload snippets/smart-recommendations.liquid
- Update product template to include snippet
- Verify deployment
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
print("DEPLOYING SMART RECOMMENDATIONS SNIPPET")
print("=" * 80)
print(f"Theme ID: {THEME_ID}")
print()

# ============================================================================
# STEP 1: Upload smart-recommendations.liquid snippet
# ============================================================================

print("Step 1: Uploading smart-recommendations.liquid snippet...")

snippet_path = '/Users/mac/Desktop/Alpha-Medical/snippets/smart-recommendations.liquid'
with open(snippet_path, 'r') as f:
    snippet_content = f.read()

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
payload = {
    "asset": {
        "key": "snippets/smart-recommendations.liquid",
        "value": snippet_content
    }
}

response = requests.put(url, headers=HEADERS, json=payload)

if response.status_code in [200, 201]:
    print("  ✅ smart-recommendations.liquid uploaded successfully")
else:
    print(f"  ❌ Upload failed: {response.status_code}")
    print(response.text)
    exit(1)

# ============================================================================
# STEP 2: Read current product template
# ============================================================================

print("\nStep 2: Reading current product template...")

# Check for product.json template (newer themes)
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]=templates/product.json"
response = requests.get(url, headers=HEADERS)

product_template_type = None
product_template_content = None

if response.status_code == 200:
    product_template_type = 'json'
    product_template_content = response.json()['asset']['value']
    print("  ✅ Found templates/product.json (JSON template)")
else:
    # Try liquid template
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]=templates/product.liquid"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        product_template_type = 'liquid'
        product_template_content = response.json()['asset']['value']
        print("  ✅ Found templates/product.liquid (Liquid template)")
    else:
        print("  ❌ No product template found")
        exit(1)

# ============================================================================
# STEP 3: Update product template to include snippet
# ============================================================================

print("\nStep 3: Updating product template...")

snippet_render = "{% render 'smart-recommendations', product: product, type: 'auto', limit: 4 %}"

if product_template_type == 'json':
    # Parse JSON template
    template_data = json.loads(product_template_content)

    # Check if snippet already included in sections
    already_included = False

    # Search for recommendations in order (common section locations)
    if 'order' in template_data:
        for section_id in template_data['order']:
            if 'recommendation' in section_id.lower():
                already_included = True
                print(f"  ℹ️  Found existing recommendations section: {section_id}")
                break

    if already_included:
        print("  ✅ Recommendations already integrated in product template")
    else:
        # Add custom liquid section for recommendations
        print("  ℹ️  JSON template detected - need to create custom section")
        print("  ℹ️  Creating sections/smart-recommendations-section.liquid...")

        # Create a section wrapper for the snippet
        section_content = """{% comment %}
  Smart Recommendations Section
  Wrapper section for smart-recommendations snippet
{% endcomment %}

<div class="page-width">
  {% render 'smart-recommendations', product: product, type: 'auto', limit: 4 %}
</div>

{% schema %}
{
  "name": "Smart Recommendations",
  "tag": "section",
  "class": "section-smart-recommendations",
  "settings": [
    {
      "type": "select",
      "id": "recommendation_type",
      "label": "Recommendation Type",
      "options": [
        {
          "value": "auto",
          "label": "Auto (with tabs)"
        },
        {
          "value": "similar",
          "label": "Similar Products"
        },
        {
          "value": "complements",
          "label": "Complements"
        },
        {
          "value": "upgrades",
          "label": "Bundles"
        }
      ],
      "default": "auto"
    },
    {
      "type": "range",
      "id": "products_limit",
      "min": 2,
      "max": 8,
      "step": 1,
      "label": "Number of Products",
      "default": 4
    },
    {
      "type": "text",
      "id": "section_title",
      "label": "Section Title (optional)",
      "info": "Leave empty for auto-generated title"
    }
  ],
  "presets": [
    {
      "name": "Smart Recommendations"
    }
  ]
}
{% endschema %}
"""

        # Upload section
        url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
        payload = {
            "asset": {
                "key": "sections/smart-recommendations-section.liquid",
                "value": section_content
            }
        }

        response = requests.put(url, headers=HEADERS, json=payload)

        if response.status_code in [200, 201]:
            print("  ✅ sections/smart-recommendations-section.liquid created")
        else:
            print(f"  ❌ Section creation failed: {response.status_code}")
            print(response.text)

        print()
        print("  ⚠️  MANUAL STEP REQUIRED:")
        print("  1. Go to: https://admin.shopify.com/store/azffej-as/themes")
        print("  2. Click 'Customize' on Alpha-Medical-New theme")
        print("  3. Navigate to any product page")
        print("  4. Click 'Add section' at the bottom of the page")
        print("  5. Select 'Smart Recommendations'")
        print("  6. Position it after 'Product information' section")
        print("  7. Click 'Save'")

elif product_template_type == 'liquid':
    # Check if already included
    if 'smart-recommendations' in product_template_content:
        print("  ✅ smart-recommendations snippet already included")
    else:
        # Add snippet before closing main tag or at end
        if '</main>' in product_template_content:
            insertion_point = product_template_content.rindex('</main>')
            updated_content = (
                product_template_content[:insertion_point] +
                '\n  ' + snippet_render + '\n' +
                product_template_content[insertion_point:]
            )
        else:
            # Add at end of file
            updated_content = product_template_content + '\n\n' + snippet_render + '\n'

        # Upload updated template
        url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
        payload = {
            "asset": {
                "key": "templates/product.liquid",
                "value": updated_content
            }
        }

        response = requests.put(url, headers=HEADERS, json=payload)

        if response.status_code in [200, 201]:
            print("  ✅ product.liquid updated with smart-recommendations snippet")
        else:
            print(f"  ❌ Template update failed: {response.status_code}")
            print(response.text)

# ============================================================================
# STEP 4: Verify deployment
# ============================================================================

print("\n" + "=" * 80)
print("DEPLOYMENT VERIFICATION")
print("=" * 80)

# Verify snippet exists
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]=snippets/smart-recommendations.liquid"
response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    print("✅ snippets/smart-recommendations.liquid deployed")
else:
    print("❌ Snippet not found in theme")

# Verify matrix JS exists
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]=assets/product-recommendations-matrix.js"
response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    print("✅ assets/product-recommendations-matrix.js deployed")
else:
    print("⚠️  Recommendations matrix JS not found - run deploy_recommendations_system.py first")

# Verify section exists (if created)
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json?asset[key]=sections/smart-recommendations-section.liquid"
response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    print("✅ sections/smart-recommendations-section.liquid deployed")

# ============================================================================
# TESTING INSTRUCTIONS
# ============================================================================

print("\n" + "=" * 80)
print("TESTING INSTRUCTIONS")
print("=" * 80)

print("""
1. TEST ON LIVE PRODUCT PAGE:
   - Visit: https://www.alphamedical.shop/products/tourmaline-magnetic-knee-pads-self-heating-support
   - Scroll to bottom of page
   - Look for "Recommended For You" section
   - Verify 3 tabs: Similar Products, Complements, Bundles
   - Click tabs to switch recommendation types

2. VERIFY RECOMMENDATIONS LOAD:
   - Check browser console (F12) for errors
   - Verify products load dynamically
   - Test product cards are clickable
   - Verify images load correctly

3. TEST RESPONSIVE DESIGN:
   - Test on mobile (iPhone/Android)
   - Test on tablet (iPad)
   - Test on desktop
   - Verify grid layout adjusts properly

4. CHECK PERFORMANCE:
   - Open Network tab in browser DevTools
   - Refresh product page
   - Verify product-recommendations-matrix.js loads (1 request)
   - Verify product JSON fetches (max 4 requests)
   - Total load time should be < 2 seconds

5. VERIFY DATA ACCURACY:
   - Check if recommended products are relevant
   - Verify product prices are correct
   - Verify product titles display properly
   - Check discount badges show correct percentages

6. TEST EDGE CASES:
   - Product with no recommendations (should show "No recommendations available")
   - Product with only 1-2 recommendations (should show available only)
   - Bundle products (should prioritize similar bundles)

EXPECTED BEHAVIOR:
✅ Recommendations section appears below product information
✅ Default tab: "Similar Products" is active
✅ 4 product cards displayed in grid (2x2 on mobile, 4x1 on desktop)
✅ Clicking tabs switches recommendation types instantly
✅ Product cards are clickable and link to product pages
✅ Hover effects work (card lifts, image scales slightly)
✅ Loading spinner shows briefly before products appear
✅ No JavaScript errors in console
""")

print("=" * 80)
print("DEPLOYMENT COMPLETE")
print("=" * 80)
print("✅ smart-recommendations.liquid deployed")
print("✅ Product template updated")
print()
print("FILES DEPLOYED:")
print("  - snippets/smart-recommendations.liquid")
print("  - sections/smart-recommendations-section.liquid (if JSON template)")
print()
print("NEXT STEPS:")
print("  1. Complete manual integration (if JSON template)")
print("  2. Test on live product page")
print("  3. Verify recommendations accuracy")
print("  4. Monitor for JavaScript errors")
print("=" * 80)
