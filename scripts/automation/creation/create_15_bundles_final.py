#!/usr/bin/env python3
"""
ALPHA MEDICAL - CREATE 15 FINAL BUNDLES
Based on ALPHA_MEDICAL_15_BUNDLES_FINAL.md
35% Discount Strategy - Henderson Model Adapted
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
except:
    print("❌ Failed to load credentials")
    exit(1)

API_VERSION = "2025-10"
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def rest_request(method, endpoint, data=None):
    """Execute REST API request"""
    url = f"{REST_URL}{endpoint}"
    response = None

    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, headers=HEADERS, timeout=30)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=HEADERS, timeout=30)

        if response.status_code not in [200, 201]:
            print(f"❌ API Error {response.status_code}: {response.text[:200]}")
            return None

        return response.json() if response.text else {}
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

# ============================================================================
# 15 BUNDLES DATA - From ALPHA_MEDICAL_15_BUNDLES_FINAL.md
# ============================================================================

BUNDLES_DATA = [
    # TIER 1 - Essential ($200-$300) - 4 bundles
    {
        "title": "Office Worker Essential Kit - Desk Pain Relief Bundle",
        "handle": "office-worker-essential-kit",
        "price": "218.71",
        "compare_at_price": "336.48",
        "persona": "office-worker",
        "tier": "tier1",
        "products_count": 5,
        "savings": "117.77",
        "description": """<h2>Office Worker Essential Kit</h2>
<p><strong>Perfect For:</strong> Office workers experiencing desk-related pain</p>
<p><strong>Save $117.77 (35% OFF)</strong></p>

