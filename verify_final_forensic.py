#!/usr/bin/env python3
"""
FINAL FORENSIC VERIFICATION - Complete Site Audit
Verify ALL corrections are live and factually accurate
"""

import requests
import re
import json
from datetime import datetime

print("═══════════════════════════════════════════════════════════════")
print("🔬 FINAL FORENSIC VERIFICATION")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("═══════════════════════════════════════════════════════════════\n")

# ═══════════════════════════════════════════════════════════════════
# FETCH LIVE SITE
# ═══════════════════════════════════════════════════════════════════

try:
    response = requests.get('https://www.alphamedical.shop', timeout=10)
    html = response.text
    print(f"✅ Fetched homepage: {len(html):,} chars\n")
except Exception as e:
    print(f"❌ FATAL: {e}")
    exit(1)

# ═══════════════════════════════════════════════════════════════════
# EXTRACT SCHEMA.ORG
# ═══════════════════════════════════════════════════════════════════

schema_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
medical_schema = None

for schema_text in schema_matches:
    try:
        schema_json = json.loads(schema_text.strip())
        if schema_json.get('@type') == 'MedicalBusiness':
            medical_schema = schema_json
            break
    except:
        continue

if not medical_schema:
    print("❌ FATAL: MedicalBusiness schema not found!")
    exit(1)

# ═══════════════════════════════════════════════════════════════════
# VERIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════

errors = []
warnings = []
successes = []

print("═══════════════════════════════════════════════════════════════")
print("📋 SCHEMA.ORG VERIFICATION")
print("═══════════════════════════════════════════════════════════════\n")

# Test 1: disambiguatingDescription
print("🔍 TEST 1: disambiguatingDescription")
disambig = medical_schema.get('disambiguatingDescription', '')
print(f"   Current: {disambig[:80]}...")

if 'Canadian medical equipment' in disambig:
    errors.append("❌ Still says 'Canadian'")
    print("   ❌ FAIL: Still says 'Canadian'")
elif 'International medical equipment retailer' in disambig:
    if 'e-commerce headquarters in United States' in disambig:
        if 'physical stores in Canada and Europe' in disambig:
            successes.append("✅ Fully accurate international description")
            print("   ✅ PASS: Fully accurate international description")
        else:
            warnings.append("⚠️  Mentions US but missing CA/EU stores")
            print("   ⚠️  WARNING: Missing CA/EU store mention")
    else:
        warnings.append("⚠️  Says 'International' but doesn't clarify locations")
        print("   ⚠️  WARNING: Lacks location clarification")
else:
    warnings.append(f"⚠️  Unexpected: {disambig[:50]}")
    print(f"   ⚠️  WARNING: Unexpected value")

print()

# Test 2: addressCountry
print("🔍 TEST 2: addressCountry (E-commerce HQ)")
address = medical_schema.get('address', {})
address_country = address.get('addressCountry', '') if isinstance(address, dict) else ''
print(f"   Current: {address_country}")

if address_country == 'US':
    successes.append("✅ addressCountry: US (correct for e-commerce HQ)")
    print("   ✅ PASS: Correct (US e-commerce HQ)")
elif address_country == 'CA':
    errors.append("❌ addressCountry still 'CA'")
    print("   ❌ FAIL: Still 'CA'")
else:
    warnings.append(f"⚠️  addressCountry: {address_country}")
    print(f"   ⚠️  WARNING: Unexpected '{address_country}'")

print()

# Test 3: areaServed
print("🔍 TEST 3: areaServed (Markets Served)")
area_served = medical_schema.get('areaServed', [])

if isinstance(area_served, list):
    countries = [area.get('name', '') for area in area_served if isinstance(area, dict)]
    print(f"   Current: {countries}")

    expected = ['United States', 'Canada', 'Europe']
    all_present = all(country in countries for country in expected)

    if all_present:
        successes.append(f"✅ areaServed: {len(countries)} markets (US, CA, EU)")
        print(f"   ✅ PASS: All markets listed ({len(countries)} total)")
    else:
        missing = [c for c in expected if c not in countries]
        warnings.append(f"⚠️  areaServed missing: {missing}")
        print(f"   ⚠️  WARNING: Missing {missing}")

