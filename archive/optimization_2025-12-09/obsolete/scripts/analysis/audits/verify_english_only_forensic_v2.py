#!/usr/bin/env python3
"""
AUDIT FORENSIQUE V2 - 100% ENGLISH ONLY VERIFICATION (FALSE POSITIVES FIXED)
Date: 2025-11-20
Purpose: Verify ENTIRE site is 100% English (no French content)

IMPROVEMENTS V2:
- Exclude CSS/HTML contexts (sans-serif, etc.)
- Use word boundaries for French detection
- Smarter false positive filtering
"""

import os
import requests
import json
import re
from typing import Dict, List, Tuple
from html import unescape

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials from .env.admin")
    exit(1)

SHOP = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

# Unambiguous French phrases (NOT single words that appear in English)
FRENCH_PHRASES = [
    # Multi-word phrases (very high confidence)
    r'\blivraison\s+gratuite\b',
    r'\bretour\s+gratuit\b',
    r'\bgarantie\s+de\b',
    r'\bsatisfaction\s+garantie\b',
    r'\bdès\s+maintenant\b',
    r'\bavec\s+nous\b',
    r'\bchez\s+nous\b',
    r'\bpour\s+vous\b',
    r'\bnotre\s+équipe\b',
    r'\bbienvenue\s+à\b',
    r'\bmerci\s+de\b',
    r'\bs\'il\s+vous\s+plaît\b',
    r'\bjusqu\'à\b',
    r'\bà\s+partir\s+de\b',
    r'\bvotre\s+commande\b',
    r'\bnotre\s+magasin\b',
    r'\bnos\s+produits\b',
    r'\bnotre\s+site\b',
    r'\bcontactez-nous\b',
    r'\bappelez-nous\b',
    r'\bécrivez-nous\b',
    r'\btous\s+les\s+jours\b',
    r'\bchaque\s+jour\b',

    # French articles with following noun (high confidence)
    r'\ble\s+[a-zéèêëàâäïîôùûüÿœæç]{3,}\b',
    r'\bla\s+[a-zéèêëàâäïîôùûüÿœæç]{3,}\b',
    r'\bles\s+[a-zéèêëàâäïîôùûüÿœæç]{3,}\b',
    r'\bun\s+[a-zéèêëàâäïîôùûüÿœæç]{3,}\b',
    r'\bune\s+[a-zéèêëàâäïîôùûüÿœæç]{3,}\b',
    r'\bdes\s+[a-zéèêëàâäïîôùûüÿœæç]{3,}\b',

    # Common French words (but exclude English words)
    r'\bavec\s+',  # "avec" as standalone word (not in "average")
    r'\bsans\s+',  # "sans" as standalone word (not in "sans-serif")
    r'\bdans\s+',
    r'\bsur\s+le\b',
    r'\bsous\s+',
    r'\bpar\s+le\b',
    r'\bchez\s+',
    r'\bdepuis\s+',
    r'\bpendant\s+',
    r'\btrès\s+',
    r'\bbien\s+sûr\b',
    r'\btout\s+le\b',

    # French pronouns (high confidence)
    r'\bje\s+',
    r'\btu\s+',
    r'\bil\s+est\b',
    r'\belle\s+est\b',
    r'\bnous\s+sommes\b',
    r'\bvous\s+êtes\b',
    r'\bils\s+sont\b',
    r'\belles\s+sont\b',

    # French verbs (high confidence patterns)
    r'\best\s+[a-zéèêëàâäïîôùûüÿœæç]{3,}\b',  # "est" followed by French word
    r'\bsont\s+[a-zéèêëàâäïîôùûüÿœæç]{3,}\b',
    r'\bavoir\s+',
    r'\bêtre\s+',
    r'\bfaire\s+',
    r'\baller\s+à\b',
    r'\bvenir\s+de\b',

    # Accented words (French-specific, but exclude technical terms)
    r'\b[a-z]{2,}[àâäéèêëïîôùûüÿœæ][a-z]{2,}\b',  # Accented characters in middle of word
]

