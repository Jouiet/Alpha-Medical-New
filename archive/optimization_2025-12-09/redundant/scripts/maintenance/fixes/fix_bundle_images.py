#!/usr/bin/env python3
"""
FIX BUNDLE IMAGES - Upload product images to bundles

PROBLÈME: 15/15 bundles have ZERO images (0% completion)
SOLUTION: Extract first product from bundle, use its image as bundle image

EXIGENCES:
- Un script pour UN problème (images uniquement)
- Vérification FACTUELLE après exécution
- 100% success required (15/15 bundles)
- Pas de suppositions, seulement des faits

Author: Claude Code
Date: 2025-11-16
"""

import requests
import json
import re
import os
import tempfile
from pathlib import Path

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

def get_all_products(store, token):
    """Fetch all regular products (non-bundles) with images"""
    headers = {
        'X-Shopify-Access-Token': token,
        'Content-Type': 'application/json'
    }

    url = f"https://{store}/admin/api/2024-10/products.json?limit=250"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch products: {response.status_code}")
        return []

    products = response.json()['products']

    # Filter non-bundles with images
    regular_products = [
        p for p in products
        if 'bundle' not in p.get('tags', '').lower()
        and len(p.get('images', [])) > 0
    ]

    return regular_products

def get_bundles_without_images(store, token):
    """Fetch all bundles without images"""
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
    bundles = [
        p for p in products
        if 'bundle' in p.get('tags', '').lower()
        and len(p.get('images', [])) == 0
    ]

    return bundles

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

            # Remove price if present (e.g., "- $123.45")
            clean = re.sub(r'\s*-\s*\$[\d,]+\.?\d*', '', clean)

            if clean and len(clean) > 10:  # Minimum length for product title
                products.append(clean)

    return products

def find_matching_product(product_title, all_products):
    """
    Find matching product from catalog based on title similarity
    Uses exact title matching with pipe separators
    """
    # Clean the bundle product title
    clean_title = product_title.strip()

    # Try exact match first (with pipe separator format)
    for product in all_products:
        if product['title'].lower() == clean_title.lower():
            return product

    # Try partial match (first part before pipe)
    title_parts = clean_title.split('|')
    if len(title_parts) > 0:
        main_part = title_parts[0].strip()

        for product in all_products:
            product_main = product['title'].split('|')[0].strip()
            if product_main.lower() == main_part.lower():
                return product

    # Try fuzzy match (key words)
    # Extract key words (3+ chars, not common words)
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

        # Calculate overlap score
        if len(words) > 0:
            score = len(words & product_words) / len(words)
            if score > best_score and score >= 0.6:  # 60% match threshold
                best_score = score
                best_match = product

    return best_match

