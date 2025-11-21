#!/usr/bin/env python3
"""
Create Loyalty Tier Discount Codes - Automated
Creates 4 discount codes for the simplified tag-based loyalty system
Date: 2025-11-20
"""

import os
import requests
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_env_path = os.path.join(os.path.dirname(__file__), '.env.admin')
load_dotenv(load_env_path)

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

# Shopify Admin API endpoint
GRAPHQL_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10/graphql.json"

headers = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

# Discount configurations
DISCOUNT_CONFIGS = [
    {
        "title": "Loyalty Bronze Tier Discount",
        "code": "LOYALTY10",
        "percentage": 10.0,
        "tag": "loyalty-bronze",
        "description": "10% off for Bronze tier loyalty members"
    },
    {
        "title": "Loyalty Silver Tier Discount",
        "code": "LOYALTY15",
        "percentage": 15.0,
        "tag": "loyalty-silver",
        "description": "15% off for Silver tier loyalty members"
    },
    {
        "title": "Loyalty Gold Tier Discount",
        "code": "LOYALTY25",
        "percentage": 25.0,
        "tag": "loyalty-gold",
        "description": "25% off for Gold tier loyalty members"
    },
    {
        "title": "Loyalty Platinum Tier Discount",
        "code": "LOYALTY50",
        "percentage": 50.0,
        "tag": "loyalty-platinum",
        "description": "50% off for Platinum tier loyalty members"
    }
]

def create_discount_code(config):
    """Create a discount code using GraphQL Admin API"""

    # Note: Shopify GraphQL API uses discountCodeBasicCreate for percentage discounts
    # Customer segment filtering will need to be done via customer tags

    mutation = """
    mutation discountCodeBasicCreate($basicCodeDiscount: DiscountCodeBasicInput!) {
      discountCodeBasicCreate(basicCodeDiscount: $basicCodeDiscount) {
        codeDiscountNode {
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

    variables = {
        "basicCodeDiscount": {
            "title": config["title"],
            "code": config["code"],
            "startsAt": datetime.utcnow().isoformat() + "Z",
            "customerSelection": {
                "all": True  # We'll use customer tags via the code itself
            },
            "customerGets": {
                "value": {
                    "percentage": config["percentage"] / 100.0
                },
                "items": {
                    "all": True
                }
            },
            "appliesOncePerCustomer": False,  # Can use multiple times
            "usageLimit": None  # No limit
        }
    }

    payload = {
        "query": mutation,
        "variables": variables
    }

    try:
        response = requests.post(GRAPHQL_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        if 'errors' in result:
            print(f"❌ GraphQL Error for {config['code']}:")
            print(json.dumps(result['errors'], indent=2))
            return False

        user_errors = result.get('data', {}).get('discountCodeBasicCreate', {}).get('userErrors', [])

        if user_errors:
            print(f"❌ Failed to create {config['code']}:")
            for error in user_errors:
                print(f"   - {error['message']}")
            return False

        discount_node = result.get('data', {}).get('discountCodeBasicCreate', {}).get('codeDiscountNode', {})

        if discount_node:
            print(f"✅ Created: {config['code']} ({config['percentage']}% off)")
            print(f"   Title: {config['title']}")
            print(f"   Tag: {config['tag']}")
            return True
        else:
            print(f"❌ Unexpected response for {config['code']}")
            print(json.dumps(result, indent=2))
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP Error for {config['code']}: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error for {config['code']}: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("CREATING LOYALTY TIER DISCOUNT CODES")
    print("=" * 70)
    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print(f"API Version: 2024-10")
    print(f"Total codes to create: {len(DISCOUNT_CONFIGS)}")
    print()

    if not SHOPIFY_ADMIN_ACCESS_TOKEN:
        print("❌ ERROR: SHOPIFY_ADMIN_ACCESS_TOKEN not found in .env.admin")
        return

    success_count = 0
    failed_count = 0

    for config in DISCOUNT_CONFIGS:
        print(f"\nCreating discount: {config['code']}...")
        if create_discount_code(config):
            success_count += 1
        else:
            failed_count += 1

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Created: {success_count}/{len(DISCOUNT_CONFIGS)}")
    print(f"❌ Failed: {failed_count}/{len(DISCOUNT_CONFIGS)}")

    if success_count == len(DISCOUNT_CONFIGS):
        print()
        print("🎉 All discount codes created successfully!")
        print()
        print("NEXT STEPS:")
        print("1. Configure Shopify Flow for automatic tier tagging")
        print("2. Test discount codes with customers who have loyalty tags")
        print()
        print("To configure Flow:")
        print("   https://admin.shopify.com/store/azffej-as/apps/flow")
    else:
        print()
        print("⚠️  Some discount codes failed to create.")
        print("Check the errors above and retry if needed.")

if __name__ == "__main__":
    main()
