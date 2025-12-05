#!/usr/bin/env python3
"""
ANALYSE FORENSIQUE COMPLÈTE DES PRODUITS SHOPIFY
Objectif: Identifier TOUS les doublons et violations de règles
"""

import os
import json
import requests
from typing import List, Dict, Set, Tuple
from collections import defaultdict
import time

# Configuration
import os
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN", "azffej-as.myshopify.com")
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")

if not SHOPIFY_ADMIN_ACCESS_TOKEN:
    raise ValueError("SHOPIFY_ADMIN_ACCESS_TOKEN not found in environment variables. Please set it in .env.admin")

GRAPHQL_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10/graphql.json"

headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN
}

def graphql_request(query: str) -> Dict:
    """Effectue une requête GraphQL avec gestion d'erreurs"""
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers)
    if response.status_code != 200:
        raise Exception(f"GraphQL Error: {response.status_code} - {response.text}")
    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL Errors: {data['errors']}")
    return data

def get_all_products() -> List[Dict]:
    """Récupère TOUS les produits avec pagination complète"""
    print("🔍 Récupération de TOUS les produits...")
    all_products = []
    has_next_page = True
    cursor = None
    page = 1

    while has_next_page:
        after_clause = f', after: "{cursor}"' if cursor else ''
        query = f'''
        {{
            products(first: 250{after_clause}) {{
                edges {{
                    node {{
                        id
                        title
                        handle
                        description
                        descriptionHtml
                        productType
                        vendor
                        tags
                        status
                        createdAt
                        updatedAt
                        priceRangeV2 {{
                            minVariantPrice {{
                                amount
                                currencyCode
                            }}
                            maxVariantPrice {{
                                amount
                                currencyCode
                            }}
                        }}
                        variants(first: 100) {{
                            edges {{
                                node {{
                                    id
                                    title
                                    price
                                    compareAtPrice
                                    sku
                                    inventoryQuantity
                                }}
                            }}
                        }}
                        collections(first: 20) {{
                            edges {{
                                node {{
                                    id
                                    title
                                    handle
                                }}
                            }}
                        }}
                        images(first: 10) {{
                            edges {{
                                node {{
                                    id
                                    url
                                    altText
                                }}
                            }}
                        }}
                    }}
                    cursor
                }}
                pageInfo {{
                    hasNextPage
                }}
            }}
        }}
        '''

        result = graphql_request(query)
        products_data = result['data']['products']

        for edge in products_data['edges']:
            all_products.append(edge['node'])
            cursor = edge['cursor']

        has_next_page = products_data['pageInfo']['hasNextPage']
        print(f"  Page {page}: {len(products_data['edges'])} produits récupérés (Total: {len(all_products)})")
        page += 1

        time.sleep(0.5)  # Rate limiting

    print(f"✅ Total: {len(all_products)} produits récupérés\n")
    return all_products

def get_all_collections() -> List[Dict]:
    """Récupère TOUTES les collections avec leurs produits"""
    print("🔍 Récupération de TOUTES les collections...")
    all_collections = []
    has_next_page = True
    cursor = None
    page = 1

    while has_next_page:
        after_clause = f', after: "{cursor}"' if cursor else ''
        query = f'''
        {{
            collections(first: 250{after_clause}) {{
                edges {{
                    node {{
                        id
                        title
                        handle
                        description
                        products(first: 250) {{
                            edges {{
                                node {{
                                    id
                                    title
                                    handle
                                }}
                            }}
                        }}
                    }}
                    cursor
                }}
                pageInfo {{
                    hasNextPage
                }}
            }}
        }}
        '''

        result = graphql_request(query)
        collections_data = result['data']['collections']

        for edge in collections_data['edges']:
            all_collections.append(edge['node'])
            cursor = edge['cursor']

        has_next_page = collections_data['pageInfo']['hasNextPage']
        print(f"  Page {page}: {len(collections_data['edges'])} collections récupérées (Total: {len(all_collections)})")
        page += 1

        time.sleep(0.5)

    print(f"✅ Total: {len(all_collections)} collections récupérées\n")
    return all_collections

def normalize_title(title: str) -> str:
    """Normalise un titre pour comparaison"""
    return title.lower().strip().replace("  ", " ").replace("-", " ")

