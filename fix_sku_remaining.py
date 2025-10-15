#!/usr/bin/env python3
"""
Script pour corriger les SKU restants (à partir de #234)
"""

import json
import time
import requests
from datetime import datetime
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

def extract_variant_rest_id(gid):
    return gid.split('/')[-1]

def update_variant_sku(correction, index, total):
    variant_id = extract_variant_rest_id(correction['variant_id'])
    new_sku = correction['new_sku']
    old_sku = correction['old_sku']
    product_title = correction['product_title']
    variant_title = correction.get('variant_title', 'Default')

    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/variants/{variant_id}.json"
    payload = {"variant": {"id": int(variant_id), "sku": new_sku}}

    try:
        print(f"[{index}/{total}] {product_title[:50]}... | {variant_title[:30]}...")
        print(f"           {old_sku} → {new_sku}")

        response = requests.put(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            print(f"           ✅ SUCCESS")
            return {"variant_id": correction['variant_id'], "status": "success"}
        else:
            print(f"           ❌ FAILED: {response.status_code}")
            return {"variant_id": correction['variant_id'], "status": "failed", "error": response.status_code}
    except Exception as e:
        print(f"           ❌ ERROR: {str(e)[:100]}")
        return {"variant_id": correction['variant_id'], "status": "error", "error": str(e)[:100]}

def main():
    START_INDEX = 233  # Start from correction #234 (0-indexed = 233)

    print("=" * 80)
    print(f"CORRECTION SKU RESTANTS - Starting from #{START_INDEX + 1}")
    print("=" * 80)

    with open('sku_correction_plan.json', 'r', encoding='utf-8') as f:
        plan = json.load(f)

    corrections = plan['corrections'][START_INDEX:]  # Skip already done
    total_remaining = len(corrections)
    total_original = len(plan['corrections'])

    print(f"Corrections restantes: {total_remaining}")
    print(f"Progression: {START_INDEX}/{total_original} déjà faites")
    print("Démarrage dans 2 secondes...\n")
    time.sleep(2)

    results = []
    success_count = 0
    failed_count = 0

    for i, correction in enumerate(corrections, START_INDEX + 1):
        result = update_variant_sku(correction, i, total_original)
        results.append(result)

        if result['status'] == 'success':
            success_count += 1
        else:
            failed_count += 1

        if i < total_original:
            time.sleep(0.6)

        if (i - START_INDEX) % 25 == 0 and i != START_INDEX + 1:
            print(f"\n--- PROGRESSION: {i}/{total_original} ({success_count} ✅, {failed_count} ❌) ---\n")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "start_index": START_INDEX + 1,
        "summary": {
            "total_processed": total_remaining,
            "successful": success_count,
            "failed": failed_count,
            "success_rate": f"{(success_count/total_remaining*100):.1f}%"
        },
        "results": results
    }

    with open('sku_corrections_remaining_results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print("RÉSUMÉ - CORRECTIONS RESTANTES")
    print("=" * 80)
    print(f"Traités: {total_remaining}")
    print(f"✅ Succès: {success_count} ({success_count/total_remaining*100:.1f}%)")
    print(f"❌ Échecs: {failed_count}")
    print(f"\nTOTAL GLOBAL: {START_INDEX + success_count}/{total_original} corrections réussies")
    print("=" * 80)

if __name__ == "__main__":
    main()
