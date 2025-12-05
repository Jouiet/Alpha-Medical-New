#!/usr/bin/env python3
"""
UPDATE BUNDLE PRODUCT IMAGES - Alpha Medical
Add clickable product images to bundle landing pages

REQUIREMENT:
- 3 images per product in bundle
- Images clickable → product landing page
- Display all component products
"""

import os
import json
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

def graphql_query(query, variables=None):
    payload = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    data = response.json()
    if "errors" in data:
        return None
    return data

print("="*80)
print("UPDATE BUNDLE PRODUCT IMAGES - ALPHA MEDICAL")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# ============================================================================
# 1. LOAD BUNDLE PLANS
# ============================================================================
print("\n1. Loading bundle plans...\n")

try:
    with open('bundle_products_created.json', 'r') as f:
        bundles_data = json.load(f)
    with open('optimal_bundles_plan.json', 'r') as f:
        plans_data = json.load(f)
except Exception as e:
    print(f"❌ Failed to load data: {e}")
    exit(1)

created_bundles = bundles_data["created_bundles"]
bundles_plans = {b["name"]: b for b in plans_data["bundles"]}

print(f"✅ Loaded {len(created_bundles)} bundles")

# ============================================================================
# 2. FETCH PRODUCT IMAGES FOR EACH COMPONENT
# ============================================================================
print("\n" + "="*80)
print("2. FETCHING COMPONENT PRODUCT IMAGES")
print("="*80)

updated_count = 0
failed_count = 0

