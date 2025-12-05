#!/usr/bin/env python3
"""
VERIFY FLOW EXECUTION - Alpha Medical Care
Check if Welcome Series Flow executed for test customer
"""

import requests
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

print("=" * 80)
print("FLOW EXECUTION VERIFICATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# Check test customer
TEST_CUSTOMER_ID = 8032261505101
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/customers/{TEST_CUSTOMER_ID}.json"
headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print(f"\n1. Checking test customer (ID: {TEST_CUSTOMER_ID})...\n")

response = requests.get(url, headers=headers)

if response.status_code == 200:
    customer = response.json()['customer']
    print(f"   ✅ Customer found")
    print(f"   Email: {customer['email']}")
    print(f"   Name: {customer['first_name']} {customer['last_name']}")
    print(f"   Created: {customer['created_at']}")
    print(f"   Marketing consent: {customer.get('email_marketing_consent', {}).get('state', 'unknown')}")
    print(f"   Orders count: {customer['orders_count']}")
else:
    print(f"   ❌ Failed to fetch customer: {response.status_code}")
    exit(1)

# Check marketing activities (emails sent)
print(f"\n2. Checking marketing activities...\n")

# Note: Shopify Flow doesn't have a public API to check workflow runs
# We can check Shopify Email campaigns sent instead

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/marketing_events.json"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    events = response.json().get('marketing_events', [])
    print(f"   Total marketing events: {len(events)}")

    if events:
        for event in events[:5]:
            print(f"\n   Event: {event.get('event_type', 'unknown')}")
            print(f"   Started: {event.get('started_at', 'N/A')}")
            print(f"   Status: {event.get('status', 'N/A')}")
    else:
        print("   No marketing events found")
else:
    print(f"   ⚠️ Failed to fetch marketing events: {response.status_code}")

print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

print(f"\n✅ Test Customer: EXISTS")
print(f"✅ Marketing Consent: {customer.get('email_marketing_consent', {}).get('state', 'unknown')}")

print(f"\n⚠️ LIMITATION:")
print(f"   Shopify Flow runs cannot be verified via API")
print(f"   Manual verification required in Shopify Admin:")
print(f"   URL: https://admin.shopify.com/store/azffej-as/flow")
print(f"   Action: Check 'Welcome Series - Newsletter Automation' → Runs tab")

print(f"\n⚠️ EMAIL VERIFICATION:")
print(f"   Manual inbox check required:")
print(f"   Email: test+flow_20251111090105@alphamedical.shop")
print(f"   Expected: Welcome email within 2-5 minutes of customer creation")
print(f"   Time elapsed: {(datetime.now().timestamp() - datetime.fromisoformat(customer['created_at'].replace('Z', '+00:00')).timestamp()) / 3600:.1f} hours")

print("\n" + "=" * 80)
