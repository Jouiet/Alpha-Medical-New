#!/usr/bin/env python3
"""
Update Main Menu via GraphQL - Remove Posture, Add Beauty
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

GRAPHQL_URL = f"https://{SHOPIFY_STORE}/admin/api/2025-10/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query, variables=None):
    """Execute GraphQL query/mutation"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    
    response = requests.post(GRAPHQL_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return None

def main():
    print("=" * 80)
    print("UPDATING MAIN MENU VIA GRAPHQL")
    print("=" * 80)
    
    # Step 1: Get menu with item IDs
    query = """
    {
      menu(id: "gid://shopify/Menu/220095053901") {
        id
        handle
        items {
          id
          title
          url
          type
        }
      }
    }
    """
    
    print("\n🔍 Fetching main menu...")
    result = graphql_query(query)
    
    if not result or 'data' not in result:
        print("❌ Failed")
        return 1
    
    menu = result['data']['menu']
    posture_item = None
    
    print(f"\n✅ Current menu items:")
    for item in menu['items']:
        print(f"   - {item['title']} ({item['url']})")
        if 'posture' in item['title'].lower():
            posture_item = item
    
    # Step 2: Delete Posture & Support
    if posture_item:
        print(f"\n🗑️  Deleting '{posture_item['title']}'...")
        
        delete_mutation = f"""
        mutation {{
          menuItemDelete(id: "{posture_item['id']}") {{
            deletedMenuItemId
            userErrors {{
              field
              message
            }}
          }}
        }}
        """
        
        delete_result = graphql_query(delete_mutation)
        
        if delete_result and 'data' in delete_result:
            if delete_result['data']['menuItemDelete']['deletedMenuItemId']:
                print(f"   ✅ Deleted!")
            else:
                errors = delete_result['data']['menuItemDelete']['userErrors']
                print(f"   ❌ Errors: {errors}")
    
    # Step 3: Add Beauty & Anti-Aging
    print(f"\n➕ Adding 'Beauty & Anti-Aging'...")
    
    create_mutation = """
    mutation menuItemCreate($menuId: ID!, $title: String!, $url: String!) {
      menuItemCreate(id: $menuId, menuItem: {title: $title, url: $url}) {
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
        "menuId": "gid://shopify/Menu/220095053901",
       "title": "Beauty & Anti-Aging",
        "url": "/collections/beauty-anti-aging"
    }
    
    create_result = graphql_query(create_mutation, variables)
    
    if create_result and 'data' in create_result:
        if create_result['data']['menuItemCreate']['menuItem']:
            print(f"   ✅ Added!")
        else:
            errors = create_result['data']['menuItemCreate']['userErrors']
            print(f"   ❌ Errors: {errors}")
    
    # Step 4: Verify final menu
    print(f"\n🎯 Final menu:")
    final_result = graphql_query(query)
    
    if final_result and 'data' in final_result:
        for item in final_result['data']['menu']['items']:
            print(f"   - {item['title']}")
    
    print(f"\n🎉 Menu updated! Visit site to verify.")
    return 0

if __name__ == "__main__":
    exit(main())
