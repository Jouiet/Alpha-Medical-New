#!/usr/bin/env python3
"""
Alpha Medical Store - Factual Audit Script
Verifies current store status via Shopify Admin API

Usage: python3 audit_store_status.py
"""

import os
import json
import requests
from datetime import datetime

# Load credentials from .env.admin
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

# Load token from .env.admin
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
    if not SHOPIFY_TOKEN:
        raise ValueError("SHOPIFY_ADMIN_ACCESS_TOKEN not found in .env.admin")
except FileNotFoundError:
    print("❌ .env.admin file not found")
    exit(1)
except Exception as e:
    print(f"❌ Error loading credentials: {e}")
    exit(1)

API_VERSION = "2025-10"

GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query):
    """Execute GraphQL query"""
    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ GraphQL Error {response.status_code}: {response.text[:200]}")
        return None

    data = response.json()

    # Check for GraphQL errors
    if "errors" in data:
        print(f"❌ GraphQL Errors:")
        for error in data["errors"]:
            print(f"   - {error.get('message', 'Unknown error')}")
        return None

    return data

def audit_collections():
    """Audit all collections - descriptions, product counts"""
    print("\n" + "="*80)
    print("COLLECTIONS AUDIT")
    print("="*80)

    query = """
    {
      collections(first: 20) {
        edges {
          node {
            id
            title
            handle
            description
            descriptionHtml
            productsCount {
              count
            }
          }
        }
      }
    }
    """

    result = graphql_query(query)
    if not result or "data" not in result:
        print("❌ Failed to fetch collections")
        return []

    collections = result["data"]["collections"]["edges"]

    print(f"\nTotal Collections: {len(collections)}")
    print("-" * 80)

    empty_desc = []

    for edge in collections:
        col = edge["node"]
        title = col["title"]
        handle = col["handle"]
        desc = col["description"]
        prod_count = col["productsCount"]["count"]

        desc_status = "✅ OK" if desc and len(desc) > 50 else "❌ EMPTY" if not desc or len(desc) < 10 else "⚠️  SHORT"

        if desc_status in ["❌ EMPTY", "⚠️  SHORT"]:
            empty_desc.append(handle)

        print(f"{title:30} | {handle:25} | {prod_count:3} products | {desc_status:10} | {len(desc) if desc else 0:4} chars")

    print("-" * 80)
    print(f"✅ Collections with descriptions: {len(collections) - len(empty_desc)}/{len(collections)}")
    print(f"❌ Collections needing descriptions: {len(empty_desc)}/{len(collections)}")

    if empty_desc:
        print(f"\nCollections to fix: {', '.join(empty_desc)}")

    return collections

def audit_products_metafields(sample_size=10):
    """Audit product metafields - check for SEO, custom fields"""
    print("\n" + "="*80)
    print("PRODUCTS METAFIELDS AUDIT")
    print("="*80)

    query = """
    {
      products(first: """ + str(sample_size) + """) {
        edges {
          node {
            id
            title
            handle
            status
            metafields(first: 20) {
              edges {
                node {
                  namespace
                  key
                  value
                  type
                }
              }
            }
          }
        }
      }
    }
    """

    result = graphql_query(query)
    if not result or "data" not in result:
        print("❌ Failed to fetch products")
        return

    products = result["data"]["products"]["edges"]

    print(f"\nSampling {len(products)} products for metafields audit")
    print("-" * 80)

    total_metafields = 0
    products_with_meta = 0

    for edge in products:
        prod = edge["node"]
        metafields = prod["metafields"]["edges"]

        if metafields:
            products_with_meta += 1
            total_metafields += len(metafields)

            print(f"\n{prod['title'][:50]:50} | {prod['status']:8} | {len(metafields):2} metafields")

            for mf_edge in metafields:
                mf = mf_edge["node"]
                value_preview = str(mf["value"])[:60]
                print(f"  - {mf['namespace']}.{mf['key']:30} | {mf['type']:15} | {value_preview}")
        else:
            print(f"\n{prod['title'][:50]:50} | {prod['status']:8} | 0 metafields ❌")

    print("-" * 80)
    print(f"✅ Products with metafields: {products_with_meta}/{len(products)}")
    print(f"📊 Total metafields: {total_metafields}")
    print(f"📊 Average per product: {total_metafields / len(products):.1f}")

def audit_bundle_deals():
    """Audit Bundle Deals collection specifically"""
    print("\n" + "="*80)
    print("BUNDLE DEALS COLLECTION AUDIT")
    print("="*80)

    query = """
    {
      collectionByHandle(handle: "bundle-deals") {
        id
        title
        handle
        description
        productsCount {
          count
        }
        products(first: 10) {
          edges {
            node {
              id
              title
              handle
            }
          }
        }
      }
    }
    """

    result = graphql_query(query)
    if not result or "data" not in result or not result["data"]["collectionByHandle"]:
        print("❌ Bundle Deals collection not found")
        return

    col = result["data"]["collectionByHandle"]

    print(f"\nCollection: {col['title']}")
    print(f"Handle: {col['handle']}")
    print(f"Products Count: {col['productsCount']['count']}")
    print(f"Description: {len(col['description']) if col['description'] else 0} chars")

    if col['productsCount']['count'] == 0:
        print("\n❌ CRITICAL: Bundle Deals has 0 products!")
        print("   → Requires Bundler app configuration (manual UI)")
    else:
        print(f"\n✅ Bundle Deals has {col['productsCount']['count']} products:")
        for edge in col["products"]["edges"]:
            prod = edge["node"]
            print(f"   - {prod['title']}")

def main():
    print("="*80)
    print("ALPHA MEDICAL STORE - FACTUAL AUDIT")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Store: {SHOPIFY_DOMAIN}")
    print("="*80)

    # Audit collections
    collections = audit_collections()

    # Audit products metafields (sample)
    audit_products_metafields(sample_size=10)

    # Audit Bundle Deals specifically
    audit_bundle_deals()

    print("\n" + "="*80)
    print("AUDIT COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
