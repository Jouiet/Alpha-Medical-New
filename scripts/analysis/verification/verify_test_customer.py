#!/usr/bin/env python3
"""
Verify Test Customer Created for Shopify Flow
"""

import os
import json
import requests

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
print("VERIFY TEST CUSTOMER")
print("=" * 70)

# Query customer by ID
query = """
{
  customer(id: "gid://shopify/Customer/8044321603661") {
    id
    email
    firstName
    lastName
    createdAt
    emailMarketingConsent {
      marketingState
      marketingOptInLevel
      consentUpdatedAt
    }
    tags
    state
  }
}
"""

result = graphql_query(query)

if not result or 'data' not in result:
    print("❌ Query failed")
    exit(1)

customer = result['data']['customer']

if not customer:
    print("❌ Customer not found")
    exit(1)

print("✅ Customer verified!")
print()
print(f"ID: {customer['id']}")
print(f"Email: {customer['email']}")
print(f"Name: {customer['firstName']} {customer['lastName']}")
print(f"Created: {customer['createdAt']}")
print(f"State: {customer['state']}")
print(f"Tags: {customer['tags']}")
print(f"Marketing State: {customer['emailMarketingConsent']['marketingState']}")
print(f"Opt-In Level: {customer['emailMarketingConsent']['marketingOptInLevel']}")
print(f"Consent Updated: {customer['emailMarketingConsent']['consentUpdatedAt']}")
print()

print("=" * 70)
print("SHOPIFY FLOW TRIGGER STATUS")
print("=" * 70)
print("✅ Customer created: Yes")
print(f"✅ Email marketing consent: {customer['emailMarketingConsent']['marketingState']}")
print(f"✅ Opt-in level: {customer['emailMarketingConsent']['marketingOptInLevel']}")
print()

if customer['emailMarketingConsent']['marketingState'] == 'SUBSCRIBED':
    print("✅ Workflow SHOULD trigger (all conditions met)")
    print()
    print("Next steps:")
    print(f"1. Check inbox: {customer['email']}")
    print("2. Wait 2-5 minutes for Email 1")
    print("3. Verify Shopify Flow runs tab")
else:
    print("❌ Workflow will NOT trigger (marketing consent not SUBSCRIBED)")

print("=" * 70)
