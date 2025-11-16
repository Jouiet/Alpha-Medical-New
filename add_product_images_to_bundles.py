#!/usr/bin/env python3
"""
ADD PRODUCT IMAGES TO BUNDLES - Native Shopify Solution

PROBLÈME: Bundles have only 1 image (bundle image)
SOLUTION: Add individual product images to bundle product gallery

BENEFIT:
- Images appear automatically in Shopify product gallery
- No custom code needed
- Native Shopify functionality
- Customers can see ALL products in bundle

EXIGENCES:
- Un script pour UN problème (images gallery)
- Vérification FACTUELLE après exécution
- 100% success required (15/15 bundles)

Author: Claude Code
Date: 2025-11-16
"""

import requests
import json
import re
import os
import time

def load_env():
    """Load credentials from .env.admin"""
    env_vars = {}
    with open('.env.admin', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    return env_vars

def get_all_bundles(store, token):
    """Fetch all bundles"""
    headers = {
        'X-Shopify-Access-Token': token,
        'Content-Type': 'application/json'
    }

    url = f"https://{store}/admin/api/2024-10/products.json?product_type=Medical Equipment Bundle&limit=250"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch bundles: {response.status_code}")
        return []

    products = response.json()['products']
    bundles = [p for p in products if 'bundle' in p.get('tags', '').lower()]

    return bundles

def get_all_products(store, token):
    """Fetch all regular products"""
    headers = {
        'X-Shopify-Access-Token': token,
        'Content-Type': 'application/json'
    }

    url = f"https://{store}/admin/api/2024-10/products.json?limit=250"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    products = response.json()['products']
    regular_products = [p for p in products if 'bundle' not in p.get('tags', '').lower()]

    return regular_products

def extract_product_titles_from_bundle(body_html):
    """Extract product titles from bundle body_html"""
    if not body_html:
        return []

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', body_html)

    # Find lines with checkmarks or bullets
    lines = text.split('\n')
    products = []

    for line in lines:
        if '✓' in line or '•' in line or line.strip().startswith(('-', '*')):
            # Clean the line
            clean = line.replace('✓', '').replace('•', '').replace('-', '').replace('*', '').strip()

            # Remove price if present
            clean = re.sub(r'\s*-\s*\$[\d,]+\.?\d*', '', clean)

            if clean and len(clean) > 10:
                products.append(clean)

    return products

def find_matching_product(product_title, all_products):
    """Find matching product from catalog"""
    clean_title = product_title.strip()

    # Try exact match
    for product in all_products:
        if product['title'].lower() == clean_title.lower():
            return product

    # Try partial match
    title_parts = clean_title.split('|')
    if len(title_parts) > 0:
        main_part = title_parts[0].strip()

        for product in all_products:
            product_main = product['title'].split('|')[0].strip()
            if product_main.lower() == main_part.lower():
                return product

    # Try fuzzy match
    common_words = {'the', 'and', 'for', 'with', 'support', 'brace', 'pain', 'relief'}
    words = set([
        w.lower() for w in re.findall(r'\b\w{3,}\b', clean_title)
        if w.lower() not in common_words
    ])

    best_match = None
    best_score = 0

    for product in all_products:
        product_words = set([
            w.lower() for w in re.findall(r'\b\w{3,}\b', product['title'])
            if w.lower() not in common_words
        ])

        if len(words) > 0:
            score = len(words & product_words) / len(words)
            if score > best_score and score >= 0.6:
                best_score = score
                best_match = product

    return best_match

def add_image_to_bundle(store, token, bundle_id, image_src):
    """Add image to bundle product via Shopify API"""
    headers = {
        'X-Shopify-Access-Token': token,
        'Content-Type': 'application/json'
    }

    url = f"https://{store}/admin/api/2024-10/products/{bundle_id}/images.json"

    payload = {
        "image": {
            "src": image_src
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return True
    else:
        print(f"   ❌ Upload failed: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return False

def add_product_images_to_bundles():
    """Main function to add product images to all bundles"""

    print("🔧 ADD PRODUCT IMAGES TO BUNDLES - Starting...\n")
    print("="*100)

    # Load credentials
    env = load_env()
    store = env.get('SHOPIFY_STORE_DOMAIN')
    token = env.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

    if not store or not token:
        print("❌ ERROR: Missing credentials")
        return 1

    # Fetch all products
    print("🔍 STEP 1: Fetching all products...")
    all_products = get_all_products(store, token)
    print(f"   ✅ Found {len(all_products)} regular products\n")

    # Fetch all bundles
    print("🔍 STEP 2: Fetching all bundles...")
    bundles = get_all_bundles(store, token)
    print(f"   ✅ Found {len(bundles)} bundles\n")

    print("="*100)
    print(f"\n🔧 STEP 3: Adding product images to {len(bundles)} bundles...\n")

    success_count = 0
    failed_count = 0
    results = []

    for i, bundle in enumerate(bundles, 1):
        print(f"\n[{i}/{len(bundles)}] {bundle['handle']}")
        print(f"   Title: {bundle['title'][:70]}")

        # Current image count
        current_image_count = len(bundle.get('images', []))
        print(f"   Current images: {current_image_count}")

        # Extract product titles from bundle
        product_titles = extract_product_titles_from_bundle(bundle.get('body_html', ''))

        if not product_titles:
            print(f"   ❌ No products found in body_html")
            failed_count += 1
            results.append({
                'handle': bundle['handle'],
                'success': False,
                'reason': 'No products in body_html',
                'images_added': 0
            })
            continue

        print(f"   📦 Found {len(product_titles)} products in bundle")

        # Match products and add their images
        images_added = 0
        for j, title in enumerate(product_titles, 1):
            print(f"      [{j}/{len(product_titles)}] Matching: {title[:50]}...")

            matching_product = find_matching_product(title, all_products)

            if not matching_product:
                print(f"         ❌ No match found")
                continue

            print(f"         ✅ Matched: {matching_product['handle']}")

            # Get product image
            if len(matching_product.get('images', [])) == 0:
                print(f"         ⚠️  Product has no images")
                continue

            first_image = matching_product['images'][0]
            image_src = first_image['src']

            # Add image to bundle
            print(f"         ⬆️  Adding image to bundle...")

            if add_image_to_bundle(store, token, bundle['id'], image_src):
                print(f"         ✅ Image added successfully")
                images_added += 1
                # Rate limit: wait 0.5s between API calls
                time.sleep(0.5)
            else:
                print(f"         ❌ Failed to add image")

        # Summary for this bundle
        print(f"   📊 RESULT: {images_added} images added (was {current_image_count}, now {current_image_count + images_added})")

        if images_added > 0:
            success_count += 1
            results.append({
                'handle': bundle['handle'],
                'success': True,
                'images_added': images_added,
                'total_images': current_image_count + images_added
            })
        else:
            failed_count += 1
            results.append({
                'handle': bundle['handle'],
                'success': False,
                'reason': 'No images could be added',
                'images_added': 0
            })

    print("\n" + "="*100)
    print(f"\n📊 RESULTS:")
    print(f"{'='*100}")
    print(f"✅ SUCCESS: {success_count}/{len(bundles)} bundles")
    print(f"❌ FAILED:  {failed_count}/{len(bundles)} bundles")
    print(f"📈 Success rate: {100*success_count/len(bundles):.1f}%")
    print(f"{'='*100}")

    # Save results
    with open('bundle_product_images_results.json', 'w') as f:
        json.dump({
            'total_bundles': len(bundles),
            'success_count': success_count,
            'failed_count': failed_count,
            'results': results
        }, f, indent=2)

    print(f"\n💾 Results saved to: bundle_product_images_results.json")

    if failed_count > 0:
        print(f"\n❌ FAILED BUNDLES:")
        for r in results:
            if not r['success']:
                print(f"   - {r['handle']}: {r.get('reason', 'Unknown')}")

    # Show summary
    if success_count > 0:
        print(f"\n📊 IMAGES ADDED SUMMARY:")
        total_images_added = sum([r.get('images_added', 0) for r in results])
        print(f"   Total images added across all bundles: {total_images_added}")
        for r in results:
            if r['success']:
                print(f"   {r['handle']}: +{r['images_added']} images (total: {r['total_images']})")

    if success_count == len(bundles):
        print(f"\n✅ 100% SUCCESS - All bundles now have product images!")
        return 0
    else:
        print(f"\n⚠️  PARTIAL SUCCESS - {failed_count} bundles need manual attention")
        return 1

if __name__ == "__main__":
    exit_code = add_product_images_to_bundles()
    exit(exit_code)
