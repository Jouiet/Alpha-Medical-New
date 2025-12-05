#!/usr/bin/env python3
"""Check which Shopify theme is currently live"""

import os
import requests

SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_STORE_DOMAIN = 'azffej-as.myshopify.com'

url = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10/themes.json'
headers = {'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    themes = response.json()['themes']

    print("=" * 60)
    print("SHOPIFY THEMES")
    print("=" * 60)

    for theme in themes:
        role_marker = "🟢 LIVE" if theme['role'] == 'main' else "⚪ Unpublished"
        print(f"{role_marker} ID: {theme['id']}")
        print(f"   Name: {theme['name']}")
        print(f"   Role: {theme['role']}")
        print(f"   Created: {theme['created_at'][:10]}")
        print()

    # Check if we deployed to the right theme
    live_theme = next((t for t in themes if t['role'] == 'main'), None)
    deployed_theme_id = '140069830733'

    print("=" * 60)
    print("DEPLOYMENT VERIFICATION")
    print("=" * 60)

    if live_theme:
        print(f"Live theme ID: {live_theme['id']}")
        print(f"Deployed to ID: {deployed_theme_id}")

        if str(live_theme['id']) == deployed_theme_id:
            print("✅ Deployed to CORRECT (live) theme")
        else:
            print("❌ Deployed to WRONG theme!")
            print(f"   Need to redeploy to theme ID: {live_theme['id']}")

else:
    print(f"Error: HTTP {response.status_code}")
    print(response.text)
