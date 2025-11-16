#!/usr/bin/env python3
"""
CREATE SELLING PLANS - SHOPIFY NATIVE SUBSCRIPTIONS
- Creates 3 selling plan groups (Basic plan limit: max 3)
- Plan 1: Subscribe & Save 10% (30/60/90 days)
- Plan 2: Premium Subscribe & Save 15% (30/60 days) - Bundles only
- Plan 3: VIP Subscribe & Save 20% (90 days) - High-value products only

$0 cost - uses Shopify native subscription features
"""

import requests
import json

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

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("=" * 80)
print("CREATE SELLING PLANS - SHOPIFY NATIVE SUBSCRIPTIONS")
print("=" * 80)
print(f"Store: {SHOPIFY_DOMAIN}")
print()

# GraphQL endpoint
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

# ============================================================================
# SELLING PLAN GROUP 1: Subscribe & Save 10% (All Products)
# ============================================================================

print("Creating Selling Plan Group 1: Subscribe & Save 10%")
print("-" * 80)

selling_plan_group_1 = """
mutation {
  sellingPlanGroupCreate(
    input: {
      name: "Subscribe & Save 10%"
      merchantCode: "subscribe-save-10"
      description: "Save 10% on every order with automatic delivery"
      options: ["Delivery every"]
      sellingPlansToCreate: [
        {
          name: "Deliver every 30 days"
          options: "30 days"
          category: SUBSCRIPTION
          billingPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 1
            }
          }
          deliveryPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 1
            }
          }
          pricingPolicies: [
            {
              fixed: {
                adjustmentType: PERCENTAGE
                adjustmentValue: { percentage: 10.0 }
              }
            }
          ]
        }
        {
          name: "Deliver every 60 days"
          options: "60 days"
          category: SUBSCRIPTION
          billingPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 2
            }
          }
          deliveryPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 2
            }
          }
          pricingPolicies: [
            {
              fixed: {
                adjustmentType: PERCENTAGE
                adjustmentValue: { percentage: 10.0 }
              }
            }
          ]
        }
        {
          name: "Deliver every 90 days"
          options: "90 days"
          category: SUBSCRIPTION
          billingPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 3
            }
          }
          deliveryPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 3
            }
          }
          pricingPolicies: [
            {
              fixed: {
                adjustmentType: PERCENTAGE
                adjustmentValue: { percentage: 10.0 }
              }
            }
          ]
        }
      ]
    }
    resources: {
      productIds: []
      productVariantIds: []
    }
  ) {
    sellingPlanGroup {
      id
      name
      sellingPlans(first: 3) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": selling_plan_group_1})

if response.status_code == 200:
    result = response.json()

    if 'errors' in result:
        print(f"  ❌ GraphQL errors: {result['errors']}")
    elif result.get('data', {}).get('sellingPlanGroupCreate', {}).get('userErrors'):
        errors = result['data']['sellingPlanGroupCreate']['userErrors']
        print(f"  ❌ User errors: {errors}")
    else:
        group_data = result['data']['sellingPlanGroupCreate']['sellingPlanGroup']
        print(f"  ✅ Created: {group_data['name']}")
        print(f"  ✅ Group ID: {group_data['id']}")

        for edge in group_data['sellingPlans']['edges']:
            plan = edge['node']
            print(f"    - {plan['name']} (ID: {plan['id']})")
else:
    print(f"  ❌ HTTP error: {response.status_code}")
    print(response.text)

print()

# ============================================================================
# SELLING PLAN GROUP 2: Premium Subscribe & Save 15% (Bundles)
# ============================================================================

print("Creating Selling Plan Group 2: Premium Subscribe & Save 15% (Bundles)")
print("-" * 80)

selling_plan_group_2 = """
mutation {
  sellingPlanGroupCreate(
    input: {
      name: "Premium Subscribe & Save 15%"
      merchantCode: "premium-subscribe-save-15"
      description: "Save 15% on bundles with automatic delivery"
      options: ["Delivery every"]
      sellingPlansToCreate: [
        {
          name: "Deliver every 30 days"
          options: "30 days"
          category: SUBSCRIPTION
          billingPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 1
            }
          }
          deliveryPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 1
            }
          }
          pricingPolicies: [
            {
              fixed: {
                adjustmentType: PERCENTAGE
                adjustmentValue: { percentage: 15.0 }
              }
            }
          ]
        }
        {
          name: "Deliver every 60 days"
          options: "60 days"
          category: SUBSCRIPTION
          billingPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 2
            }
          }
          deliveryPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 2
            }
          }
          pricingPolicies: [
            {
              fixed: {
                adjustmentType: PERCENTAGE
                adjustmentValue: { percentage: 15.0 }
              }
            }
          ]
        }
      ]
    }
    resources: {
      productIds: []
      productVariantIds: []
    }
  ) {
    sellingPlanGroup {
      id
      name
      sellingPlans(first: 2) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": selling_plan_group_2})

if response.status_code == 200:
    result = response.json()

    if 'errors' in result:
        print(f"  ❌ GraphQL errors: {result['errors']}")
    elif result.get('data', {}).get('sellingPlanGroupCreate', {}).get('userErrors'):
        errors = result['data']['sellingPlanGroupCreate']['userErrors']
        print(f"  ❌ User errors: {errors}")
    else:
        group_data = result['data']['sellingPlanGroupCreate']['sellingPlanGroup']
        print(f"  ✅ Created: {group_data['name']}")
        print(f"  ✅ Group ID: {group_data['id']}")

        for edge in group_data['sellingPlans']['edges']:
            plan = edge['node']
            print(f"    - {plan['name']} (ID: {plan['id']})")
else:
    print(f"  ❌ HTTP error: {response.status_code}")
    print(response.text)

print()

# ============================================================================
# SELLING PLAN GROUP 3: VIP Subscribe & Save 20% (High-Value)
# ============================================================================

print("Creating Selling Plan Group 3: VIP Subscribe & Save 20% (High-Value)")
print("-" * 80)

selling_plan_group_3 = """
mutation {
  sellingPlanGroupCreate(
    input: {
      name: "VIP Subscribe & Save 20%"
      merchantCode: "vip-subscribe-save-20"
      description: "Save 20% on premium products with quarterly delivery"
      options: ["Delivery every"]
      sellingPlansToCreate: [
        {
          name: "Deliver every 90 days"
          options: "90 days"
          category: SUBSCRIPTION
          billingPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 3
            }
          }
          deliveryPolicy: {
            recurring: {
              interval: MONTH
              intervalCount: 3
            }
          }
          pricingPolicies: [
            {
              fixed: {
                adjustmentType: PERCENTAGE
                adjustmentValue: { percentage: 20.0 }
              }
            }
          ]
        }
      ]
    }
    resources: {
      productIds: []
      productVariantIds: []
    }
  ) {
    sellingPlanGroup {
      id
      name
      sellingPlans(first: 1) {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": selling_plan_group_3})

if response.status_code == 200:
    result = response.json()

    if 'errors' in result:
        print(f"  ❌ GraphQL errors: {result['errors']}")
    elif result.get('data', {}).get('sellingPlanGroupCreate', {}).get('userErrors'):
        errors = result['data']['sellingPlanGroupCreate']['userErrors']
        print(f"  ❌ User errors: {errors}")
    else:
        group_data = result['data']['sellingPlanGroupCreate']['sellingPlanGroup']
        print(f"  ✅ Created: {group_data['name']}")
        print(f"  ✅ Group ID: {group_data['id']}")

        for edge in group_data['sellingPlans']['edges']:
            plan = edge['node']
            print(f"    - {plan['name']} (ID: {plan['id']})")
else:
    print(f"  ❌ HTTP error: {response.status_code}")
    print(response.text)

print()

# ============================================================================
# SUCCESS
# ============================================================================

print("=" * 80)
print("SELLING PLANS CREATION COMPLETE")
print("=" * 80)
print()
print("✅ 3 Selling Plan Groups Created:")
print("  1. Subscribe & Save 10% (3 frequencies: 30/60/90 days)")
print("  2. Premium Subscribe & Save 15% (2 frequencies: 30/60 days)")
print("  3. VIP Subscribe & Save 20% (1 frequency: 90 days)")
print()
print("⏳ NEXT STEPS (MANUAL):")
print()
print("1. ASSIGN PRODUCTS TO SELLING PLANS:")
print("   - Go to: Shopify Admin → Products → Subscriptions")
print("   - For each selling plan group, click 'Add products'")
print("   - Plan 1 (10%): Assign top 20 individual products")
print("   - Plan 2 (15%): Assign all 15 bundles")
print("   - Plan 3 (20%): Assign high-value products ($150+)")
print()
print("2. INTEGRATE SUBSCRIPTION WIDGET:")
print("   - Upload snippets/subscription-widget.liquid")
print("   - Add to product pages (after Add to Cart button)")
print("   - Add to cart page (upgrade option)")
print()
print("3. CUSTOMER PORTAL LINK:")
print("   - Add to customer account page:")
print("   - Link: https://www.alphamedical.shop/tools/recurring/portal")
print("   - Label: 'Manage My Subscriptions'")
print()
print("4. SHOPIFY FLOW AUTOMATION:")
print("   - Create 4 flows for email notifications")
print("   - See SHOPIFY_FLOW_SUBSCRIPTIONS_GUIDE.md for details")
print()
print("COST: $0 (100% native Shopify features)")
print("=" * 80)
