#!/usr/bin/env python3
"""
Verify Critical Discount Codes for Klaviyo Flows
Checks: WELCOME10, WINBACK15, REVIEW10
"""

import requests
import json
import os
from datetime import datetime

# Load credentials
def load_credentials():
    env_path = "/Users/mac/Desktop/Alpha-Medical/.env.admin"
    creds = {}

    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                creds[key] = value

    return creds

creds = load_credentials()

# Shopify API configuration
SHOPIFY_STORE = "azffej-as"
ACCESS_TOKEN = creds.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

if not ACCESS_TOKEN:
    print("❌ Missing SHOPIFY_ADMIN_ACCESS_TOKEN in .env.admin")
    exit(1)

BASE_URL = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/2024-10"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

REQUIRED_CODES = {
    "WELCOME10": {
        "type": "percentage",
        "value": "10.00",
        "usage": "Welcome series (Klaviyo + Shopify Email)"
    },
    "WINBACK15": {
        "type": "percentage",
        "value": "15.00",
        "usage": "Win-back campaign (Klaviyo)"
    },
    "REVIEW10": {
        "type": "percentage",
        "value": "10.00",
        "usage": "Review request (Klaviyo post-purchase)"
    }
}

def get_price_rules():
    """Get all price rules (discount codes)"""
    url = f"{BASE_URL}/price_rules.json"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        return []

    return response.json().get('price_rules', [])

def get_discount_codes(price_rule_id):
    """Get discount codes for a price rule"""
    url = f"{BASE_URL}/price_rules/{price_rule_id}/discount_codes.json"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return []

    return response.json().get('discount_codes', [])

def verify_codes():
    print("=" * 70)
    print("🔍 VERIFYING CRITICAL DISCOUNT CODES")
    print("=" * 70)
    print()

    # Get all price rules
    print("📥 Fetching price rules from Shopify API...")
    price_rules = get_price_rules()
    print(f"   Found {len(price_rules)} price rules\n")

    # Build code map
    all_codes = {}
    for rule in price_rules:
        rule_id = rule['id']
        codes = get_discount_codes(rule_id)

        for code in codes:
            code_name = code['code']
            all_codes[code_name] = {
                'id': code['id'],
                'price_rule_id': rule_id,
                'value': rule['value'],
                'value_type': rule['value_type'],
                'usage_count': code['usage_count'],
                'created_at': rule['created_at'],
                'starts_at': rule['starts_at'],
                'ends_at': rule['ends_at'],
                'title': rule['title']
            }

    # Verify required codes
    print("=" * 70)
    print("📊 VERIFICATION RESULTS")
    print("=" * 70)
    print()

    found_count = 0
    missing_count = 0

    for code_name, requirements in REQUIRED_CODES.items():
        print(f"🎫 {code_name}")
        print(f"   Purpose: {requirements['usage']}")

        if code_name in all_codes:
            code_data = all_codes[code_name]

            # Check value type
            if code_data['value_type'] == 'percentage':
                discount_value = f"{code_data['value']}%"
            elif code_data['value_type'] == 'fixed_amount':
                discount_value = f"${float(code_data['value']) / 100:.2f}"
            else:
                discount_value = code_data['value']

            # Verify value matches requirement
            expected_value = f"-{requirements['value']}"

            if code_data['value'] == expected_value:
                print(f"   ✅ EXISTS - Discount: {discount_value}")
            else:
                print(f"   ⚠️  EXISTS but WRONG VALUE")
                print(f"      Expected: {requirements['value']}%")
                print(f"      Actual: {discount_value}")

            print(f"   Usage count: {code_data['usage_count']}")
            print(f"   Created: {code_data['created_at'][:10]}")

            if code_data['ends_at']:
                print(f"   Expires: {code_data['ends_at'][:10]}")
            else:
                print(f"   Expires: Never ✅")

            found_count += 1
        else:
            print(f"   ❌ MISSING - Required for {requirements['usage']}")
            print(f"      Expected: {requirements['value']}% discount")
            print(f"      Action: Create in Shopify Admin")
            missing_count += 1

        print()

    # Summary
    print("=" * 70)
    print("📈 SUMMARY")
    print("=" * 70)
    print(f"\n✅ Found: {found_count}/{len(REQUIRED_CODES)}")
    print(f"❌ Missing: {missing_count}/{len(REQUIRED_CODES)}")

    if missing_count == 0:
        print("\n🎉 ALL REQUIRED DISCOUNT CODES ARE CONFIGURED")
        print("   Klaviyo flows can use these codes successfully")
    else:
        print(f"\n⚠️  {missing_count} DISCOUNT CODE(S) MISSING")
        print("   Manual creation required in Shopify Admin:")
        print("   Settings → Discounts → Create discount code")

    # Additional codes found
    additional = [code for code in all_codes.keys() if code not in REQUIRED_CODES]
    if additional:
        print(f"\n📋 Additional discount codes found ({len(additional)}):")
        for code in sorted(additional):
            print(f"   - {code}")

    print()

if __name__ == "__main__":
    verify_codes()
