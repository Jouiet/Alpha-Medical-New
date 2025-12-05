#!/usr/bin/env python3
"""
Vérification POST-SUPPRESSION Special Offers
S'assurer que les 20 produits sont toujours dans leurs collections principales
"""

import json
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2025-10')

headers = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

MAIN_COLLECTIONS = {
    'pain-relief-recovery',
    'therapy-wellness',
    'posture-support'
}

# Liste des 20 produits qui étaient dans Special Offers
PRODUCTS_TO_CHECK = [
    'spring-knee-booster-elderly-climbing-power-support',
    'back-support-brace-adjustable-posture-corrector',
    'ems-body-sculptor-wireless-butt-trainer-29-levels',
    'ems-abdominal-belt-usb-rechargeable-muscle-toner',
    'electric-hip-trainer-39-gears-buttock-massage-machine',
    'automatic-abdominal-massager-electric-belly-flattening-device',
    'smart-facial-massager-v-line-face-lifting-device',
    '7-color-led-silicone-face-mask-home-beauty-device',
    'foreverlily-7-color-led-mask-face-neck-skin-rejuvenation',
    '7-color-led-vibrating-neck-face-massager',
    'electric-lumbar-massager-heated-vibration-back-brace',
    'electric-neck-massager-shoulder-vibration-cervical',
    'electric-leg-massager-air-compression-heat-therapy',
    'knee-stabilizer-brace-aluminum-alloy-support',
    'orthopedic-knee-brace-adjustable-open-patella-support',
    '5-in-1-smart-cupping-therapy-set-12-level-control',
    'rom-elbow-brace-post-surgery-adjustable-stabilizer',
    'shoulder-posture-corrector-back-support-brace',
    'back-brace-posture-corrector-scoliosis-hunchback-support',
    'full-leg-compression-sleeve-unisex-knee-support'
]

def fetch_product_by_handle(handle):
    """Récupère un produit et ses collections par handle"""
    query = """
    {
      productByHandle(handle: "%s") {
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
    """ % handle

    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
    response = requests.post(url, headers=headers, json={'query': query})

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']['productByHandle']:
            return data['data']['productByHandle']
    return None

def main():
    print("=" * 80)
    print("VÉRIFICATION POST-SUPPRESSION SPECIAL OFFERS")
    print("=" * 80)
    print(f"\nVérification de {len(PRODUCTS_TO_CHECK)} produits...\n")

    verification_results = []
    all_safe = True

    for i, handle in enumerate(PRODUCTS_TO_CHECK, 1):
        print(f"[{i}/{len(PRODUCTS_TO_CHECK)}] Vérification: {handle}")

        product = fetch_product_by_handle(handle)

        if not product:
            print(f"   ❌ ERREUR: Produit introuvable!")
            all_safe = False
            verification_results.append({
                'handle': handle,
                'status': 'NOT_FOUND',
                'collections': [],
                'has_main_collection': False
            })
            continue

        # Analyser les collections
        collections = []
        main_collections_count = 0

        for coll_edge in product['collections']['edges']:
            coll = coll_edge['node']
            collections.append({
                'id': coll['id'],
                'title': coll['title'],
                'handle': coll['handle']
            })

            if coll['handle'] in MAIN_COLLECTIONS:
                main_collections_count += 1

        has_main = main_collections_count > 0

        if not has_main:
            all_safe = False
            print(f"   ❌ ORPHELIN: Aucune collection principale!")
        else:
            print(f"   ✅ OK: {main_collections_count} collection(s) principale(s)")

        # Vérifier si Special Offers est encore présente
        has_special_offers = any(c['handle'] == 'special-offers' for c in collections)

        if has_special_offers:
            print(f"   ⚠️ ANOMALIE: Special Offers toujours présente!")
            all_safe = False

        verification_results.append({
            'product_id': product['id'],
            'product_title': product['title'],
            'handle': handle,
            'status': 'OK' if has_main and not has_special_offers else 'ERROR',
            'has_main_collection': has_main,
            'has_special_offers': has_special_offers,
            'total_collections': len(collections),
            'main_collections_count': main_collections_count,
            'collections': collections
        })

    # Résumé
    print("\n" + "=" * 80)
    print("RÉSUMÉ VÉRIFICATION")
    print("=" * 80)

    products_ok = [p for p in verification_results if p['status'] == 'OK']
    products_error = [p for p in verification_results if p['status'] != 'OK']

    print(f"\n✅ Produits OK: {len(products_ok)}/{len(PRODUCTS_TO_CHECK)}")
    print(f"❌ Produits en ERREUR: {len(products_error)}/{len(PRODUCTS_TO_CHECK)}")

    if all_safe:
        print("\n✅ VÉRIFICATION RÉUSSIE")
        print("✅ Tous les produits sont dans leurs collections principales")
        print("✅ Special Offers a été correctement supprimée")
    else:
        print("\n❌ VÉRIFICATION ÉCHOUÉE")
        print("❌ Des problèmes ont été détectés")

        if products_error:
            print("\nProduits en erreur:")
            for p in products_error:
                print(f"   - {p.get('product_title', p['handle'])}")
                if not p['has_main_collection']:
                    print(f"      Raison: Aucune collection principale")
                if p.get('has_special_offers'):
                    print(f"      Raison: Special Offers toujours présente")

    # Sauvegarder
    output = {
        'timestamp': '2025-10-15T04:40:00',
        'total_products_checked': len(PRODUCTS_TO_CHECK),
        'products_ok': len(products_ok),
        'products_error': len(products_error),
        'all_safe': all_safe,
        'verification_results': verification_results
    }

    with open('post_deletion_verification.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Résultats sauvegardés: post_deletion_verification.json")
    print("=" * 80)

    return all_safe

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🟢 SUPPRESSION VALIDÉE - AUCUN PRODUIT ORPHELIN")
    else:
        print("\n🔴 PROBLÈMES DÉTECTÉS - VÉRIFICATION REQUISE")
