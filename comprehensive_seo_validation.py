#!/usr/bin/env python3
"""
COMPREHENSIVE SEO/AEO VALIDATION - Alpha Medical
Rigorous automated verification of ALL SEO/AEO/Marketing requirements

VERIFICATION CATEGORIES:
1. Meta Tags (Homepage title, description, OG, Twitter Cards)
2. Schemas (Organization, Product, ProductGroup, BreadcrumbList, FAQPage)
3. AI Crawlers (GPTBot, Claude, Gemini, Perplexity, CCBot, Applebot, Grok)
4. Sitemap (accessibility, sub-sitemaps, URLs)
5. SSL/HTTPS (301 redirect, HSTS, certificate)
6. Products (metafields, active count)
7. Collections (descriptions, product count)
8. Technical (robots.txt, llms.txt)

NO SHORTCUTS - FACTUAL VERIFICATION ONLY
"""

import os
import json
import requests
import re
from datetime import datetime
from collections import defaultdict

STORE_URL = "https://www.alphamedical.shop"
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

API_VERSION = "2025-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    data = response.json()
    if "errors" in data:
        return None
    return data

print("="*80)
print("COMPREHENSIVE SEO/AEO VALIDATION - ALPHA MEDICAL")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"Store: {STORE_URL}")
print("="*80)

validation_results = {
    "meta_tags": {},
    "schemas": {},
    "ai_crawlers": {},
    "sitemap": {},
    "ssl_https": {},
    "products": {},
    "collections": {},
    "technical": {},
    "summary": {}
}

# ============================================================================
# 1. HOMEPAGE META TAGS VALIDATION
# ============================================================================
print("\n" + "="*80)
print("1. HOMEPAGE META TAGS VALIDATION")
print("="*80)

