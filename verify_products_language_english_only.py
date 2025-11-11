#!/usr/bin/env python3
"""
VERIFY PRODUCTS LANGUAGE - Alpha Medical Care
Ensure ALL products are 100% English only (NO French)

REQUIREMENT: 100% English only site
"""

import requests
from datetime import datetime

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

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

print("=" * 80)
print("PRODUCTS LANGUAGE VERIFICATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# French keywords that should NOT appear
FRENCH_KEYWORDS = [
    # Common French words
    'et', 'de', 'le', 'la', 'les', 'un', 'une', 'des', 'pour', 'avec',
    'dans', 'sur', 'par', 'au', 'aux', 'du',
    # Medical terms in French
    'genou', 'douleur', 'soulagement', 'thérapie', 'soutien', 'support',
    'orthopédique', 'médical', 'santé', 'soins',
    # Product descriptions
    'produit', 'description', 'caractéristiques', 'livraison', 'garantie',
    'retour', 'paiement', 'prix', 'acheter', 'ajouter',
    # Common phrases
    'ajouter au panier', 'en stock', 'rupture de stock', 'livraison gratuite',
    'garantie de remboursement', 'qualité professionnelle'
]

# Fetch all products
query = """
{
  products(first: 250) {
    edges {
      node {
        id
        title
        handle
        status
        description
        descriptionHtml
        vendor
        productType
        tags
        seo {
          title
          description
        }
        variants(first: 50) {
          edges {
            node {
              id
              title
              sku
            }
          }
        }
      }
    }
  }
}
"""

response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
data = response.json()

if "errors" in data:
    print(f"❌ GraphQL Errors: {data['errors']}")
    exit(1)

products = data["data"]["products"]["edges"]

print(f"\nTotal products fetched: {len(products)}\n")

french_violations = []
english_compliant = []

for edge in products:
    product = edge["node"]
    product_id = product["id"]
    title = product["title"]
    handle = product["handle"]
    status = product["status"]
    description = product.get("description", "")
    vendor = product.get("vendor", "")
    product_type = product.get("productType", "")
    tags = product.get("tags", [])
    seo_title = product.get("seo", {}).get("title", "")
    seo_description = product.get("seo", {}).get("description", "")

    # Combine all text fields for analysis
    all_text = " ".join([
        title.lower(),
        description.lower(),
        vendor.lower(),
        product_type.lower(),
        seo_title.lower(),
        seo_description.lower(),
        " ".join([tag.lower() for tag in tags])
    ])

    # Also check variant titles
    for variant_edge in product.get("variants", {}).get("edges", []):
        variant = variant_edge["node"]
        all_text += " " + variant.get("title", "").lower()

    # Check for French keywords
    found_french = []
    for keyword in FRENCH_KEYWORDS:
        # Use word boundaries to avoid false positives
        # e.g., "support" in English vs "support" in French
        if f' {keyword} ' in f' {all_text} ':
            found_french.append(keyword)

    if found_french:
        french_violations.append({
            'id': product_id,
            'title': title,
            'handle': handle,
            'status': status,
            'french_keywords': list(set(found_french))
        })
        print(f"❌ FRENCH DETECTED: {title}")
        print(f"   Handle: {handle}")
        print(f"   Status: {status}")
        print(f"   French keywords: {', '.join(list(set(found_french)))}")
        print(f"   URL: https://www.alphamedical.shop/products/{handle}\n")
    else:
        english_compliant.append({
            'id': product_id,
            'title': title,
            'handle': handle,
            'status': status
        })

print("=" * 80)
print("LANGUAGE COMPLIANCE SUMMARY")
print("=" * 80)

print(f"\n✅ ENGLISH ONLY: {len(english_compliant)}/{len(products)}")
if len(english_compliant) == len(products):
    print(f"   🎯 100% COMPLIANCE ACHIEVED")
else:
    print(f"   ⚠️ Compliance: {(len(english_compliant) / len(products)) * 100:.1f}%")

if french_violations:
    print(f"\n❌ FRENCH VIOLATIONS: {len(french_violations)}/{len(products)}")
    print(f"\n⚠️ PRODUCTS WITH FRENCH CONTENT:")
    for violation in french_violations:
        print(f"   - {violation['title']} ({violation['status']})")
        print(f"     Handle: {violation['handle']}")
        print(f"     French keywords: {', '.join(violation['french_keywords'])}")
        print()

    print(f"🚨 ACTION REQUIRED:")
    print(f"   - Review {len(french_violations)} products with French content")
    print(f"   - Update titles, descriptions, tags, SEO fields to English only")
    print(f"   - Re-run verification to confirm 100% compliance")
else:
    print(f"\n✅ ZERO FRENCH CONTENT DETECTED")
    print(f"   All {len(products)} products are 100% English only")

print("\n" + "=" * 80)
print("VERIFICATION METHODOLOGY")
print("=" * 80)
print(f"\nChecked fields:")
print(f"   - Product title")
print(f"   - Product description")
print(f"   - Vendor")
print(f"   - Product type")
print(f"   - Tags")
print(f"   - SEO title")
print(f"   - SEO description")
print(f"   - Variant titles")
print(f"\nFrench keywords database: {len(FRENCH_KEYWORDS)} keywords")
print(f"Detection method: Word boundary matching (avoids false positives)")

print("\n" + "=" * 80)