def analyze_duplicates(products: List[Dict]) -> Dict:
    """Analyse COMPLÈTE des doublons"""
    print("🔍 ANALYSE DES DOUBLONS...")

    # Structures de données pour l'analyse
    exact_duplicates = defaultdict(list)  # titre exact -> produits
    similar_duplicates = defaultdict(list)  # titre normalisé -> produits
    handle_duplicates = defaultdict(list)  # handle -> produits
    sku_duplicates = defaultdict(list)  # SKU -> produits

    # Analyse produit par produit
    for product in products:
        title = product['title']
        normalized_title = normalize_title(title)
        handle = product['handle']

        # Doublons exacts
        exact_duplicates[title].append(product)

        # Doublons similaires
        similar_duplicates[normalized_title].append(product)

        # Doublons de handle
        handle_duplicates[handle].append(product)

        # Doublons de SKU
        for variant_edge in product['variants']['edges']:
            sku = variant_edge['node'].get('sku')
            if sku:
                sku_duplicates[sku].append({
                    'product': product,
                    'variant': variant_edge['node']
                })

    # Filtrer pour ne garder que les vraies duplications
    results = {
        'exact_title_duplicates': {k: v for k, v in exact_duplicates.items() if len(v) > 1},
        'similar_title_duplicates': {k: v for k, v in similar_duplicates.items() if len(v) > 1},
        'handle_duplicates': {k: v for k, v in handle_duplicates.items() if len(v) > 1},
        'sku_duplicates': {k: v for k, v in sku_duplicates.items() if len(v) > 1}
    }

    print(f"  ✓ Doublons titre exact: {len(results['exact_title_duplicates'])}")
    print(f"  ✓ Doublons titre similaire: {len(results['similar_title_duplicates'])}")
    print(f"  ✓ Doublons handle: {len(results['handle_duplicates'])}")
    print(f"  ✓ Doublons SKU: {len(results['sku_duplicates'])}\n")

    return results

def analyze_multi_collection_products(products: List[Dict]) -> Dict:
    """Identifie les produits présents dans plusieurs collections"""
    print("🔍 ANALYSE PRODUITS MULTI-COLLECTIONS...")

    multi_collection_products = []

    for product in products:
        collections = [edge['node'] for edge in product['collections']['edges']]
        if len(collections) > 1:
            multi_collection_products.append({
                'product': product,
                'collections': collections,
                'collection_count': len(collections)
            })

    print(f"  ✓ Produits dans plusieurs collections: {len(multi_collection_products)}\n")

    return {
        'multi_collection_products': multi_collection_products,
        'count': len(multi_collection_products)
    }

def create_price_matrix(products: List[Dict]) -> Dict:
    """Crée une matrice complète: produit -> prix -> collections"""
    print("🔍 CRÉATION MATRICE PRIX...")

    matrix = []

    for product in products:
        min_price = float(product['priceRangeV2']['minVariantPrice']['amount'])
        max_price = float(product['priceRangeV2']['maxVariantPrice']['amount'])
        collections = [edge['node']['title'] for edge in product['collections']['edges']]

        # Tous les prix des variantes
        variant_prices = []
        for variant_edge in product['variants']['edges']:
            variant = variant_edge['node']
            variant_prices.append({
                'variant_title': variant['title'],
                'price': float(variant['price']),
                'compare_at_price': float(variant['compareAtPrice']) if variant['compareAtPrice'] else None,
                'sku': variant['sku']
            })

        matrix.append({
            'product_id': product['id'],
            'product_title': product['title'],
            'handle': product['handle'],
            'min_price': min_price,
            'max_price': max_price,
            'price_range': max_price - min_price,
            'collections': collections,
            'collection_count': len(collections),
            'variant_prices': variant_prices,
            'variant_count': len(variant_prices)
        })

    # Trier par titre
    matrix.sort(key=lambda x: x['product_title'])

    print(f"  ✓ Matrice créée: {len(matrix)} produits\n")

    return matrix

