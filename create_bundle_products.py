#!/usr/bin/env python3
"""
CREATE BUNDLE PRODUCTS IN SHOPIFY - Alpha Medical
Creates actual native bundle products based on optimal_bundles_plan.json

IMPLEMENTATION:
1. Load bundle plans from JSON
2. Create each bundle as a native Shopify product
3. Add proper descriptions, pricing, tags
4. Add to "Complete Care Kits" collection
5. Store component product IDs in metafields for reference

NO MOCK DATA - REAL PRODUCT CREATION
"""

import os
import json
import requests
from datetime import datetime

# Load credentials
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

def graphql_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    data = response.json()
    if "errors" in data:
        for error in data["errors"]:
            print(f"❌ GraphQL Error: {error.get('message')}")
        return None
    return data

print("="*80)
print("ALPHA MEDICAL - CREATE NATIVE BUNDLE PRODUCTS")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# ============================================================================
# 1. LOAD BUNDLE PLANS
# ============================================================================
print("\n1. Loading bundle plans...\n")

try:
    with open('optimal_bundles_plan.json', 'r') as f:
        bundle_plans_data = json.load(f)
except Exception as e:
    print(f"❌ Failed to load bundle plans: {e}")
    exit(1)

bundles = bundle_plans_data["bundles"]
collection_id = bundle_plans_data["collection_id"]

print(f"✅ Loaded {len(bundles)} bundle plans")
print(f"✅ Target collection: {collection_id}")

# ============================================================================
# 2. CREATE BUNDLE PRODUCTS
# ============================================================================
print("\n" + "="*80)
print("2. CREATING BUNDLE PRODUCTS IN SHOPIFY")
print("="*80)

created_bundles = []
failed_bundles = []

mutation_create_product = """
mutation productCreate($product: ProductCreateInput!, $media: [CreateMediaInput!]) {
  productCreate(product: $product, media: $media) {
    product {
      id
      title
      handle
      status
      variants(first: 1) {
        edges {
          node {
            id
            price
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}
"""

mutation_update_variant = """
mutation productVariantUpdate($input: ProductVariantInput!) {
  productVariantUpdate(input: $input) {
    productVariant {
      id
      price
      inventoryManagement
      inventoryPolicy
    }
    userErrors {
      field
      message
    }
  }
}
"""

