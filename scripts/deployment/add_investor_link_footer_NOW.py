#!/usr/bin/env python3
"""
ADD INVESTOR RELATIONS LINK TO FOOTER - NOW
Uses Shopify theme files API to add the link directly to footer.liquid
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

def get_published_theme_id():
    """Get the published theme ID"""
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        themes = response.json()['themes']
        for theme in themes:
            if theme['role'] == 'main':
                return theme['id']
    return None

def get_footer_asset(theme_id):
    """Get footer.liquid content"""
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    params = {'asset[key]': 'sections/footer.liquid'}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['asset']['value']
    return None

def update_footer_asset(theme_id, new_content):
    """Update footer.liquid"""
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    data = {
        'asset': {
            'key': 'sections/footer.liquid',
            'value': new_content
        }
    }

    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200

def add_investor_link_to_footer():
    """Add Investor Relations link to footer COMPANY section"""

    # Get theme ID
    theme_id = get_published_theme_id()
    if not theme_id:
        print("❌ Could not find published theme")
        return False

    print(f"✅ Found theme ID: {theme_id}")

    # Get footer content
    footer_content = get_footer_asset(theme_id)
    if not footer_content:
        print("❌ Could not fetch footer.liquid")
        return False

    print(f"✅ Fetched footer.liquid ({len(footer_content)} characters)")

    # Check if already added
    if 'Investor Relations' in footer_content or '/pages/investors' in footer_content:
        print("✅ Investor Relations link already exists in footer")
        return True

    # Find COMPANY section or About Us section
    # Look for patterns like "About" or "Company" menu

    # Strategy: Add after "About Us" link if it exists
    patterns_to_try = [
        ('About</a>', 'About</a>\n              <li><a href="/pages/investors">Investor Relations</a></li>'),
        ('About Us</a>', 'About Us</a>\n              <li><a href="/pages/investors">Investor Relations</a></li>'),
        ('Contact</a>', 'Contact</a>\n              <li><a href="/pages/investors">Investor Relations</a></li>'),
        ('Policies</a>', '<li><a href="/pages/investors">Investor Relations</a></li>\n              Policies</a>'),
    ]

    updated = False
    for pattern, replacement in patterns_to_try:
        if pattern in footer_content:
            new_content = footer_content.replace(pattern, replacement, 1)
            if update_footer_asset(theme_id, new_content):
                print(f"✅ Added Investor Relations link after '{pattern}'")
                return True
            break

    if not updated:
        # Fallback: Add to end of first <ul> in footer
        if '<ul>' in footer_content:
            first_ul_close = footer_content.find('</ul>')
            if first_ul_close != -1:
                new_content = (
                    footer_content[:first_ul_close] +
                    '            <li><a href="/pages/investors">Investor Relations</a></li>\n          ' +
                    footer_content[first_ul_close:]
                )
                if update_footer_asset(theme_id, new_content):
                    print("✅ Added Investor Relations link to footer (fallback position)")
                    return True

    print("❌ Could not find suitable location in footer to add link")
    print("   Manual addition required via Shopify Admin")
    return False

if __name__ == "__main__":
    print("="*70)
    print("ADD INVESTOR RELATIONS LINK TO FOOTER - AUTOMATED")
    print("="*70)
    print()

    if add_investor_link_to_footer():
        print()
        print("="*70)
        print("✅ SUCCESS: Investor Relations link added to footer")
        print("="*70)
        print()
        print("Verify at: https://alphamedical.shop (scroll to footer)")
    else:
        print()
        print("="*70)
        print("⚠️  FALLBACK: Manual addition required")
        print("="*70)
        print()
        print("Go to: https://admin.shopify.com/store/azffej-as/themes/current/editor")
        print("Edit footer section → Add link manually")