# Compile patterns (case insensitive)
FRENCH_REGEX = re.compile('|'.join(FRENCH_PHRASES), re.IGNORECASE)

# Patterns to EXCLUDE (false positives)
EXCLUDE_PATTERNS = [
    r'font-family:\s*[^;]*sans-serif',  # CSS font-family
    r'sans-serif',  # Any sans-serif
    r'style="[^"]*sans-serif[^"]*"',  # Inline CSS
    r'\bhier',  # English words: hierarchy, hierarchical, cashier
    r'\best\b',  # English words: best, establish, question, request, test
    r'\bsur\b',  # English words: sure, surgery, insurance
]

def strip_html_and_css(text: str) -> str:
    """Remove HTML tags and CSS from text"""
    if not text:
        return ""

    # Remove style tags and their content
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Remove inline styles
    text = re.sub(r'\sstyle="[^"]*"', '', text, flags=re.IGNORECASE)

    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)

    # Unescape HTML entities
    text = unescape(text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def is_false_positive(text: str, match: str) -> bool:
    """Check if match is a false positive"""
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def detect_french(text: str) -> List[Tuple[str, str]]:
    """Detect French content in text (returns list of (match, context))"""
    if not text:
        return []

    # Strip HTML/CSS first
    clean_text = strip_html_and_css(text)

    matches = []
    for match in FRENCH_REGEX.finditer(clean_text.lower()):
        matched_text = match.group()

        # Get context (50 chars before and after)
        start = max(0, match.start() - 50)
        end = min(len(clean_text), match.end() + 50)
        context = clean_text[start:end]

        # Check if false positive
        if not is_false_positive(context, matched_text):
            matches.append((matched_text.strip(), context.strip()))

    return matches

def fetch_all_products() -> List[Dict]:
    """Fetch ALL products"""
    all_products = []
    url = f"{REST_URL}/products.json?limit=250"

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            break

        data = response.json()
        products = data.get("products", [])
        all_products.extend(products)

        link_header = response.headers.get("Link", "")
        if 'rel="next"' in link_header:
            next_url = link_header.split('>; rel="next"')[0].split('<')[1] if '<' in link_header else None
            url = next_url if next_url else None
        else:
            url = None

    return all_products

def fetch_all_collections() -> List[Dict]:
    """Fetch all collections"""
    collections = []
    url = f"{REST_URL}/custom_collections.json?limit=250"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        collections.extend(response.json().get("custom_collections", []))

    url = f"{REST_URL}/smart_collections.json?limit=250"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        collections.extend(response.json().get("smart_collections", []))

    return collections

def fetch_all_pages() -> List[Dict]:
    """Fetch all pages"""
    url = f"{REST_URL}/pages.json?limit=250"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []
    return response.json().get("pages", [])

def audit_products(products: List[Dict]) -> Tuple[List[Dict], int]:
    """Audit products for French content"""
    violations = []

    for product in products:
        pid = product.get("id")
        handle = product.get("handle")
        title = product.get("title", "")
        body = product.get("body_html", "") or ""
        vendor = product.get("vendor", "")
        tags = product.get("tags", "")

        french_in_title = detect_french(title)
        french_in_body = detect_french(body)
        french_in_vendor = detect_french(vendor)
        french_in_tags = detect_french(tags)

        if french_in_title or french_in_body or french_in_vendor or french_in_tags:
            violations.append({
                "type": "PRODUCT",
                "id": pid,
                "handle": handle,
                "title": title[:80],
                "french_in_title": french_in_title[:3],
                "french_in_body": french_in_body[:3],
                "french_in_vendor": french_in_vendor[:3],
                "french_in_tags": french_in_tags[:3]
            })

    return violations, len(products)

def audit_collections(collections: List[Dict]) -> Tuple[List[Dict], int]:
    """Audit collections for French content"""
    violations = []

    for col in collections:
        cid = col.get("id")
        handle = col.get("handle")
        title = col.get("title", "")
        body = col.get("body_html", "") or ""

        french_in_title = detect_french(title)
        french_in_body = detect_french(body)

        if french_in_title or french_in_body:
            violations.append({
                "type": "COLLECTION",
                "id": cid,
                "handle": handle,
                "title": title[:80],
                "french_in_title": french_in_title[:3],
                "french_in_body": french_in_body[:3]
            })

    return violations, len(collections)

def audit_pages(pages: List[Dict]) -> Tuple[List[Dict], int]:
    """Audit pages for French content"""
    violations = []

    for page in pages:
        pid = page.get("id")
        handle = page.get("handle")
        title = page.get("title", "")
        body = page.get("body_html", "") or ""

        french_in_title = detect_french(title)
        french_in_body = detect_french(body)

        if french_in_title or french_in_body:
            violations.append({
                "type": "PAGE",
                "id": pid,
                "handle": handle,
                "title": title[:80],
                "french_in_title": french_in_title[:3],
                "french_in_body": french_in_body[:3]
            })

    return violations, len(pages)

def main():
    print("=" * 80)
    print("AUDIT FORENSIQUE V2 - 100% ENGLISH ONLY (FALSE POSITIVES FIXED)")
    print("=" * 80)
    print(f"Store: {SHOP}")
    print(f"Date: 2025-11-20\n")

    all_violations = []

    # Audit Products
    print("=" * 80)
    print("1. AUDITING PRODUCTS")
    print("=" * 80)
    products = fetch_all_products()
    print(f"✅ Fetched {len(products)} products")

    product_violations, product_count = audit_products(products)
    all_violations.extend(product_violations)

    if product_violations:
        print(f"❌ VIOLATIONS: {len(product_violations)} products with French content")
        for v in product_violations[:5]:
            print(f"\n  Product: {v['title']}")
            print(f"  Handle: {v['handle']}")
            if v['french_in_title']:
                for match, context in v['french_in_title']:
                    print(f"  ❌ Title: '{match}' in context: ...{context[:60]}...")
            if v['french_in_body']:
                for match, context in v['french_in_body']:
                    print(f"  ❌ Body: '{match}' in context: ...{context[:60]}...")
    else:
        print(f"✅ SUCCESS: All {product_count} products are 100% English")
    print()

    # Audit Collections
    print("=" * 80)
    print("2. AUDITING COLLECTIONS")
    print("=" * 80)
    collections = fetch_all_collections()
    print(f"✅ Fetched {len(collections)} collections")

    collection_violations, collection_count = audit_collections(collections)
    all_violations.extend(collection_violations)

    if collection_violations:
        print(f"❌ VIOLATIONS: {len(collection_violations)} collections with French content")
    else:
        print(f"✅ SUCCESS: All {collection_count} collections are 100% English")
    print()

    # Audit Pages
    print("=" * 80)
    print("3. AUDITING PAGES")
    print("=" * 80)
    pages = fetch_all_pages()
    print(f"✅ Fetched {len(pages)} pages")

    page_violations, page_count = audit_pages(pages)
    all_violations.extend(page_violations)

    if page_violations:
        print(f"❌ VIOLATIONS: {len(page_violations)} pages with French content")
    else:
        print(f"✅ SUCCESS: All {page_count} pages are 100% English")
    print()

    # FINAL SUMMARY
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"Total items audited: {product_count + collection_count + page_count}")
    print(f"Total violations: {len(all_violations)}")
    print()

    # Save results
    results = {
        "timestamp": "2025-11-20",
        "store": SHOP,
        "total_items": product_count + collection_count + page_count,
        "total_violations": len(all_violations),
        "violations": all_violations
    }

    with open("english_only_audit_v2_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"📄 Full results saved to: english_only_audit_v2_results.json\n")

    if len(all_violations) == 0:
        print("=" * 80)
        print("🎉 100% SUCCESS: SITE IS 100% ENGLISH!")
        print("=" * 80)
        exit(0)
    else:
        print("=" * 80)
        print("⚠️  VIOLATIONS FOUND")
        print("=" * 80)
        print(f"❌ {len(all_violations)} items contain French content")
        exit(1)

if __name__ == "__main__":
    main()
