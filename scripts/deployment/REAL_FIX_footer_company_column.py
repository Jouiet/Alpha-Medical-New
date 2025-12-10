#!/usr/bin/env python3
"""
REAL FIX - Add Investor Relations to COMPANY column properly
This time VERIFY the result
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

footer = get_footer()

# Save original for debugging
with open('/tmp/footer_before.liquid', 'w') as f:
    f.write(footer)

print("STEP 1: Remove the isolated 'Investors' section (lines 277-286)")

# Find and remove the exact block
isolated_section_start = footer.find('<div class="footer__column footer__localization isolate">\n          <div class="footer__item">\n            <h2 class="footer-block__heading inline-richtext">Investors</h2>')

if isolated_section_start != -1:
    # Find the closing </div></div> for this block
    # Count from start to find matching closing tags
    search_pos = isolated_section_start
    div_count = 2  # We have 2 opening divs
    current_pos = search_pos

    while div_count > 0:
        next_open = footer.find('<div', current_pos + 1)
        next_close = footer.find('</div>', current_pos + 1)

        if next_close == -1:
            break

        if next_open != -1 and next_open < next_close:
            div_count += 1
            current_pos = next_open
        else:
            div_count -= 1
            current_pos = next_close

    if div_count == 0:
        # Found the matching closing tag
        end_pos = current_pos + len('</div>')
        footer = footer[:isolated_section_start] + footer[end_pos:]
        print(f"✅ Removed isolated section (chars {isolated_section_start} to {end_pos})")
    else:
        print("❌ Could not find matching closing tags")
else:
    print("❌ Isolated section not found")

# Save after removal
with open('/tmp/footer_after_removal.liquid', 'w') as f:
    f.write(footer)

print("\nSTEP 2: Find COMPANY menu block and add Investor Relations")

# Look for the COMPANY menu block - it's defined in the schema
# Find the menu block that contains "About Us" or "Our Quality Promise"

# Strategy: Find "Our Quality Promise" link and add after it
quality_link = 'Our Quality Promise</a>'

if quality_link in footer:
    pos = footer.find(quality_link)
    # Find the </li> after this link
    closing_li = footer.find('</li>', pos)

    if closing_li != -1:
        # Insert new list item
        new_link = '''
              <li>
                <a href="/pages/investors" class="link link--text list-menu__item">Investor Relations</a>
              </li>'''

        footer = footer[:closing_li + 5] + new_link + footer[closing_li + 5:]
        print(f"✅ Added Investor Relations after 'Our Quality Promise'")
    else:
        print("❌ Could not find closing </li>")
else:
    print("❌ Could not find 'Our Quality Promise' link")

# Save final version
with open('/tmp/footer_final.liquid', 'w') as f:
    f.write(footer)

# Verify before uploading
if 'Investor Relations' in footer:
    # Check it's NOT in an isolated "Investors" section
    if '<h2 class="footer-block__heading inline-richtext">Investors</h2>' not in footer:
        print("\n✅ VERIFICATION PASSED: Investor Relations link exists, no isolated section")

        # Update
        if update_footer(footer):
            print("\n" + "="*70)
            print("✅ FOOTER UPDATED SUCCESSFULLY")
            print("="*70)
            print("\nFooter structure:")
            print("- COMPANY column now includes: About Us, Our Quality Promise, Investor Relations")
            print("- No isolated 'Investors' section")
            print("\nVerify: https://alphamedical.shop")
        else:
            print("\n❌ Failed to update Shopify")
    else:
        print("\n❌ VERIFICATION FAILED: Isolated 'Investors' section still exists!")
else:
    print("\n❌ VERIFICATION FAILED: Investor Relations link not found!")
