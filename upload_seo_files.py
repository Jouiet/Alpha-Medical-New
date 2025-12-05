#!/usr/bin/env python3
"""
Upload SEO files (robots.txt) to Shopify via Admin REST API
Note: Shopify auto-generates sitemap.xml, but we can upload custom robots.txt
"""

import os
import requests
from dotenv import load_dotenv

# Load environment
load_dotenv('.env.admin')

# Configuration
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = "2025-10"

def get_active_theme():
    """Get the active theme ID"""
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/themes.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code != 200:
        print(f"❌ Error fetching themes: {response.status_code}")
        return None

    themes = response.json().get('themes', [])
    active_theme = next((t for t in themes if t['role'] == 'main'), None)

    if active_theme:
        print(f"✅ Active theme: {active_theme['name']} (ID: {active_theme['id']})")
        return active_theme['id']

    return None

def upload_robots_txt(theme_id):
    """Upload robots.txt as a Liquid template"""
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    # Read robots.txt
    with open('robots.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    # Upload as robots.txt.liquid (Shopify convention)
    payload = {
        "asset": {
            "key": "templates/robots.txt.liquid",
            "value": content
        }
    }

    response = requests.put(url, headers=headers, json=payload, timeout=30)

    if response.status_code in [200, 201]:
        print(f"✅ Uploaded: robots.txt ({len(content)} bytes)")
        return True
    else:
        print(f"❌ Failed to upload robots.txt: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def main():
    """Upload SEO files to Shopify"""
    print("=" * 70)
    print("SEO FILES UPLOAD")
    print("=" * 70)
    print()

    # Get active theme
    print("1. Fetching active theme...")
    theme_id = get_active_theme()
    if not theme_id:
        print("❌ No active theme found")
        return False
    print()

    # Upload robots.txt
    print("2. Uploading robots.txt...")
    robots_success = upload_robots_txt(theme_id)
    print()

    # Info about sitemap.xml
    print("=" * 70)
    print("UPLOAD RESULTS")
    print("=" * 70)
    print()

    if robots_success:
        print("✅ robots.txt uploaded successfully!")
        print()
        print("📝 Note about sitemap.xml:")
        print("   Shopify auto-generates sitemap.xml at:")
        print("   https://www.alphamedical.shop/sitemap.xml")
        print()
        print("   The sitemap includes:")
        print("   - All products")
        print("   - All collections")
        print("   - All pages")
        print("   - All blog posts")
        print()
        print("   No manual upload needed! ✅")
        print()
        print("🎯 Next steps:")
        print("1. Verify robots.txt: https://www.alphamedical.shop/robots.txt")
        print("2. Submit Shopify's sitemap to Google Search Console:")
        print("   https://www.alphamedical.shop/sitemap.xml")
        print("3. Submit to Bing Webmaster Tools")
    else:
        print("❌ Failed to upload robots.txt")

    print()
    return robots_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