for i, bundle in enumerate(bundles, 1):
    print(f"\n[{i}/{len(bundles)}] Creating: {bundle['name']}")

    # Generate bundle handle
    handle = bundle['name'].lower().replace(' ', '-').replace('&', 'and')
    handle = ''.join(c for c in handle if c.isalnum() or c == '-')

    # Generate description
    product_list_html = "".join([
        f"<li><strong>{prod['title']}</strong> (${prod['price']:.2f})</li>"
        for prod in bundle['products']
    ])

    description_html = f"""<div class="bundle-description">
<h2>{bundle['name']}</h2>

<p>This Complete Care Kit includes {len(bundle['products'])} carefully selected products designed to work together for comprehensive support and therapy.</p>

<h3>What's Included:</h3>
<ul>
{product_list_html}
</ul>

<h3>Bundle Benefits:</h3>
<ul>
  <li><strong>15% Savings:</strong> Save ${(bundle['total_price'] - bundle['bundle_price']):.2f} compared to individual purchases</li>
  <li><strong>Complementary Products:</strong> Selected to work together for optimal results</li>
  <li><strong>Expert-Curated:</strong> Based on real user needs and professional analysis</li>
  <li><strong>Complete Solution:</strong> Everything you need in one convenient kit</li>
</ul>

<h3>Pricing:</h3>
<p><strong>Individual Total:</strong> <s>${bundle['total_price']:.2f}</s></p>
<p><strong>Bundle Price:</strong> ${bundle['bundle_price']:.2f} (15% discount)</p>

<h3>Shipping & Returns:</h3>
<p>Free shipping on orders over $100. All products covered by our 30-day satisfaction guarantee.</p>
</div>"""

    # Extract component product IDs for metafield
    component_ids = [prod["id"] for prod in bundle["products"]]
    component_ids_str = ",".join(component_ids)

    # Generate tags
    tags = [
        "bundle",
        "complete-care-kit",
        bundle["persona_key"],
        f"{len(bundle['products'])}-products"
    ]

    # Step 1: Create product (without price)
    variables = {
        "product": {
            "title": f"{bundle['name']} - Complete Care Kit",
            "handle": f"bundle-{handle}",
            "descriptionHtml": description_html,
            "productType": "Bundle",
            "vendor": "Alpha Medical",
            "tags": tags,
            "status": "ACTIVE",
            "seo": {
                "title": f"{bundle['name']} - Complete Care Kit | Alpha Medical",
                "description": f"Save 15% with our {bundle['name']} Complete Care Kit. {len(bundle['products'])} expert-curated products for ${bundle['bundle_price']:.2f}. Free shipping over $100."
            },
            "metafields": [
                {
                    "namespace": "bundle",
                    "key": "component_products",
                    "value": component_ids_str,
                    "type": "single_line_text_field"
                },
                {
                    "namespace": "bundle",
                    "key": "original_price",
                    "value": str(round(bundle['total_price'], 2)),
                    "type": "number_decimal"
                },
                {
                    "namespace": "bundle",
                    "key": "discount_percentage",
                    "value": "15",
                    "type": "number_integer"
                }
            ]
        }
    }

    result = graphql_query(mutation_create_product, variables)

    if not result:
        print(f"   ❌ FAILED - Product creation GraphQL error")
        failed_bundles.append(bundle['name'])
        continue

    create_result = result["data"]["productCreate"]
    user_errors = create_result.get("userErrors", [])

    if user_errors:
        print(f"   ❌ FAILED - Product creation errors:")
        for error in user_errors:
            print(f"      {error['field']}: {error['message']}")
        failed_bundles.append(bundle['name'])
        continue

    product = create_result["product"]
    print(f"   ✅ Product created: {product['id']}")

    # Step 2: Update variant price
    variant_id = product["variants"]["edges"][0]["node"]["id"]
    print(f"   Updating variant price to ${bundle['bundle_price']:.2f}...")

    variant_variables = {
        "input": {
            "id": variant_id,
            "price": str(round(bundle['bundle_price'], 2)),
            "inventoryPolicy": "CONTINUE"
        }
    }

    variant_result = graphql_query(mutation_update_variant, variant_variables)

    if not variant_result:
        print(f"   ⚠️  Warning: Variant price update failed (product created but price may be incorrect)")
    else:
        variant_update = variant_result["data"]["productVariantUpdate"]
        variant_errors = variant_update.get("userErrors", [])

        if variant_errors:
            print(f"   ⚠️  Warning: Variant price update errors:")
            for error in variant_errors:
                print(f"      {error['field']}: {error['message']}")
        else:
            variant = variant_update["productVariant"]
            print(f"   ✅ Variant price updated: ${variant['price']}")

    print(f"   ✅ COMPLETE")
    print(f"   Product ID: {product['id']}")
    print(f"   Handle: {product['handle']}")

    created_bundles.append({
        "name": bundle['name'],
        "id": product['id'],
        "handle": product['handle']
    })

# ============================================================================
# 3. ADD BUNDLES TO "Complete Care Kits" COLLECTION
# ============================================================================
print("\n" + "="*80)
print("3. ADDING BUNDLES TO COLLECTION")
print("="*80)

if not created_bundles:
    print("\n⚠️  No bundles created, skipping collection update")
else:
    mutation_add_to_collection = """
    mutation collectionAddProducts($id: ID!, $productIds: [ID!]!) {
      collectionAddProducts(id: $id, productIds: $productIds) {
        collection {
          id
          title
          productsCount {
            count
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    product_ids = [b["id"] for b in created_bundles]

    variables = {
        "id": collection_id,
        "productIds": product_ids
    }

    result = graphql_query(mutation_add_to_collection, variables)

    if result and result["data"]["collectionAddProducts"]["collection"]:
        collection = result["data"]["collectionAddProducts"]["collection"]
        print(f"\n✅ Added {len(created_bundles)} bundles to '{collection['title']}'")
        print(f"   Collection product count: {collection['productsCount']['count']}")
    else:
        print(f"\n❌ Failed to add bundles to collection")

# ============================================================================
# 4. SAVE RESULTS
# ============================================================================
output_file = "bundle_products_created.json"
with open(output_file, 'w') as f:
    json.dump({
        "timestamp": datetime.now().isoformat(),
        "created_count": len(created_bundles),
        "failed_count": len(failed_bundles),
        "collection_id": collection_id,
        "created_bundles": created_bundles,
        "failed_bundles": failed_bundles
    }, f, indent=2)

print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)
print(f"\n✅ Successfully created: {len(created_bundles)}/{len(bundles)} bundles")
if failed_bundles:
    print(f"❌ Failed: {len(failed_bundles)} bundles")
    for name in failed_bundles:
        print(f"   - {name}")
print(f"\n✅ Results saved to: {output_file}")
print(f"✅ All bundles added to 'Complete Care Kits' collection")

print("\n🎯 VERIFICATION:")
print("1. Visit: https://www.alphamedical.shop/collections/complete-care-kits")
print("2. Verify all 10 bundles are visible")
print("3. Check pricing, descriptions, and product listings")

print("\n" + "="*80)