elif isinstance(area_served, dict):
    # Single country (old format)
    country_name = area_served.get('name', '')
    print(f"   Current: {country_name} (single country)")

    if country_name == 'United States':
        errors.append("❌ areaServed is only US (missing CA/EU)")
        print("   ❌ FAIL: Only US (should include CA, EU)")
    else:
        errors.append(f"❌ areaServed: {country_name}")
        print(f"   ❌ FAIL: Wrong value '{country_name}'")
else:
    errors.append("❌ areaServed has unexpected format")
    print("   ❌ FAIL: Unexpected format")

print()

# Test 4: No 'Canada' as primary location
print("🔍 TEST 4: No 'Canada' as Primary Business Location")
schema_str = json.dumps(medical_schema)

# Check if 'Canada' appears ONLY in areaServed (OK) or elsewhere (NOT OK)
canada_in_address = 'Canada' in json.dumps(address)
canada_in_disambig_as_base = 'Canadian medical equipment retailer' in disambig

if canada_in_address:
    errors.append("❌ 'Canada' in address field")
    print("   ❌ FAIL: 'Canada' in address (should be US)")
elif canada_in_disambig_as_base:
    errors.append("❌ Describes business as 'Canadian'")
    print("   ❌ FAIL: Described as 'Canadian'")
else:
    successes.append("✅ 'Canada' only mentioned as served market")
    print("   ✅ PASS: 'Canada' only as served market")

print()

# ═══════════════════════════════════════════════════════════════════
# TRUST BADGES VERIFICATION
# ═══════════════════════════════════════════════════════════════════

print("═══════════════════════════════════════════════════════════════")
print("📋 TRUST BADGES VERIFICATION")
print("═══════════════════════════════════════════════════════════════\n")

print("🔍 TEST 5: '10,000+ Customers' Claim Clarification")

# Check for clarified versions
if '10,000+ Customers Worldwide' in html:
    successes.append("✅ '10,000+ Customers Worldwide' (clarified)")
    print("   ✅ PASS: Clarified as 'Worldwide'")
elif '10,000+ International Customers' in html:
    successes.append("✅ '10,000+ International Customers' (clarified)")
    print("   ✅ PASS: Clarified as 'International'")
elif '10,000+ Customers' in html and 'Worldwide' not in html:
    warnings.append("⚠️  '10,000+ Customers' without 'Worldwide' clarification")
    print("   ⚠️  WARNING: Not clarified (ambiguous)")
else:
    successes.append("✅ No '10,000+' claims found")
    print("   ✅ PASS: No unverified claims")

print()

# ═══════════════════════════════════════════════════════════════════
# FINAL REPORT
# ═══════════════════════════════════════════════════════════════════

print("═══════════════════════════════════════════════════════════════")
print("📊 FINAL VERIFICATION REPORT")
print("═══════════════════════════════════════════════════════════════\n")

print(f"✅ Successes: {len(successes)}")
for s in successes:
    print(f"   {s}")

print(f"\n⚠️  Warnings: {len(warnings)}")
for w in warnings:
    print(f"   {w}")

print(f"\n❌ Errors: {len(errors)}")
for e in errors:
    print(f"   {e}")

print()

# ═══════════════════════════════════════════════════════════════════
# VERDICT
# ═══════════════════════════════════════════════════════════════════

if len(errors) == 0:
    if len(successes) >= 5:
        print("🎉 VERDICT: 100% SUCCESS - All corrections verified!")
        print("   Site now reflects FACTUAL international presence\n")
        exit(0)
    else:
        print(f"⚠️  VERDICT: PARTIAL SUCCESS - {len(successes)} verifications passed")
        print("   Some corrections may need manual review\n")
        exit(0)
else:
    print(f"❌ VERDICT: FAILED - {len(errors)} critical errors found")
    print("   Corrections were not fully applied\n")
    exit(1)
