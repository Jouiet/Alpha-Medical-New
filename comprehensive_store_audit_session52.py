#!/usr/bin/env python3
"""
Comprehensive Store Audit - Session 52
Identify programmatic tasks that can be executed via API

Focus: What CAN be automated vs what requires manual UI work
"""

import os
import json
import requests
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables
load_dotenv('.env.admin')

SHOPIFY_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_THEME_ID = os.getenv('SHOPIFY_THEME_ID', '140069830733')
API_VERSION = '2025-10'
BASE_URL = f'https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}'

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

def api_request(endpoint, method='GET'):
    """Make API request"""
    url = f'{BASE_URL}{endpoint}'
    try:
        response = requests.request(method, url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e)}

print("=" * 80)
print("COMPREHENSIVE STORE AUDIT - SESSION 52")
print("=" * 80)
print("Objective: Identify programmatic tasks that can be executed")
print("=" * 80)

results = {}

# 1. CHECK PRODUCTS STATUS
print("\n1. PRODUCTS AUDIT:")
print("   " + "-" * 76)

products_result = api_request('/products.json?limit=250&status=any')
if 'products' in products_result:
    products = products_result['products']

    published = [p for p in products if p['status'] == 'active']
    draft = [p for p in products if p['status'] == 'draft']
    archived = [p for p in products if p['status'] == 'archived']

    print(f"   Total products: {len(products)}")
    print(f"   - Published: {len(published)}")
    print(f"   - Draft: {len(draft)}")
    print(f"   - Archived: {len(archived)}")

    # Check for missing images
    products_no_images = [p for p in published if not p.get('images')]
    if products_no_images:
        print(f"   ⚠️  Products without images: {len(products_no_images)}")
        for p in products_no_images[:5]:
            print(f"      - {p['title']} (ID: {p['id']})")
    else:
        print(f"   ✅ All published products have images")

    # Check for missing descriptions
    products_no_desc = [p for p in published if not p.get('body_html') or len(p['body_html'].strip()) < 50]
    if products_no_desc:
        print(f"   ⚠️  Products with short/missing descriptions: {len(products_no_desc)}")
    else:
        print(f"   ✅ All published products have descriptions")

    results['products'] = {
        'total': len(products),
        'published': len(published),
        'draft': len(draft),
        'archived': len(archived),
        'missing_images': len(products_no_images),
        'missing_descriptions': len(products_no_desc)
    }

# 2. CHECK COLLECTIONS
print("\n2. COLLECTIONS AUDIT:")
print("   " + "-" * 76)

collections_result = api_request('/custom_collections.json')
if 'custom_collections' in collections_result:
    collections = collections_result['custom_collections']
    print(f"   Custom collections: {len(collections)}")

    # Check for collections without images
    collections_no_images = [c for c in collections if not c.get('image')]
    if collections_no_images:
        print(f"   ⚠️  Collections without images: {len(collections_no_images)}")
        for c in collections_no_images[:3]:
            print(f"      - {c['title']}")

    results['collections'] = {
        'total': len(collections),
        'missing_images': len(collections_no_images)
    }

# 3. CHECK THEME ASSETS
print("\n3. THEME ASSETS AUDIT:")
print("   " + "-" * 76)

critical_assets = [
    'assets/product-recommendations-matrix.js',
    'layout/theme.liquid',
    'sections/header.liquid',
    'sections/footer.liquid'
]

assets_status = {}
for asset_key in critical_assets:
    asset_result = api_request(f'/themes/{SHOPIFY_THEME_ID}/assets.json?asset[key]={asset_key}')

    if 'asset' in asset_result and asset_result['asset']:
        asset = asset_result['asset']
        print(f"   ✅ {asset_key}")
        print(f"      Size: {asset.get('size', 0):,} bytes")
        assets_status[asset_key] = 'exists'
    else:
        print(f"   ❌ {asset_key} - NOT FOUND")
        assets_status[asset_key] = 'missing'

results['theme_assets'] = assets_status

# 4. CHECK PAGES
print("\n4. PAGES AUDIT:")
print("   " + "-" * 76)

pages_result = api_request('/pages.json')
if 'pages' in pages_result:
    pages = pages_result['pages']
    print(f"   Total pages: {len(pages)}")

    critical_pages = ['about-us', 'contact', 'privacy-policy', 'terms-of-service', 'shipping-policy', 'refund-policy']
    existing_handles = [p['handle'] for p in pages]

    for critical in critical_pages:
        if critical in existing_handles:
            print(f"   ✅ {critical}")
        else:
            print(f"   ❌ {critical} - MISSING")

    results['pages'] = {
        'total': len(pages),
        'existing_handles': existing_handles
    }

# 5. CHECK NAVIGATION MENUS
print("\n5. NAVIGATION MENUS:")
print("   " + "-" * 76)

# Note: Menus are in theme code, not accessible via Shop API
print("   ⚠️  Navigation menus require theme code inspection")
print("   Status: Requires theme.liquid verification")

# 6. CHECK BLOG POSTS
print("\n6. BLOG POSTS AUDIT:")
print("   " + "-" * 76)

blogs_result = api_request('/blogs.json')
if 'blogs' in blogs_result:
    for blog in blogs_result['blogs']:
        articles_result = api_request(f'/blogs/{blog["id"]}/articles.json')
        if 'articles' in articles_result:
            articles = articles_result['articles']
            print(f"   Blog: {blog['title']}")
            print(f"   - Total articles: {len(articles)}")
            print(f"   - Published: {len([a for a in articles if a.get('published_at')])}")

# 7. PROGRAMMATIC TASKS AVAILABLE
print("\n" + "=" * 80)
print("PROGRAMMATIC TASKS AVAILABLE (CAN BE AUTOMATED):")
print("=" * 80)

tasks = []

if results.get('products', {}).get('missing_images', 0) > 0:
    tasks.append(f"Fix {results['products']['missing_images']} products without images")

if results.get('products', {}).get('missing_descriptions', 0) > 0:
    tasks.append(f"Fix {results['products']['missing_descriptions']} products with short descriptions")

if results.get('collections', {}).get('missing_images', 0) > 0:
    tasks.append(f"Add images to {results['collections']['missing_images']} collections")

# Check if any critical assets are missing
missing_assets = [k for k, v in assets_status.items() if v == 'missing']
if missing_assets:
    for asset in missing_assets:
        tasks.append(f"Deploy {asset} to theme")

if tasks:
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
else:
    print("✅ No programmatic tasks identified - Store is in good shape!")

# 8. MANUAL TASKS REQUIRED
print("\n" + "=" * 80)
print("MANUAL TASKS (CANNOT BE AUTOMATED):")
print("=" * 80)

manual_tasks = [
    "Shopify Flow configurations (no API, cross-origin iframe blocks automation)",
    "Upload social share image to Theme Settings → Social media (5 min)",
    "Configure GitHub Secrets (5 min)",
    "Setup Google Sheets API credentials (10 min)",
    "Create snippets/smart-recommendations.liquid component (15 hours)",
    "Subscriptions configuration (Admin UI only)",
    "Loyalty system setup (requires plan upgrade to $79/mo)"
]

for i, task in enumerate(manual_tasks, 1):
    print(f"{i}. {task}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Programmatic tasks available: {len(tasks)}")
print(f"Manual tasks required: {len(manual_tasks)}")
print(f"Store status: {'GOOD' if len(tasks) == 0 else 'NEEDS FIXES'}")
print("=" * 80)

# Save results to file
output_file = '/tmp/comprehensive_audit_session52.json'
with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n✅ Results saved to: {output_file}")
