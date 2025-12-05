#!/usr/bin/env python3
"""
Alpha Medical - Automated Store Validation Script
Comprehensive validation of all store configuration requirements

Date: 2025-11-15
Purpose: Automated validation of SEO, compliance, and configuration
"""

import os
import json
import requests
import re
from datetime import datetime

# Configuration
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
STORE_URL = "https://www.alphamedical.shop"

# Load admin token
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except FileNotFoundError:
    SHOPIFY_TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

if not SHOPIFY_TOKEN:
    print("❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found")
    exit(1)

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# Results storage
results = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "tests": [],
    "summary": {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "warnings": 0
    }
}

def add_result(category, test_name, status, details="", expected="", actual=""):
    """Add test result"""
    result = {
        "category": category,
        "test": test_name,
        "status": status,  # "PASS", "FAIL", "WARN"
        "details": details,
        "expected": expected,
        "actual": actual
    }
    results["tests"].append(result)
    results["summary"]["total"] += 1

    if status == "PASS":
        results["summary"]["passed"] += 1
        print(f"✅ {test_name}")
    elif status == "FAIL":
        results["summary"]["failed"] += 1
        print(f"❌ {test_name}")
        if details:
            print(f"   Details: {details}")
    elif status == "WARN":
        results["summary"]["warnings"] += 1
        print(f"⚠️  {test_name}")
        if details:
            print(f"   Details: {details}")

def graphql_query(query, variables=None):
    """Execute GraphQL query"""
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            return None, data['errors']
        return data.get('data'), None
    return None, f"HTTP {response.status_code}"

def rest_get(endpoint):
    """Execute REST GET request"""
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}{endpoint}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json(), None
    return None, f"HTTP {response.status_code}"

