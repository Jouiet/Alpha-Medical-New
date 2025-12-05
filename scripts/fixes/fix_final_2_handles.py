#!/usr/bin/env python3
"""
CORRECTION PHASE 3 FINALE: 2 DERNIERS HANDLES >100 CHARS
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(root_dir, '.env.admin'))

DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

# 2 final handles >100 chars
CORRECTIONS_PHASE_3 = {
    # 109 chars → 38 chars (-65%)
    'professional-full-body-shiatsu-massage-chair-automatic-household-kneading-neck-shoulder-back-cushion-recliner':
        'professional-shiatsu-massage-recliner',

    # 104 chars → 34 chars (-67%)
    'adjustable-cervical-collar-spine-thoracic-orthosis-head-chest-neck-fixed-brace-posture-corrector-support':
        'cervical-collar-posture-corrector',
}

def api_get(endpoint, params=None):
    """Shopify API GET"""
    url = f'https://{DOMAIN}/admin/api/{API_VERSION}/{endpoint}'
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    r = requests.get(url, headers=headers, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def api_put(endpoint, data):
    """Shopify API PUT"""
    url = f'https://{DOMAIN}/admin/api/{API_VERSION}/{endpoint}'
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN, 'Content-Type': 'application/json'}
    r = requests.put(url, headers=headers, json=data, timeout=30)
    r.raise_for_status()
    return r.json()

def main():
    print("=" * 80)
    print("🔧 CORRECTION PHASE 3 FINALE: 2 DERNIERS HANDLES >100 CHARS")
    print("=" * 80)
    print()

    if not DOMAIN or not ACCESS_TOKEN:
        print("❌ ERREUR: Credentials manquantes")
        return 1

    success = 0
    skipped = 0
    failed = 0

    for old_handle, new_handle in CORRECTIONS_PHASE_3.items():
        old_len = len(old_handle)
        new_len = len(new_handle)
        reduction = round((1 - new_len/old_len) * 100, 1)

        print(f"📝 {old_handle[:60]}...")
        print(f"   [{old_len} → {new_len} chars, -{reduction}%]")
        print(f"   → {new_handle}")

        try:
            items = api_get('products.json', {'handle': old_handle, 'fields': 'id,title,handle,status'})

            if not items.get('products'):
                print(f"   ⚠️  SKIP: Not found")
                skipped += 1
                print()
                continue

            item = items['products'][0]

            if item['status'] != 'active':
                print(f"   ⚠️  SKIP: Not published")
                skipped += 1
                print()
                continue

            print(f"   🔄 Updating...")
            updated = api_put(f'products/{item["id"]}.json', {
                'product': {'id': item['id'], 'handle': new_handle}
            })

            print(f"   ✅ DONE: {updated['product']['title'][:50]}...")
            print(f"      URL: https://{DOMAIN}/products/{new_handle}")
            success += 1

            time.sleep(0.6)

        except requests.exceptions.HTTPError as e:
            err = e.response.text[:100] if hasattr(e.response, 'text') else str(e)
            print(f"   ❌ HTTP {e.response.status_code}: {err}")
            failed += 1
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            failed += 1

        print()

    print("=" * 80)
    print("RÉSULTAT PHASE 3 FINALE")
    print("=" * 80)
    print(f"✅ Success: {success}/{len(CORRECTIONS_PHASE_3)}")
    print(f"⚠️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print()

    if success == len(CORRECTIONS_PHASE_3) and failed == 0:
        print("🎉 100% COMPLET!")
        print()
        print("📊 CORRECTIONS TOTALES:")
        print("   Phase 1: 5 handles (125-128 chars)")
        print("   Phase 2: 5 handles (109-123 chars)")
        print(f"   Phase 3: {success} handles (104-109 chars)")
        print(f"   TOTAL: {5 + 5 + success} handles = 100% problèmes critiques résolus")

    return 0 if (success == len(CORRECTIONS_PHASE_3) and failed == 0) else 1

if __name__ == '__main__':
    sys.exit(main())
