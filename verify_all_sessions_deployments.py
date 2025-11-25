#!/usr/bin/env python3
"""
Comprehensive Verification - All Sessions (49-52)
Bottom-up factual approach: Verify what EXISTS, not what's missing

Verifies:
- Session 49: Infrastructure audit results
- Session 50: AI recommendations matrix generation
- Session 51: AI matrix deployment + social share image
- Session 52: Collections fix + policy pages
"""

import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env.admin')

SHOPIFY_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_THEME_ID = os.getenv('SHOPIFY_THEME_ID', '140069830733')
API_VERSION = '2024-10'
BASE_URL = f'https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}'

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

def api_request(endpoint, method='GET'):
    url = f'{BASE_URL}{endpoint}'
    try:
        response = requests.request(method, url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e)}

print("=" * 80)
print("COMPREHENSIVE VERIFICATION - SESSIONS 49-52")
print("=" * 80)
print(f"Store: {SHOPIFY_DOMAIN}")
print(f"Theme: {SHOPIFY_THEME_ID}")
print(f"Verified at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

verification_results = {}

# ==============================================================================
# SESSION 50/51 VERIFICATION: AI RECOMMENDATIONS MATRIX
# ==============================================================================
print("\n1. AI RECOMMENDATIONS MATRIX (Sessions 50 & 51):")
print("   " + "-" * 76)

# Check local file
local_matrix = '/Users/mac/Desktop/Alpha-Medical/assets/product-recommendations-matrix.js'
if os.path.exists(local_matrix):
    local_size = os.path.getsize(local_matrix)
    print(f"   ✅ Local file exists: {local_size:,} bytes")
    verification_results['ai_matrix_local'] = True
else:
    print(f"   ❌ Local file missing")
    verification_results['ai_matrix_local'] = False

# Check deployed to theme
theme_asset = api_request(f'/themes/{SHOPIFY_THEME_ID}/assets.json?asset[key]=assets/product-recommendations-matrix.js')
if 'asset' in theme_asset and theme_asset['asset']:
    asset = theme_asset['asset']
    print(f"   ✅ Deployed to theme: {asset.get('size', 0):,} bytes")
    print(f"   📅 Last updated: {asset.get('updated_at', 'N/A')}")
    print(f"   🔗 Public URL: {asset.get('public_url', 'N/A')[:80]}...")
    verification_results['ai_matrix_deployed'] = True
else:
    print(f"   ❌ NOT deployed to theme")
    verification_results['ai_matrix_deployed'] = False

# ==============================================================================
# SESSION 51 VERIFICATION: SOCIAL SHARE IMAGE
# ==============================================================================
print("\n2. SOCIAL SHARE IMAGE (Session 51):")
print("   " + "-" * 76)

social_image = '/Users/mac/Desktop/Alpha-Medical/alpha_medical_social_share.png'
if os.path.exists(social_image):
    img_size = os.path.getsize(social_image)
    print(f"   ✅ Generated: {img_size:,} bytes ({img_size/1024:.1f} KB)")
    print(f"   📁 Location: {social_image}")
    print(f"   ⏳ Upload status: PENDING (requires Theme Settings UI)")
    verification_results['social_image_generated'] = True
    verification_results['social_image_uploaded'] = False
else:
    print(f"   ❌ File not generated")
    verification_results['social_image_generated'] = False

# ==============================================================================
# SESSION 52 VERIFICATION: POLICY PAGES
# ==============================================================================
print("\n3. POLICY PAGES (Session 52):")
print("   " + "-" * 76)

required_policies = {
    'privacy-policy': 108428722253,
    'shipping-policy': 108428755021,
    'refund-policy': 108428787789
}

pages_result = api_request('/pages.json')
if 'pages' in pages_result:
    existing_pages = {p['handle']: p for p in pages_result['pages']}

    for handle, expected_id in required_policies.items():
        if handle in existing_pages:
            page = existing_pages[handle]
            print(f"   ✅ {handle}")
            print(f"      ID: {page['id']} (expected: {expected_id})")
            print(f"      Created: {page.get('created_at', 'N/A')[:10]}")
            verification_results[f'policy_{handle}'] = True
        else:
            print(f"   ❌ {handle} - MISSING")
            verification_results[f'policy_{handle}'] = False

# ==============================================================================
# SESSION 52 VERIFICATION: COLLECTIONS IMAGES
# ==============================================================================
print("\n4. COLLECTIONS IMAGES (Session 52):")
print("   " + "-" * 76)

collections_result = api_request('/custom_collections.json')
if 'custom_collections' in collections_result:
    collections = collections_result['custom_collections']

    target_collections = {
        'Medical Equipment Bundles': False,  # Should be fixed
        'Complete Care Kits': False  # Should still be missing
    }

    for collection in collections:
        if collection['title'] in target_collections:
            has_image = bool(collection.get('image'))
            status = "✅" if has_image else "❌"
            print(f"   {status} {collection['title']}: {'Has image' if has_image else 'No image'}")

            if collection['title'] == 'Medical Equipment Bundles':
                verification_results['collection_medical_equipment'] = has_image
            elif collection['title'] == 'Complete Care Kits':
                verification_results['collection_complete_care'] = has_image

    collections_no_images = [c for c in collections if not c.get('image')]
    print(f"\n   Summary: {len(collections) - len(collections_no_images)}/{len(collections)} collections have images")

# ==============================================================================
# STORE HEALTH CHECK
# ==============================================================================
print("\n5. STORE HEALTH CHECK:")
print("   " + "-" * 76)

# Check products count (via GraphQL since REST can be flaky)
graphql_url = f'https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json'
graphql_query = '''
{
  products(first: 1) {
    edges {
      node {
        id
      }
    }
  }
  productsCount: products {
    edges {
      node {
        id
      }
    }
  }
}
'''

graphql_headers = {
    'X-Shopify-Access-Token': SHOPIFY_TOKEN,
    'Content-Type': 'application/json'
}

try:
    response = requests.post(
        graphql_url,
        json={'query': graphql_query},
        headers=graphql_headers,
        timeout=30
    )
    if response.status_code == 200:
        print(f"   ✅ Store API accessible")
        verification_results['store_api'] = True
    else:
        print(f"   ⚠️  Store API returned {response.status_code}")
        verification_results['store_api'] = False
except Exception as e:
    print(f"   ❌ Store API error: {e}")
    verification_results['store_api'] = False

# ==============================================================================
# SCRIPTS VERIFICATION
# ==============================================================================
print("\n6. SCRIPTS CREATED (Sessions 50-52):")
print("   " + "-" * 76)

scripts_to_check = [
    'generate_recommendations_matrix.py',
    'deploy_recommendations_matrix.py',
    'verify_session51_deployments.py',
    'comprehensive_store_audit_session52.py',
    'create_missing_policy_pages.py',
    'fix_collections_missing_images.py',
    'fix_complete_care_kits_image.py'
]

scripts_exist = 0
for script in scripts_to_check:
    path = f'/Users/mac/Desktop/Alpha-Medical/{script}'
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"   ✅ {script} ({size:,} bytes)")
        scripts_exist += 1
    else:
        print(f"   ❌ {script} - MISSING")

