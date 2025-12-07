#!/usr/bin/env python3
"""
Add Investor Relations link to Footer menu
Adds a link to https://alphamedical.shop/pages/investors in the footer navigation
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('/Users/mac/Desktop/Alpha-Medical/.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2025-10')

def get_menus():
    """Get all navigation menus via GraphQL"""
    query = """
    {
      menus(first: 10) {
        edges {
          node {
            id
            handle
            title
            items {
              id
              title
              url
            }
          }
        }
      }
    }
    """

    url = f'https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/graphql.json'
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    r = requests.post(url, headers=headers, json={'query': query})
    data = r.json()

    if 'data' in data and 'menus' in data['data']:
        return data['data']['menus']['edges']
    else:
        print("Error fetching menus:", data)
        return []

def add_investor_link_to_menu(menu_id, menu_handle):
    """Add Investor Relations link to menu via GraphQL"""
    # Check if link already exists
    menus = get_menus()
    for menu in menus:
        if menu['node']['handle'] == menu_handle:
            for item in menu['node']['items']:
                if 'investors' in item['url'].lower():
                    print(f"✅ Investor Relations link already exists in {menu_handle} menu")
                    return True

    # Add the link
    mutation = """
    mutation menuItemAdd($menuId: ID!, $menuItem: MenuItemInput!) {
      menuItemAdd(menuId: $menuId, menuItem: $menuItem) {
        menuItem {
          id
          title
          url
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "menuId": menu_id,
        "menuItem": {
            "title": "Investor Relations",
            "url": "/pages/investors",
            "type": "HTTP"
        }
    }

    url = f'https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/graphql.json'
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    r = requests.post(url, headers=headers, json={'query': mutation, 'variables': variables})
    data = r.json()

    if 'data' in data and 'menuItemAdd' in data['data']:
        result = data['data']['menuItemAdd']
        if result['userErrors']:
            print("Error adding menu item:", result['userErrors'])
            return False
        else:
            print(f"✅ Investor Relations link added to {menu_handle} menu")
            print(f"   Title: {result['menuItem']['title']}")
            print(f"   URL: {result['menuItem']['url']}")
            return True
    else:
        print("Error:", data)
        return False

def main():
    print("=" * 80)
    print("ADD INVESTOR RELATIONS LINK TO FOOTER")
    print("=" * 80)
    print()

    # Get all menus
    print("Fetching navigation menus...")
    menus = get_menus()

    if not menus:
        print("❌ No menus found or error fetching menus")
        return

    print(f"Found {len(menus)} menus:\n")

    # Display menus
    footer_menu = None
    for menu in menus:
        node = menu['node']
        print(f"Menu: {node['title']} (handle: {node['handle']}, id: {node['id']})")
        print(f"Items: {len(node['items'])}")
        for item in node['items']:
            print(f"  - {item['title']}: {item['url']}")
        print()

        # Find footer menu
        if 'footer' in node['handle'].lower():
            footer_menu = node

    if footer_menu:
        print(f"\n✅ Found footer menu: {footer_menu['title']} (handle: {footer_menu['handle']})")
        print("\nAdding Investor Relations link to footer...")
        success = add_investor_link_to_menu(footer_menu['id'], footer_menu['handle'])

        if success:
            print("\n✅ SUCCESS! Investor Relations link added to footer")
            print(f"   URL: https://alphamedical.shop/pages/investors")
            print("\n   Investors can now access the page from the footer navigation.")
        else:
            print("\n❌ Failed to add link to footer")
    else:
        print("\n⚠️  No footer menu found. Available menus:")
        for menu in menus:
            print(f"  - {menu['node']['title']} (handle: {menu['node']['handle']})")
        print("\nManual action required: Add 'Investor Relations' link via Shopify Admin:")
        print("  1. Go to: Online Store → Navigation")
        print("  2. Select footer menu")
        print("  3. Add menu item:")
        print("     - Name: Investor Relations")
        print("     - Link: /pages/investors")

    print("=" * 80)

if __name__ == '__main__':
    main()
