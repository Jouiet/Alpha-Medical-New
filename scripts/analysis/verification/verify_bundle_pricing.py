#!/usr/bin/env python3
"""
VERIFY BUNDLE PRICING - Alpha Medical Care
Factual verification of bundle pricing compliance
REQUIREMENT: "Bundles 35% du prix fournisseur (35% du chiffre compare at price)"
"""

import json
from datetime import datetime

print("=" * 80)
print("BUNDLE PRICING VERIFICATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# Load bundle plans
with open('optimal_bundles_plan.json', 'r') as f:
    bundles_plan = json.load(f)

print(f"\nREQUIREMENT: Bundles 35% du prix fournisseur (35% du chiffre compare at price)")
print(f"INTERPRETATION: bundle_price should be 35% of total_price (compare_at_price)")
print(f"\nTotal Bundles: {bundles_plan['total_bundles']}")

print("\n" + "=" * 80)
print("PRICING ANALYSIS")
print("=" * 80)

violations = []
compliant = []

for bundle in bundles_plan['bundles']:
    total_price = bundle['total_price']
    current_bundle_price = bundle['bundle_price']
    expected_bundle_price = total_price * 0.35  # 35% of total

    current_percentage = (current_bundle_price / total_price) * 100
    discount_percentage = ((total_price - current_bundle_price) / total_price) * 100

    print(f"\n{bundle['name']}:")
    print(f"   Compare At Price (Total): ${total_price:.2f}")
    print(f"   Current Bundle Price:     ${current_bundle_price:.2f} ({current_percentage:.1f}% of total)")
    print(f"   Current Discount:         {discount_percentage:.1f}% OFF")
    print(f"   Expected Price (35%):     ${expected_bundle_price:.2f}")
    print(f"   Difference:               ${current_bundle_price - expected_bundle_price:.2f}")

    if abs(current_percentage - 35.0) > 1.0:  # Allow 1% tolerance
        print(f"   Status: ❌ VIOLATION (should be 35%, is {current_percentage:.1f}%)")
        violations.append({
            'name': bundle['name'],
            'current': current_bundle_price,
            'expected': expected_bundle_price,
            'current_pct': current_percentage
        })
    else:
        print(f"   Status: ✅ COMPLIANT")
        compliant.append(bundle['name'])

print("\n" + "=" * 80)
print("COMPLIANCE SUMMARY")
print("=" * 80)

print(f"\n✅ Compliant Bundles: {len(compliant)}/{bundles_plan['total_bundles']}")
print(f"❌ Violation Bundles: {len(violations)}/{bundles_plan['total_bundles']}")

if violations:
    print(f"\n🔴 CRITICAL PRICING VIOLATION DETECTED")
    print(f"\n   Current Implementation: Bundle price = 85% of total (15% discount)")
    print(f"   Required Implementation: Bundle price = 35% of total (65% discount)")
    print(f"\n   Financial Impact Analysis:")

    current_total_revenue = sum([b['bundle_price'] for b in bundles_plan['bundles']])
    expected_total_revenue = sum([b['total_price'] * 0.35 for b in bundles_plan['bundles']])
    revenue_diff = current_total_revenue - expected_total_revenue

    print(f"      Current Total Bundle Revenue:  ${current_total_revenue:.2f}")
    print(f"      Expected Total Bundle Revenue: ${expected_total_revenue:.2f}")
    print(f"      Difference:                    ${revenue_diff:.2f} ({(revenue_diff/current_total_revenue)*100:.1f}%)")

    print(f"\n   CORRECTION REQUIRED:")
    print(f"   - All {len(violations)} bundles must be repriced")
    print(f"   - Script needed: update_bundle_prices_to_35_percent.py")
    print(f"   - Action: Update bundle variant prices via GraphQL")
else:
    print(f"\n✅ ALL BUNDLES COMPLIANT WITH 35% PRICING REQUIREMENT")

print("\n" + "=" * 80)
