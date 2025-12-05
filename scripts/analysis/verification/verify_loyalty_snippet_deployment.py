#!/usr/bin/env python3
"""
VERIFICATION: loyalty-tier-badge.liquid Deployment Status
Date: 2025-11-20
Purpose: Verify if loyalty snippet is deployed to Shopify and integrated in account template
"""

import os
import requests

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

SHOP = "azffej-as.myshopify.com"
THEME_ID = "140069830733"  # Alpha-Medical-New/main
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN}

print("=" * 80)
print("VERIFICATION: loyalty-tier-badge.liquid Deployment")
print("=" * 80)
print(f"Theme ID: {THEME_ID}\n")

# Check 1: Verify snippet exists on Shopify
print("=" * 80)
print("CHECK 1: Snippet Deployment Status")
print("=" * 80)

response = requests.get(
    f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]=snippets/loyalty-tier-badge.liquid",
    headers=HEADERS
)

snippet_deployed = False
if response.status_code == 200:
    asset = response.json().get('asset', {})
    if asset:
        size = len(asset.get('value', ''))
        print(f"✅ DEPLOYED: snippets/loyalty-tier-badge.liquid")
        print(f"   Size: {size} bytes")
        print(f"   Status: LIVE on theme {THEME_ID}\n")
        snippet_deployed = True
    else:
        print("❌ NOT FOUND: snippets/loyalty-tier-badge.liquid")
        print("   Status: NOT deployed to Shopify\n")
else:
    print(f"❌ API Error: {response.status_code}")
    print(f"Response: {response.text[:200]}\n")

# Check 2: Verify account template integration
print("=" * 80)
print("CHECK 2: Account Template Integration")
print("=" * 80)

response2 = requests.get(
    f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]=templates/customers/account.liquid",
    headers=HEADERS
)

account_integrated = False
if response2.status_code == 200:
    asset2 = response2.json().get('asset', {})
    if asset2:
        template_content = asset2.get('value', '')
        print(f"✅ FETCHED: templates/customers/account.liquid")
        print(f"   Size: {len(template_content)} bytes\n")

        if 'loyalty-tier-badge' in template_content:
            print("✅ INTEGRATED: loyalty-tier-badge is referenced in account template")
            print()
            # Find exact line
            for i, line in enumerate(template_content.split('\n'), 1):
                if 'loyalty-tier-badge' in line:
                    print(f"   Line {i}: {line.strip()}")
            print()
            account_integrated = True
        else:
            print("❌ NOT INTEGRATED: loyalty-tier-badge is NOT referenced")
            print("   ACTION: Need to add {% render 'loyalty-tier-badge' %} to account template\n")
    else:
        print("❌ NOT FOUND: templates/customers/account.liquid")
        print("   Note: Theme might use JSON template instead\n")

        # Try JSON template
        response3 = requests.get(
            f"{REST_URL}/themes/{THEME_ID}/assets.json?asset[key]=templates/customers/account.json",
            headers=HEADERS
        )

        if response3.status_code == 200:
            asset3 = response3.json().get('asset', {})
            if asset3:
                json_content = asset3.get('value', '')
                print(f"✅ FOUND: templates/customers/account.json (JSON template)")
                print(f"   Size: {len(json_content)} bytes\n")

                if 'loyalty-tier-badge' in json_content:
                    print("✅ INTEGRATED: loyalty-tier-badge section referenced in JSON template\n")
                    account_integrated = True
                else:
                    print("❌ NOT INTEGRATED: Need to add loyalty section to JSON template\n")
else:
    print(f"❌ API Error: {response2.status_code}\n")

# Summary
print("=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

if snippet_deployed and account_integrated:
    print("✅ FULLY DEPLOYED & INTEGRATED")
    print("   - Snippet exists on Shopify")
    print("   - Integrated in account template")
    print("   - Ready for use\n")
    exit(0)
elif snippet_deployed and not account_integrated:
    print("⚠️  PARTIALLY DEPLOYED")
    print("   - ✅ Snippet exists on Shopify")
    print("   - ❌ NOT integrated in account template")
    print("\n📋 NEXT STEPS:")
    print("   1. Add {% render 'loyalty-tier-badge' %} to account template")
    print("   2. Deploy account template to Shopify\n")
    exit(1)
else:
    print("❌ NOT DEPLOYED")
    print("\n📋 NEXT STEPS:")
    print("   1. Deploy snippets/loyalty-tier-badge.liquid to Shopify")
    print("   2. Integrate in account template")
    print("   3. Create discount codes (LOYALTY10, LOYALTY15, LOYALTY25, LOYALTY50)\n")
    exit(1)
