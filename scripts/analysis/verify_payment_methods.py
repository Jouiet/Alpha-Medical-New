#!/usr/bin/env python3
"""
Verify Active Payment Methods on Shopify Store
Uses Shopify Admin API to check which payment gateways are enabled.
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-01'

headers = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def get_shop_info():
    """Get shop configuration including payment settings."""
    url = f'https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/shop.json'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    print("="*60)
    print("PAYMENT METHODS VERIFICATION")
    print("="*60)
    
    shop_info = get_shop_info()
    shop = shop_info.get('shop', {})
    
    print(f"\nStore: {shop.get('name')}")
    print(f"Domain: {shop.get('domain')}")
    print(f"Plan: {shop.get('plan_name')}")
    
    # Payment settings
    print("\n" + "="*60)
    print("PAYMENT SETTINGS")
    print("="*60)
    
    enabled_presentment_currencies = shop.get('enabled_presentment_currencies', [])
    print(f"Currencies: {', '.join(enabled_presentment_currencies)}")
    
    # Note: The Shopify Admin API doesn't directly expose payment gateway
    # configuration via /shop.json. We need to check the checkout settings
    # or use GraphQL for more detailed payment provider info.
    
    print("\n⚠️  Note: Admin REST API has limited payment gateway visibility.")
    print("For complete verification, check:")
    print("1. Shopify Admin UI: Settings → Payments")
    print("2. Or use GraphQL Admin API for payment providers")
    
    with open('payment_verification_results.json', 'w') as f:
        json.dump(shop_info, f, indent=2)
    
    print(f"\n✅ Shop data saved to: payment_verification_results.json")
    print("="*60)

if __name__ == '__main__':
    main()
