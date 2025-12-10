#!/usr/bin/env python3
"""
Script de vérification de l'état des 149 produits sur Shopify
Vérifie que tous les produits sont bien optimisés
"""

import requests
import json
from pathlib import Path

# Load token from .env.admin file
env_file = Path(__file__).parent / '.env.admin'
ACCESS_TOKEN = None

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                ACCESS_TOKEN = line.split('=', 1)[1].strip()
                break

if not ACCESS_TOKEN:
    print("❌ ERROR: SHOPIFY_ADMIN_ACCESS_TOKEN not found in .env.admin")
    exit(1)

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
BASE_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def get_all_products():
    """Récupère tous les produits du store"""
    all_products = []
    url = f"{BASE_URL}/products.json?limit=250"

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Erreur: {response.status_code}")
            print(response.text)
            break

        data = response.json()
        all_products.extend(data.get("products", []))

        # Pagination via Link header
        link_header = response.headers.get('Link', '')
        url = None
        if 'rel="next"' in link_header:
            # Extract next URL from Link header
            for link in link_header.split(','):
                if 'rel="next"' in link:
                    url = link.split(';')[0].strip('<> ')
                    break

    return all_products

def verify_product_optimization(product):
    """Vérifie si un produit est optimisé"""
    title = product.get('title', '')
    tags = product.get('tags', '')
    body_html = product.get('body_html', '')

    # Critères d'optimisation
    title_short = len(title) <= 70
    has_tags = len(tags) > 20  # Au moins quelques tags
    has_description = len(body_html) > 200  # Description substantielle

    is_optimized = title_short and has_tags and has_description

    return {
        'id': product['id'],
        'title': title,
        'title_length': len(title),
        'tags_count': len(tags.split(',')) if tags else 0,
        'description_length': len(body_html),
        'is_optimized': is_optimized,
        'title_short': title_short,
        'has_tags': has_tags,
        'has_description': has_description
    }

def main():
    print("=" * 70)
    print("🔍 VÉRIFICATION ÉTAT DES PRODUITS - ALPHA MEDICAL CARE")
    print("=" * 70)
    print()

    # Récupérer tous les produits
    print("📥 Récupération des produits depuis Shopify...")
    products = get_all_products()
    print(f"✅ {len(products)} produits trouvés\n")

    if not products:
        print("❌ Aucun produit trouvé.")
        return

    # Vérifier l'optimisation de chaque produit
    print("🔍 Analyse de l'optimisation...")
    print()

    optimized = []
    not_optimized = []

    for product in products:
        result = verify_product_optimization(product)
        if result['is_optimized']:
            optimized.append(result)
        else:
            not_optimized.append(result)

    # Statistiques
    print("=" * 70)
    print("📊 STATISTIQUES D'OPTIMISATION")
    print("=" * 70)
    print()
    print(f"✅ Produits optimisés: {len(optimized)}/{len(products)} ({len(optimized)*100//len(products)}%)")
    print(f"❌ Produits non-optimisés: {len(not_optimized)}/{len(products)} ({len(not_optimized)*100//len(products)}%)")
    print()

    # Statistiques détaillées
    total_title_length = sum(p['title_length'] for p in optimized)
    avg_title_length = total_title_length // len(optimized) if optimized else 0

    total_tags = sum(p['tags_count'] for p in optimized)
    avg_tags = total_tags // len(optimized) if optimized else 0

    print(f"📏 Longueur moyenne des titles optimisés: {avg_title_length} caractères")
    print(f"🏷️  Nombre moyen de tags: {avg_tags} tags/produit")
    print()

    # Produits non-optimisés (si présents)
    if not_optimized:
        print("=" * 70)
        print("⚠️  PRODUITS NÉCESSITANT OPTIMISATION")
        print("=" * 70)
        print()

        for i, prod in enumerate(not_optimized[:10], 1):  # Afficher max 10
            print(f"{i}. ID {prod['id']}: {prod['title'][:50]}...")
            issues = []
            if not prod['title_short']:
                issues.append(f"Title trop long ({prod['title_length']} chars)")
            if not prod['has_tags']:
                issues.append(f"Tags insuffisants ({prod['tags_count']} tags)")
            if not prod['has_description']:
                issues.append(f"Description courte ({prod['description_length']} chars)")
            print(f"   Issues: {', '.join(issues)}")
            print()

        if len(not_optimized) > 10:
            print(f"... et {len(not_optimized) - 10} autres produits\n")

    # Conclusion
    print("=" * 70)
    print("✅ VÉRIFICATION TERMINÉE")
    print("=" * 70)
    print()

    if len(optimized) == len(products):
        print("🎉 TOUS LES PRODUITS SONT OPTIMISÉS! 100% COMPLET!")
    elif len(optimized) >= len(products) * 0.95:
        print("✅ QUASI-COMPLET! Plus de 95% des produits optimisés.")
    else:
        print(f"⚠️  Optimisation à {len(optimized)*100//len(products)}% - Travail restant requis.")

    print()

if __name__ == "__main__":
    main()
