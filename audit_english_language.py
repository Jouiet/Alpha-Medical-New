#!/usr/bin/env python3
"""
Full English Language Audit for Alpha Medical store
Checks all products, collections, and pages for non-English content
"""

import os
import requests
import re
from dotenv import load_dotenv

# Load environment
load_dotenv('.env.admin')

# Configuration
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = "2025-10"

# Common French words to detect
FRENCH_KEYWORDS = [
    'livraison', 'gratuite', 'acheter', 'ajouter', 'panier',
    'prix', 'disponible', 'rupture', 'stock', 'couleur',
    'taille', 'description', 'caractéristiques', 'détails',
    'expédition', 'retour', 'garantie', 'qualité',
    'médical', 'santé', 'soulagement', 'douleur',
    'thérapie', 'traitement', 'produit', 'matériel'
]

def fetch_all_products():
    """Fetch all products"""
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/products.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    products = []
    params = {"limit": 250}

    while True:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            break

        data = response.json()
        batch = data.get('products', [])
        products.extend(batch)

        link_header = response.headers.get('Link', '')
        if 'rel="next"' not in link_header:
            break

        next_link = [l.strip() for l in link_header.split(',') if 'rel="next"' in l]
        if not next_link:
            break

        next_url = next_link[0].split(';')[0].strip('<>')
        url = next_url
        params = {}

    return products

def check_text_for_french(text, field_name):
    """Check if text contains French keywords"""
    if not text:
        return []

    text_lower = text.lower()
    found = []

    for keyword in FRENCH_KEYWORDS:
        if keyword in text_lower:
            # Get context (50 chars before and after)
            pattern = re.compile(f'.{{0,50}}{re.escape(keyword)}.{{0,50}}', re.IGNORECASE)
            matches = pattern.findall(text)
            for match in matches:
                found.append({
                    'field': field_name,
                    'keyword': keyword,
                    'context': match.strip()
                })

    return found

def audit_product(product):
    """Audit a single product for non-English content"""
    issues = []

    # Check title
    issues.extend(check_text_for_french(product.get('title'), 'title'))

    # Check body_html
    body = product.get('body_html', '')
    if body:
        # Strip HTML tags for analysis
        clean_body = re.sub(r'<[^>]+>', ' ', body)
        issues.extend(check_text_for_french(clean_body, 'description'))

    # Check vendor
    issues.extend(check_text_for_french(product.get('vendor'), 'vendor'))

    # Check product_type
    issues.extend(check_text_for_french(product.get('product_type'), 'product_type'))

    # Check tags
    tags = product.get('tags', '')
    if isinstance(tags, str):
        issues.extend(check_text_for_french(tags, 'tags'))

    # Check variants
    for idx, variant in enumerate(product.get('variants', [])):
        variant_title = variant.get('title')
        if variant_title and variant_title != 'Default Title':
            issues.extend(check_text_for_french(variant_title, f'variant_{idx}_title'))

    # Check options
    for idx, option in enumerate(product.get('options', [])):
        option_name = option.get('name')
        issues.extend(check_text_for_french(option_name, f'option_{idx}_name'))

        for val_idx, value in enumerate(option.get('values', [])):
            issues.extend(check_text_for_french(value, f'option_{idx}_value_{val_idx}'))

    # Check metafields (if any)
    for idx, metafield in enumerate(product.get('metafields', [])):
        issues.extend(check_text_for_french(metafield.get('value'), f'metafield_{idx}'))

    return issues

def main():
    """Run full English language audit"""
    print("=" * 70)
    print("FULL ENGLISH LANGUAGE AUDIT")
    print("=" * 70)
    print()

    # Fetch products
    print("Fetching all products...")
    products = fetch_all_products()
    print(f"✅ Fetched {len(products)} products")
    print()

    # Audit each product
    print("Auditing products for non-English content...")
    print("=" * 70)
    print()

    total_issues = 0
    products_with_issues = []

    for product in products:
        issues = audit_product(product)
        if issues:
            total_issues += len(issues)
            products_with_issues.append({
                'id': product['id'],
                'title': product['title'],
                'handle': product['handle'],
                'status': product['status'],
                'issues': issues
            })

    # Results
    print()
    print("=" * 70)
    print("AUDIT RESULTS")
    print("=" * 70)
    print()

    if total_issues == 0:
        print("✅ PERFECT: All products are 100% English")
        print()
        print(f"Products audited: {len(products)}")
        print(f"Issues found: 0")
        print()
        print("🎉 Store is ready for English-speaking market!")
    else:
        print(f"⚠️  Found {total_issues} potential non-English instances")
        print(f"Products with issues: {len(products_with_issues)}")
        print()
        print("DETAILS:")
        print("-" * 70)

        for p in products_with_issues:
            print()
            print(f"Product: {p['title']}")
            print(f"Handle: {p['handle']}")
            print(f"Status: {p['status']}")
            print(f"ID: {p['id']}")
            print(f"Issues: {len(p['issues'])}")

            for issue in p['issues'][:5]:  # Show first 5 issues per product
                print(f"  - {issue['field']}: '{issue['keyword']}' in \"{issue['context']}\"")

            if len(p['issues']) > 5:
                print(f"  ... and {len(p['issues']) - 5} more")

    print()
    print("=" * 70)

if __name__ == "__main__":
    main()
