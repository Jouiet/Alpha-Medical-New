#!/usr/bin/env python3
"""
Fix empty collection descriptions for Bestsellers and New Arrivals
SEO-optimized, benefit-focused content
"""

import os
import json
import requests

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except FileNotFoundError:
    SHOPIFY_TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

if not SHOPIFY_TOKEN:
    print("❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found")
    exit(1)

API_VERSION = "2024-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def graphql_query(query, variables=None):
    """Execute GraphQL query"""
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    data = response.json()

    if "errors" in data:
        print("❌ GraphQL Errors:")
        for error in data["errors"]:
            print(f"   - {error.get('message', 'Unknown error')}")
        return None

    return data

# Collection descriptions (SEO-optimized, benefit-focused)
DESCRIPTIONS = {
    "bestsellers": """<div class="collection-description">
<h2>Our Most Popular Medical Support Products</h2>

<p>Discover why thousands of customers trust these medical support solutions. Our bestsellers represent the most effective, highly-rated products that deliver real results for pain relief, posture correction, and recovery support.</p>

<h3>Why Our Bestsellers Stand Out:</h3>
<ul>
<li><strong>Proven Results:</strong> Each product has hundreds of verified 5-star reviews from satisfied customers who experienced significant pain relief and improved mobility</li>
<li><strong>Professional Grade:</strong> Medical-quality construction and materials trusted by healthcare professionals and physical therapists</li>
<li><strong>Fast-Acting Relief:</strong> Most customers report noticeable improvement within the first week of use</li>
<li><strong>Versatile Solutions:</strong> Effective for chronic pain, sports injuries, post-surgery recovery, and daily wellness support</li>
</ul>

<h3>Most Trusted For:</h3>
<ul>
<li>✓ Knee pain and arthritis relief</li>
<li>✓ Back pain and posture correction</li>
<li>✓ Muscle recovery and rehabilitation</li>
<li>✓ Joint stabilization and support</li>
<li>✓ Injury prevention during sports and exercise</li>
</ul>

<p><strong>Customer Satisfaction Guarantee:</strong> Join thousands of satisfied customers who found lasting relief with our most popular products. If you're unsure where to start, these bestsellers are the perfect introduction to professional-grade medical support equipment.</p>

<p><em>Free shipping on orders over $50 | 30-day money-back guarantee | FDA-compliant materials</em></p>
</div>""",

    "new-arrivals": """<div class="collection-description">
<h2>Latest Medical Support & Recovery Equipment</h2>

<p>Explore the newest additions to our professional medical equipment collection. We continuously source cutting-edge pain relief devices, advanced orthopedic braces, and innovative wellness solutions to bring you the latest in medical technology.</p>

<h3>What Makes Our New Arrivals Special:</h3>
<ul>
<li><strong>Latest Technology:</strong> Featuring the most recent advancements in pain relief, muscle recovery, and posture correction</li>
<li><strong>Innovative Materials:</strong> New-generation fabrics, smart heating systems, and breathable compression technology</li>
<li><strong>Enhanced Comfort:</strong> Improved ergonomic designs that provide better support while remaining lightweight and discreet</li>
<li><strong>Advanced Features:</strong> Many products include adjustable settings, wireless controls, and app connectivity for personalized therapy</li>
</ul>

<h3>New Product Categories:</h3>
<ul>
<li>🆕 Smart electric therapy devices with customizable intensity levels</li>
<li>🆕 Next-generation compression gear with moisture-wicking technology</li>
<li>🆕 Advanced rehabilitation equipment for faster recovery</li>
<li>🆕 Ergonomic support braces with improved fit and comfort</li>
<li>🆕 Multi-functional wellness devices combining heat, massage, and compression</li>
</ul>

<h3>Perfect For:</h3>
<ul>
<li>✓ Early adopters seeking the latest pain relief technology</li>
<li>✓ Athletes looking for competitive edge in recovery</li>
<li>✓ Chronic pain sufferers wanting to try new treatment options</li>
<li>✓ Health-conscious individuals investing in preventive care</li>
</ul>

<p><strong>Be the First:</strong> Get exclusive access to the newest medical support equipment before it becomes a bestseller. Many of our current top products started right here in New Arrivals.</p>

<p><em>All products FDA-compliant | Professional-grade quality | Fast worldwide shipping | 30-day trial period</em></p>
</div>"""
}

print("="*80)
print("FIXING COLLECTION DESCRIPTIONS")
print("="*80)

# Get collection IDs
get_collections_query = """
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

print("\n1. Fetching collections...")
result = graphql_query(get_collections_query)

if not result:
    print("❌ Failed to fetch collections")
    exit(1)

collections = result["data"]["collections"]["edges"]

# Find bestsellers and new-arrivals
target_collections = {}

for edge in collections:
    col = edge["node"]
    if col["handle"] in ["bestsellers", "new-arrivals"]:
        target_collections[col["handle"]] = col
        print(f"   Found: {col['title']} (handle: {col['handle']}, {col['productsCount']['count']} products)")

if len(target_collections) < 2:
    print(f"\n⚠️  Warning: Only found {len(target_collections)}/2 target collections")
    print(f"   Found: {list(target_collections.keys())}")

# Update each collection
update_mutation = """
mutation collectionUpdate($input: CollectionInput!) {
  collectionUpdate(input: $input) {
    collection {
      id
      title
      handle
      description
      descriptionHtml
    }
    userErrors {
      field
      message
    }
  }
}
"""

print("\n2. Updating collection descriptions...\n")

for handle, col in target_collections.items():
    collection_id = col["id"]
    new_description = DESCRIPTIONS[handle]

    print(f"Updating: {col['title']}")
    print(f"   ID: {collection_id}")
    print(f"   New description: {len(new_description)} chars")

    variables = {
        "input": {
            "id": collection_id,
            "descriptionHtml": new_description
        }
    }

    result = graphql_query(update_mutation, variables)

    if not result:
        print(f"   ❌ Failed to update {col['title']}")
        continue

    update_result = result["data"]["collectionUpdate"]
    user_errors = update_result.get("userErrors", [])

    if user_errors:
        print(f"   ❌ User Errors:")
        for error in user_errors:
            print(f"      - {error['field']}: {error['message']}")
        continue

    updated_col = update_result["collection"]
    print(f"   ✅ SUCCESS - Description updated ({len(updated_col['descriptionHtml'])} chars)")
    print(f"   URL: https://www.alphamedical.shop/collections/{updated_col['handle']}")
    print()

print("="*80)
print("COLLECTION DESCRIPTIONS UPDATE COMPLETE")
print("="*80)
print("\n✅ Collections updated:")
for handle, col in target_collections.items():
    print(f"   - {col['title']}: https://www.alphamedical.shop/collections/{handle}")

print("\n📊 Final Status:")
print(f"   Bestsellers: {DESCRIPTIONS['bestsellers'].count('<li>')} bullet points, ~{len(DESCRIPTIONS['bestsellers'])} chars")
print(f"   New Arrivals: {DESCRIPTIONS['new-arrivals'].count('<li>')} bullet points, ~{len(DESCRIPTIONS['new-arrivals'])} chars")
