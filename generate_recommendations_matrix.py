#!/usr/bin/env python3
"""
GENERATE AI RECOMMENDATIONS MATRIX - Priority 1
Rule-based product similarity mapping (not true AI)
Creates static JavaScript file for frontend use
"""

import os
import json
import requests
from collections import defaultdict
from datetime import datetime

# Load credentials
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

def graphql_query(query):
    """Execute GraphQL query"""
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.json()

print("=" * 80)
print("GENERATING AI RECOMMENDATIONS MATRIX")
print("=" * 80)
print("Approach: Rule-based collaborative filtering (not true AI)")
print("Method: Product similarity based on tags, collections, type")
print()

# ============================================================================
# STEP 1: FETCH ALL ACTIVE PRODUCTS
# ============================================================================

print("Step 1: Fetching all active products...")

query = """
{
  products(first: 250, query: "status:active") {
    edges {
      node {
        id
        title
        handle
        productType
        tags
        collections(first: 10) {
          edges {
            node {
              title
              handle
            }
          }
        }
        variants(first: 1) {
          edges {
            node {
              price
              compareAtPrice
            }
          }
        }
      }
    }
  }
}
"""

result = graphql_query(query)

if not result or 'data' not in result:
    print("❌ Failed to fetch products")
    exit(1)

products = []
for edge in result['data']['products']['edges']:
    product = edge['node']

    # Extract collections
    collections = [c['node']['handle'] for c in product['collections']['edges']]

    # Extract variant info
    variant = product['variants']['edges'][0]['node'] if product['variants']['edges'] else None
    price = float(variant['price']) if variant else 0
    compare_at = float(variant['compareAtPrice']) if variant and variant['compareAtPrice'] else 0

    products.append({
        'id': product['id'],
        'title': product['title'],
        'handle': product['handle'],
        'type': product['productType'],
        'tags': product['tags'],
        'collections': collections,
        'price': price,
        'compare_at': compare_at
    })

print(f"✅ Fetched {len(products)} active products")

# ============================================================================
# STEP 2: BUILD SIMILARITY MATRIX
# ============================================================================

print("\nStep 2: Building similarity matrix...")

recommendations = {}

for product in products:
    handle = product['handle']

    # Find similar products (same collection + overlapping tags)
    similar = []
    complements = []
    upgrades = []

    for other in products:
        if other['handle'] == handle:
            continue

        # Calculate similarity score
        similarity_score = 0

        # Same collection = +3 points
        common_collections = set(product['collections']) & set(other['collections'])
        if len(common_collections) > 0:
            similarity_score += 3

        # Common tags = +1 point per tag (max 5)
        common_tags = set(product['tags']) & set(other['tags'])
        similarity_score += min(len(common_tags), 5)

        # Same product type = +2 points
        if product['type'] == other['type']:
            similarity_score += 2

        # Categorize based on score
        if similarity_score >= 6:
            similar.append(other['handle'])
        elif similarity_score >= 3:
            complements.append(other['handle'])

    # Find bundles containing this product (upgrades)
    for bundle in products:
        # Bundles have "bundle" in tags or "bundles" collection
        is_bundle = any('bundle' in tag.lower() for tag in bundle['tags'])
        is_bundle_collection = any('bundle' in col for col in bundle['collections'])

        if (is_bundle or is_bundle_collection) and bundle['handle'] != handle:
            # Check if current product type matches bundle tags
            product_keywords = product['type'].lower().split() + [tag.lower() for tag in product['tags']]
            bundle_keywords = bundle['title'].lower().split() + [tag.lower() for tag in bundle['tags']]

            overlap = set(product_keywords) & set(bundle_keywords)
            if len(overlap) >= 2:
                upgrades.append(bundle['handle'])

    # Limit recommendations
    recommendations[handle] = {
        'similar': similar[:5],  # Top 5 similar
        'complements': complements[:5],  # Top 5 complements
        'upgrades': upgrades[:3]  # Top 3 bundles
    }

print(f"✅ Generated recommendations for {len(recommendations)} products")

# ============================================================================
# STEP 3: GENERATE JAVASCRIPT FILE
# ============================================================================

print("\nStep 3: Generating JavaScript file...")

