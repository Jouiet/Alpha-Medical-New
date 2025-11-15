#!/usr/bin/env python3
"""
BUNDLE AUTO-CREATION API - Vercel Serverless Function
Handles bundle proposals aggregation and auto-creation at 10+ identical proposals
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import hashlib
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for Shopify frontend

# Shopify credentials from environment variables
SHOPIFY_DOMAIN = os.environ.get('SHOPIFY_DOMAIN', 'azffej-as.myshopify.com')
SHOPIFY_TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = "2025-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# Get Page ID for bundle-creator (will be set via env var)
BUNDLE_CREATOR_PAGE_GID = os.environ.get('BUNDLE_CREATOR_PAGE_GID', '')

# Collection ID for bundles
BUNDLES_COLLECTION_GID = "gid://shopify/Collection/296239169613"

THRESHOLD = 10  # 10+ identical proposals = auto-create


@app.route('/api/submit', methods=['POST', 'OPTIONS'])
def submit_proposal():
    """
    Receives bundle proposal, aggregates in Metafields, auto-creates if 10+

    Request body:
    {
        "product_ids": [123, 456, 789],
        "email": "customer@email.com",
        "hash": "hash_abc123def456"
    }

    Response:
    {
        "success": true,
        "message": "Proposal recorded",
        "count": 5,
        "remaining": 5,
        "bundle_created": false
    }
    """

    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.json

        product_ids = data.get('product_ids', [])
        email = data.get('email', '').strip().lower()
        proposal_hash = data.get('hash', '')

        # Validate input
        if not product_ids or not email or not proposal_hash:
            return jsonify({'error': 'Missing required fields: product_ids, email, hash'}), 400

        if len(product_ids) < 3 or len(product_ids) > 4:
            return jsonify({'error': 'Must select 3-4 products'}), 400

        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Read existing metafield
        metafield_key = proposal_hash
        metafield = read_metafield(BUNDLE_CREATOR_PAGE_GID, 'bundle_proposals', metafield_key)

        if metafield:
            # Update existing proposal
            value = json.loads(metafield['value'])

            # Check if email already submitted
            if email in value['emails']:
                return jsonify({
                    'success': False,
                    'error': 'You already submitted this proposal',
                    'count': value['count']
                }), 400

            # Check if bundle already created
            if value.get('bundle_created'):
                return jsonify({
                    'success': False,
                    'error': 'This bundle was already created',
                    'bundle_id': value.get('bundle_id'),
                    'count': value['count']
                }), 400

            # Increment count
            value['count'] += 1
            value['emails'].append(email)
            value['updated_at'] = datetime.utcnow().isoformat()

            # Save updated metafield
            update_metafield(metafield['id'], value)

            # Check if threshold reached
            if value['count'] >= THRESHOLD:
                # AUTO-CREATE BUNDLE
                print(f"🎉 THRESHOLD REACHED: {value['count']} proposals for {proposal_hash}")

                bundle_data = create_bundle_auto(
                    product_ids=value['product_ids'],
                    proposal_hash=proposal_hash,
                    customer_emails=value['emails']
                )

                # Update metafield to mark as created
                value['bundle_created'] = True
                value['bundle_id'] = bundle_data['id']
                value['bundle_title'] = bundle_data['title']
                value['bundle_url'] = bundle_data['url']
                update_metafield(metafield['id'], value)

                return jsonify({
                    'success': True,
                    'message': 'Bundle auto-created! You and all proposers will be notified.',
                    'count': value['count'],
                    'bundle_created': True,
                    'bundle_id': bundle_data['id'],
                    'bundle_title': bundle_data['title'],
                    'bundle_url': bundle_data['url']
                })

            return jsonify({
                'success': True,
                'message': f'Proposal recorded! {THRESHOLD - value["count"]} more needed.',
                'count': value['count'],
                'remaining': THRESHOLD - value['count'],
                'bundle_created': False
            })

        else:
            # Create new proposal
            value = {
                'product_ids': product_ids,
                'count': 1,
                'emails': [email],
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'bundle_created': False,
                'bundle_id': None
            }

            # Create metafield
            create_metafield(BUNDLE_CREATOR_PAGE_GID, 'bundle_proposals', metafield_key, value)

            return jsonify({
                'success': True,
                'message': f'Proposal created! {THRESHOLD - 1} more needed.',
                'count': 1,
                'remaining': THRESHOLD - 1,
                'bundle_created': False
            })

    except Exception as e:
        print(f"❌ Error in submit_proposal: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def read_metafield(owner_id, namespace, key):
    """Read metafield via GraphQL"""
    query = """
    query($id: ID!, $namespace: String!, $key: String!) {
      page(id: $id) {
        metafield(namespace: $namespace, key: $key) {
          id
          value
        }
      }
    }
    """

    variables = {"id": owner_id, "namespace": namespace, "key": key}

    try:
        response = requests.post(
            GRAPHQL_URL,
            headers=HEADERS,
            json={"query": query, "variables": variables},
            timeout=10
        )

        data = response.json()

        if 'errors' in data:
            print(f"❌ GraphQL error in read_metafield: {data['errors']}")
            return None

        return data.get('data', {}).get('page', {}).get('metafield')

    except Exception as e:
        print(f"❌ Exception in read_metafield: {str(e)}")
        return None


def create_metafield(owner_id, namespace, key, value):
    """Create metafield via GraphQL"""
    mutation = """
    mutation($input: MetafieldsSetInput!) {
      metafieldsSet(metafields: [$input]) {
        metafields {
          id
          key
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
            "ownerId": owner_id,
            "namespace": namespace,
            "key": key,
            "type": "json",
            "value": json.dumps(value)
        }
    }

    try:
        response = requests.post(
            GRAPHQL_URL,
            headers=HEADERS,
            json={"query": mutation, "variables": variables},
            timeout=10
        )

        data = response.json()

        if 'errors' in data or data.get('data', {}).get('metafieldsSet', {}).get('userErrors'):
            print(f"❌ Error creating metafield: {data}")

        return data

    except Exception as e:
        print(f"❌ Exception in create_metafield: {str(e)}")
        return None


def update_metafield(metafield_id, value):
    """Update metafield via GraphQL"""
    mutation = """
    mutation($input: MetafieldsSetInput!) {
      metafieldsSet(metafields: [$input]) {
        metafields {
          id
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
            "id": metafield_id,
            "value": json.dumps(value)
        }
    }

    try:
        response = requests.post(
            GRAPHQL_URL,
            headers=HEADERS,
            json={"query": mutation, "variables": variables},
            timeout=10
        )

        return response.json()

    except Exception as e:
        print(f"❌ Exception in update_metafield: {str(e)}")
        return None


def create_bundle_auto(product_ids, proposal_hash, customer_emails):
    """
    Auto-create bundle product via Shopify Admin API
    Returns: {id, title, url}
    """

    # Fetch product details for pricing
    products = fetch_products_bulk(product_ids)

    if not products:
        raise Exception("Failed to fetch product details")

    # Calculate pricing
    total_price = sum(float(p['price']) for p in products)
    bundle_price = round(total_price * 0.65, 2)  # 35% OFF

    # Generate title
    short_hash = proposal_hash.replace('hash_', '')[:6].upper()
    bundle_title = f"Custom Bundle #{short_hash}"

    # Generate description
    product_titles = [p['title'] for p in products]
    description = f"""
    <h2>Community-Created Bundle</h2>
    <p>This bundle was created based on {len(customer_emails)} customer requests!</p>
    <h3>Includes:</h3>
    <ul>
        {"".join(f"<li>{title}</li>" for title in product_titles)}
    </ul>
    <p><strong>Save 35% OFF</strong> when you buy these products together.</p>
    """

    # Create product via REST API (simpler than GraphQL for this)
    product_data = {
        "product": {
            "title": bundle_title,
            "vendor": "Alpha Medical",
            "product_type": "Bundle",
            "tags": "bundle, auto-created, " + f"proposal-{proposal_hash}",
            "body_html": description,
            "published": True,
            "variants": [{
                "price": str(bundle_price),
                "compare_at_price": str(total_price),
                "inventory_policy": "continue",
                "inventory_management": None,
                "requires_shipping": True
            }],
            "metafields": [
                {
                    "namespace": "auto_bundle",
                    "key": "proposal_hash",
                    "type": "single_line_text_field",
                    "value": proposal_hash
                },
                {
                    "namespace": "auto_bundle",
                    "key": "customer_emails",
                    "type": "json",
                    "value": json.dumps(customer_emails)
                },
                {
                    "namespace": "auto_bundle",
                    "key": "product_ids",
                    "type": "json",
                    "value": json.dumps([str(pid) for pid in product_ids])
                },
                {
                    "namespace": "auto_bundle",
                    "key": "created_at",
                    "type": "single_line_text_field",
                    "value": datetime.utcnow().isoformat()
                }
            ]
        }
    }

    try:
        response = requests.post(
            f"{REST_URL}/products.json",
            headers=HEADERS,
            json=product_data,
            timeout=15
        )

        if response.status_code != 201:
            print(f"❌ Error creating product: {response.status_code} {response.text}")
            raise Exception(f"Failed to create bundle: {response.text}")

        created_product = response.json()['product']
        product_id = created_product['id']
        product_handle = created_product['handle']

        print(f"✅ Bundle created: {bundle_title} (ID: {product_id})")

        # Add to collection
        add_to_collection_rest(product_id, 296239169613)

        return {
            'id': str(product_id),
            'title': bundle_title,
            'url': f"https://www.alphamedical.shop/products/{product_handle}",
            'price': bundle_price,
            'compare_at_price': total_price
        }

    except Exception as e:
        print(f"❌ Exception in create_bundle_auto: {str(e)}")
        raise


def fetch_products_bulk(product_ids):
    """Fetch product details via REST API"""
    products = []

    for product_id in product_ids:
        try:
            response = requests.get(
                f"{REST_URL}/products/{product_id}.json",
                headers=HEADERS,
                timeout=5
            )

            if response.status_code == 200:
                product = response.json()['product']
                variant = product['variants'][0]

                products.append({
                    'id': product_id,
                    'title': product['title'],
                    'price': variant['price'],
                    'handle': product['handle']
                })

        except Exception as e:
            print(f"❌ Error fetching product {product_id}: {str(e)}")

    return products


def add_to_collection_rest(product_id, collection_id):
    """Add product to collection via REST API"""
    collect_data = {
        "collect": {
            "product_id": product_id,
            "collection_id": collection_id
        }
    }

    try:
        response = requests.post(
            f"{REST_URL}/collects.json",
            headers=HEADERS,
            json=collect_data,
            timeout=5
        )

        if response.status_code == 201:
            print(f"✅ Product {product_id} added to collection {collection_id}")
        else:
            print(f"❌ Error adding to collection: {response.status_code}")

    except Exception as e:
        print(f"❌ Exception adding to collection: {str(e)}")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'bundle-auto-creation-api',
        'version': '1.0.0'
    })


# Vercel serverless handler
def handler(request):
    return app(request)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
