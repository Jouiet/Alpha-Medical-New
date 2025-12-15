#!/usr/bin/env python3
"""
FORENSIC PRODUCT-COLLECTION AUDIT
Alpha Medical - Session 98 CONTINUED
Vérification EXHAUSTIVE produit par produit

Approche bottom-up factuelle:
1. Récupérer TOUS les produits (active + draft)
2. Récupérer TOUTES les collections
3. Pour CHAQUE produit, vérifier ses collections
4. Rapport détaillé avec ZERO suppositions
"""

import os
import requests
import json
from datetime import datetime

# Load credentials
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '../../.env.admin')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

load_env()

STORE = os.environ.get('SHOPIFY_STORE_DOMAIN', 'azffej-as.myshopify.com')
TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')
BASE_URL = f'https://{STORE}/admin/api/2025-01'
HEADERS = {'X-Shopify-Access-Token': TOKEN}

def api_get(endpoint):
    """Make API request with error handling"""
    url = f'{BASE_URL}/{endpoint}'
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code != 200:
        print(f"❌ API ERROR: {endpoint} - {resp.status_code}")
        return None
    return resp.json()

def get_all_products():
    """Get ALL products (active + draft) with pagination"""
    all_products = []
    url = f'{BASE_URL}/products.json?limit=250'

    while url:
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code != 200:
            print(f"❌ API ERROR: products - {resp.status_code}")
            break

        data = resp.json()
        products = data.get('products', [])
        all_products.extend(products)

        # Check for pagination
        link_header = resp.headers.get('Link', '')
        if 'rel="next"' in link_header:
            # Extract next URL
            for part in link_header.split(','):
                if 'rel="next"' in part:
                    url = part.split(';')[0].strip('<> ')
                    break
        else:
            url = None

    return all_products

def get_all_collections():
    """Get all custom and smart collections"""
    custom = api_get('custom_collections.json?limit=250')
    smart = api_get('smart_collections.json?limit=250')

    collections = []
    if custom:
        for c in custom.get('custom_collections', []):
            collections.append({
                'id': c['id'],
                'title': c['title'],
                'handle': c['handle'],
                'type': 'custom'
            })
    if smart:
        for c in smart.get('smart_collections', []):
            collections.append({
                'id': c['id'],
                'title': c['title'],
                'handle': c['handle'],
                'type': 'smart'
            })

    return collections

def get_products_in_collection(collection_id, collection_type):
    """Get all product IDs in a collection"""
    if collection_type == 'custom':
        # Use collects endpoint for custom collections
        data = api_get(f'collects.json?collection_id={collection_id}&limit=250')
        if data:
            return [c['product_id'] for c in data.get('collects', [])]
    else:
        # Use products endpoint for smart collections
        data = api_get(f'products.json?collection_id={collection_id}&limit=250')
        if data:
            return [p['id'] for p in data.get('products', [])]
    return []

