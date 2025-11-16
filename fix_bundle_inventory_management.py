#!/usr/bin/env python3
"""
FIX BUNDLE INVENTORY MANAGEMENT - Set inventory tracking to Shopify

PROBLÈME: 15/15 bundles have inventory_management = null
SOLUTION: Set inventory_management = "shopify" for all bundle variants

EXIGENCES:
- Un script pour UN problème (inventory management uniquement)
- Vérification FACTUELLE après exécution
- 100% success required (15/15 bundles)
- Pas de suppositions, seulement des faits

Author: Claude Code
Date: 2025-11-16
"""

import requests
import json

def load_env():
    """Load credentials from .env.admin"""
    env_vars = {}
    with open('.env.admin', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def get_all_bundles(store, token):
    """Fetch all bundles"""
    headers = {
        'X-Shopify-Access-Token': token,
        'Content-Type': 'application/json'
    }

    url = f"https://{store}/admin/api/2024-10/products.json?product_type=Medical Equipment Bundle&limit=250"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch bundles: {response.status_code}")
        return []

    products = response.json()['products']
    bundles = [p for p in products if 'bundle' in p.get('tags', '').lower()]

    return bundles

def update_variant_inventory(store, token, variant_id, inventory_management):
    """Update variant inventory management"""
    headers = {
        'X-Shopify-Access-Token': token,
        'Content-Type': 'application/json'
    }

    url = f"https://{store}/admin/api/2024-10/variants/{variant_id}.json"

    payload = {
        "variant": {
            "id": variant_id,
            "inventory_management": inventory_management
        }
    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        return True
    else:
        print(f"   ❌ Update failed: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return False

def fix_inventory_management():
    """Main function to fix inventory management for all bundles"""

    print("🔧 FIX BUNDLE INVENTORY MANAGEMENT - Starting...\n")
    print("="*100)

    # Load credentials
    env = load_env()
    store = env.get('SHOPIFY_STORE_DOMAIN')
    token = env.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

    if not store or not token:
        print("❌ ERROR: Missing credentials")
        return 1

    # Fetch all bundles
    print("🔍 STEP 1: Fetching all bundles...")
    bundles = get_all_bundles(store, token)
    print(f"   ✅ Found {len(bundles)} bundles\n")

    if len(bundles) == 0:
        print("❌ No bundles found!")
        return 1

    # Count bundles with null inventory management
    bundles_to_fix = []
    for bundle in bundles:
        for variant in bundle.get('variants', []):
            if variant.get('inventory_management') is None:
                bundles_to_fix.append({
                    'bundle_id': bundle['id'],
                    'bundle_handle': bundle['handle'],
                    'variant_id': variant['id'],
                    'variant_title': variant['title']
                })
                break  # Only need to fix one variant per bundle

    print(f"🔍 STEP 2: Analyzing inventory management...")
    print(f"   ⚠️  Bundles with NULL inventory_management: {len(bundles_to_fix)}/{len(bundles)}\n")

    if len(bundles_to_fix) == 0:
        print("✅ All bundles already have inventory management configured!")
        return 0

    print("="*100)
    print(f"\n🔧 STEP 3: Fixing {len(bundles_to_fix)} bundles...\n")

    success_count = 0
    failed_count = 0
    results = []

    for i, item in enumerate(bundles_to_fix, 1):
        print(f"[{i}/{len(bundles_to_fix)}] {item['bundle_handle']}")

        # Update variant to use Shopify inventory management
        if update_variant_inventory(store, token, item['variant_id'], "shopify"):
            print(f"   ✅ SUCCESS: Inventory management set to 'shopify'\n")
            success_count += 1
            results.append({
                'handle': item['bundle_handle'],
                'variant_id': item['variant_id'],
                'success': True
            })
        else:
            print(f"   ❌ FAILED to update\n")
            failed_count += 1
            results.append({
                'handle': item['bundle_handle'],
                'variant_id': item['variant_id'],
                'success': False
            })

    print("="*100)
    print(f"\n📊 RESULTS:")
    print(f"{'='*100}")
    print(f"✅ SUCCESS: {success_count}/{len(bundles_to_fix)} bundles")
    print(f"❌ FAILED:  {failed_count}/{len(bundles_to_fix)} bundles")
    print(f"📈 Success rate: {100*success_count/len(bundles_to_fix):.1f}%")
    print(f"{'='*100}")

    # Save results
    with open('bundle_inventory_fix_results.json', 'w') as f:
        json.dump({
            'total_bundles': len(bundles),
            'bundles_to_fix': len(bundles_to_fix),
            'success_count': success_count,
            'failed_count': failed_count,
            'results': results
        }, f, indent=2)

    print(f"\n💾 Results saved to: bundle_inventory_fix_results.json")

    if failed_count > 0:
        print(f"\n❌ FAILED BUNDLES:")
        for r in results:
            if not r['success']:
                print(f"   - {r['handle']} (variant: {r['variant_id']})")

    if success_count == len(bundles_to_fix):
        print(f"\n✅ 100% SUCCESS - All bundles now have inventory management!")
        return 0
    else:
        print(f"\n⚠️  PARTIAL SUCCESS - {failed_count} bundles still need manual attention")
        return 1

if __name__ == "__main__":
    exit_code = fix_inventory_management()
    exit(exit_code)