print("="*80)
print("ALPHA MEDICAL - AUTOMATED STORE VALIDATION")
print("="*80)
print(f"Store: {STORE_URL}")
print(f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
print("="*80)

# ============================================================================
# CATEGORY 1: BUNDLES VALIDATION
# ============================================================================
print("\n📦 CATEGORY 1: BUNDLES VALIDATION")
print("-"*80)

# Test 1.1: Bundles collection exists and active
query = """
{
  collection(id: "gid://shopify/Collection/296239169613") {
    id
    title
    products(first: 1) {
      edges {
        node {
          id
        }
      }
    }
  }
}
"""

data, error = graphql_query(query)
if data and data.get('collection'):
    collection = data['collection']
    # Collection exists - we'll count products in next test
    add_result("Bundles", "Bundles collection exists", "PASS",
               expected="Collection 296239169613", actual="Collection found")
elif error:
    add_result("Bundles", "Bundles collection exists", "FAIL",
               details=f"Error: {error}")
else:
    add_result("Bundles", "Bundles collection exists", "FAIL",
               details="Collection 296239169613 not found")

# Test 1.2: Bundle product count and 35% discount
query = """
{
  collection(id: "gid://shopify/Collection/296239169613") {
    products(first: 20) {
      edges {
        node {
          id
          title
          priceRangeV2 {
            minVariantPrice {
              amount
            }
          }
          compareAtPriceRange {
            maxVariantCompareAtPrice {
              amount
            }
          }
        }
      }
    }
  }
}
"""

data, error = graphql_query(query)
if data and data.get('collection'):
    products = data['collection']['products']['edges']
    product_count = len(products)

    # Test bundle count
    if product_count == 15:
        add_result("Bundles", "Bundles collection product count", "PASS",
                   expected="15 products", actual=f"{product_count} products")
    else:
        add_result("Bundles", "Bundles collection product count", "FAIL",
                   f"Expected 15 bundles, found {product_count}",
                   expected="15", actual=str(product_count))

    # Test discounts
    discount_violations = []
    for edge in products:
        product = edge['node']
        price = float(product['priceRangeV2']['minVariantPrice']['amount'])
        compare_price = product['compareAtPriceRange']['maxVariantCompareAtPrice']

        if compare_price:
            compare_amt = float(compare_price['amount'])
            discount = ((compare_amt - price) / compare_amt) * 100

            if abs(discount - 35.0) > 0.5:  # Allow 0.5% tolerance
                discount_violations.append({
                    'title': product['title'][:40],
                    'discount': f"{discount:.1f}%"
                })

    if len(discount_violations) == 0:
        add_result("Bundles", "All bundles have 35% discount", "PASS",
                   expected="35% on all bundles", actual=f"35% on {product_count} bundles")
    else:
        add_result("Bundles", "All bundles have 35% discount", "FAIL",
                   f"{len(discount_violations)} bundles have incorrect discount",
                   expected="35%", actual=str(discount_violations))
else:
    add_result("Bundles", "Bundles collection product count", "FAIL",
               details="Could not fetch collection products")

# ============================================================================
# CATEGORY 2: DRAFT PRODUCTS
# ============================================================================
print("\n📝 CATEGORY 2: DRAFT PRODUCTS VALIDATION")
print("-"*80)

# Test 2.1: All draft products remain draft
query = """
{
  products(first: 10, query: "status:draft") {
    edges {
      node {
        id
        title
        status
        publishedAt
      }
    }
  }
}
"""

data, error = graphql_query(query)
if data:
    drafts = data['products']['edges']
    published_drafts = []

    for edge in drafts:
        product = edge['node']
        if product['status'] != 'DRAFT' or product['publishedAt'] is not None:
            published_drafts.append(product['title'][:40])

    if len(published_drafts) == 0:
        add_result("Compliance", "Draft products stay draft", "PASS",
                   f"{len(drafts)} draft products remain unpublished",
                   expected="All drafts unpublished", actual="All drafts unpublished")
    else:
        add_result("Compliance", "Draft products stay draft", "FAIL",
                   f"{len(published_drafts)} drafts are published",
                   expected="Unpublished", actual=str(published_drafts))

# ============================================================================
# CATEGORY 3: ENGLISH CONTENT
# ============================================================================
print("\n🌐 CATEGORY 3: ENGLISH CONTENT VALIDATION")
print("-"*80)

# Test 3.1: All active products are 100% English
FRENCH_PHRASES = [
    'livraison gratuite', 'frais de port', 'retour gratuit',
    'garantie satisfait', 'sous 30 jours', 'en stock',
    'ajouter au panier', 'acheter maintenant'
]

query = """
{
  products(first: 100, query: "status:active") {
    edges {
      node {
        id
        title
        descriptionHtml
      }
    }
  }
}
"""

data, error = graphql_query(query)
if data:
    products = data['products']['edges']
    french_violations = []

    for edge in products:
        product = edge['node']
        full_text = f"{product['title']} {product.get('descriptionHtml', '')}".lower()

        found_french = [phrase for phrase in FRENCH_PHRASES if phrase in full_text]
        if found_french:
            french_violations.append({
                'title': product['title'][:40],
                'phrases': found_french[:2]
            })

    if len(french_violations) == 0:
        add_result("Compliance", "Site 100% English content", "PASS",
                   f"Analyzed {len(products)} products, 0 French content",
                   expected="100% English", actual="100% English")
    else:
        add_result("Compliance", "Site 100% English content", "FAIL",
                   f"{len(french_violations)} products contain French",
                   expected="100% English", actual=str(french_violations))

# ============================================================================
# CATEGORY 4: METAFIELDS
# ============================================================================
print("\n🏷️  CATEGORY 4: METAFIELDS VALIDATION")
print("-"*80)

# Test 4.1: Loyalty metafield definitions exist
query = """
{
  metafieldDefinitions(first: 20, ownerType: CUSTOMER) {
    edges {
      node {
        namespace
        key
      }
    }
  }
}
"""

data, error = graphql_query(query)
if data:
    definitions = data['metafieldDefinitions']['edges']
    loyalty_defs = [d for d in definitions if d['node']['namespace'] == 'loyalty']

    REQUIRED_LOYALTY_FIELDS = [
        'points', 'tier', 'history', 'signup_bonus_claimed',
        'lifetime_points_earned', 'lifetime_points_redeemed'
    ]

    found_fields = [d['node']['key'] for d in loyalty_defs]
    missing_fields = [f for f in REQUIRED_LOYALTY_FIELDS if f not in found_fields]

    if len(missing_fields) == 0:
        add_result("Metafields", "Loyalty metafield definitions", "PASS",
                   "All 6 loyalty metafield definitions exist",
                   expected="6 definitions", actual=f"{len(found_fields)} definitions")
    else:
        add_result("Metafields", "Loyalty metafield definitions", "FAIL",
                   f"Missing: {', '.join(missing_fields)}",
                   expected="6 definitions", actual=f"{len(found_fields)} definitions")

# Test 4.2: Product metafields populated (sample)
query = """
{
  products(first: 10, query: "status:active") {
    edges {
      node {
        id
        title
        metafields(first: 10) {
          edges {
            node {
              namespace
              key
            }
          }
        }
      }
    }
  }
}
"""

data, error = graphql_query(query)
if data:
    products = data['products']['edges']
    products_with_seo = 0

    for edge in products:
        metafields = edge['node']['metafields']['edges']
        has_title_tag = any(m['node']['namespace'] == 'global' and m['node']['key'] == 'title_tag' for m in metafields)
        has_desc_tag = any(m['node']['namespace'] == 'global' and m['node']['key'] == 'description_tag' for m in metafields)

        if has_title_tag and has_desc_tag:
            products_with_seo += 1

    if products_with_seo >= 8:  # At least 80% of sample
        add_result("Metafields", "Product SEO metafields populated", "PASS",
                   f"{products_with_seo}/10 products have SEO metafields",
                   expected="≥80%", actual=f"{products_with_seo*10}%")
    else:
        add_result("Metafields", "Product SEO metafields populated", "WARN",
                   f"Only {products_with_seo}/10 products have SEO metafields",
                   expected="≥80%", actual=f"{products_with_seo*10}%")

# ============================================================================
# CATEGORY 5: SEO & META TAGS
# ============================================================================
print("\n🔍 CATEGORY 5: SEO & META TAGS VALIDATION")
print("-"*80)

# Test 5.1: Homepage meta tags
try:
    response = requests.get(STORE_URL, timeout=10, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
    if response.status_code == 200:
        html = response.text

        # Check og:image (case-insensitive and flexible matching)
        og_image_pattern = re.compile(r'property=["\']og:image["\']', re.IGNORECASE)
        if og_image_pattern.search(html):
            add_result("SEO", "og:image tag present", "PASS")
        else:
            add_result("SEO", "og:image tag present", "FAIL", "Missing og:image tag")

        # Check twitter:image (case-insensitive and flexible matching)
        twitter_image_pattern = re.compile(r'name=["\']twitter:image["\']', re.IGNORECASE)
        if twitter_image_pattern.search(html):
            add_result("SEO", "twitter:image tag present", "PASS")
        else:
            add_result("SEO", "twitter:image tag present", "FAIL", "Missing twitter:image tag")

        # Check JSON-LD Organization schema
        if '"@type": "Organization"' in html or '"@type":"Organization"' in html:
            add_result("SEO", "Organization schema present", "PASS")
        else:
            add_result("SEO", "Organization schema present", "FAIL", "Missing Organization schema")

        # Check canonical
        if '<link rel="canonical"' in html:
            add_result("SEO", "Canonical tag present", "PASS")
        else:
            add_result("SEO", "Canonical tag present", "FAIL", "Missing canonical tag")
    else:
        add_result("SEO", "og:image tag present", "FAIL", f"HTTP {response.status_code}")
        add_result("SEO", "twitter:image tag present", "FAIL", f"HTTP {response.status_code}")
        add_result("SEO", "Organization schema present", "FAIL", f"HTTP {response.status_code}")
        add_result("SEO", "Canonical tag present", "FAIL", f"HTTP {response.status_code}")
except Exception as e:
    add_result("SEO", "og:image tag present", "FAIL", f"Exception: {str(e)}")
    add_result("SEO", "twitter:image tag present", "FAIL", f"Exception: {str(e)}")
    add_result("SEO", "Organization schema present", "FAIL", f"Exception: {str(e)}")
    add_result("SEO", "Canonical tag present", "FAIL", f"Exception: {str(e)}")

# Test 5.2: Robots.txt AI crawlers
response = requests.get(f"{STORE_URL}/robots.txt", timeout=10)
if response.status_code == 200:
    robots_txt = response.text

    ai_crawlers = ['GPTBot', 'Claude-Web', 'Google-Extended', 'PerplexityBot',
                   'CCBot', 'Applebot-Extended', 'Grok']

    enabled_crawlers = [c for c in ai_crawlers if f"User-agent: {c}" in robots_txt and "Allow: /" in robots_txt]

    if len(enabled_crawlers) == len(ai_crawlers):
        add_result("SEO", "AI crawlers enabled", "PASS",
                   f"All {len(ai_crawlers)} AI crawlers enabled",
                   expected="7 crawlers", actual=f"{len(enabled_crawlers)} crawlers")
    else:
        missing = [c for c in ai_crawlers if c not in enabled_crawlers]
        add_result("SEO", "AI crawlers enabled", "WARN",
                   f"Missing: {', '.join(missing)}",
                   expected="7 crawlers", actual=f"{len(enabled_crawlers)} crawlers")

# Test 5.3: Sitemap accessible
response = requests.get(f"{STORE_URL}/sitemap.xml", timeout=10)
if response.status_code == 200:
    add_result("SEO", "Sitemap accessible", "PASS")
else:
    add_result("SEO", "Sitemap accessible", "FAIL", f"HTTP {response.status_code}")

# Test 5.4: SSL/HTTPS redirect
response = requests.get(f"http://www.alphamedical.shop/", timeout=10, allow_redirects=False)
if response.status_code == 301 and 'https://' in response.headers.get('Location', ''):
    add_result("SEO", "HTTP to HTTPS redirect", "PASS")
else:
    add_result("SEO", "HTTP to HTTPS redirect", "FAIL", f"Expected 301, got {response.status_code}")

# Test 5.5: HSTS header
response = requests.get(STORE_URL, timeout=10)
if 'strict-transport-security' in response.headers:
    add_result("SEO", "HSTS enabled", "PASS")
else:
    add_result("SEO", "HSTS enabled", "WARN", "HSTS header not found")

# ============================================================================
# RESULTS SUMMARY
# ============================================================================
print("\n" + "="*80)
print("VALIDATION SUMMARY")
print("="*80)

summary = results["summary"]
total = summary["total"]
passed = summary["passed"]
failed = summary["failed"]
warnings = summary["warnings"]

pass_rate = (passed / total * 100) if total > 0 else 0
fail_rate = (failed / total * 100) if total > 0 else 0
warn_rate = (warnings / total * 100) if total > 0 else 0

print(f"\nTotal Tests: {total}")
print(f"✅ Passed:   {passed} ({pass_rate:.1f}%)")
print(f"❌ Failed:   {failed} ({fail_rate:.1f}%)")
print(f"⚠️  Warnings: {warnings} ({warn_rate:.1f}%)")

# Overall status
if failed == 0 and warnings == 0:
    print(f"\n🎉 OVERALL STATUS: ✅ ALL TESTS PASSED (100%)")
elif failed == 0:
    print(f"\n✅ OVERALL STATUS: PASSED with {warnings} warnings ({pass_rate:.1f}%)")
else:
    print(f"\n❌ OVERALL STATUS: FAILED - {failed} critical failures")

# Save results to JSON
output_file = "automated_validation_results.json"
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n📄 Full results saved to: {output_file}")
print("="*80)

# Exit code
exit(0 if failed == 0 else 1)
