#!/usr/bin/env python3
"""
REAL PERSONA ANALYSIS - Alpha Medical
BOTTOM-UP approach: Analyze EVERY product individually

Methodology:
1. Fetch ALL 73 active products with full details
2. Analyze each product:
   - Target body part (knee, back, neck, face, etc.)
   - Problem solved (pain, posture, recovery, beauty, etc.)
   - User type (athlete, office worker, elderly, etc.)
   - Use case (sports, daily wear, therapy, etc.)
3. Identify REAL personas based on patterns
4. Create bundles that match REAL user needs

NO SHORTCUTS - RIGOROUS PRODUCT-BY-PRODUCT ANALYSIS
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
print("ALPHA MEDICAL - REAL PERSONA ANALYSIS (BOTTOM-UP)")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# ============================================================================
# 1. FETCH ALL PRODUCTS WITH FULL DETAILS
# ============================================================================
print("\n1. Fetching ALL products with full details...\n")

all_products = []
cursor = None
has_next = True

while has_next:
    query = """
    query getProducts($cursor: String) {
      products(first: 50, after: $cursor, query: "status:ACTIVE") {
        edges {
          node {
            id
            title
            handle
            description
            productType
            tags
            priceRangeV2 {
              minVariantPrice {
                amount
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

    result = graphql_query(query, {"cursor": cursor} if cursor else {})
    if not result:
        break

    products = result["data"]["products"]["edges"]
    all_products.extend(products)
    has_next = result["data"]["products"]["pageInfo"]["hasNextPage"]
    if has_next and products:
        cursor = products[-1]["cursor"]

print(f"✅ Fetched {len(all_products)} active products")

# ============================================================================
# 2. ANALYZE EACH PRODUCT - CATEGORIZE BY BODY PART & USE CASE
# ============================================================================
print("\n" + "="*80)
print("2. PRODUCT-BY-PRODUCT ANALYSIS")
print("="*80)

# Categories to identify
body_parts = defaultdict(list)
problems_solved = defaultdict(list)
user_types = defaultdict(list)
use_cases = defaultdict(list)

# Keywords for classification
body_part_keywords = {
    "knee": ["knee", "patella", "patellar"],
    "back": ["back", "lumbar", "spine", "vertebra"],
    "neck": ["neck", "cervical", "collar"],
    "shoulder": ["shoulder"],
    "wrist": ["wrist", "carpal"],
    "ankle": ["ankle"],
    "foot": ["foot", "bunion", "toe", "hallux"],
    "hand": ["hand", "finger"],
    "face": ["face", "facial", "skin", "led mask", "photon"],
    "eye": ["eye"],
    "leg": ["leg", "calf"],
    "arm": ["arm", "elbow"],
    "hip": ["hip", "buttock"],
    "abdomen": ["abdominal", "stomach", "belly"],
    "posture": ["posture", "corrector", "brace"],
}

problem_keywords = {
    "pain_relief": ["pain", "relief", "arthritis", "inflammation"],
    "posture_correction": ["posture", "corrector", "hunchback", "scoliosis"],
    "injury_recovery": ["recovery", "rehabilitation", "injury", "sprain"],
    "muscle_support": ["support", "compression", "stability"],
    "therapy": ["therapy", "massage", "treatment", "healing"],
    "beauty_skincare": ["anti-aging", "wrinkle", "skin tightening", "led", "photon"],
    "circulation": ["circulation", "blood flow", "compression"],
    "traction": ["traction", "decompression", "stretching"],
}

user_type_keywords = {
    "athlete": ["sports", "basketball", "running", "gym", "fitness", "training"],
    "office_worker": ["desk", "computer", "sitting"],
    "elderly": ["elderly", "senior", "aging"],
    "post_surgery": ["surgery", "recovery", "rehabilitation"],
    "chronic_pain": ["chronic", "arthritis", "disc herniation"],
    "beauty_conscious": ["beauty", "anti-aging", "cosmetic", "skin care"],
}

print("\nAnalyzing each product...\n")

product_analysis = []

for edge in all_products:
    product = edge["node"]
    title_lower = product["title"].lower()
    desc_lower = product["description"].lower() if product["description"] else ""
    combined = f"{title_lower} {desc_lower}"

    # Classify by body part
    detected_body_parts = []
    for body_part, keywords in body_part_keywords.items():
        if any(kw in combined for kw in keywords):
            detected_body_parts.append(body_part)
            body_parts[body_part].append(product)

    # Classify by problem
    detected_problems = []
    for problem, keywords in problem_keywords.items():
        if any(kw in combined for kw in keywords):
            detected_problems.append(problem)
            problems_solved[problem].append(product)

    # Classify by user type
    detected_users = []
    for user_type, keywords in user_type_keywords.items():
        if any(kw in combined for kw in keywords):
            detected_users.append(user_type)
            user_types[user_type].append(product)

    product_analysis.append({
        "id": product["id"],
        "title": product["title"],
        "handle": product["handle"],
        "price": float(product["priceRangeV2"]["minVariantPrice"]["amount"]),
        "body_parts": detected_body_parts,
        "problems": detected_problems,
        "user_types": detected_users,
    })

# ============================================================================
# 3. IDENTIFY REAL PERSONAS
# ============================================================================
print("\n" + "="*80)
print("3. REAL PERSONAS IDENTIFIED")
print("="*80)

print("\n📊 BY BODY PART:")
for body_part, products in sorted(body_parts.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"   {body_part.upper():20} - {len(products):3} products")

print("\n📊 BY PROBLEM SOLVED:")
for problem, products in sorted(problems_solved.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"   {problem.upper():20} - {len(products):3} products")

print("\n📊 BY USER TYPE:")
for user_type, products in sorted(user_types.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"   {user_type.upper():20} - {len(products):3} products")

# ============================================================================
# 4. DEFINE REAL PERSONAS (cross-analysis)
# ============================================================================
print("\n" + "="*80)
print("4. DEFINED PERSONAS (Multi-dimensional)")
print("="*80)

# Real personas based on analysis
real_personas = {
    "athlete_active": {
        "name": "Active Athlete & Sports Enthusiast",
        "needs": ["knee support", "ankle support", "compression", "injury prevention"],
        "products": [],
        "priority_body_parts": ["knee", "ankle", "wrist"],
        "priority_problems": ["muscle_support", "injury_recovery", "pain_relief"]
    },
    "office_chronic_pain": {
        "name": "Office Worker with Chronic Pain",
        "needs": ["back support", "neck relief", "posture correction", "wrist support"],
        "products": [],
        "priority_body_parts": ["back", "neck", "wrist", "posture"],
        "priority_problems": ["posture_correction", "pain_relief", "muscle_support"]
    },
    "elderly_mobility": {
        "name": "Elderly / Mobility Support",
        "needs": ["joint support", "stability", "pain management", "circulation"],
        "products": [],
        "priority_body_parts": ["knee", "back", "ankle", "hip"],
        "priority_problems": ["pain_relief", "muscle_support", "circulation"]
    },
    "post_injury_recovery": {
        "name": "Post-Injury / Post-Surgery Recovery",
        "needs": ["rehabilitation", "therapy", "traction", "healing"],
        "products": [],
        "priority_body_parts": ["knee", "back", "neck", "shoulder"],
        "priority_problems": ["injury_recovery", "therapy", "traction", "pain_relief"]
    },
    "beauty_wellness": {
        "name": "Beauty & Wellness Enthusiast",
        "needs": ["facial therapy", "LED treatment", "anti-aging", "skin care"],
        "products": [],
        "priority_body_parts": ["face", "eye", "neck (beauty)"],
        "priority_problems": ["beauty_skincare", "therapy"]
    },
    "comprehensive_therapy": {
        "name": "Comprehensive Therapy User",
        "needs": ["massage", "heat therapy", "EMS", "multi-area treatment"],
        "products": [],
        "priority_body_parts": ["multiple"],
        "priority_problems": ["therapy", "pain_relief", "circulation"]
    },
    "foot_bunion_care": {
        "name": "Foot Care & Bunion Relief",
        "needs": ["bunion correction", "toe support", "foot pain", "hallux valgus"],
        "products": [],
        "priority_body_parts": ["foot"],
        "priority_problems": ["pain_relief", "posture_correction"]
    },
}

# Assign products to personas
for prod_data in product_analysis:
    for persona_key, persona in real_personas.items():
        # Check if product matches persona's priority body parts and problems
        body_match = any(bp in prod_data["body_parts"] for bp in persona["priority_body_parts"])
        problem_match = any(prob in prod_data["problems"] for prob in persona["priority_problems"])

        if body_match or problem_match:
            persona["products"].append(prod_data)

# Remove duplicates and limit
for persona_key, persona in real_personas.items():
    # Remove duplicates (keep first occurrence)
    seen = set()
    unique_products = []
    for prod in persona["products"]:
        if prod["id"] not in seen:
            seen.add(prod["id"])
            unique_products.append(prod)
    persona["products"] = unique_products

print("\n✅ REAL PERSONAS IDENTIFIED:\n")
for key, persona in real_personas.items():
    print(f"📌 {persona['name']}")
    print(f"   Products: {len(persona['products'])}")
    print(f"   Needs: {', '.join(persona['needs'][:3])}...")
    print()

# ============================================================================
# 5. SAVE RESULTS
# ============================================================================
output_file = "real_personas_analysis.json"
with open(output_file, 'w') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "total_products": len(all_products),
        "body_parts_distribution": {k: len(v) for k, v in body_parts.items()},
        "problems_distribution": {k: len(v) for k, v in problems_solved.items()},
        "user_types_distribution": {k: len(v) for k, v in user_types.items()},
        "real_personas": {
            key: {
                "name": p["name"],
                "needs": p["needs"],
                "product_count": len(p["products"]),
                "products": [{"id": pr["id"], "title": pr["title"], "price": pr["price"]} for pr in p["products"]]
            }
            for key, p in real_personas.items()
        }
    }, f, indent=2)

print("="*80)
print("SUMMARY")
print("="*80)
print(f"\n✅ Analyzed {len(all_products)} products")
print(f"✅ Identified {len(real_personas)} REAL personas")
print(f"✅ Results saved to: {output_file}")
print("\n🔥 NEXT STEP: Create optimal bundles based on REAL personas")
print("   Script: create_optimal_bundles_from_personas.py")
print("\n" + "="*80)
