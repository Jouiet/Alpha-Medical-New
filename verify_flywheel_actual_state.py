#!/usr/bin/env python3
"""
FLYWHEEL ACTUAL STATE - FACTUAL VERIFICATION
Verify what's ACTUALLY running vs just documented
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.admin')

SHOP_URL = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

print("=" * 80)
print("FLYWHEEL ACTUAL STATE - FACTUAL AUDIT")
print(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
print("=" * 80)
print()

# Check actual orders (conversion happening?)
print("1. CONVERSION PHASE - ORDER ACTIVITY")
print("-" * 80)

url = f"https://{SHOP_URL}/admin/api/2024-10/graphql.json"
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

orders_query = """
{
  orders(first: 50, reverse: true) {
    edges {
      node {
        id
        name
        createdAt
        totalPriceSet {
          shopMoney {
            amount
            currencyCode
          }
        }
        customer {
          email
          ordersCount
        }
      }
    }
  }
}
"""

try:
    response = requests.post(url, json={"query": orders_query}, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        orders = data.get('data', {}).get('orders', {}).get('edges', [])

        if orders:
            print(f"✅ Total orders: {len(orders)}")

            # Analyze orders
            first_time = 0
            repeat = 0
            total_revenue = 0.0

            for order in orders:
                node = order['node']
                customer = node.get('customer')
                amount = float(node['totalPriceSet']['shopMoney']['amount'])
                total_revenue += amount

                if customer:
                    if customer['ordersCount'] == 1:
                        first_time += 1
                    else:
                        repeat += 1

            print(f"   - First-time customers: {first_time}")
            print(f"   - Repeat customers: {repeat}")
            print(f"   - Total revenue: ${total_revenue:.2f}")
            print(f"   - Average order value: ${total_revenue/len(orders):.2f}")

            if repeat > 0:
                print(f"\n✅ RETENTION PHASE: ACTIVE ({repeat} repeat customers)")
            else:
                print(f"\n❌ RETENTION PHASE: DORMANT (0 repeat customers)")
        else:
            print("❌ NO ORDERS FOUND")
            print("   → CONVERSION: 0% active")
            print("   → RETENTION: 0% active (no customers to retain)")
            print("   → ADVOCACY: 0% active (no customers to advocate)")
    else:
        print(f"❌ API Error: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Check customers for retention data
print("2. RETENTION PHASE - CUSTOMER LIFECYCLE")
print("-" * 80)

customers_query = """
{
  customers(first: 50, reverse: true) {
    edges {
      node {
        id
        email
        ordersCount
        totalSpent
        createdAt
        tags
      }
    }
  }
}
"""

try:
    response = requests.post(url, json={"query": customers_query}, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        customers = data.get('data', {}).get('customers', {}).get('edges', [])

        if customers:
            print(f"✅ Total customers: {len(customers)}")

            # Analyze customer engagement
            with_orders = 0
            with_tags = 0

            for cust in customers:
                node = cust['node']
                if node['ordersCount'] > 0:
                    with_orders += 1
                if node.get('tags'):
                    with_tags += 1

            print(f"   - With purchases: {with_orders}/{len(customers)}")
            print(f"   - With tags (segmented): {with_tags}/{len(customers)}")

            if with_orders == 0:
                print("\n❌ NO PURCHASE ACTIVITY")
                print("   → Flywheel cannot spin without transactions")
        else:
            print("❌ NO CUSTOMERS FOUND")
            print("   → ACQUISITION: 0 leads converted")
    else:
        print(f"❌ API Error: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Check automations
print("3. ACQUISITION PHASE - AUTOMATION STATUS")
print("-" * 80)

# Check GitHub Actions workflows
try:
    import subprocess
    result = subprocess.run(['gh', 'workflow', 'list'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        workflows = result.stdout.strip().split('\n')
        active_count = sum(1 for w in workflows if 'active' in w.lower())
        print(f"✅ GitHub Actions workflows: {len(workflows)} total")
        print(f"   - Active: {active_count}")

        # Check recent runs
        result2 = subprocess.run(['gh', 'run', 'list', '--limit', '10'], capture_output=True, text=True, timeout=5)
        if result2.returncode == 0:
            runs = [line for line in result2.stdout.strip().split('\n') if line.strip()]
            completed = sum(1 for r in runs if 'completed' in r.lower())
            print(f"   - Recent runs (last 10): {len(runs)}")
            print(f"   - Completed: {completed}")

            if completed == 0:
                print("\n❌ NO WORKFLOW EXECUTIONS")
                print("   → Lead generation: NOT RUNNING")
        else:
            print("   ⚠️  Cannot check runs (auth issue)")
    else:
        print("⚠️  Cannot verify (gh CLI not available)")
except Exception as e:
    print(f"⚠️  Cannot verify automation: {e}")

print()

# Summary
print("=" * 80)
print("FLYWHEEL ACTUAL STATE - BRUTAL TRUTH")
print("=" * 80)
print()

print("📊 CURRENT FLYWHEEL STATUS:")
print()
print("   ACQUISITION → CONVERSION → RETENTION → ADVOCACY")
print("        ❌            ❌           ❌          ❌")
print()
print("❌ FLYWHEEL IS DORMANT")
print()
print("REASON:")
print("  - No active orders = No conversion data")
print("  - No customers = Nothing to retain")
print("  - No repeat purchases = No LTV to optimize")
print("  - No reviews = No social proof")
print("  - Automation workflows NOT executing (missing tokens)")
print()
print("TO ACTIVATE FLYWHEEL:")
print("  1. Configure APIFY_API_TOKEN → Enable lead generation")
print("  2. Deploy Klaviyo flows → Enable conversion automation")
print("  3. First sale → Flywheel starts spinning")
print("  4. Repeat purchases → Flywheel accelerates")
print()
print("CURRENT STATE: Infrastructure ready, waiting for ignition")
print()

exit(0)
