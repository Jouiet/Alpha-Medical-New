#!/usr/bin/env python3
"""
FAVICON UPLOADER - Alpha Medical
Uploads logo as favicon to Shopify theme settings
"""

import os
import json
import requests
import base64
from PIL import Image
from io import BytesIO

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
print("FAVICON UPLOAD - Alpha Medical Logo")
print("="*80)

# ============================================================================
# STEP 1: Convert PNG to optimized favicon (512x512)
# ============================================================================
print("\n1. Processing logo image...")

logo_path = "Images/Alpha Medical Logo Negatif.png"

if not os.path.exists(logo_path):
    print(f"❌ Logo file not found: {logo_path}")
    print("   Trying alternative: Images/Alpha Medical Logo.svg")
    logo_path = "Images/Alpha Medical Logo.svg"

    if not os.path.exists(logo_path):
        print("❌ No logo files found")
        exit(1)

try:
    # Open and resize image
    if logo_path.endswith('.svg'):
        print("⚠️  SVG detected - Converting to PNG...")
        # For SVG, we need to convert it first (requires cairosvg or similar)
        # For now, let's use the PNG version
        logo_path = "Images/Alpha Medical Logo Negatif.png"

    img = Image.open(logo_path)

    # Convert to RGBA if not already
    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    # Resize to 512x512 (Shopify recommended size)
    favicon_size = 512
    img_resized = img.resize((favicon_size, favicon_size), Image.Resampling.LANCZOS)

    # Save to BytesIO buffer
    buffer = BytesIO()
    img_resized.save(buffer, format='PNG', optimize=True)
    buffer.seek(0)

    # Encode as base64
    favicon_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    print(f"✅ Logo processed: {favicon_size}x{favicon_size}px PNG")
    print(f"   Original size: {img.size}")
    print(f"   File size: {len(favicon_base64)} bytes (base64)")

except Exception as e:
    print(f"❌ Image processing error: {str(e)}")
    exit(1)

# ============================================================================
# STEP 2: Get active theme ID
# ============================================================================
print("\n2. Getting active theme ID...")

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
# STEP 3: Upload favicon as theme asset
# ============================================================================
print("\n3. Uploading favicon to theme assets...")

# Upload favicon.png to assets/
favicon_data = {
    "asset": {
        "key": "assets/favicon.png",
        "attachment": favicon_base64
    }
}

favicon_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", favicon_data)
if favicon_result:
    favicon_url = f"https://cdn.shopify.com/s/files/1/0876/6345/6337/files/favicon.png"
    print(f"✅ Favicon uploaded to assets/favicon.png")
else:
    print("❌ Failed to upload favicon")
    exit(1)

# ============================================================================
# STEP 4: Update theme settings to use favicon
# ============================================================================
print("\n4. Updating theme settings...")

# Get current settings_data.json
settings_response = rest_request("GET", f"/themes/{theme_id}/assets.json?asset[key]=config/settings_data.json")

if not settings_response or 'asset' not in settings_response:
    print("❌ Failed to fetch theme settings")
    exit(1)

settings = json.loads(settings_response['asset']['value'])

# Update favicon in current settings
if 'current' not in settings:
    settings['current'] = {}

# Set favicon to use the uploaded file
settings['current']['favicon'] = "shopify://shop_images/favicon.png"

# Upload updated settings
settings_data = {
    "asset": {
        "key": "config/settings_data.json",
        "value": json.dumps(settings)
    }
}

settings_result = rest_request("PUT", f"/themes/{theme_id}/assets.json", settings_data)

if settings_result:
    print("✅ Theme settings updated with favicon")
else:
    print("❌ Failed to update theme settings")
    exit(1)

# ============================================================================
# STEP 5: Upload to Files (for theme settings reference)
# ============================================================================
print("\n5. Uploading favicon to Files section...")

# We need to use the GraphQL API for this
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

graphql_headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# First, create a staged upload
staged_upload_mutation = """
mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets {
      url
      resourceUrl
      parameters {
        name
        value
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

staged_upload_variables = {
    "input": [{
        "resource": "IMAGE",
        "filename": "favicon.png",
        "mimeType": "image/png",
        "fileSize": str(len(favicon_base64)),
        "httpMethod": "POST"
    }]
}

staged_response = requests.post(
    GRAPHQL_URL,
    json={"query": staged_upload_mutation, "variables": staged_upload_variables},
    headers=graphql_headers
)

if staged_response.status_code == 200:
    staged_data = staged_response.json()
    if 'data' in staged_data and staged_data['data']['stagedUploadsCreate']['stagedTargets']:
        staged_target = staged_data['data']['stagedUploadsCreate']['stagedTargets'][0]
        upload_url = staged_target['url']

        # Upload the file
        files = {'file': ('favicon.png', buffer, 'image/png')}
        upload_response = requests.post(upload_url, files=files)

        if upload_response.status_code in [200, 201]:
            print("✅ Favicon uploaded to Files section")
        else:
            print(f"⚠️  File upload warning: {upload_response.status_code}")
    else:
        print("⚠️  Staged upload creation failed")
else:
    print(f"⚠️  GraphQL API error: {staged_response.status_code}")

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================
print("\n" + "="*80)
print("DEPLOYMENT SUMMARY")
print("="*80)
print()
print("✅ COMPLETED:")
print("   1. Logo processed (512x512px PNG)")
print("   2. Favicon uploaded to theme assets")
print("   3. Theme settings updated")
print()
print("📋 VERIFICATION:")
print("   1. Visit: https://alphamedical.shop")
print("   2. Check browser tab for Alpha Medical logo")
print("   3. Check bookmarks (logo should appear)")
print()
print("⏰ NOTE:")
print("   - Browser cache may take 5-10 minutes to update")
print("   - Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)")
print("   - Mobile devices may need app restart")
print()
print("🔧 MANUAL ALTERNATIVE:")
print("   If logo doesn't appear after 10 minutes:")
print("   1. Shopify Admin → Online Store → Themes → Customize")
print("   2. Theme Settings → Favicon")
print("   3. Upload Images/Alpha Medical Logo Negatif.png")
print()
print("="*80)
print("FAVICON UPLOAD COMPLETE")
print("="*80)
