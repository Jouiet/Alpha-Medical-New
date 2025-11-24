#!/usr/bin/env python3
"""
Verify current Shopify store state and identify optimization opportunities.
NO modifications - read-only verification.
"""

import os
import json
import sys
from pathlib import Path

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import shopify
except ImportError:
    print("❌ shopify module not installed. Run: pip install ShopifyAPI")
    sys.exit(1)

# Load environment variables
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

# Shopify credentials
API_KEY = os.getenv('SHOPIFY_API_KEY')
API_SECRET = os.getenv('SHOPIFY_API_SECRET')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_API_TOKEN')
STORE_URL = os.getenv('SHOPIFY_STORE_DOMAIN', 'azffej-as.myshopify.com')

if not all([API_KEY, ACCESS_TOKEN]):
    print("❌ Missing Shopify credentials in .env")
    print(f"  API_KEY: {'✅' if API_KEY else '❌'}")
    print(f"  ACCESS_TOKEN: {'✅' if ACCESS_TOKEN else '❌'}")
    sys.exit(1)

# Setup Shopify session
shop_url = f"https://{API_KEY}:{ACCESS_TOKEN}@{STORE_URL}/admin"
shopify.ShopifyResource.set_site(shop_url)

print("🔍 SHOPIFY STORE STATE VERIFICATION\n")
print(f"Store: {STORE_URL}")
print(f"Public URL: https://alphamedical.shop\n")
print("="*60)

# 1. Shop info
try:
    shop = shopify.Shop.current()
    print(f"\n📊 SHOP INFO:")
    print(f"  Name: {shop.name}")
    print(f"  Email: {shop.email}")
    print(f"  Currency: {shop.currency}")
    print(f"  Plan: {shop.plan_name}")
    print(f"  Domain: {shop.domain}")
    print(f"  Customer email: {shop.customer_email}")
except Exception as e:
    print(f"❌ Failed to get shop info: {e}")

# 2. Products count
try:
    products_count = shopify.Product.count()
    print(f"\n📦 PRODUCTS:")
    print(f"  Total: {products_count}")

    # Get first 10 products to check status
    products = shopify.Product.find(limit=10)
    active = sum(1 for p in products if p.status == 'active')
    draft = sum(1 for p in products if p.status == 'draft')
    print(f"  Sample (first 10): {active} active, {draft} draft")
except Exception as e:
    print(f"❌ Failed to get products: {e}")

# 3. Collections count
try:
    collections_count = shopify.CustomCollection.count() + shopify.SmartCollection.count()
    print(f"\n📂 COLLECTIONS:")
    print(f"  Total: {collections_count}")
except Exception as e:
    print(f"❌ Failed to get collections: {e}")

# 4. Customer count & segments
try:
    customers_count = shopify.Customer.count()
    print(f"\n👥 CUSTOMERS:")
    print(f"  Total: {customers_count}")

    # Check if we can access customer segments (requires customer_read scope)
    # Customer segments are NOT directly accessible via REST API - Shopify Admin UI only
    print(f"  Segments: (Manual check required - Shopify Admin UI)")
except Exception as e:
    print(f"❌ Failed to get customers: {e}")

# 5. Installed apps (limited info via API)
try:
    # Note: Full app list requires private app access
    print(f"\n🔌 APPS:")
    print(f"  Loox: (Check manual - app not queryable via API)")
    print(f"  Shopify Flow: (Check manual - native app)")
    print(f"  Shopify Email: (Check manual - native app)")
    print(f"  Infinite Pixels: (Check manual - app not queryable via API)")
except Exception as e:
    print(f"❌ Failed to get apps: {e}")

# 6. Shopify Flow workflows (NOT accessible via API)
print(f"\n🔄 SHOPIFY FLOW:")
print(f"  Status: (Manual check required - no API access)")
print(f"  Workflows created: (Manual check required)")
print(f"  ⚠️  Shopify Flow has NO public API for workflow management")

