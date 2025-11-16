#!/usr/bin/env python3
"""
AUDIT BUNDLE PAGES DISPLAY - Verify product display on bundle pages

PROBLÈME IDENTIFIÉ:
- Bundle pages show only 1 image (bundle image)
- Individual product images from bundle composition NOT displayed
- UX issue: Customers can't SEE what they're getting

AUDIT:
- Check all 15 bundle pages
- Verify if individual product images are displayed
- Check if there's a product showcase section

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

def extract_product_count_from_body(body_html):
    """Count products listed in bundle body_html"""
    if not body_html:
        return 0

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', body_html)

    # Find lines with checkmarks or bullets
    lines = text.split('\n')
    count = 0

    for line in lines:
        if '✓' in line or '•' in line or line.strip().startswith(('-', '*')):
            # Clean the line
            clean = line.replace('✓', '').replace('•', '').replace('-', '').replace('*', '').strip()

            # Remove price if present
            clean = re.sub(r'\s*-\s*\$[\d,]+\.?\d*', '', clean)

            if clean and len(clean) > 10:
                count += 1

    return count

def audit_bundle_display():
    """Audit bundle page display for all bundles"""

    print("🔍 AUDIT BUNDLE PAGE DISPLAY - Visual Product Showcase\n")
    print("="*100)

    # Load credentials
    env = load_env()
    store = env.get('SHOPIFY_STORE_DOMAIN')
    token = env.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

    if not store or not token:
        print("❌ ERROR: Missing credentials")
        return 1

    # Fetch all bundles
    print("📦 Fetching all bundles...")
    bundles = get_all_bundles(store, token)
    print(f"   ✅ Found {len(bundles)} bundles\n")
    print("="*100)

    issues = []
    results = []

    for i, bundle in enumerate(bundles, 1):
        handle = bundle['handle']
        title = bundle['title']
        image_count = len(bundle.get('images', []))
        product_count = extract_product_count_from_body(bundle.get('body_html', ''))

        print(f"\n[{i}/{len(bundles)}] {handle}")
        print(f"   Title: {title[:70]}")
        print(f"   Products in bundle: {product_count}")
        print(f"   Images on product: {image_count}")

        # ISSUE: Bundle shows only 1 image (the bundle image itself)
        # Should show: 1 bundle image + individual product images
        if image_count == 1 and product_count > 0:
            print(f"   ⚠️  ISSUE: Only 1 image for {product_count} products")
            print(f"   ❌ Individual product images NOT displayed")
            issues.append({
                'handle': handle,
                'title': title,
                'product_count': product_count,
                'image_count': image_count,
                'issue': f'Only {image_count} image for {product_count} products'
            })
        elif image_count == 0:
            print(f"   ❌ CRITICAL: NO IMAGES")
            issues.append({
                'handle': handle,
                'title': title,
                'product_count': product_count,
                'image_count': image_count,
                'issue': 'No images at all'
            })
        else:
            print(f"   ✅ OK: {image_count} images")

        results.append({
            'handle': handle,
            'title': title,
            'product_count': product_count,
            'image_count': image_count,
            'has_issue': image_count <= 1 and product_count > 0
        })

    print("\n" + "="*100)
    print(f"\n📊 AUDIT RESULTS:")
    print(f"{'='*100}")
    print(f"Total bundles audited: {len(bundles)}")
    print(f"Bundles with display issues: {len(issues)}/{len(bundles)}")
    print(f"{'='*100}")

    if issues:
        print(f"\n⚠️  BUNDLES WITH DISPLAY ISSUES:")
        print(f"{'='*100}")
        for issue in issues:
            print(f"   {issue['handle']}")
            print(f"      Products: {issue['product_count']} | Images: {issue['image_count']}")
            print(f"      Issue: {issue['issue']}")
        print(f"{'='*100}")

    # Save results
    output = {
        'audit_date': '2025-11-16',
        'total_bundles': len(bundles),
        'bundles_with_issues': len(issues),
        'issues': issues,
        'all_results': results
    }

    with open('bundle_display_audit_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n💾 Results saved to: bundle_display_audit_results.json")

    # Conclusion
    print(f"\n🎯 CONCLUSION:")
    print(f"{'='*100}")
    if len(issues) == len(bundles):
        print(f"❌ ALL {len(bundles)} bundles have display issues!")
        print(f"Problem: Customers can't SEE individual products in bundle")
        print(f"Impact: Lower conversion rates (customers don't trust what they can't see)")
        print(f"Solution needed: Add product showcase section with individual product images")
    elif len(issues) > 0:
        print(f"⚠️  {len(issues)}/{len(bundles)} bundles have display issues")
        print(f"Action required: Fix display for affected bundles")
    else:
        print(f"✅ All bundles display correctly")
    print(f"{'='*100}")

    return 0 if len(issues) == 0 else 1

if __name__ == "__main__":
    exit_code = audit_bundle_display()
    exit(exit_code)
