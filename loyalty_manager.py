#!/usr/bin/env python3
"""
Loyalty Manager - Full CRUD operations for customer loyalty points
Handles: earning, redemption, tier calculation, discount code generation
"""

import os
import requests
import json
from datetime import datetime, timezone
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


# ============================================================
# TIER CONFIGURATION
# ============================================================

TIER_THRESHOLDS = {
    'bronze': 0,
    'silver': 501,
    'gold': 1501
}

TIER_BENEFITS = {
    'bronze': ['Birthday reward', 'Exclusive deals'],
    'silver': ['Birthday reward', 'Exclusive deals', 'Early access', 'Free shipping'],
    'gold': ['Birthday reward', 'Exclusive deals', 'Early access', 'Free shipping', 'VIP support', '2x points']
}

REDEMPTION_TIERS = {
    100: 5,    # 100 points = $5 OFF
    200: 12,   # 200 points = $12 OFF (bonus $2)
    500: 35,   # 500 points = $35 OFF (bonus $10)
    1000: 80   # 1000 points = $80 OFF (bonus $20)
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_tier(points):
    """Calculate tier based on points"""
    if points >= TIER_THRESHOLDS['gold']:
        return 'gold'
    elif points >= TIER_THRESHOLDS['silver']:
        return 'silver'
    else:
        return 'bronze'


def get_customer_by_email(email):
    """Get customer ID by email"""
    query = """
    query GetCustomer($query: String!) {
      customers(first: 1, query: $query) {
        edges {
          node {
            id
            email
            firstName
            lastName
          }
        }
      }
    }
    """

    variables = {"query": f"email:{email}"}

    response = requests.post(
        f'{BASE_URL}/graphql.json',
        headers=HEADERS,
        json={'query': query, 'variables': variables}
    )

    result = response.json()

    if 'errors' in result:
        print(f"❌ Error finding customer: {result['errors']}")
        return None

    edges = result.get('data', {}).get('customers', {}).get('edges', [])

    if not edges:
        print(f"❌ No customer found with email: {email}")
        return None

    return edges[0]['node']


def get_customer_metafields(customer_gid):
    """Get all loyalty metafields for a customer"""
    query = """
    query GetCustomerMetafields($id: ID!) {
      customer(id: $id) {
        id
        email
        metafield_points: metafield(namespace: "loyalty", key: "points") {
          value
        }
        metafield_tier: metafield(namespace: "loyalty", key: "tier") {
          value
        }
        metafield_history: metafield(namespace: "loyalty", key: "history") {
          value
        }
        metafield_signup_bonus: metafield(namespace: "loyalty", key: "signup_bonus_claimed") {
          value
        }
        metafield_lifetime_earned: metafield(namespace: "loyalty", key: "lifetime_points_earned") {
          value
        }
        metafield_lifetime_redeemed: metafield(namespace: "loyalty", key: "lifetime_points_redeemed") {
          value
        }
      }
    }
    """

    variables = {"id": customer_gid}

    response = requests.post(
        f'{BASE_URL}/graphql.json',
        headers=HEADERS,
        json={'query': query, 'variables': variables}
    )

    result = response.json()

    if 'errors' in result:
        print(f"❌ Error getting metafields: {result['errors']}")
        return None

    customer_data = result.get('data', {}).get('customer', {})

    # Parse metafields
    loyalty_data = {
        'customer_id': customer_gid,
        'email': customer_data.get('email'),
        'points': int(customer_data.get('metafield_points', {}).get('value', 0) or 0),
        'tier': customer_data.get('metafield_tier', {}).get('value', 'bronze') or 'bronze',
        'history': json.loads(customer_data.get('metafield_history', {}).get('value', '[]') or '[]'),
        'signup_bonus_claimed': customer_data.get('metafield_signup_bonus', {}).get('value', 'false') == 'true',
        'lifetime_earned': int(customer_data.get('metafield_lifetime_earned', {}).get('value', 0) or 0),
        'lifetime_redeemed': int(customer_data.get('metafield_lifetime_redeemed', {}).get('value', 0) or 0)
    }

    return loyalty_data


def update_customer_metafields(customer_gid, points, tier, history, signup_bonus_claimed, lifetime_earned, lifetime_redeemed):
    """Update all loyalty metafields for a customer"""
    mutation = """
    mutation UpdateCustomerMetafields($input: CustomerInput!) {
      customerUpdate(input: $input) {
        customer {
          id
          metafields(first: 10, namespace: "loyalty") {
            edges {
              node {
                key
                value
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

    customer_input = {
        "id": customer_gid,
        "metafields": [
            {
                "namespace": "loyalty",
                "key": "points",
                "value": str(points),
                "type": "number_integer"
            },
            {
                "namespace": "loyalty",
                "key": "tier",
                "value": tier,
                "type": "single_line_text_field"
            },
            {
                "namespace": "loyalty",
                "key": "history",
                "value": json.dumps(history),
                "type": "json"
            },
            {
                "namespace": "loyalty",
                "key": "signup_bonus_claimed",
                "value": str(signup_bonus_claimed).lower(),
                "type": "boolean"
            },
            {
                "namespace": "loyalty",
                "key": "lifetime_points_earned",
                "value": str(lifetime_earned),
                "type": "number_integer"
            },
            {
                "namespace": "loyalty",
                "key": "lifetime_points_redeemed",
                "value": str(lifetime_redeemed),
                "type": "number_integer"
            }
        ]
    }

    variables = {"input": customer_input}

    response = requests.post(
        f'{BASE_URL}/graphql.json',
        headers=HEADERS,
        json={'mutation': mutation, 'variables': variables}
    )

    result = response.json()

    if 'errors' in result:
        print(f"❌ GraphQL Error: {result['errors']}")
        return False

    data = result.get('data', {}).get('customerUpdate', {})

    if data.get('userErrors'):
        print(f"❌ User Errors: {data['userErrors']}")
        return False

    return True


# ============================================================
# PUBLIC API FUNCTIONS
# ============================================================

def add_points(email, points, action, metadata=None):
    """
    Add points to customer account

    Args:
        email: Customer email
        points: Points to add (positive integer)
        action: Action type (e.g., 'purchase', 'signup_bonus', 'review')
        metadata: Optional dict with additional info (e.g., order_id, product_id)

    Returns:
        dict with success status and new balance
    """
    print(f"\n{'='*60}")
    print(f"ADD POINTS: {email}")
    print(f"{'='*60}")

    # Get customer
    customer = get_customer_by_email(email)
    if not customer:
        return {'success': False, 'error': 'Customer not found'}

    customer_gid = customer['id']

    # Get current loyalty data
    loyalty = get_customer_metafields(customer_gid)
    if not loyalty:
        return {'success': False, 'error': 'Failed to get loyalty data'}

    # Calculate new values
    new_points = loyalty['points'] + points
    new_lifetime_earned = loyalty['lifetime_earned'] + points
    new_tier = calculate_tier(new_points)

    # Add transaction to history
    transaction = {
        'date': datetime.now(timezone.utc).isoformat(),
        'action': action,
        'points': points,
        'balance_after': new_points
    }

    if metadata:
        transaction.update(metadata)

    history = loyalty['history']
    history.append(transaction)

    # Update metafields
    success = update_customer_metafields(
        customer_gid,
        new_points,
        new_tier,
        history,
        loyalty['signup_bonus_claimed'],
        new_lifetime_earned,
        loyalty['lifetime_redeemed']
    )

    if success:
        print(f"✅ Added {points} points to {email}")
        print(f"   Previous: {loyalty['points']} points ({loyalty['tier']})")
        print(f"   New: {new_points} points ({new_tier})")

        if new_tier != loyalty['tier']:
            print(f"   🎉 TIER UPGRADE: {loyalty['tier']} → {new_tier}")

        return {
            'success': True,
            'previous_balance': loyalty['points'],
            'new_balance': new_points,
            'previous_tier': loyalty['tier'],
            'new_tier': new_tier,
            'tier_upgraded': new_tier != loyalty['tier']
        }
    else:
        return {'success': False, 'error': 'Failed to update metafields'}


def deduct_points(email, points, action, metadata=None):
    """
    Deduct points from customer account (for redemption)

    Args:
        email: Customer email
        points: Points to deduct (positive integer)
        action: Action type (e.g., 'redemption')
        metadata: Optional dict (e.g., discount_code, discount_value)

    Returns:
        dict with success status and new balance
    """
    print(f"\n{'='*60}")
    print(f"DEDUCT POINTS: {email}")
    print(f"{'='*60}")

    # Get customer
    customer = get_customer_by_email(email)
    if not customer:
        return {'success': False, 'error': 'Customer not found'}

    customer_gid = customer['id']

    # Get current loyalty data
    loyalty = get_customer_metafields(customer_gid)
    if not loyalty:
        return {'success': False, 'error': 'Failed to get loyalty data'}

    # Validate sufficient balance
    if loyalty['points'] < points:
        print(f"❌ Insufficient balance: {loyalty['points']} points (need {points})")
        return {
            'success': False,
            'error': 'Insufficient points',
            'current_balance': loyalty['points'],
            'required': points
        }

    # Calculate new values
    new_points = loyalty['points'] - points
    new_lifetime_redeemed = loyalty['lifetime_redeemed'] + points
    new_tier = calculate_tier(new_points)

    # Add transaction to history
    transaction = {
        'date': datetime.now(timezone.utc).isoformat(),
        'action': action,
        'points': -points,  # Negative for deduction
        'balance_after': new_points
    }

    if metadata:
        transaction.update(metadata)

    history = loyalty['history']
    history.append(transaction)

    # Update metafields
    success = update_customer_metafields(
        customer_gid,
        new_points,
        new_tier,
        history,
        loyalty['signup_bonus_claimed'],
        loyalty['lifetime_earned'],
        new_lifetime_redeemed
    )

    if success:
        print(f"✅ Deducted {points} points from {email}")
        print(f"   Previous: {loyalty['points']} points")
        print(f"   New: {new_points} points")

        if new_tier != loyalty['tier']:
            print(f"   ⬇️  TIER DOWNGRADE: {loyalty['tier']} → {new_tier}")

        return {
            'success': True,
            'previous_balance': loyalty['points'],
            'new_balance': new_points,
            'previous_tier': loyalty['tier'],
            'new_tier': new_tier
        }
    else:
        return {'success': False, 'error': 'Failed to update metafields'}


def get_balance(email):
    """Get customer loyalty balance and info"""
    customer = get_customer_by_email(email)
    if not customer:
        return {'success': False, 'error': 'Customer not found'}

    loyalty = get_customer_metafields(customer['id'])
    if not loyalty:
        return {'success': False, 'error': 'Failed to get loyalty data'}

    return {
        'success': True,
        'email': email,
        'points': loyalty['points'],
        'tier': loyalty['tier'],
        'tier_benefits': TIER_BENEFITS[loyalty['tier']],
        'lifetime_earned': loyalty['lifetime_earned'],
        'lifetime_redeemed': loyalty['lifetime_redeemed'],
        'signup_bonus_claimed': loyalty['signup_bonus_claimed'],
        'transaction_count': len(loyalty['history'])
    }


def get_history(email, limit=10):
    """Get customer transaction history"""
    customer = get_customer_by_email(email)
    if not customer:
        return {'success': False, 'error': 'Customer not found'}

    loyalty = get_customer_metafields(customer['id'])
    if not loyalty:
        return {'success': False, 'error': 'Failed to get loyalty data'}

    # Sort history by date (most recent first)
    history = sorted(loyalty['history'], key=lambda x: x['date'], reverse=True)

    if limit:
        history = history[:limit]

    return {
        'success': True,
        'email': email,
        'total_transactions': len(loyalty['history']),
        'history': history
    }


def create_discount_code(email, points_value):
    """
    Create single-use discount code for point redemption

    Args:
        email: Customer email
        points_value: Points to redeem (must match REDEMPTION_TIERS)

    Returns:
        dict with discount code and value
    """
    if points_value not in REDEMPTION_TIERS:
        return {
            'success': False,
            'error': f'Invalid points value. Must be one of: {list(REDEMPTION_TIERS.keys())}'
        }

    discount_amount = REDEMPTION_TIERS[points_value]

    # Get customer
    customer = get_customer_by_email(email)
    if not customer:
        return {'success': False, 'error': 'Customer not found'}

    # Extract customer ID number from GID (gid://shopify/Customer/123 → 123)
    customer_id_num = customer['id'].split('/')[-1]

    # Generate unique code
    code = f"LOYALTY{points_value}-{customer_id_num}"

    # Create price rule (REST API - easier for discount codes)
    price_rule_data = {
        "price_rule": {
            "title": f"Loyalty Redemption - {email} - {points_value} points",
            "target_type": "line_item",
            "target_selection": "all",
            "allocation_method": "across",
            "value_type": "fixed_amount",
            "value": f"-{discount_amount}.00",
            "customer_selection": "prerequisite",
            "prerequisite_customer_ids": [int(customer_id_num)],
            "usage_limit": 1,
            "once_per_customer": True,
            "starts_at": datetime.now(timezone.utc).isoformat()
        }
    }

    response = requests.post(
        f'{BASE_URL}/price_rules.json',
        headers=HEADERS,
        json=price_rule_data
    )

    if response.status_code != 201:
        print(f"❌ Failed to create price rule: {response.text}")
        return {'success': False, 'error': 'Failed to create price rule'}

    price_rule = response.json()['price_rule']
    price_rule_id = price_rule['id']

    # Create discount code
    discount_code_data = {
        "discount_code": {
            "code": code
        }
    }

    response = requests.post(
        f'{BASE_URL}/price_rules/{price_rule_id}/discount_codes.json',
        headers=HEADERS,
        json=discount_code_data
    )

    if response.status_code != 201:
        print(f"❌ Failed to create discount code: {response.text}")
        return {'success': False, 'error': 'Failed to create discount code'}

    print(f"✅ Created discount code: {code} (${discount_amount} OFF)")

    return {
        'success': True,
        'code': code,
        'points': points_value,
        'discount_value': discount_amount,
        'usage_limit': 1
    }


def redeem_points(email, points_value):
    """
    Full redemption flow: validate, deduct points, create discount code

    Args:
        email: Customer email
        points_value: Points to redeem (100, 200, 500, or 1000)

    Returns:
        dict with discount code
    """
    print(f"\n{'='*60}")
    print(f"REDEEM POINTS: {email} ({points_value} points)")
    print(f"{'='*60}")

    # Validate points value
    if points_value not in REDEMPTION_TIERS:
        return {
            'success': False,
            'error': f'Invalid redemption amount. Choose: {list(REDEMPTION_TIERS.keys())}'
        }

    # Deduct points
    deduct_result = deduct_points(
        email,
        points_value,
        'redemption',
        metadata={'discount_value': REDEMPTION_TIERS[points_value]}
    )

    if not deduct_result['success']:
        return deduct_result

    # Create discount code
    discount_result = create_discount_code(email, points_value)

    if not discount_result['success']:
        # Rollback: add points back
        print("⚠️  Discount creation failed, rolling back points...")
        add_points(email, points_value, 'redemption_rollback')
        return discount_result

    print(f"✅ Redemption complete!")
    print(f"   Code: {discount_result['code']}")
    print(f"   Value: ${discount_result['discount_value']} OFF")
    print(f"   New balance: {deduct_result['new_balance']} points")

    return {
        'success': True,
        'code': discount_result['code'],
        'discount_value': discount_result['discount_value'],
        'points_redeemed': points_value,
        'new_balance': deduct_result['new_balance'],
        'new_tier': deduct_result['new_tier']
    }


# ============================================================
# CLI TESTING INTERFACE
# ============================================================

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("""
Loyalty Manager CLI

Usage:
  python3 loyalty_manager.py balance <email>
  python3 loyalty_manager.py add <email> <points> <action>
  python3 loyalty_manager.py deduct <email> <points> <action>
  python3 loyalty_manager.py redeem <email> <points>
  python3 loyalty_manager.py history <email> [limit]

Examples:
  python3 loyalty_manager.py balance customer@example.com
  python3 loyalty_manager.py add customer@example.com 50 signup_bonus
  python3 loyalty_manager.py add customer@example.com 150 purchase
  python3 loyalty_manager.py redeem customer@example.com 100
  python3 loyalty_manager.py history customer@example.com 20
""")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'balance':
        email = sys.argv[2]
        result = get_balance(email)
        print(json.dumps(result, indent=2))

    elif command == 'add':
        email = sys.argv[2]
        points = int(sys.argv[3])
        action = sys.argv[4]
        result = add_points(email, points, action)
        print(json.dumps(result, indent=2))

    elif command == 'deduct':
        email = sys.argv[2]
        points = int(sys.argv[3])
        action = sys.argv[4]
        result = deduct_points(email, points, action)
        print(json.dumps(result, indent=2))

    elif command == 'redeem':
        email = sys.argv[2]
        points = int(sys.argv[3])
        result = redeem_points(email, points)
        print(json.dumps(result, indent=2))

    elif command == 'history':
        email = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        result = get_history(email, limit)
        print(json.dumps(result, indent=2))

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
