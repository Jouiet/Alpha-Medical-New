#!/usr/bin/env python3
"""
Fix Missing Collections for Two Specific Products
Alpha Medical - Fix products with NO_COLLECTIONS status
"""

import json
import requests
import sys
from typing import Dict, Tuple

# Shopify API Configuration
SHOPIFY_STORE = "azffej-as.myshopify.com"
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = "2025-10"

# API Headers
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Products to fix (both going to Therapy & Wellness)
PRODUCTS_TO_FIX = [
    {
        "product_id": 7586408890445,
        "title": "Nano Steam Eye Massager | Warm Spa Acupressure Mask",
        "collection_id": 295060504653,  # Therapy & Wellness
        "collection_name": "Therapy & Wellness"
    },
    {
        "product_id": 7585886732365,
        "title": "Rehabilitation Robot Gloves | Stroke Cerebral Palsy",
        "collection_id": 295060504653,  # Therapy & Wellness
        "collection_name": "Therapy & Wellness"
    }
]

def assign_product_to_collection(product_id: int, collection_id: int) -> Tuple[int, Dict]:
    """
    Assign a product to a collection using the collects API.

    Returns:
        Tuple of (status_code, response_data)
    """
    url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/collects.json"

    payload = {
        "collect": {
            "product_id": product_id,
            "collection_id": collection_id
        }
    }

    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        return response.status_code, response.json() if response.text else {}
    except Exception as e:
        return 0, {"error": str(e)}

def verify_product_collections(product_id: int) -> list:
    """
    Verify which collections a product belongs to.

    Returns:
        List of collection IDs
    """
    url = f"https://{SHOPIFY_STORE}/admin/api/{API_VERSION}/collects.json"
    params = {"product_id": product_id}

    try:
        response = requests.get(url, params=params, headers=HEADERS)
        if response.status_code == 200:
            collects = response.json().get("collects", [])
            return [collect["collection_id"] for collect in collects]
        return []
    except Exception as e:
        print(f"Error verifying collections: {e}")
        return []

def main():
    """Main execution function."""
    print("=" * 70)
    print("FIXING MISSING COLLECTIONS FOR PRODUCTS")
    print("=" * 70)
    print()

    overall_success = True
    results = []

    for product in PRODUCTS_TO_FIX:
        product_id = product["product_id"]
        collection_id = product["collection_id"]

        print(f"Processing Product ID: {product_id}")
        print(f"Title: {product['title'][:50]}...")
        print(f"Target Collection: {product['collection_name']} (ID: {collection_id})")

        # Attempt to assign the product to the collection
        status_code, response_data = assign_product_to_collection(product_id, collection_id)

        # Interpret the result
        if status_code == 201:
            status = "ASSIGNED"
            print(f"✅ Successfully assigned to {product['collection_name']}")
        elif status_code == 422:
            # Check if it's a duplicate error
            error_msg = response_data.get("errors", {})
            if "already exists" in str(error_msg).lower() or "duplicate" in str(error_msg).lower():
                status = "ALREADY_ASSIGNED"
                print(f"ℹ️  Product already in collection (duplicate detected)")
            else:
                status = "FAILED"
                print(f"❌ Failed with 422: {error_msg}")
                overall_success = False
        elif status_code == 0:
            status = "ERROR"
            print(f"❌ Connection error: {response_data.get('error', 'Unknown')}")
            overall_success = False
        else:
            status = "FAILED"
            print(f"❌ Failed with status {status_code}: {response_data}")
            overall_success = False

        # Verify the assignment
        collections = verify_product_collections(product_id)
        if collection_id in collections:
            print(f"✅ Verification: Product IS in collection {collection_id}")
            verification = "CONFIRMED"
        else:
            print(f"⚠️  Verification: Product NOT found in collection {collection_id}")
            verification = "NOT_FOUND"
            if status == "ASSIGNED":
                overall_success = False

        results.append({
            "product_id": product_id,
            "title": product["title"],
            "collection": product["collection_name"],
            "api_response": status_code,
            "status": status,
            "verification": verification
        })

        print("-" * 50)
        print()

    # Final Report
    print("=" * 70)
    print("SCRIPT RESULT:", "SUCCESS" if overall_success else "FAILED")
    print("=" * 70)
    print()

    for i, result in enumerate(results, 1):
        print(f"Product {i} ({result['product_id']}):")
        print(f"- Collection: {result['collection']}")
        print(f"- API Response: {result['api_response']}")
        print(f"- Status: {result['status']}")
        print(f"- Verification: {result['verification']}")
        print()

    # Final verification summary
    all_verified = all(r["verification"] == "CONFIRMED" for r in results)
    if all_verified:
        print("✅ Verification: Confirmed both products have collections")
    else:
        print("⚠️  Verification: Not all products confirmed in collections")

    return 0 if overall_success and all_verified else 1

if __name__ == "__main__":
    sys.exit(main())