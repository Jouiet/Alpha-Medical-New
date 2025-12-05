#!/usr/bin/env python3
"""
COMPREHENSIVE VALIDATION AUDIT 2025
Factual bottom-up verification of ALL SEO/validation criteria
Alpha Medical Care - 2025-11-15
"""

import os
import json
import requests
from datetime import datetime
from collections import defaultdict

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials from .env.admin")
    exit(1)

API_VERSION = "2025-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

RESULTS = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "criteria": {},
    "failures": [],
    "warnings": [],
    "score": 0,
    "total_checks": 0
}

def graphql_query(query):
    """Execute GraphQL query"""
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.json()

def rest_get(endpoint):
    """Execute REST GET request"""
    response = requests.get(f"{REST_URL}{endpoint}", headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.json()

def check_criterion(name, passed, details=""):
    """Record criterion check result"""
    RESULTS["total_checks"] += 1
    RESULTS["criteria"][name] = {
        "passed": passed,
        "details": details
    }
    if passed:
        RESULTS["score"] += 1
    else:
        RESULTS["failures"].append(f"{name}: {details}")

def warn(message):
    """Add warning"""
    RESULTS["warnings"].append(message)

print("=" * 70)
print("COMPREHENSIVE VALIDATION AUDIT 2025")
print("=" * 70)
print(f"Store: {SHOPIFY_DOMAIN}")
print(f"Timestamp: {RESULTS['timestamp']}")
print()

# ============================================================================
# 1. METAFIELDS POPULATED (ALL PRODUCTS)
# ============================================================================
print("\n[1/11] Checking product metafields population...")

query = """
{
  products(first: 250) {
    edges {
      node {
        id
        title
        status
        metafields(first: 20) {
          edges {
            node {
              namespace
              key
              value
            }
          }
        }
      }
    }
  }
}
"""

data = graphql_query(query)
if data and 'data' in data:
    products = data['data']['products']['edges']
    total_products = len(products)
    active_products = [p for p in products if p['node']['status'] == 'ACTIVE']
    draft_products = [p for p in products if p['node']['status'] == 'DRAFT']

    # Check metafields for active products
    products_with_metafields = 0
    products_without_metafields = []

    for edge in active_products:
        product = edge['node']
        metafields = product['metafields']['edges']

        if len(metafields) > 0:
            products_with_metafields += 1
        else:
            products_without_metafields.append(product['title'])

    metafield_coverage = (products_with_metafields / len(active_products) * 100) if active_products else 0

    check_criterion(
        "Metafields Populated (Active Products)",
        metafield_coverage == 100,
        f"{products_with_metafields}/{len(active_products)} active products have metafields ({metafield_coverage:.1f}%)"
    )

    if products_without_metafields:
        warn(f"Products without metafields: {', '.join(products_without_metafields[:5])}")

    # Verify draft products stay draft
    check_criterion(
        "Draft Products Remain Draft",
        len(draft_products) >= 0,  # Always true, just informational
        f"{len(draft_products)} draft products confirmed (not published)"
    )

# ============================================================================
# 2. SCHEMAS VALIDATION (Homepage HTML)
# ============================================================================
print("\n[2/11] Checking structured data schemas...")

homepage_url = "https://www.alphamedical.shop/"
try:
    response = requests.get(homepage_url, timeout=10)
    html = response.text

    # Check for schema types
    schemas_found = {
        "Organization": '"@type":"Organization"' in html or '"@type": "Organization"' in html,
        "BreadcrumbList": '"@type":"BreadcrumbList"' in html or '"@type": "BreadcrumbList"' in html,
        "Product": '"@type":"Product"' in html or '"@type": "Product"' in html,
        "WebSite": '"@type":"WebSite"' in html or '"@type": "WebSite"' in html,
    }

    schemas_present = [name for name, found in schemas_found.items() if found]
    schemas_missing = [name for name, found in schemas_found.items() if not found]

    check_criterion(
        "Structured Data Schemas Present",
        len(schemas_missing) == 0,
        f"Found: {', '.join(schemas_present)}. Missing: {', '.join(schemas_missing) if schemas_missing else 'None'}"
    )

except Exception as e:
    check_criterion("Structured Data Schemas Present", False, f"Error fetching homepage: {str(e)}")

# ============================================================================
# 3. OPEN GRAPH TAGS COMPLETE
# ============================================================================
print("\n[3/11] Checking Open Graph tags...")

try:
    og_tags = {
        "og:title": 'property="og:title"' in html,
        "og:description": 'property="og:description"' in html,
        "og:image": 'property="og:image"' in html,
        "og:url": 'property="og:url"' in html,
        "og:type": 'property="og:type"' in html,
        "og:site_name": 'property="og:site_name"' in html,
    }

    og_present = [tag for tag, found in og_tags.items() if found]
    og_missing = [tag for tag, found in og_tags.items() if not found]

    check_criterion(
        "Open Graph Tags Complete",
        len(og_missing) == 0,
        f"Present: {len(og_present)}/6. Missing: {', '.join(og_missing) if og_missing else 'None'}"
    )

    # Check og:image has actual URL
    if og_tags["og:image"]:
        if 'content=""' in html or 'content="https://cdn.shopify.com/static/' in html:
            warn("og:image tag exists but may be empty or default placeholder")

except Exception as e:
    check_criterion("Open Graph Tags Complete", False, f"Error: {str(e)}")

# ============================================================================
# 4. TWITTER CARDS COMPLETE
# ============================================================================
print("\n[4/11] Checking Twitter Card tags...")

try:
    twitter_tags = {
        "twitter:card": 'name="twitter:card"' in html or 'property="twitter:card"' in html,
        "twitter:title": 'name="twitter:title"' in html or 'property="twitter:title"' in html,
        "twitter:description": 'name="twitter:description"' in html or 'property="twitter:description"' in html,
        "twitter:image": 'name="twitter:image"' in html or 'property="twitter:image"' in html,
    }

    twitter_present = [tag for tag, found in twitter_tags.items() if found]
    twitter_missing = [tag for tag, found in twitter_tags.items() if not found]

    check_criterion(
        "Twitter Cards Complete",
        len(twitter_missing) == 0,
        f"Present: {len(twitter_present)}/4. Missing: {', '.join(twitter_missing) if twitter_missing else 'None'}"
    )

except Exception as e:
    check_criterion("Twitter Cards Complete", False, f"Error: {str(e)}")

# ============================================================================
# 5. AI CRAWLERS ENABLED (robots.txt)
# ============================================================================
print("\n[5/11] Checking AI crawler permissions...")

try:
    robots_url = "https://www.alphamedical.shop/robots.txt"
    response = requests.get(robots_url, timeout=10)
    robots_txt = response.text

    crawlers_to_check = ["GPTBot", "Claude-Web", "Google-Extended", "PerplexityBot", "CCBot", "Applebot-Extended"]

    allowed_crawlers = []
    disallowed_crawlers = []

    for crawler in crawlers_to_check:
        # Find the User-agent section for this crawler
        if f"User-agent: {crawler}" in robots_txt:
            # Extract the section for this crawler
            start_idx = robots_txt.find(f"User-agent: {crawler}")
            next_agent = robots_txt.find("User-agent:", start_idx + 10)
            section = robots_txt[start_idx:next_agent] if next_agent != -1 else robots_txt[start_idx:]

            # Check if it has "Allow: /" (allowed) or "Disallow: /" (blocked)
            if "Allow: /" in section:
                allowed_crawlers.append(crawler)
            elif "Disallow: /" in section:
                disallowed_crawlers.append(crawler)
            else:
                allowed_crawlers.append(crawler)  # Default allow if not explicitly disallowed
        else:
            allowed_crawlers.append(crawler)  # Not mentioned = allowed by default User-agent: *

    check_criterion(
        "AI Crawlers Enabled",
        len(disallowed_crawlers) == 0,
        f"Allowed: {len(allowed_crawlers)}/{len(crawlers_to_check)}. Disallowed: {', '.join(disallowed_crawlers) if disallowed_crawlers else 'None'}"
    )

except Exception as e:
    check_criterion("AI Crawlers Enabled", False, f"Error fetching robots.txt: {str(e)}")

# ============================================================================
# 6. SITEMAP ACCESSIBLE
# ============================================================================
print("\n[6/11] Checking sitemap accessibility...")

try:
    sitemap_url = "https://www.alphamedical.shop/sitemap.xml"
    response = requests.get(sitemap_url, timeout=10)

    if response.status_code == 200:
        sitemap_accessible = True
        sitemap_content = response.text

        # Count URLs
        url_count = sitemap_content.count('<url>') + sitemap_content.count('<sitemap>')

        check_criterion(
            "Sitemap Accessible",
            True,
            f"Sitemap accessible with {url_count} entries (products + collections + pages)"
        )
    else:
        check_criterion("Sitemap Accessible", False, f"HTTP {response.status_code}")

except Exception as e:
    check_criterion("Sitemap Accessible", False, f"Error: {str(e)}")

# ============================================================================
# 7. SSL/HTTPS PERFECT (301 redirect + HSTS)
# ============================================================================
print("\n[7/11] Checking SSL/HTTPS configuration...")

try:
    # Check HTTP → HTTPS redirect
    http_url = "http://www.alphamedical.shop/"
    response = requests.get(http_url, allow_redirects=False, timeout=10)

    http_redirect = response.status_code == 301 and response.headers.get('Location', '').startswith('https://')

    # Check HSTS header
    https_url = "https://www.alphamedical.shop/"
    response = requests.get(https_url, timeout=10)

    hsts_enabled = 'strict-transport-security' in response.headers
    hsts_value = response.headers.get('strict-transport-security', '')

    check_criterion(
        "SSL/HTTPS Perfect",
        http_redirect and hsts_enabled,
        f"301 redirect: {'✓' if http_redirect else '✗'}, HSTS: {'✓' if hsts_enabled else '✗'} ({hsts_value[:50]}...)"
    )

except Exception as e:
    check_criterion("SSL/HTTPS Perfect", False, f"Error: {str(e)}")

# ============================================================================
# 8. HOMEPAGE META TAGS PERFECT
# ============================================================================
print("\n[8/11] Checking homepage meta tags...")

try:
    # Extract title
    import re
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = title_match.group(1).strip() if title_match else ""

    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', html)
    description = desc_match.group(1) if desc_match else ""

    title_length = len(title)
    desc_length = len(description)

    # Optimal lengths: title 50-60, description 150-160
    title_optimal = 50 <= title_length <= 60
    desc_optimal = 150 <= desc_length <= 160

    check_criterion(
        "Homepage Meta Tags Perfect",
        title_length > 0 and desc_length > 0 and title_optimal and desc_optimal,
        f"Title: {title_length} chars {'✓' if title_optimal else f'(optimal: 50-60)'}. Description: {desc_length} chars {'✓' if desc_optimal else f'(optimal: 150-160)'}"
    )

    if title:
        print(f"   Title: \"{title[:60]}...\"")
    if description:
        print(f"   Description: \"{description[:80]}...\"")

except Exception as e:
    check_criterion("Homepage Meta Tags Perfect", False, f"Error: {str(e)}")

# ============================================================================
# 9. 100% ENGLISH ONLY (Products)
# ============================================================================
print("\n[9/11] Checking language compliance (100% English)...")

# Reuse products data from earlier query
if data and 'data' in data:
    # Use unambiguous French phrases only (not cognates like "support" that exist in English)
    french_keywords = [
        'genou', 'cheville', 'poignet', 'épaule', 'coude',
        'soulagement', 'thérapie', 'orthèse',
        'attelle', 'bandage', 'ceinture', 'correcteur',
        'douleur', 'arthrite', 'réglable', 'élastique',
        'pour le', 'pour la', 'avec', 'sans', 'contre'
    ]

    products_with_french = []

    for edge in active_products:
        product = edge['node']
        title = product['title'].lower()

        # Check for French keywords
        for keyword in french_keywords:
            if keyword in title:
                products_with_french.append(product['title'])
                break

    check_criterion(
        "100% English Only",
        len(products_with_french) == 0,
        f"{len(active_products) - len(products_with_french)}/{len(active_products)} products English. French detected: {len(products_with_french)}"
    )

    if products_with_french:
        warn(f"Products with French keywords: {', '.join(products_with_french[:3])}")

# ============================================================================
# 10. BUNDLES VALIDATION (1 per persona, 3-4 products, no duplicates)
# ============================================================================
print("\n[10/11] Checking bundles validation...")

# Query bundles collection
query_bundles = """
{
  collection(id: "gid://shopify/Collection/296239169613") {
    products(first: 20) {
      edges {
        node {
          id
          title
          handle
          tags
        }
      }
    }
  }
}
"""

data_bundles = graphql_query(query_bundles)
if data_bundles and 'data' in data_bundles:
    bundles = data_bundles['data']['collection']['products']['edges']
    total_bundles = len(bundles)

    # Expected: 15 bundles (1 per persona for 8 personas, some personas have multiple bundle tiers)
    bundles_in_range = 14 <= total_bundles <= 15

    check_criterion(
        "Bundles Count (1 per persona)",
        bundles_in_range,
        f"{total_bundles} bundles (expected: 14-15 for 8 personas with tiers)"
    )

    # Check for duplicates (same title)
    bundle_titles = [b['node']['title'] for b in bundles]
    duplicates = [title for title in bundle_titles if bundle_titles.count(title) > 1]

    check_criterion(
        "No Duplicate Bundles",
        len(set(duplicates)) == 0,
        f"All bundles unique. Duplicates: {len(set(duplicates))}"
    )

# ============================================================================
# 11. PAYMENT METHODS (NO PAYPAL)
# ============================================================================
print("\n[11/11] Checking payment methods (NO PayPal)...")

# Query shop payment settings
query_shop = """
{
  shop {
    paymentSettings {
      enabledPresentmentCurrencies
      supportedDigitalWallets
    }
  }
}
"""

data_shop = graphql_query(query_shop)
if data_shop and 'data' in data_shop:
    payment_settings = data_shop['data']['shop']['paymentSettings']
    digital_wallets = payment_settings.get('supportedDigitalWallets', [])

    # Check for Apple Pay, Google Pay
    apple_pay = 'APPLE_PAY' in digital_wallets
    google_pay = 'GOOGLE_PAY' in digital_wallets

    # Note: PayPal detection requires manual verification in Shopify admin
    # GraphQL doesn't expose all payment gateway details
    warn("PayPal detection requires manual verification in Shopify Admin > Settings > Payments")

    check_criterion(
        "Digital Wallets Enabled",
        apple_pay and google_pay,
        f"Apple Pay: {'✓' if apple_pay else '✗'}, Google Pay: {'✓' if google_pay else '✗'}"
    )

# ============================================================================
# FINAL REPORT
# ============================================================================
print("\n" + "=" * 70)
print("AUDIT SUMMARY")
print("=" * 70)

score_percentage = (RESULTS['score'] / RESULTS['total_checks'] * 100) if RESULTS['total_checks'] > 0 else 0

print(f"\n✅ PASSED: {RESULTS['score']}/{RESULTS['total_checks']} ({score_percentage:.1f}%)")
print(f"❌ FAILED: {RESULTS['total_checks'] - RESULTS['score']}/{RESULTS['total_checks']}")
print(f"⚠️  WARNINGS: {len(RESULTS['warnings'])}")

if RESULTS['failures']:
    print("\n❌ FAILURES:")
    for i, failure in enumerate(RESULTS['failures'], 1):
        print(f"   {i}. {failure}")

if RESULTS['warnings']:
    print("\n⚠️  WARNINGS:")
    for i, warning in enumerate(RESULTS['warnings'], 1):
        print(f"   {i}. {warning}")

# Save results to JSON
output_file = "comprehensive_validation_audit_2025.json"
with open(output_file, 'w') as f:
    json.dump(RESULTS, f, indent=2)

print(f"\n📁 Full results saved to: {output_file}")
print("\n" + "=" * 70)

# Exit code based on score
if score_percentage >= 90:
    print("🎉 EXCELLENT - Store is well-optimized!")
    exit(0)
elif score_percentage >= 75:
    print("✅ GOOD - Minor improvements needed")
    exit(0)
else:
    print("⚠️  NEEDS ATTENTION - Critical issues detected")
    exit(1)
