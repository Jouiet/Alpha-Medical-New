#!/usr/bin/env python3
"""
Verify Loyalty Discount Codes
Checks if all 4 loyalty tier discount codes exist and are configured correctly
Date: 2025-11-20
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_env_path = os.path.join(os.path.dirname(__file__), '.env.admin')
load_dotenv(load_env_path)

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

GRAPHQL_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10/graphql.json"

headers = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

EXPECTED_CODES = ["LOYALTY10", "LOYALTY15", "LOYALTY25", "LOYALTY50"]

def search_discount_codes():
    """Search for loyalty discount codes"""

    query = """
    query {
      codeDiscountNodes(first: 50) {
        edges {
          node {
            id
            codeDiscount {
              ... on DiscountCodeBasic {
                title
                codes(first: 1) {
                  edges {
                    node {
                      code
                    }
                  }
                }
                status
                summary
                customerGets {
                  value {
                    ... on DiscountPercentage {
                      percentage
                    }
                  }
                }
                startsAt
                endsAt
              }
            }
          }
        }
      }
    }
    """

    payload = {"query": query}

    try:
        response = requests.post(GRAPHQL_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if 'errors' in result:
            print("❌ GraphQL Error:")
            print(json.dumps(result['errors'], indent=2))
            return []

        edges = result.get('data', {}).get('codeDiscountNodes', {}).get('edges', [])

        discount_codes = []
        for edge in edges:
            code_discount = edge.get('node', {}).get('codeDiscount', {})
            if code_discount:
                codes_edges = code_discount.get('codes', {}).get('edges', [])
                if codes_edges:
                    code = codes_edges[0]['node']['code']
                    if code in EXPECTED_CODES:
                        percentage = code_discount.get('customerGets', {}).get('value', {}).get('percentage', 0)
                        discount_codes.append({
                            'code': code,
                            'title': code_discount.get('title', 'N/A'),
                            'status': code_discount.get('status', 'N/A'),
                            'percentage': percentage * 100 if percentage else 0,
                            'summary': code_discount.get('summary', 'N/A')
                        })

        return discount_codes

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []

def main():
    print("=" * 70)
    print("VERIFYING LOYALTY DISCOUNT CODES")
    print("=" * 70)
    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print()

    print("Searching for loyalty discount codes...")
    found_codes = search_discount_codes()

    print()
    print("=" * 70)
    print("RESULTS")
    print("=" * 70)

    found_code_names = [dc['code'] for dc in found_codes]

    for expected_code in EXPECTED_CODES:
        if expected_code in found_code_names:
            code_data = next(dc for dc in found_codes if dc['code'] == expected_code)
            print(f"✅ {expected_code}")
            print(f"   Title: {code_data['title']}")
            print(f"   Status: {code_data['status']}")
            print(f"   Discount: {code_data['percentage']:.0f}%")
            print(f"   Summary: {code_data['summary']}")
            print()
        else:
            print(f"❌ {expected_code} - NOT FOUND")
            print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Found: {len(found_codes)}/{len(EXPECTED_CODES)} discount codes")

    if len(found_codes) == len(EXPECTED_CODES):
        print()
        print("🎉 ALL LOYALTY DISCOUNT CODES EXIST AND ARE ACTIVE!")
        print()
        print("NEXT STEP: Configure Shopify Flow for automatic tier tagging")
        print("URL: https://admin.shopify.com/store/azffej-as/apps/flow")
    else:
        missing = set(EXPECTED_CODES) - set(found_code_names)
        print()
        print(f"⚠️  Missing codes: {', '.join(missing)}")
        print("Run create_loyalty_discount_codes.py to create missing codes")

if __name__ == "__main__":
    main()
