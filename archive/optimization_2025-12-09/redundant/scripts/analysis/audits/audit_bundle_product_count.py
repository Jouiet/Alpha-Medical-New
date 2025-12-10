#!/usr/bin/env python3
"""
AUDIT BUNDLE PRODUCT COUNT - CRITICAL COMPLIANCE CHECK

RÈGLE STRICTE: TOUS les bundles doivent avoir 3-4 produits MAXIMUM
AUCUN bundle ne doit dépasser 4 produits

Author: Claude Code
Date: 2025-11-16
"""

import requests
import json
import re

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

def extract_product_count_from_body(body_html):
    """Count products listed in bundle body_html"""
    if not body_html:
        return 0, []

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', body_html)

    # Find lines with checkmarks or bullets
    lines = text.split('\n')
    products = []

    for line in lines:
        if '✓' in line or '•' in line or line.strip().startswith(('-', '*')):
            # Clean the line
            clean = line.replace('✓', '').replace('•', '').replace('-', '').replace('*', '').strip()

            # Remove price if present
            clean = re.sub(r'\s*-\s*\$[\d,]+\.?\d*', '', clean)

            if clean and len(clean) > 10:
                products.append(clean)

    return len(products), products

def audit_product_counts():
    """Audit all bundles for product count compliance"""

    print("🔍 AUDIT BUNDLE PRODUCT COUNT - COMPLIANCE CHECK\n")
    print("="*100)
    print("RÈGLE: TOUS les bundles doivent avoir 3-4 produits MAXIMUM")
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

    products_data = response.json()['products']
    bundles = [p for p in products_data if 'bundle' in p.get('tags', '').lower()]

    print(f"\n📦 TOTAL BUNDLES: {len(bundles)}\n")
    print("="*100)

    # Categorize bundles
    compliant = []      # 3-4 products
    too_few = []        # < 3 products
    violations = []     # > 4 products

    for i, bundle in enumerate(bundles, 1):
        handle = bundle['handle']
        title = bundle['title']
        bundle_id = bundle['id']

        count, product_list = extract_product_count_from_body(bundle.get('body_html', ''))

        print(f"\n[{i}/{len(bundles)}] {handle}")
        print(f"   Title: {title[:70]}")
        print(f"   Product count: {count}")

        if count < 3:
            print(f"   ⚠️  WARNING: TOO FEW products (minimum 3)")
            too_few.append({
                'handle': handle,
                'title': title,
                'id': bundle_id,
                'count': count,
                'products': product_list
            })
        elif count > 4:
            print(f"   ❌ VIOLATION: TOO MANY products (maximum 4)")
            print(f"   🚨 CRITICAL: Must reduce from {count} to 4 products")
            violations.append({
                'handle': handle,
                'title': title,
                'id': bundle_id,
                'count': count,
                'products': product_list,
                'excess': count - 4
            })
        else:
            print(f"   ✅ COMPLIANT: {count} products (3-4 range)")
            compliant.append({
                'handle': handle,
                'title': title,
                'id': bundle_id,
                'count': count,
                'products': product_list
            })

    print("\n" + "="*100)
    print(f"\n📊 COMPLIANCE AUDIT RESULTS:")
    print(f"{'='*100}\n")

    print(f"✅ COMPLIANT (3-4 products):  {len(compliant)}/15")
    print(f"⚠️  TOO FEW (<3 products):    {len(too_few)}/15")
    print(f"❌ VIOLATIONS (>4 products):  {len(violations)}/15")
    print(f"\n📈 Compliance rate: {100*len(compliant)/15:.1f}%")
    print(f"{'='*100}")

    # Show violations
    if violations:
        print(f"\n🚨 CRITICAL VIOLATIONS - Bundles with >4 products:")
        print(f"{'='*100}")
        for v in violations:
            print(f"\n❌ {v['handle']}")
            print(f"   Count: {v['count']} products ({v['excess']} over limit)")
            print(f"   Products:")
            for j, p in enumerate(v['products'], 1):
                print(f"      {j}. {p[:70]}")
        print(f"{'='*100}")

    # Show too few
    if too_few:
        print(f"\n⚠️  WARNING - Bundles with <3 products:")
        print(f"{'='*100}")
        for t in too_few:
            print(f"\n⚠️  {t['handle']}")
            print(f"   Count: {t['count']} products (need {3-t['count']} more)")
            print(f"   Products:")
            for j, p in enumerate(t['products'], 1):
                print(f"      {j}. {p[:70]}")
        print(f"{'='*100}")

    # Save results
    output = {
        'audit_date': '2025-11-16',
        'rule': 'ALL bundles must have 3-4 products',
        'total_bundles': len(bundles),
        'compliant': len(compliant),
        'too_few': len(too_few),
        'violations': len(violations),
        'compliance_rate': f"{100*len(compliant)/15:.1f}%",
        'compliant_bundles': compliant,
        'too_few_bundles': too_few,
        'violation_bundles': violations
    }

    with open('bundle_product_count_audit.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n💾 Results saved to: bundle_product_count_audit.json")

    # Final verdict
    print(f"\n🎯 FINAL VERDICT:")
    print(f"{'='*100}")

    if violations:
        print(f"❌ AUDIT FAILED: {len(violations)} bundles violate 4-product maximum")
        print(f"ACTION REQUIRED: Reduce {len(violations)} bundles to 3-4 products")
        print(f"Total excess products: {sum([v['excess'] for v in violations])}")
        return 1
    elif too_few:
        print(f"⚠️  PARTIAL COMPLIANCE: {len(too_few)} bundles below 3-product minimum")
        return 1
    else:
        print(f"✅ FULL COMPLIANCE: All 15 bundles have 3-4 products")
        return 0

if __name__ == "__main__":
    exit_code = audit_product_counts()
    exit(exit_code)
