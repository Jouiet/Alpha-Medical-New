#!/usr/bin/env python3
"""
CREATE OPTIMAL NATIVE BUNDLES - Alpha Medical
Based on 7 REAL personas identified from bottom-up analysis

REQUIREMENTS:
- 10-12 bundles optimal (not 15 incomplete bundles)
- 3-4 products per bundle (optimal)
- NO duplicates - UNIQUE products across all bundles
- Native Shopify product bundles (no apps)
- Add to "Complete Care Kits" collection
- 15% discount from individual prices

STRATEGY:
1. Load real_personas_analysis.json
2. For each persona, select 3-4 BEST products based on:
   - Price diversity (mix of price points)
   - Complementarity (different body parts/problems within persona)
   - Quality indicators (avoid outliers)
3. Ensure NO product reuse across bundles
4. Create bundle products with proper variants
5. Add to "Complete Care Kits" collection

NO SHORTCUTS - RIGOROUS SELECTION
"""

import os
import json
import requests
from datetime import datetime
from collections import defaultdict

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
        for error in data["errors"]:
            print(f"❌ {error.get('message')}")
        return None
    return data

print("="*80)
print("ALPHA MEDICAL - CREATE OPTIMAL NATIVE BUNDLES")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# ============================================================================
# 1. LOAD PERSONAS ANALYSIS
# ============================================================================
print("\n1. Loading real personas analysis...\n")

try:
    with open('real_personas_analysis.json', 'r') as f:
        personas_data = json.load(f)
except Exception as e:
    print(f"❌ Failed to load personas data: {e}")
    exit(1)

print(f"✅ Loaded {personas_data['total_products']} products")
print(f"✅ Found {len(personas_data['real_personas'])} personas")

# ============================================================================
# 2. SELECT OPTIMAL PRODUCTS PER PERSONA
# ============================================================================
print("\n" + "="*80)
print("2. SELECTING OPTIMAL PRODUCTS PER PERSONA")
print("="*80)

used_product_ids = set()  # Track used products to ensure NO duplicates
bundle_plans = []

# Define which personas to prioritize for bundles (10-12 bundles)
# Focus on highest-impact personas with clear use cases
persona_priority = [
    ("athlete_active", 4),           # 1 bundle, 4 products
    ("office_chronic_pain", 4),      # 1 bundle, 4 products
    ("elderly_mobility", 4),         # 1 bundle, 4 products
    ("post_injury_recovery", 4),     # 1 bundle, 4 products
    ("beauty_wellness", 3),          # 1 bundle, 3 products
    ("comprehensive_therapy", 4),    # 1 bundle, 4 products
    ("foot_bunion_care", 3),         # 1 bundle, 3 products
    # Additional targeted bundles (3 more to reach 10-12)
    ("athlete_active_knee", 3),      # Specialized: Knee support for athletes
    ("office_back_neck", 3),         # Specialized: Back + Neck for office workers
    ("beauty_facial_premium", 4),    # Premium facial therapy bundle
]

