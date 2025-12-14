#!/usr/bin/env python3
"""
Debug Customer Creation Response - See Exact JSON
"""

import os
import json
import requests
from datetime import datetime

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

API_VERSION = "2025-10"
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("=" * 70)
print("DEBUG: CUSTOMER CREATION RESPONSE")
print("=" * 70)

# Generate unique email
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
test_email = f"test+debug_{timestamp}@alphamedical.shop"

print(f"Creating customer: {test_email}")
print()

# REST API payload
payload = {
    "customer": {
        "first_name": "Debug",
        "last_name": "Customer",
        "email": test_email,
        "email_marketing_consent": {
            "state": "subscribed",
            "opt_in_level": "confirmed_opt_in"
        },
        "tags": "debug-test"
    }
}

# POST to REST API
response = requests.post(
    f"{REST_URL}/customers.json",
    headers=HEADERS,
    json=payload
)

print(f"Status Code: {response.status_code}")
print()

if response.status_code not in [200, 201]:
    print(f"❌ Error:")
    print(response.text)
    exit(1)

print("=" * 70)
print("FULL JSON RESPONSE")
print("=" * 70)
result = response.json()
print(json.dumps(result, indent=2))
print()

print("=" * 70)
print("CUSTOMER OBJECT KEYS")
print("=" * 70)
if 'customer' in result:
    print(f"Keys: {list(result['customer'].keys())}")
else:
    print("No 'customer' key in response")

print("=" * 70)
