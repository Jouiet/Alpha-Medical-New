#!/usr/bin/env python3
"""
AUDIT SEO COMPLET - Alpha Medical Store
Vérification FACTUELLE RIGOUREUSE de TOUS les critères SEO

Critères audités:
1. Meta tags (title, description chars)
2. Open Graph tags completeness
3. Twitter Cards completeness
4. Structured data schemas (BreadcrumbList, Organization, Product, FAQPage, ProductGroup)
5. AI crawlers enabled (robots.txt)
6. Sitemap accessibility
7. SSL/HTTPS (301 redirect, HSTS)
8. Homepage meta tags quality
"""

import requests
import json
import re
from urllib.parse import urljoin
from datetime import datetime

STORE_URL = "https://www.alphamedical.shop"
ADMIN_DOMAIN = "azffej-as.myshopify.com"

print("="*80)
print("ALPHA MEDICAL - AUDIT SEO COMPLET FACTUEL")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

results = {
    "meta_tags": {},
    "og_tags": {},
    "twitter_cards": {},
    "schemas": {},
    "ai_crawlers": {},
    "sitemap": {},
    "ssl_https": {},
    "homepage_meta": {}
}

# ============================================================================
# 1. HOMEPAGE META TAGS AUDIT
# ============================================================================
print("\n" + "="*80)
print("1. HOMEPAGE META TAGS AUDIT")
print("="*80)

try:
    response = requests.get(STORE_URL, timeout=10)
    html = response.text

    # Extract title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else None

    # Extract meta description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    description = desc_match.group(1).strip() if desc_match else None

    results["homepage_meta"] = {
        "title": title,
        "title_length": len(title) if title else 0,
        "description": description,
        "description_length": len(description) if description else 0,
        "title_optimal": 50 <= len(title) <= 60 if title else False,
        "description_optimal": 150 <= len(description) <= 160 if description else False
    }

    print(f"\n✅ Title: {title}")
    title_len = len(title) if title else 0
    title_status = "✅ OPTIMAL" if (title and 50 <= len(title) <= 60) else "⚠️ NOT OPTIMAL"
    print(f"   Length: {title_len} chars {title_status}")

    print(f"\n✅ Description: {description[:80] if description else 'NONE'}...")
    desc_len = len(description) if description else 0
    desc_status = "✅ OPTIMAL" if (description and 150 <= len(description) <= 160) else "⚠️ NOT OPTIMAL"
    print(f"   Length: {desc_len} chars {desc_status}")

except Exception as e:
    print(f"❌ Failed to fetch homepage: {e}")
    results["homepage_meta"]["error"] = str(e)

# ============================================================================
# 2. OPEN GRAPH TAGS AUDIT
# ============================================================================
print("\n" + "="*80)
print("2. OPEN GRAPH TAGS AUDIT")
print("="*80)

