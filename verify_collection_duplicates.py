#!/usr/bin/env python3
"""
Vérification exhaustive des doublons de produits entre collections
"""

import json
import requests
from dotenv import load_dotenv
import os
from collections import defaultdict

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-10')

headers = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def fetch_all_collections():
    """Récupère toutes les collections avec leurs produits"""
    query = """
    {
      collections(first: 250) {
        edges {
          node {
            id
            title
            handle
            productsCount
            products(first: 250) {
              edges {
                node {
                  id
                  title
                  handle
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
        print(response.text)
        return None

def main():
    print("=" * 80)
    print("VÉRIFICATION EXHAUSTIVE DES DOUBLONS ENTRE COLLECTIONS")
    print("=" * 80)

    data = fetch_all_collections()

    if not data or 'data' not in data:
        print("❌ Erreur lors de la récupération des collections")
        return

    collections = data['data']['collections']['edges']

    # Mapping produit_id → liste des collections
    product_to_collections = defaultdict(list)

    # Mapping pour les détails
    collection_details = {}
    product_details = {}

    print(f"\nCollections trouvées: {len(collections)}\n")

    for coll_edge in collections:
        coll = coll_edge['node']
        coll_id = coll['id']
        coll_title = coll['title']
        coll_handle = coll['handle']
        product_count = coll['productsCount']

        collection_details[coll_id] = {
            'title': coll_title,
            'handle': coll_handle,
            'product_count': product_count
        }

        print(f"📦 {coll_title} ({coll_handle}): {product_count} produits")

        # Parcourir les produits de cette collection
        for prod_edge in coll['products']['edges']:
            prod = prod_edge['node']
            prod_id = prod['id']
            prod_title = prod['title']

            product_details[prod_id] = {
                'title': prod_title,
                'handle': prod['handle']
            }

            product_to_collections[prod_id].append({
                'collection_id': coll_id,
                'collection_title': coll_title,
                'collection_handle': coll_handle
            })

    print("\n" + "=" * 80)
    print("ANALYSE DES DOUBLONS")
    print("=" * 80)

    # Trouver les produits dans multiple collections
    duplicates = {
        prod_id: colls
        for prod_id, colls in product_to_collections.items()
        if len(colls) > 1
    }

    if not duplicates:
        print("\n✅ AUCUN DOUBLON DÉTECTÉ!")
        print("Tous les produits sont dans exactement 1 collection.")
        return

    print(f"\n❌ DOUBLONS DÉTECTÉS: {len(duplicates)} produits")
    print(f"Total produits analysés: {len(product_to_collections)}")
    print(f"Taux de duplication: {len(duplicates)/len(product_to_collections)*100:.1f}%\n")

    # Catégoriser les doublons
    duplicate_details = []

    for prod_id, colls in duplicates.items():
        prod_title = product_details[prod_id]['title']
        collection_names = [c['collection_title'] for c in colls]
        collection_handles = [c['collection_handle'] for c in colls]

        duplicate_details.append({
            'product_id': prod_id,
            'product_title': prod_title,
            'product_handle': product_details[prod_id]['handle'],
            'collections': colls,
            'collection_count': len(colls)
        })

        print(f"\n🔴 Produit: {prod_title}")
        print(f"   ID: {prod_id}")
        print(f"   Présent dans {len(colls)} collections:")
        for i, coll in enumerate(colls, 1):
            print(f"   {i}. {coll['collection_title']} ({coll['collection_handle']})")

    # Sauvegarder les résultats
    output = {
        'timestamp': '2025-10-15T03:30:00',
        'summary': {
            'total_collections': len(collections),
            'total_products': len(product_to_collections),
            'duplicate_products': len(duplicates),
            'duplication_rate': f"{len(duplicates)/len(product_to_collections)*100:.1f}%"
        },
        'duplicates': duplicate_details,
        'collections': collection_details
    }

    with open('collection_duplicates_verification.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"Résultats sauvegardés: collection_duplicates_verification.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
