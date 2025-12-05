#!/usr/bin/env python3
"""
Generate sitemap.xml for Alpha Medical store
Fetches all products and creates SEO-optimized sitemap
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv('.env.admin')

# Configuration
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = "2025-10"
STORE_URL = "https://www.alphamedical.shop"

def fetch_all_products():
    """Fetch all published products from Shopify"""
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/products.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    products = []
    params = {"status": "active", "limit": 250}

    while True:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code != 200:
            print(f"❌ Error fetching products: {response.status_code}")
            print(response.text)
            break

        data = response.json()
        batch = data.get('products', [])
        products.extend(batch)

        print(f"Fetched {len(batch)} products (total: {len(products)})")

        # Check for pagination
        link_header = response.headers.get('Link', '')
        if 'rel="next"' not in link_header:
            break

        # Extract next page URL
        next_link = [l.strip() for l in link_header.split(',') if 'rel="next"' in l]
        if not next_link:
            break

        next_url = next_link[0].split(';')[0].strip('<>')
        url = next_url
        params = {}

    return products

def fetch_all_collections():
    """Fetch all collections from Shopify"""
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/custom_collections.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        print(f"❌ Error fetching collections: {response.status_code}")
        return []

    collections = response.json().get('custom_collections', [])
    print(f"Fetched {len(collections)} collections")
    return collections

def generate_sitemap(products, collections):
    """Generate sitemap.xml content"""
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00:00')

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '',
        '  <!-- Homepage -->',
        '  <url>',
        f'    <loc>{STORE_URL}/</loc>',
        f'    <lastmod>{now}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '',
        '  <!-- Collections -->',
    ]

    # Add collections
    for collection in collections:
        handle = collection['handle']
        updated = collection.get('updated_at', now)
        xml.extend([
            '  <url>',
            f'    <loc>{STORE_URL}/collections/{handle}</loc>',
            f'    <lastmod>{updated}</lastmod>',
            '    <changefreq>weekly</changefreq>',
            '    <priority>0.8</priority>',
            '  </url>',
        ])

    xml.append('')
    xml.append('  <!-- Products -->')

    # Add products
    for product in products:
        handle = product['handle']
        updated = product.get('updated_at', now)
        xml.extend([
            '  <url>',
            f'    <loc>{STORE_URL}/products/{handle}</loc>',
            f'    <lastmod>{updated}</lastmod>',
            '    <changefreq>weekly</changefreq>',
            '    <priority>0.7</priority>',
            '  </url>',
        ])

    # Add static pages
    xml.extend([
        '',
        '  <!-- Static Pages -->',
        '  <url>',
        f'    <loc>{STORE_URL}/pages/about</loc>',
        f'    <lastmod>{now}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.6</priority>',
        '  </url>',
        '  <url>',
        f'    <loc>{STORE_URL}/pages/contact</loc>',
        f'    <lastmod>{now}</lastmod>',
        '    <changefreq>monthly</changefreq>',
        '    <priority>0.6</priority>',
        '  </url>',
        '',
        '</urlset>'
    ])

    return '\n'.join(xml)

def main():
    """Generate sitemap.xml"""
    print("=" * 60)
    print("SITEMAP.XML GENERATOR")
    print("=" * 60)
    print()

    # Fetch data
    print("Fetching products...")
    products = fetch_all_products()

    print("Fetching collections...")
    collections = fetch_all_collections()

    # Generate sitemap
    print()
    print("Generating sitemap...")
    sitemap_xml = generate_sitemap(products, collections)

    # Write to file
    output_path = "sitemap.xml"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(sitemap_xml)

    print()
    print("=" * 60)
    print("✅ SITEMAP GENERATED")
    print("=" * 60)
    print(f"File: {output_path}")
    print(f"Products: {len(products)}")
    print(f"Collections: {len(collections)}")
    print(f"Total URLs: {1 + len(collections) + len(products) + 2}")  # homepage + collections + products + static pages
    print()
    print("📝 Next steps:")
    print("1. Upload sitemap.xml to root of Shopify store")
    print("2. Submit to Google Search Console: https://search.google.com/search-console")
    print("3. Submit to Bing Webmaster Tools: https://www.bing.com/webmasters")
    print()

if __name__ == "__main__":
    main()
