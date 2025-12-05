#!/usr/bin/env python3
"""
Check footer menu structure via GraphQL Admin API
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
API_VERSION = '2025-10'

graphql_url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

HEADERS = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

# Query to get all menus
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
          type
        }
      }
    }
  }
}
"""

response = requests.post(
    graphql_url,
    headers=HEADERS,
    json={'query': query}
)

if response.status_code != 200:
    print(f"❌ ERROR: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()

if 'errors' in data:
    print(f"❌ GraphQL ERRORS: {json.dumps(data['errors'], indent=2)}")
    exit(1)

menus = data.get('data', {}).get('menus', {}).get('edges', [])

print(f"\n{'='*60}")
print(f"FOUND {len(menus)} MENUS")
print(f"{'='*60}\n")

for menu_edge in menus:
    menu = menu_edge['node']
    print(f"Menu: {menu['title']}")
    print(f"  Handle: {menu['handle']}")
    print(f"  ID: {menu['id']}")
    print(f"  Items: {len(menu['items'])}")

    if 'footer' in menu['handle'].lower() or 'footer' in menu['title'].lower():
        print(f"\n  📋 FOOTER MENU ITEMS:")
        for item in menu['items']:
            print(f"    - {item['title']}: {item['url']}")

        # Check for required policy links
        required_links = {
            'Privacy Policy': '/policies/privacy-policy',
            'Terms of Service': '/policies/terms-of-service',
            'Refund Policy': '/policies/refund-policy',
            'Shipping Policy': '/pages/shipping-delivery',
            'Accessibility': '/pages/accessibility'
        }

        found_links = {item['title']: item['url'] for item in menu['items']}

        print(f"\n  ✅ VERIFICATION:")
        for name, url in required_links.items():
            if any(url in found_url for found_url in found_links.values()):
                print(f"    ✅ {name}: FOUND")
            else:
                print(f"    ❌ {name}: MISSING")

    print()
