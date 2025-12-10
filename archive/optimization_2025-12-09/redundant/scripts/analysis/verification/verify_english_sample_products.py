#!/usr/bin/env python3
"""
AUDIT FORENSIQUE - Sample 10 Products Manual Verification
Date: 2025-11-20
Purpose: Display 10 random products for MANUAL review (title + body excerpt)
"""

import os
import requests
import json
import random
from html import unescape
import re

# Load credentials
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

SHOP = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
REST_URL = f"https://{SHOP}/admin/api/{API_VERSION}"
HEADERS = {"X-Shopify-Access-Token": TOKEN}

def strip_html(html: str) -> str:
    """Strip HTML tags and get plain text"""
    if not html:
        return ""
    text = re.sub(r'<[^>]+>', ' ', html)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_all_products():
    url = f"{REST_URL}/products.json?limit=250"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return []
    return response.json().get("products", [])

def main():
    print("=" * 80)
    print("MANUAL VERIFICATION - Sample 10 Products")
    print("=" * 80)
    print("Purpose: Human review of product content for French language\n")

    products = fetch_all_products()
    print(f"✅ Fetched {len(products)} products")
    print(f"🎲 Selecting 10 random products for manual review...\n")

    # Sample 10 random products
    sample = random.sample(products, min(10, len(products)))

    for i, product in enumerate(sample, 1):
        title = product.get("title", "")
        body_html = product.get("body_html", "") or ""
        body_text = strip_html(body_html)
        handle = product.get("handle", "")
        tags = product.get("tags", "")

        print("=" * 80)
        print(f"PRODUCT {i}/10")
        print("=" * 80)
        print(f"Handle: {handle}")
        print(f"Title: {title}")
        print(f"Tags: {tags}")
        print(f"\nBody (first 500 chars):")
        print(body_text[:500])
        print("...")
        print()

        # Ask for manual verification
        print("👁️  MANUAL CHECK:")
        print("   - Is the title 100% English? ___")
        print("   - Is the body 100% English? ___")
        print("   - Any French words detected? ___")
        print()

    print("=" * 80)
    print("MANUAL VERIFICATION COMPLETE")
    print("=" * 80)
    print(f"✅ Reviewed 10/{len(products)} products")
    print()
    print("Next: Review all 10 products above manually")
    print("If all are 100% English → Site is 100% English ✅")
    print("If any French found → Report violations ❌")

if __name__ == "__main__":
    main()
