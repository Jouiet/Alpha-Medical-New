#!/usr/bin/env python3
"""
ANALYZE PERSONAS & IDENTIFY OPTIMAL BUNDLES
Alpha Medical Store - Bottom-up approach basée sur FAITS

Objectif:
1. Analyser collections existantes pour identifier personas
2. Analyser produits par collection
3. Identifier 10-12 bundles optimaux:
   - 1 bundle par persona (optimal)
   - 3-4 produits par bundle
   - AUCUN doublon (produits UNIQUES)
   - Synergies produits (complémentaires)

NO SUPPOSITIONS - ONLY DATA-DRIVEN DECISIONS
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

API_VERSION = "2024-10"
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
print("ALPHA MEDICAL - PERSONAS & BUNDLES ANALYSIS")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# ============================================================================
# 1. FETCH ALL COLLECTIONS WITH PRODUCTS
# ============================================================================
print("\n1. Fetching collections with products...\n")

query = """
{
  collections(first: 20) {
    edges {
      node {
        id
        title
        handle
        description
        productsCount {
          count
        }
        products(first: 100) {
          edges {
            node {
              id
              title
              handle
              status
              priceRangeV2 {
                minVariantPrice {
                  amount
                }
              }
            }
          }
        }
      }
    }
  }
}
"""

result = graphql_query(query)

if not result:
    print("❌ Failed to fetch collections")
    exit(1)

collections = result["data"]["collections"]["edges"]

print(f"Found {len(collections)} collections:\n")

# Filter main collections (exclude promotional)
main_collections = []
promotional_collections = []

for edge in collections:
    col = edge["node"]
    handle = col["handle"]
    count = col["productsCount"]["count"]

    # Classify collections
    if handle in ["bestsellers", "new-arrivals", "bundle-deals", "frontpage"]:
        promotional_collections.append(col)
    else:
        main_collections.append(col)

    collection_type = "PROMOTIONAL" if handle in ["bestsellers", "new-arrivals", "bundle-deals", "frontpage"] else "MAIN"
    print(f"{'📌' if collection_type == 'MAIN' else '🏷️'} {col['title']:30} ({count:3} products) - {collection_type}")

print(f"\nMain Collections: {len(main_collections)}")
print(f"Promotional Collections: {len(promotional_collections)}")

# ============================================================================
# 2. ANALYZE PERSONAS FROM MAIN COLLECTIONS
# ============================================================================
print("\n" + "="*80)
print("2. PERSONA IDENTIFICATION (based on collections)")
print("="*80)

personas = {}

for col in main_collections:
    handle = col["handle"]
    title = col["title"]
    products = [p["node"] for p in col["products"]["edges"] if p["node"]["status"] == "ACTIVE"]

    # Identify persona from collection name/description
    persona_name = title  # Collection title as persona

    personas[handle] = {
        "name": title,
        "handle": handle,
        "product_count": len(products),
        "products": products,
        "description": col["description"][:200] if col["description"] else ""
    }

    print(f"\n📌 PERSONA: {title}")
    print(f"   Handle: {handle}")
    print(f"   Products: {len(products)} active")
    print(f"   Description: {personas[handle]['description'][:80]}...")

# ============================================================================
# 3. BUNDLE STRATEGY PLANNING
# ============================================================================
print("\n" + "="*80)
print("3. BUNDLE STRATEGY PLANNING")
print("="*80)

print("\n🎯 BUNDLE RULES:")
print("   - 10-12 bundles total (optimal)")
print("   - 3-4 products per bundle")
print("   - NO duplicates across bundles (each product used max 1x)")
print("   - Products must be complementary (same persona/use case)")
print("   - Priority: Main collections (Pain Relief, Posture, Therapy)")

# Identify top products by collection
bundle_candidates = []

for handle, persona in personas.items():
    products = persona["products"]

    if len(products) < 3:
        print(f"\n⚠️  {persona['name']}: Only {len(products)} products (skip)")
        continue

    # Sort by price (mix of price points in bundle)
    products_sorted = sorted(products, key=lambda p: float(p["priceRangeV2"]["minVariantPrice"]["amount"]))

    # Calculate how many bundles we can create from this persona
    max_bundles = len(products) // 4  # 4 products per bundle (conservative)

    print(f"\n✅ {persona['name']}:")
    print(f"   Products available: {len(products)}")
    print(f"   Max bundles (4 prod/bundle): {max_bundles}")
    print(f"   Price range: ${float(products_sorted[0]['priceRangeV2']['minVariantPrice']['amount']):.2f} - ${float(products_sorted[-1]['priceRangeV2']['minVariantPrice']['amount']):.2f}")

    # Generate bundle suggestions for this persona
    bundles_for_persona = []

    for i in range(min(max_bundles, 3)):  # Max 3 bundles per persona
        start_idx = i * 4
        end_idx = start_idx + 4

        if end_idx > len(products_sorted):
            break

        bundle_products = products_sorted[start_idx:end_idx]
        bundle_name = f"{persona['name']} Bundle #{i+1}"
        bundle_price = sum(float(p["priceRangeV2"]["minVariantPrice"]["amount"]) for p in bundle_products)

        bundles_for_persona.append({
            "name": bundle_name,
            "persona": persona["name"],
            "products": bundle_products,
            "product_count": len(bundle_products),
            "total_price": bundle_price,
            "suggested_bundle_price": bundle_price * 0.85  # 15% discount
        })

    if bundles_for_persona:
        bundle_candidates.extend(bundles_for_persona)
        print(f"   Generated {len(bundles_for_persona)} bundle(s)")

# ============================================================================
# 4. FINAL BUNDLE SELECTION (Top 10-12)
# ============================================================================
print("\n" + "="*80)
print("4. FINAL BUNDLE SELECTION (Top 10-12)")
print("="*80)

# Sort bundles by total price (diversify price points)
bundle_candidates_sorted = sorted(bundle_candidates, key=lambda b: b["total_price"], reverse=True)

# Select top 10-12 bundles
final_bundles = bundle_candidates_sorted[:12]

print(f"\n📦 SELECTED {len(final_bundles)} BUNDLES:\n")

for idx, bundle in enumerate(final_bundles, 1):
    print(f"{idx}. {bundle['name']}")
    print(f"   Persona: {bundle['persona']}")
    print(f"   Products: {bundle['product_count']}")
    print(f"   Total Price: ${bundle['total_price']:.2f}")
    print(f"   Bundle Price (15% off): ${bundle['suggested_bundle_price']:.2f}")
    print(f"   Savings: ${bundle['total_price'] - bundle['suggested_bundle_price']:.2f}")
    print(f"   Products:")
    for prod in bundle["products"]:
        price = float(prod["priceRangeV2"]["minVariantPrice"]["amount"])
        print(f"      - {prod['title'][:60]:60} | ${price:.2f}")
    print()

# ============================================================================
# 5. SAVE RESULTS
# ============================================================================
output_file = "bundles_strategy.json"
with open(output_file, 'w') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "personas": {k: {"name": v["name"], "product_count": v["product_count"]} for k, v in personas.items()},
        "bundle_candidates_count": len(bundle_candidates),
        "final_bundles": final_bundles
    }, f, indent=2)

print("="*80)
print("SUMMARY")
print("="*80)
print(f"\n✅ Identified {len(personas)} personas")
print(f"✅ Generated {len(bundle_candidates)} bundle candidates")
print(f"✅ Selected {len(final_bundles)} final bundles")
print(f"\n📄 Results saved to: {output_file}")
print("\n🔥 NEXT STEP: Create these bundles as native Shopify products")
print("   Script: create_native_bundles.py")
print("\n" + "="*80)
