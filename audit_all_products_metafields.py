#!/usr/bin/env python3
"""
AUDIT COMPLET - TOUS LES PRODUITS ACTIFS
Vérification FACTUELLE RIGOUREUSE des metafields sur CHAQUE produit

Critères vérifiés:
1. global.title_tag (SEO title)
2. global.description_tag (SEO meta description)
3. Loox reviews (loox.avg_rating, loox.num_reviews)
4. Product status (ACTIVE only)
5. Draft products exclusion

NO SUPPOSITIONS - ONLY VERIFIED FACTS
"""

import os
import json
import requests
from datetime import datetime

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
    if not SHOPIFY_TOKEN:
        raise ValueError("SHOPIFY_ADMIN_ACCESS_TOKEN not found")
except Exception as e:
    print(f"❌ Error loading credentials: {e}")
    exit(1)

API_VERSION = "2024-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query, variables=None):
    """Execute GraphQL query"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    data = response.json()

    if "errors" in data:
        print("❌ GraphQL Errors:")
        for error in data["errors"]:
            print(f"   - {error.get('message', 'Unknown error')}")
        return None

    return data

print("="*80)
print("ALPHA MEDICAL - AUDIT COMPLET PRODUITS ACTIFS")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# Fetch ALL active products with pagination
all_products = []
has_next_page = True
cursor = None

print("\n1. Fetching ALL active products...")

while has_next_page:
    query = """
    query getProducts($cursor: String) {
      products(first: 50, after: $cursor, query: "status:ACTIVE") {
        edges {
          node {
            id
            title
            handle
            status
            metafields(first: 20) {
              edges {
                node {
                  namespace
                  key
                  value
                  type
                }
              }
            }
          }
          cursor
        }
        pageInfo {
          hasNextPage
        }
      }
    }
    """

    variables = {"cursor": cursor} if cursor else {}
    result = graphql_query(query, variables)

    if not result or "data" not in result:
        print("❌ Failed to fetch products")
        break

    products = result["data"]["products"]["edges"]
    all_products.extend(products)

    has_next_page = result["data"]["products"]["pageInfo"]["hasNextPage"]
    if has_next_page and products:
        cursor = products[-1]["cursor"]

    print(f"   Fetched {len(products)} products (Total: {len(all_products)})")

print(f"\n✅ Total active products fetched: {len(all_products)}")

# Analyze metafields
print("\n" + "="*80)
print("2. METAFIELDS ANALYSIS")
print("="*80)

metafields_stats = {
    "total_products": len(all_products),
    "has_title_tag": 0,
    "has_description_tag": 0,
    "has_loox_rating": 0,
    "has_loox_reviews": 0,
    "has_all_seo": 0,
    "has_no_metafields": 0,
    "missing_title": [],
    "missing_description": [],
    "draft_products_found": 0
}

products_details = []

for edge in all_products:
    product = edge["node"]

    # Check if DRAFT (should not happen with query filter, but verify)
    if product["status"] != "ACTIVE":
        metafields_stats["draft_products_found"] += 1
        continue

    metafields = product["metafields"]["edges"]

    # Extract metafield keys
    metafield_keys = {}
    for mf_edge in metafields:
        mf = mf_edge["node"]
        key = f"{mf['namespace']}.{mf['key']}"
        metafield_keys[key] = mf['value']

    has_title = "global.title_tag" in metafield_keys
    has_desc = "global.description_tag" in metafield_keys
    has_loox_rating = "loox.avg_rating" in metafield_keys
    has_loox_reviews = "loox.num_reviews" in metafield_keys

    # Update stats
    if has_title:
        metafields_stats["has_title_tag"] += 1
    else:
        metafields_stats["missing_title"].append(product["handle"])

    if has_desc:
        metafields_stats["has_description_tag"] += 1
    else:
        metafields_stats["missing_description"].append(product["handle"])

    if has_loox_rating:
        metafields_stats["has_loox_rating"] += 1

    if has_loox_reviews:
        metafields_stats["has_loox_reviews"] += 1

    if has_title and has_desc:
        metafields_stats["has_all_seo"] += 1

    if not metafields:
        metafields_stats["has_no_metafields"] += 1

    # Store product details
    products_details.append({
        "id": product["id"],
        "title": product["title"],
        "handle": product["handle"],
        "status": product["status"],
        "metafields_count": len(metafields),
        "has_title_tag": has_title,
        "has_description_tag": has_desc,
        "has_loox_rating": has_loox_rating,
        "has_loox_reviews": has_loox_reviews,
        "has_all_seo": has_title and has_desc
    })

# Calculate percentages
total = metafields_stats["total_products"]

print(f"\n📊 METAFIELDS COMPLIANCE:\n")
print(f"Total ACTIVE products: {total}")
print(f"\nSEO Metafields:")
print(f"   ✅ global.title_tag: {metafields_stats['has_title_tag']}/{total} ({metafields_stats['has_title_tag']/total*100:.1f}%)")
print(f"   ✅ global.description_tag: {metafields_stats['has_description_tag']}/{total} ({metafields_stats['has_description_tag']/total*100:.1f}%)")
print(f"   ✅ Both SEO tags: {metafields_stats['has_all_seo']}/{total} ({metafields_stats['has_all_seo']/total*100:.1f}%)")

print(f"\nLoox Reviews:")
print(f"   📊 loox.avg_rating: {metafields_stats['has_loox_rating']}/{total} ({metafields_stats['has_loox_rating']/total*100:.1f}%)")
print(f"   📊 loox.num_reviews: {metafields_stats['has_loox_reviews']}/{total} ({metafields_stats['has_loox_reviews']/total*100:.1f}%)")

print(f"\nNo Metafields: {metafields_stats['has_no_metafields']}/{total} ({metafields_stats['has_no_metafields']/total*100:.1f}%)")

if metafields_stats["draft_products_found"] > 0:
    print(f"\n⚠️  DRAFT products found (should be filtered): {metafields_stats['draft_products_found']}")

# Show missing SEO products
if metafields_stats["missing_title"]:
    print(f"\n❌ Products missing title_tag ({len(metafields_stats['missing_title'])}):")
    for handle in metafields_stats["missing_title"][:10]:
        print(f"   - {handle}")
    if len(metafields_stats["missing_title"]) > 10:
        print(f"   ... and {len(metafields_stats['missing_title']) - 10} more")

if metafields_stats["missing_description"]:
    print(f"\n❌ Products missing description_tag ({len(metafields_stats['missing_description'])}):")
    for handle in metafields_stats["missing_description"][:10]:
        print(f"   - {handle}")
    if len(metafields_stats["missing_description"]) > 10:
        print(f"   ... and {len(metafields_stats['missing_description']) - 10} more")

# Final verdict
print("\n" + "="*80)
print("VERDICT")
print("="*80)

seo_compliance = metafields_stats["has_all_seo"] / total * 100

if seo_compliance == 100:
    print(f"\n✅ SEO COMPLIANCE: 100% PERFECT")
    print(f"   All {total} active products have both title_tag and description_tag")
elif seo_compliance >= 95:
    print(f"\n✅ SEO COMPLIANCE: {seo_compliance:.1f}% EXCELLENT")
    print(f"   {metafields_stats['has_all_seo']}/{total} products have both SEO tags")
elif seo_compliance >= 80:
    print(f"\n⚠️  SEO COMPLIANCE: {seo_compliance:.1f}% GOOD (needs improvement)")
    print(f"   {metafields_stats['has_all_seo']}/{total} products have both SEO tags")
else:
    print(f"\n❌ SEO COMPLIANCE: {seo_compliance:.1f}% POOR (action required)")
    print(f"   Only {metafields_stats['has_all_seo']}/{total} products have both SEO tags")

# Save results
output_file = "audit_products_metafields_results.json"
with open(output_file, 'w') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "stats": metafields_stats,
        "products": products_details
    }, f, indent=2)

print(f"\n✅ Detailed results saved to: {output_file}")
print("\n" + "="*80)
