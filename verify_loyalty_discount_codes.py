#!/usr/bin/env python3
"""
VERIFICATION: Loyalty Discount Codes Status
Date: 2025-11-20
Purpose: Verify if loyalty discount codes (LOYALTY10, LOYALTY15, LOYALTY25, LOYALTY50) exist
"""

import requests

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

SHOP = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN}

print("=" * 80)
print("VERIFICATION: Loyalty Discount Codes")
print("=" * 80)
print()

REQUIRED_CODES = {
    "LOYALTY10": {"discount": "10%", "tier": "Bronze"},
    "LOYALTY15": {"discount": "15%", "tier": "Silver"},
    "LOYALTY25": {"discount": "25%", "tier": "Gold"},
    "LOYALTY50": {"discount": "50%", "tier": "Platinum"}
}

# Fetch all discount codes (price rules)
print("Fetching all discount codes from Shopify...\n")

response = requests.get(
    f"{REST_URL}/price_rules.json?limit=250",
    headers=HEADERS
)

if response.status_code != 200:
    print(f"❌ API Error: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    exit(1)

price_rules = response.json().get('price_rules', [])
print(f"✅ Fetched {len(price_rules)} price rules\n")

# Check each required code
print("=" * 80)
print("LOYALTY CODE STATUS")
print("=" * 80)

found_codes = {}
missing_codes = []

for code_name, details in REQUIRED_CODES.items():
    print(f"\nChecking: {code_name} ({details['tier']} - {details['discount']})")

    # Find matching price rule
    matching_rule = None
    for rule in price_rules:
        if code_name.lower() in rule.get('title', '').lower():
            matching_rule = rule
            break

    if matching_rule:
        rule_id = matching_rule['id']
        value = matching_rule.get('value', 0)
        value_type = matching_rule.get('value_type', 'unknown')

        # Fetch discount codes for this rule
        codes_response = requests.get(
            f"{REST_URL}/price_rules/{rule_id}/discount_codes.json",
            headers=HEADERS
        )

        if codes_response.status_code == 200:
            codes = codes_response.json().get('discount_codes', [])
            if codes:
                code = codes[0].get('code', 'UNKNOWN')
                print(f"   ✅ FOUND")
                print(f"      Code: {code}")
                print(f"      Value: {abs(value)}{'' if value_type == 'percentage' else '$'} off")
                print(f"      Rule ID: {rule_id}")
                found_codes[code_name] = {
                    "code": code,
                    "value": abs(value),
                    "value_type": value_type,
                    "rule_id": rule_id
                }
            else:
                print(f"   ⚠️  Price rule exists but no discount code created")
                print(f"      Rule ID: {rule_id}")
                missing_codes.append(code_name)
        else:
            print(f"   ⚠️  Price rule exists but couldn't fetch codes")
            print(f"      Rule ID: {rule_id}")
            missing_codes.append(code_name)
    else:
        print(f"   ❌ NOT FOUND")
        missing_codes.append(code_name)

# Summary
print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

print(f"\n✅ Found: {len(found_codes)}/{len(REQUIRED_CODES)} discount codes")
print(f"❌ Missing: {len(missing_codes)}/{len(REQUIRED_CODES)} discount codes")

if missing_codes:
    print(f"\n🔴 MISSING CODES:")
    for code in missing_codes:
        details = REQUIRED_CODES[code]
        print(f"   - {code} ({details['tier']} tier - {details['discount']} off)")

    print("\n📋 MANUAL ACTION REQUIRED:")
    print("\n1. Go to Shopify Admin → Discounts")
    print("2. Create each missing discount code:")
    print()
    for code in missing_codes:
        details = REQUIRED_CODES[code]
        print(f"   {code}:")
        print(f"   - Title: Loyalty {details['tier']} Tier Discount")
        print(f"   - Code: {code}")
        print(f"   - Type: Percentage")
        print(f"   - Value: {details['discount']}")
        print(f"   - Customer eligibility: Customers with tag 'loyalty-{details['tier'].lower()}'")
        print(f"   - Usage limit: No limit")
        print(f"   - Active dates: No end date")
        print()

    print("⏱️  Time required: ~5 minutes total")
    print()
    exit(1)
else:
    print("\n✅ ALL LOYALTY DISCOUNT CODES EXIST")
    print("✅ Loyalty discount system is ready to use")
    print()
    exit(0)
