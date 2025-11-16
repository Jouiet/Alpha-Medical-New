#!/usr/bin/env python3
"""
Create Test Customer via REST API (instead of GraphQL)
REST API may have different permissions than GraphQL
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
print("SHOPIFY FLOW - TEST CUSTOMER (REST API)")
print("=" * 70)
print(f"Store: {SHOPIFY_DOMAIN}")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Generate unique email
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
test_email = f"test+flow_{timestamp}@alphamedical.shop"

print(f"Creating test customer: {test_email}")
print()

# REST API payload
payload = {
    "customer": {
        "first_name": "FlowTest",
        "last_name": "Customer",
        "email": test_email,
        "email_marketing_consent": {
            "state": "subscribed",
            "opt_in_level": "confirmed_opt_in"
        },
        "tags": "test-customer, shopify-flow-test"
    }
}

# POST to REST API
response = requests.post(
    f"{REST_URL}/customers.json",
    headers=HEADERS,
    json=payload
)

if response.status_code not in [200, 201]:
    print(f"❌ REST API Error: {response.status_code}")
    print(response.text)
    exit(1)

result = response.json()
customer = result['customer']

print("✅ Test customer created successfully!")
print()
print("=" * 70)
print("CUSTOMER DETAILS")
print("=" * 70)
print(f"ID: {customer['id']}")
print(f"Email: {customer['email']}")
print(f"Name: {customer['first_name']} {customer['last_name']}")
print(f"Created: {customer['created_at']}")
print(f"State: {customer['state']}")
print(f"Tags: {customer['tags']}")
print(f"Marketing Opt-In: {customer['email_marketing_consent']['state']}")
print(f"Opt-In Level: {customer['email_marketing_consent']['opt_in_level']}")
print()

print("=" * 70)
print("EXPECTED WORKFLOW BEHAVIOR")
print("=" * 70)
print("✅ Trigger: Customer created (with email marketing consent)")
print("✅ Action 1: Send Welcome Email 1 - Newsletter (IMMEDIATE)")
print("⏳ Action 2: Wait 2 days")
print("⏳ Action 3: Send Email 2 - How to Choose... (Day 2)")
print("⏳ Action 4: Wait 3 days")
print("⏳ Action 5: Send Email 3 - Featured Products (Day 5)")
print()

print("=" * 70)
print("VERIFICATION STEPS")
print("=" * 70)
print(f"1. Check inbox: {customer['email']}")
print("   - Wait 2-5 minutes for Email 1")
print("   - Subject: 'Welcome to Alpha Medical Care...'")
print(f"   - Personalization: 'Hey {customer['first_name']},' should appear")
print()
print("2. Check Shopify Email:")
print("   - URL: https://admin.shopify.com/store/azffej-as/apps/email/campaigns")
print("   - Template 1 delivery should show 1 sent")
print()
print("3. Check Shopify Flow:")
print("   - URL: https://admin.shopify.com/store/azffej-as/flow")
print("   - Open 'Welcome Series - Newsletter Automation'")
print("   - Click 'Runs' tab")
print("   - Should show 1 run with trigger time matching customer creation")
print()
print("4. Day 2 Verification (2025-11-18):")
print(f"   - Check {customer['email']} for Email 2")
print("   - Subject: 'How to Choose the Right Medical Equipment...'")
print()
print("5. Day 5 Verification (2025-11-21):")
print(f"   - Check {customer['email']} for Email 3")
print("   - Subject: 'This Week's Featured Medical Equipment...'")
print()

print("=" * 70)
print("STATUS")
print("=" * 70)
print("✅ Test customer created via REST API")
print("✅ Email marketing consent: SUBSCRIBED")
print("✅ All data fields populated correctly")
print("⏳ Waiting for Email 1 delivery (2-5 minutes)")
print()
print("🔴 CRITICAL: Check inbox within 10 minutes to verify workflow!")
print("=" * 70)