try:
    og_tags = {
        "og:site_name": re.search(r'<meta\s+property=["\']og:site_name["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
        "og:title": re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
        "og:description": re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
        "og:image": re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
        "og:url": re.search(r'<meta\s+property=["\']og:url["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
        "og:type": re.search(r'<meta\s+property=["\']og:type["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
    }

    og_found = {k: v.group(1) if v else None for k, v in og_tags.items()}
    og_complete = all(og_found.values())

    results["og_tags"] = {
        "tags": og_found,
        "complete": og_complete,
        "missing": [k for k, v in og_found.items() if not v]
    }

    print(f"\n{'✅' if og_complete else '⚠️'} Open Graph Tags: {'COMPLETE' if og_complete else 'INCOMPLETE'}")
    for tag, value in og_found.items():
        status = "✅" if value else "❌"
        print(f"   {status} {tag}: {value[:60] if value else 'MISSING'}...")

    if results["og_tags"]["missing"]:
        print(f"\n❌ Missing tags: {', '.join(results['og_tags']['missing'])}")

except Exception as e:
    print(f"❌ Failed to parse OG tags: {e}")
    results["og_tags"]["error"] = str(e)

# ============================================================================
# 3. TWITTER CARDS AUDIT
# ============================================================================
print("\n" + "="*80)
print("3. TWITTER CARDS AUDIT")
print("="*80)

try:
    twitter_tags = {
        "twitter:card": re.search(r'<meta\s+name=["\']twitter:card["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
        "twitter:title": re.search(r'<meta\s+name=["\']twitter:title["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
        "twitter:description": re.search(r'<meta\s+name=["\']twitter:description["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
        "twitter:image": re.search(r'<meta\s+name=["\']twitter:image["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE),
    }

    twitter_found = {k: v.group(1) if v else None for k, v in twitter_tags.items()}
    twitter_complete = all(twitter_found.values())

    results["twitter_cards"] = {
        "tags": twitter_found,
        "complete": twitter_complete,
        "missing": [k for k, v in twitter_found.items() if not v]
    }

    print(f"\n{'✅' if twitter_complete else '⚠️'} Twitter Cards: {'COMPLETE' if twitter_complete else 'INCOMPLETE'}")
    for tag, value in twitter_found.items():
        status = "✅" if value else "❌"
        print(f"   {status} {tag}: {value[:60] if value else 'MISSING'}...")

    if results["twitter_cards"]["missing"]:
        print(f"\n❌ Missing tags: {', '.join(results['twitter_cards']['missing'])}")

except Exception as e:
    print(f"❌ Failed to parse Twitter cards: {e}")
    results["twitter_cards"]["error"] = str(e)

# ============================================================================
# 4. STRUCTURED DATA SCHEMAS AUDIT
# ============================================================================
print("\n" + "="*80)
print("4. STRUCTURED DATA SCHEMAS AUDIT")
print("="*80)

try:
    # Extract all JSON-LD schemas
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
        "FAQPage": "FAQPage" in schema_types
    }

    results["schemas"] = {
        "found": schema_types,
        "required": required_schemas,
        "complete": all(required_schemas.values()),
        "missing": [k for k, v in required_schemas.items() if not v]
    }

    print(f"\n{'✅' if results['schemas']['complete'] else '⚠️'} Structured Data: {'COMPLETE' if results['schemas']['complete'] else 'INCOMPLETE'}")
    print(f"\nFound {len(schemas_found)} schema blocks with {len(schema_types)} types:")
    for schema_type in set(schema_types):
        count = schema_types.count(schema_type)
        print(f"   ✅ {schema_type}: {count}x")

    print(f"\nRequired schemas:")
    for schema, present in required_schemas.items():
        status = "✅" if present else "❌"
        print(f"   {status} {schema}: {'PRESENT' if present else 'MISSING'}")

    if results["schemas"]["missing"]:
        print(f"\n❌ Missing schemas: {', '.join(results['schemas']['missing'])}")

except Exception as e:
    print(f"❌ Failed to parse schemas: {e}")
    results["schemas"]["error"] = str(e)

# ============================================================================
# 5. AI CRAWLERS (robots.txt)
# ============================================================================
print("\n" + "="*80)
print("5. AI CRAWLERS AUDIT (robots.txt)")
print("="*80)

try:
    robots_url = urljoin(STORE_URL, "/robots.txt")
    response = requests.get(robots_url, timeout=10)
    robots_txt = response.text

    ai_crawlers = {
        "GPTBot": "GPTBot" in robots_txt,
        "Claude-Web": "Claude-Web" in robots_txt or "Claude" in robots_txt,
        "Google-Extended": "Google-Extended" in robots_txt or "Gemini" in robots_txt,
        "PerplexityBot": "PerplexityBot" in robots_txt or "Perplexity" in robots_txt,
        "CCBot": "CCBot" in robots_txt,
        "Applebot": "Applebot" in robots_txt,
    }

    # Check if any are explicitly disallowed
    disallowed_crawlers = []
    for crawler, found in ai_crawlers.items():
        if found:
            # Check if Disallow: / follows this user-agent
            pattern = rf'User-agent:\s*{crawler}.*?Disallow:\s*/\s'
            if re.search(pattern, robots_txt, re.IGNORECASE | re.DOTALL):
                disallowed_crawlers.append(crawler)

    results["ai_crawlers"] = {
        "mentioned": {k: v for k, v in ai_crawlers.items() if v},
        "allowed": [k for k in ai_crawlers if ai_crawlers[k] and k not in disallowed_crawlers],
        "disallowed": disallowed_crawlers,
        "llms_txt_reference": "llms.txt" in robots_txt or "llms-txt" in robots_txt
    }

    print(f"\n✅ robots.txt accessible")
    print(f"\nAI Crawlers mentioned: {len(results['ai_crawlers']['mentioned'])}")
    for crawler in results["ai_crawlers"]["mentioned"]:
        allowed = crawler not in disallowed_crawlers
        status = "✅ ALLOWED" if allowed else "❌ DISALLOWED"
        print(f"   {status}: {crawler}")

    print(f"\n{'✅' if results['ai_crawlers']['llms_txt_reference'] else '❌'} llms.txt reference: {'PRESENT' if results['ai_crawlers']['llms_txt_reference'] else 'MISSING'}")

except Exception as e:
    print(f"❌ Failed to fetch robots.txt: {e}")
    results["ai_crawlers"]["error"] = str(e)

# ============================================================================
# 6. SITEMAP AUDIT
# ============================================================================
print("\n" + "="*80)
print("6. SITEMAP AUDIT")
print("="*80)

try:
    sitemap_url = urljoin(STORE_URL, "/sitemap.xml")
    response = requests.get(sitemap_url, timeout=10)
    sitemap_xml = response.text

    # Count sitemap entries
    sitemap_pattern = r'<sitemap>|<url>'
    sitemaps_count = sitemap_xml.count("<sitemap>")
    urls_count = sitemap_xml.count("<url>")

    results["sitemap"] = {
        "accessible": response.status_code == 200,
        "sub_sitemaps": sitemaps_count,
        "urls": urls_count,
        "size_bytes": len(sitemap_xml)
    }

    print(f"\n✅ Sitemap accessible: {sitemap_url}")
    print(f"   Sub-sitemaps: {sitemaps_count}")
    print(f"   Total URLs: {urls_count}")
    print(f"   Size: {len(sitemap_xml):,} bytes")

except Exception as e:
    print(f"❌ Failed to fetch sitemap: {e}")
    results["sitemap"]["error"] = str(e)

# ============================================================================
# 7. SSL/HTTPS AUDIT
# ============================================================================
print("\n" + "="*80)
print("7. SSL/HTTPS AUDIT")
print("="*80)

try:
    # Test HTTP -> HTTPS redirect
    http_url = STORE_URL.replace("https://", "http://")
    response = requests.get(http_url, timeout=10, allow_redirects=False)

    redirect_301 = response.status_code == 301 and response.headers.get("Location", "").startswith("https://")

    # Check HSTS header
    https_response = requests.get(STORE_URL, timeout=10)
    hsts_header = https_response.headers.get("Strict-Transport-Security", "")
    hsts_enabled = bool(hsts_header)

    results["ssl_https"] = {
        "redirect_301": redirect_301,
        "hsts_enabled": hsts_enabled,
        "hsts_header": hsts_header,
        "ssl_valid": https_response.url.startswith("https://")
    }

    print(f"\n{'✅' if redirect_301 else '❌'} 301 Redirect HTTP → HTTPS: {'WORKING' if redirect_301 else 'MISSING'}")
    print(f"{'✅' if hsts_enabled else '❌'} HSTS Header: {'ENABLED' if hsts_enabled else 'MISSING'}")
    if hsts_enabled:
        print(f"   Header: {hsts_header[:80]}...")
    print(f"{'✅' if results['ssl_https']['ssl_valid'] else '❌'} SSL Certificate: {'VALID' if results['ssl_https']['ssl_valid'] else 'INVALID'}")

except Exception as e:
    print(f"❌ Failed SSL/HTTPS audit: {e}")
    results["ssl_https"]["error"] = str(e)

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("AUDIT SUMMARY")
print("="*80)

summary = {
    "Homepage Meta Tags": results["homepage_meta"].get("title_optimal") and results["homepage_meta"].get("description_optimal"),
    "Open Graph Tags": results["og_tags"].get("complete", False),
    "Twitter Cards": results["twitter_cards"].get("complete", False),
    "Structured Data Schemas": results["schemas"].get("complete", False),
    "AI Crawlers Enabled": len(results["ai_crawlers"].get("allowed", [])) > 0,
    "Sitemap Accessible": results["sitemap"].get("accessible", False),
    "SSL/HTTPS Perfect": results["ssl_https"].get("redirect_301") and results["ssl_https"].get("hsts_enabled"),
}

print("\n📊 COMPLIANCE STATUS:\n")
for category, status in summary.items():
    symbol = "✅" if status else "❌"
    print(f"{symbol} {category}: {'PASS' if status else 'FAIL'}")

overall_score = sum(summary.values()) / len(summary) * 100
print(f"\n🎯 Overall Score: {overall_score:.1f}% ({sum(summary.values())}/{len(summary)} passed)")

# Save results to JSON
output_file = "audit_seo_results.json"
with open(output_file, 'w') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "store_url": STORE_URL,
        "results": results,
        "summary": summary,
        "overall_score": overall_score
    }, f, indent=2)

print(f"\n✅ Results saved to: {output_file}")
print("\n" + "="*80)
