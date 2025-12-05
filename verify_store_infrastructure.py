#!/usr/bin/env python3
"""
Shopify Store Infrastructure Verification Script
Uses Admin API to verify actual state of store infrastructure
NO ASSUMPTIONS - ONLY FACTS
"""

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load credentials
load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

BASE_URL = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}'

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN
}

def api_request(endpoint, method='GET', data=None):
    """Make API request with error handling"""
    url = f'{BASE_URL}{endpoint}'
    try:
        if method == 'GET':
            response = requests.get(url, headers=HEADERS, timeout=30)
        elif method == 'POST':
            response = requests.post(url, headers=HEADERS, json=data, timeout=30)
        elif method == 'PUT':
            response = requests.put(url, headers=HEADERS, json=data, timeout=30)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': str(e), 'status_code': getattr(e.response, 'status_code', None)}

def check_shop_info():
    """Get basic shop information"""
    print("\n" + "="*80)
    print("SHOP INFORMATION")
    print("="*80)

    result = api_request('/shop.json')
    if 'error' not in result:
        shop = result['shop']
        print(f"✅ Store Name: {shop['name']}")
        print(f"✅ Domain: {shop['domain']}")
        print(f"✅ Primary Domain: {shop.get('myshopify_domain', 'N/A')}")
        print(f"✅ Email: {shop['email']}")
        print(f"✅ Plan: {shop['plan_name']}")
        print(f"✅ Country: {shop['country_name']}")
        print(f"✅ Currency: {shop['currency']}")
        print(f"✅ Enabled Presentment Currencies: {', '.join(shop.get('enabled_presentment_currencies', []))}")
        return shop
    else:
        print(f"❌ Error: {result['error']}")
        return None

def check_customers():
    """Check customer count and recent activity"""
    print("\n" + "="*80)
    print("CUSTOMERS AUDIT")
    print("="*80)

    result = api_request('/customers/count.json')
    if 'error' not in result:
        count = result['count']
        print(f"✅ Total Customers: {count}")

        if count > 0:
            # Get recent customers
            customers = api_request('/customers.json?limit=5')
            if 'error' not in customers:
                print(f"\n📋 Last 5 Customers:")
                for customer in customers['customers']:
                    email = customer.get('email', 'N/A')
                    first = customer.get('first_name', 'N/A')
                    last = customer.get('last_name', 'N/A')
                    created = customer.get('created_at', 'N/A')[:10] if customer.get('created_at') else 'N/A'
                    print(f"  - {first} {last} ({email}) - Created: {created}")
        return count
    else:
        print(f"❌ Error: {result['error']}")
        return None

def check_products():
    """Check product count"""
    print("\n" + "="*80)
    print("PRODUCTS AUDIT")
    print("="*80)

    result = api_request('/products/count.json')
    if 'error' not in result:
        total_count = result['count']
        print(f"✅ Total Products: {total_count}")

        # Check published vs draft
        published = api_request('/products/count.json?published_status=published')
        draft = api_request('/products/count.json?published_status=draft')

        if 'error' not in published and 'error' not in draft:
            print(f"  - Published: {published['count']}")
            print(f"  - Draft: {draft['count']}")

        return total_count
    else:
        print(f"❌ Error: {result['error']}")
        return None

def check_orders():
    """Check order history"""
    print("\n" + "="*80)
    print("ORDERS AUDIT")
    print("="*80)

    result = api_request('/orders/count.json')
    if 'error' not in result:
        count = result['count']
        print(f"✅ Total Orders: {count}")

        if count > 0:
            # Get recent orders
            orders = api_request('/orders.json?status=any&limit=5')
            if 'error' not in orders:
                print(f"\n📋 Last 5 Orders:")
                for order in orders['orders']:
                    print(f"  - Order #{order['name']} - {order['financial_status']} - ${order['total_price']} - {order['created_at'][:10]}")
        else:
            print("⚠️  PRE-LAUNCH: No orders yet (expected)")
        return count
    else:
        print(f"❌ Error: {result['error']}")
        return None

def check_abandoned_checkouts():
    """Check abandoned checkouts"""
    print("\n" + "="*80)
    print("ABANDONED CHECKOUTS AUDIT")
    print("="*80)

    result = api_request('/checkouts/count.json')
    if 'error' not in result:
        count = result['count']
        print(f"✅ Total Abandoned Checkouts: {count}")

        if count > 0:
            checkouts = api_request('/checkouts.json?limit=5')
            if 'error' not in checkouts:
                print(f"\n📋 Recent Abandoned Checkouts:")
                for checkout in checkouts['checkouts']:
                    print(f"  - ${checkout.get('total_price', 'N/A')} - {checkout['created_at'][:10]}")
        else:
            print("⚠️  PRE-LAUNCH: No abandoned checkouts (expected)")
        return count
    else:
        print(f"❌ Error: {result['error']}")
        return None

