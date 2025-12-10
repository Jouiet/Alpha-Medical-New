#!/usr/bin/env python3
"""
Verify collections and their product counts via Shopify Admin API.
Script: verify_collections_products.py
Purpose: Identify empty collections that need product assignment
"""

import os
import json
import requests
from pathlib import Path

# Load credentials
env_path = Path(__file__).parent / '.env.admin'
with open(env_path) as f:
    for line in f:
        if line.strip() and not line.startswith('#') and '=' in line:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value.strip('"').strip("'")

SHOP_DOMAIN = os.environ.get('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

def get_collections():
    """Get all collections with product counts."""
    url = f"https://{SHOP_DOMAIN}/admin/api/2024-10/custom_collections.json?limit=250"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    collections = data.get('custom_collections', [])
    
    print(f"{'ID':<15} {'Handle':<30} {'Title':<40} {'Products':<10}")
    print("-" * 95)
    
    empty_collections = []
    for c in collections:
        # Get actual product count
        products_url = f"https://{SHOP_DOMAIN}/admin/api/2024-10/collections/{c['id']}/products.json?limit=1"
        products_response = requests.get(products_url, headers=headers)
        products_data = products_response.json()
        product_count = len(products_data.get('products', []))
        
        # Check if collection has products
        if product_count == 0:
            empty_collections.append(c)
            marker = "❌ EMPTY"
        else:
            marker = "✅"
        
        print(f"{c['id']:<15} {c['handle']:<30} {c['title']:<40} {product_count:<10} {marker}")
    
    if empty_collections:
        print(f"\n🚨 FOUND {len(empty_collections)} EMPTY COLLECTIONS:")
        for c in empty_collections:
            print(f"  - {c['title']} (ID: {c['id']}, handle: {c['handle']})")
    else:
        print("\n✅ ALL COLLECTIONS HAVE PRODUCTS")
    
    return empty_collections

if __name__ == '__main__':
    try:
        empty = get_collections()
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