def main():
    print("=" * 80)
    print("FORENSIC PRODUCT-COLLECTION AUDIT")
    print(f"Date: {datetime.now().isoformat()}")
    print("=" * 80)
    print()

    # PHASE 1: Get ALL products
    print("PHASE 1: RÉCUPÉRATION PRODUITS")
    print("-" * 40)
    all_products = get_all_products()

    active_products = [p for p in all_products if p['status'] == 'active']
    draft_products = [p for p in all_products if p['status'] == 'draft']
    archived_products = [p for p in all_products if p['status'] == 'archived']

    print(f"Total produits: {len(all_products)}")
    print(f"  - Active: {len(active_products)}")
    print(f"  - Draft: {len(draft_products)}")
    print(f"  - Archived: {len(archived_products)}")
    print()

    # PHASE 2: Get ALL collections
    print("PHASE 2: RÉCUPÉRATION COLLECTIONS")
    print("-" * 40)
    collections = get_all_collections()
    print(f"Total collections: {len(collections)}")
    for c in collections:
        print(f"  - [{c['type']}] {c['title']} (ID: {c['id']})")
    print()

    # PHASE 3: Map products to collections
    print("PHASE 3: MAPPING PRODUIT → COLLECTIONS")
    print("-" * 40)

    # Build collection → products map
    collection_products = {}
    for c in collections:
        product_ids = get_products_in_collection(c['id'], c['type'])
        collection_products[c['id']] = {
            'title': c['title'],
            'product_ids': set(product_ids),
            'count': len(product_ids)
        }
        print(f"  {c['title']}: {len(product_ids)} produits")
    print()

    # PHASE 4: Build product → collections map (REVERSE)
    print("PHASE 4: MAPPING INVERSE (PRODUIT → SES COLLECTIONS)")
    print("-" * 40)

    product_collections = {}
    for p in all_products:
        pid = p['id']
        product_collections[pid] = {
            'title': p['title'],
            'status': p['status'],
            'handle': p['handle'],
            'collections': []
        }

        for c in collections:
            if pid in collection_products[c['id']]['product_ids']:
                product_collections[pid]['collections'].append(c['title'])

    # PHASE 5: IDENTIFY ORPHANS (CRITICAL)
    print("PHASE 5: IDENTIFICATION ORPHELINS")
    print("-" * 40)

    orphan_active = []
    orphan_draft = []

    for pid, pdata in product_collections.items():
        if len(pdata['collections']) == 0:
            if pdata['status'] == 'active':
                orphan_active.append(pdata)
            elif pdata['status'] == 'draft':
                orphan_draft.append(pdata)

    print(f"Orphelins ACTIFS: {len(orphan_active)}")
    print(f"Orphelins DRAFT: {len(orphan_draft)}")
    print()

    # PHASE 6: DETAILED REPORT
    print("=" * 80)
    print("RAPPORT DÉTAILLÉ - PRODUITS ACTIFS")
    print("=" * 80)

    # Group by collection count
    products_0_coll = []
    products_1_coll = []
    products_2plus_coll = []

    for pid, pdata in product_collections.items():
        if pdata['status'] != 'active':
            continue

        num_colls = len(pdata['collections'])
        if num_colls == 0:
            products_0_coll.append(pdata)
        elif num_colls == 1:
            products_1_coll.append(pdata)
        else:
            products_2plus_coll.append(pdata)

    print(f"\n📊 DISTRIBUTION DES PRODUITS ACTIFS ({len(active_products)} total):")
    print(f"  🔴 0 collections (ORPHELINS): {len(products_0_coll)}")
    print(f"  🟡 1 collection: {len(products_1_coll)}")
    print(f"  🟢 2+ collections: {len(products_2plus_coll)}")

    # LIST ORPHANS IN DETAIL
    if products_0_coll:
        print("\n" + "=" * 80)
        print("🚨 ORPHELINS ACTIFS - DÉTAIL COMPLET")
        print("=" * 80)
        for i, p in enumerate(products_0_coll, 1):
            print(f"\n{i}. {p['title']}")
            print(f"   Handle: {p['handle']}")
            print(f"   Status: {p['status']}")
            print(f"   Collections: AUCUNE ❌")
    else:
        print("\n✅ AUCUN ORPHELIN ACTIF - Tous les produits sont dans au moins 1 collection")

    # LIST DRAFT ORPHANS
    if orphan_draft:
        print("\n" + "=" * 80)
        print("⚠️ ORPHELINS DRAFT (info seulement)")
        print("=" * 80)
        for i, p in enumerate(orphan_draft, 1):
            print(f"\n{i}. {p['title']}")
            print(f"   Handle: {p['handle']}")

    # PHASE 7: VERIFICATION SUMMARY
    print("\n" + "=" * 80)
    print("RÉSUMÉ VÉRIFICATION FACTUELLE")
    print("=" * 80)

    total_active = len(active_products)
    orphans_active = len(products_0_coll)
    coverage = ((total_active - orphans_active) / total_active * 100) if total_active > 0 else 0

    print(f"""
┌────────────────────────────────────────────────────────────────────────┐
│ AUDIT FORENSIQUE - RÉSULTAT                                            │
├────────────────────────────────────────────────────────────────────────┤
│ Produits ACTIFS total:          {total_active:>3}                                     │
│ Produits dans ≥1 collection:    {total_active - orphans_active:>3}                                     │
│ Produits ORPHELINS (0 coll):    {orphans_active:>3}                                     │
│ Couverture:                     {coverage:>6.2f}%                                 │
├────────────────────────────────────────────────────────────────────────┤
│ STATUS: {'✅ 100% COUVERTURE' if orphans_active == 0 else '❌ ORPHELINS DÉTECTÉS - ACTION REQUISE':48} │
└────────────────────────────────────────────────────────────────────────┘
""")

    # Return for programmatic use
    return {
        'total_products': len(all_products),
        'active_products': len(active_products),
        'draft_products': len(draft_products),
        'collections': len(collections),
        'orphans_active': orphans_active,
        'orphans_draft': len(orphan_draft),
        'coverage_percent': coverage,
        'orphan_list': products_0_coll
    }

if __name__ == '__main__':
    result = main()

    # Exit code for CI/CD
    if result['orphans_active'] > 0:
        exit(1)
    else:
        exit(0)
