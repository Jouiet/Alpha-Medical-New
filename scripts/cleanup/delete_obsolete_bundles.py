#!/usr/bin/env python3
"""
Delete Obsolete Bundle Products
Removes the 10 old 'Complete Care Kit' bundles from Nov 11 that have 0 inventory, no images.
These are obsolete drafts superseded by newer bundles created in Dec 2025.
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

# IDs of obsolete bundles (from investigation)
OBSOLETE_BUNDLE_IDS = [
    7620850876493,  # Active Athlete & Sports Enthusiast
    7620851105869,  # Active Athlete - Knee Support Kit
    7620851171405,  # Beauty & Wellness - Premium Facial Therapy Kit
    7620851007565,  # Beauty & Wellness Enthusiast
    7620851040333,  # Comprehensive Therapy User
    7620850942029,  # Elderly / Mobility Support
    7620851073101,  # Foot Care & Bunion Relief
    7620851138637,  # Office Worker - Back & Neck Relief Kit
    7620850909261,  # Office Worker with Chronic Pain
    7620850974797,  # Post-Injury / Post-Surgery Recovery
]

def delete_product(product_id):
    """Delete a product by ID."""
    url = f'https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/products/{product_id}.json'
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 200:
        return {'success': True, 'id': product_id}
    else:
        return {
            'success': False,
            'id': product_id,
            'error': response.text
        }

def main():
    print("="*60)
    print("DELETING OBSOLETE BUNDLE PRODUCTS")
    print("="*60)
    print(f"Total bundles to delete: {len(OBSOLETE_BUNDLE_IDS)}")
    print()
    
    results = {
        'deleted': [],
        'failed': []
    }
    
    for idx, product_id in enumerate(OBSOLETE_BUNDLE_IDS, 1):
        print(f"[{idx}/{len(OBSOLETE_BUNDLE_IDS)}] Deleting product ID: {product_id}...")
        
        result = delete_product(product_id)
        
        if result['success']:
            print(f"   ✅ DELETED")
            results['deleted'].append(product_id)
        else:
            print(f"   ❌ FAILED: {result.get('error', 'Unknown error')}")
            results['failed'].append({
                'id': product_id,
                'error': result.get('error')
            })
        print()
    
    # Save results
    output_file = 'obsolete_bundles_deletion_log.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("="*60)
    print("DELETION SUMMARY")
    print("="*60)
    print(f"✅ Successfully deleted: {len(results['deleted'])}/{len(OBSOLETE_BUNDLE_IDS)}")
    print(f"❌ Failed: {len(results['failed'])}/{len(OBSOLETE_BUNDLE_IDS)}")
    
    if results['failed']:
        print("\nFailed deletions:")
        for fail in results['failed']:
            print(f"  - ID {fail['id']}: {fail['error']}")
    
    print(f"\n📄 Results saved to: {output_file}")
    print("="*60)

if __name__ == '__main__':
    main()