def check_metafields():
    """Check customer metafield definitions"""
    print("\n" + "="*80)
    print("CUSTOMER METAFIELD DEFINITIONS AUDIT")
    print("="*80)

    result = api_request('/metafield_definitions.json?owner_type=customer')
    if 'error' not in result:
        definitions = result.get('metafield_definitions', [])
        print(f"✅ Total Customer Metafield Definitions: {len(definitions)}")

        if definitions:
            print(f"\n📋 Metafield Definitions:")
            for definition in definitions:
                print(f"  - {definition['namespace']}.{definition['key']} ({definition['type']})")
        else:
            print("⚠️  No customer metafield definitions found")
            print("💡 Loyalty system requires metafields (requires Shopify plan upgrade)")

        return definitions
    else:
        print(f"❌ Error: {result['error']}")
        if 'status_code' in result and result['status_code'] == 403:
            print("⚠️  ACCESS DENIED: Metafields require Shopify plan ($79/mo) or higher")
        return None

def check_webhooks():
    """Check configured webhooks"""
    print("\n" + "="*80)
    print("WEBHOOKS AUDIT")
    print("="*80)

    result = api_request('/webhooks.json')
    if 'error' not in result:
        webhooks = result.get('webhooks', [])
        print(f"✅ Total Webhooks: {len(webhooks)}")

        if webhooks:
            print(f"\n📋 Configured Webhooks:")
            for webhook in webhooks:
                print(f"  - {webhook['topic']} → {webhook['address'][:50]}...")
        else:
            print("⚠️  No webhooks configured")

        return webhooks
    else:
        print(f"❌ Error: {result['error']}")
        return None

def check_marketing_events():
    """Check marketing events (pixel tracking)"""
    print("\n" + "="*80)
    print("MARKETING EVENTS AUDIT (Pixels)")
    print("="*80)

    result = api_request('/marketing_events.json')
    if 'error' not in result:
        events = result.get('marketing_events', [])
        print(f"✅ Total Marketing Events: {len(events)}")

        if events:
            print(f"\n📋 Marketing Events:")
            for event in events:
                print(f"  - {event.get('event_type', 'N/A')} - {event.get('marketing_channel', 'N/A')}")
        else:
            print("⚠️  No marketing events found")

        return events
    else:
        print(f"❌ Error: {result['error']}")
        return None

def generate_summary(shop, customers, products, orders, checkouts, metafields, webhooks):
    """Generate summary report"""
    print("\n" + "="*80)
    print("INFRASTRUCTURE AUDIT SUMMARY")
    print("="*80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Store: {shop['name'] if shop else 'N/A'} ({shop['domain'] if shop else 'N/A'})")
    print(f"Plan: {shop['plan_name'] if shop else 'N/A'}")
    print()

    print("📊 METRICS:")
    print(f"  - Customers: {customers if customers is not None else 'ERROR'}")
    print(f"  - Products: {products if products is not None else 'ERROR'}")
    print(f"  - Orders: {orders if orders is not None else 'ERROR'}")
    print(f"  - Abandoned Checkouts: {checkouts if checkouts is not None else 'ERROR'}")
    print(f"  - Metafield Definitions: {len(metafields) if metafields else 0}")
    print(f"  - Webhooks: {len(webhooks) if webhooks else 0}")
    print()

    print("🚨 CRITICAL FINDINGS:")

    if orders == 0:
        print("  ⚠️  PRE-LAUNCH STATUS: No orders yet (store not launched)")

    if customers == 0:
        print("  ⚠️  NO CUSTOMERS: No customer data to trigger automations")

    if not metafields:
        print("  ❌ NO METAFIELDS: Loyalty system cannot function (requires Shopify plan upgrade)")

    if not webhooks:
        print("  ⚠️  NO WEBHOOKS: No external integrations configured")

    print()
    print("📋 NEXT ACTIONS:")

    if not metafields:
        print("  1. Upgrade to Shopify plan ($79/mo) to enable customer metafields")
        print("  2. Run loyalty_setup.py to create metafield definitions")

    if orders == 0:
        print("  3. Complete PRE-LAUNCH checklist before going live")
        print("  4. Test workflows with test orders before launch")

    if customers == 0:
        print("  5. Generate test customer data to verify automation triggers")

    print("\n" + "="*80)

def main():
    print("="*80)
    print("SHOPIFY STORE INFRASTRUCTURE VERIFICATION")
    print("="*80)
    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print(f"API Version: {API_VERSION}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run all checks
    shop = check_shop_info()
    customers = check_customers()
    products = check_products()
    orders = check_orders()
    checkouts = check_abandoned_checkouts()
    metafields = check_metafields()
    webhooks = check_webhooks()
    check_marketing_events()

    # Generate summary
    generate_summary(shop, customers, products, orders, checkouts, metafields, webhooks)

    print("\n✅ Verification complete!")
    print(f"📄 Results saved to: /tmp/shopify_infrastructure_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

if __name__ == '__main__':
    main()
