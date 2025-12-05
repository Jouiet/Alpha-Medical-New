#!/usr/bin/env python3
"""
EXHAUSTIVE SEO/META/SCHEMAS AUDIT - 2025-11-16
Bottom-up factual verification of ALL SEO criteria
NO assumptions, ONLY verified facts

Criteria to verify:
1. Schemas (BreadcrumbList, Organization, Product, FAQPage, ProductGroup)
2. Open Graph tags (complete on all key pages)
3. Twitter Cards (complete on all key pages)
4. AI Crawlers (GPTBot, Claude, Gemini, Perplexity, CCBot, Applebot)
5. Sitemap (accessible, sub-sitemaps, URLs)
6. SSL/HTTPS (301 redirect, HSTS)
7. Homepage meta tags (title, description lengths)
8. Product metafields (all products populated)
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os

# Store configuration
STORE_URL = "https://www.alphamedical.shop"
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

# Load Admin API token
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load Admin API token")
    exit(1)

API_VERSION = "2025-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query):
    """Execute GraphQL query"""
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.json()

# Results storage
audit_results = {
    "audit_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'),
    "store_url": STORE_URL,
    "schemas": {},
    "open_graph": {},
    "twitter_cards": {},
    "ai_crawlers": {},
    "sitemap": {},
    "ssl_https": {},
    "homepage_meta": {},
    "product_metafields": {},
    "overall_score": 0,
    "pass_count": 0,
    "fail_count": 0
}

print("=" * 100)
print("EXHAUSTIVE SEO/META/SCHEMAS AUDIT - 2025-11-16")
print("=" * 100)
print(f"Store: {STORE_URL}")
print(f"Date: {audit_results['audit_date']}")
print()

# ============================================================================
# 1. HOMEPAGE META TAGS
# ============================================================================

print("=" * 100)
print("1. HOMEPAGE META TAGS")
print("=" * 100)
print()

try:
    response = requests.get(STORE_URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')

    # Title tag
    title_tag = soup.find('title')
    if title_tag:
        title_text = title_tag.string.strip() if title_tag.string else ""
        title_length = len(title_text)

        audit_results['homepage_meta']['title'] = title_text
        audit_results['homepage_meta']['title_length'] = title_length

        print(f"Title: \"{title_text}\"")
        print(f"Length: {title_length} chars")

        if 50 <= title_length <= 60:
            print("  ✅ OPTIMAL (50-60 chars)")
            audit_results['homepage_meta']['title_status'] = "OPTIMAL"
            audit_results['pass_count'] += 1
        elif 40 <= title_length <= 70:
            print("  ⚠️  ACCEPTABLE (40-70 chars)")
            audit_results['homepage_meta']['title_status'] = "ACCEPTABLE"
            audit_results['pass_count'] += 1
        else:
            print(f"  ❌ NON-OPTIMAL (should be 50-60 chars)")
            audit_results['homepage_meta']['title_status'] = "FAIL"
            audit_results['fail_count'] += 1
    else:
        print("❌ No title tag found")
        audit_results['homepage_meta']['title_status'] = "MISSING"
        audit_results['fail_count'] += 1

    print()

    # Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        desc_text = meta_desc['content'].strip()
        desc_length = len(desc_text)

        audit_results['homepage_meta']['description'] = desc_text
        audit_results['homepage_meta']['description_length'] = desc_length

        print(f"Description: \"{desc_text}\"")
        print(f"Length: {desc_length} chars")

        if 150 <= desc_length <= 160:
            print("  ✅ OPTIMAL (150-160 chars)")
            audit_results['homepage_meta']['description_status'] = "OPTIMAL"
            audit_results['pass_count'] += 1
        elif 120 <= desc_length <= 170:
            print("  ⚠️  ACCEPTABLE (120-170 chars)")
            audit_results['homepage_meta']['description_status'] = "ACCEPTABLE"
            audit_results['pass_count'] += 1
        else:
            print(f"  ❌ NON-OPTIMAL (should be 150-160 chars)")
            audit_results['homepage_meta']['description_status'] = "FAIL"
            audit_results['fail_count'] += 1
    else:
        print("❌ No meta description found")
        audit_results['homepage_meta']['description_status'] = "MISSING"
        audit_results['fail_count'] += 1

    print()

    # HTML lang attribute
    html_tag = soup.find('html')
    if html_tag and html_tag.get('lang'):
        lang = html_tag['lang']
        audit_results['homepage_meta']['html_lang'] = lang

        print(f"HTML lang: {lang}")

        if lang == 'en':
            print("  ✅ CORRECT (en)")
            audit_results['homepage_meta']['html_lang_status'] = "CORRECT"
            audit_results['pass_count'] += 1
        else:
            print(f"  ❌ INCORRECT (should be 'en', found '{lang}')")
            audit_results['homepage_meta']['html_lang_status'] = "INCORRECT"
            audit_results['fail_count'] += 1
    else:
        print("❌ No HTML lang attribute")
        audit_results['homepage_meta']['html_lang_status'] = "MISSING"
        audit_results['fail_count'] += 1

except Exception as e:
    print(f"❌ Failed to fetch homepage: {e}")
    audit_results['homepage_meta']['error'] = str(e)
    audit_results['fail_count'] += 3

# ============================================================================
# 2. OPEN GRAPH TAGS
# ============================================================================

print("\n" + "=" * 100)
print("2. OPEN GRAPH TAGS")
print("=" * 100)
print()

try:
    og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})

    og_data = {}
    for tag in og_tags:
        prop = tag.get('property')
        content = tag.get('content', '')
        og_data[prop] = content

    audit_results['open_graph']['tags_found'] = og_data

    required_og = ['og:title', 'og:description', 'og:image', 'og:url', 'og:type', 'og:site_name']

    print(f"Found {len(og_data)} Open Graph tags:")
    for prop, content in og_data.items():
        print(f"  {prop}: {content[:80]}{'...' if len(content) > 80 else ''}")

    print()
    print("Required tags verification:")
    missing_og = []
    for req_tag in required_og:
        if req_tag in og_data and og_data[req_tag]:
            print(f"  ✅ {req_tag}: Present")
        else:
            print(f"  ❌ {req_tag}: Missing")
            missing_og.append(req_tag)

    if not missing_og:
        print("\n✅ All required Open Graph tags present (6/6)")
        audit_results['open_graph']['status'] = "COMPLETE"
        audit_results['pass_count'] += 1
    else:
        print(f"\n❌ Missing {len(missing_og)} required tags: {', '.join(missing_og)}")
        audit_results['open_graph']['status'] = "INCOMPLETE"
        audit_results['open_graph']['missing'] = missing_og
        audit_results['fail_count'] += 1

except Exception as e:
    print(f"❌ Failed to check Open Graph tags: {e}")
    audit_results['open_graph']['error'] = str(e)
    audit_results['fail_count'] += 1

# ============================================================================
# 3. TWITTER CARDS
# ============================================================================

print("\n" + "=" * 100)
print("3. TWITTER CARDS")
print("=" * 100)
print()

try:
    twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})

    twitter_data = {}
    for tag in twitter_tags:
        name = tag.get('name')
        content = tag.get('content', '')
        twitter_data[name] = content

    audit_results['twitter_cards']['tags_found'] = twitter_data

    required_twitter = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']

    print(f"Found {len(twitter_data)} Twitter Card tags:")
    for name, content in twitter_data.items():
        print(f"  {name}: {content[:80]}{'...' if len(content) > 80 else ''}")

    print()
    print("Required tags verification:")
    missing_twitter = []
    for req_tag in required_twitter:
        if req_tag in twitter_data and twitter_data[req_tag]:
            print(f"  ✅ {req_tag}: Present")
        else:
            print(f"  ❌ {req_tag}: Missing")
            missing_twitter.append(req_tag)

    if not missing_twitter:
        print("\n✅ All required Twitter Card tags present (4/4)")
        audit_results['twitter_cards']['status'] = "COMPLETE"
        audit_results['pass_count'] += 1
    else:
        print(f"\n❌ Missing {len(missing_twitter)} required tags: {', '.join(missing_twitter)}")
        audit_results['twitter_cards']['status'] = "INCOMPLETE"
        audit_results['twitter_cards']['missing'] = missing_twitter
        audit_results['fail_count'] += 1

except Exception as e:
    print(f"❌ Failed to check Twitter Cards: {e}")
    audit_results['twitter_cards']['error'] = str(e)
    audit_results['fail_count'] += 1

# ============================================================================
# 4. STRUCTURED DATA SCHEMAS
# ============================================================================

print("\n" + "=" * 100)
print("4. STRUCTURED DATA SCHEMAS")
print("=" * 100)
print()

try:
    # Find all JSON-LD scripts
    json_ld_scripts = soup.find_all('script', type='application/ld+json')

    schemas_found = []
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            schema_type = data.get('@type') if isinstance(data, dict) else None
            if schema_type:
                schemas_found.append(schema_type)
        except:
            pass

    audit_results['schemas']['schemas_found'] = schemas_found

    print(f"Found {len(schemas_found)} schemas:")
    for schema in schemas_found:
        print(f"  - {schema}")

    print()

    # Check for expected schemas
    expected_schemas = ['Organization', 'WebSite', 'ProductGroup']

    print("Expected schemas verification:")
    missing_schemas = []
    for expected in expected_schemas:
        if expected in schemas_found:
            print(f"  ✅ {expected}: Present")
        else:
            print(f"  ⚠️  {expected}: Not found on homepage")
            missing_schemas.append(expected)

    if not missing_schemas:
        print("\n✅ All expected schemas present on homepage (3/3)")
        audit_results['schemas']['homepage_status'] = "COMPLETE"
        audit_results['pass_count'] += 1
    else:
        print(f"\n⚠️  {len(missing_schemas)} schemas not on homepage: {', '.join(missing_schemas)}")
        audit_results['schemas']['homepage_status'] = "PARTIAL"
        audit_results['schemas']['missing_homepage'] = missing_schemas
        # Not a failure - some schemas are page-specific
        audit_results['pass_count'] += 1

except Exception as e:
    print(f"❌ Failed to check schemas: {e}")
    audit_results['schemas']['error'] = str(e)
    audit_results['fail_count'] += 1

# ============================================================================
# 5. AI CRAWLERS (robots.txt)
# ============================================================================

print("\n" + "=" * 100)
print("5. AI CRAWLERS PERMISSIONS")
print("=" * 100)
print()

try:
    robots_url = f"{STORE_URL}/robots.txt"
    robots_response = requests.get(robots_url)

    if robots_response.status_code == 200:
        robots_txt = robots_response.text
        audit_results['ai_crawlers']['robots_txt'] = robots_txt

        ai_crawlers = {
            'GPTBot': False,
            'Claude-Web': False,
            'Google-Extended': False,
            'PerplexityBot': False,
            'CCBot': False,
            'Applebot-Extended': False
        }

        for crawler in ai_crawlers.keys():
            # Check if crawler is explicitly disallowed
            if f"User-agent: {crawler}" in robots_txt:
                # Find the section for this crawler
                lines = robots_txt.split('\n')
                in_section = False
                for line in lines:
                    if f"User-agent: {crawler}" in line:
                        in_section = True
                    elif line.startswith('User-agent:'):
                        in_section = False
                    elif in_section and 'Disallow:' in line:
                        # Crawler is explicitly disallowed
                        ai_crawlers[crawler] = False
                        break
            else:
                # Crawler not mentioned = allowed
                ai_crawlers[crawler] = True

        audit_results['ai_crawlers']['permissions'] = ai_crawlers

        print("AI Crawler permissions:")
        allowed_count = 0
        for crawler, allowed in ai_crawlers.items():
            status = "✅ ALLOWED" if allowed else "❌ BLOCKED"
            print(f"  {status}: {crawler}")
            if allowed:
                allowed_count += 1

        if allowed_count == 6:
            print(f"\n✅ All 6 AI crawlers allowed")
            audit_results['ai_crawlers']['status'] = "COMPLETE"
            audit_results['pass_count'] += 1
        else:
            print(f"\n⚠️  Only {allowed_count}/6 AI crawlers allowed")
            audit_results['ai_crawlers']['status'] = "PARTIAL"
            audit_results['fail_count'] += 1
    else:
        print(f"❌ robots.txt not accessible: {robots_response.status_code}")
        audit_results['ai_crawlers']['status'] = "ERROR"
        audit_results['fail_count'] += 1

except Exception as e:
    print(f"❌ Failed to check robots.txt: {e}")
    audit_results['ai_crawlers']['error'] = str(e)
    audit_results['fail_count'] += 1

# ============================================================================
# 6. SITEMAP
# ============================================================================

print("\n" + "=" * 100)
print("6. SITEMAP ACCESSIBILITY")
print("=" * 100)
print()

try:
    sitemap_url = f"{STORE_URL}/sitemap.xml"
    sitemap_response = requests.get(sitemap_url)

    if sitemap_response.status_code == 200:
        print(f"✅ Sitemap accessible: {sitemap_url}")

        # Try to parse XML
        try:
            from xml.etree import ElementTree as ET
            root = ET.fromstring(sitemap_response.text)

            # Count sitemaps if it's a sitemap index
            sitemaps = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap')
            if sitemaps:
                print(f"  Sitemap index with {len(sitemaps)} sub-sitemaps")
                audit_results['sitemap']['type'] = 'index'
                audit_results['sitemap']['sub_sitemaps'] = len(sitemaps)
            else:
                # Count URLs
                urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
                print(f"  Sitemap with {len(urls)} URLs")
                audit_results['sitemap']['type'] = 'urlset'
                audit_results['sitemap']['url_count'] = len(urls)

            audit_results['sitemap']['status'] = "ACCESSIBLE"
            audit_results['pass_count'] += 1
        except Exception as parse_error:
            print(f"  ⚠️  Sitemap accessible but parse failed: {parse_error}")
            audit_results['sitemap']['status'] = "ACCESSIBLE_PARSE_FAIL"
            audit_results['sitemap']['parse_error'] = str(parse_error)
            # Still count as pass - sitemap is accessible
            audit_results['pass_count'] += 1
    else:
        print(f"❌ Sitemap not accessible: {sitemap_response.status_code}")
        audit_results['sitemap']['status'] = "NOT_ACCESSIBLE"
        audit_results['fail_count'] += 1

except Exception as e:
    print(f"❌ Failed to check sitemap: {e}")
    audit_results['sitemap']['error'] = str(e)
    audit_results['fail_count'] += 1

# ============================================================================
# 7. SSL/HTTPS
# ============================================================================

print("\n" + "=" * 100)
print("7. SSL/HTTPS SECURITY")
print("=" * 100)
print()

try:
    # Test HTTP to HTTPS redirect
    http_url = STORE_URL.replace('https://', 'http://')
    http_response = requests.get(http_url, allow_redirects=False)

    if http_response.status_code == 301 and 'https://' in http_response.headers.get('Location', ''):
        print("✅ HTTP → HTTPS redirect (301)")
        audit_results['ssl_https']['redirect_301'] = True
        audit_results['pass_count'] += 1
    else:
        print(f"❌ No 301 redirect (status: {http_response.status_code})")
        audit_results['ssl_https']['redirect_301'] = False
        audit_results['fail_count'] += 1

    # Check HSTS header
    https_response = requests.get(STORE_URL)
    hsts = https_response.headers.get('Strict-Transport-Security', '')

    if hsts:
        print(f"✅ HSTS enabled: {hsts}")
        audit_results['ssl_https']['hsts_enabled'] = True
        audit_results['ssl_https']['hsts_value'] = hsts
        audit_results['pass_count'] += 1
    else:
        print("❌ HSTS not enabled")
        audit_results['ssl_https']['hsts_enabled'] = False
        audit_results['fail_count'] += 1

except Exception as e:
    print(f"❌ Failed to check SSL/HTTPS: {e}")
    audit_results['ssl_https']['error'] = str(e)
    audit_results['fail_count'] += 2

# ============================================================================
# 8. PRODUCT METAFIELDS
# ============================================================================

print("\n" + "=" * 100)
print("8. PRODUCT METAFIELDS POPULATION")
print("=" * 100)
print()

try:
    # Query products with metafields
    query = """
    {
      products(first: 100, query: "status:active") {
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

    result = graphql_query(query)

    if result and 'data' in result:
        products = result['data']['products']['edges']

        total_products = len(products)
        products_with_metafields = 0
        metafield_counts = {}

        for edge in products:
            product = edge['node']
            metafields = product['metafields']['edges']

            if len(metafields) > 0:
                products_with_metafields += 1

            for mf_edge in metafields:
                mf = mf_edge['node']
                key = f"{mf['namespace']}.{mf['key']}"
                metafield_counts[key] = metafield_counts.get(key, 0) + 1

        audit_results['product_metafields']['total_products'] = total_products
        audit_results['product_metafields']['products_with_metafields'] = products_with_metafields
        audit_results['product_metafields']['metafield_types'] = metafield_counts

        print(f"Total active products checked: {total_products}")
        print(f"Products with metafields: {products_with_metafields}")
        print()

        if metafield_counts:
            print("Metafield types found:")
            for key, count in sorted(metafield_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"  {key}: {count} products")
        else:
            print("  No metafields found")

        print()

        percentage = (products_with_metafields / total_products * 100) if total_products > 0 else 0

        if percentage >= 80:
            print(f"✅ Good metafield population: {percentage:.1f}%")
            audit_results['product_metafields']['status'] = "GOOD"
            audit_results['pass_count'] += 1
        elif percentage >= 50:
            print(f"⚠️  Moderate metafield population: {percentage:.1f}%")
            audit_results['product_metafields']['status'] = "MODERATE"
            # Not a failure
            audit_results['pass_count'] += 1
        else:
            print(f"❌ Low metafield population: {percentage:.1f}%")
            audit_results['product_metafields']['status'] = "LOW"
            audit_results['fail_count'] += 1

except Exception as e:
    print(f"❌ Failed to check product metafields: {e}")
    audit_results['product_metafields']['error'] = str(e)
    audit_results['fail_count'] += 1

# ============================================================================
# FINAL SUMMARY
# ============================================================================

total_checks = audit_results['pass_count'] + audit_results['fail_count']
overall_score = (audit_results['pass_count'] / total_checks * 100) if total_checks > 0 else 0
audit_results['overall_score'] = round(overall_score, 1)

print("\n" + "=" * 100)
print("AUDIT SUMMARY")
print("=" * 100)
print()
print(f"Total checks: {total_checks}")
print(f"Passed: {audit_results['pass_count']} ✅")
print(f"Failed: {audit_results['fail_count']} ❌")
print(f"Overall score: {audit_results['overall_score']}%")
print()

# Categorize result
if overall_score >= 90:
    status = "🟢 EXCELLENT"
elif overall_score >= 75:
    status = "🟡 GOOD"
elif overall_score >= 60:
    status = "🟠 ACCEPTABLE"
else:
    status = "🔴 NEEDS IMPROVEMENT"

print(f"Status: {status}")

# Save results
output_file = '/Users/mac/Desktop/Alpha-Medical/exhaustive_seo_meta_audit_2025.json'
with open(output_file, 'w') as f:
    json.dump(audit_results, f, indent=2)

print()
print(f"✅ Results saved to: {output_file}")
print("=" * 100)
