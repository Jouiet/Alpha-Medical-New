#!/usr/bin/env python3
"""
Vérification LIVE de l'overlap entre Bestsellers et Special Offers
Données FRAÎCHES directement de l'API Shopify (pas de cache)
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
    """Récupère tous les produits d'une collection spécifique - FRESH DATA"""
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

    print(f"❌ ERROR fetching {collection_handle}: {response.status_code}")
    print(response.text[:500])
    return None

def main():
    print("=" * 80)
    print("VÉRIFICATION LIVE: BESTSELLERS vs SPECIAL OFFERS")
    print("=" * 80)
    print("Source: API Shopify GraphQL (données fraîches)")
    print("=" * 80)

    # Fetch Bestsellers
    print("\n🔄 Récupération Bestsellers...")
    bestsellers = fetch_collection_products('bestsellers')

    if not bestsellers:
        print("❌ Impossible de récupérer Bestsellers")
        return

    bestsellers_products = {}
    for edge in bestsellers['products']['edges']:
        prod = edge['node']
        bestsellers_products[prod['id']] = {
            'title': prod['title'],
            'handle': prod['handle']
        }

    print(f"✅ Bestsellers: {len(bestsellers_products)} produits")

    # Fetch Special Offers
    print("\n🔄 Récupération Special Offers...")
    special_offers = fetch_collection_products('special-offers')

    if not special_offers:
        print("❌ Impossible de récupérer Special Offers")
        return

    special_offers_products = {}
    for edge in special_offers['products']['edges']:
        prod = edge['node']
        special_offers_products[prod['id']] = {
            'title': prod['title'],
            'handle': prod['handle']
        }

    print(f"✅ Special Offers: {len(special_offers_products)} produits")

    # Vérifier overlap
    print("\n" + "=" * 80)
    print("ANALYSE OVERLAP")
    print("=" * 80)

    bestsellers_ids = set(bestsellers_products.keys())
    special_offers_ids = set(special_offers_products.keys())

    overlap_ids = bestsellers_ids.intersection(special_offers_ids)

    print(f"\n📊 RÉSULTATS:")
    print(f"   Bestsellers: {len(bestsellers_ids)} produits")
    print(f"   Special Offers: {len(special_offers_ids)} produits")
    print(f"   Overlap: {len(overlap_ids)} produits")

    if len(overlap_ids) == 0:
        print("\n✅ AUCUN OVERLAP DÉTECTÉ")
        print("Les collections Bestsellers et Special Offers sont 100% séparées")
    else:
        print(f"\n❌ OVERLAP DÉTECTÉ: {len(overlap_ids)} produits présents dans les DEUX collections")
        print("\nProduits en double:")

        overlap_details = []
        for prod_id in sorted(overlap_ids, key=lambda x: bestsellers_products[x]['title']):
            prod_info = bestsellers_products[prod_id]
            print(f"\n   🔴 {prod_info['title']}")
            print(f"      ID: {prod_id}")
            print(f"      Handle: {prod_info['handle']}")
            print(f"      URL: https://alphamedical.shop/products/{prod_info['handle']}")

            overlap_details.append({
                'product_id': prod_id,
                'product_title': prod_info['title'],
                'product_handle': prod_info['handle'],
                'url': f"https://alphamedical.shop/products/{prod_info['handle']}"
            })

    # Vérifier les 2 produits mentionnés par l'utilisateur
    print("\n" + "=" * 80)
    print("VÉRIFICATION DES PRODUITS MENTIONNÉS PAR L'UTILISATEUR")
    print("=" * 80)

    user_handles = [
        'led-face-neck-mask-red-light-infrared-therapy',
        'hello-face-red-light-therapy-mask-face-neck-infrared-led'
    ]

    for handle in user_handles:
        in_bestsellers = any(p['handle'] == handle for p in bestsellers_products.values())
        in_special_offers = any(p['handle'] == handle for p in special_offers_products.values())

        print(f"\n📦 Produit: {handle}")
        print(f"   Dans Bestsellers: {'✅ OUI' if in_bestsellers else '❌ NON'}")
        print(f"   Dans Special Offers: {'✅ OUI' if in_special_offers else '❌ NON'}")

        if in_bestsellers and in_special_offers:
            print(f"   🔴 DOUBLON CONFIRMÉ!")
        elif in_bestsellers or in_special_offers:
            print(f"   ✅ Pas de doublon (seulement dans 1 collection)")
        else:
            print(f"   ⚠️ Produit introuvable dans les deux collections")

    # Sauvegarder les résultats
    output = {
        'timestamp': '2025-10-15T04:00:00',
        'source': 'FRESH_API_DATA',
        'summary': {
            'bestsellers_count': len(bestsellers_ids),
            'special_offers_count': len(special_offers_ids),
            'overlap_count': len(overlap_ids),
            'overlap_percentage': f"{len(overlap_ids)/max(len(bestsellers_ids), 1)*100:.1f}%"
        },
        'overlap_products': overlap_details if len(overlap_ids) > 0 else []
    }

    with open('bestsellers_special_offers_overlap_LIVE.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"✅ Résultats sauvegardés: bestsellers_special_offers_overlap_LIVE.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
