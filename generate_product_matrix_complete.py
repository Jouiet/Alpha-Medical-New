#!/usr/bin/env python3
"""
GENERATE PRODUCT MATRIX COMPLETE - All 96 products with 6-dimension scoring
Date: 2025-11-19
Purpose: Create complete product_matrix.json for dynamic merchandising
"""

import os
import requests
import json
from typing import Dict, List

# Load credentials from .env.admin directly
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

HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

def fetch_all_products() -> List[Dict]:
    """Fetch ALL products with pagination"""
    all_products = []
    url = f"https://{SHOP}/admin/api/{API_VERSION}/products.json?limit=250"

    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            break

        data = response.json()
        products = data.get("products", [])
        all_products.extend(products)

        # Check for next page
        link_header = response.headers.get("Link", "")
        if 'rel="next"' in link_header:
            next_url = link_header.split('>; rel="next"')[0].split('<')[1] if '<' in link_header else None
            url = next_url if next_url else None
        else:
            url = None

    return all_products

def score_seasonality(title: str, desc: str, product_type: str, tags: str) -> Dict[str, float]:
    """Score product relevance for each season (0-1)"""
    title_lower = title.lower()
    desc_lower = (desc or "").lower()
    type_lower = product_type.lower()
    tags_lower = tags.lower()

    text = f"{title_lower} {desc_lower} {type_lower} {tags_lower}"

    scores = {
        "winter": 0.5,  # Default baseline
        "spring": 0.5,
        "summer": 0.5,
        "fall": 0.5
    }

    # Winter boosters (cold weather, arthritis, heated therapy)
    winter_keywords = ["heated", "thermal", "heat", "arthritis", "magnetic", "tourmaline", "hot compress", "warming"]
    for kw in winter_keywords:
        if kw in text:
            scores["winter"] = min(scores["winter"] + 0.15, 1.0)

    # Summer boosters (sports, outdoor, lightweight, recovery)
    summer_keywords = ["sports", "athletic", "basketball", "running", "cycling", "outdoor", "lightweight", "compression"]
    for kw in summer_keywords:
        if kw in text:
            scores["summer"] = min(scores["summer"] + 0.15, 1.0)

    # Fall boosters (back-to-school, posture, desk work)
    fall_keywords = ["posture", "desk", "ergonomic", "office", "shoulder", "back support", "hunchback"]
    for kw in fall_keywords:
        if kw in text:
            scores["fall"] = min(scores["fall"] + 0.15, 1.0)

    # Spring boosters (recovery, rehabilitation, injury prevention)
    spring_keywords = ["recovery", "rehabilitation", "therapy", "injury", "physical therapy", "healing"]
    for kw in spring_keywords:
        if kw in text:
            scores["spring"] = min(scores["spring"] + 0.15, 1.0)

    return scores

def score_demographics(title: str, desc: str, product_type: str, tags: str, price: float) -> Dict[str, float]:
    """Score product relevance for each demographic (0-1)"""
    title_lower = title.lower()
    desc_lower = (desc or "").lower()
    type_lower = product_type.lower()
    tags_lower = tags.lower()

    text = f"{title_lower} {desc_lower} {type_lower} {tags_lower}"

    scores = {
        "office_workers_25_55": 0.2,
        "seniors_65plus": 0.2,
        "beauty_wellness_25_55": 0.2,
        "athletes_18_45": 0.2,
        "gamers_16_35": 0.2,
        "specialized_medical_rehabilitation": 0.2
    }

    # Office Workers 25-55 (28.2% of catalog - LARGEST)
    office_kw = ["posture", "desk", "office", "ergonomic", "tech neck", "cervical", "back", "lumbar", "shoulder", "hunchback", "scoliosis"]
    for kw in office_kw:
        if kw in text:
            scores["office_workers_25_55"] = min(scores["office_workers_25_55"] + 0.15, 1.0)

    # Seniors 65+ (26.9% of catalog)
    senior_kw = ["arthritis", "chronic pain", "magnetic", "heated", "tourmaline", "oa", "osteoarthritis", "joint pain", "mobility", "aging"]
    for kw in senior_kw:
        if kw in text:
            scores["seniors_65plus"] = min(scores["seniors_65plus"] + 0.15, 1.0)

    # Beauty/Wellness 25-55 (20.5% of catalog - non-orthopedic)
    beauty_kw = ["led", "face mask", "anti-aging", "wrinkle", "skin", "rejuvenation", "photon", "eye massager", "facial", "beauty", "cosmetic", "gua sha"]
    for kw in beauty_kw:
        if kw in text:
            scores["beauty_wellness_25_55"] = min(scores["beauty_wellness_25_55"] + 0.15, 1.0)

    # Athletes 18-45 (10.3% of catalog)
    athlete_kw = ["sports", "basketball", "running", "cycling", "athletic", "performance", "competition", "gym", "exercise", "training"]
    for kw in athlete_kw:
        if kw in text:
            scores["athletes_18_45"] = min(scores["athletes_18_45"] + 0.15, 1.0)

    # Gamers 16-35 (5.1% of catalog)
    gamer_kw = ["wrist", "carpal tunnel", "gaming", "hand", "typing", "mouse", "keyboard", "controller"]
    for kw in gamer_kw:
        if kw in text:
            scores["gamers_16_35"] = min(scores["gamers_16_35"] + 0.15, 1.0)

    # Specialized Medical (3.8% of catalog)
    medical_kw = ["stroke", "cerebral palsy", "rehabilitation robot", "mirror training", "o/x-type leg", "bow legs", "knock knees", "post-surgery", "medical-grade"]
    for kw in medical_kw:
        if kw in text:
            scores["specialized_medical_rehabilitation"] = min(scores["specialized_medical_rehabilitation"] + 0.15, 1.0)

    return scores

