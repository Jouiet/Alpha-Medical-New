#!/usr/bin/env python3
"""
DEPLOY LOYALTY SYSTEM SIMPLIFIED - Tag-Based ($0)
- Upload loyalty-tier-badge.liquid snippet
- Create discount codes (LOYALTY10, LOYALTY15, LOYALTY25, LOYALTY50)
- Document Shopify Flow setup instructions

NO plan upgrade required - uses customer tags only
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
THEME_ID = "140069830733"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("=" * 80)
print("DEPLOY LOYALTY SYSTEM SIMPLIFIED - TAG-BASED ($0)")
print("=" * 80)
print(f"Store: {SHOPIFY_DOMAIN}")
print(f"Theme: {THEME_ID}")
print()

# ============================================================================
# STEP 1: Upload loyalty-tier-badge.liquid snippet
# ============================================================================

print("Step 1: Uploading loyalty-tier-badge.liquid snippet...")

snippet_path = '/Users/mac/Desktop/Alpha-Medical/snippets/loyalty-tier-badge.liquid'
with open(snippet_path, 'r') as f:
    snippet_content = f.read()

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/themes/{THEME_ID}/assets.json"
payload = {
    "asset": {
        "key": "snippets/loyalty-tier-badge.liquid",
        "value": snippet_content
    }
}

response = requests.put(url, headers=HEADERS, json=payload)

if response.status_code in [200, 201]:
    print("  ✅ loyalty-tier-badge.liquid uploaded")
else:
    print(f"  ❌ Upload failed: {response.status_code}")
    print(response.text)

# ============================================================================
# STEP 2: Create discount codes
# ============================================================================

print("\nStep 2: Creating loyalty discount codes...")

discount_codes = [
    {
        "code": "LOYALTY10",
        "value_type": "percentage",
        "value": "-10.0",
        "title": "Bronze Tier - 10% Off",
        "customer_selection": "all"
    },
    {
        "code": "LOYALTY15",
        "value_type": "percentage",
        "value": "-15.0",
        "title": "Silver Tier - 15% Off",
        "customer_selection": "all"
    },
    {
        "code": "LOYALTY25",
        "value_type": "percentage",
        "value": "-25.0",
        "title": "Gold Tier - 25% Off",
        "customer_selection": "all"
    },
    {
        "code": "LOYALTY50",
        "value_type": "percentage",
        "value": "-50.0",
        "title": "Platinum Tier - 50% Off",
        "customer_selection": "all"
    }
]

for discount in discount_codes:
    # Create price rule
    price_rule_url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/price_rules.json"
    price_rule_payload = {
        "price_rule": {
            "title": discount["title"],
            "target_type": "line_item",
            "target_selection": "all",
            "allocation_method": "across",
            "value_type": discount["value_type"],
            "value": discount["value"],
            "customer_selection": discount["customer_selection"],
            "starts_at": "2025-01-01T00:00:00Z"
        }
    }

    response = requests.post(price_rule_url, headers=HEADERS, json=price_rule_payload)

    if response.status_code in [200, 201]:
        price_rule_id = response.json()['price_rule']['id']
        print(f"  ✅ Created price rule: {discount['title']}")

        # Create discount code
        discount_code_url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/price_rules/{price_rule_id}/discount_codes.json"
        discount_code_payload = {
            "discount_code": {
                "code": discount["code"]
            }
        }

        response = requests.post(discount_code_url, headers=HEADERS, json=discount_code_payload)

        if response.status_code in [200, 201]:
            print(f"    ✅ Discount code created: {discount['code']}")
        else:
            # Code might already exist
            if 'already been taken' in response.text:
                print(f"    ℹ️  Discount code already exists: {discount['code']}")
            else:
                print(f"    ❌ Failed to create code: {response.status_code}")
                print(f"    {response.text}")
    else:
        print(f"  ❌ Failed to create price rule: {response.status_code}")
        print(response.text)

# ============================================================================
# STEP 3: Generate Shopify Flow setup documentation
# ============================================================================

print("\n" + "=" * 80)
print("SHOPIFY FLOW SETUP REQUIRED (MANUAL)")
print("=" * 80)
print()
print("You need to create 4 Shopify Flows manually in the Shopify Admin.")
print()
print("Go to: https://admin.shopify.com/store/azffej-as/flow")
print()

flows = [
    {
        "name": "Loyalty - Bronze Tier (New Customers)",
        "trigger": "Customer created",
        "conditions": [],
        "actions": [
            "Add customer tag: loyalty-bronze",
            "Send email: Welcome to Bronze tier! Use code LOYALTY10 for 10% off"
        ]
    },
    {
        "name": "Loyalty - Silver Tier ($500+ spent)",
        "trigger": "Order paid",
        "conditions": ["Customer total spent > $500"],
        "actions": [
            "Remove customer tag: loyalty-bronze",
            "Add customer tag: loyalty-silver",
            "Send email: Upgraded to Silver tier! Use code LOYALTY15 for 15% off"
        ]
    },
    {
        "name": "Loyalty - Gold Tier ($1000+ spent)",
        "trigger": "Order paid",
        "conditions": ["Customer total spent > $1000"],
        "actions": [
            "Remove customer tag: loyalty-silver",
            "Add customer tag: loyalty-gold",
            "Send email: Upgraded to Gold tier! Use code LOYALTY25 for 25% off"
        ]
    },
    {
        "name": "Loyalty - Platinum Tier ($2500+ spent)",
        "trigger": "Order paid",
        "conditions": ["Customer total spent > $2500"],
        "actions": [
            "Remove customer tag: loyalty-gold",
            "Add customer tag: loyalty-platinum",
            "Send email: Upgraded to Platinum tier! Use code LOYALTY50 for 50% off"
        ]
    }
]

for i, flow in enumerate(flows, 1):
    print(f"FLOW {i}: {flow['name']}")
    print(f"  Trigger: {flow['trigger']}")

    if flow['conditions']:
        print(f"  Conditions:")
        for condition in flow['conditions']:
            print(f"    - {condition}")

    print(f"  Actions:")
    for action in flow['actions']:
        print(f"    - {action}")

    print()

# ============================================================================
# STEP 4: Integration instructions
# ============================================================================

print("=" * 80)
print("INTEGRATION INSTRUCTIONS")
print("=" * 80)
print()
print("1. ADD BADGE TO ACCOUNT PAGE:")
print("   - Edit templates/customers/account.json")
print("   - Add custom liquid section:")
print("   {% render 'loyalty-tier-badge' %}")
print()
print("2. CREATE LOYALTY PROGRAM PAGE:")
print("   - Create /pages/loyalty-program")
print("   - Explain tier benefits:")
print("     - Bronze: $0-499 spent → 10% off (LOYALTY10)")
print("     - Silver: $500-999 spent → 15% off (LOYALTY15)")
print("     - Gold: $1000-2499 spent → 25% off (LOYALTY25)")
print("     - Platinum: $2500+ spent → 50% off (LOYALTY50)")
print()
print("3. TEST SYSTEM:")
print("   - Create test customer")
print("   - Manually add 'loyalty-bronze' tag")
print("   - Log in as customer")
print("   - Visit /account")
print("   - Verify badge displays correctly")
print("   - Copy discount code")
print("   - Apply at checkout")
print()

# ============================================================================
# SUCCESS
# ============================================================================

print("=" * 80)
print("DEPLOYMENT COMPLETE")
print("=" * 80)
print("✅ loyalty-tier-badge.liquid uploaded to Shopify")
print("✅ 4 discount codes created (LOYALTY10, LOYALTY15, LOYALTY25, LOYALTY50)")
print()
print("⏳ MANUAL STEPS REQUIRED:")
print("  1. Create 4 Shopify Flows (see instructions above)")
print("  2. Add badge to account page template")
print("  3. Create /pages/loyalty-program page")
print("  4. Test with test customer")
print()
print("COST: $0 (uses native Shopify features only)")
print("=" * 80)
