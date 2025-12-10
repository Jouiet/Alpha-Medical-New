#!/usr/bin/env python3
"""
BUNDLE IMAGE AUDIT SCRIPT
Identifies all bundles missing images - CRITICAL for e-commerce

EXIGENCES:
- Vérification FACTUELLE de tous les bundles
- Identification précise des bundles sans images
- Génération de rapport détaillé pour correction

Author: Claude Code
Date: 2025-11-16
"""

import requests
import json
import os

# Load credentials from .env.admin
def load_env():
    """Load environment variables from .env.admin"""
    env_vars = {}
    try:
        with open('.env.admin', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        print("❌ ERROR: .env.admin file not found")
        exit(1)
    return env_vars

def audit_bundle_images():
    """Audit all bundles for missing images"""

    # Load credentials
    env = load_env()
    admin_token = env.get('SHOPIFY_ADMIN_ACCESS_TOKEN')
    store = env.get('SHOPIFY_STORE_DOMAIN')

    if not admin_token or not store:
        print("❌ ERROR: Missing credentials in .env.admin")
        exit(1)

    headers = {
        'X-Shopify-Access-Token': admin_token,
        'Content-Type': 'application/json'
    }

    # Fetch all products with bundle tag
    print("🔍 FETCHING BUNDLES FROM SHOPIFY...\n")

    url = f"https://{store}/admin/api/2024-10/products.json?product_type=Medical Equipment Bundle&limit=250"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ API ERROR: {response.status_code}")
        print(response.text)
        exit(1)

    products = response.json()['products']
    bundles = [p for p in products if 'bundle' in p.get('tags', '').lower()]

    print(f"📦 TOTAL BUNDLES FOUND: {len(bundles)}\n")
    print("=" * 100)

    # Categorize bundles
    no_images = []
    with_images = []
    critical_issues = []

    for bundle in bundles:
        image_count = len(bundle.get('images', []))
        handle = bundle['handle']
        title = bundle['title']
        bundle_id = bundle['id']
        status = bundle['status']

        bundle_data = {
            'id': bundle_id,
            'handle': handle,
            'title': title,
            'image_count': image_count,
            'status': status,
            'images': bundle.get('images', [])
        }

        if image_count == 0:
            no_images.append(bundle_data)
            print(f"❌ ZERO IMAGES: {handle}")
            print(f"   Title: {title}")
            print(f"   ID: {bundle_id}")
            print(f"   Status: {status}")

            # Check for other critical issues
            issues = []
            if bundle.get('variants', [{}])[0].get('inventory_management') is None:
                issues.append("No inventory management")
            if bundle.get('variants', [{}])[0].get('weight', 0) == 0:
                issues.append("Weight = 0")
            if not bundle.get('body_html'):
                issues.append("Empty description")

            if issues:
                critical_issues.append({
                    'handle': handle,
                    'issues': issues
                })
                print(f"   🚨 Additional issues: {', '.join(issues)}")

            print()
        else:
            with_images.append(bundle_data)

    print("=" * 100)
    print(f"\n📊 AUDIT SUMMARY:")
    print(f"{'='*100}")
    print(f"✅ Bundles WITH images:    {len(with_images):>3} bundles")
    print(f"❌ Bundles WITHOUT images: {len(no_images):>3} bundles")
    print(f"📈 Image completion rate:  {len(with_images)}/{len(bundles)} ({100*len(with_images)/len(bundles):.1f}%)")
    print(f"{'='*100}")

    # Critical bundles without images
    if no_images:
        print(f"\n🚨 CRITICAL: {len(no_images)} BUNDLES HAVE ZERO IMAGES (CATASTROPHIC FOR SALES)")
        print(f"{'='*100}")
        for i, bundle in enumerate(no_images, 1):
            print(f"{i:2d}. {bundle['handle']}")
            print(f"    Status: {bundle['status']}")
        print(f"{'='*100}")

    # Additional issues
    if critical_issues:
        print(f"\n⚠️  BUNDLES WITH MULTIPLE CRITICAL ISSUES:")
        print(f"{'='*100}")
        for issue in critical_issues:
            print(f"- {issue['handle']}")
            for i in issue['issues']:
                print(f"  • {i}")
        print(f"{'='*100}")

    # Save results to JSON for script use
    results = {
        'audit_date': '2025-11-16',
        'total_bundles': len(bundles),
        'bundles_with_images': len(with_images),
        'bundles_without_images': len(no_images),
        'completion_rate': f"{100*len(with_images)/len(bundles):.1f}%",
        'missing_images_list': no_images,
        'critical_issues': critical_issues
    }

    output_file = 'bundles_missing_images_audit.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 AUDIT RESULTS SAVED TO: {output_file}")

    # Return status code
    if no_images:
        print(f"\n🔴 AUDIT FAILED: {len(no_images)} bundles require immediate attention")
        return 1
    else:
        print(f"\n✅ AUDIT PASSED: All bundles have images")
        return 0

if __name__ == "__main__":
    exit_code = audit_bundle_images()
    exit(exit_code)
