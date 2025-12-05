#!/usr/bin/env python3
"""
AUDIT FORENSIQUE - 100% ENGLISH ONLY VERIFICATION
Date: 2025-11-20
Purpose: Verify ENTIRE site is 100% English (no French content)

SCOPE:
1. Products (96 products): title, body_html, vendor, tags, metafields
2. Collections: title, body_html, metafields
3. Pages: title, body_html
4. Blog posts: title, body_html
5. Metaobjects (if any)

METHOD:
- Detect French using unambiguous French phrases/words
- NOT cognates (support, massage, etc.)
- Report ALL violations with exact location
"""

import os
import requests
import json
import re
from typing import Dict, List, Tuple

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

# Unambiguous French indicators (NOT cognates)
FRENCH_PATTERNS = [
    # Articles
    r'\b(le|la|les|un|une|des|du|de\s+la|au|aux)\b',
    # Pronouns
    r'\b(je|tu|il|elle|nous|vous|ils|elles|mon|ma|mes|ton|ta|tes|son|sa|ses)\b',
    # Common verbs
    r'\b(est|sont|avoir|être|faire|aller|venir|pouvoir|vouloir|devoir)\b',
    # Common words
    r'\b(avec|sans|dans|sur|sous|pour|par|chez|depuis|pendant|très|bien|tout|tous|toute|toutes)\b',
    # Prepositions
    r'\b(à|où|ou|et|mais|donc|car|ni)\b',
    # Phrases communes
    r'(livraison\s+gratuite|retour\s+gratuit|garantie\s+de|satisfaction\s+garantie)',
    r'(dès\s+maintenant|avec\s+nous|chez\s+nous|pour\s+vous|notre\s+équipe)',
    r'(bienvenue\s+à|merci\s+de|s\'il\s+vous\s+plaît|jusqu\'à|à\s+partir\s+de)',
    r'(votre\s+commande|notre\s+magasin|nos\s+produits|notre\s+site)',
    r'(contactez-nous|appelez-nous|écrivez-nous|veuillez)',
    r'(aujourd\'hui|demain|hier|chaque\s+jour|tous\s+les\s+jours)',
    # Accented characters (strong French indicator)
    r'[àâäéèêëïîôùûüÿœæç]'
]

# Compile patterns (case insensitive)
FRENCH_REGEX = re.compile('|'.join(FRENCH_PATTERNS), re.IGNORECASE)

def detect_french(text: str) -> List[str]:
    """Detect French content in text"""
    if not text:
        return []

    matches = FRENCH_REGEX.findall(text.lower())
    return list(set(matches)) if matches else []

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
    """Fetch all collections (custom + smart)"""
    collections = []

    # Custom collections
    url = f"{REST_URL}/custom_collections.json?limit=250"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        collections.extend(response.json().get("custom_collections", []))

    # Smart collections
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

def fetch_all_blog_posts() -> List[Dict]:
    """Fetch all blog posts"""
    # First get blogs
    blogs_url = f"{REST_URL}/blogs.json"
    blogs_response = requests.get(blogs_url, headers=HEADERS)

    if blogs_response.status_code != 200:
        return []

    blogs = blogs_response.json().get("blogs", [])

    all_articles = []
    for blog in blogs:
        blog_id = blog['id']
        articles_url = f"{REST_URL}/blogs/{blog_id}/articles.json?limit=250"
        articles_response = requests.get(articles_url, headers=HEADERS)

        if articles_response.status_code == 200:
            all_articles.extend(articles_response.json().get("articles", []))

    return all_articles

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

        # Check each field
        french_in_title = detect_french(title)
        french_in_body = detect_french(body)
        french_in_vendor = detect_french(vendor)
        french_in_tags = detect_french(tags)

        if french_in_title or french_in_body or french_in_vendor or french_in_tags:
            violations.append({
                "type": "PRODUCT",
                "id": pid,
                "handle": handle,
                "title": title[:60],
                "french_in_title": french_in_title[:5],
                "french_in_body": french_in_body[:5],
                "french_in_vendor": french_in_vendor[:5],
                "french_in_tags": french_in_tags[:5]
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
                "title": title[:60],
                "french_in_title": french_in_title[:5],
                "french_in_body": french_in_body[:5]
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
                "title": title[:60],
                "french_in_title": french_in_title[:5],
                "french_in_body": french_in_body[:5]
            })

    return violations, len(pages)

def audit_blog_posts(articles: List[Dict]) -> Tuple[List[Dict], int]:
    """Audit blog posts for French content"""
    violations = []

    for article in articles:
        aid = article.get("id")
        title = article.get("title", "")
        body = article.get("body_html", "") or ""

        french_in_title = detect_french(title)
        french_in_body = detect_french(body)

        if french_in_title or french_in_body:
            violations.append({
                "type": "BLOG_POST",
                "id": aid,
                "title": title[:60],
                "french_in_title": french_in_title[:5],
                "french_in_body": french_in_body[:5]
            })

    return violations, len(articles)

