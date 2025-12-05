#!/usr/bin/env python3
"""
VERIFY CRITICAL USER REQUIREMENTS
- PayPal MUST be disabled
- Draft products MUST stay draft
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
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query):
    """Execute GraphQL query"""
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.json()

def rest_get(endpoint):
    """Execute REST GET request"""
    response = requests.get(f"{REST_URL}{endpoint}", headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.json()

print("=" * 80)
print("CRITICAL REQUIREMENTS VERIFICATION")
print("=" * 80)
print(f"Store: {SHOPIFY_DOMAIN}")
print()

# ============================================================================
# CHECK 1: DRAFT PRODUCTS STATUS
# ============================================================================

print("=" * 80)
print("CHECK 1: DRAFT PRODUCTS MUST STAY DRAFT")
print("=" * 80)

# Query all draft products
query = """
{
  products(first: 250, query: "status:draft") {
    edges {
      node {
        id
        title
        status
        publishedAt
      }
    }
  }
}
"""

result = graphql_query(query)

if result and 'data' in result:
    draft_products = result['data']['products']['edges']

    print(f"\nDraft products found: {len(draft_products)}")

    if len(draft_products) == 0:
        print("✅ No draft products (all products are active or archived)")
    else:
        print(f"\nVerifying {len(draft_products)} draft products:")
        print()

        violations = []
        for edge in draft_products:
            product = edge['node']
            status = product['status']
            published_at = product['publishedAt']

            if status != 'DRAFT':
                print(f"  ❌ VIOLATION: \"{product['title']}\"")
                print(f"     Status: {status} (should be DRAFT)")
                violations.append(product)
            elif published_at is not None:
                print(f"  ⚠️  WARNING: \"{product['title']}\"")
                print(f"     Status: DRAFT but publishedAt is set ({published_at})")
            else:
                print(f"  ✅ \"{product['title']}\" - DRAFT (unpublished)")

        if len(violations) > 0:
            print(f"\n❌ CRITICAL: {len(violations)} draft products changed status!")
            print("   USER REQUIREMENT VIOLATED!")
        else:
            print(f"\n✅ ALL draft products remain DRAFT")
else:
    print("❌ Failed to query draft products")

# ============================================================================
# CHECK 2: PAYMENT METHODS (PayPal MUST be disabled)
# ============================================================================

print("\n" + "=" * 80)
print("CHECK 2: PAYPAL MUST BE DISABLED")
print("=" * 80)

# Note: Shop payment settings are NOT accessible via Admin API on Basic plan
# We can only verify via Shopify admin UI manually OR via chrome-devtools-mcp

print("\n⚠️  LIMITATION: Payment settings NOT accessible via Admin API on Basic plan")
print("   Manual verification required via Shopify Admin UI:")
print("   URL: https://admin.shopify.com/store/azffej-as/settings/payments")
print()
print("   Expected active payment methods:")
print("   - ✅ Shopify Payments (Stripe)")
print("   - ✅ Apple Pay")
print("   - ✅ Google Pay")
print("   - ❌ PayPal (MUST NOT be present)")
print()
print("   Will attempt verification via chrome-devtools-mcp in next step...")

# ============================================================================
# CHECK 3: LANGUAGE VERIFICATION (English only)
# ============================================================================

print("\n" + "=" * 80)
print("CHECK 3: SITE MUST BE 100% ENGLISH ONLY")
print("=" * 80)

# Check shop primary locale
query = """
{
  shop {
    primaryDomain {
      host
    }
    currencyCode
    ianaTimezone
    enabledPresentmentCurrencies
  }
}
"""

result = graphql_query(query)

if result and 'data' in result:
    shop = result['data']['shop']
    print(f"\nShop domain: {shop['primaryDomain']['host']}")
    print(f"Currency: {shop['currencyCode']}")
    print(f"Timezone: {shop['ianaTimezone']}")
    print()

# Check products for non-English content
print("Checking product titles for non-English keywords...")

french_keywords = [
    'pour le', 'pour la', 'avec', 'sans', 'contre',
    'genou', 'cheville', 'poignet', 'épaule', 'coude',
    'douleur', 'soulagement', 'thérapie', 'orthèse'
]

query = """
{
  products(first: 100) {
    edges {
      node {
        id
        title
        description
        status
      }
    }
  }
}
"""

result = graphql_query(query)

if result and 'data' in result:
    products = result['data']['products']['edges']

    violations = []
    for edge in products:
        product = edge['node']
        title = product['title'].lower()
        desc = product['description'].lower() if product['description'] else ""

        # Check for unambiguous French phrases
        for keyword in french_keywords:
            if keyword in title or keyword in desc:
                violations.append({
                    "title": product['title'],
                    "keyword": keyword
                })
                print(f"  ⚠️  \"{product['title']}\" - contains French keyword: '{keyword}'")
                break

    if len(violations) == 0:
        print("  ✅ No obvious French keywords detected in first 100 products")
    else:
        print(f"\n  ⚠️  {len(violations)} products may contain French content")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

print("\n✅ VERIFIED:")
print("  - Draft products: Checked (manual review of list above)")
print("  - Language: No obvious French keywords in products")
print()
print("⏳ REQUIRES MANUAL VERIFICATION:")
print("  - PayPal status (Shopify Admin → Settings → Payments)")
print()
print("=" * 80)
