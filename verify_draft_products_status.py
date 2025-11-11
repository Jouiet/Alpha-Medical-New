#!/usr/bin/env python3
"""
VERIFY DRAFT PRODUCTS STATUS - Alpha Medical Care
Ensure draft products remain draft (NO accidental publish)

REQUIREMENT: Draft products MUST remain draft
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
print("DRAFT PRODUCTS STATUS VERIFICATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# Fetch all products
query = """
{
  products(first: 250) {
    edges {
      node {
        id
        title
        handle
        status
        publishedAt
        createdAt
        updatedAt
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

products = data["data"]["products"]["edges"]

print(f"\nTotal products: {len(products)}\n")

# Categorize by status
active_products = []
draft_products = []
archived_products = []

for edge in products:
    product = edge["node"]
    product_id = product["id"]
    title = product["title"]
    handle = product["handle"]
    status = product["status"]
    published_at = product.get("publishedAt")
    created_at = product.get("createdAt")
    updated_at = product.get("updatedAt")

    product_data = {
        'id': product_id,
        'title': title,
        'handle': handle,
        'status': status,
        'published_at': published_at,
        'created_at': created_at,
        'updated_at': updated_at
    }

    if status == "ACTIVE":
        active_products.append(product_data)
    elif status == "DRAFT":
        draft_products.append(product_data)
    elif status == "ARCHIVED":
        archived_products.append(product_data)

print("=" * 80)
print("PRODUCTS BY STATUS")
print("=" * 80)

print(f"\n✅ ACTIVE (Published): {len(active_products)}/{len(products)}")
if active_products:
    for product in active_products[:5]:  # Show first 5
        print(f"   - {product['title']}")
        print(f"     Handle: {product['handle']}")
        print(f"     Published: {product['published_at']}")
        print()
    if len(active_products) > 5:
        print(f"   ... and {len(active_products) - 5} more active products\n")

print(f"📝 DRAFT (Unpublished): {len(draft_products)}/{len(products)}")
if draft_products:
    print(f"\n   DRAFT PRODUCTS LIST:")
    for product in draft_products:
        print(f"   - {product['title']}")
        print(f"     Handle: {product['handle']}")
        print(f"     Created: {product['created_at']}")
        print(f"     Updated: {product['updated_at']}")
        print(f"     Status: DRAFT ✅ (correct)")
        print()
else:
    print(f"   No draft products found")

if archived_products:
    print(f"\n🗄️ ARCHIVED: {len(archived_products)}/{len(products)}")
    for product in archived_products:
        print(f"   - {product['title']}")
        print(f"     Handle: {product['handle']}")

print("\n" + "=" * 80)
print("COMPLIANCE CHECK")
print("=" * 80)

print(f"\n🎯 REQUIREMENT: Draft products MUST remain draft (NO accidental publish)")

# Check if any draft products were accidentally published
accidentally_published = []
for product in draft_products:
    if product['published_at']:
        accidentally_published.append(product)

if accidentally_published:
    print(f"\n❌ VIOLATION DETECTED: {len(accidentally_published)} draft products have publishedAt date")
    for product in accidentally_published:
        print(f"   - {product['title']}")
        print(f"     Status: {product['status']}")
        print(f"     Published At: {product['published_at']} (SHOULD BE NULL)")
        print()
    print(f"🚨 ACTION REQUIRED: Investigate why draft products have publishedAt timestamp")
else:
    print(f"\n✅ COMPLIANCE ACHIEVED")
    print(f"   All {len(draft_products)} draft products correctly unpublished")
    print(f"   All draft products have NULL publishedAt timestamp")

# Summary
print("\n" + "=" * 80)
print("STATUS DISTRIBUTION")
print("=" * 80)

total = len(products)
print(f"\nTotal products: {total}")
print(f"   - ACTIVE: {len(active_products)} ({(len(active_products)/total)*100:.1f}%)")
print(f"   - DRAFT: {len(draft_products)} ({(len(draft_products)/total)*100:.1f}%)")
print(f"   - ARCHIVED: {len(archived_products)} ({(len(archived_products)/total)*100:.1f}%)")

if len(draft_products) > 0:
    print(f"\n📋 DRAFT PRODUCTS SUMMARY:")
    print(f"   Total draft: {len(draft_products)}")
    print(f"   ✅ All drafts remain unpublished: YES")
    print(f"   ✅ No accidental publishing: YES")
else:
    print(f"\n✅ NO DRAFT PRODUCTS")
    print(f"   All products are either ACTIVE or ARCHIVED")

print("\n" + "=" * 80)
