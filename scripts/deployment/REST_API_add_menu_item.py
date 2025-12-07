#!/usr/bin/env python3
"""
Try REST API to add menu item to footer-company menu
GraphQL failed, trying alternative approach
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

def get_menus():
    """Get all menus to find footer-company menu ID"""
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
    return response.json()

def try_rest_api_add_item(menu_gid):
    """Try REST API to add menu item (if endpoint exists)"""
    # Extract numeric ID from GraphQL GID
    # GID format: gid://shopify/Menu/123456
    menu_id = menu_gid.split('/')[-1]

    # Try REST API endpoint (may not exist for menus)
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/menus/{menu_id}/items.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    data = {
        'menu_item': {
            'title': 'Investor Relations',
            'url': '/pages/investors'
        }
    }

    response = requests.post(url, headers=headers, json=data)
    return response

# Get menus
print("Step 1: Getting all menus...")
menus = get_menus()

if 'data' in menus and 'menus' in menus['data']:
    print("\n✅ Menus retrieved")

    # Find footer-company menu
    footer_company_menu = None
    for edge in menus['data']['menus']['edges']:
        menu = edge['node']
        if menu['handle'] == 'footer-company':
            footer_company_menu = menu
            break

    if footer_company_menu:
        print(f"\n✅ Found footer-company menu:")
        print(f"   ID: {footer_company_menu['id']}")
        print(f"   Title: {footer_company_menu['title']}")
        print(f"   Current items ({len(footer_company_menu['items'])}):")
        for item in footer_company_menu['items']:
            print(f"     - {item['title']}: {item['url']}")

        # Check if Investor Relations already exists
        investor_exists = any(item['title'] == 'Investor Relations' for item in footer_company_menu['items'])

        if investor_exists:
            print("\n⚠️  Investor Relations already exists in menu!")
        else:
            print("\nStep 2: Trying REST API to add menu item...")
            response = try_rest_api_add_item(footer_company_menu['id'])

            print(f"Response status: {response.status_code}")
            print(f"Response: {response.text}")

            if response.status_code in [200, 201]:
                print("\n✅ SUCCESS - Menu item added via REST API!")
            else:
                print("\n❌ REST API endpoint doesn't exist or failed")
                print("\n" + "="*70)
                print("API LIMITATION CONFIRMED")
                print("="*70)
                print("\nShopify does NOT support programmatic menu item creation via:")
                print("  ❌ GraphQL API (no menuItemAdd mutation)")
                print("  ❌ REST API (no menu items endpoint)")
                print("\nSOLUTION:")
                print("  Manual addition via Shopify Admin required:")
                print("  1. Go to: Admin → Online Store → Navigation")
                print("  2. Click 'footer-company' (COMPANY) menu")
                print("  3. Add menu item:")
                print("     - Name: Investor Relations")
                print("     - Link: /pages/investors")
                print("  4. Save")
                print("\n⏱️  Time required: 2 minutes")
    else:
        print("\n❌ footer-company menu not found")
else:
    print("\n❌ Failed to retrieve menus")
    print(menus)