def score_pain_type(title: str, desc: str, product_type: str, tags: str) -> Dict[str, float]:
    """Score product relevance for pain types (0-1)"""
    title_lower = title.lower()
    desc_lower = (desc or "").lower()
    type_lower = product_type.lower()
    tags_lower = tags.lower()

    text = f"{title_lower} {desc_lower} {type_lower} {tags_lower}"

    scores = {
        "knee": 0.0,
        "back": 0.0,
        "neck": 0.0,
        "foot": 0.0,
        "wrist": 0.0,
        "shoulder": 0.0
    }

    # Knee
    if any(kw in text for kw in ["knee", "patella", "patellar", "meniscus", "acl"]):
        scores["knee"] = 1.0

    # Back
    if any(kw in text for kw in ["back", "lumbar", "spine", "disc", "herniation", "posture", "hunchback", "scoliosis"]):
        scores["back"] = 0.9 if "back" in text else 0.7

    # Neck
    if any(kw in text for kw in ["neck", "cervical", "collar", "traction"]):
        scores["neck"] = 1.0

    # Foot
    if any(kw in text for kw in ["foot", "ankle", "plantar", "bunion", "afo", "drop foot"]):
        scores["foot"] = 1.0

    # Wrist
    if any(kw in text for kw in ["wrist", "carpal tunnel", "hand", "finger"]):
        scores["wrist"] = 1.0

    # Shoulder
    if any(kw in text for kw in ["shoulder", "rotator cuff", "clavicle"]):
        scores["shoulder"] = 1.0

    return scores

def score_price_tier(price: float) -> Dict[str, float]:
    """Score product for price tiers (0-1)"""
    scores = {
        "budget": 0.0,
        "mid_range": 0.0,
        "premium": 0.0,
        "luxury": 0.0
    }

    if price < 30:
        scores["budget"] = 1.0
        scores["mid_range"] = 0.3
    elif 30 <= price < 80:
        scores["mid_range"] = 1.0
        scores["budget"] = 0.4
        scores["premium"] = 0.3
    elif 80 <= price < 200:
        scores["premium"] = 1.0
        scores["mid_range"] = 0.4
        scores["luxury"] = 0.3
    else:
        scores["luxury"] = 1.0
        scores["premium"] = 0.4

    return scores

def score_usage_intensity(title: str, desc: str, product_type: str, tags: str) -> Dict[str, float]:
    """Score usage intensity (0-1)"""
    title_lower = title.lower()
    desc_lower = (desc or "").lower()
    type_lower = product_type.lower()
    tags_lower = tags.lower()

    text = f"{title_lower} {desc_lower} {type_lower} {tags_lower}"

    scores = {
        "daily_wear": 0.3,
        "occasional": 0.3,
        "recovery": 0.3,
        "performance": 0.3
    }

    # Daily wear
    daily_kw = ["daily", "all day", "chronic", "prevention", "posture", "ergonomic"]
    for kw in daily_kw:
        if kw in text:
            scores["daily_wear"] = min(scores["daily_wear"] + 0.2, 1.0)

    # Occasional
    occasional_kw = ["as needed", "adjustable", "travel", "flare-up"]
    for kw in occasional_kw:
        if kw in text:
            scores["occasional"] = min(scores["occasional"] + 0.2, 1.0)

    # Recovery
    recovery_kw = ["recovery", "rehabilitation", "therapy", "post-op", "injury", "healing"]
    for kw in recovery_kw:
        if kw in text:
            scores["recovery"] = min(scores["recovery"] + 0.2, 1.0)

    # Performance
    performance_kw = ["sports", "athletic", "exercise", "competition", "training", "performance"]
    for kw in performance_kw:
        if kw in text:
            scores["performance"] = min(scores["performance"] + 0.2, 1.0)

    return scores

