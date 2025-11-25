#!/usr/bin/env python3
"""
Audit Shopify Subscriptions (Selling Plans)
Check if native subscriptions are configured
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2024-10'

BASE_URL = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}'
HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN
}

def api_request(endpoint):
    """Make API request"""
    url = f'{BASE_URL}{endpoint}'
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e), 'status_code': getattr(e.response, 'status_code', None)}

print("="*80)
print("SUBSCRIPTION AUDIT (Selling Plans)")
print("="*80)
print(f"Store: {SHOPIFY_STORE_DOMAIN}\n")

# Check selling plan groups
print("Checking Selling Plan Groups...")
result = api_request('/selling_plan_groups.json')

if 'error' in result:
    print(f"❌ Error: {result['error']}")
    if result.get('status_code') == 404:
        print("⚠️  Selling Plans API endpoint not found")
        print("💡 This may mean Basic plan doesn't support Selling Plans via API")
    elif result.get('status_code') == 403:
        print("⚠️  ACCESS DENIED - Selling Plans may require higher plan")
else:
    groups = result.get('selling_plan_groups', [])
    print(f"✅ Total Selling Plan Groups: {len(groups)}\n")

    if groups:
        for i, group in enumerate(groups, 1):
            print(f"Group {i}: {group.get('name', 'N/A')}")
            print(f"  ID: {group.get('id', 'N/A')}")
            print(f"  Admin GraphQL ID: {group.get('admin_graphql_api_id', 'N/A')}")
            print(f"  Merchant Code: {group.get('merchant_code', 'N/A')}")
            print(f"  Description: {group.get('description', 'N/A')}")
            print(f"  Options: {group.get('options', [])}")
            print(f"  Selling Plans Count: {len(group.get('selling_plans', []))}")

            if group.get('selling_plans'):
                for j, plan in enumerate(group['selling_plans'], 1):
                    print(f"\n  Plan {j}: {plan.get('name', 'N/A')}")
                    print(f"    ID: {plan.get('id', 'N/A')}")
                    print(f"    Billing Policy: {plan.get('billing_policy', {})}")
                    print(f"    Delivery Policy: {plan.get('delivery_policy', {})}")
                    print(f"    Pricing Policies: {plan.get('pricing_policies', [])}")
            print()
    else:
        print("⚠️  NO Selling Plan Groups configured")
        print("💡 Native subscriptions NOT set up")
        print("📋 Action: Create selling plan groups via Shopify Admin UI")

print("="*80)
print("VERDICT")
print("="*80)

if 'error' not in result:
    groups = result.get('selling_plan_groups', [])
    if groups:
        print(f"✅ Subscriptions CONFIGURED ({len(groups)} groups)")
    else:
        print("❌ Subscriptions NOT CONFIGURED")
        print("   Status: Available but not set up")
        print("   Next: Create selling plan groups in Shopify Admin")
else:
    print("❌ Subscriptions API ERROR")
    print(f"   Error: {result.get('error', 'Unknown')}")
    print("   May require manual verification or plan upgrade")

print("="*80)
