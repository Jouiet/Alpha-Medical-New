#!/usr/bin/env python3
"""
FACTUAL VERIFICATION - Check confetti script is deployed correctly
Uses Shopify Admin API to fetch theme files and verify content
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_NAME = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2024-10'
THEME_ID = '140069830733'

BASE_URL = f'https://{SHOP_NAME}/admin/api/{API_VERSION}'
HEADERS = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def fetch_asset(theme_key):
    """Fetch asset content from Shopify."""
    url = f'{BASE_URL}/themes/{THEME_ID}/assets.json'
    params = {'asset[key]': theme_key}

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        return response.json()['asset']['value']
    else:
        return None

print("=" * 80)
print("FACTUAL VERIFICATION - Confetti Deployment Check")
print("=" * 80)
print()

# TEST 1: Verify theme.liquid contains confetti script
print("TEST 1: Checking layout/theme.liquid...")
theme_content = fetch_asset('layout/theme.liquid')

if theme_content:
    if 'window.triggerFreeShippingConfetti' in theme_content:
        print("  ✅ Confetti script found in theme.liquid")

        # Count lines
        script_start = theme_content.find('window.triggerFreeShippingConfetti')
        if script_start > 0:
            lines_before = theme_content[:script_start].count('\n')
            print(f"  ✅ Function starts around line {lines_before}")

        # Check for MutationObserver
        if 'MutationObserver' in theme_content:
            print("  ✅ MutationObserver present")
        else:
            print("  ❌ MutationObserver MISSING")

        # Check for console logs
        if 'console.log' in theme_content and '🎊' in theme_content:
            print("  ✅ Debug logging present")
        else:
            print("  ❌ Debug logging MISSING")
    else:
        print("  ❌ Confetti script NOT found in theme.liquid")
        print("  🚨 CRITICAL ERROR: Script not deployed!")
else:
    print("  ❌ Could not fetch theme.liquid")

print()

# TEST 2: Verify snippet has CSS but no script
print("TEST 2: Checking snippets/free-shipping-progress-bar.liquid...")
snippet_content = fetch_asset('snippets/free-shipping-progress-bar.liquid')

if snippet_content:
    has_css = '#confetti-container' in snippet_content or 'confetti-piece' in snippet_content
    has_script = 'window.triggerFreeShippingConfetti' in snippet_content
    has_trigger_attr = 'data-confetti-trigger' in snippet_content

    print(f"  CSS present: {'✅' if has_css else '❌'}")
    print(f"  Script present: {'❌ (correct)' if not has_script else '🚨 (should be removed!)'}")
    print(f"  Trigger attribute: {'✅' if has_trigger_attr else '❌'}")

    if has_css and not has_script and has_trigger_attr:
        print("  ✅ Snippet correctly configured")
    else:
        print("  ❌ Snippet configuration issue")
else:
    print("  ❌ Could not fetch snippet")

print()

# TEST 3: Verify CSS animations
print("TEST 3: Checking confetti CSS animations...")
if snippet_content:
    animations = [
        '@keyframes confetti-fall',
        'pointer-events: none',
        'position: fixed',
        'z-index: 9999'
    ]

    for animation in animations:
        if animation in snippet_content:
            print(f"  ✅ {animation}")
        else:
            print(f"  ❌ MISSING: {animation}")
else:
    print("  ⚠️  Could not verify CSS")

print()
print("=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

# Calculate status
script_in_theme = theme_content and 'window.triggerFreeShippingConfetti' in theme_content
css_in_snippet = snippet_content and '#confetti-container' in snippet_content
no_script_in_snippet = snippet_content and 'window.triggerFreeShippingConfetti' not in snippet_content
trigger_in_snippet = snippet_content and 'data-confetti-trigger' in snippet_content

all_checks = [
    script_in_theme,
    css_in_snippet,
    no_script_in_snippet,
    trigger_in_snippet
]

if all(all_checks):
    print("✅ ALL CHECKS PASSED - Confetti correctly deployed")
    print()
    print("Next step: Test on live site with Console open")
    print("Expected logs:")
    print("  1. ✅ Confetti system initialized")
    print("  2. 👀 MutationObserver started")
    print("  3. 🎯 Confetti trigger found! (when cart >= $150)")
    print("  4. 🎉 50 confetti pieces launched!")
else:
    print("❌ DEPLOYMENT ISSUES DETECTED")
    print()
    if not script_in_theme:
        print("  🚨 Script NOT in theme.liquid - redeploy required")
    if not css_in_snippet:
        print("  🚨 CSS NOT in snippet - redeploy required")
    if not no_script_in_snippet:
        print("  🚨 Script still in snippet - should be removed")
    if not trigger_in_snippet:
        print("  🚨 Trigger attribute missing from snippet")

print("=" * 80)