def score_medical_condition(title: str, desc: str, product_type: str, tags: str) -> Dict[str, float]:
    """Score medical conditions (0-1)"""
    title_lower = title.lower()
    desc_lower = (desc or "").lower()
    type_lower = product_type.lower()
    tags_lower = tags.lower()

    text = f"{title_lower} {desc_lower} {type_lower} {tags_lower}"

    scores = {
        "arthritis": 0.1,
        "post_surgery": 0.1,
        "prevention": 0.1,
        "chronic_pain": 0.1,
        "injury_recovery": 0.1
    }

    # Arthritis
    arthritis_kw = ["arthritis", "oa", "osteoarthritis", "ra", "rheumatoid", "joint pain"]
    for kw in arthritis_kw:
        if kw in text:
            scores["arthritis"] = min(scores["arthritis"] + 0.3, 1.0)

    # Post-surgery
    surgery_kw = ["post-op", "post surgery", "surgical", "recovery", "rehabilitation"]
    for kw in surgery_kw:
        if kw in text:
            scores["post_surgery"] = min(scores["post_surgery"] + 0.3, 1.0)

    # Prevention
    prevention_kw = ["prevention", "preventive", "posture", "ergonomic", "support", "protective"]
    for kw in prevention_kw:
        if kw in text:
            scores["prevention"] = min(scores["prevention"] + 0.25, 1.0)

    # Chronic pain
    chronic_kw = ["chronic", "persistent", "long-term", "daily pain", "fibromyalgia"]
    for kw in chronic_kw:
        if kw in text:
            scores["chronic_pain"] = min(scores["chronic_pain"] + 0.3, 1.0)

    # Injury recovery
    injury_kw = ["injury", "sprain", "strain", "fracture", "tear", "trauma"]
    for kw in injury_kw:
        if kw in text:
            scores["injury_recovery"] = min(scores["injury_recovery"] + 0.3, 1.0)

    return scores

def generate_product_matrix(products: List[Dict]) -> Dict:
    """Generate complete product matrix with all products scored"""
    matrix = {}

    for product in products:
        handle = product.get("handle")
        title = product.get("title", "")
        desc = product.get("body_html", "") or ""
        product_type = product.get("product_type", "")
        tags = product.get("tags", "")

        # Get price from first variant
        variants = product.get("variants", [])
        price = float(variants[0].get("price", 0)) if variants else 0.0

        # Score all dimensions
        matrix[handle] = {
            "name": title,
            "scores": {
                "seasonality": score_seasonality(title, desc, product_type, tags),
                "demographics": score_demographics(title, desc, product_type, tags, price),
                "pain_type": score_pain_type(title, desc, product_type, tags),
                "price_tier": score_price_tier(price),
                "usage_intensity": score_usage_intensity(title, desc, product_type, tags),
                "medical_condition": score_medical_condition(title, desc, product_type, tags)
            }
        }

    return matrix

def main():
    print("=" * 80)
    print("GENERATE PRODUCT MATRIX COMPLETE - All Products with 6D Scoring")
    print("=" * 80)
    print(f"Store: {SHOP}")
    print(f"API Version: {API_VERSION}\n")

    # Fetch products
    print("📥 Fetching ALL products...")
    products = fetch_all_products()
    print(f"✅ Fetched {len(products)} products\n")

    if len(products) == 0:
        print("❌ ERROR: 0 products fetched!")
        return

    # Load base matrix template
    print("📖 Loading base matrix template...")
    with open("segmentation_matrix_alpha_medical.json", "r") as f:
        base_matrix = json.load(f)

    # Generate product scores
    print("🔢 Scoring all products across 6 dimensions...")
    product_matrix = generate_product_matrix(products)
    print(f"✅ Scored {len(product_matrix)} products\n")

    # Create complete matrix
    complete_matrix = {
        "_metadata": {
            "version": "2.1",
            "date": "2025-11-19",
            "last_update": "2025-11-19 - Complete product matrix generation",
            "purpose": "Multi-dimensional product segmentation for dynamic merchandising",
            "methodology": "Based on ACTUAL Alpha Medical inventory analysis (96 products)",
            "product_count": len(products),
            "last_generated": "2025-11-19",
            "status": "COMPLETE - All products scored"
        },
        "market_facts_2025": base_matrix["market_facts_2025"],
        "dimensions": base_matrix["dimensions"],
        "product_matrix": product_matrix,
        "contexts_examples": base_matrix["contexts_examples"]
    }

    # Save complete matrix
    output_file = "product_matrix_complete.json"
    with open(output_file, "w") as f:
        json.dump(complete_matrix, f, indent=2)

    print(f"✅ Complete product matrix saved to: {output_file}")
    print(f"📊 Total products: {len(products)}")
    print(f"📊 Products scored: {len(product_matrix)}")
    print(f"✅ SUCCESS: Product matrix generation complete!\n")

    # Sample output (first 3 products)
    print("=" * 80)
    print("SAMPLE OUTPUT (First 3 Products)")
    print("=" * 80)
    sample_handles = list(product_matrix.keys())[:3]
    for handle in sample_handles:
        product = product_matrix[handle]
        print(f"\n{handle}:")
        print(f"  Name: {product['name']}")
        print(f"  Seasonality: Winter={product['scores']['seasonality']['winter']:.2f}, Summer={product['scores']['seasonality']['summer']:.2f}")
        print(f"  Demographics: Office={product['scores']['demographics']['office_workers_25_55']:.2f}, Seniors={product['scores']['demographics']['seniors_65plus']:.2f}")
        print(f"  Pain Type: {max(product['scores']['pain_type'], key=product['scores']['pain_type'].get)}")

if __name__ == "__main__":
    main()