# 7. Email marketing status
try:
    # Check for customer email consent
    customers = shopify.Customer.find(limit=5)
    consent_count = 0
    for customer in customers:
        if hasattr(customer, 'email_marketing_consent'):
            if customer.email_marketing_consent and customer.email_marketing_consent.state == 'subscribed':
                consent_count += 1

    print(f"\n📧 EMAIL MARKETING:")
    print(f"  Sample consent rate: {consent_count}/{len(customers)} (first 5 customers)")
    print(f"  Klaviyo integration: (External - check Klaviyo dashboard)")
except Exception as e:
    print(f"❌ Failed to check email marketing: {e}")

# 8. Metafields (for loyalty system)
try:
    # Check if store has customer metafields namespace (loyalty points)
    sample_customer = shopify.Customer.find(limit=1)[0] if shopify.Customer.count() > 0 else None
    if sample_customer:
        metafields = sample_customer.metafields()
        loyalty_meta = [m for m in metafields if 'loyalty' in m.namespace.lower()]
        print(f"\n🎁 LOYALTY SYSTEM (Metafields):")
        if loyalty_meta:
            print(f"  ✅ Loyalty metafields detected: {len(loyalty_meta)}")
        else:
            print(f"  ❌ No loyalty metafields found (system not deployed)")
            print(f"  Note: Requires Shopify Plan upgrade for customer metafields API")
except Exception as e:
    print(f"\n🎁 LOYALTY SYSTEM (Metafields):")
    print(f"  ⚠️  Could not check: {e}")

# 9. Subscription products (selling plans)
try:
    # Note: Selling Plans API requires specific scope
    print(f"\n🔁 SUBSCRIPTIONS:")
    print(f"  Native Shopify Subscriptions: (Manual check required)")
    print(f"  ⚠️  Requires 'read_own_subscription_contracts' scope")
except Exception as e:
    print(f"\n🔁 SUBSCRIPTIONS:")
    print(f"  ⚠️  Could not check: {e}")

# 10. Payment providers
try:
    # Note: Payment providers NOT accessible via standard API
    print(f"\n💳 PAYMENT PROVIDERS:")
    print(f"  ⚠️  Payment settings NOT accessible via REST API")
    print(f"  Manual check required: Shopify Admin → Settings → Payments")
    print(f"  Expected: Shopify Payments (Stripe) + Apple Pay + Google Pay")
    print(f"  CRITICAL: Verify PayPal is DISABLED (requirement violation)")
except Exception as e:
    print(f"\n💳 PAYMENT PROVIDERS:")
    print(f"  ❌ Error: {e}")

print("\n" + "="*60)
print("\n✅ VERIFICATION COMPLETE")
print("\n📋 ACTIONABLE ITEMS IDENTIFIED:")
print("  1. Customer segments: Manual creation required (Shopify Admin)")
print("  2. Shopify Flow workflows: Manual configuration required (UI only)")
print("  3. PayPal status: Manual verification required (Settings → Payments)")
print("  4. Loyalty metafields: Requires Shopify Plan upgrade OR tags-based approach")
print("  5. Subscriptions: Native setup requires manual admin configuration")
print("\n⚠️  API LIMITATIONS:")
print("  - Shopify Flow: NO API access (cross-origin iframe limitation)")
print("  - Customer Segments: UI-only creation (API read-only)")
print("  - Payment Providers: NOT accessible via API")
print("  - Apps list: Limited API access")
print("\n💡 RECOMMENDATION:")
print("  Focus on what CAN be automated:")
print("  - Product/Collection optimization via API ✅")
print("  - Customer tagging via API ✅")
print("  - Order processing automation ✅")
print("  - Inventory sync via API ✅")
print("  Accept manual actions for:")
print("  - Shopify Flow configuration (55 min)")
print("  - Customer segments creation (10 min)")
print("  - Payment provider verification (5 min)")
