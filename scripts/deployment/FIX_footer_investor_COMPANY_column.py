#!/usr/bin/env python3
"""
FIX Footer - Add Investor Relations to COMPANY column (NOT separate section)
CORRECTION: Remove isolated "Investors" section, add link to COMPANY column
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

print("STEP 1: Remove isolated 'Investors' section...")

# Remove the entire isolated investors section I wrongly added
if 'Investors' in footer and 'Investor Relations' in footer:
    # Find and remove the investor section
    start_markers = [
        '<div class="footer__column footer__localization isolate">',
        '<h2 class="footer-block__heading inline-richtext">Investors</h2>'
    ]

    for marker in start_markers:
        if marker in footer:
            start = footer.find(marker)
            if start != -1:
                # Find the closing </div> for this section
                # Look for the pattern that closes this entire column
                search_from = start
                div_count = 1
                pos = footer.find('<div', start + 1)
                end_pos = footer.find('</div>', start + 1)

                # Find matching closing div
                while div_count > 0 and end_pos != -1:
                    if pos != -1 and pos < end_pos:
                        div_count += 1
                        pos = footer.find('<div', pos + 1)
                    else:
                        div_count -= 1
                        if div_count > 0:
                            end_pos = footer.find('</div>', end_pos + 1)

                if end_pos != -1:
                    # Remove the entire section
                    footer = footer[:start] + footer[end_pos + 6:]
                    print("✅ Removed isolated 'Investors' section")
                    break

print("\nSTEP 2: Find COMPANY column and add 'Investor Relations' link...")

# Now find the COMPANY column and add Investor Relations link
# Look for "Healthcare Professionals" link (last item in COMPANY column)
healthcare_pattern = 'Healthcare Professionals</a>'

if healthcare_pattern in footer:
    # Find the position after this link
    pos = footer.find(healthcare_pattern)
    if pos != -1:
        # Move to after the closing tag
        closing_pos = footer.find('</li>', pos)
        if closing_pos != -1:
            # Insert new list item for Investor Relations
            investor_link = '\n              <li>\n                <a href="/pages/investors" class="link link--text list-menu__item">Investor Relations</a>\n              </li>'

            footer = footer[:closing_pos + 5] + investor_link + footer[closing_pos + 5:]
            print("✅ Added 'Investor Relations' to COMPANY column (after Healthcare Professionals)")
        else:
            print("❌ Could not find closing </li> tag")
    else:
        print("❌ Could not find Healthcare Professionals link")
else:
    print("❌ Healthcare Professionals pattern not found")
    print("Looking for alternative patterns...")

    # Alternative: Look for "Our Quality Promise" and add after it
    quality_pattern = 'Our Quality Promise</a>'
    if quality_pattern in footer:
        pos = footer.find(quality_pattern)
        closing_pos = footer.find('</li>', pos)
        if closing_pos != -1:
            investor_link = '\n              <li>\n                <a href="/pages/investors" class="link link--text list-menu__item">Investor Relations</a>\n              </li>'
            footer = footer[:closing_pos + 5] + investor_link + footer[closing_pos + 5:]
            print("✅ Added 'Investor Relations' to COMPANY column (after Our Quality Promise)")

# Update footer
if update_footer(footer):
    print("\n" + "="*70)
    print("✅ FOOTER FIXED - Investor Relations now in COMPANY column")
    print("="*70)
    print("\nVerify at: https://alphamedical.shop (footer → COMPANY column)")
    print("Expected: About Us, Our Quality Promise, Healthcare Professionals, Investor Relations")
else:
    print("\n❌ Failed to update footer")
