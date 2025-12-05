#!/usr/bin/env python3
"""
DEPLOY TRANSPARENCY UPDATES
1. Add physical address to footer
2. Deploy "Our Story" page
3. Verify all changes forensically
"""

import os
import requests
import json

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

# ═══════════════════════════════════════════════════════════════════
# BUSINESS INFO
# ═══════════════════════════════════════════════════════════════════

BUSINESS_INFO = {
    "legal_name": "JoHat Services LLC",
    "dba": "Alpha Medical Care",
    "address_line1": "611 South DuPont Highway Suite 102",
    "city": "Dover",
    "state": "DE",
    "zip": "19901",
    "country": "United States",
    "email": "support@alphamedical.shop"
}

# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def rest_request(method, endpoint, data=None):
    url = f"{REST_URL}{endpoint}"
    if method == "GET":
        response = requests.get(url, headers=HEADERS)
    elif method == "PUT":
        response = requests.put(url, headers=HEADERS, json=data)
    elif method == "POST":
        response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code not in [200, 201]:
        print(f"❌ API Error: {response.status_code}")
        print(response.text[:500])
        return None
    return response.json()

print("═══════════════════════════════════════════════════════════════")
print("🚀 TRANSPARENCY UPDATES DEPLOYMENT")
print("═══════════════════════════════════════════════════════════════\n")

# ═══════════════════════════════════════════════════════════════════
# STEP 1: Get Published Theme
# ═══════════════════════════════════════════════════════════════════

print("📋 STEP 1: Get Published Theme")
print("─" * 60)

themes = rest_request("GET", "/themes.json")
if not themes:
    exit(1)

theme_id = None
for theme in themes.get('themes', []):
    if theme.get('role') == 'main':
        theme_id = theme['id']
        print(f"✅ Theme: {theme['name']} (ID: {theme_id})\n")
        break

if not theme_id:
    print("❌ No published theme found!")
    exit(1)

# ═══════════════════════════════════════════════════════════════════
# STEP 2: Download Current Footer
# ═══════════════════════════════════════════════════════════════════

print("📋 STEP 2: Download Current Footer")
print("─" * 60)

# Try sections/footer.liquid first
footer_asset = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=sections/footer.liquid")

if footer_asset and footer_asset.get('asset'):
    footer_content = footer_asset['asset']['value']
    footer_key = "sections/footer.liquid"
    print(f"✅ Downloaded {footer_key} ({len(footer_content):,} chars)\n")
else:
    # Try snippets/footer.liquid
    footer_asset = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=snippets/footer.liquid")
    if footer_asset and footer_asset.get('asset'):
        footer_content = footer_asset['asset']['value']
        footer_key = "snippets/footer.liquid"
        print(f"✅ Downloaded {footer_key} ({len(footer_content):,} chars)\n")
    else:
        print("❌ Footer file not found! Trying layout/theme.liquid footer section...")

        # Last resort: Add to theme.liquid before </body>
        theme_asset = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=layout/theme.liquid")
        if not theme_asset:
            print("❌ Could not download theme.liquid either!")
            exit(1)

        footer_content = theme_asset['asset']['value']
        footer_key = "layout/theme.liquid"
        print(f"✅ Will add address section to {footer_key}\n")

# ═══════════════════════════════════════════════════════════════════
# STEP 3: Add Business Address to Footer
# ═══════════════════════════════════════════════════════════════════

print("📋 STEP 3: Add Business Address to Footer")
print("─" * 60)

# Create address HTML snippet
ADDRESS_HTML = f'''
<!-- Business Address for Transparency & Legal Compliance -->
<div class="footer-business-address" style="margin-top: 30px; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.1); text-align: center;">
  <p style="margin: 0 0 10px; font-size: 14px; color: rgba(255,255,255,0.7);">
    <strong style="color: rgba(255,255,255,0.9);">{BUSINESS_INFO['legal_name']}</strong><br>
    <span style="font-size: 13px;">(d/b/a {BUSINESS_INFO['dba']})</span><br>
    {BUSINESS_INFO['address_line1']}<br>
    {BUSINESS_INFO['city']}, {BUSINESS_INFO['state']} {BUSINESS_INFO['zip']}, {BUSINESS_INFO['country']}<br>
    Email: <a href="mailto:{BUSINESS_INFO['email']}" style="color: #4770DB; text-decoration: underline;">{BUSINESS_INFO['email']}</a>
  </p>
  <p style="margin: 15px 0 0; font-size: 12px; color: rgba(255,255,255,0.5); font-style: italic;">
    Not affiliated with Hello Alpha (telemedicine) or AlphaMedicalStore.com
  </p>
</div>
'''

