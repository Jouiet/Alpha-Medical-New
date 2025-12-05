#!/usr/bin/env python3
"""
ALPHA MEDICAL - FORENSIC ANALYSIS SCRIPT
Complete factual verification of Shopify store infrastructure
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load credentials
load_dotenv('.env.admin')

SHOPIFY_STORE = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-01')

BASE_URL = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def api_get(endpoint):
    """Make GET request to Shopify Admin API"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def count_api_get(endpoint):
    """Get count from Shopify Admin API"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    print("=" * 80)
    print("ALPHA MEDICAL - FORENSIC INFRASTRUCTURE ANALYSIS")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)
    print()

    # 1. STORE CONFIGURATION
    print("=" * 80)
    print("1. STORE CONFIGURATION")
    print("=" * 80)
    shop_data = api_get("shop.json")
    if 'shop' in shop_data:
        shop = shop_data['shop']
        print(f"Store Name: {shop.get('name')}")
        print(f"Store Domain: {shop.get('domain')}")
        print(f"Primary Domain: {shop.get('primary_domain')}")
        print(f"Email: {shop.get('email')}")
        print(f"Currency: {shop.get('currency')}")
        print(f"Money Format: {shop.get('money_format')}")
        print(f"Timezone: {shop.get('timezone')}")
        print(f"Plan: {shop.get('plan_name')}")
        print(f"Country: {shop.get('country_name')}")
        print(f"Province: {shop.get('province')}")
        print(f"Setup Required: {shop.get('setup_required')}")
        print(f"Enabled Presentment Currencies: {shop.get('enabled_presentment_currencies')}")
    else:
        print(f"ERROR: {shop_data}")
    print()

    # 2. PRODUCTS
    print("=" * 80)
    print("2. PRODUCTS")
    print("=" * 80)
    products_count = count_api_get("products/count.json")
    if 'count' in products_count:
        print(f"Total Products: {products_count['count']}")

    # Get product status breakdown
    published_count = count_api_get("products/count.json?status=active")
    draft_count = count_api_get("products/count.json?status=draft")
    archived_count = count_api_get("products/count.json?status=archived")

    if 'count' in published_count:
        print(f"  - Published: {published_count['count']}")
    if 'count' in draft_count:
        print(f"  - Draft: {draft_count['count']}")
    if 'count' in archived_count:
        print(f"  - Archived: {archived_count['count']}")

    # Sample 5 products for analysis
    products = api_get("products.json?limit=5")
    if 'products' in products:
        print(f"\nSample Products (first 5):")
        for p in products['products']:
            print(f"  - {p.get('title')} | Status: {p.get('status')} | Variants: {len(p.get('variants', []))} | Price: ${p.get('variants', [{}])[0].get('price', '0')}")
    print()

    # 3. ORDERS
    print("=" * 80)
    print("3. ORDERS & REVENUE")
    print("=" * 80)
    orders_count = count_api_get("orders/count.json")
    if 'count' in orders_count:
        print(f"Total Orders: {orders_count['count']}")

    orders = api_get("orders.json?limit=10&status=any")
    if 'orders' in orders:
        total_revenue = sum(float(o.get('total_price', 0)) for o in orders['orders'])
        print(f"Recent Orders Count: {len(orders['orders'])}")
        print(f"Total Revenue (recent): ${total_revenue:.2f}")
    print()

    # 4. CUSTOMERS
    print("=" * 80)
    print("4. CUSTOMERS")
    print("=" * 80)
    customers_count = count_api_get("customers/count.json")
    if 'count' in customers_count:
        print(f"Total Customers: {customers_count['count']}")
    print()

    # 5. THEMES
    print("=" * 80)
    print("5. THEMES")
    print("=" * 80)
    themes = api_get("themes.json")
    if 'themes' in themes:
        print(f"Total Themes: {len(themes['themes'])}")
        for theme in themes['themes']:
            role = "LIVE" if theme.get('role') == 'main' else theme.get('role', 'unknown').upper()
            print(f"  - [{role}] {theme.get('name')} (ID: {theme.get('id')})")
            print(f"    Created: {theme.get('created_at')}")
            print(f"    Updated: {theme.get('updated_at')}")
    print()

    # 6. SCRIPTS (Shopify Scripts)
    print("=" * 80)
    print("6. SCRIPT TAGS (External Scripts)")
    print("=" * 80)
    script_tags = api_get("script_tags.json")
    if 'script_tags' in script_tags:
        print(f"Total Script Tags: {len(script_tags['script_tags'])}")
        for script in script_tags['script_tags']:
            print(f"  - {script.get('event')}: {script.get('src')}")
    else:
        print("No script tags found or error")
    print()

    # 7. WEBHOOKS
    print("=" * 80)
    print("7. WEBHOOKS")
    print("=" * 80)
    webhooks = api_get("webhooks.json")
    if 'webhooks' in webhooks:
        print(f"Total Webhooks: {len(webhooks['webhooks'])}")
        for wh in webhooks['webhooks']:
            print(f"  - {wh.get('topic')} -> {wh.get('address')}")
    else:
        print("No webhooks found or error")
    print()

    # 8. METAFIELDS (Store-level)
    print("=" * 80)
    print("8. METAFIELDS (Store-level)")
    print("=" * 80)
    metafields = api_get("metafields.json")
    if 'metafields' in metafields:
        print(f"Total Store Metafields: {len(metafields['metafields'])}")
        for mf in metafields['metafields']:
            value = str(mf.get('value', ''))[:50] if mf.get('value') else 'N/A'
            print(f"  - {mf.get('namespace')}.{mf.get('key')}: {value}...")
    else:
        print("No metafields found or error")
    print()

    # 9. LOCATIONS (Inventory)
    print("=" * 80)
    print("9. LOCATIONS (Inventory)")
    print("=" * 80)
    locations = api_get("locations.json")
    if 'locations' in locations:
        print(f"Total Locations: {len(locations['locations'])}")
        for loc in locations['locations']:
            print(f"  - {loc.get('name')}")
            print(f"    Address: {loc.get('address1')}, {loc.get('city')}, {loc.get('province')} {loc.get('zip')}")
            print(f"    Active: {loc.get('active')}")
    print()

    # 10. SHIPPING ZONES
    print("=" * 80)
    print("10. SHIPPING ZONES")
    print("=" * 80)
    # Note: Shipping zones might require GraphQL API
    print("Shipping zones require GraphQL API - will verify separately")
    print()

    # 11. PAYMENT SETTINGS
    print("=" * 80)
    print("11. PAYMENT SETTINGS")
    print("=" * 80)
    print("Payment settings verification requires manual inspection in Shopify Admin")
    print("Will verify via Chrome DevTools")
    print()

    # 12. POLICIES
    print("=" * 80)
    print("12. POLICIES")
    print("=" * 80)
    policies = api_get("policies.json")
    if 'policies' in policies:
        print(f"Total Policies: {len(policies['policies'])}")
        for policy in policies['policies']:
            print(f"  - {policy.get('title')}: {'SET' if policy.get('body') else 'NOT SET'}")
    print()

    # 13. COLLECTIONS
    print("=" * 80)
    print("13. COLLECTIONS")
    print("=" * 80)
    collections = api_get("custom_collections.json")
    smart_collections = api_get("smart_collections.json")

    custom_count = len(collections.get('custom_collections', [])) if 'custom_collections' in collections else 0
    smart_count = len(smart_collections.get('smart_collections', [])) if 'smart_collections' in smart_collections else 0

    print(f"Custom Collections: {custom_count}")
    print(f"Smart Collections: {smart_count}")
    print(f"Total Collections: {custom_count + smart_count}")
    print()

    # 14. PAGES
    print("=" * 80)
    print("14. PAGES")
    print("=" * 80)
    pages = api_get("pages.json")
    if 'pages' in pages:
        print(f"Total Pages: {len(pages['pages'])}")
        for page in pages['pages']:
            print(f"  - {page.get('title')} (Handle: {page.get('handle')})")
    print()

    # 15. BLOG POSTS
    print("=" * 80)
    print("15. BLOG POSTS")
    print("=" * 80)
    blogs = api_get("blogs.json")
    if 'blogs' in blogs:
        print(f"Total Blogs: {len(blogs['blogs'])}")
        for blog in blogs['blogs']:
            articles_count = count_api_get(f"blogs/{blog['id']}/articles/count.json")
            article_count = articles_count.get('count', 0)
            print(f"  - {blog.get('title')}: {article_count} articles")
    print()

    print("=" * 80)
    print("FORENSIC ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