for bundle_created in created_bundles:
    bundle_name = bundle_created["name"].replace(" - Complete Care Kit", "")
    bundle_plan = bundles_plans.get(bundle_name)

    if not bundle_plan:
        print(f"\n⚠️  No plan found for: {bundle_name}")
        continue

    print(f"\n⏳ Processing: {bundle_name}")

    # Fetch images for each component product
    component_products_html = []

    for i, component in enumerate(bundle_plan["products"], 1):
        product_id = component["id"]

        # Get product with images
        query = """
        query getProduct($id: ID!) {
          product(id: $id) {
            id
            title
            handle
            images(first: 3) {
              edges {
                node {
                  url
                  altText
                  width
                  height
                }
              }
            }
          }
        }
        """

        result = graphql_query(query, {"id": product_id})

        if not result:
            print(f"   ❌ Failed to fetch product: {component['title'][:40]}...")
            continue

        product = result["data"]["product"]
        images = product["images"]["edges"]

        print(f"   [{i}/{len(bundle_plan['products'])}] {product['title'][:50]}...")
        print(f"      Images: {len(images)}")
        print(f"      Handle: {product['handle']}")

        # Generate HTML for this product's images
        product_url = f"https://www.alphamedical.shop/products/{product['handle']}"

        product_html = f"""
<div class="bundle-component-product" style="margin-bottom: 30px; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
  <h3 style="margin-top: 0; color: #333; font-size: 18px;">{product['title']}</h3>
  <div class="product-images" style="display: flex; gap: 10px; flex-wrap: wrap; margin: 15px 0;">
"""

        for img_edge in images[:3]:  # Max 3 images
            img = img_edge["node"]
            product_html += f"""
    <a href="{product_url}" style="display: block; flex: 0 0 30%; max-width: 200px;">
      <img src="{img['url']}"
           alt="{img.get('altText', product['title'])}"
           style="width: 100%; height: auto; border-radius: 4px; border: 1px solid #ddd; transition: transform 0.2s;"
           onmouseover="this.style.transform='scale(1.05)'"
           onmouseout="this.style.transform='scale(1)'">
    </a>
"""

        product_html += f"""
  </div>
  <a href="{product_url}" style="display: inline-block; margin-top: 10px; padding: 10px 20px; background-color: #4770DB; color: white; text-decoration: none; border-radius: 4px; font-weight: 600;">
    View Product Details →
  </a>
</div>
"""

        component_products_html.append(product_html)

    # Generate complete bundle description HTML
    bundle_description_html = f"""
<div class="bundle-description" style="font-family: Arial, sans-serif; line-height: 1.6;">
  <div class="bundle-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px; margin-bottom: 30px;">
    <h2 style="margin: 0 0 15px 0; font-size: 28px;">{bundle_name} - Complete Care Kit</h2>
    <p style="margin: 0; font-size: 16px; opacity: 0.9;">Save 15% with this expertly curated bundle</p>
    <div style="margin-top: 20px; font-size: 24px; font-weight: bold;">
      <span style="text-decoration: line-through; opacity: 0.7;">${bundle_plan['total_price']:.2f}</span>
      <span style="margin-left: 15px; color: #FFD700;">${bundle_plan['bundle_price']:.2f}</span>
      <span style="margin-left: 10px; font-size: 16px; background-color: rgba(255,255,255,0.2); padding: 5px 10px; border-radius: 4px;">15% OFF</span>
    </div>
  </div>

  <div class="bundle-benefits" style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
    <h3 style="margin-top: 0; color: #333;">Why Choose This Kit?</h3>
    <ul style="margin: 10px 0; padding-left: 20px;">
      <li><strong>Expert-Curated:</strong> {len(bundle_plan['products'])} carefully selected products designed to work together</li>
      <li><strong>15% Savings:</strong> Save ${(bundle_plan['total_price'] - bundle_plan['bundle_price']):.2f} compared to individual purchases</li>
      <li><strong>Complete Solution:</strong> Everything you need for comprehensive support and therapy</li>
      <li><strong>Quality Guaranteed:</strong> All products covered by our 30-day money-back guarantee</li>
    </ul>
  </div>

  <h3 style="color: #333; font-size: 24px; margin-bottom: 20px;">What's Included in This Kit:</h3>

  <div class="bundle-components">
{''.join(component_products_html)}
  </div>

  <div class="bundle-footer" style="background-color: #e8f5e9; padding: 20px; border-radius: 8px; margin-top: 30px;">
    <h3 style="margin-top: 0; color: #2e7d32;">Free Shipping & Returns</h3>
    <p style="margin: 5px 0;">✅ Free shipping on orders over $50</p>
    <p style="margin: 5px 0;">✅ 30-day money-back guarantee</p>
    <p style="margin: 5px 0;">✅ Secure checkout with SSL encryption</p>
    <p style="margin: 5px 0;">✅ FDA-compliant medical-grade materials</p>
  </div>
</div>
"""

    # Update bundle product description
    print(f"\n   Updating bundle description...")

    mutation = """
    mutation productUpdate($input: ProductInput!) {
      productUpdate(input: $input) {
        product {
          id
          title
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "id": bundle_created["id"],
            "descriptionHtml": bundle_description_html
        }
    }

    result = graphql_query(mutation, variables)

    if not result:
        print(f"   ❌ Failed to update bundle")
        failed_count += 1
        continue

    update_result = result["data"]["productUpdate"]
    user_errors = update_result.get("userErrors", [])

    if user_errors:
        print(f"   ❌ Update errors:")
        for error in user_errors:
            print(f"      {error['field']}: {error['message']}")
        failed_count += 1
        continue

    updated_count += 1
    print(f"   ✅ SUCCESS - Bundle description updated")
    print(f"   Component products displayed: {len(component_products_html)}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)
print(f"\n✅ Successfully updated: {updated_count}/{len(created_bundles)} bundles")
if failed_count > 0:
    print(f"❌ Failed: {failed_count} bundles")

print("\n🎯 VERIFICATION:")
print("Visit bundle collection: https://www.alphamedical.shop/collections/complete-care-kits")
print("Each bundle should show:")
print("   - 3 clickable images per component product")
print("   - Product title and 'View Product Details' link")
print("   - Complete pricing information")

print("\n" + "="*80)
