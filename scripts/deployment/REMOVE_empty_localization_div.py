#!/usr/bin/env python3
"""
REMOVE empty footer__localization div that breaks country selector
This div was added by FORCE_add_investor_footer.py and is now empty after removing Investors
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'
theme_id = 140069830733

def get_footer():
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    response = requests.get(url, headers=headers, params={'asset[key]': 'sections/footer.liquid'})
    return response.json()['asset']['value']

def update_footer(content):
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    data = {'asset': {'key': 'sections/footer.liquid', 'value': content}}
    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200

# Get footer
footer = get_footer()

print("Searching for empty footer__localization div...")

lines = footer.split('\n')

# Find the empty localization div (lines 286-288)
# Pattern:
#   <div class="footer__column footer__localization isolate">
#   </div>
# </div>

target_found = False
for i in range(len(lines) - 2):
    if ('footer__localization' in lines[i] and
        lines[i+1].strip() == '</div>' and
        lines[i+2].strip() == '</div>'):

        print(f"\n✅ Found empty localization div at lines {i+1}-{i+3}:")
        print(f"   {i+1}: {lines[i]}")
        print(f"   {i+2}: {lines[i+1]}")
        print(f"   {i+3}: {lines[i+2]}")

        # Remove these 3 lines
        new_lines = lines[:i] + lines[i+3:]
        footer = '\n'.join(new_lines)

        target_found = True
        print(f"\n✅ Removed lines {i+1}-{i+3}")
        break

if target_found:
    # Verify removal
    if 'footer__localization' not in footer:
        print("\n✅ Verification: footer__localization div completely removed")

        # Save for inspection
        with open('/tmp/footer_localization_removed.liquid', 'w') as f:
            f.write(footer)

        # Update Shopify
        print("\nUpdating Shopify...")
        if update_footer(footer):
            print("\n" + "="*70)
            print("✅ EMPTY DIV REMOVED - Country selector should be restored")
            print("="*70)
            print("\nRemoved:")
            print("  ❌ Empty <div class='footer__localization'> (artifact from FORCE_add_investor_footer.py)")
            print("\nResult:")
            print("  ✅ Footer structure cleaned")
            print("  ✅ Country/region selector should now display correctly")
            print("\nVerify: https://alphamedical.shop")
            print("Look for 'Country/region' selector at bottom of footer")
        else:
            print("\n❌ Failed to update Shopify")
    else:
        print("\n⚠️ Warning: footer__localization still present after removal")
else:
    print("\n❌ Empty localization div not found")
    print("Checking current state...")

    # Show current lines around 286
    for i in range(280, min(295, len(lines))):
        print(f"{i+1:4d}: {lines[i]}")
