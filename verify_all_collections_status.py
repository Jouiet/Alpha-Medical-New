#!/usr/bin/env python3
"""
Vérification de TOUTES les collections et leur statut de publication
"""

import json
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-10')

headers = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def fetch_all_collections_detailed():
    """Récupère toutes les collections avec détails de publication"""
    query = """
    {
      collections(first: 250) {
        edges {
          node {
            id
            title
            handle
            products(first: 1) {
              edges {
                node {
                  id
                }
              }
            }
            publications(first: 10) {
              edges {
                node {
                  publishDate
                  publication {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    """

    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
    response = requests.post(url, headers=headers, json={'query': query})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"ERROR: {response.status_code}")
        print(response.text[:500])
        return None

def main():
    print("=" * 80)
    print("VÉRIFICATION EXHAUSTIVE DE TOUTES LES COLLECTIONS")
    print("=" * 80)

    data = fetch_all_collections_detailed()

    if not data or 'data' not in data:
        print("❌ Erreur lors de la récupération")
        if data:
            print(json.dumps(data, indent=2)[:500])
        return

    collections = data['data']['collections']['edges']

    print(f"\nTotal collections: {len(collections)}\n")

    collections_info = []

    for coll_edge in collections:
        coll = coll_edge['node']
        coll_id = coll['id']
        coll_title = coll['title']
        coll_handle = coll['handle']
        publications = coll['publications']['edges']

        # Vérifier si publié sur Online Store
        published_on_storefront = False
        for pub_edge in publications:
            pub_name = pub_edge['node']['publication']['name']
            if pub_name == 'Online Store':
                published_on_storefront = True
                break

        status_icon = "✅" if published_on_storefront else "❌"

        collections_info.append({
            'id': coll_id,
            'title': coll_title,
            'handle': coll_handle,
            'published_on_storefront': published_on_storefront,
            'total_publications': len(publications)
        })

        print(f"{status_icon} {coll_title}")
        print(f"   Handle: {coll_handle}")
        print(f"   Published on Online Store: {'YES' if published_on_storefront else 'NO'}")
        print(f"   URL: https://alphamedical.shop/collections/{coll_handle}")
        print()

    # Résumé
    published = [c for c in collections_info if c['published_on_storefront']]
    unpublished = [c for c in collections_info if not c['published_on_storefront']]

    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"Total: {len(collections_info)} collections")
    print(f"✅ Publiées sur Online Store: {len(published)}")
    print(f"❌ NON publiées: {len(unpublished)}")

    if unpublished:
        print(f"\n⚠️ Collections NON PUBLIÉES:")
        for c in unpublished:
            print(f"   - {c['title']} ({c['handle']})")

    # Sauvegarder
    output = {
        'timestamp': '2025-10-15T04:10:00',
        'summary': {
            'total_collections': len(collections_info),
            'published': len(published),
            'unpublished': len(unpublished)
        },
        'collections': collections_info
    }

    with open('all_collections_status.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Résultats sauvegardés: all_collections_status.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
