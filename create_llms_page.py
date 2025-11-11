#!/usr/bin/env python3
"""
Create llms.txt page in Shopify
Makes Alpha Medical documentation accessible to AI models
"""

import os
import json
import requests

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

# Try .env.admin first, fallback to .env
try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except FileNotFoundError:
    SHOPIFY_TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')

if not SHOPIFY_TOKEN:
    print("❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found in .env.admin or environment")
    exit(1)

API_VERSION = "2024-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# Check if page already exists
check_query = """
{
  pages(first: 50) {
    edges {
      node {
        id
        title
        handle
        body
      }
    }
  }
}
"""

print("="*80)
print("CHECKING FOR EXISTING LLMS.TXT PAGE")
print("="*80)

response = requests.post(GRAPHQL_URL, json={"query": check_query}, headers=HEADERS)
data = response.json()

if "errors" in data:
    print("❌ GraphQL Errors:")
    for error in data["errors"]:
        print(f"   - {error.get('message', 'Unknown error')}")
    exit(1)

all_pages = data.get("data", {}).get("pages", {}).get("edges", [])
existing_pages = [edge for edge in all_pages if edge["node"]["handle"] in ["llms-txt", "llms"]]

if existing_pages:
    print(f"\n✅ Found {len(existing_pages)} existing llms.txt page(s):")
    for edge in existing_pages:
        page = edge["node"]
        print(f"   - ID: {page['id']}")
        print(f"     Title: {page['title']}")
        print(f"     Handle: {page['handle']}")
        print(f"     Body length: {len(page['body'])} chars")
    print("\n⚠️  Page already exists. Skipping creation.")
    print(f"   Access at: https://www.alphamedical.shop/pages/{existing_pages[0]['node']['handle']}")
    exit(0)

# Create new page
print("\n❌ No existing llms.txt page found. Creating new page...")

# Read template content for body preview
try:
    with open('templates/page.llms-txt.liquid', 'r') as f:
        template_content = f.read()
    print(f"   Template file: templates/page.llms-txt.liquid ({len(template_content)} chars)")
except FileNotFoundError:
    print("   ⚠️  Warning: templates/page.llms-txt.liquid not found")
    template_content = ""

create_mutation = """
mutation pageCreate($input: PageCreateInput!) {
  pageCreate(page: $input) {
    page {
      id
      title
      handle
      body
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
        "title": "llms.txt",
        "handle": "llms-txt",
        "body": "# Alpha Medical Care - LLM Documentation\n\nThis page provides documentation for AI language models about Alpha Medical Care.\n\n**Note:** This page uses a custom Liquid template (`page.llms-txt.liquid`) to render the full documentation."
    }
}

print("\nCreating page with:")
print(f"   Title: llms.txt")
print(f"   Handle: llms-txt")
print(f"   Template: page.llms-txt.liquid")

response = requests.post(GRAPHQL_URL, json={"query": create_mutation, "variables": variables}, headers=HEADERS)
data = response.json()

if "errors" in data:
    print("\n❌ GraphQL Errors:")
    for error in data["errors"]:
        print(f"   - {error.get('message', 'Unknown error')}")
    exit(1)

result = data.get("data", {}).get("pageCreate", {})
user_errors = result.get("userErrors", [])

if user_errors:
    print("\n❌ User Errors:")
    for error in user_errors:
        print(f"   - {error['field']}: {error['message']}")
    exit(1)

page = result.get("page")

if page:
    print("\n✅ SUCCESS - Page created!")
    print(f"   ID: {page['id']}")
    print(f"   Title: {page['title']}")
    print(f"   Handle: {page['handle']}")
    print(f"   URL: https://www.alphamedical.shop/pages/{page['handle']}")
    print(f"\n⚠️  IMPORTANT:")
    print(f"   1. The page will use template: page.llms-txt.liquid")
    print(f"   2. Push theme to Shopify: shopify theme push")
    print(f"   3. Verify template at: https://www.alphamedical.shop/pages/llms-txt")
else:
    print("\n❌ Failed to create page (no page object returned)")
    print(f"   Response: {json.dumps(data, indent=2)}")
    exit(1)

print("\n" + "="*80)
print("NEXT STEPS")
print("="*80)
print("1. Push theme to deploy template:")
print("   shopify theme push")
print("2. Update robots.txt reference (already points to /llms.txt)")
print("3. Add redirect /llms.txt → /pages/llms-txt in Shopify Navigation")
print("4. Verify page renders correctly at:")
print("   https://www.alphamedical.shop/pages/llms-txt")