def download_image(image_url, temp_dir):
    """Download image to temporary directory"""
    try:
        response = requests.get(image_url, timeout=30)
        if response.status_code == 200:
            # Extract filename from URL
            filename = image_url.split('/')[-1].split('?')[0]
            if not filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                filename += '.jpg'

            filepath = os.path.join(temp_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(response.content)

            return filepath
    except Exception as e:
        print(f"   ❌ Failed to download image: {e}")

    return None

def upload_image_to_bundle(store, token, bundle_id, image_path):
    """Upload image to bundle product"""
    headers = {
        'X-Shopify-Access-Token': token
    }

    url = f"https://{store}/admin/api/2024-10/products/{bundle_id}/images.json"

    # Read image file
    with open(image_path, 'rb') as f:
        image_data = f.read()

    # Encode as base64
    import base64
    image_b64 = base64.b64encode(image_data).decode('utf-8')

    # Get filename
    filename = os.path.basename(image_path)

    payload = {
        "image": {
            "attachment": image_b64,
            "filename": filename
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        return True
    else:
        print(f"   ❌ Upload failed: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return False

def fix_bundle_images():
    """Main function to fix all bundle images"""

    print("🔧 FIX BUNDLE IMAGES - Starting...\n")
    print("="*100)

    # Load credentials
    env = load_env()
    store = env.get('SHOPIFY_STORE_DOMAIN')
    token = env.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

    if not store or not token:
        print("❌ ERROR: Missing credentials")
        return 1

    # Create temp directory for downloads
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Temp directory: {temp_dir}\n")

    # Fetch all products
    print("🔍 STEP 1: Fetching all products...")
    all_products = get_all_products(store, token)
    print(f"   ✅ Found {len(all_products)} regular products with images\n")

    # Fetch bundles without images
    print("🔍 STEP 2: Fetching bundles without images...")
    bundles = get_bundles_without_images(store, token)
    print(f"   ✅ Found {len(bundles)} bundles without images\n")

    if len(bundles) == 0:
        print("✅ All bundles already have images!")
        return 0

    print("="*100)
    print(f"\n🔧 STEP 3: Processing {len(bundles)} bundles...\n")

    success_count = 0
    failed_count = 0
    results = []

    for i, bundle in enumerate(bundles, 1):
        print(f"\n[{i}/{len(bundles)}] {bundle['handle']}")
        print(f"   Title: {bundle['title'][:70]}")

        # Extract product titles from bundle
        product_titles = extract_product_titles_from_bundle(bundle.get('body_html', ''))

        if not product_titles:
            print(f"   ❌ No products found in body_html")
            failed_count += 1
            results.append({
                'handle': bundle['handle'],
                'success': False,
                'reason': 'No products in body_html'
            })
            continue

        print(f"   📦 Found {len(product_titles)} products in bundle")

        # Try to find matching product for first product
        first_product_title = product_titles[0]
        print(f"   🔍 Searching for: {first_product_title[:60]}...")

        matching_product = find_matching_product(first_product_title, all_products)

        if not matching_product:
            print(f"   ❌ No matching product found")
            failed_count += 1
            results.append({
                'handle': bundle['handle'],
                'success': False,
                'reason': 'No matching product'
            })
            continue

        print(f"   ✅ Matched: {matching_product['handle']}")
        print(f"   🖼️  Image count: {len(matching_product['images'])}")

        # Download first image
        first_image_url = matching_product['images'][0]['src']
        print(f"   ⬇️  Downloading image...")

        image_path = download_image(first_image_url, temp_dir)

        if not image_path:
            print(f"   ❌ Failed to download image")
            failed_count += 1
            results.append({
                'handle': bundle['handle'],
                'success': False,
                'reason': 'Image download failed'
            })
            continue

        print(f"   ✅ Downloaded to: {os.path.basename(image_path)}")

        # Upload to bundle
        print(f"   ⬆️  Uploading to bundle...")

        if upload_image_to_bundle(store, token, bundle['id'], image_path):
            print(f"   ✅ SUCCESS: Image uploaded!")
            success_count += 1
            results.append({
                'handle': bundle['handle'],
                'success': True,
                'matched_product': matching_product['handle'],
                'image_url': first_image_url
            })
        else:
            print(f"   ❌ Upload failed")
            failed_count += 1
            results.append({
                'handle': bundle['handle'],
                'success': False,
                'reason': 'Upload failed'
            })

        # Clean up downloaded file
        try:
            os.remove(image_path)
        except:
            pass

    # Clean up temp directory
    try:
        os.rmdir(temp_dir)
    except:
        pass

    print("\n" + "="*100)
    print(f"\n📊 RESULTS:")
    print(f"{'='*100}")
    print(f"✅ SUCCESS: {success_count}/{len(bundles)} bundles")
    print(f"❌ FAILED:  {failed_count}/{len(bundles)} bundles")
    print(f"📈 Success rate: {100*success_count/len(bundles):.1f}%")
    print(f"{'='*100}")

    # Save results
    with open('bundle_images_fix_results.json', 'w') as f:
        json.dump({
            'total_bundles': len(bundles),
            'success_count': success_count,
            'failed_count': failed_count,
            'results': results
        }, f, indent=2)

    print(f"\n💾 Results saved to: bundle_images_fix_results.json")

    if failed_count > 0:
        print(f"\n❌ FAILED BUNDLES:")
        for r in results:
            if not r['success']:
                print(f"   - {r['handle']}: {r.get('reason', 'Unknown')}")

    if success_count == len(bundles):
        print(f"\n✅ 100% SUCCESS - All bundles now have images!")
        return 0
    else:
        print(f"\n⚠️  PARTIAL SUCCESS - {failed_count} bundles still need manual attention")
        return 1

if __name__ == "__main__":
    exit_code = fix_bundle_images()
    exit(exit_code)