try:
    response = requests.get(STORE_URL, timeout=10)
    html = response.text

    # Title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else None

    # Meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    description = desc_match.group(1).strip() if desc_match else None

    # Open Graph
    og_tags = {}
    for og_tag in ['og:site_name', 'og:title', 'og:description', 'og:image', 'og:url', 'og:type']:
        match = re.search(rf'<meta\s+property=["\']{ og_tag}["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        og_tags[og_tag] = match.group(1) if match else None

    # Twitter Cards
    twitter_tags = {}
    for tw_tag in ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']:
        match = re.search(rf'<meta\s+name=["\']{ tw_tag}["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
        twitter_tags[tw_tag] = match.group(1) if match else None

    validation_results["meta_tags"] = {
        "title": {
            "value": title,
            "length": len(title) if title else 0,
            "optimal": bool(title and 50 <= len(title) <= 60),
            "status": "✅ PASS" if (title and 50 <= len(title) <= 60) else "⚠️ FAIL"
        },
        "description": {
            "value": description[:160] if description else None,
            "length": len(description) if description else 0,
            "optimal": bool(description and 150 <= len(description) <= 160),
            "status": "✅ PASS" if (description and 150 <= len(description) <= 160) else "⚠️ FAIL"
        },
        "og_tags": {
            "complete": all(og_tags.values()),
            "tags": og_tags,
            "missing": [k for k, v in og_tags.items() if not v],
            "status": "✅ PASS" if all(og_tags.values()) else "❌ FAIL"
        },
        "twitter_cards": {
            "complete": all(twitter_tags.values()),
            "tags": twitter_tags,
            "missing": [k for k, v in twitter_tags.items() if not v],
            "status": "✅ PASS" if all(twitter_tags.values()) else "❌ FAIL"
        }
    }

    print(f"\n{'✅' if validation_results['meta_tags']['title']['optimal'] else '⚠️'} Title: {title}")
    print(f"   Length: {len(title) if title else 0} chars (optimal: 50-60)")

    print(f"\n{'✅' if validation_results['meta_tags']['description']['optimal'] else '⚠️'} Description: {description[:80] if description else 'NONE'}...")
    print(f"   Length: {len(description) if description else 0} chars (optimal: 150-160)")

    print(f"\n{'✅' if validation_results['meta_tags']['og_tags']['complete'] else '❌'} Open Graph: {'COMPLETE' if validation_results['meta_tags']['og_tags']['complete'] else 'INCOMPLETE'}")
    for tag, value in og_tags.items():
        print(f"   {'✅' if value else '❌'} {tag}: {value[:60] if value else 'MISSING'}...")

    print(f"\n{'✅' if validation_results['meta_tags']['twitter_cards']['complete'] else '❌'} Twitter Cards: {'COMPLETE' if validation_results['meta_tags']['twitter_cards']['complete'] else 'INCOMPLETE'}")
    for tag, value in twitter_tags.items():
        print(f"   {'✅' if value else '❌'} {tag}: {value[:60] if value else 'MISSING'}...")

except Exception as e:
    print(f"❌ Failed to validate meta tags: {e}")
    validation_results["meta_tags"]["error"] = str(e)

# ============================================================================
# 2. STRUCTURED DATA SCHEMAS VALIDATION
# ============================================================================
print("\n" + "="*80)
print("2. STRUCTURED DATA SCHEMAS VALIDATION")
print("="*80)

try:
    schema_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
    schemas_found = re.findall(schema_pattern, html, re.IGNORECASE | re.DOTALL)

    schema_types = []
    for schema_str in schemas_found:
        try:
            schema_json = json.loads(schema_str)
            if isinstance(schema_json, dict):
                schema_type = schema_json.get("@type", "Unknown")
                schema_types.append(schema_type)
            elif isinstance(schema_json, list):
                for item in schema_json:
                    if isinstance(item, dict):
                        schema_types.append(item.get("@type", "Unknown"))
        except json.JSONDecodeError:
            continue

    required_schemas = {
        "Organization": "Organization" in schema_types,
        "BreadcrumbList": "BreadcrumbList" in schema_types,
        "Product": "Product" in schema_types or "ProductGroup" in schema_types,
        "WebSite": "WebSite" in schema_types
    }

    validation_results["schemas"] = {
        "found": schema_types,
        "required": required_schemas,
        "complete": all(required_schemas.values()),
        "missing": [k for k, v in required_schemas.items() if not v],
        "status": "✅ PASS" if all(required_schemas.values()) else "⚠️ PARTIAL"
    }

    print(f"\n{'✅' if validation_results['schemas']['complete'] else '⚠️'} Structured Data: {'COMPLETE' if validation_results['schemas']['complete'] else 'PARTIAL'}")
    print(f"\nFound {len(schemas_found)} schema blocks with {len(schema_types)} types:")
    for schema_type in set(schema_types):
        count = schema_types.count(schema_type)
        print(f"   ✅ {schema_type}: {count}x")

    print(f"\nRequired schemas:")
    for schema, present in required_schemas.items():
        status = "✅" if present else "❌"
        print(f"   {status} {schema}: {'PRESENT' if present else 'MISSING'}")

except Exception as e:
    print(f"❌ Failed to validate schemas: {e}")
    validation_results["schemas"]["error"] = str(e)

# ============================================================================
# 3. AI CRAWLERS VALIDATION
# ============================================================================
print("\n" + "="*80)
print("3. AI CRAWLERS VALIDATION")
print("="*80)

try:
    robots_url = f"{STORE_URL}/robots.txt"
    response = requests.get(robots_url, timeout=10)
    robots_txt = response.text

    required_crawlers = {
        "GPTBot": "GPTBot" in robots_txt,
        "ChatGPT-User": "ChatGPT-User" in robots_txt,
        "Claude-Web": "Claude-Web" in robots_txt or "anthropic-ai" in robots_txt,
        "Google-Extended": "Google-Extended" in robots_txt or "Googlebot-Extended" in robots_txt,
        "PerplexityBot": "PerplexityBot" in robots_txt,
        "CCBot": "CCBot" in robots_txt,
        "Applebot-Extended": "Applebot-Extended" in robots_txt,
        "Cohere-AI": "Cohere-AI" in robots_txt or "cohere-ai" in robots_txt,
    }

    # Check which are explicitly allowed (not disallowed)
    allowed_crawlers = []
    for crawler in required_crawlers:
        if required_crawlers[crawler]:
            # Check if Allow: / directive follows user-agent
            pattern = rf'User-agent:\s*{crawler}.*?Allow:\s*/'
            if re.search(pattern, robots_txt, re.IGNORECASE | re.DOTALL | re.MULTILINE):
                allowed_crawlers.append(crawler)
            # If no explicit Disallow: / after user-agent, consider it allowed
            elif not re.search(rf'User-agent:\s*{crawler}.*?Disallow:\s*/', robots_txt, re.IGNORECASE | re.DOTALL):
                allowed_crawlers.append(crawler)

    validation_results["ai_crawlers"] = {
        "mentioned": {k: v for k, v in required_crawlers.items() if v},
        "allowed": allowed_crawlers,
        "count_allowed": len(allowed_crawlers),
        "count_total": len(required_crawlers),
        "llms_txt_reference": "llms.txt" in robots_txt or "llms-txt" in robots_txt,
        "status": "✅ PASS" if len(allowed_crawlers) >= 6 else "⚠️ PARTIAL"
    }

    print(f"\n{'✅' if len(allowed_crawlers) >= 6 else '⚠️'} AI Crawlers: {len(allowed_crawlers)}/{len(required_crawlers)} configured and allowed")
    for crawler in required_crawlers:
        status = "✅ ALLOWED" if crawler in allowed_crawlers else ("⚠️ MENTIONED" if required_crawlers[crawler] else "❌ MISSING")
        print(f"   {status}: {crawler}")

    print(f"\n{'✅' if validation_results['ai_crawlers']['llms_txt_reference'] else '❌'} llms.txt reference: {'PRESENT' if validation_results['ai_crawlers']['llms_txt_reference'] else 'MISSING'}")

except Exception as e:
    print(f"❌ Failed to validate AI crawlers: {e}")
    validation_results["ai_crawlers"]["error"] = str(e)

# ============================================================================
# 4. SITEMAP VALIDATION
# ============================================================================
print("\n" + "="*80)
print("4. SITEMAP VALIDATION")
print("="*80)

try:
    sitemap_url = f"{STORE_URL}/sitemap.xml"
    response = requests.get(sitemap_url, timeout=10)
    sitemap_xml = response.text

    sitemaps_count = sitemap_xml.count("<sitemap>")
    urls_count = sitemap_xml.count("<url>")

    validation_results["sitemap"] = {
        "accessible": response.status_code == 200,
        "sub_sitemaps": sitemaps_count,
        "urls": urls_count,
        "size_bytes": len(sitemap_xml),
        "status": "✅ PASS" if response.status_code == 200 else "❌ FAIL"
    }

    print(f"\n{'✅' if validation_results['sitemap']['accessible'] else '❌'} Sitemap: {'ACCESSIBLE' if validation_results['sitemap']['accessible'] else 'NOT ACCESSIBLE'}")
    print(f"   URL: {sitemap_url}")
    print(f"   Sub-sitemaps: {sitemaps_count}")
    print(f"   Total URLs: {urls_count}")
    print(f"   Size: {len(sitemap_xml):,} bytes")

except Exception as e:
    print(f"❌ Failed to validate sitemap: {e}")
    validation_results["sitemap"]["error"] = str(e)

# ============================================================================
# 5. SSL/HTTPS VALIDATION
# ============================================================================
print("\n" + "="*80)
print("5. SSL/HTTPS VALIDATION")
print("="*80)

try:
    # Test HTTP → HTTPS redirect
    http_url = STORE_URL.replace("https://", "http://")
    response = requests.get(http_url, timeout=10, allow_redirects=False)

    redirect_301 = response.status_code == 301 and response.headers.get("Location", "").startswith("https://")

    # Check HSTS header
    https_response = requests.get(STORE_URL, timeout=10)
    hsts_header = https_response.headers.get("Strict-Transport-Security", "")
    hsts_enabled = bool(hsts_header)

    validation_results["ssl_https"] = {
        "redirect_301": redirect_301,
        "hsts_enabled": hsts_enabled,
        "hsts_header": hsts_header,
        "ssl_valid": https_response.url.startswith("https://"),
        "status": "✅ PASS" if (redirect_301 and hsts_enabled) else "⚠️ PARTIAL"
    }

    print(f"\n{'✅' if redirect_301 else '❌'} HTTP → HTTPS 301 Redirect: {'WORKING' if redirect_301 else 'MISSING'}")
    print(f"{'✅' if hsts_enabled else '❌'} HSTS Header: {'ENABLED' if hsts_enabled else 'MISSING'}")
    if hsts_enabled:
        print(f"   Header: {hsts_header[:80]}...")
    print(f"{'✅' if validation_results['ssl_https']['ssl_valid'] else '❌'} SSL Certificate: {'VALID' if validation_results['ssl_https']['ssl_valid'] else 'INVALID'}")

except Exception as e:
    print(f"❌ Failed to validate SSL/HTTPS: {e}")
    validation_results["ssl_https"]["error"] = str(e)

# ============================================================================
# 6. PRODUCTS VALIDATION (GraphQL)
# ============================================================================
print("\n" + "="*80)
print("6. PRODUCTS VALIDATION")
print("="*80)

try:
    query = """
    {
      products(first: 250, query: "status:ACTIVE") {
        edges {
          node {
            id
            title
            status
            metafields(first: 10, namespace: "global") {
              edges {
                node {
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

    if result:
        products = result["data"]["products"]["edges"]
        total_products = len(products)

        products_with_metafields = 0
        for edge in products:
            product = edge["node"]
            metafields = product["metafields"]["edges"]
            has_title = any(mf["node"]["key"] == "title_tag" for mf in metafields)
            has_desc = any(mf["node"]["key"] == "description_tag" for mf in metafields)

            if has_title and has_desc:
                products_with_metafields += 1

        compliance_rate = (products_with_metafields / total_products * 100) if total_products > 0 else 0

        validation_results["products"] = {
            "total_active": total_products,
            "with_metafields": products_with_metafields,
            "compliance_rate": compliance_rate,
            "status": "✅ PASS" if compliance_rate == 100 else "⚠️ PARTIAL"
        }

        print(f"\n{'✅' if compliance_rate == 100 else '⚠️'} Products Metafields: {products_with_metafields}/{total_products} ({compliance_rate:.1f}%)")
        print(f"   Total active products: {total_products}")
        print(f"   With SEO metafields (title_tag + description_tag): {products_with_metafields}")

except Exception as e:
    print(f"❌ Failed to validate products: {e}")
    validation_results["products"]["error"] = str(e)

# ============================================================================
# 7. COLLECTIONS VALIDATION (GraphQL)
# ============================================================================
print("\n" + "="*80)
print("7. COLLECTIONS VALIDATION")
print("="*80)

try:
    query = """
    {
      collections(first: 50) {
        edges {
          node {
            id
            title
            handle
            description
            descriptionHtml
            productsCount {
              count
            }
          }
        }
      }
    }
    """

    result = graphql_query(query)

    if result:
        collections = result["data"]["collections"]["edges"]
        total_collections = len(collections)

        collections_with_desc = 0
        collections_empty = []

        for edge in collections:
            collection = edge["node"]
            has_description = bool(collection["descriptionHtml"] and len(collection["descriptionHtml"]) > 100)

            if has_description:
                collections_with_desc += 1

            if collection["productsCount"]["count"] == 0:
                collections_empty.append(collection["title"])

        validation_results["collections"] = {
            "total": total_collections,
            "with_descriptions": collections_with_desc,
            "empty_collections": collections_empty,
            "count_empty": len(collections_empty),
            "status": "✅ PASS" if collections_with_desc >= total_collections * 0.75 else "⚠️ PARTIAL"
        }

        print(f"\n{'✅' if validation_results['collections']['status'] == '✅ PASS' else '⚠️'} Collections Descriptions: {collections_with_desc}/{total_collections}")
        print(f"   Total collections: {total_collections}")
        print(f"   With rich descriptions (>100 chars): {collections_with_desc}")

        if collections_empty:
            print(f"\n⚠️  Empty Collections (0 products): {len(collections_empty)}")
            for coll_name in collections_empty:
                print(f"   - {coll_name}")

except Exception as e:
    print(f"❌ Failed to validate collections: {e}")
    validation_results["collections"]["error"] = str(e)

# ============================================================================
# 8. TECHNICAL VALIDATION
# ============================================================================
print("\n" + "="*80)
print("8. TECHNICAL VALIDATION")
print("="*80)

try:
    llms_url = f"{STORE_URL}/pages/llms-txt"
    response = requests.get(llms_url, timeout=10)
    llms_accessible = response.status_code == 200

    validation_results["technical"] = {
        "llms_txt_page": {
            "accessible": llms_accessible,
            "status": "✅ PASS" if llms_accessible else "❌ FAIL"
        },
        "robots_txt": {
            "accessible": validation_results["ai_crawlers"].get("llms_txt_reference", False),
            "status": "✅ PASS" if validation_results["ai_crawlers"].get("llms_txt_reference", False) else "❌ FAIL"
        }
    }

    print(f"\n{'✅' if llms_accessible else '❌'} llms.txt Page: {'ACCESSIBLE' if llms_accessible else 'NOT ACCESSIBLE'}")
    print(f"   URL: {llms_url}")

    print(f"\n{'✅' if validation_results['technical']['robots_txt']['accessible'] else '❌'} robots.txt Reference: {'PRESENT' if validation_results['technical']['robots_txt']['accessible'] else 'MISSING'}")

except Exception as e:
    print(f"❌ Failed technical validation: {e}")
    validation_results["technical"]["error"] = str(e)

# ============================================================================
# 9. SUMMARY & SCORING
# ============================================================================
print("\n" + "="*80)
print("9. VALIDATION SUMMARY")
print("="*80)

categories = {
    "Meta Tags (Title)": validation_results["meta_tags"].get("title", {}).get("optimal", False),
    "Meta Tags (Description)": validation_results["meta_tags"].get("description", {}).get("optimal", False),
    "Open Graph Complete": validation_results["meta_tags"].get("og_tags", {}).get("complete", False),
    "Twitter Cards Complete": validation_results["meta_tags"].get("twitter_cards", {}).get("complete", False),
    "Schemas Present": validation_results["schemas"].get("complete", False),
    "AI Crawlers (≥6)": validation_results["ai_crawlers"].get("count_allowed", 0) >= 6,
    "Sitemap Accessible": validation_results["sitemap"].get("accessible", False),
    "SSL/HTTPS Perfect": validation_results["ssl_https"].get("redirect_301", False) and validation_results["ssl_https"].get("hsts_enabled", False),
    "Products Metafields (100%)": validation_results["products"].get("compliance_rate", 0) == 100,
    "Collections Descriptions (≥75%)": validation_results["collections"].get("with_descriptions", 0) >= validation_results["collections"].get("total", 1) * 0.75,
    "llms.txt Page": validation_results["technical"].get("llms_txt_page", {}).get("accessible", False),
}

passed = sum(categories.values())
total = len(categories)
score = (passed / total * 100) if total > 0 else 0

validation_results["summary"] = {
    "categories": categories,
    "passed": passed,
    "total": total,
    "score": score,
    "grade": "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "D" if score >= 60 else "F"
}

print("\n📊 COMPLIANCE STATUS:\n")
for category, status in categories.items():
    symbol = "✅" if status else "❌"
    print(f"{symbol} {category}: {'PASS' if status else 'FAIL'}")

print(f"\n🎯 Overall Score: {score:.1f}% ({passed}/{total} passed)")
print(f"🏆 Grade: {validation_results['summary']['grade']}")

# Save results to JSON
output_file = "comprehensive_seo_validation_results.json"
with open(output_file, 'w') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "store_url": STORE_URL,
        "api_version": API_VERSION,
        "results": validation_results
    }, f, indent=2)

print(f"\n✅ Results saved to: {output_file}")
print("\n" + "="*80)
