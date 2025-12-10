#!/usr/bin/env python3
"""
Bundle Products Investigation Script
Fetches all Bundle products and analyzes inventory structure.
"""
import os
import json
import requests
from dotenv import load_dotenv

# Load credentials
load_dotenv('.env.admin')

SHOPIFY_STORE = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-01'

headers = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def fetch_bundle_products():
    """Fetch all products in the Bundles collection."""
    url = f'https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/products.json'
    
    all_bundles = []
    params = {'limit': 250, 'product_type': 'Bundle'}
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        products = data.get('products', [])
        all_bundles.extend(products)
        
        # Check for pagination
        link_header = response.headers.get('Link', '')
        if 'rel="next"' not in link_header:
            break
            
        # Extract next page URL
        next_url = None
        for link in link_header.split(','):
            if 'rel="next"' in link:
                next_url = link.split(';')[0].strip('<> ')
                break
        
        if not next_url:
            break
            
        url = next_url
        params = {}  # Pagination URL already has params
    
    return all_bundles

def analyze_bundle_structure(bundles):
    """Analyze Bundle product structure and inventory."""
    analysis = {
        'total_bundles': len(bundles),
        'bundles': []
    }
    
    for bundle in bundles:
        variants = bundle.get('variants', [])
        
        bundle_info = {
            'id': bundle['id'],
            'title': bundle['title'],
            'handle': bundle['handle'],
            'status': bundle['status'],
            'product_type': bundle['product_type'],
            'total_inventory': 0,
            'variants': [],
            'metafields_count': len(bundle.get('metafields', [])),
            'images_count': len(bundle.get('images', []))
        }
        
        for variant in variants:
            variant_info = {
                'id': variant['id'],
                'title': variant['title'],
                'price': variant['price'],
                'inventory_quantity': variant.get('inventory_quantity', 0),
                'inventory_management': variant.get('inventory_management'),
                'inventory_policy': variant.get('inventory_policy')
            }
            bundle_info['variants'].append(variant_info)
            bundle_info['total_inventory'] += variant.get('inventory_quantity', 0)
        
        analysis['bundles'].append(bundle_info)
    
    return analysis

def main():
    print("Fetching Bundle products from Shopify...")
    bundles = fetch_bundle_products()
    
    print(f"Found {len(bundles)} Bundle products")
    
    print("\nAnalyzing Bundle structure...")
    analysis = analyze_bundle_structure(bundles)
    
    # Save results
    output_file = 'bundle_inventory_investigation.json'
    with open(output_file, 'w') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\n✅ Analysis saved to {output_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("BUNDLE INVENTORY SUMMARY")
    print("="*60)
    
    for bundle in analysis['bundles']:
        status_icon = "✅" if bundle['total_inventory'] > 0 else "❌"
        print(f"{status_icon} {bundle['title']}")
        print(f"   ID: {bundle['id']}")
        print(f"   Status: {bundle['status']}")
        print(f"   Total Inventory: {bundle['total_inventory']}")
        print(f"   Variants: {len(bundle['variants'])}")
        print()
    
    # Check for critical issues
    zero_inventory_count = sum(1 for b in analysis['bundles'] if b['total_inventory'] == 0)
    
    if zero_inventory_count > 0:
        print(f"\n🚨 WARNING: {zero_inventory_count}/{len(bundles)} bundles have 0 inventory")
    else:
        print(f"\n✅ All bundles have inventory set")

if __name__ == '__main__':
    main()