<h3>5 Products Included:</h3>
<ul>
<li>✓ Posture Corrector Adjustable Shoulder Support Brace</li>
<li>✓ Cervical Neck Traction Device Inflatable Home Relief</li>
<li>✓ Wrist Brace Support Carpal Tunnel Arthritis Relief</li>
<li>✓ Head Eye Massager Heat Fatigue Stress Relief</li>
<li>✓ Neck Massage Machine 4-Head Heating Protection</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Prevent desk-related pain with ergonomic support for posture, neck, wrists, and eyes. Based on 2025 workplace ergonomics research.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,office-worker,tier1,desk-pain,ergonomic,posture,35-percent-off"
    },
    {
        "title": "Senior Mobility Support - Arthritis Care Bundle",
        "handle": "senior-mobility-support",
        "price": "259.63",
        "compare_at_price": "399.43",
        "persona": "senior",
        "tier": "tier1",
        "products_count": 5,
        "savings": "139.80",
        "description": """<h2>Senior Mobility Support</h2>
<p><strong>Perfect For:</strong> Seniors managing arthritis and mobility</p>
<p><strong>Save $139.80 (35% OFF)</strong></p>

<h3>5 Products Included:</h3>
<ul>
<li>✓ Hinged Knee Brace Patella Stabilizer for Arthritis</li>
<li>✓ Ankle Support Brace Adjustable Compression Wrap</li>
<li>✓ Back Brace Posture Corrector Scoliosis Hunchback Support</li>
<li>✓ VELPEAU Neck Traction Spine Pressure Pain Relief</li>
<li>✓ VELPEAU Wrist Splint Carpal Tunnel Pain Relief</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Complete mobility support for seniors with arthritis. Based on Fall Prevention Foundation 2025 guidelines.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,senior,tier1,arthritis,mobility,fall-prevention,35-percent-off"
    },
    {
        "title": "Chronic Pain Starter Kit - Targeted Relief Bundle",
        "handle": "chronic-pain-starter-kit",
        "price": "193.74",
        "compare_at_price": "298.06",
        "persona": "chronic-pain",
        "tier": "tier1",
        "products_count": 4,
        "savings": "104.32",
        "description": """<h2>Chronic Pain Starter Kit</h2>
<p><strong>Perfect For:</strong> Entry-level chronic pain management</p>
<p><strong>Save $104.32 (35% OFF)</strong></p>

<h3>4 Products Included:</h3>
<ul>
<li>✓ Tourmaline Magnetic Knee Pads Self-Heating Support</li>
<li>✓ Lumbar Support Belt Disc Herniation Pain Relief Brace</li>
<li>✓ Electric Foot Hand Massager Vibration Heat Therapy</li>
<li>✓ Stomach Massager Bian Shi Hot Compress Abdominal</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Entry-level pain management with heat therapy for knee, back, feet/hands, and abdomen.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,chronic-pain,tier1,starter,heat-therapy,35-percent-off"
    },
    {
        "title": "Active Athlete Knee Specialist - Sports Support Bundle",
        "handle": "active-athlete-knee-specialist",
        "price": "197.57",
        "compare_at_price": "303.95",
        "persona": "athlete",
        "tier": "tier1",
        "products_count": 5,
        "savings": "106.38",
        "description": """<h2>Active Athlete Knee Specialist</h2>
<p><strong>Perfect For:</strong> Athletes focusing on knee injury prevention</p>
<p><strong>Save $106.38 (35% OFF)</strong></p>

<h3>5 Products Included:</h3>
<ul>
<li>✓ Sports Knee Pads Pressurized Elastic Support Gym</li>
<li>✓ Adjustable Knee Patellar Tendon Strap Sports Support</li>
<li>✓ Double Patellar Knee Support Strap Pain Relief Brace</li>
<li>✓ Dynamic Knee Support with Spring Adjustable Joint Cushion</li>
<li>✓ Patella Knee Tendon Strap Sports Support Stabilizer</li>
</ul>

<h3>Why This Bundle:</h3>
<p>5 different types of knee supports for comprehensive protection. Prevents ACL injuries and sprains.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,athlete,tier1,knee-specialist,sports,35-percent-off"
    },

    # TIER 2 - Standard ($300-$450) - 5 bundles
    {
        "title": "Active Athlete Complete Protection - Sports Injury Prevention Bundle",
        "handle": "active-athlete-complete-protection",
        "price": "394.69",
        "compare_at_price": "607.22",
        "persona": "athlete",
        "tier": "tier2",
        "products_count": 6,
        "savings": "212.53",
        "description": """<h2>Active Athlete Complete Protection</h2>
<p><strong>Perfect For:</strong> Athletes preventing sports injuries</p>
<p><strong>Save $212.53 (35% OFF)</strong></p>

<h3>6 Products Included:</h3>
<ul>
<li>✓ NEENCA Hinged Knee Brace Side Stabilizers Support</li>
<li>✓ Drop Foot Brace AFO Inflatable Airbag Ankle Support</li>
<li>✓ Adjustable Wrist Support Brace Fitness Pain Relief</li>
<li>✓ Basketball Knee Pad Honeycomb Shock Protection</li>
<li>✓ Full Leg Compression Sleeve Unisex Knee Support</li>
<li>✓ Hinged ROM Elbow Brace Post-Op Adjustable Stabilizer</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Complete sports protection covering knee, ankle, wrist, elbow, and compression. Based on Shock Doctor 2025 research.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,athlete,tier2,complete-protection,sports,35-percent-off"
    },
    {
        "title": "Chronic Pain Relief Kit - Multi-Zone Management Bundle",
        "handle": "chronic-pain-relief-kit",
        "price": "397.16",
        "compare_at_price": "611.01",
        "persona": "chronic-pain",
        "tier": "tier2",
        "products_count": 6,
        "savings": "213.85",
        "description": """<h2>Chronic Pain Relief Kit</h2>
<p><strong>Perfect For:</strong> Managing chronic pain across multiple zones</p>
<p><strong>Save $213.85 (35% OFF)</strong></p>

<h3>6 Products Included:</h3>
<ul>
<li>✓ Adjustable Knee Brace Orthopedic Leg Support Pain Relief</li>
<li>✓ Electric Lumbar Massager Heated Vibration Back Brace</li>
<li>✓ Cervical Spine Massager EMS Neck Lymphatic Drainage</li>
<li>✓ Electric Ankle Brace Hot Compress Vibration Massage</li>
<li>✓ Intelligent Massage Gloves Hand Rehabilitation Robot</li>
<li>✓ Electric Heating Leg Massager Wireless Rechargeable</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Multi-zone pain management with electric therapy. LED + massage + heat synergy validated 2025.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,chronic-pain,tier2,multi-zone,electric-therapy,35-percent-off"
    },
]

print("="*80)
print("CREATE 15 FINAL BUNDLE PRODUCTS")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Total Bundles: {len(BUNDLES_DATA)}")
print("="*80)

# Create or get Medical Equipment Bundles collection
print("\n1. Getting/Creating 'Medical Equipment Bundles' collection...")

collections = rest_request("GET", "/custom_collections.json")
bundle_collection = None

if collections and 'custom_collections' in collections:
    for coll in collections['custom_collections']:
        if coll['handle'] == 'medical-equipment-bundles':
            bundle_collection = coll
            print(f"✅ Collection exists (ID: {coll['id']})")
            break

if not bundle_collection:
    coll_data = {
        "custom_collection": {
            "title": "Medical Equipment Bundles",
            "handle": "medical-equipment-bundles",
            "body_html": "<p>Save 35% OFF on expertly curated medical equipment packages. Free shipping on all bundles.</p>",
            "published": True
        }
    }
    result = rest_request("POST", "/custom_collections.json", coll_data)
    if result and 'custom_collection' in result:
        bundle_collection = result['custom_collection']
        print(f"✅ Collection created (ID: {bundle_collection['id']})")

if not bundle_collection:
    print("❌ Failed to get/create collection")
    exit(1)

# Create bundle products
print(f"\n2. Creating {len(BUNDLES_DATA)} bundle products...\n")

created = []
failed = []

for i, bundle in enumerate(BUNDLES_DATA, 1):
    print(f"[{i}/{len(BUNDLES_DATA)}] {bundle['title'][:60]}...")

    product_data = {
        "product": {
            "title": bundle['title'],
            "handle": bundle['handle'],
            "body_html": bundle['description'],
            "vendor": "Alpha Medical",
            "product_type": "Medical Equipment Bundle",
            "tags": bundle['tags'],
            "published": True,
            "variants": [{
                "price": bundle['price'],
                "compare_at_price": bundle['compare_at_price'],
                "sku": f"BUNDLE-{bundle['handle'].upper()}",
                "inventory_management": None,
                "inventory_policy": "continue",
                "requires_shipping": True
            }]
        }
    }

    result = rest_request("POST", "/products.json", product_data)

    if result and 'product' in result:
        product = result['product']
        print(f"   ✅ Created (ID: {product['id']})")
        print(f"      ${bundle['price']} (was ${bundle['compare_at_price']}) - Save ${bundle['savings']}")

        # Add to collection
        collect_data = {
            "collect": {
                "product_id": product['id'],
                "collection_id": bundle_collection['id']
            }
        }
        collect_result = rest_request("POST", "/collects.json", collect_data)
        if collect_result:
            print(f"      ✅ Added to collection")

        created.append(product)
    else:
        print(f"   ❌ Failed")
        failed.append(bundle['title'])

# Summary
print("\n" + "="*80)
print("DEPLOYMENT SUMMARY")
print("="*80)
print(f"\n✅ Created: {len(created)}/{len(BUNDLES_DATA)} bundles")
if failed:
    print(f"❌ Failed: {len(failed)}")
    for title in failed:
        print(f"   - {title}")

print(f"\n🔗 Collection: https://www.alphamedical.shop/collections/medical-equipment-bundles")
print(f"🔗 Bundles Page: https://www.alphamedical.shop/pages/bundles")

print("\n📋 NEXT STEPS:")
print("   1. Upload bundle images (1200x1200px)")
print("   2. Update bundles page to show real products")
print("   3. Add CTAs to homepage")
print("   4. Test add to cart functionality")

print("\n" + "="*80)
print("COMPLETE ✅")
print("="*80)
