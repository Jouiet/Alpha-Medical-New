#!/usr/bin/env python3
"""
Suppression de la collection Special Offers
"""

import json
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-10')

headers = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

def delete_collection(collection_id):
    """Supprime une collection par ID"""
    mutation = """
    mutation collectionDelete($input: CollectionDeleteInput!) {
      collectionDelete(input: $input) {
        deletedCollectionId
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "id": collection_id
        }
    }

    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
    response = requests.post(url, headers=headers, json={'query': mutation, 'variables': variables})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"ERROR: {response.status_code}")
        print(response.text)
        return None

def main():
    collection_id = "gid://shopify/Collection/295136034893"

    print("=" * 80)
    print("SUPPRESSION COLLECTION SPECIAL OFFERS")
    print("=" * 80)
    print(f"\nCollection ID: {collection_id}")
    print("Collection Handle: special-offers")
    print("Collection Title: Special Offers")
    print("\n⚠️ SUPPRESSION EN COURS...\n")

    result = delete_collection(collection_id)

    if not result:
        print("❌ Erreur lors de la suppression")
        return False

    if 'errors' in result:
        print("❌ ERREURS GRAPHQL:")
        for error in result['errors']:
            print(f"   - {error.get('message', 'Unknown error')}")
        return False

    data = result.get('data', {})
    collection_delete = data.get('collectionDelete', {})

    user_errors = collection_delete.get('userErrors', [])
    if user_errors:
        print("❌ ERREURS UTILISATEUR:")
        for error in user_errors:
            print(f"   - {error.get('field')}: {error.get('message')}")
        return False

    deleted_id = collection_delete.get('deletedCollectionId')

    if deleted_id:
        print("✅ SUPPRESSION RÉUSSIE!")
        print(f"   Collection supprimée: {deleted_id}")

        # Sauvegarder log
        log = {
            'timestamp': '2025-10-15T04:35:00',
            'action': 'collection_delete',
            'collection_id': collection_id,
            'collection_handle': 'special-offers',
            'collection_title': 'Special Offers',
            'deleted_collection_id': deleted_id,
            'status': 'success'
        }

        with open('special_offers_deletion_log.json', 'w', encoding='utf-8') as f:
            json.dump(log, f, indent=2, ensure_ascii=False)

        print("\n✅ Log sauvegardé: special_offers_deletion_log.json")
        print("=" * 80)
        return True
    else:
        print("❌ Échec: Aucun ID retourné")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🟢 COLLECTION SPECIAL OFFERS SUPPRIMÉE AVEC SUCCÈS")
    else:
        print("\n🔴 ÉCHEC SUPPRESSION COLLECTION")
