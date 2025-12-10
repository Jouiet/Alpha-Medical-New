#!/usr/bin/env python3
"""
ALPHA MEDICAL - CREATE REMAINING 9 BUNDLES (5-8, 10, 12-15)
Completes the 15 bundles system based on ALPHA_MEDICAL_15_BUNDLES_FINAL.md
35% Discount Strategy - Henderson Model
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
# REMAINING 9 BUNDLES DATA (Bundles 5-8, 10, 12-15)
# From ALPHA_MEDICAL_15_BUNDLES_FINAL.md
# ============================================================================

REMAINING_BUNDLES = [
    # BUNDLE 5: Post-Surgery Recovery Complete (TIER 3)
    {
        "title": "Post-Surgery Recovery Complete - Orthopedic Support Bundle",
        "handle": "post-surgery-recovery-complete",
        "price": "520.82",
        "compare_at_price": "801.26",
        "persona": "post-surgery",
        "tier": "tier3",
        "products_count": 7,
        "savings": "280.44",
        "description": """<h2>Post-Surgery Recovery Complete</h2>
<p><strong>Perfect For:</strong> Post-surgery patients requiring comprehensive orthopedic support</p>
<p><strong>Save $280.44 (35% OFF)</strong></p>

<h3>7 Products Included:</h3>
<ul>
<li>✓ Adjustable Cervical Collar Neck Brace Orthosis</li>
<li>✓ AFO Drop Foot Brace Ankle Foot Orthosis</li>
<li>✓ Lower Back Brace 6 Stays Anti-Skid Lumbar Support</li>
<li>✓ Hip Fixation Brace Femoral Thigh Fracture Support</li>
<li>✓ O/X-Type Leg Corrector Adjustable Leg Straightener</li>
<li>✓ Neck Traction Device Heating Inflatable Cervical</li>
<li>✓ Electric Foot Hand Massager Vibration Heat Therapy</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Complete post-operative support covering neck, ankle, back, hip, legs, and therapeutic massage. Based on Cardinal Health 2025 customizable care packs.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,post-surgery,tier3,recovery,orthopedic,comprehensive,35-percent-off"
    },

    # BUNDLE 6: Ultimate Pain Management (TIER 4)
    {
        "title": "Ultimate Pain Management System - Advanced Therapy Bundle",
        "handle": "ultimate-pain-management-system",
        "price": "673.56",
        "compare_at_price": "1036.24",
        "persona": "chronic-pain",
        "tier": "tier4",
        "products_count": 8,
        "savings": "362.68",
        "description": """<h2>Ultimate Pain Management System</h2>
<p><strong>Perfect For:</strong> Advanced chronic pain sufferers needing comprehensive relief</p>
<p><strong>Save $362.68 (35% OFF)</strong></p>

<h3>8 Products Included:</h3>
<ul>
<li>✓ Adjustable Knee Brace Orthopedic Leg Support Pain Relief</li>
<li>✓ Electric Lumbar Massager Heated Vibration Back Brace</li>
<li>✓ Hello Face Red Light Therapy Mask Face Neck Infrared LED</li>
<li>✓ Foreverlily Smart Knee Massager Vibration Air Pressure</li>
<li>✓ Electric Medical Cupping Therapy Set</li>
<li>✓ Nano Steam Eye Massager Warm Spa Acupressure Mask</li>
<li>✓ Vibration Shoulder Steamer Heated Belt Massager</li>
<li>✓ Cervical Spine Massager EMS Neck Lymphatic Drainage</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Complete pain management system combining structural support with 7 advanced massage devices. LED + massage + heat synergy validated 2025.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,chronic-pain,tier4,ultimate,advanced-therapy,massage,35-percent-off"
    },

    # BUNDLE 7: Office Worker Advanced Ergonomic (TIER 2)
    {
        "title": "Office Worker Advanced Ergonomic - LED Therapy Bundle",
        "handle": "office-worker-advanced-ergonomic",
        "price": "318.44",
        "compare_at_price": "489.91",
        "persona": "office-worker",
        "tier": "tier2",
        "products_count": 6,
        "savings": "171.47",
        "description": """<h2>Office Worker Advanced Ergonomic</h2>
<p><strong>Perfect For:</strong> Office workers seeking advanced ergonomic support with LED therapy</p>
<p><strong>Save $171.47 (35% OFF)</strong></p>

<h3>6 Products Included:</h3>
<ul>
<li>✓ Magnetic Posture Corrector Shoulder Orthopedic Brace</li>
<li>✓ 7 Color LED Vibrating Neck Face Massager</li>
<li>✓ Adjustable Cervical Collar Spine Thoracic Orthosis</li>
<li>✓ EMS Red Light Eye Massager Dark Circles Wrinkle Reduction</li>
<li>✓ Electric Gua Sha Board Vibration Hot Compress Massage</li>
<li>✓ Kids Posture Corrector Adjustable Back Support</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Advanced ergonomics with LED therapy for posture, neck, and eye strain relief. Based on Upright Go 2025 workplace wellness research.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,office-worker,tier2,advanced,ergonomic,led-therapy,35-percent-off"
    },

    # BUNDLE 8: Office Worker Premium Workspace (TIER 3)
    {
        "title": "Office Worker Premium Workspace - Eye Fatigue Relief Bundle",
        "handle": "office-worker-premium-workspace",
        "price": "451.43",
        "compare_at_price": "694.50",
        "persona": "office-worker",
        "tier": "tier3",
        "products_count": 6,
        "savings": "243.07",
        "description": """<h2>Office Worker Premium Workspace</h2>
<p><strong>Perfect For:</strong> Office workers with severe eye strain and screen fatigue</p>
<p><strong>Save $243.07 (35% OFF)</strong></p>

<h3>6 Products Included:</h3>
<ul>
<li>✓ LED Facial Mask with Neck 7 Colors Photon Anti-Aging</li>
<li>✓ Neck LED Lift Mask Anti-Wrinkle Skin Tightening</li>
<li>✓ Electric Airbag Eye Massager Heated Hot Compress</li>
<li>✓ Super Relax Eye Massager Heating Vibration Sleep Aid</li>
<li>✓ EMS Hip Trainer 3 Modes Buttock Lifting Massage</li>
<li>✓ Smart Electric Vacuum Cupping Device</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Premium workspace health with LED therapy and advanced eye massagers for screen fatigue relief. Ergonomic 2025 standards.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,office-worker,tier3,premium,eye-fatigue,screen-relief,35-percent-off"
    },

    # BUNDLE 10: Chronic Pain Whole-Body (TIER 3)
    {
        "title": "Chronic Pain Whole-Body - LED Therapy Complete Bundle",
        "handle": "chronic-pain-whole-body",
        "price": "488.64",
        "compare_at_price": "751.75",
        "persona": "chronic-pain",
        "tier": "tier3",
        "products_count": 6,
        "savings": "263.11",
        "description": """<h2>Chronic Pain Whole-Body</h2>
<p><strong>Perfect For:</strong> Whole-body chronic pain management with LED therapy</p>
<p><strong>Save $263.11 (35% OFF)</strong></p>

<h3>6 Products Included:</h3>
<ul>
<li>✓ Hello Face Red Light Therapy Mask Face Neck Infrared LED</li>
<li>✓ Foreverlily Smart Knee Massager Vibration Air Pressure</li>
<li>✓ Electric Medical Cupping Therapy Set</li>
<li>✓ Nano Steam Eye Massager Warm Spa Acupressure Mask</li>
<li>✓ Vibration Shoulder Steamer Heated Belt Massager</li>
<li>✓ 4-in-1 Cavitation Body Slimming Machine 40K Ultrasound</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Whole-body therapy combining LED, massage, cupping, and cavitation. Therapeutic synergies validated 2025.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,chronic-pain,tier3,whole-body,led-therapy,massage,35-percent-off"
    },

    # BUNDLE 12: Manual Labor Heavy-Duty (TIER 4)
    {
        "title": "Manual Labor Heavy-Duty - Industrial Protection Bundle",
        "handle": "manual-labor-heavy-duty",
        "price": "602.85",
        "compare_at_price": "927.46",
        "persona": "manual-labor",
        "tier": "tier4",
        "products_count": 7,
        "savings": "324.61",
        "description": """<h2>Manual Labor Heavy-Duty</h2>
<p><strong>Perfect For:</strong> Manual workers requiring heavy-duty protection</p>
<p><strong>Save $324.61 (35% OFF)</strong></p>

<h3>7 Products Included:</h3>
<ul>
<li>✓ Posture Corrector Adjustable Back Brace for Women Men</li>
<li>✓ Hip Fixation Brace Femoral Thigh Fracture Support</li>
<li>✓ O/X-Type Leg Corrector Adjustable Leg Straightener</li>
<li>✓ Silicone Patellar Tendon Strap Knee Pain Relief</li>
<li>✓ Lower Back Brace 6 Stays Anti-Skid Lumbar Support</li>
<li>✓ Electric Vibration Massager Bunion Corrector</li>
<li>✓ Effective Bunion Corrector Airbag traction Foot</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Heavy-duty protection for back, hips, legs, knees, and feet. Based on OSHA/NIOSH 2025 industrial safety guidelines.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,manual-labor,tier4,heavy-duty,industrial,osha,35-percent-off"
    },

    # BUNDLE 13: Rehab Stroke Recovery (TIER 2)
    {
        "title": "Rehab Stroke Recovery - Robot Gloves Therapy Bundle",
        "handle": "rehab-stroke-recovery",
        "price": "281.58",
        "compare_at_price": "433.20",
        "persona": "rehab",
        "tier": "tier2",
        "products_count": 6,
        "savings": "151.62",
        "description": """<h2>Rehab Stroke Recovery</h2>
<p><strong>Perfect For:</strong> Post-stroke rehabilitation with robot gloves therapy</p>
<p><strong>Save $151.62 (35% OFF)</strong></p>

<h3>6 Products Included:</h3>
<ul>
<li>✓ Rehabilitation Robot Gloves Mirror Training Device</li>
<li>✓ Rehabilitation Robot Gloves Stroke Cerebral Palsy</li>
<li>✓ Posture Corrector Adjustable Back Brace for Women Men</li>
<li>✓ Silicone Patellar Tendon Strap Knee Pain Relief</li>
<li>✓ Bunion Corrector Toe Separator</li>
<li>✓ Electric Lumbar Massager Heated Vibration Back Brace</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Post-stroke recovery with 2 robot gloves models plus multi-zone support. Mirror therapy validated 2025.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,rehab,tier2,stroke-recovery,robot-gloves,therapy,35-percent-off"
    },

    # BUNDLE 14: Beauty & Wellness LED Complete (TIER 2)
    {
        "title": "Beauty & Wellness LED Complete - Anti-Aging Bundle",
        "handle": "beauty-wellness-led-complete",
        "price": "342.79",
        "compare_at_price": "527.37",
        "persona": "beauty",
        "tier": "tier2",
        "products_count": 5,
        "savings": "184.58",
        "description": """<h2>Beauty & Wellness LED Complete</h2>
<p><strong>Perfect For:</strong> Beauty enthusiasts seeking complete LED facial therapy</p>
<p><strong>Save $184.58 (35% OFF)</strong></p>

<h3>5 Products Included:</h3>
<ul>
<li>✓ 7 Color LED Light Therapy Face Mask Anti-Aging</li>
<li>✓ Professional 7-Color LED Mask Facial Light Therapy</li>
<li>✓ V-Line Face Slimming EMS Lifting Microcurrent Device</li>
<li>✓ Face Lifting Device Red Light Skin Rejuvenation V-Face</li>
<li>✓ Foreverlily LED Face Neck Mask 7 Colors 3D Flexible</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Complete LED facial therapy with 3 LED masks and 2 EMS devices. Light therapy before massage enhances results - clinical research 2025.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,beauty,tier2,led-therapy,anti-aging,facial,35-percent-off"
    },

    # BUNDLE 15: Senior Advanced Arthritis (TIER 3)
    {
        "title": "Senior Advanced Arthritis - Bunion & Joint Relief Bundle",
        "handle": "senior-advanced-arthritis",
        "price": "458.09",
        "compare_at_price": "704.75",
        "persona": "senior",
        "tier": "tier3",
        "products_count": 5,
        "savings": "246.66",
        "description": """<h2>Senior Advanced Arthritis</h2>
<p><strong>Perfect For:</strong> Seniors with advanced arthritis and bunion issues</p>
<p><strong>Save $246.66 (35% OFF)</strong></p>

<h3>5 Products Included:</h3>
<ul>
<li>✓ Electric Vibration Massager Bunion Corrector</li>
<li>✓ Effective Bunion Corrector Airbag traction Foot</li>
<li>✓ Electric Airbag Eye Massager Heated Hot Compress</li>
<li>✓ Cervical Spine Massager EMS Neck Lymphatic Drainage</li>
<li>✓ Stomach Massager Bian Shi Hot Compress Abdominal</li>
</ul>

<h3>Why This Bundle:</h3>
<p>Advanced arthritis management focusing on bunions, joint pain, and massage therapy. Fall Prevention Foundation 2025 guidelines.</p>

<p><strong>Free Shipping | 30-Day Returns</strong></p>""",
        "tags": "bundle,senior,tier3,arthritis,bunion-relief,joint-pain,35-percent-off"
    }
]

print("="*80)
print("CREATE REMAINING 9 BUNDLES (5-8, 10, 12-15)")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Bundles to create: {len(REMAINING_BUNDLES)}")
print("="*80)

# Get collection ID
print("\n1. Getting 'Medical Equipment Bundles' collection...")

collections = rest_request("GET", "/custom_collections.json")
bundle_collection = None

if collections and 'custom_collections' in collections:
    for coll in collections['custom_collections']:
        if coll['handle'] == 'medical-equipment-bundles':
            bundle_collection = coll
            print(f"✅ Collection found (ID: {coll['id']})")
            break

if not bundle_collection:
    print("❌ Collection not found")
    exit(1)

# Create remaining bundles
print(f"\n2. Creating {len(REMAINING_BUNDLES)} remaining bundles...\n")

created = []
failed = []

for i, bundle in enumerate(REMAINING_BUNDLES, 1):
    print(f"[{i}/{len(REMAINING_BUNDLES)}] {bundle['title'][:60]}...")

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
                "sku": f"BUNDLE-{bundle['handle'].upper()[:20]}",
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
print(f"\n✅ Created: {len(created)}/{len(REMAINING_BUNDLES)} bundles")
if failed:
    print(f"❌ Failed: {len(failed)}")
    for title in failed:
        print(f"   - {title}")

print(f"\n🔗 Collection: https://www.alphamedical.shop/collections/medical-equipment-bundles")
print(f"   Total bundles in collection: 6 (previous) + {len(created)} (new) = {6 + len(created)}")

print("\n📋 BUNDLES CREATED:")
for i, product in enumerate(created, 1):
    variant = product['variants'][0]
    savings = float(variant['compare_at_price']) - float(variant['price'])
    print(f"   {i}. {product['title'][:70]}")
    print(f"      ${variant['price']} (was ${variant['compare_at_price']}) - Save ${savings:.2f}")

print("\n" + "="*80)
print(f"COMPLETE ✅ - Total: {6 + len(created)}/15 bundles in Shopify")
print("="*80)
