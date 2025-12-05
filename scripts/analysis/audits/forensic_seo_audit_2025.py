#!/usr/bin/env python3
"""
FORENSIC SEO AUDIT - Alpha Medical 2025-11-16
Ultra-rigorous verification of ALL SEO criteria
NO ASSUMPTIONS - ONLY VERIFIABLE FACTS
"""

import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

print("=" * 80)
print("FORENSIC SEO AUDIT - ALPHA MEDICAL")
print("=" * 80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print(f"Approach: Bottom-up, fact-based verification")
print(f"Standard: BRUTAL HONESTY - No bullshit, no wishful thinking")
print()

audit_results = {
    "timestamp": datetime.now().isoformat(),
    "url": "https://www.alphamedical.shop",
    "criteria": {}
}

# ============================================================================
# SECTION 1: HOMEPAGE META TAGS
# ============================================================================

print("=" * 80)
print("SECTION 1: HOMEPAGE META TAGS")
print("=" * 80)

try:
    response = requests.get("https://www.alphamedical.shop/", timeout=10)
    if response.status_code != 200:
        print(f"❌ Homepage error: {response.status_code}")
        audit_results['criteria']['homepage_access'] = {"status": "FAIL", "code": response.status_code}
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check 1.1: Title tag
        print("\n[1.1] Homepage Title Tag...")
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.string.strip() if title_tag.string else ""
            title_length = len(title_text)
            print(f"  Content: \"{title_text}\"")
            print(f"  Length: {title_length} characters")

            if 50 <= title_length <= 60:
                print("  ✅ OPTIMAL length (50-60 chars)")
                status = "PASS"
            elif 40 <= title_length <= 70:
                print("  ⚠️  ACCEPTABLE length (40-70 chars)")
                status = "ACCEPTABLE"
            else:
                print("  ❌ NON-OPTIMAL length (should be 50-60 chars)")
                status = "FAIL"

            audit_results['criteria']['title_tag'] = {
                "status": status,
                "content": title_text,
                "length": title_length,
                "optimal_range": "50-60 characters"
            }
        else:
            print("  ❌ Title tag NOT FOUND")
            audit_results['criteria']['title_tag'] = {"status": "FAIL", "reason": "Not found"}

        # Check 1.2: Meta description
        print("\n[1.2] Meta Description...")
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc_text = meta_desc['content'].strip()
            desc_length = len(desc_text)
            print(f"  Content: \"{desc_text[:100]}...\"")
            print(f"  Length: {desc_length} characters")

            if 150 <= desc_length <= 160:
                print("  ✅ OPTIMAL length (150-160 chars)")
                status = "PASS"
            elif 120 <= desc_length <= 170:
                print("  ⚠️  ACCEPTABLE length (120-170 chars)")
                status = "ACCEPTABLE"
            else:
                print("  ❌ NON-OPTIMAL length (should be 150-160 chars)")
                status = "FAIL"

            audit_results['criteria']['meta_description'] = {
                "status": status,
                "content": desc_text,
                "length": desc_length,
                "optimal_range": "150-160 characters"
            }
        else:
            print("  ❌ Meta description NOT FOUND")
            audit_results['criteria']['meta_description'] = {"status": "FAIL", "reason": "Not found"}

        # Check 1.3: Language attribute
        print("\n[1.3] HTML Language Attribute...")
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            lang = html_tag['lang']
            print(f"  Language: {lang}")
            if lang == 'en' or lang.startswith('en-'):
                print("  ✅ CORRECT (English)")
                audit_results['criteria']['html_lang'] = {"status": "PASS", "value": lang}
            else:
                print(f"  ❌ WRONG language: {lang} (should be 'en')")
                audit_results['criteria']['html_lang'] = {"status": "FAIL", "value": lang}
        else:
            print("  ❌ Language attribute NOT FOUND")
            audit_results['criteria']['html_lang'] = {"status": "FAIL", "reason": "Not found"}

except Exception as e:
    print(f"❌ Homepage fetch failed: {e}")
    audit_results['criteria']['homepage_access'] = {"status": "FAIL", "error": str(e)}

# ============================================================================
# SECTION 2: OPEN GRAPH TAGS
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 2: OPEN GRAPH TAGS")
print("=" * 80)

try:
    response = requests.get("https://www.alphamedical.shop/", timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    required_og_tags = ['og:title', 'og:description', 'og:image', 'og:url', 'og:type', 'og:site_name']
    og_tags_found = {}

    print("\n[2.1] Required Open Graph Tags...")
    for tag_name in required_og_tags:
        tag = soup.find('meta', property=tag_name)
        if tag and tag.get('content'):
            content = tag['content'].strip()
            og_tags_found[tag_name] = content
            print(f"  ✅ {tag_name}: \"{content[:60]}...\"" if len(content) > 60 else f"  ✅ {tag_name}: \"{content}\"")
        else:
            og_tags_found[tag_name] = None
            print(f"  ❌ {tag_name}: NOT FOUND")

    found_count = sum(1 for v in og_tags_found.values() if v is not None)
    total_count = len(required_og_tags)

    if found_count == total_count:
        print(f"\n  ✅ ALL Open Graph tags present ({found_count}/{total_count})")
        status = "PASS"
    else:
        print(f"\n  ❌ INCOMPLETE Open Graph tags ({found_count}/{total_count})")
        status = "FAIL"

    audit_results['criteria']['open_graph'] = {
        "status": status,
        "tags_found": og_tags_found,
        "count": f"{found_count}/{total_count}"
    }

except Exception as e:
    print(f"❌ Open Graph check failed: {e}")
    audit_results['criteria']['open_graph'] = {"status": "FAIL", "error": str(e)}

# ============================================================================
# SECTION 3: TWITTER CARDS
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 3: TWITTER CARDS")
print("=" * 80)

try:
    response = requests.get("https://www.alphamedical.shop/", timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    required_twitter_tags = ['twitter:card', 'twitter:title', 'twitter:description', 'twitter:image']
    twitter_tags_found = {}

    print("\n[3.1] Required Twitter Card Tags...")
    for tag_name in required_twitter_tags:
        tag = soup.find('meta', attrs={'name': tag_name})
        if tag and tag.get('content'):
            content = tag['content'].strip()
            twitter_tags_found[tag_name] = content
            print(f"  ✅ {tag_name}: \"{content[:60]}...\"" if len(content) > 60 else f"  ✅ {tag_name}: \"{content}\"")
        else:
            twitter_tags_found[tag_name] = None
            print(f"  ❌ {tag_name}: NOT FOUND")

    found_count = sum(1 for v in twitter_tags_found.values() if v is not None)
    total_count = len(required_twitter_tags)

    if found_count == total_count:
        print(f"\n  ✅ ALL Twitter Card tags present ({found_count}/{total_count})")
        status = "PASS"
    else:
        print(f"\n  ❌ INCOMPLETE Twitter Card tags ({found_count}/{total_count})")
        status = "FAIL"

    audit_results['criteria']['twitter_cards'] = {
        "status": status,
        "tags_found": twitter_tags_found,
        "count": f"{found_count}/{total_count}"
    }

except Exception as e:
    print(f"❌ Twitter Cards check failed: {e}")
    audit_results['criteria']['twitter_cards'] = {"status": "FAIL", "error": str(e)}

# ============================================================================
# SECTION 4: STRUCTURED DATA (SCHEMAS)
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 4: STRUCTURED DATA (JSON-LD SCHEMAS)")
print("=" * 80)

try:
    response = requests.get("https://www.alphamedical.shop/", timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all JSON-LD scripts
    json_ld_scripts = soup.find_all('script', type='application/ld+json')

    print(f"\n[4.1] JSON-LD Scripts Found: {len(json_ld_scripts)}")

    schemas_found = {
        'Organization': False,
        'WebSite': False,
        'BreadcrumbList': False,
        'Product': False,
        'FAQPage': False,
        'ProductGroup': False
    }

    schemas_details = []

    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)

            # Handle @graph arrays
            if isinstance(data, dict) and '@graph' in data:
                schemas_in_graph = data['@graph']
                for schema in schemas_in_graph:
                    schema_type = schema.get('@type')
                    if schema_type in schemas_found:
                        schemas_found[schema_type] = True
                        schemas_details.append({
                            "type": schema_type,
                            "keys": list(schema.keys())
                        })
            # Handle single schema objects
            elif isinstance(data, dict) and '@type' in data:
                schema_type = data.get('@type')
                if schema_type in schemas_found:
                    schemas_found[schema_type] = True
                    schemas_details.append({
                        "type": schema_type,
                        "keys": list(data.keys())
                    })
        except json.JSONDecodeError:
            continue

    print("\n[4.2] Schema Types Verification...")
    for schema_type, found in schemas_found.items():
        if found:
            print(f"  ✅ {schema_type}: FOUND")
        else:
            print(f"  ❌ {schema_type}: NOT FOUND")

    found_count = sum(1 for v in schemas_found.values() if v)
    total_count = len(schemas_found)

    if found_count >= 3:  # At minimum Organization, WebSite, Product
        print(f"\n  ✅ PASS: {found_count}/{total_count} schema types found")
        status = "PASS"
    else:
        print(f"\n  ❌ FAIL: Only {found_count}/{total_count} schema types found")
        status = "FAIL"

    audit_results['criteria']['structured_data'] = {
        "status": status,
        "schemas_found": schemas_found,
        "count": f"{found_count}/{total_count}",
        "details": schemas_details
    }

except Exception as e:
    print(f"❌ Structured data check failed: {e}")
    audit_results['criteria']['structured_data'] = {"status": "FAIL", "error": str(e)}

# ============================================================================
# SECTION 5: AI CRAWLERS (robots.txt)
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 5: AI CRAWLERS PERMISSIONS")
print("=" * 80)

try:
    response = requests.get("https://www.alphamedical.shop/robots.txt", timeout=10)
    robots_txt = response.text

    ai_crawlers = [
        'GPTBot',
        'Claude-Web',
        'Google-Extended',
        'PerplexityBot',
        'CCBot',
        'Applebot-Extended'
    ]

    print("\n[5.1] AI Crawler Permissions...")

    crawler_status = {}

    for crawler in ai_crawlers:
        if f"User-agent: {crawler}" in robots_txt:
            # Extract the section for this crawler
            start_idx = robots_txt.find(f"User-agent: {crawler}")
            next_agent_idx = robots_txt.find("User-agent:", start_idx + len(f"User-agent: {crawler}"))

            if next_agent_idx == -1:
                section = robots_txt[start_idx:]
            else:
                section = robots_txt[start_idx:next_agent_idx]

            if "Disallow: /" in section and "Allow:" not in section:
                print(f"  ❌ {crawler}: DISALLOWED")
                crawler_status[crawler] = "DISALLOWED"
            elif "Allow: /" in section:
                print(f"  ✅ {crawler}: ALLOWED")
                crawler_status[crawler] = "ALLOWED"
            else:
                print(f"  ⚠️  {crawler}: IMPLICIT ALLOW (no disallow rule)")
                crawler_status[crawler] = "IMPLICIT_ALLOW"
        else:
            print(f"  ✅ {crawler}: IMPLICIT ALLOW (not listed)")
            crawler_status[crawler] = "IMPLICIT_ALLOW"

    allowed_count = sum(1 for v in crawler_status.values() if v in ['ALLOWED', 'IMPLICIT_ALLOW'])
    total_count = len(ai_crawlers)

    if allowed_count == total_count:
        print(f"\n  ✅ ALL AI crawlers allowed ({allowed_count}/{total_count})")
        status = "PASS"
    else:
        print(f"\n  ❌ Some AI crawlers blocked ({allowed_count}/{total_count})")
        status = "FAIL"

    audit_results['criteria']['ai_crawlers'] = {
        "status": status,
        "crawler_status": crawler_status,
        "count": f"{allowed_count}/{total_count}"
    }

except Exception as e:
    print(f"❌ AI crawlers check failed: {e}")
    audit_results['criteria']['ai_crawlers'] = {"status": "FAIL", "error": str(e)}

# ============================================================================
# SECTION 6: SITEMAP
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 6: SITEMAP ACCESSIBILITY")
print("=" * 80)

try:
    print("\n[6.1] Main Sitemap...")
    response = requests.get("https://www.alphamedical.shop/sitemap.xml", timeout=10)

    if response.status_code == 200:
        print(f"  ✅ Sitemap accessible (200 OK)")

        # Parse sitemap to find sub-sitemaps
        soup = BeautifulSoup(response.text, 'xml')
        sitemaps = soup.find_all('sitemap')

        print(f"  ✅ Sub-sitemaps found: {len(sitemaps)}")

        sub_sitemap_urls = []
        for sitemap in sitemaps:
            loc = sitemap.find('loc')
            if loc:
                sub_sitemap_urls.append(loc.text)
                print(f"    - {loc.text}")

        audit_results['criteria']['sitemap'] = {
            "status": "PASS",
            "main_sitemap": "https://www.alphamedical.shop/sitemap.xml",
            "sub_sitemaps": sub_sitemap_urls,
            "count": len(sitemaps)
        }
    else:
        print(f"  ❌ Sitemap error: {response.status_code}")
        audit_results['criteria']['sitemap'] = {"status": "FAIL", "code": response.status_code}

except Exception as e:
    print(f"❌ Sitemap check failed: {e}")
    audit_results['criteria']['sitemap'] = {"status": "FAIL", "error": str(e)}

# ============================================================================
# SECTION 7: SSL/HTTPS
# ============================================================================

print("\n" + "=" * 80)
print("SECTION 7: SSL/HTTPS SECURITY")
print("=" * 80)

try:
    print("\n[7.1] HTTPS Redirect...")
    response_http = requests.get("http://www.alphamedical.shop/", timeout=10, allow_redirects=False)

    if response_http.status_code in [301, 302]:
        redirect_location = response_http.headers.get('Location', '')
        if redirect_location.startswith('https://'):
            print(f"  ✅ HTTP → HTTPS redirect (Status: {response_http.status_code})")
            print(f"  ✅ Redirect to: {redirect_location}")
            https_redirect = "PASS"
        else:
            print(f"  ❌ Redirect NOT to HTTPS: {redirect_location}")
            https_redirect = "FAIL"
    else:
        print(f"  ❌ No redirect (Status: {response_http.status_code})")
        https_redirect = "FAIL"

    print("\n[7.2] HSTS Header...")
    response_https = requests.get("https://www.alphamedical.shop/", timeout=10)
    hsts_header = response_https.headers.get('Strict-Transport-Security')

    if hsts_header:
        print(f"  ✅ HSTS enabled: {hsts_header}")
        hsts_status = "PASS"
    else:
        print(f"  ❌ HSTS NOT enabled")
        hsts_status = "FAIL"

    if https_redirect == "PASS" and hsts_status == "PASS":
        overall_status = "PASS"
    else:
        overall_status = "FAIL"

    audit_results['criteria']['ssl_https'] = {
        "status": overall_status,
        "https_redirect": https_redirect,
        "hsts_enabled": hsts_status,
        "hsts_header": hsts_header
    }

except Exception as e:
    print(f"❌ SSL/HTTPS check failed: {e}")
    audit_results['criteria']['ssl_https'] = {"status": "FAIL", "error": str(e)}

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("FORENSIC AUDIT SUMMARY")
print("=" * 80)

total_criteria = len(audit_results['criteria'])
passed_criteria = sum(1 for c in audit_results['criteria'].values()
                      if isinstance(c, dict) and c.get('status') == 'PASS')
acceptable_criteria = sum(1 for c in audit_results['criteria'].values()
                          if isinstance(c, dict) and c.get('status') == 'ACCEPTABLE')
failed_criteria = sum(1 for c in audit_results['criteria'].values()
                      if isinstance(c, dict) and c.get('status') == 'FAIL')

print(f"\nTotal Criteria: {total_criteria}")
print(f"✅ PASS: {passed_criteria}")
print(f"⚠️  ACCEPTABLE: {acceptable_criteria}")
print(f"❌ FAIL: {failed_criteria}")

score = ((passed_criteria + (acceptable_criteria * 0.5)) / total_criteria) * 100

print(f"\n📊 OVERALL SCORE: {score:.1f}%")

if score >= 90:
    print("🎉 EXCELLENT - SEO optimized to high standard")
elif score >= 75:
    print("✅ GOOD - Most SEO criteria met")
elif score >= 60:
    print("⚠️  ACCEPTABLE - Some improvements needed")
else:
    print("❌ POOR - Significant SEO issues detected")

# Save results
output_file = '/Users/mac/Desktop/Alpha-Medical/forensic_seo_audit_2025.json'
with open(output_file, 'w') as f:
    json.dump(audit_results, f, indent=2)

print(f"\n📁 Full audit results saved to: {output_file}")
print("=" * 80)
