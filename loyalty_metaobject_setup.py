#!/usr/bin/env python3
"""
Loyalty System - Metaobjects Setup (Workaround for Customer API restriction)
Creates metaobject definition to store loyalty data indexed by email
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE = os.getenv('SHOPIFY_STORE_DOMAIN')
ADMIN_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2024-10'

HEADERS = {
    'X-Shopify-Access-Token': ADMIN_TOKEN,
    'Content-Type': 'application/json'
}

BASE_URL = f'https://{SHOPIFY_STORE}/admin/api/{API_VERSION}'


def create_loyalty_metaobject_definition():
    """Create metaobject definition for loyalty accounts"""

    mutation = """
    mutation CreateMetaobjectDefinition($definition: MetaobjectDefinitionCreateInput!) {
      metaobjectDefinitionCreate(definition: $definition) {
        metaobjectDefinition {
          id
          name
          type
          fieldDefinitions {
            key
            name
            type {
              name
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

    definition_input = {
        "name": "Loyalty Account",
        "type": "loyalty_account",
        "fieldDefinitions": [
            {
                "name": "Email",
                "key": "email",
                "type": "single_line_text_field",
                "required": True,
                "validations": [
                    {"name": "unique", "value": "true"}
                ]
            },
            {
                "name": "Customer ID",
                "key": "customer_id",
                "type": "single_line_text_field",
                "required": False
            },
            {
                "name": "Points",
                "key": "points",
                "type": "number_integer",
                "required": True,
                "validations": [
                    {"name": "min", "value": "0"}
                ]
            },
            {
                "name": "Tier",
                "key": "tier",
                "type": "single_line_text_field",
                "required": True
            },
            {
                "name": "History",
                "key": "history",
                "type": "json",
                "required": True
            },
            {
                "name": "Signup Bonus Claimed",
                "key": "signup_bonus_claimed",
                "type": "boolean",
                "required": True
            },
            {
                "name": "Lifetime Earned",
                "key": "lifetime_earned",
                "type": "number_integer",
                "required": True,
                "validations": [
                    {"name": "min", "value": "0"}
                ]
            },
            {
                "name": "Lifetime Redeemed",
                "key": "lifetime_redeemed",
                "type": "number_integer",
                "required": True,
                "validations": [
                    {"name": "min", "value": "0"}
                ]
            }
        ],
        "access": {
            "admin": "MERCHANT_READ_WRITE",
            "storefront": "PUBLIC_READ"
        }
    }

    variables = {"definition": definition_input}

    response = requests.post(
        f'{BASE_URL}/graphql.json',
        headers=HEADERS,
        json={'query': mutation, 'variables': variables}
    )

    result = response.json()

    if 'errors' in result:
        print(f"❌ GraphQL Error:")
        print(json.dumps(result['errors'], indent=2))
        return False

    data = result.get('data', {}).get('metaobjectDefinitionCreate', {})

    if data.get('userErrors'):
        print(f"❌ User Errors:")
        print(json.dumps(data['userErrors'], indent=2))
        return False

    if data.get('metaobjectDefinition'):
        metaobj_def = data['metaobjectDefinition']
        print(f"✅ Created metaobject definition: {metaobj_def['type']}")
        print(f"   Name: {metaobj_def['name']}")
        print(f"   ID: {metaobj_def['id']}")
        print(f"   Fields: {len(metaobj_def['fieldDefinitions'])}")
        return True

    return False


def verify_metaobject_definition():
    """Verify metaobject definition was created"""

    query = """
    {
      metaobjectDefinitions(first: 20) {
        edges {
          node {
            id
            name
            type
            fieldDefinitions {
              key
              name
              type {
                name
              }
            }
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

    definitions = result.get('data', {}).get('metaobjectDefinitions', {}).get('edges', [])

    loyalty_def = [d for d in definitions if d['node']['type'] == 'loyalty_account']

    if not loyalty_def:
        print("⚠️  No loyalty_account metaobject definition found!")
        return

    print(f"\n✅ Verified loyalty_account metaobject definition:")
    node = loyalty_def[0]['node']
    print(f"   ID: {node['id']}")
    print(f"   Name: {node['name']}")
    print(f"   Fields: {len(node['fieldDefinitions'])}")

    for field_def in node['fieldDefinitions']:
        print(f"     • {field_def['key']} ({field_def['type']['name']})")


if __name__ == '__main__':
    print("="*60)
    print("LOYALTY METAOBJECT SETUP")
    print("="*60)
    print(f"Store: {SHOPIFY_STORE}")
    print()

    success = create_loyalty_metaobject_definition()

    if success:
        verify_metaobject_definition()
        print("\n✅ Metaobject definition created! Ready for loyalty_manager_v2.py")
    else:
        print("\n⚠️  Setup failed. Check errors above.")
