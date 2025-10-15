#!/usr/bin/env python3
"""
Vérification des 20 produits de Special Offers avant suppression
S'assurer que tous ont une collection principale
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

MAIN_COLLECTIONS = {
    'pain-relief-recovery',
    'therapy-wellness',
    'posture-support'
}

def fetch_special_offers_products():
    """Récupère tous les produits de Special Offers avec leurs collections"""
    query = """
    {
      collectionByHandle(handle: "special-offers") {
        id
        title
        handle
        products(first: 250) {
          edges {
            node {
              id
              title
              handle
              collections(first: 10) {
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
    print("VÉRIFICATION PRODUITS SPECIAL OFFERS AVANT SUPPRESSION")
    print("=" * 80)

    data = fetch_special_offers_products()

    if not data or 'data' not in data:
        print("❌ Erreur lors de la récupération")
        return

    special_offers = data['data']['collectionByHandle']

    if not special_offers:
        print("❌ Collection Special Offers introuvable")
        return

    collection_id = special_offers['id']
    products = special_offers['products']['edges']

    print(f"\nCollection ID: {collection_id}")
    print(f"Total produits: {len(products)}\n")

    # Analyser chaque produit
    safe_to_delete = True
    products_analysis = []

    for prod_edge in products:
        prod = prod_edge['node']
        prod_id = prod['id']
        prod_title = prod['title']
        prod_handle = prod['handle']

        # Récupérer toutes les collections du produit
        prod_collections = []
        main_collections_count = 0

        for coll_edge in prod['collections']['edges']:
            coll = coll_edge['node']
            coll_handle = coll['handle']
            prod_collections.append({
                'id': coll['id'],
                'title': coll['title'],
                'handle': coll_handle
            })

            if coll_handle in MAIN_COLLECTIONS:
                main_collections_count += 1

        # Vérifier si le produit a au moins 1 collection principale
        has_main_collection = main_collections_count > 0

        if not has_main_collection:
            safe_to_delete = False

        products_analysis.append({
            'product_id': prod_id,
            'product_title': prod_title,
            'product_handle': prod_handle,
            'total_collections': len(prod_collections),
            'main_collections_count': main_collections_count,
            'has_main_collection': has_main_collection,
            'collections': prod_collections
        })

        # Afficher
        status_icon = "✅" if has_main_collection else "❌"
        print(f"{status_icon} {prod_title}")
        print(f"   Handle: {prod_handle}")
        print(f"   Collections: {len(prod_collections)} total, {main_collections_count} principales")

        if not has_main_collection:
            print(f"   ⚠️ DANGER: Aucune collection principale!")

        for coll in prod_collections:
            is_main = "🟢 PRINCIPALE" if coll['handle'] in MAIN_COLLECTIONS else "🔵 promotionnelle"
            print(f"      - {coll['title']} ({coll['handle']}) {is_main}")
        print()

    # Résumé
    print("=" * 80)
    print("RÉSUMÉ SÉCURITÉ")
    print("=" * 80)

    products_with_main = [p for p in products_analysis if p['has_main_collection']]
    products_without_main = [p for p in products_analysis if not p['has_main_collection']]

    print(f"\n✅ Produits avec collection principale: {len(products_with_main)}/{len(products)}")
    print(f"❌ Produits SANS collection principale: {len(products_without_main)}/{len(products)}")

    if safe_to_delete:
        print("\n✅ SÉCURISÉ: Tous les produits ont une collection principale")
        print("✅ La suppression de Special Offers est SAFE")
    else:
        print("\n❌ DANGER: Certains produits n'ont QUE Special Offers")
        print("❌ La suppression de Special Offers causera des produits ORPHELINS")
        print("\nProduits à risque:")
        for p in products_without_main:
            print(f"   - {p['product_title']}")

    # Sauvegarder
    output = {
        'timestamp': '2025-10-15T04:30:00',
        'collection_id': collection_id,
        'collection_handle': 'special-offers',
        'total_products': len(products),
        'products_with_main_collection': len(products_with_main),
        'products_without_main_collection': len(products_without_main),
        'safe_to_delete': safe_to_delete,
        'products': products_analysis
    }

    with open('special_offers_deletion_check.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Résultats sauvegardés: special_offers_deletion_check.json")
    print("=" * 80)

    # Retourner le statut
    return safe_to_delete, collection_id

if __name__ == "__main__":
    safe, coll_id = main()
    if safe:
        print(f"\n🟢 AUTORISATION SUPPRESSION: Collection {coll_id}")
    else:
        print(f"\n🔴 INTERDICTION SUPPRESSION: Produits orphelins détectés")
