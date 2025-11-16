#!/usr/bin/env python3
"""
Create Test Customer for Shopify Flow Welcome Series
Validates: Email workflow triggers correctly
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
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query):
    """Execute GraphQL query/mutation"""
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ GraphQL Error: {response.status_code}")
        print(response.text)
        return None
    return response.json()

print("=" * 70)
print("SHOPIFY FLOW - TEST CUSTOMER CREATION")
print("=" * 70)
print(f"Store: {SHOPIFY_DOMAIN}")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Generate unique email with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
test_email = f"test+flow_{timestamp}@alphamedical.shop"

print(f"Creating test customer: {test_email}")
print()

# GraphQL mutation to create customer
mutation = f"""
mutation {{
  customerCreate(input: {{
    email: "{test_email}"
    firstName: "FlowTest"
    lastName: "Customer"
    emailMarketingConsent: {{
      marketingState: SUBSCRIBED
      marketingOptInLevel: CONFIRMED_OPT_IN
    }}
  }}) {{
    customer {{
      id
      email
      firstName
      lastName
      createdAt
      emailMarketingConsent {{
        marketingState
        marketingOptInLevel
      }}
    }}
    userErrors {{
      field
      message
    }}
  }}
}}
"""

result = graphql_query(mutation)

if not result or 'data' not in result:
    print("❌ Mutation failed")
    exit(1)

user_errors = result['data']['customerCreate']['userErrors']
customer = result['data']['customerCreate']['customer']

if len(user_errors) > 0:
    print(f"❌ Errors:")
    for error in user_errors:
        print(f"   - {error['field']}: {error['message']}")
    exit(1)

if not customer:
    print("❌ Customer not created")
    exit(1)

print("✅ Test customer created successfully!")
print()
print("=" * 70)
print("CUSTOMER DETAILS")
print("=" * 70)
print(f"ID: {customer['id']}")
print(f"Email: {customer['email']}")
print(f"Name: {customer['firstName']} {customer['lastName']}")
print(f"Created: {customer['createdAt']}")
print(f"Marketing Consent: {customer['emailMarketingConsent']['marketingState']}")
print(f"Opt-In Level: {customer['emailMarketingConsent']['marketingOptInLevel']}")
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
print(f"1. Check inbox: {test_email}")
print("   - Wait 2-5 minutes for Email 1")
print("   - Subject: 'Welcome to Alpha Medical Care...'")
print("   - Personalization: 'Hey FlowTest,' should appear")
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
print(f"   - Check {test_email} for Email 2")
print("   - Subject: 'How to Choose the Right Medical Equipment...'")
print()
print("5. Day 5 Verification (2025-11-21):")
print(f"   - Check {test_email} for Email 3")
print("   - Subject: 'This Week's Featured Medical Equipment...'")
print()

print("=" * 70)
print("STATUS")
print("=" * 70)
print("✅ Test customer created")
print("⏳ Waiting for Email 1 delivery (2-5 minutes)")
print("⏳ Waiting for Email 2 (Day 2)")
print("⏳ Waiting for Email 3 (Day 5)")
print()
print("🔴 CRITICAL: Check inbox within 10 minutes to verify workflow!")
print("=" * 70)
