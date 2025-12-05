#!/usr/bin/env python3
"""
Create test customer to verify Welcome Series Flow
Email will be sent via Shopify Flow (if configured)
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
except FileNotFoundError:
    SHOPIFY_TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

if not SHOPIFY_TOKEN:
    print("❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found")
    exit(1)

API_VERSION = "2025-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query, variables=None):
    """Execute GraphQL query"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    data = response.json()

    if "errors" in data:
        print("❌ GraphQL Errors:")
        for error in data["errors"]:
            print(f"   - {error.get('message', 'Unknown error')}")
        return None

    return data

print("="*80)
print("WELCOME SERIES FLOW - TEST CUSTOMER CREATION")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# Generate unique email for testing
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
test_email = f"test+flow_{timestamp}@alphamedical.shop"

print(f"\n📧 Test Email: {test_email}")
print("   This email will receive:")
print("   - Email 1 (Day 0): Welcome + WELCOME10 code")
print("   - Email 2 (Day 2): How to choose equipment guide")
print("   - Email 3 (Day 5): Featured products showcase")

# Create customer with email marketing consent
create_mutation = """
mutation customerCreate($input: CustomerInput!) {
  customerCreate(input: $input) {
    customer {
      id
      email
      firstName
      lastName
      emailMarketingConsent {
        marketingState
        consentUpdatedAt
      }
      createdAt
    }
    userErrors {
      field
      message
    }
  }
}
"""

variables = {
    "input": {
        "email": test_email,
        "firstName": "Test",
        "lastName": "FlowUser",
        "emailMarketingConsent": {
            "marketingState": "SUBSCRIBED",
            "marketingOptInLevel": "CONFIRMED_OPT_IN"
        }
    }
}

print("\n1. Creating test customer...")
print(f"   Name: Test FlowUser")
print(f"   Email: {test_email}")
print(f"   Marketing Consent: SUBSCRIBED (CONFIRMED_OPT_IN)")

result = graphql_query(create_mutation, variables)

if not result:
    print("❌ Failed to create customer")
    exit(1)

create_result = result["data"]["customerCreate"]
user_errors = create_result.get("userErrors", [])

if user_errors:
    print("\n❌ User Errors:")
    for error in user_errors:
        print(f"   - {error['field']}: {error['message']}")
    exit(1)

customer = create_result["customer"]

print("\n✅ SUCCESS - Test customer created!")
print(f"   ID: {customer['id']}")
print(f"   Email: {customer['email']}")
print(f"   Name: {customer['firstName']} {customer['lastName']}")
print(f"   Marketing State: {customer['emailMarketingConsent']['marketingState']}")
print(f"   Created At: {customer['createdAt']}")

print("\n" + "="*80)
print("NEXT STEPS - MANUAL VERIFICATION")
print("="*80)

print("\n1. CHECK SHOPIFY FLOW (2-5 minutes):")
print(f"   URL: https://admin.shopify.com/store/azffej-as/flow")
print("   - Open 'Welcome Series - Newsletter Automation' workflow")
print("   - Click 'Runs' tab")
print(f"   - Look for run triggered by customer: {customer['email']}")
print("   - Verify status: 'Success' (green checkmark)")

print("\n2. CHECK SHOPIFY EMAIL (2-5 minutes):")
print("   URL: https://admin.shopify.com/store/azffej-as/apps/email/campaigns")
print("   - Check 'Welcome Email 1 - Newsletter' template")
print("   - Look for delivery to test customer")
print("   - Verify delivery status (should be 'Delivered')")

print("\n3. CHECK TEST EMAIL INBOX (5-10 minutes):")
print(f"   Email: {test_email}")
print("   - Gmail: Create label to filter 'test+flow_*@alphamedical.shop'")
print("   - Check spam/junk folder if not in inbox")
print("   - Verify email content:")
print("     ✓ Subject: 'Welcome to Alpha Medical Care...'")
print("     ✓ Personalization: 'Hey Test,' appears")
print("     ✓ WELCOME10 promo code visible")
print("     ✓ Unsubscribe link functional")
print("     ✓ All images load correctly")

print("\n4. MONITOR TIMELINE:")
print(f"   Day 0 ({datetime.now().strftime('%Y-%m-%d %H:%M')}): Email 1 should arrive within 5-10 min")
print(f"   Day 2 (in 48 hours): Email 2 should arrive")
print(f"   Day 5 (in 120 hours): Email 3 should arrive")

print("\n" + "="*80)
print("TROUBLESHOOTING")
print("="*80)

print("\nIf Email 1 does NOT arrive within 10 minutes:")
print("   1. Check Shopify Flow → Workflow Runs for errors")
print("   2. Verify workflow status is 'Active' (green toggle)")
print("   3. Check Shopify Email templates are 'Active' (not Draft)")
print("   4. Verify customer has emailMarketingConsent.marketingState = 'SUBSCRIBED'")
print("   5. Check spam folder in test email inbox")

print("\nIf Workflow NOT triggering:")
print("   1. Go to Shopify Flow → 'Welcome Series' workflow")
print("   2. Verify trigger: 'Customer created' with condition 'Email marketing consent = true'")
print("   3. Check workflow was SAVED after last configuration")
print("   4. Try creating another test customer with different email")

print("\n" + "="*80)
print("TEST CUSTOMER CREATED SUCCESSFULLY")
print("="*80)
print(f"\nMonitor email: {test_email}")
print("Expected first email: Within 5-10 minutes")
print("\n⏱️  Please wait 10 minutes before considering the test failed.")
