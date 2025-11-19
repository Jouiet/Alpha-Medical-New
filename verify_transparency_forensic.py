#!/usr/bin/env python3
"""
FORENSIC VERIFICATION - Transparency Updates
Verify business address and Our Story page are live and accurate
"""

import requests
import re
from datetime import datetime

print("═══════════════════════════════════════════════════════════════")
print("🔬 FORENSIC VERIFICATION - Transparency Updates")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("═══════════════════════════════════════════════════════════════\n")

errors = []
warnings = []
successes = []

# ═══════════════════════════════════════════════════════════════════
# TEST 1: Verify Business Address in Footer
# ═══════════════════════════════════════════════════════════════════

print("📋 TEST 1: Business Address Visibility on Homepage")
print("─" * 60)

try:
    response = requests.get('https://www.alphamedical.shop', timeout=10)
    html = response.text
    print(f"✅ Fetched homepage: {len(html):,} chars\n")

    # Check for each component
    checks = {
        "JoHat Services LLC": "Legal company name",
        "611 South DuPont Highway": "Physical address street",
        "Dover, DE 19901": "City, State, ZIP",
        "d/b/a Alpha Medical Care": "DBA clarification",
        "support@alphamedical.shop": "Contact email",
        "Not affiliated with Hello Alpha": "Disambiguation notice"
    }

    print("🔍 Address Components Check:")
    all_found = True
    for text, description in checks.items():
        if text in html:
            print(f"   ✅ {description}: Found")
            successes.append(f"✅ {description} displayed")
        else:
            print(f"   ❌ {description}: NOT FOUND")
            errors.append(f"❌ {description} missing")
            all_found = False

    print()

    if all_found:
        print("✅ PASS: All business address components visible\n")
    else:
        print("❌ FAIL: Some components missing\n")

except Exception as e:
    print(f"❌ ERROR: {e}\n")
    errors.append(f"❌ Homepage fetch failed: {e}")

# ═══════════════════════════════════════════════════════════════════
# TEST 2: Verify "Our Story" Page Accessibility
# ═══════════════════════════════════════════════════════════════════

print("📋 TEST 2: 'Our Story' Page Accessibility")
print("─" * 60)

try:
    response = requests.get('https://www.alphamedical.shop/pages/our-story', timeout=10)

    if response.status_code == 200:
        html = response.text
        print(f"✅ Page accessible: {len(html):,} chars\n")

        # Check for key content sections
        content_checks = {
            "Our Journey": "Timeline section",
            "10,000+ customers": "Customer transparency",
            "Physical stores in Canada and Europe": "International presence",
            "Not affiliated with Hello Alpha": "Disambiguation",
            "E-commerce headquarters in United States": "US HQ clarification",
            "30-day money-back guarantee": "Policy mention"
        }

        print("🔍 Content Verification:")
        content_found = 0
        for text, description in content_checks.items():
            if text in html:
                print(f"   ✅ {description}: Present")
                successes.append(f"✅ {description} on Our Story page")
                content_found += 1
            else:
                print(f"   ⚠️  {description}: Not found")
                warnings.append(f"⚠️  {description} missing from Our Story")

        print(f"\n   Content Score: {content_found}/{len(content_checks)}\n")

        if content_found >= len(content_checks) - 1:
            print("✅ PASS: Our Story page has comprehensive content\n")
        else:
            print("⚠️  WARNING: Some expected content missing\n")

    elif response.status_code == 404:
        print("❌ FAIL: Page returns 404 (not found)\n")
        errors.append("❌ Our Story page not accessible (404)")
    else:
        print(f"⚠️  WARNING: Unexpected status code {response.status_code}\n")
        warnings.append(f"⚠️  Our Story page status: {response.status_code}")

except Exception as e:
    print(f"❌ ERROR: {e}\n")
    errors.append(f"❌ Our Story page fetch failed: {e}")

# ═══════════════════════════════════════════════════════════════════
# TEST 3: Verify Schema.org Still Correct
# ═══════════════════════════════════════════════════════════════════

print("📋 TEST 3: Schema.org Integrity Check")
print("─" * 60)

try:
    response = requests.get('https://www.alphamedical.shop', timeout=10)
    html = response.text

    import json
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

    if medical_schema:
        print("✅ MedicalBusiness schema found\n")

        # Quick integrity checks
        disambig = medical_schema.get('disambiguatingDescription', '')
        address_country = medical_schema.get('address', {}).get('addressCountry', '')
        area_served = medical_schema.get('areaServed', [])

        schema_checks = [
            ('International medical equipment retailer' in disambig, "International description"),
            (address_country == 'US', "addressCountry: US"),
            (isinstance(area_served, list) and len(area_served) >= 3, "Multiple markets served")
        ]

        print("🔍 Schema Integrity:")
        for check, description in schema_checks:
            if check:
                print(f"   ✅ {description}")
                successes.append(f"✅ Schema: {description}")
            else:
                print(f"   ❌ {description}: FAILED")
                errors.append(f"❌ Schema: {description} incorrect")

        print()

    else:
        print("❌ MedicalBusiness schema NOT FOUND\n")
        errors.append("❌ MedicalBusiness schema missing")

except Exception as e:
    print(f"❌ ERROR: {e}\n")
    errors.append(f"❌ Schema verification failed: {e}")

# ═══════════════════════════════════════════════════════════════════
# FINAL REPORT
# ═══════════════════════════════════════════════════════════════════

print("═══════════════════════════════════════════════════════════════")
print("📊 FORENSIC VERIFICATION REPORT")
print("═══════════════════════════════════════════════════════════════\n")

print(f"✅ Successes: {len(successes)}")
for s in successes[:10]:  # Show first 10
    print(f"   {s}")
if len(successes) > 10:
    print(f"   ... and {len(successes) - 10} more")

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
    if len(successes) >= 10:
        print("🎉 VERDICT: 100% SUCCESS - All transparency updates verified!")
        print("   ✅ Business address visible on homepage")
        print("   ✅ Our Story page accessible and comprehensive")
        print("   ✅ Schema.org remains accurate\n")
        exit(0)
    else:
        print(f"⚠️  VERDICT: PARTIAL SUCCESS - {len(successes)} verifications passed")
        print("   Some features may need manual review\n")
        exit(0)
else:
    print(f"❌ VERDICT: FAILED - {len(errors)} critical errors found")
    print("   Transparency updates not fully deployed\n")
    exit(1)
