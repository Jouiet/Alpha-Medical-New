#!/usr/bin/env python3
"""
Loyalty System Setup - Create Customer Metafield Definitions
One-time setup script to define loyalty metafields structure
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.admin')

SHOPIFY_STORE = os.getenv('SHOPIFY_STORE_DOMAIN')
ADMIN_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2024-10'

HEADERS = {
    'X-Shopify-Access-Token': ADMIN_TOKEN,
    'Content-Type': 'application/json'
}

BASE_URL = f'https://{SHOPIFY_STORE}/admin/api/{API_VERSION}'


def create_metafield_definition(namespace, key, name, description, field_type, validations=None):
    """Create a metafield definition via GraphQL Admin API"""

    mutation = """
    mutation CreateMetafieldDefinition($definition: MetafieldDefinitionInput!) {
      metafieldDefinitionCreate(definition: $definition) {
        createdDefinition {
          id
          name
          namespace
          key
          type {
            name
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    definition_input = {
        "name": name,
        "namespace": namespace,
        "key": key,
        "description": description,
        "type": field_type,
        "ownerType": "CUSTOMER"
    }

    if validations:
        definition_input["validations"] = validations

    variables = {
        "definition": definition_input
    }

    response = requests.post(
        f'{BASE_URL}/graphql.json',
        headers=HEADERS,
        json={'query': mutation, 'variables': variables}
    )

    result = response.json()

    if 'errors' in result:
        print(f"❌ GraphQL Error for {namespace}.{key}:")
        print(json.dumps(result['errors'], indent=2))
        return False

    data = result.get('data', {}).get('metafieldDefinitionCreate', {})

    if data.get('userErrors'):
        print(f"❌ User Error for {namespace}.{key}:")
        print(json.dumps(data['userErrors'], indent=2))
        return False

    if data.get('createdDefinition'):
        created = data['createdDefinition']
        print(f"✅ Created: {created['namespace']}.{created['key']} ({created['type']['name']})")
        return True

    print(f"⚠️  Unknown response for {namespace}.{key}:")
    print(json.dumps(data, indent=2))
    return False


def setup_loyalty_metafields():
    """Create all loyalty metafield definitions"""

    print("=" * 60)
    print("LOYALTY SYSTEM METAFIELD SETUP")
    print("=" * 60)
    print(f"Store: {SHOPIFY_STORE}")
    print(f"API Version: {API_VERSION}")
    print()

    metafields = [
        {
            "namespace": "loyalty",
            "key": "points",
            "name": "Loyalty Points Balance",
            "description": "Current loyalty points balance",
            "field_type": "number_integer",
            "validations": [{"name": "min", "value": "0"}]
        },
        {
            "namespace": "loyalty",
            "key": "tier",
            "name": "Loyalty Tier",
            "description": "Customer loyalty tier: bronze, silver, or gold",
            "field_type": "single_line_text_field",
            "validations": None
        },
        {
            "namespace": "loyalty",
            "key": "history",
            "name": "Loyalty Transaction History",
            "description": "JSON array of all loyalty transactions",
            "field_type": "json",
            "validations": None
        },
        {
            "namespace": "loyalty",
            "key": "signup_bonus_claimed",
            "name": "Signup Bonus Claimed",
            "description": "Has customer claimed the 50-point signup bonus",
            "field_type": "boolean",
            "validations": None
        },
        {
            "namespace": "loyalty",
            "key": "lifetime_points_earned",
            "name": "Lifetime Points Earned",
            "description": "Total points earned (including redeemed)",
            "field_type": "number_integer",
            "validations": [{"name": "min", "value": "0"}]
        },
        {
            "namespace": "loyalty",
            "key": "lifetime_points_redeemed",
            "name": "Lifetime Points Redeemed",
            "description": "Total points redeemed for discounts",
            "field_type": "number_integer",
            "validations": [{"name": "min", "value": "0"}]
        }
    ]

    results = {
        'success': 0,
        'failed': 0,
        'total': len(metafields)
    }

    for mf in metafields:
        success = create_metafield_definition(
            namespace=mf['namespace'],
            key=mf['key'],
            name=mf['name'],
            description=mf['description'],
            field_type=mf['field_type'],
            validations=mf.get('validations')
        )

        if success:
            results['success'] += 1
        else:
            results['failed'] += 1

    print()
    print("=" * 60)
    print("SETUP COMPLETE")
    print("=" * 60)
    print(f"✅ Success: {results['success']}/{results['total']}")
    print(f"❌ Failed: {results['failed']}/{results['total']}")
    print()

    if results['failed'] > 0:
        print("⚠️  Some metafield definitions failed to create.")
        print("This may be normal if they already exist.")
        print("Check errors above for details.")
    else:
        print("🎉 All metafield definitions created successfully!")

    return results['failed'] == 0


def verify_metafields():
    """Verify metafield definitions were created"""

    print("\n" + "=" * 60)
    print("VERIFICATION - Listing Customer Metafield Definitions")
    print("=" * 60)

    query = """
    {
      metafieldDefinitions(first: 20, ownerType: CUSTOMER) {
        edges {
          node {
            id
            name
            namespace
            key
            type {
              name
            }
            description
          }
        }
      }
    }
    """

    response = requests.post(
        f'{BASE_URL}/graphql.json',
        headers=HEADERS,
        json={'query': query}
    )

    result = response.json()

    if 'errors' in result:
        print("❌ GraphQL Error:")
        print(json.dumps(result['errors'], indent=2))
        return

    definitions = result.get('data', {}).get('metafieldDefinitions', {}).get('edges', [])

    loyalty_defs = [d for d in definitions if d['node']['namespace'] == 'loyalty']

    if not loyalty_defs:
        print("⚠️  No loyalty metafield definitions found!")
        return

    print(f"\n✅ Found {len(loyalty_defs)} loyalty metafield definitions:\n")

    for edge in loyalty_defs:
        node = edge['node']
        print(f"  • {node['namespace']}.{node['key']}")
        print(f"    Name: {node['name']}")
        print(f"    Type: {node['type']['name']}")
        print(f"    Description: {node['description']}")
        print()


if __name__ == '__main__':
    # Create metafield definitions
    success = setup_loyalty_metafields()

    # Verify they were created
    verify_metafields()

    if success:
        print("\n✅ Setup complete! Ready to create loyalty_manager.py")
    else:
        print("\n⚠️  Setup completed with some errors. Check output above.")
