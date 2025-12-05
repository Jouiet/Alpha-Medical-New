#!/usr/bin/env python3
"""
CORRECTION PHASE 2: 7 HANDLES RESTANTS >100 CHARS
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

# 7 remaining handles >100 chars → short SEO-friendly versions
CORRECTIONS_PHASE_2 = {
    # 123 chars → 38 chars (-69%)
    'electric-vibration-massager-bunion-corrector-unisex-foot-hallux-valgus-braces-adjustable-toe-separator-finger-toe-corrector':
        'electric-bunion-corrector-toe-separator',

    # 122 chars → 33 chars (-73%)
    'smart-electric-vacuum-cupping-device-body-scraping-massager-heating-suction-cup-device-physical-fatigue-relief-health-care':
        'electric-vacuum-cupping-massager',

    # 120 chars → 35 chars (-71%)
    'effective-bunion-corrector-airbag-traction-foot-hallux-valgus-braces-toe-separator-straightener-orthotics-toe-correction':
        'airbag-bunion-corrector-orthotic',

    # 120 chars → 36 chars (-70%)
    'adjustable-hunchback-orthotic-brace-back-waist-posture-corrector-back-support-corset-shoulder-spine-brace-neck-stretcher':
        'posture-corrector-back-support-brace',

    # 109 chars → 34 chars (-69%)
    'electric-medical-cupping-therapy-set-beauty-massager-glass-jars-anti-cellulite-cupping-vacuum-slimming-guasha':
        'medical-cupping-therapy-set-glass',
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
    print("🔧 CORRECTION PHASE 2: 7 HANDLES RESTANTS >100 CHARS")
    print("=" * 80)
    print()

    if not DOMAIN or not ACCESS_TOKEN:
        print("❌ ERREUR: Credentials manquantes")
        return 1

    success = 0
    skipped = 0
    failed = 0

    for old_handle, new_handle in CORRECTIONS_PHASE_2.items():
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
    print("RÉSULTAT PHASE 2")
    print("=" * 80)
    print(f"✅ Success: {success}/{len(CORRECTIONS_PHASE_2)}")
    print(f"⚠️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print()

    if success > 0:
        print("🎉 PHASE 2 TERMINÉE!")
        print()
        print("📊 TOTAL CORRECTIONS:")
        print("   Phase 1: 5 handles (125-128 chars) → 30-37 chars")
        print(f"   Phase 2: {success} handles (109-123 chars) → 33-38 chars")
        print(f"   TOTAL: {5 + success} handles corrigés")

    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
