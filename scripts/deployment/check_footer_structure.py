#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

# Get all menus
url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

query = """
{
  shop {
    navigationMenus(first: 20) {
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
}
"""

response = requests.post(
    url,
    headers={
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    },
    json={'query': query}
)

import json
print(json.dumps(response.json(), indent=2))
