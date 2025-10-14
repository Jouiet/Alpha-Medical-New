#!/usr/bin/env python3
"""
Vérifier l'état des fichiers uploadés dans Shopify
"""

import requests
import json
from pathlib import Path

# Load token
env_file = Path(__file__).parent / '.env.admin'
ACCESS_TOKEN = None

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                ACCESS_TOKEN = line.split('=', 1)[1].strip()
                break

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-01"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# IDs des images uploadées
image_ids = [
    "gid://shopify/MediaImage/25778709626957",
    "gid://shopify/MediaImage/25778709725261",
    "gid://shopify/MediaImage/25778709758029",
    "gid://shopify/MediaImage/25778709856333",
    "gid://shopify/MediaImage/25778709921869"
]

def check_files():
    """Query files via GraphQL"""
    graphql_url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

    query = """
    {
      files(first: 20, query: "media_type:IMAGE") {
        edges {
          node {
            ... on MediaImage {
              id
              alt
              image {
                url
                width
                height
              }
              fileStatus
              createdAt
            }
          }
        }
      }
    }
    """

    response = requests.post(
        graphql_url,
        headers=headers,
        json={"query": query}
    )

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return

    data = response.json()

    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    check_files()
