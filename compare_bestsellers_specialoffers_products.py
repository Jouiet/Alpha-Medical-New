#!/usr/bin/env python3
"""
Comparaison détaillée des produits dans Bestsellers vs Special Offers
Vérification si les MÊMES produits existent dans les deux collections
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

def fetch_collection_products(collection_handle):
    """Récupère tous les produits d'une collection"""
    query = """
    {
      collectionByHandle(handle: "%s") {
        id
        title
        handle
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
    """ % collection_handle

    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
    response = requests.post(url, headers=headers, json={'query': query})

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']['collectionByHandle']:
            return data['data']['collectionByHandle']
    return None

def main():
    print("=" * 80)
    print("COMPARAISON DÉTAILLÉE: BESTSELLERS vs SPECIAL OFFERS")
    print("=" * 80)

    # Fetch Bestsellers
    bestsellers = fetch_collection_products('bestsellers')
    special_offers = fetch_collection_products('special-offers')

    if not bestsellers:
        print("❌ Impossible de récupérer Bestsellers")
        return

    if not special_offers:
        print("❌ Impossible de récupérer Special Offers")
        return

    # Extraire les produits
    bestsellers_products = {}
    for edge in bestsellers['products']['edges']:
        prod = edge['node']
        bestsellers_products[prod['id']] = {
            'title': prod['title'],
            'handle': prod['handle']
        }

    special_offers_products = {}
    for edge in special_offers['products']['edges']:
        prod = edge['node']
        special_offers_products[prod['id']] = {
            'title': prod['title'],
            'handle': prod['handle']
        }

    print(f"✅ Bestsellers: {len(bestsellers_products)} produits")
    print(f"✅ Special Offers: {len(special_offers_products)} produits")

    # Trouver overlap
    bestsellers_ids = set(bestsellers_products.keys())
    special_offers_ids = set(special_offers_products.keys())
    overlap_ids = bestsellers_ids.intersection(special_offers_ids)

    print("\n" + "=" * 80)
    print("ANALYSE OVERLAP")
    print("=" * 80)

    print(f"\n📊 Overlap: {len(overlap_ids)} produits présents dans les DEUX collections")

    if len(overlap_ids) > 0:
        print("\n❌ DOUBLONS DÉTECTÉS:")
        overlap_list = []
        for prod_id in sorted(overlap_ids, key=lambda x: bestsellers_products[x]['title']):
            prod = bestsellers_products[prod_id]
            print(f"\n   🔴 {prod['title']}")
            print(f"      ID: {prod_id}")
            print(f"      Handle: {prod['handle']}")
            overlap_list.append({
                'product_id': prod_id,
                'title': prod['title'],
                'handle': prod['handle']
            })
    else:
        print("\n✅ AUCUN DOUBLON - Collections 100% séparées")

    # Afficher produits UNIQUEMENT dans Bestsellers
    only_bestsellers = bestsellers_ids - special_offers_ids
    print(f"\n📦 Produits UNIQUEMENT dans Bestsellers: {len(only_bestsellers)}")
    if len(only_bestsellers) > 0 and len(only_bestsellers) <= 5:
        for prod_id in list(only_bestsellers)[:5]:
            prod = bestsellers_products[prod_id]
            print(f"   - {prod['title']}")

    # Afficher produits UNIQUEMENT dans Special Offers
    only_special = special_offers_ids - bestsellers_ids
    print(f"\n📦 Produits UNIQUEMENT dans Special Offers: {len(only_special)}")
    if len(only_special) > 0 and len(only_special) <= 5:
        for prod_id in list(only_special)[:5]:
            prod = special_offers_products[prod_id]
            print(f"   - {prod['title']}")

    # Sauvegarder résultats détaillés
    output = {
        'timestamp': '2025-10-15T04:15:00',
        'summary': {
            'bestsellers_count': len(bestsellers_ids),
            'special_offers_count': len(special_offers_ids),
            'overlap_count': len(overlap_ids),
            'only_bestsellers': len(only_bestsellers),
            'only_special_offers': len(only_special)
        },
        'overlap': overlap_list if len(overlap_ids) > 0 else [],
        'all_bestsellers': list(bestsellers_products.values()),
        'all_special_offers': list(special_offers_products.values())
    }

    with open('bestsellers_vs_specialoffers_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("✅ Résultats sauvegardés: bestsellers_vs_specialoffers_detailed.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
