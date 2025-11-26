#!/usr/bin/env python3
"""
Create Klaviyo discount codes via Shopify API
Created: 2025-11-26 Session 56+
Codes: WINBACK15 (15% OFF), REVIEW10 (10% OFF)
"""

import requests
import json
from datetime import datetime, timedelta

# Load from .env.admin
SHOPIFY_TOKEN = None
SHOPIFY_STORE = None

with open('.env.admin', 'r') as f:
    for line in f:
        if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
            SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
        elif line.startswith('SHOPIFY_STORE_DOMAIN='):
            SHOPIFY_STORE = line.split('=', 1)[1].strip()

if not SHOPIFY_TOKEN or not SHOPIFY_STORE:
    print("❌ ERROR: Missing Shopify credentials in .env.admin")
    exit(1)

SHOPIFY_API = f"https://{SHOPIFY_STORE}/admin/api/2024-10"
headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# Tomorrow's date for start (2025-11-27)
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

print("="*60)
print("CREATING KLAVIYO DISCOUNT CODES")
print("="*60)

# ============================================================
# DISCOUNT CODE #1: WINBACK15
# ============================================================

print("\n[1/2] Creating WINBACK15 - Customer Winback 15% OFF...")
print("-" * 60)

winback_data = {
    "price_rule": {
        "title": "WINBACK15 - Customer Winback 15% OFF",
        "target_type": "line_item",
        "target_selection": "all",  # ALL PRODUCTS (not specific collections)
        "allocation_method": "across",
        "value_type": "percentage",
        "value": "-15.0",
        "customer_selection": "all",
        "starts_at": f"{tomorrow}T00:00:00Z",
        "usage_limit": 1000,  # Max 1000 uses
        "once_per_customer": True  # Once per customer
    }
}

r = requests.post(f"{SHOPIFY_API}/price_rules.json",
                  headers=headers,
                  data=json.dumps(winback_data))

if r.status_code == 201:
    price_rule_id = r.json()['price_rule']['id']
    print(f"✅ Price rule created: ID {price_rule_id}")

    # Create discount code
    code_data = {
        "discount_code": {
            "code": "WINBACK15"
        }
    }

    r2 = requests.post(f"{SHOPIFY_API}/price_rules/{price_rule_id}/discount_codes.json",
                       headers=headers,
                       data=json.dumps(code_data))

    if r2.status_code == 201:
        print(f"✅ Code WINBACK15 created successfully")
        print(f"   - Value: 15% OFF")
        print(f"   - Applies to: ALL PRODUCTS")
        print(f"   - Usage limit: 1000 total, once per customer")
        print(f"   - Active from: {tomorrow}")
    else:
        print(f"❌ Error creating code: {r2.status_code}")
        print(f"   Response: {r2.text}")
else:
    print(f"❌ Error creating price rule: {r.status_code}")
    print(f"   Response: {r.text}")

# ============================================================
# DISCOUNT CODE #2: REVIEW10
# ============================================================

print("\n[2/2] Creating REVIEW10 - Product Review 10% OFF...")
print("-" * 60)

review_data = {
    "price_rule": {
        "title": "REVIEW10 - Product Review 10% OFF",
        "target_type": "line_item",
        "target_selection": "all",  # ALL PRODUCTS
        "allocation_method": "across",
        "value_type": "percentage",
        "value": "-10.0",
        "customer_selection": "all",
        "starts_at": f"{tomorrow}T00:00:00Z",
        "usage_limit": 2000,  # Max 2000 uses
        "once_per_customer": True  # Once per customer
    }
}

r = requests.post(f"{SHOPIFY_API}/price_rules.json",
                  headers=headers,
                  data=json.dumps(review_data))

if r.status_code == 201:
    price_rule_id = r.json()['price_rule']['id']
    print(f"✅ Price rule created: ID {price_rule_id}")

    # Create discount code
    code_data = {
        "discount_code": {
            "code": "REVIEW10"
        }
    }

    r2 = requests.post(f"{SHOPIFY_API}/price_rules/{price_rule_id}/discount_codes.json",
                       headers=headers,
                       data=json.dumps(code_data))

    if r2.status_code == 201:
        print(f"✅ Code REVIEW10 created successfully")
        print(f"   - Value: 10% OFF")
        print(f"   - Applies to: ALL PRODUCTS")
        print(f"   - Usage limit: 2000 total, once per customer")
        print(f"   - Active from: {tomorrow}")
    else:
        print(f"❌ Error creating code: {r2.status_code}")
        print(f"   Response: {r2.text}")
else:
    print(f"❌ Error creating price rule: {r.status_code}")
    print(f"   Response: {r.text}")

print("\n" + "="*60)
print("SUMMARY - DISCOUNT CODES FOR KLAVIYO FLOWS")
print("="*60)
print("\nCodes Created:")
print("  1. WINBACK15: 15% OFF, 1000 uses max, once per customer")
print("     → Flow: Customer Winback - Standard (Email & SMS)")
print("\n  2. REVIEW10: 10% OFF, 2000 uses max, once per customer")
print("     → Flow: Product Review / Cross-Sell - Standard")
print("\nActive From: 2025-11-27")
print("Applies To: ALL PRODUCTS (entire order)")
print("\n✅ Ready for Klaviyo flows deployment!")
print("="*60)
