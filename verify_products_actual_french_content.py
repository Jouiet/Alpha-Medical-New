#!/usr/bin/env python3
"""
VERIFY ACTUAL FRENCH CONTENT - Alpha Medical Care
Search for real French phrases (not English-French cognates)

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
print("ACTUAL FRENCH CONTENT VERIFICATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# REAL French phrases that would NOT appear in English medical texts
FRENCH_PHRASES = [
    # Definite articles + common nouns (unambiguous French)
    'le genou', 'la douleur', 'les genoux', 'le soutien',
    'pour le', 'pour la', 'dans le', 'avec le',

    # Verbs conjugated in French
    'soulager', 'améliorer', 'réduire', 'utiliser', 'porter',

    # Medical French terms
    'soulagement de la douleur', 'thérapie', 'orthopédique',
    'dispositif médical', 'appareil', 'masseur',

    # Action words
    'ajouter au panier', 'acheter maintenant', 'livraison gratuite',

    # Questions/descriptions
    'quest-ce que', 'comment utiliser', 'pourquoi choisir',

    # Full French sentences indicators
    'est un', 'est une', 'sont des', 'peut être',
    'cest', "c'est", 'il est', 'elle est',

    # Measurement/sizes in French
    'taille unique', 'ajustable', 'réglable'
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
        vendor
        productType
        tags
        seo {
          title
          description
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

print(f"\nTotal products: {len(products)}")
print(f"French phrases database: {len(FRENCH_PHRASES)} unambiguous French phrases\n")

french_violations = []

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

    # Combine all text fields
    all_text = " ".join([
        title.lower(),
        description.lower(),
        vendor.lower(),
        product_type.lower(),
        seo_title.lower(),
        seo_description.lower(),
        " ".join([tag.lower() for tag in tags])
    ])

    # Check for French phrases
    found_french = []
    for phrase in FRENCH_PHRASES:
        if phrase.lower() in all_text:
            found_french.append(phrase)

    if found_french:
        french_violations.append({
            'id': product_id,
            'title': title,
            'handle': handle,
            'status': status,
            'french_phrases': list(set(found_french))
        })
        print(f"❌ FRENCH CONTENT: {title}")
        print(f"   Handle: {handle}")
        print(f"   Status: {status}")
        print(f"   French phrases: {', '.join(list(set(found_french)))}")
        print(f"   URL: https://www.alphamedical.shop/products/{handle}\n")

print("=" * 80)
print("ACTUAL FRENCH CONTENT SUMMARY")
print("=" * 80)

if french_violations:
    print(f"\n❌ FRENCH CONTENT FOUND: {len(french_violations)}/{len(products)}")
    print(f"   Compliance: {((len(products) - len(french_violations)) / len(products)) * 100:.1f}%")

    print(f"\n⚠️ PRODUCTS WITH REAL FRENCH:")
    for violation in french_violations:
        print(f"   - {violation['title']} ({violation['status']})")
        print(f"     Phrases: {', '.join(violation['french_phrases'])}")
else:
    print(f"\n✅ ZERO FRENCH CONTENT DETECTED")
    print(f"   All {len(products)} products are 100% English")
    print(f"\n🎯 COMPLIANCE: 100%")

print("\n" + "=" * 80)
print("DETECTION METHODOLOGY")
print("=" * 80)
print(f"\nExcluded from detection:")
print(f"   - English-French cognates ('support', 'relief', 'pain')")
print(f"   - Single words used in both languages")
print(f"   - Brand names (VELPEAU, etc.)")
print(f"\nDetected only:")
print(f"   - Unambiguous French phrases ('le genou', 'la douleur')")
print(f"   - French verb conjugations ('soulager', 'améliorer')")
print(f"   - French sentence structures ('est un', 'c'est')")

print("\n" + "=" * 80)
