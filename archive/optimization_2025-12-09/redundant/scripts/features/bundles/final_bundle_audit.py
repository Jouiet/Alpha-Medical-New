#!/usr/bin/env python3
"""
FINAL BUNDLE AUDIT - Comprehensive verification of all fixes

VERIFICATION FACTUELLE:
- Images: 15/15 bundles must have at least 1 image
- Inventory: 15/15 bundles must have inventory_management = "shopify"
- Weight: 15/15 bundles must have weight > 0

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

def final_audit():
    """Comprehensive audit of all bundles"""

    print("🔍 FINAL BUNDLE AUDIT - Comprehensive Verification\n")
    print("="*100)

    # Load credentials
    env = load_env()
    store = env.get('SHOPIFY_STORE_DOMAIN')
    token = env.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

    headers = {
        'X-Shopify-Access-Token': token,
        'Content-Type': 'application/json'
    }

    # Fetch all bundles
    url = f"https://{store}/admin/api/2024-10/products.json?product_type=Medical Equipment Bundle&limit=250"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        return 1

    products = response.json()['products']
    bundles = [p for p in products if 'bundle' in p.get('tags', '').lower()]

    print(f"📦 TOTAL BUNDLES: {len(bundles)}\n")
    print("="*100)

    # Audit metrics
    images_pass = 0
    images_fail = 0
    inventory_pass = 0
    inventory_fail = 0
    weight_pass = 0
    weight_fail = 0

    all_pass = []
    failures = []

    for i, bundle in enumerate(bundles, 1):
        handle = bundle['handle']
        image_count = len(bundle.get('images', []))

        # Get variant data
        variant = bundle.get('variants', [{}])[0]
        inventory_mgmt = variant.get('inventory_management')
        weight = variant.get('weight', 0)

        # Check images
        has_images = image_count > 0
        if has_images:
            images_pass += 1
        else:
            images_fail += 1

        # Check inventory
        has_inventory = inventory_mgmt == 'shopify'
        if has_inventory:
            inventory_pass += 1
        else:
            inventory_fail += 1

        # Check weight
        has_weight = weight > 0
        if has_weight:
            weight_pass += 1
        else:
            weight_fail += 1

        # Overall pass/fail
        all_checks_pass = has_images and has_inventory and has_weight

        if all_checks_pass:
            all_pass.append(handle)
        else:
            issues = []
            if not has_images:
                issues.append(f"No images ({image_count})")
            if not has_inventory:
                issues.append(f"Inventory: {inventory_mgmt}")
            if not has_weight:
                issues.append(f"Weight: {weight}")

            failures.append({
                'handle': handle,
                'issues': issues
            })

        # Print status
        status = "✅" if all_checks_pass else "❌"
        print(f"{status} [{i:2d}/15] {handle}")
        print(f"      Images: {image_count:>2} | Inventory: {str(inventory_mgmt):>10} | Weight: {weight:>5.2f} kg")

        if not all_checks_pass:
            for issue in issues:
                print(f"      🚨 {issue}")

        print()

    print("="*100)
    print(f"\n📊 AUDIT RESULTS:")
    print(f"{'='*100}\n")

    print(f"🖼️  IMAGES:")
    print(f"   ✅ PASS: {images_pass}/15 bundles have images")
    print(f"   ❌ FAIL: {images_fail}/15 bundles have NO images")
    print(f"   📈 Success rate: {100*images_pass/15:.1f}%\n")

    print(f"📦 INVENTORY MANAGEMENT:")
    print(f"   ✅ PASS: {inventory_pass}/15 bundles have inventory_management = 'shopify'")
    print(f"   ❌ FAIL: {inventory_fail}/15 bundles have NULL inventory_management")
    print(f"   📈 Success rate: {100*inventory_pass/15:.1f}%\n")

    print(f"⚖️  WEIGHT:")
    print(f"   ✅ PASS: {weight_pass}/15 bundles have weight > 0")
    print(f"   ❌ FAIL: {weight_fail}/15 bundles have weight = 0")
    print(f"   📈 Success rate: {100*weight_pass/15:.1f}%\n")

    print(f"{'='*100}")
    print(f"\n🎯 OVERALL COMPLIANCE:")
    print(f"   ✅ ALL CHECKS PASS: {len(all_pass)}/15 bundles")
    print(f"   ❌ SOME CHECKS FAIL: {len(failures)}/15 bundles")
    print(f"   📈 Overall success rate: {100*len(all_pass)/15:.1f}%")
    print(f"{'='*100}")

    if len(failures) > 0:
        print(f"\n❌ BUNDLES WITH ISSUES:")
        print(f"{'='*100}")
        for f in failures:
            print(f"   {f['handle']}")
            for issue in f['issues']:
                print(f"      • {issue}")
        print(f"{'='*100}")

    # Save results
    results = {
        'audit_date': '2025-11-16',
        'total_bundles': len(bundles),
        'images': {
            'pass': images_pass,
            'fail': images_fail,
            'rate': f"{100*images_pass/15:.1f}%"
        },
        'inventory': {
            'pass': inventory_pass,
            'fail': inventory_fail,
            'rate': f"{100*inventory_pass/15:.1f}%"
        },
        'weight': {
            'pass': weight_pass,
            'fail': weight_fail,
            'rate': f"{100*weight_pass/15:.1f}%"
        },
        'overall': {
            'pass': len(all_pass),
            'fail': len(failures),
            'rate': f"{100*len(all_pass)/15:.1f}%"
        },
        'failures': failures,
        'all_pass': all_pass
    }

    with open('final_bundle_audit_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Audit results saved to: final_bundle_audit_results.json\n")

    if len(all_pass) == 15:
        print("✅ ✅ ✅ AUDIT PASSED: ALL 15 BUNDLES ARE COMPLIANT! ✅ ✅ ✅\n")
        return 0
    else:
        print(f"❌ AUDIT FAILED: {len(failures)} bundles still have issues\n")
        return 1

if __name__ == "__main__":
    exit_code = final_audit()
    exit(exit_code)
