#!/usr/bin/env python3
"""
CREATE TEST CUSTOMER FOR FLOW VALIDATION - Alpha Medical
Test Welcome Series - Newsletter Automation workflow
"""

import requests
import json
from datetime import datetime

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

print("="*80)
print("CREATE TEST CUSTOMER FOR FLOW VALIDATION")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/customers.json"
headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# Test email with timestamp to ensure uniqueness
test_email = f"test+flow_{datetime.now().strftime('%Y%m%d%H%M%S')}@alphamedical.shop"

payload = {
    "customer": {
        "first_name": "Test",
        "last_name": "FlowCustomer",
        "email": test_email,
        "email_marketing_consent": {
            "state": "subscribed",
            "opt_in_level": "confirmed_opt_in"
        },
        "accepts_marketing": True,
        "tags": "test-customer, flow-validation"
    }
}

print(f"\n📝 Creating test customer:")
print(f"   Email: {test_email}")
print(f"   Name: Test FlowCustomer")
print(f"   Marketing Consent: subscribed")

try:
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in [200, 201]:
        customer = response.json().get("customer", {})
        print(f"\n✅ SUCCESS - Test customer created")
        print(f"   Customer ID: {customer.get('id')}")
        print(f"   Email: {customer.get('email')}")
        print(f"   Marketing consent: {customer.get('email_marketing_consent', {}).get('state')}")
        print(f"   Created at: {customer.get('created_at')}")

        print(f"\n🎯 NEXT STEPS:")
        print(f"1. Check inbox: {test_email}")
        print(f"2. Email 1 should arrive within 2-5 minutes")
        print(f"3. Verify subject: 'Welcome to Alpha Medical Care...'")
        print(f"4. Check personalization: 'Hey Test,' appears")
        print(f"5. Verify WELCOME10 code present")

        print(f"\n📋 Flow Timeline:")
        print(f"   Day 0 (Now): Email 1 - Welcome")
        print(f"   Day 2 ({(datetime.now().timestamp() + 2*24*3600):.0f}): Email 2 - How It Works")
        print(f"   Day 5 ({(datetime.now().timestamp() + 5*24*3600):.0f}): Email 3 - Featured Products")

        print(f"\n⏰ Monitor Flow Runs:")
        print(f"   URL: https://admin.shopify.com/store/azffej-as/flow")
        print(f"   Check 'Welcome Series - Newsletter Automation' workflow")
        print(f"   Click 'Runs' tab to see execution logs")

    else:
        print(f"\n❌ FAILED - Status {response.status_code}")
        print(f"   Response: {response.text[:500]}")

except Exception as e:
    print(f"\n❌ Exception: {e}")

print("\n" + "="*80)
