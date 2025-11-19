#!/usr/bin/env python3
"""
FORENSIC VERIFICATION - Country Information Corrections
NO TRUST - Verify EVERY claim with factual evidence from live site
"""

import requests
import re
import json
from datetime import datetime

print("═══════════════════════════════════════════════════════════════")
print("🔬 FORENSIC VERIFICATION - Country Information")
print(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
print("═══════════════════════════════════════════════════════════════\n")

# ═══════════════════════════════════════════════════════════════════
# TEST 1: Fetch Live HTML (Source of Truth)
# ═══════════════════════════════════════════════════════════════════

print("📋 TEST 1: Extract Schema.org from Live Site")
print("─" * 60)

try:
    response = requests.get('https://www.alphamedical.shop', timeout=10)
    html = response.text
    print(f"✅ Fetched homepage: {len(html):,} chars")
except Exception as e:
    print(f"❌ FATAL: Could not fetch homepage - {e}")
    exit(1)

# Extract all JSON-LD schemas
schema_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
print(f"✅ Found {len(schema_matches)} JSON-LD schemas\n")

# ═══════════════════════════════════════════════════════════════════
# TEST 2: Parse MedicalBusiness Schema (Critical)
# ═══════════════════════════════════════════════════════════════════

print("📋 TEST 2: Verify MedicalBusiness Schema Corrections")
print("─" * 60)

medical_business_schema = None
for schema_text in schema_matches:
    try:
        schema_json = json.loads(schema_text.strip())
        if schema_json.get('@type') == 'MedicalBusiness':
            medical_business_schema = schema_json
            break
    except json.JSONDecodeError:
        continue

if not medical_business_schema:
    print("❌ FATAL: MedicalBusiness schema NOT found!")
    exit(1)

print("✅ MedicalBusiness schema found\n")

# ═══════════════════════════════════════════════════════════════════
# TEST 3: Verify Each Correction (3 Expected)
# ═══════════════════════════════════════════════════════════════════

errors = []
warnings = []
successes = []

# Verification 1: disambiguatingDescription
print("🔍 VERIFICATION 1: disambiguatingDescription")
disambig = medical_business_schema.get('disambiguatingDescription', '')
print(f"   Current value: {disambig[:80]}...")

if 'Canadian medical equipment retailer' in disambig:
    errors.append("❌ FAILED: Still says 'Canadian medical equipment retailer'")
    print("   ❌ FAILED: Still says 'Canadian'")
elif 'US-based medical equipment retailer' in disambig or 'American medical equipment' in disambig:
    successes.append("✅ PASS: Says 'US-based medical equipment retailer'")
    print("   ✅ PASS: Correctly says 'US-based'")
else:
    warnings.append(f"⚠️  WARNING: Unexpected value: {disambig}")
    print(f"   ⚠️  WARNING: Unexpected value")

print()

# Verification 2: addressCountry
print("🔍 VERIFICATION 2: addressCountry")
address = medical_business_schema.get('address', {})
address_country = address.get('addressCountry', '') if isinstance(address, dict) else ''
print(f"   Current value: {address_country}")

if address_country == 'CA':
    errors.append("❌ FAILED: addressCountry is still 'CA'")
    print("   ❌ FAILED: Still 'CA' (should be 'US')")
elif address_country == 'US':
    successes.append("✅ PASS: addressCountry is 'US'")
    print("   ✅ PASS: Correctly set to 'US'")
else:
    warnings.append(f"⚠️  WARNING: addressCountry is '{address_country}'")
    print(f"   ⚠️  WARNING: Unexpected value '{address_country}'")

print()

# Verification 3: areaServed
print("🔍 VERIFICATION 3: areaServed")
area_served = medical_business_schema.get('areaServed', {})
area_name = area_served.get('name', '') if isinstance(area_served, dict) else ''
print(f"   Current value: {area_name}")

if area_name == 'Canada':
    errors.append("❌ FAILED: areaServed is still 'Canada'")
    print("   ❌ FAILED: Still 'Canada' (should be 'United States')")
elif area_name == 'United States':
    successes.append("✅ PASS: areaServed is 'United States'")
    print("   ✅ PASS: Correctly set to 'United States'")
else:
    warnings.append(f"⚠️  WARNING: areaServed is '{area_name}'")
    print(f"   ⚠️  WARNING: Unexpected value '{area_name}'")

print()

# ═══════════════════════════════════════════════════════════════════
# TEST 4: Search for ANY Remaining "Canada" in Schema
# ═══════════════════════════════════════════════════════════════════

print("📋 TEST 4: Search for Remaining 'Canada' Mentions in Schema")
print("─" * 60)

schema_str = json.dumps(medical_business_schema)
canada_count = schema_str.count('Canada')

if canada_count > 0:
    errors.append(f"❌ FAILED: 'Canada' found {canada_count} times in schema")
    print(f"   ❌ FAILED: 'Canada' appears {canada_count} times")

    # Find and display occurrences
    for key, value in medical_business_schema.items():
        value_str = json.dumps(value)
        if 'Canada' in value_str:
            print(f"      Found in '{key}': {value_str[:100]}")
else:
    successes.append("✅ PASS: No 'Canada' mentions in schema")
    print("   ✅ PASS: No 'Canada' mentions found")

print()

# ═══════════════════════════════════════════════════════════════════
# TEST 5: Verify "10,000+ customers" Claims (Bonus Test)
# ═══════════════════════════════════════════════════════════════════

print("📋 TEST 5: Check for '10,000+ customers' Claims (Bonus)")
print("─" * 60)

customer_patterns = [
    r'10[,\s]?000\+?\s*[Cc]ustomers?',
    r'10k\+?\s*[Cc]ustomers?',
]

customer_claims_found = []
for pattern in customer_patterns:
    matches = re.findall(pattern, html, re.IGNORECASE)
    if matches:
        customer_claims_found.extend(set(matches))

if customer_claims_found:
    warnings.append(f"⚠️  '10,000+ customers' claims still present: {customer_claims_found}")
    print(f"   ⚠️  Found unverifiable claims: {customer_claims_found}")
else:
    print("   ✅ No '10,000+ customers' claims found")

print()

# ═══════════════════════════════════════════════════════════════════
# FINAL REPORT
# ═══════════════════════════════════════════════════════════════════

print("═══════════════════════════════════════════════════════════════")
print("📊 FORENSIC VERIFICATION REPORT")
print("═══════════════════════════════════════════════════════════════\n")

print(f"✅ Successes: {len(successes)}")
for success in successes:
    print(f"   {success}")

print(f"\n⚠️  Warnings: {len(warnings)}")
for warning in warnings:
    print(f"   {warning}")

print(f"\n❌ Errors: {len(errors)}")
for error in errors:
    print(f"   {error}")

print()

if len(errors) == 0 and len(successes) == 3:
    print("🎉 VERDICT: 100% SUCCESS - All 3 corrections verified on live site")
    print("   Country information is now FACTUALLY CORRECT\n")
    exit(0)
elif len(errors) == 0:
    print(f"⚠️  VERDICT: PARTIAL SUCCESS - {len(successes)}/3 corrections verified")
    print("   Some corrections may not have been applied\n")
    exit(1)
else:
    print(f"❌ VERDICT: FAILED - {len(errors)} errors found")
    print("   Corrections were NOT successfully applied\n")
    exit(1)