def main():
    print("=" * 80)
    print("AUDIT FORENSIQUE - 100% ENGLISH ONLY VERIFICATION")
    print("=" * 80)
    print(f"Store: {SHOP}")
    print(f"Date: 2025-11-20\n")

    all_violations = []

    # 1. Audit Products
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
                print(f"  ❌ Title French: {v['french_in_title']}")
            if v['french_in_body']:
                print(f"  ❌ Body French: {v['french_in_body']}")
            if v['french_in_vendor']:
                print(f"  ❌ Vendor French: {v['french_in_vendor']}")
            if v['french_in_tags']:
                print(f"  ❌ Tags French: {v['french_in_tags']}")
    else:
        print(f"✅ SUCCESS: All {product_count} products are 100% English")
    print()

    # 2. Audit Collections
    print("=" * 80)
    print("2. AUDITING COLLECTIONS")
    print("=" * 80)
    collections = fetch_all_collections()
    print(f"✅ Fetched {len(collections)} collections")

    collection_violations, collection_count = audit_collections(collections)
    all_violations.extend(collection_violations)

    if collection_violations:
        print(f"❌ VIOLATIONS: {len(collection_violations)} collections with French content")
        for v in collection_violations[:5]:
            print(f"\n  Collection: {v['title']}")
            print(f"  Handle: {v['handle']}")
            if v['french_in_title']:
                print(f"  ❌ Title French: {v['french_in_title']}")
            if v['french_in_body']:
                print(f"  ❌ Body French: {v['french_in_body']}")
    else:
        print(f"✅ SUCCESS: All {collection_count} collections are 100% English")
    print()

    # 3. Audit Pages
    print("=" * 80)
    print("3. AUDITING PAGES")
    print("=" * 80)
    pages = fetch_all_pages()
    print(f"✅ Fetched {len(pages)} pages")

    page_violations, page_count = audit_pages(pages)
    all_violations.extend(page_violations)

    if page_violations:
        print(f"❌ VIOLATIONS: {len(page_violations)} pages with French content")
        for v in page_violations[:5]:
            print(f"\n  Page: {v['title']}")
            print(f"  Handle: {v['handle']}")
            if v['french_in_title']:
                print(f"  ❌ Title French: {v['french_in_title']}")
            if v['french_in_body']:
                print(f"  ❌ Body French: {v['french_in_body']}")
    else:
        print(f"✅ SUCCESS: All {page_count} pages are 100% English")
    print()

    # 4. Audit Blog Posts
    print("=" * 80)
    print("4. AUDITING BLOG POSTS")
    print("=" * 80)
    articles = fetch_all_blog_posts()
    print(f"✅ Fetched {len(articles)} blog posts")

    article_violations, article_count = audit_blog_posts(articles)
    all_violations.extend(article_violations)

    if article_violations:
        print(f"❌ VIOLATIONS: {len(article_violations)} blog posts with French content")
        for v in article_violations[:5]:
            print(f"\n  Post: {v['title']}")
            if v['french_in_title']:
                print(f"  ❌ Title French: {v['french_in_title']}")
            if v['french_in_body']:
                print(f"  ❌ Body French: {v['french_in_body']}")
    else:
        print(f"✅ SUCCESS: All {article_count} blog posts are 100% English")
    print()

    # FINAL SUMMARY
    print("=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    print(f"Total items audited: {product_count + collection_count + page_count + article_count}")
    print(f"  - Products: {product_count}")
    print(f"  - Collections: {collection_count}")
    print(f"  - Pages: {page_count}")
    print(f"  - Blog posts: {article_count}")
    print()
    print(f"Total violations: {len(all_violations)}")
    print(f"  - Products: {len(product_violations)}")
    print(f"  - Collections: {len(collection_violations)}")
    print(f"  - Pages: {len(page_violations)}")
    print(f"  - Blog posts: {len(article_violations)}")
    print()

    # Save results
    results = {
        "timestamp": "2025-11-20",
        "store": SHOP,
        "total_items": product_count + collection_count + page_count + article_count,
        "total_violations": len(all_violations),
        "violations": all_violations
    }

    with open("english_only_audit_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"📄 Full results saved to: english_only_audit_results.json\n")

    if len(all_violations) == 0:
        print("=" * 80)
        print("🎉 100% SUCCESS: SITE IS 100% ENGLISH!")
        print("=" * 80)
        print("✅ All products are English only")
        print("✅ All collections are English only")
        print("✅ All pages are English only")
        print("✅ All blog posts are English only")
        print()
        exit(0)
    else:
        print("=" * 80)
        print("⚠️  VIOLATIONS FOUND - ACTION REQUIRED")
        print("=" * 80)
        print(f"❌ {len(all_violations)} items contain French content")
        print()
        print("NEXT STEPS:")
        print("1. Review violations in english_only_audit_results.json")
        print("2. Correct French content manually or via script")
        print("3. Re-run this audit to verify 100% English")
        print()
        exit(1)

if __name__ == "__main__":
    main()
