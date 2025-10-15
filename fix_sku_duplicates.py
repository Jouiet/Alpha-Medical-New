#!/usr/bin/env python3
"""
Script pour corriger les 328 SKU dupliqués via Shopify REST API
Utilise le plan de correction généré dans sku_correction_plan.json
"""

import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-10')

# Headers pour les requêtes REST API
headers = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def extract_variant_rest_id(gid):
    """Extrait l'ID numérique du GID Shopify"""
    return gid.split('/')[-1]

def update_variant_sku(correction, index, total):
    """Met à jour le SKU d'une variante via REST API"""
    variant_id = extract_variant_rest_id(correction['variant_id'])
    new_sku = correction['new_sku']
    old_sku = correction['old_sku']
    product_title = correction['product_title']
    variant_title = correction.get('variant_title', 'Default')

    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/variants/{variant_id}.json"

    payload = {
        "variant": {
            "id": int(variant_id),
            "sku": new_sku
        }
    }

    try:
        print(f"[{index}/{total}] Updating: {product_title} | {variant_title}")
        print(f"           Old SKU: {old_sku} → New SKU: {new_sku}")

        response = requests.put(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            print(f"           ✅ SUCCESS")
            return {
                "variant_id": correction['variant_id'],
                "product_title": product_title,
                "variant_title": variant_title,
                "old_sku": old_sku,
                "new_sku": new_sku,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
        else:
            print(f"           ❌ FAILED: {response.status_code} - {response.text[:200]}")
            return {
                "variant_id": correction['variant_id'],
                "product_title": product_title,
                "variant_title": variant_title,
                "old_sku": old_sku,
                "new_sku": new_sku,
                "status": "failed",
                "error": f"{response.status_code}: {response.text[:200]}",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        print(f"           ❌ ERROR: {str(e)}")
        return {
            "variant_id": correction['variant_id'],
            "product_title": product_title,
            "variant_title": variant_title,
            "old_sku": old_sku,
            "new_sku": new_sku,
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def main():
    print("=" * 80)
    print("CORRECTION DES SKU DUPLIQUÉS - SHOPIFY REST API")
    print("=" * 80)
    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print(f"API Version: {API_VERSION}")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)

    # Charger le plan de correction
    with open('sku_correction_plan.json', 'r', encoding='utf-8') as f:
        plan = json.load(f)

    corrections = plan['corrections']
    total = len(corrections)

    print(f"\nTotal corrections à effectuer: {total}")
    print(f"Produits affectés: {plan['summary']['affected_products']}")
    print(f"Duplicats originaux: {plan['summary']['original_duplicates']}")
    print("\nDémarrage dans 3 secondes...")
    time.sleep(3)
    print("\n" + "=" * 80)

    results = []
    success_count = 0
    failed_count = 0

    # Traiter chaque correction
    for i, correction in enumerate(corrections, 1):
        result = update_variant_sku(correction, i, total)
        results.append(result)

        if result['status'] == 'success':
            success_count += 1
        else:
            failed_count += 1

        # Rate limiting: 2 requêtes/seconde max
        if i < total:
            time.sleep(0.6)

        # Afficher progression tous les 50
        if i % 50 == 0:
            print(f"\n--- PROGRESSION: {i}/{total} ({success_count} succès, {failed_count} échecs) ---\n")

    # Sauvegarder les résultats
    output = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_corrections": total,
            "successful": success_count,
            "failed": failed_count,
            "success_rate": f"{(success_count/total*100):.1f}%"
        },
        "results": results
    }

    with open('sku_corrections_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("RÉSUMÉ FINAL")
    print("=" * 80)
    print(f"Total corrections: {total}")
    print(f"✅ Succès: {success_count} ({success_count/total*100:.1f}%)")
    print(f"❌ Échecs: {failed_count} ({failed_count/total*100:.1f}%)")
    print(f"\nRésultats sauvegardés dans: sku_corrections_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
