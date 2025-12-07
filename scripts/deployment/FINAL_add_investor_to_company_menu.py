#!/usr/bin/env python3
"""
FINAL FIX - Add Investor Relations to COMPANY menu
Approach: Hardcode link in footer.liquid WITHIN the menu loop structure
Conditional: Only add to footer-company menu (not other menus)
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

# Get current footer
footer = get_footer()

print("Step 1: Locating menu rendering structure...")

# Find the exact location where menu links are rendered
# We need to add our link AFTER the {% endfor %} but BEFORE the </ul>
target_pattern = '{%- endfor -%}\n                      </ul>'

if target_pattern in footer:
    print("✅ Found menu rendering structure")

    # Create the conditional link that only shows for footer-company menu
    investor_link = '''                        {%- comment -%} Hardcoded Investor Relations link for COMPANY menu {%- endcomment -%}
                        {%- if block.settings.menu.handle == 'footer-company' -%}
                          <li>
                            <a href="/pages/investors" class="link link--text list-menu__item list-menu__item--link">
                              Investor Relations
                            </a>
                          </li>
                        {%- endif -%}
'''

    # Insert the link after the endfor and before the </ul>
    replacement = '{%- endfor -%}\n' + investor_link + '                      </ul>'

    footer = footer.replace(target_pattern, replacement)

    print("\nStep 2: Verifying modification...")

    # Save for inspection
    with open('/tmp/footer_final_fix.liquid', 'w') as f:
        f.write(footer)

    # Verify the change was made
    if 'footer-company' in footer and 'Investor Relations' in footer:
        print("✅ Modification verified - conditional link added")

        print("\nStep 3: Updating Shopify theme...")
        if update_footer(footer):
            print("\n" + "="*70)
            print("✅ FOOTER FIXED - Investor Relations added to COMPANY menu")
            print("="*70)
            print("\nImplementation:")
            print("  • Added hardcoded link within COMPANY menu structure")
            print("  • Conditional: Only shows for footer-company menu")
            print("  • Location: After dynamic menu items, before </ul>")
            print("\nExpected footer COMPANY column:")
            print("  1. About Us")
            print("  2. Our Quality Promise")
            print("  3. Healthcare Professionals")
            print("  4. Investor Relations  ← NEW (hardcoded)")
            print("\nVerify: https://alphamedical.shop")
            print("\nSaved preview: /tmp/footer_final_fix.liquid")
        else:
            print("\n❌ Failed to update Shopify")
    else:
        print("❌ Modification verification failed")
else:
    print("❌ Could not find target pattern in footer")
    print("\nSearching for alternative patterns...")

    # Try alternative pattern (with different spacing)
    lines = footer.split('\n')
    for i, line in enumerate(lines):
        if 'endfor' in line and i+1 < len(lines) and '</ul>' in lines[i+1]:
            print(f"Found potential location at line {i+1}:")
            print(f"  {i+1}: {line}")
            print(f"  {i+2}: {lines[i+1]}")
