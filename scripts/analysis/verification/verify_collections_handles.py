#!/usr/bin/env python3
"""
VERIFY COLLECTIONS HANDLES - Alpha Medical Care
Check all collection handles for dead links
"""

import requests
from datetime import datetime

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
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

print("=" * 80)
print("COLLECTIONS HANDLES VERIFICATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# Fetch all collections
query = """
{
  collections(first: 50) {
    edges {
      node {
        id
        title
        handle
        productsCount
        description(truncateAt: 100)
      }
    }
  }
}
"""

response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
data = response.json()

if "errors" in data:
    print(f"❌ GraphQL Errors: {data['errors']}")
    exit(1)

collections = data["data"]["collections"]["edges"]

print(f"\nTotal collections: {len(collections)}\n")

dead_links = []
live_links = []

for edge in collections:
    collection = edge["node"]
    handle = collection["handle"]
    title = collection["title"]
    products_count = collection["productsCount"]

    # Test URL
    url = f"https://www.alphamedical.shop/collections/{handle}"

    try:
        check_response = requests.head(url, timeout=5, allow_redirects=True)
        status = check_response.status_code

        if status == 200:
            live_links.append({
                'title': title,
                'handle': handle,
                'url': url,
                'products': products_count
            })
            print(f"✅ {title}")
            print(f"   Handle: {handle}")
            print(f"   URL: {url}")
            print(f"   Products: {products_count}")
            print(f"   Status: {status} OK\n")
        else:
            dead_links.append({
                'title': title,
                'handle': handle,
                'url': url,
                'status': status,
                'products': products_count
            })
            print(f"❌ {title}")
            print(f"   Handle: {handle}")
            print(f"   URL: {url}")
            print(f"   Products: {products_count}")
            print(f"   Status: {status} DEAD LINK\n")

    except Exception as e:
        dead_links.append({
            'title': title,
            'handle': handle,
            'url': url,
            'error': str(e),
            'products': products_count
        })
        print(f"❌ {title}")
        print(f"   Handle: {handle}")
        print(f"   URL: {url}")
        print(f"   Error: {e}\n")

print("=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\n✅ Live Collections: {len(live_links)}/{len(collections)}")
for col in live_links:
    print(f"   - {col['title']} ({col['products']} products)")

if dead_links:
    print(f"\n❌ Dead Links: {len(dead_links)}/{len(collections)}")
    for col in dead_links:
        print(f"   - {col['title']} (handle: {col['handle']})")
        print(f"     URL: {col['url']}")
        print(f"     Issue: {col.get('status', col.get('error'))}")

    print(f"\n⚠️ ACTION REQUIRED:")
    print(f"   - Remove dead links from navigation")
    print(f"   - OR fix collection handles")
    print(f"   - OR update internal links")
else:
    print(f"\n✅ ALL COLLECTIONS ACCESSIBLE")

print("\n" + "=" * 80)