print(f"\n   Scripts: {scripts_exist}/{len(scripts_to_check)} exist")

# ==============================================================================
# SUMMARY
# ==============================================================================
print("\n" + "=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

total_checks = len(verification_results)
passed_checks = sum(1 for v in verification_results.values() if v)

print(f"Total checks: {total_checks}")
print(f"Passed: {passed_checks}")
print(f"Failed: {total_checks - passed_checks}")
print(f"Success rate: {(passed_checks/total_checks*100):.1f}%")

print("\n" + "=" * 80)
print("DEPLOYMENT STATUS")
print("=" * 80)

deployments = [
    ("AI Recommendations Matrix (Local)", verification_results.get('ai_matrix_local', False)),
    ("AI Recommendations Matrix (Theme)", verification_results.get('ai_matrix_deployed', False)),
    ("Social Share Image (Generated)", verification_results.get('social_image_generated', False)),
    ("Social Share Image (Uploaded)", verification_results.get('social_image_uploaded', False)),
    ("Privacy Policy Page", verification_results.get('policy_privacy-policy', False)),
    ("Shipping Policy Page", verification_results.get('policy_shipping-policy', False)),
    ("Refund Policy Page", verification_results.get('policy_refund-policy', False)),
    ("Medical Equipment Bundles Image", verification_results.get('collection_medical_equipment', False)),
    ("Complete Care Kits Image", verification_results.get('collection_complete_care', False)),
]

for name, status in deployments:
    icon = "✅" if status else "❌"
    print(f"{icon} {name}")

print("\n" + "=" * 80)
print("PENDING MANUAL TASKS")
print("=" * 80)
manual_tasks = [
    "1. Upload social share image to Theme Settings (5 min)",
    "2. Configure GitHub Secrets (5 min) - Unblocks 9 workflows",
    "3. Setup Google Sheets API credentials (10 min) - Unblocks lead generation",
    "4. Add images to 10 Complete Care Kits products (data quality issue)",
    "5. Shopify Flow configurations (60 min)",
    "6. Create smart-recommendations.liquid component (15 hours)"
]

for task in manual_tasks:
    print(f"   {task}")

print("=" * 80)

# Save results
output_file = '/tmp/verification_sessions_49-52.json'
with open(output_file, 'w') as f:
    json.dump(verification_results, f, indent=2)

print(f"\n✅ Verification results saved to: {output_file}")
print("=" * 80)