def identify_cheapest_duplicates(duplicates: Dict, products: List[Dict]) -> List[Dict]:
    """Identifie le produit le moins cher parmi les doublons"""
    print("🔍 IDENTIFICATION PRODUITS LES MOINS CHERS...")

    recommendations = []

    # Analyser les doublons similaires (les plus pertinents)
    for normalized_title, duplicate_products in duplicates['similar_title_duplicates'].items():
        if len(duplicate_products) < 2:
            continue

        # Extraire les prix min de chaque produit
        products_with_prices = []
        for product in duplicate_products:
            min_price = float(product['priceRangeV2']['minVariantPrice']['amount'])
            products_with_prices.append({
                'product': product,
                'min_price': min_price
            })

        # Trier par prix croissant
        products_with_prices.sort(key=lambda x: x['min_price'])

        cheapest = products_with_prices[0]
        to_delete = products_with_prices[1:]

        recommendations.append({
            'normalized_title': normalized_title,
            'duplicate_count': len(duplicate_products),
            'keep': {
                'id': cheapest['product']['id'],
                'title': cheapest['product']['title'],
                'handle': cheapest['product']['handle'],
                'price': cheapest['min_price']
            },
            'delete': [
                {
                    'id': p['product']['id'],
                    'title': p['product']['title'],
                    'handle': p['product']['handle'],
                    'price': p['min_price'],
                    'price_difference': p['min_price'] - cheapest['min_price']
                }
                for p in to_delete
            ]
        })

    print(f"  ✓ {len(recommendations)} groupes de doublons identifiés\n")

    return recommendations

def main():
    print("="*80)
    print("ANALYSE FORENSIQUE SHOPIFY - ALPHA MEDICAL")
    print("="*80)
    print()

    # 1. Récupérer tous les produits
    products = get_all_products()

    # 2. Récupérer toutes les collections
    collections = get_all_collections()

    # 3. Analyser les doublons
    duplicates = analyze_duplicates(products)

    # 4. Analyser produits multi-collections
    multi_collections = analyze_multi_collection_products(products)

    # 5. Créer matrice de prix
    price_matrix = create_price_matrix(products)

    # 6. Identifier les produits à garder/supprimer
    cleanup_recommendations = identify_cheapest_duplicates(duplicates, products)

    # 7. Sauvegarder les données brutes
    print("💾 SAUVEGARDE DES DONNÉES...")

    data = {
        'metadata': {
            'total_products': len(products),
            'total_collections': len(collections),
            'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S')
        },
        'products': products,
        'collections': collections,
        'duplicates': {
            'exact_title_duplicates': {k: [{'id': p['id'], 'title': p['title'], 'handle': p['handle']} for p in v]
                                        for k, v in duplicates['exact_title_duplicates'].items()},
            'similar_title_duplicates': {k: [{'id': p['id'], 'title': p['title'], 'handle': p['handle']} for p in v]
                                          for k, v in duplicates['similar_title_duplicates'].items()},
            'handle_duplicates': duplicates['handle_duplicates'],
            'sku_duplicates_count': len(duplicates['sku_duplicates'])
        },
        'multi_collection_analysis': {
            'count': multi_collections['count'],
            'products': [
                {
                    'id': item['product']['id'],
                    'title': item['product']['title'],
                    'handle': item['product']['handle'],
                    'collections': [c['title'] for c in item['collections']],
                    'collection_count': item['collection_count']
                }
                for item in multi_collections['multi_collection_products']
            ]
        },
        'price_matrix': price_matrix,
        'cleanup_recommendations': cleanup_recommendations
    }

    with open('forensic_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Données sauvegardées: forensic_data.json")
    print()

    # 8. Statistiques finales
    print("="*80)
    print("STATISTIQUES FINALES")
    print("="*80)
    print(f"Total produits:                      {len(products)}")
    print(f"Total collections:                   {len(collections)}")
    print(f"Groupes de doublons (titre exact):   {len(duplicates['exact_title_duplicates'])}")
    print(f"Groupes de doublons (similaires):    {len(duplicates['similar_title_duplicates'])}")
    print(f"Produits multi-collections:          {multi_collections['count']}")
    print(f"Produits à supprimer (recommandés):  {sum(len(r['delete']) for r in cleanup_recommendations)}")
    print("="*80)

    return data

if __name__ == "__main__":
    data = main()
