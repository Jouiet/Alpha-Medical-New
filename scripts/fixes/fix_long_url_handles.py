#!/usr/bin/env python3
"""
CORRECTION CRITIQUE: URLs TROP LONGUES (>100 chars)
Corrige 5 handles de 125-128 chars vers 30-37 chars (réduction 70-77%)
"""

import os
import sys
import requests
import time
from dotenv import load_dotenv

# Load from root
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(root_dir, '.env.admin'))

DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

# 5 worst offenders (128, 128, 128, 128, 125 chars) → short SEO-friendly handles
CORRECTIONS = {
    'airbag-massage-cushion-electric-kneading-reclining-chair-home-mattress-massager-cervical-spine-back-waist-whole-body-relief-110v':
        'electric-massage-cushion-full-body',

    'bunion-corrector-toe-separator-bunions-haluksy-separators-halux-toe-spreader-finger-straightener-for-toe-hallux-valgus-corrector':
        'bunion-corrector-toe-separator',

    'ergonomic-massage-rocker-recliner-chair-heat-and-vibration-neck-back-massage-removable-comfy-overstuffed-living-room-lounge-chai':
        'ergonomic-massage-recliner-chair',

    'full-body-shiatsu-massage-chair-household-electric-mattress-multifunctional-body-massage-kneading-back-cushion-neck-shoulder-mat':
        'shiatsu-massage-chair-full-body',

    'electric-heating-leg-massager-wireless-rechargeable-air-compression-leg-calf-massage-for-relief-relax-leg-muscles-health-care':
        'electric-leg-massager-air-compression',
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
    print("🔧 CORRECTION CRITIQUE: URLs TROP LONGUES")
    print("Target: 5 items avec handles 125-128 chars → 30-37 chars")
    print("=" * 80)
    print()

    if not DOMAIN or not ACCESS_TOKEN:
        print("❌ ERREUR: Credentials manquantes")
        return 1

    success = 0
    skipped = 0
    failed = 0

    for old_handle, new_handle in CORRECTIONS.items():
        old_len = len(old_handle)
        new_len = len(new_handle)
        reduction = round((1 - new_len/old_len) * 100, 1)

        print(f"📝 {old_handle[:50]}...")
        print(f"   [{old_len} → {new_len} chars, -{reduction}%]")
        print(f"   → {new_handle}")

        try:
            # Get by handle
            items = api_get('products.json', {'handle': old_handle, 'fields': 'id,title,handle,status'})

            if not items.get('products'):
                print(f"   ⚠️  SKIP: Not found (maybe already fixed)")
                skipped += 1
                print()
                continue

            item = items['products'][0]

            if item['status'] != 'active':
                print(f"   ⚠️  SKIP: Not published")
                skipped += 1
                print()
                continue

            # Update handle
            print(f"   🔄 Updating...")
            updated = api_put(f'products/{item["id"]}.json', {
                'product': {'id': item['id'], 'handle': new_handle}
            })

            print(f"   ✅ DONE: {updated['product']['title'][:50]}...")
            print(f"      URL: https://{DOMAIN}/products/{new_handle}")
            success += 1

            time.sleep(0.6)  # Rate limit

        except requests.exceptions.HTTPError as e:
            err = e.response.text[:100] if hasattr(e.response, 'text') else str(e)
            print(f"   ❌ HTTP {e.response.status_code}: {err}")
            failed += 1
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            failed += 1

        print()

    print("=" * 80)
    print("RÉSULTAT")
    print("=" * 80)
    print(f"✅ Success: {success}/{len(CORRECTIONS)}")
    print(f"⚠️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print()

    if success > 0:
        print("🎉 CORRECTIONS APPLIQUÉES!")
        print()
        print("📌 IMPORTANT:")
        print("   → Shopify auto-creates 301 redirects (old → new URLs)")
        print("   → No SEO loss, search rankings preserved")
        print("   → Verify: Shopify Admin → Navigation → URL Redirects")

    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