# Check if address already exists
if 'footer-business-address' in footer_content:
    print("⚠️  Address section already exists in footer")
    print("   Skipping to avoid duplication\n")
else:
    # Find insertion point (before closing footer tag or </body>)
    if '</footer>' in footer_content:
        # Insert before </footer>
        footer_content = footer_content.replace('</footer>', f'{ADDRESS_HTML}\n</footer>')
        print("✅ Address inserted before </footer> tag")
    elif '</div>' in footer_content and 'footer' in footer_content.lower():
        # Find last </div> in footer context
        last_div_pos = footer_content.rfind('</div>')
        if last_div_pos != -1:
            footer_content = footer_content[:last_div_pos] + ADDRESS_HTML + '\n' + footer_content[last_div_pos:]
            print("✅ Address inserted before last </div>")
    elif '</body>' in footer_content:
        # Insert before </body> (last resort - theme.liquid)
        footer_content = footer_content.replace('</body>', f'{ADDRESS_HTML}\n</body>')
        print("✅ Address inserted before </body> tag")
    else:
        # Append to end
        footer_content += '\n' + ADDRESS_HTML
        print("✅ Address appended to end of file")

    print()

    # Upload modified footer
    print(f"📤 Uploading modified {footer_key}...")
    update_data = {
        "asset": {
            "key": footer_key,
            "value": footer_content
        }
    }

    result = rest_request("PUT", f"/themes/{theme_id}/assets.json", update_data)
    if result:
        print(f"✅ {footer_key} updated successfully!\n")
    else:
        print(f"❌ Failed to update {footer_key}!\n")
        exit(1)

# ═══════════════════════════════════════════════════════════════════
# STEP 4: Deploy "Our Story" Page
# ═══════════════════════════════════════════════════════════════════

print("📋 STEP 4: Deploy 'Our Story' Page")
print("─" * 60)

# Check if page.our-story.liquid exists locally
our_story_path = '/Users/mac/Desktop/Alpha-Medical/templates/page.our-story.liquid'

if not os.path.exists(our_story_path):
    print(f"❌ {our_story_path} not found!")
    exit(1)

with open(our_story_path, 'r') as f:
    our_story_content = f.read()

print(f"✅ Loaded page.our-story.liquid ({len(our_story_content):,} chars)")

# Upload template to Shopify
print("📤 Uploading page.our-story.liquid to theme...")
upload_data = {
    "asset": {
        "key": "templates/page.our-story.liquid",
        "value": our_story_content
    }
}

result = rest_request("PUT", f"/themes/{theme_id}/assets.json", upload_data)
if result:
    print("✅ page.our-story.liquid uploaded successfully!\n")
else:
    print("❌ Failed to upload page.our-story.liquid!\n")
    exit(1)

# Create the /pages/our-story page in Shopify Admin
print("📄 Creating /pages/our-story page in Shopify Admin...")

pages_response = rest_request("GET", "/pages.json")
our_story_page = None

if pages_response:
    for page in pages_response.get('pages', []):
        if page.get('handle') == 'our-story':
            our_story_page = page
            print(f"⚠️  Page already exists: {page['title']} (ID: {page['id']})")
            break

if not our_story_page:
    # Create new page
    page_data = {
        "page": {
            "title": "Our Story",
            "body_html": "<p>This page uses the custom template.</p>",
            "template_suffix": "our-story",
            "published": True
        }
    }

    result = rest_request("POST", "/pages.json", page_data)
    if result and result.get('page'):
        page_id = result['page']['id']
        print(f"✅ Page created: /pages/our-story (ID: {page_id})")
        print(f"   URL: https://www.alphamedical.shop/pages/our-story\n")
    else:
        print("❌ Failed to create page!\n")
else:
    print(f"✅ Page already exists: /pages/our-story\n")

# ═══════════════════════════════════════════════════════════════════
# STEP 5: Summary
# ═══════════════════════════════════════════════════════════════════

print("═══════════════════════════════════════════════════════════════")
print("📊 DEPLOYMENT SUMMARY")
print("═══════════════════════════════════════════════════════════════\n")

print("✅ Files deployed: 2")
print(f"   1. {footer_key} (business address added)")
print("   2. templates/page.our-story.liquid (brand story)")
print()

print("📍 Business Address Now Visible:")
print(f"   {BUSINESS_INFO['legal_name']}")
print(f"   {BUSINESS_INFO['address_line1']}")
print(f"   {BUSINESS_INFO['city']}, {BUSINESS_INFO['state']} {BUSINESS_INFO['zip']}")
print()

print("🌐 New Page Live:")
print("   https://www.alphamedical.shop/pages/our-story")
print()

print("🔍 Next: Run forensic verification to confirm all changes\n")
