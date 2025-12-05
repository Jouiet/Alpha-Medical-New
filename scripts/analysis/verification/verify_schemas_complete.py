#!/usr/bin/env python3
"""
VERIFY JSON-LD SCHEMAS - Alpha Medical Care
Validate all structured data schemas compliance

REQUIRED SCHEMAS:
- BreadcrumbList (navigation paths)
- Organization (store info)
- Product (product pages)
- FAQPage (if applicable)
- ProductGroup (for variants)
"""

import requests
import json
import re
from datetime import datetime
from urllib.parse import urljoin

STORE_URL = "https://www.alphamedical.shop"

print("=" * 80)
print("JSON-LD SCHEMAS VALIDATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

def extract_schemas(html):
    """Extract all JSON-LD schemas from HTML"""
    pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    matches = re.findall(pattern, html, re.DOTALL | re.IGNORECASE)

    schemas = []
    for match in matches:
        try:
            schema = json.loads(match.strip())
            schemas.append(schema)
        except json.JSONDecodeError as e:
            print(f"   ⚠️ JSON parse error: {e}")

    return schemas

def validate_page(url, page_type):
    """Validate schemas for a specific page"""
    print(f"\n{'='*80}")
    print(f"PAGE: {page_type.upper()}")
    print(f"URL: {url}")
    print(f"{'='*80}")

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"   ❌ HTTP {response.status_code}")
            return {}

        html = response.text
        schemas = extract_schemas(html)

        print(f"\n   Schemas found: {len(schemas)}")

        schema_types = {}
        for schema in schemas:
            schema_type = schema.get('@type', 'Unknown')
            if isinstance(schema_type, list):
                for t in schema_type:
                    schema_types[t] = schema_types.get(t, 0) + 1
            else:
                schema_types[schema_type] = schema_types.get(schema_type, 0) + 1

            print(f"   - {schema_type}")

            # Validate required fields
            if schema_type == 'BreadcrumbList':
                items = schema.get('itemListElement', [])
                print(f"     ✅ Items: {len(items)}")

            elif schema_type == 'Organization':
                name = schema.get('name')
                url = schema.get('url')
                print(f"     Name: {name}")
                print(f"     URL: {url}")
                if name and url:
                    print(f"     ✅ Valid Organization schema")
                else:
                    print(f"     ⚠️ Missing required fields")

            elif schema_type == 'Product':
                name = schema.get('name')
                offers = schema.get('offers')
                print(f"     Name: {name[:50] if name else 'N/A'}...")
                print(f"     Offers: {'Present' if offers else 'Missing'}")
                if name and offers:
                    print(f"     ✅ Valid Product schema")
                else:
                    print(f"     ⚠️ Missing required fields")

            elif schema_type == 'FAQPage':
                questions = schema.get('mainEntity', [])
                print(f"     ✅ Questions: {len(questions)}")

        return schema_types

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return {}

# Test URLs
pages_to_test = [
    (f"{STORE_URL}/", "Homepage"),
    (f"{STORE_URL}/products/silicone-patellar-tendon-strap-knee-pain-relief", "Product Page"),
    (f"{STORE_URL}/collections/knee-support", "Collection Page"),
    (f"{STORE_URL}/collections/complete-care-kits", "Bundle Collection"),
]

all_schema_types = {}

for url, page_type in pages_to_test:
    schema_types = validate_page(url, page_type)
    for schema_type, count in schema_types.items():
        all_schema_types[schema_type] = all_schema_types.get(schema_type, 0) + count

# Summary
print(f"\n{'='*80}")
print("SCHEMA VALIDATION SUMMARY")
print(f"{'='*80}")

required_schemas = {
    'BreadcrumbList': False,
    'Organization': False,
    'Product': False,
    'FAQPage': False,
    'ProductGroup': False
}

print(f"\n📊 All schema types found across {len(pages_to_test)} pages:")
for schema_type, count in sorted(all_schema_types.items()):
    print(f"   - {schema_type}: {count} occurrences")
    if schema_type in required_schemas:
        required_schemas[schema_type] = True

print(f"\n🎯 REQUIRED SCHEMAS COMPLIANCE:")
for schema_type, found in required_schemas.items():
    status = "✅ PRESENT" if found else "❌ MISSING"
    print(f"   {status}: {schema_type}")

compliance_count = sum(1 for found in required_schemas.values() if found)
compliance_pct = (compliance_count / len(required_schemas)) * 100

print(f"\n📈 COMPLIANCE RATE: {compliance_count}/{len(required_schemas)} ({compliance_pct:.1f}%)")

if compliance_pct < 100:
    print(f"\n⚠️ MISSING SCHEMAS:")
    for schema_type, found in required_schemas.items():
        if not found:
            print(f"   - {schema_type}")
            if schema_type == 'FAQPage':
                print(f"     Note: Optional unless FAQ section exists")
            elif schema_type == 'ProductGroup':
                print(f"     Note: Required for products with variants")

print("\n" + "=" * 80)
