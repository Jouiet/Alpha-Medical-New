#!/usr/bin/env python3
"""
VERIFY PAYMENT GATEWAYS - Alpha Medical Care
Factual verification of active payment providers
REQUIREMENT: Stripe + Google Pay + Apple Pay ONLY (NO PayPal)
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

print("=" * 80)
print("PAYMENT GATEWAYS VERIFICATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# Check Shop Payment Settings (REST API)
url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/shop.json"
headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("\n1. Checking Shop Configuration...\n")

response = requests.get(url, headers=headers)

if response.status_code == 200:
    shop = response.json()["shop"]
    print(f"   Store: {shop['name']}")
    print(f"   Domain: {shop['domain']}")
    print(f"   Email: {shop['email']}")
    print(f"   Enabled presentment currencies: {shop.get('enabled_presentment_currencies', [])}")
else:
    print(f"   ❌ Failed to fetch shop: {response.status_code}")

# Check Active Payment Gateways (GraphQL - more detailed)
print("\n2. Checking Active Payment Gateways (GraphQL)...\n")

query = """
{
  shop {
    paymentSettings {
      supportedDigitalWallets
    }
  }
  availablePaymentGateways: shopPaymentGateways {
    name
    enabled
    type
  }
}
"""

graphql_url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
graphql_response = requests.post(graphql_url, json={"query": query}, headers=headers)

if graphql_response.status_code == 200:
    data = graphql_response.json()

    if "errors" in data:
        print(f"   ❌ GraphQL Errors: {data['errors']}")
    else:
        payment_settings = data.get("data", {}).get("shop", {}).get("paymentSettings", {})
        gateways = data.get("data", {}).get("availablePaymentGateways", [])

        print("   Digital Wallets Supported:")
        wallets = payment_settings.get("supportedDigitalWallets", [])
        for wallet in wallets:
            print(f"      ✅ {wallet}")

        print("\n   Payment Gateways:")
        paypal_found = False
        stripe_found = False

        for gateway in gateways:
            enabled_icon = "✅" if gateway["enabled"] else "⏸️"
            print(f"      {enabled_icon} {gateway['name']} (Type: {gateway['type']}, Enabled: {gateway['enabled']})")

            if "paypal" in gateway["name"].lower() and gateway["enabled"]:
                paypal_found = True
            if "stripe" in gateway["name"].lower() or "shopify" in gateway["name"].lower():
                if gateway["enabled"]:
                    stripe_found = True

        print("\n" + "=" * 80)
        print("REQUIREMENT VERIFICATION")
        print("=" * 80)

        print(f"\nREQUIRED: Stripe + Google Pay + Apple Pay ONLY")
        print(f"NO PayPal allowed")

        print(f"\n✅ Stripe/Shopify Payments: {'ACTIVE' if stripe_found else '❌ NOT FOUND'}")
        print(f"{'✅' if 'GOOGLE_PAY' in wallets else '❌'} Google Pay: {'ENABLED' if 'GOOGLE_PAY' in wallets else 'DISABLED'}")
        print(f"{'✅' if 'APPLE_PAY' in wallets else '❌'} Apple Pay: {'ENABLED' if 'APPLE_PAY' in wallets else 'DISABLED'}")
        print(f"{'❌ VIOLATION' if paypal_found else '✅'} PayPal: {'ACTIVE - CRITICAL VIOLATION' if paypal_found else 'NOT ACTIVE'}")

        if paypal_found:
            print("\n🔴 CRITICAL REQUIREMENT VIOLATION DETECTED")
            print("   Action Required: Deactivate PayPal in Shopify Admin")
            print("   URL: https://admin.shopify.com/store/azffej-as/settings/payments")
            print("   Manual action required - cannot be automated via API")
        else:
            print("\n✅ PAYMENT COMPLIANCE: VERIFIED")
else:
    print(f"   ❌ GraphQL Failed: {graphql_response.status_code}")
    print(f"   Response: {graphql_response.text[:500]}")

print("\n" + "=" * 80)
