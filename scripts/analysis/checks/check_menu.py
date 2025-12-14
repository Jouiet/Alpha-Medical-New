#!/usr/bin/env python3
"""
Update Shopify Navigation Menu - Remove Posture & Support, Add Beauty & Anti-Aging
"""

import requests
import json
import sys

# Load credentials
SHOPIFY_STORE = None
SHOPIFY_ACCESS_TOKEN = None

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_ACCESS_TOKEN = line.split('=', 1)[1].strip()
            elif line.startswith('SHOPIFY_STORE_DOMAIN='):
                SHOPIFY_STORE = line.split('=', 1)[1].strip()
except FileNotFoundError:
    print("❌ .env.admin not found")
    sys.exit(1)

if not SHOPIFY_STORE or not SHOPIFY_ACCESS_TOKEN:
    print("❌ Missing credentials")
    sys.exit(1)

GRAPHQL_URL = f"https://{SHOPIFY_STORE}/admin/api/2025-10/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query):
    """Execute GraphQL query"""
    response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ GraphQL Error: {response.status_code}")
        print(response.text)
        return None

def main():
    print("=" * 80)
    print("UPDATING NAVIGATION MENU")
    print("=" * 80)
    
    # Get all menus (linklists)
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
    
    print("\n🔍 Fetching menus...")
    result = graphql_query(query)
    
    if not result or 'data' not in result:
        print("❌ Failed to fetch menus")
        return 1
    
    menus = result['data']['menus']['edges']
    
    print(f"Found {len(menus)} menus:")
    for menu_edge in menus:
        menu = menu_edge['node']
        print(f"\n📋 {menu['title']} (handle: {menu['handle']})")
        print(f"   ID: {menu['id']}")
        print(f"   Items:")
        for item in menu['items']:
            print(f"     - {item['title']}: {item['url']}")
    
    # Find main-menu
    main_menu = None
    for menu_edge in menus:
        if menu_edge['node']['handle'] == 'main-menu':
            main_menu = menu_edge['node']
            break
    
    if not main_menu:
        print("\n❌ main-menu not found!")
        return 1
    
    print(f"\n✅ Found main-menu (ID: {main_menu['id']})")
    
    # Check if Posture & Support exists
    has_posture = any('posture' in item['title'].lower() for item in main_menu['items'])
    has_beauty = any('beauty' in item['title'].lower() or 'anti-aging' in item['title'].lower() for item in main_menu['items'])
    
    print(f"\n📊 Current state:")
    print(f"   - Has 'Posture & Support': {has_posture}")
    print(f"   - Has 'Beauty & Anti-Aging': {has_beauty}")
    
    if has_posture:
        print("\n⚠️  'Posture & Support' still in menu - needs removal")
        print("   This must be updated in Shopify Admin → Navigation")
        print("   Or via menu update mutation")
    
    if not has_beauty:
        print("\n⚠️  'Beauty & Anti-Aging' missing from menu - needs addition")
    
    # Print instructions
    print("\n" + "=" * 80)
    print("INSTRUCTIONS TO UPDATE MENU")
    print("=" * 80)
    print("\n🛠️  MANUAL METHOD (Shopify Admin):")
    print("   1. Go to: Shopify Admin → Online Store → Navigation")
    print("   2. Click 'Main menu'")
    print("   3. Remove 'Posture & Support' menu item")
    print("   4. Add 'Beauty & Anti-Aging' menu item:")
    print("      - Title: Beauty & Anti-Aging")
    print("      - Link: /collections/beauty-anti-aging")
    print("   5. Save")
    
    print("\n🤖 AUTOMATED METHOD (Using Browser MCP):")
    print("   Will use chrome-devtools-mcp to automate this")
    
    return 0

if __name__ == "__main__":
    exit(main())
