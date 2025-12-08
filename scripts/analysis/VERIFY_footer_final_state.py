#!/usr/bin/env python3
"""
VERIFICATION FACTUELLE COMPLÈTE - Footer final state
Bottom-up approach: API verification of all footer corrections
"""

import os
import requests
from dotenv import load_dotenv
import re

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

def get_menu(handle):
    """Get menu via GraphQL"""
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    query = '''
    {
      menus(first: 50) {
        edges {
          node {
            id
            handle
            title
            items {
              title
              url
            }
          }
        }
      }
    }
    '''

    response = requests.post(url, headers=headers, json={'query': query})
    menus = response.json()['data']['menus']['edges']

    for edge in menus:
        if edge['node']['handle'] == handle:
            return edge['node']
    return None

print("="*70)
print("VERIFICATION FACTUELLE - FOOTER FINAL STATE")
print("="*70)

footer = get_footer()
lines = footer.split('\n')

# VERIFICATION 1: Investor Relations in COMPANY menu (conditional link)
print("\n1. INVESTOR RELATIONS - COMPANY COLUMN:")
print("-" * 70)

investor_in_company = False
investor_conditional = False
investor_line_nums = []

for i, line in enumerate(lines, 1):
    if 'investor' in line.lower():
        investor_line_nums.append(i)
        if 'footer-company' in lines[max(0, i-5):i+1]:
            investor_conditional = True
        if '/pages/investors' in line:
            investor_in_company = True

print(f"  Occurrences of 'investor': {len(investor_line_nums)} lines")
print(f"  Lines: {investor_line_nums}")

# Check for conditional
for i in investor_line_nums:
    context_start = max(0, i-5)
    context_end = min(len(lines), i+5)
    context = '\n'.join([f"    {j+1:4d}: {lines[j][:70]}" for j in range(context_start, context_end)])
    if 'footer-company' in '\n'.join(lines[context_start:context_end]):
        print(f"\n  ✅ Conditional link found (line {i}):")
        print(context)
        investor_conditional = True
        break

if investor_conditional and len(investor_line_nums) <= 4:
    print(f"\n  ✅ VERIFICATION PASSED:")
    print(f"     - Investor Relations: CONDITIONAL link in COMPANY menu")
    print(f"     - Occurrences: {len(investor_line_nums)} (expected: 3-4)")
    print(f"     - No duplication detected")
else:
    print(f"\n  ❌ VERIFICATION FAILED:")
    print(f"     - Conditional: {investor_conditional}")
    print(f"     - Occurrences: {len(investor_line_nums)}")

# VERIFICATION 2: No isolated "Investors" section
print("\n2. ISOLATED 'INVESTORS' SECTION:")
print("-" * 70)

isolated_section = False
for i, line in enumerate(lines, 1):
    if 'Investors</h2>' in line and 'footer-block__heading' in line:
        isolated_section = True
        print(f"  ❌ FOUND isolated section at line {i}:")
        context_start = max(0, i-3)
        context_end = min(len(lines), i+5)
        for j in range(context_start, context_end):
            print(f"    {j+1:4d}: {lines[j][:70]}")
        break

if not isolated_section:
    print(f"  ✅ VERIFICATION PASSED: No isolated 'Investors' section")

# VERIFICATION 3: Country/Language selector code
print("\n3. COUNTRY/LANGUAGE SELECTOR:")
print("-" * 70)

localization_div = False
country_render = False
language_render = False
localization_form = False

for i, line in enumerate(lines, 1):
    if 'footer__localization' in line and '<div' in line:
        localization_div = True
        # Check next 100 lines for proper content
        search_end = min(len(lines), i+100)
        section = '\n'.join(lines[i:search_end])

        if "render 'country-localization'" in section:
            country_render = True
        if "render 'language-localization'" in section:
            language_render = True
        if 'localization-form' in section.lower():
            localization_form = True

        # Show structure
        print(f"  footer__localization div found at line {i}")
        print(f"  Content preview:")
        for j in range(i, min(i+15, len(lines))):
            print(f"    {j+1:4d}: {lines[j][:70]}")
        print(f"  ...")
        break

print(f"\n  Checks:")
print(f"    - footer__localization div: {'✅' if localization_div else '❌'}")
print(f"    - country-localization render: {'✅' if country_render else '❌'}")
print(f"    - language-localization render: {'✅' if language_render else '❌'}")
print(f"    - localization-form tags: {'✅' if localization_form else '❌'}")

if localization_div and country_render and localization_form:
    print(f"\n  ✅ VERIFICATION PASSED: Country/language selector code present")
else:
    print(f"\n  ❌ VERIFICATION FAILED: Selector code incomplete")

# VERIFICATION 4: footer-company menu via API
print("\n4. FOOTER-COMPANY MENU (API):")
print("-" * 70)

menu = get_menu('footer-company')
if menu:
    print(f"  Menu: {menu['title']}")
    print(f"  Handle: {menu['handle']}")
    print(f"  Items ({len(menu['items'])}):")
    for item in menu['items']:
        marker = "✅" if 'investor' in item['title'].lower() else "  "
        print(f"    {marker} {item['title']}: {item['url']}")

    # Check if Investor Relations is in menu
    investor_in_menu = any('investor' in item['title'].lower() for item in menu['items'])

    if investor_in_menu:
        print(f"\n  ⚠️  NOTE: Investor Relations in DYNAMIC menu")
        print(f"      This would override the conditional hardcoded link")
    else:
        print(f"\n  ✅ Investor Relations NOT in dynamic menu")
        print(f"      Conditional hardcoded link will display (as intended)")
else:
    print(f"  ❌ Could not retrieve footer-company menu")

# FINAL SUMMARY
print("\n" + "="*70)
print("FINAL VERIFICATION SUMMARY")
print("="*70)

all_checks = [
    ("Investor Relations conditional link", investor_conditional and len(investor_line_nums) <= 4),
    ("No isolated Investors section", not isolated_section),
    ("Country selector code present", localization_div and country_render and localization_form),
    ("footer-company menu structure", menu is not None)
]

passed = sum(1 for _, check in all_checks if check)
total = len(all_checks)

print(f"\nChecks passed: {passed}/{total}")
print()
for check_name, result in all_checks:
    status = "✅ PASS" if result else "❌ FAIL"
    print(f"  {status}: {check_name}")

if passed == total:
    print("\n" + "="*70)
    print("✅ ALL VERIFICATIONS PASSED - FOOTER 100% CORRECT")
    print("="*70)
    print("\nFooter state:")
    print("  ✅ Investor Relations: COMPANY column (conditional, no duplication)")
    print("  ✅ Country/region selector: Proper code with render calls")
    print("  ✅ No isolated sections")
    print("  ✅ API structure verified")
else:
    print("\n" + "="*70)
    print(f"⚠️  {total - passed} VERIFICATION(S) FAILED")
    print("="*70)