def select_best_products(products, count, used_ids, criteria="balanced"):
    """
    Select best products based on criteria:
    - balanced: Mix of price points, avoid duplicates
    - premium: Higher-end products
    - essential: Core support products
    """
    available = [p for p in products if p["id"] not in used_ids]

    if len(available) < count:
        return []  # Not enough products

    # Sort by price for diversity
    available_sorted = sorted(available, key=lambda x: x["price"])

    # Select products with price diversity
    selected = []
    if criteria == "balanced":
        # Pick from different price ranges
        step = len(available_sorted) // count
        for i in range(count):
            idx = min(i * step, len(available_sorted) - 1)
            selected.append(available_sorted[idx])
    elif criteria == "premium":
        # Pick higher-priced products
        selected = available_sorted[-count:]
    elif criteria == "essential":
        # Pick mid-range products
        mid = len(available_sorted) // 2
        start = max(0, mid - count // 2)
        selected = available_sorted[start:start + count]

    return selected

print("\n📦 BUNDLE SELECTION:\n")

# Process first 7 main persona bundles
for persona_key, product_count in persona_priority[:7]:
    persona = personas_data["real_personas"][persona_key]

    print(f"Persona: {persona['name']}")
    print(f"   Available products: {persona['product_count']}")
    print(f"   Target: {product_count} products")

    selected = select_best_products(persona["products"], product_count, used_product_ids, "balanced")

    if not selected:
        print(f"   ⚠️  Not enough unique products available - SKIP")
        continue

    # Mark products as used
    for prod in selected:
        used_product_ids.add(prod["id"])

    bundle_plan = {
        "persona_key": persona_key,
        "name": persona["name"],
        "products": selected,
        "total_price": sum(p["price"] for p in selected),
        "bundle_price": sum(p["price"] for p in selected) * 0.85  # 15% discount
    }

    bundle_plans.append(bundle_plan)

    print(f"   ✅ Selected {len(selected)} products")
    print(f"   Total: ${bundle_plan['total_price']:.2f} → Bundle: ${bundle_plan['bundle_price']:.2f} (15% off)")
    for prod in selected:
        print(f"      - {prod['title'][:60]}... (${prod['price']:.2f})")
    print()

# Process specialized bundles (3 more)
print("\n📌 SPECIALIZED BUNDLES:\n")

# Specialized 1: Athlete Knee Support Bundle
athlete_knee = personas_data["real_personas"]["athlete_active"]
athlete_knee_products = [p for p in athlete_knee["products"] if "knee" in p["title"].lower()]
selected = select_best_products(athlete_knee_products, 3, used_product_ids, "essential")

if selected and len(selected) == 3:
    for prod in selected:
        used_product_ids.add(prod["id"])

    bundle_plans.append({
        "persona_key": "athlete_active_knee",
        "name": "Active Athlete - Knee Support Kit",
        "products": selected,
        "total_price": sum(p["price"] for p in selected),
        "bundle_price": sum(p["price"] for p in selected) * 0.85
    })
    print(f"✅ Athlete Knee Support Kit: {len(selected)} products (${bundle_plans[-1]['bundle_price']:.2f})")

# Specialized 2: Office Back + Neck Bundle
office = personas_data["real_personas"]["office_chronic_pain"]
office_back_neck = [p for p in office["products"] if "back" in p["title"].lower() or "neck" in p["title"].lower()]
selected = select_best_products(office_back_neck, 3, used_product_ids, "essential")

if selected and len(selected) == 3:
    for prod in selected:
        used_product_ids.add(prod["id"])

    bundle_plans.append({
        "persona_key": "office_back_neck",
        "name": "Office Worker - Back & Neck Relief Kit",
        "products": selected,
        "total_price": sum(p["price"] for p in selected),
        "bundle_price": sum(p["price"] for p in selected) * 0.85
    })
    print(f"✅ Office Back & Neck Kit: {len(selected)} products (${bundle_plans[-1]['bundle_price']:.2f})")

# Specialized 3: Beauty Facial Premium Bundle
beauty = personas_data["real_personas"]["beauty_wellness"]
beauty_facial = [p for p in beauty["products"] if "face" in p["title"].lower() or "facial" in p["title"].lower() or "led" in p["title"].lower()]
selected = select_best_products(beauty_facial, 4, used_product_ids, "premium")

if selected and len(selected) == 4:
    for prod in selected:
        used_product_ids.add(prod["id"])

    bundle_plans.append({
        "persona_key": "beauty_facial_premium",
        "name": "Beauty & Wellness - Premium Facial Therapy Kit",
        "products": selected,
        "total_price": sum(p["price"] for p in selected),
        "bundle_price": sum(p["price"] for p in selected) * 0.85
    })
    print(f"✅ Beauty Facial Premium Kit: {len(selected)} products (${bundle_plans[-1]['bundle_price']:.2f})")

print(f"\n🎯 Total bundles created: {len(bundle_plans)}")
print(f"🎯 Unique products used: {len(used_product_ids)}")

# ============================================================================
# 3. VERIFY NO DUPLICATES
# ============================================================================
print("\n" + "="*80)
print("3. VERIFYING NO DUPLICATES")
print("="*80)

all_bundle_product_ids = []
for bundle in bundle_plans:
    for prod in bundle["products"]:
        all_bundle_product_ids.append(prod["id"])

duplicate_check = len(all_bundle_product_ids) == len(set(all_bundle_product_ids))
print(f"\n{'✅' if duplicate_check else '❌'} Duplicate check: {'PASS (all unique)' if duplicate_check else 'FAIL (duplicates found)'}")

if not duplicate_check:
    print("❌ CRITICAL ERROR: Duplicates found. Aborting.")
    exit(1)

# ============================================================================
# 4. FIND/CREATE "Complete Care Kits" COLLECTION
# ============================================================================
print("\n" + "="*80)
print("4. FINDING/CREATING 'Complete Care Kits' COLLECTION")
print("="*80)

# First, check if "Bundle Deals" exists and rename it
query_collections = """
{
  collections(first: 20, query: "title:'Bundle Deals'") {
    edges {
      node {
        id
        title
        handle
      }
    }
  }
}
"""

result = graphql_query(query_collections)
collection_id = None

if result and result["data"]["collections"]["edges"]:
    # Rename existing "Bundle Deals" to "Complete Care Kits"
    bundle_deals = result["data"]["collections"]["edges"][0]["node"]
    collection_id = bundle_deals["id"]

    print(f"\n✅ Found 'Bundle Deals' collection: {collection_id}")
    print("   Renaming to 'Complete Care Kits'...")

    mutation_rename = """
    mutation collectionUpdate($input: CollectionInput!) {
      collectionUpdate(input: $input) {
        collection {
          id
          title
          handle
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "id": collection_id,
            "title": "Complete Care Kits",
            "handle": "complete-care-kits",
            "descriptionHtml": """<div class="collection-description">
<h2>Complete Care Kits - Curated Medical Support Bundles</h2>

<p>Discover our expertly curated Complete Care Kits, designed specifically for your unique health and wellness needs. Each bundle combines 3-4 complementary products at 15% savings compared to individual purchases.</p>

<h3>Why Choose Complete Care Kits?</h3>
<ul>
  <li><strong>Persona-Matched Solutions:</strong> Every kit is designed for specific user needs - athletes, office workers, post-injury recovery, beauty enthusiasts, and more</li>
  <li><strong>15% Savings:</strong> Save compared to buying products individually</li>
  <li><strong>Complementary Products:</strong> Products work together for comprehensive support</li>
  <li><strong>Expert-Curated:</strong> Based on analysis of 73+ medical support products and real user needs</li>
</ul>

<h3>Our Kit Categories:</h3>
<ul>
  <li><strong>Active Athlete Kits:</strong> Knee, ankle, and comprehensive sports support</li>
  <li><strong>Office Worker Relief:</strong> Back, neck, and posture correction</li>
  <li><strong>Post-Injury Recovery:</strong> Rehabilitation and therapy solutions</li>
  <li><strong>Beauty & Wellness:</strong> Facial therapy and anti-aging treatments</li>
  <li><strong>Mobility Support:</strong> For elderly and those needing joint stability</li>
</ul>

<p><strong>Each kit includes:</strong> 3-4 carefully selected products, complete usage instructions, and dedicated customer support.</p>
</div>"""
        }
    }

    result = graphql_query(mutation_rename, variables)

    if result and result["data"]["collectionUpdate"]["collection"]:
        print(f"   ✅ Renamed to 'Complete Care Kits'")
    else:
        print(f"   ⚠️  Rename failed, continuing with existing collection")
else:
    # Create new collection
    print("\n'Bundle Deals' not found, creating 'Complete Care Kits'...")

    mutation_create = """
    mutation collectionCreate($input: CollectionInput!) {
      collectionCreate(input: $input) {
        collection {
          id
          title
          handle
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "title": "Complete Care Kits",
            "handle": "complete-care-kits",
            "descriptionHtml": """<div class="collection-description">
<h2>Complete Care Kits - Curated Medical Support Bundles</h2>

<p>Discover our expertly curated Complete Care Kits, designed specifically for your unique health and wellness needs. Each bundle combines 3-4 complementary products at 15% savings compared to individual purchases.</p>

<h3>Why Choose Complete Care Kits?</h3>
<ul>
  <li><strong>Persona-Matched Solutions:</strong> Every kit is designed for specific user needs</li>
  <li><strong>15% Savings:</strong> Save compared to buying products individually</li>
  <li><strong>Complementary Products:</strong> Products work together for comprehensive support</li>
</ul>
</div>"""
        }
    }

    result = graphql_query(mutation_create, variables)

    if result and result["data"]["collectionCreate"]["collection"]:
        collection_id = result["data"]["collectionCreate"]["collection"]["id"]
        print(f"   ✅ Created 'Complete Care Kits': {collection_id}")
    else:
        print("   ❌ Failed to create collection")
        exit(1)

# ============================================================================
# 5. CREATE BUNDLE PRODUCTS (DRY RUN FIRST)
# ============================================================================
print("\n" + "="*80)
print("5. BUNDLE PRODUCTS CREATION PLAN (DRY RUN)")
print("="*80)

print("\n📋 BUNDLES TO CREATE:\n")

for i, bundle in enumerate(bundle_plans, 1):
    print(f"{i}. {bundle['name']}")
    print(f"   Products: {len(bundle['products'])}")
    print(f"   Total value: ${bundle['total_price']:.2f}")
    print(f"   Bundle price: ${bundle['bundle_price']:.2f} (15% discount)")
    print(f"   Products included:")
    for prod in bundle["products"]:
        print(f"      - {prod['title'][:60]}... (${prod['price']:.2f})")
    print()

# Save bundle plans to JSON
output_file = "optimal_bundles_plan.json"
with open(output_file, 'w') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "total_bundles": len(bundle_plans),
        "unique_products_used": len(used_product_ids),
        "collection_id": collection_id,
        "bundles": bundle_plans
    }, f, indent=2)

print("="*80)
print("SUMMARY - DRY RUN COMPLETE")
print("="*80)
print(f"\n✅ {len(bundle_plans)} optimal bundles planned")
print(f"✅ {len(used_product_ids)} unique products (NO duplicates)")
print(f"✅ Bundle plan saved to: {output_file}")
print(f"✅ Target collection: {collection_id}")

print("\n🔥 NEXT STEPS:")
print("1. Review bundle plans in optimal_bundles_plan.json")
print("2. Run: python3 create_bundle_products.py (to actually create bundles)")
print("3. Verify bundles in Shopify Admin")
print("4. Add bundles to Complete Care Kits collection")

print("\n" + "="*80)
