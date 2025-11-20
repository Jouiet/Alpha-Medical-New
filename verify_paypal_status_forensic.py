#!/usr/bin/env python3
"""
VERIFICATION FORENSIQUE - PayPal Status
Date: 2025-11-20
Purpose: Verify FACTUALLY if PayPal is still active on checkout

REQUIREMENT: "PAS de PayPal!!" (only Shopify Payments: Stripe + Google Pay + Apple Pay)

METHODOLOGY:
1. Fetch homepage HTML source
2. Search for PayPal-specific JavaScript/code
3. Search for PayPal Express Checkout button
4. Provide factual evidence (not assumptions)

LIMITATION: Cannot access checkout page without creating real order
WORKAROUND: Search homepage + cart for PayPal scripts
"""

import requests
import re

STORE_URL = "https://www.alphamedical.shop"

print("=" * 80)
print("VERIFICATION FORENSIQUE - PAYPAL STATUS")
print("=" * 80)
print(f"Store: {STORE_URL}")
print(f"Date: 2025-11-20\n")

# Fetch homepage HTML
print("=" * 80)
print("STEP 1: FETCH HOMEPAGE HTML SOURCE")
print("=" * 80)

try:
    response = requests.get(STORE_URL, timeout=30)
    if response.status_code != 200:
        print(f"❌ Failed to fetch homepage: HTTP {response.status_code}")
        exit(1)

    html = response.text
    print(f"✅ Fetched homepage: {len(html)} characters\n")
except Exception as e:
    print(f"❌ Error fetching homepage: {e}")
    exit(1)

# Search for PayPal indicators
print("=" * 80)
print("STEP 2: SEARCH FOR PAYPAL INDICATORS")
print("=" * 80)

paypal_indicators = []

# Indicator 1: PayPal JavaScript tracking
if "ShopifyPaypalV4VisibilityTracking" in html:
    paypal_indicators.append({
        "type": "JavaScript Variable",
        "evidence": "ShopifyPaypalV4VisibilityTracking",
        "severity": "HIGH",
        "context": "PayPal V4 visibility tracking enabled"
    })
    print("❌ FOUND: ShopifyPaypalV4VisibilityTracking = true")
    print("   Location: Homepage HTML")
    print("   Severity: HIGH (indicates PayPal integration active)\n")

# Indicator 2: PayPal SDK/Scripts
paypal_scripts = re.findall(r'(paypal[^\s"\'<>]*)', html, re.IGNORECASE)
if paypal_scripts:
    unique_scripts = list(set(paypal_scripts))[:5]  # Show max 5
    paypal_indicators.append({
        "type": "PayPal Scripts",
        "evidence": unique_scripts,
        "severity": "HIGH",
        "context": f"{len(unique_scripts)} PayPal-related scripts found"
    })
    print(f"❌ FOUND: {len(unique_scripts)} PayPal-related references:")
    for script in unique_scripts:
        print(f"   - {script}")
    print()

# Indicator 3: Payment provider meta tags
if re.search(r'payment.*paypal', html, re.IGNORECASE):
    paypal_indicators.append({
        "type": "Payment Meta Tags",
        "evidence": "payment + paypal keywords",
        "severity": "MEDIUM",
        "context": "PayPal mentioned in payment context"
    })
    print("⚠️  FOUND: PayPal mentioned in payment context\n")

# Indicator 4: Express Checkout button
if re.search(r'paypal.*express|express.*paypal', html, re.IGNORECASE):
    paypal_indicators.append({
        "type": "Express Checkout",
        "evidence": "PayPal Express keywords",
        "severity": "HIGH",
        "context": "PayPal Express Checkout likely enabled"
    })
    print("❌ FOUND: PayPal Express Checkout keywords\n")

# SUMMARY
print("=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

if len(paypal_indicators) == 0:
    print("✅ NO PAYPAL INDICATORS FOUND")
    print("✅ PayPal appears to be DEACTIVATED\n")
    print("VERIFICATION RESULT: ✅ COMPLIANT")
    print("Evidence: No PayPal scripts, tracking, or buttons detected in homepage HTML\n")
else:
    print(f"❌ {len(paypal_indicators)} PAYPAL INDICATORS FOUND")
    print("❌ PayPal appears to be ACTIVE\n")

    print("EVIDENCE:")
    for i, indicator in enumerate(paypal_indicators, 1):
        print(f"{i}. {indicator['type']}")
        print(f"   Evidence: {indicator['evidence']}")
        print(f"   Severity: {indicator['severity']}")
        print(f"   Context: {indicator['context']}\n")

    print("=" * 80)
    print("VERIFICATION RESULT: ❌ NON-COMPLIANT")
    print("=" * 80)
    print("REQUIREMENT VIOLATION: 'PAS de PayPal!!'")
    print("ACTUAL STATE: PayPal integration detected\n")

    print("NEXT STEPS:")
    print("1. Deactivate PayPal in Shopify Admin → Settings → Payments")
    print("2. Remove PayPal Express Checkout if enabled")
    print("3. Re-run this script to verify deactivation")
    print("4. Verify live checkout page (manual test)")
    print()

    print("GUIDE: See PAYPAL_DEACTIVATION_GUIDE.md for step-by-step instructions")
    print()

# Save results
results = {
    "timestamp": "2025-11-20",
    "store": STORE_URL,
    "paypal_active": len(paypal_indicators) > 0,
    "indicators_count": len(paypal_indicators),
    "indicators": paypal_indicators
}

import json
with open("paypal_verification_results.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"📄 Results saved to: paypal_verification_results.json\n")

# Exit code
if len(paypal_indicators) > 0:
    exit(1)  # Non-compliant
else:
    exit(0)  # Compliant
