#!/usr/bin/env python3
"""
FIX PRODUCT SEO - Add Missing Meta Descriptions
URGENT: All 96 products missing meta descriptions for SEO
"""

import requests
import os
import time
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

headers = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

graphql_url = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10/graphql.json'

def generate_meta_description(product):
    """
    Generate SEO-optimized meta description (max 160 characters)
    Format: [Product Type] - [Key Benefits] | Alpha Medical Care
    """
    title = product['title']

    # Extract key words from title
    title_lower = title.lower()

    # Template based on product type
    templates = {
        'knee': "Professional knee support for pain relief and injury prevention. Medical-grade orthopedic brace for active recovery.",
        'back': "Posture corrector and back pain relief. Adjustable medical brace for spine support and pain management.",
        'ankle': "Ankle support brace for stability and injury recovery. Professional-grade compression for pain relief.",
        'neck': "Cervical neck support and traction device. Medical collar for pain relief and posture correction.",
        'wrist': "Wrist brace for carpal tunnel and pain relief. Adjustable support for injury recovery and prevention.",
        'elbow': "Elbow support brace for tendonitis and pain relief. Compression sleeve for sports and injury recovery.",
        'shoulder': "Shoulder brace for rotator cuff support. Medical-grade compression for pain relief and stability.",
        'massager': "Professional massager for pain relief and muscle recovery. Medical-grade device for therapeutic use.",
        'ems': "EMS muscle stimulation device for training and recovery. Electric stimulation for pain relief and toning.",
        'led': "LED light therapy for skin rejuvenation and anti-aging. Professional-grade beauty device for home use.",
        'cupping': "Medical cupping therapy set for pain relief. Professional vacuum cupping for muscle recovery and wellness.",
        'bundle': "Complete care kit with professional medical equipment. Comprehensive solution for pain relief and recovery."
    }

    # Match product type
    for keyword, template in templates.items():
        if keyword in title_lower:
            return template

    # Default template
    return f"Professional medical equipment for pain relief and recovery. Shop {title[:80]} at Alpha Medical Care."

def fix_product_meta_description(product_id, product_title):
    """
    Add meta description metafield to product using GraphQL
    """
    product = {'title': product_title, 'id': product_id}
    meta_desc = generate_meta_description(product)

    # GraphQL mutation to add metafield
    mutation = """
    mutation productUpdate($input: ProductInput!) {
      productUpdate(input: $input) {
        product {
          id
          metafield(namespace: "global", key: "description_tag") {
            value
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
        "input": {
            "id": f"gid://shopify/Product/{product_id}",
            "metafields": [
                {
                    "namespace": "global",
                    "key": "description_tag",
                    "value": meta_desc,
                    "type": "single_line_text_field"
                }
            ]
        }
    }

    response = requests.post(
        graphql_url,
        json={'query': mutation, 'variables': variables},
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            return False, f"GraphQL errors: {data['errors']}"
        if data['data']['productUpdate']['userErrors']:
            return False, f"User errors: {data['data']['productUpdate']['userErrors']}"
        return True, meta_desc
    else:
        return False, f"HTTP {response.status_code}"

def main():
    print("=" * 80)
    print("FIX PRODUCT SEO METAFIELDS - ADD META DESCRIPTIONS")
    print("=" * 80)

    # Get all active products
    url = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10/products.json?limit=250&status=active'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Erreur API: {response.status_code}")
        return

    products = response.json()['products']

    print(f"\n📦 {len(products)} produits actifs trouvés")
    print(f"\n🔧 Ajout des meta descriptions...")
    print(f"\n{'='*80}\n")

    stats = {
        'total': len(products),
        'success': 0,
        'failed': 0,
        'skipped': 0
    }

    for i, product in enumerate(products, 1):
        product_id = product['id']
        title = product['title']

        print(f"[{i}/{len(products)}] {title[:60]}...")

        success, result = fix_product_meta_description(product_id, title)

        if success:
            stats['success'] += 1
            print(f"   ✅ Meta description ajoutée: {result[:80]}...")
        else:
            stats['failed'] += 1
            print(f"   ❌ Erreur: {result}")

        # Rate limiting: 2 requests per second (GraphQL limit)
        time.sleep(0.5)

    print("\n" + "=" * 80)
    print("RÉSULTATS FINAUX")
    print("=" * 80)
    print(f"Total produits: {stats['total']}")
    print(f"✅ Succès: {stats['success']}")
    print(f"❌ Échecs: {stats['failed']}")
    print(f"⏭️  Ignorés: {stats['skipped']}")
    print("=" * 80)

    if stats['success'] == stats['total']:
        print("\n🎉 SUCCÈS: Toutes les meta descriptions ont été ajoutées!")
    else:
        print(f"\n⚠️  ATTENTION: {stats['failed']} produits ont échoué")

if __name__ == '__main__':
    main()
