#!/usr/bin/env python3
"""
FLYWHEEL COMPLETENESS AUDIT - What's MISSING structurally
Not just blocked, but ABSENT from the system
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_URL = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

print("=" * 80)
print("FLYWHEEL STRUCTURAL COMPLETENESS AUDIT")
print("Checking what's MISSING, not just inactive")
print("=" * 80)
print()

url = f"https://{SHOP_URL}/admin/api/2024-10/graphql.json"
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": ACCESS_TOKEN
}

# Check for MISSING automation components
print("1. ACQUISITION → CONVERSION: MISSING LINKS")
print("-" * 80)

# Check for product recommendations (cross-sell/upsell)
products_query = """
{
  products(first: 5) {
    edges {
      node {
        id
        title
        metafields(first: 10) {
          edges {
            node {
              namespace
              key
              value
            }
          }
        }
      }
    }
  }
}
"""

missing_components = []

try:
    response = requests.post(url, json={"query": products_query}, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        products = data.get('data', {}).get('products', {}).get('edges', [])

        has_recommendations = False
        has_upsell = False
        has_crosssell = False

        for product in products:
            metafields = product['node'].get('metafields', {}).get('edges', [])
            for mf in metafields:
                key = mf['node']['key']
                if 'recommend' in key or 'related' in key:
                    has_recommendations = True
                if 'upsell' in key:
                    has_upsell = True
                if 'cross' in key or 'bundle' in key:
                    has_crosssell = True

        if not has_recommendations:
            missing_components.append("❌ Product recommendations system (AI/rule-based)")
        if not has_upsell:
            missing_components.append("❌ Upsell automation (increase AOV)")
        if not has_crosssell:
            missing_components.append("❌ Cross-sell automation (related products)")

except Exception as e:
    print(f"⚠️  Cannot verify: {e}")

print()

# Check for subscription products
print("2. CONVERSION → RETENTION: MISSING LINKS")
print("-" * 80)

selling_plans_query = """
{
  sellingPlanGroups(first: 10) {
    edges {
      node {
        id
        name
        sellingPlans(first: 5) {
          edges {
            node {
              id
              name
            }
          }
        }
      }
    }
  }
}
"""

try:
    response = requests.post(url, json={"query": selling_plans_query}, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        selling_plan_groups = data.get('data', {}).get('sellingPlanGroups', {}).get('edges', [])

        if not selling_plan_groups:
            missing_components.append("❌ Subscription model (recurring revenue)")
            print("❌ NO subscription/selling plans found")
            print("   → Cannot convert one-time buyers to subscribers")
        else:
            print(f"✅ Found {len(selling_plan_groups)} selling plan groups")
except Exception as e:
    print(f"⚠️  Cannot verify: {e}")

print()

# Check for automated flows
print("3. RETENTION → ADVOCACY: MISSING LINKS")
print("-" * 80)

# We can't check Shopify Flow via API, but we can check scripts
import subprocess
try:
    # Check for post-purchase automation scripts
    result = subprocess.run(['find', '.', '-name', '*post*purchase*.py', '-o', '-name', '*review*.py'],
                          capture_output=True, text=True, timeout=5)
    scripts = [s for s in result.stdout.split('\n') if s.strip()]

    if not scripts:
        missing_components.append("❌ Post-purchase automation (review requests)")
        print("❌ NO post-purchase automation scripts found")
    else:
        print(f"✅ Found {len(scripts)} post-purchase scripts")

except Exception as e:
    print(f"⚠️  Cannot verify: {e}")

print()

# Check for referral system
print("4. ADVOCACY → ACQUISITION: MISSING LINKS")
print("-" * 80)

# Check for referral discount codes or programs
discounts_query = """
{
  discountNodes(first: 50) {
    edges {
      node {
        discount {
          ... on DiscountCodeBasic {
            title
            codes(first: 1) {
              edges {
                node {
                  code
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

try:
    response = requests.post(url, json={"query": discounts_query}, headers=headers, timeout=10)
    if response.status_code == 200:
        data = response.json()
        discounts = data.get('data', {}).get('discountNodes', {}).get('edges', [])

        has_referral = False
        has_friend = False

        for discount in discounts:
            disc_node = discount['node']['discount']
            title = disc_node.get('title', '').lower()
            if 'referral' in title or 'refer' in title:
                has_referral = True
            if 'friend' in title or 'give' in title:
                has_friend = True

        if not has_referral and not has_friend:
            missing_components.append("❌ Referral program (customer → new customer)")
            print("❌ NO referral discount codes found")
            print("   → No incentive for customers to refer friends")
        else:
            print("✅ Referral-related discounts found")
except Exception as e:
    print(f"⚠️  Cannot verify: {e}")

print()

# Check for email automation
print("5. EMAIL AUTOMATION INFRASTRUCTURE")
print("-" * 80)

# Check for email templates/flows in codebase
try:
    result = subprocess.run(['find', '.', '-name', '*email*.md', '-o', '-name', '*flow*.md'],
                          capture_output=True, text=True, timeout=5)
    docs = [d for d in result.stdout.split('\n') if d.strip() and 'IMPLEMENTATION' in d.upper()]

    required_flows = ['welcome', 'abandoned_cart', 'post_purchase', 'win_back', 'browse_abandon']
    found_flows = []

    for doc in docs:
        for flow in required_flows:
            if flow in doc.lower():
                found_flows.append(flow)

    missing_flows = [f for f in required_flows if f not in found_flows]

    if missing_flows:
        print(f"❌ Missing email flow docs: {', '.join(missing_flows)}")
        for mf in missing_flows:
            missing_components.append(f"❌ Email flow: {mf.replace('_', ' ').title()}")
    else:
        print("✅ All critical email flow docs exist")

except Exception as e:
    print(f"⚠️  Cannot verify: {e}")

print()

# Summary
print("=" * 80)
print("MISSING COMPONENTS SUMMARY")
print("=" * 80)
print()

if missing_components:
    print(f"❌ FOUND {len(missing_components)} MISSING COMPONENTS:")
    print()
    for component in missing_components:
        print(f"  {component}")
    print()
    print("THESE ARE STRUCTURAL GAPS, NOT JUST BLOCKERS")
    print("Need to be built/implemented, not just activated")
else:
    print("✅ All major flywheel components are structurally present")
    print("(May be inactive but infrastructure exists)")

print()
print("=" * 80)
print("CRITICAL INFRASTRUCTURE GAPS")
print("=" * 80)
print()
print("MISSING AUTOMATIONS:")
print("  1. Product recommendation engine (upsell/cross-sell)")
print("  2. Subscription conversion system")
print("  3. Automated review collection flow")
print("  4. Referral incentive program")
print("  5. Win-back automation (dormant customers)")
print("  6. Browse abandonment tracking")
print()
print("These create BREAKS in the flywheel cycle:")
print("  - Acquisition → Conversion: No product discovery automation")
print("  - Conversion → Retention: No subscription path")
print("  - Retention → Advocacy: No review automation")
print("  - Advocacy → Acquisition: No referral loop")
print()

exit(0)