js_content = """/**
 * AI RECOMMENDATIONS MATRIX
 * Generated: """ + str(datetime.now()) + """
 * Products: """ + str(len(recommendations)) + """
 * Approach: Rule-based collaborative filtering
 *
 * Usage:
 * - similar: Same category/type products
 * - complements: Related products from different categories
 * - upgrades: Bundles containing similar products
 */

window.PRODUCT_RECOMMENDATIONS = """ + json.dumps(recommendations, indent=2) + """;

/**
 * Get recommendations for a product
 * @param {string} productHandle - Product handle
 * @param {string} type - Type of recommendations ('similar', 'complements', 'upgrades')
 * @returns {Array} Array of product handles
 */
window.getRecommendations = function(productHandle, type = 'similar') {
  const recs = window.PRODUCT_RECOMMENDATIONS[productHandle];
  if (!recs) return [];
  return recs[type] || [];
};

/**
 * Get all recommendations for a product
 * @param {string} productHandle - Product handle
 * @returns {Object} Object with similar, complements, upgrades arrays
 */
window.getAllRecommendations = function(productHandle) {
  return window.PRODUCT_RECOMMENDATIONS[productHandle] || {
    similar: [],
    complements: [],
    upgrades: []
  };
};
"""

js_content = js_content.replace("datetime.now()", datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC'))

# Save JS file
output_path = '/Users/mac/Desktop/Alpha-Medical/assets/product-recommendations-matrix.js'
with open(output_path, 'w') as f:
    f.write(js_content)

print(f"✅ JavaScript file created: {output_path}")

# ============================================================================
# STEP 4: GENERATE STATISTICS
# ============================================================================

print("\nStep 4: Generating statistics...")

total_products = len(recommendations)
products_with_similar = sum(1 for r in recommendations.values() if len(r['similar']) > 0)
products_with_complements = sum(1 for r in recommendations.values() if len(r['complements']) > 0)
products_with_upgrades = sum(1 for r in recommendations.values() if len(r['upgrades']) > 0)

avg_similar = sum(len(r['similar']) for r in recommendations.values()) / total_products
avg_complements = sum(len(r['complements']) for r in recommendations.values()) / total_products
avg_upgrades = sum(len(r['upgrades']) for r in recommendations.values()) / total_products

print(f"\n📊 STATISTICS:")
print(f"  Total products: {total_products}")
print(f"  Products with similar: {products_with_similar} ({products_with_similar/total_products*100:.1f}%)")
print(f"  Products with complements: {products_with_complements} ({products_with_complements/total_products*100:.1f}%)")
print(f"  Products with upgrades: {products_with_upgrades} ({products_with_upgrades/total_products*100:.1f}%)")
print(f"\n  Average similar/product: {avg_similar:.1f}")
print(f"  Average complements/product: {avg_complements:.1f}")
print(f"  Average upgrades/product: {avg_upgrades:.1f}")

# ============================================================================
# STEP 5: SAMPLE RECOMMENDATIONS
# ============================================================================

print("\n" + "=" * 80)
print("SAMPLE RECOMMENDATIONS")
print("=" * 80)

# Show sample for 3 products
sample_products = products[:3]

for product in sample_products:
    handle = product['handle']
    recs = recommendations[handle]

    print(f"\nProduct: \"{product['title']}\"")
    print(f"Handle: {handle}")
    print(f"  Similar ({len(recs['similar'])}): {', '.join(recs['similar'][:3]) if recs['similar'] else 'None'}")
    print(f"  Complements ({len(recs['complements'])}): {', '.join(recs['complements'][:3]) if recs['complements'] else 'None'}")
    print(f"  Upgrades ({len(recs['upgrades'])}): {', '.join(recs['upgrades'][:2]) if recs['upgrades'] else 'None'}")

# ============================================================================
# FINAL OUTPUT
# ============================================================================

print("\n" + "=" * 80)
print("SUCCESS")
print("=" * 80)
print(f"✅ Recommendations matrix generated")
print(f"✅ JavaScript file: assets/product-recommendations-matrix.js")
print(f"✅ Products covered: {len(recommendations)}")
print()
print("NEXT STEPS:")
print("1. Deploy to Shopify theme assets")
print("2. Create smart-recommendations.liquid snippet")
print("3. Integrate into product pages")
print("=" * 80)
