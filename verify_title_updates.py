#!/usr/bin/env python3
"""
Verify that all product titles have been successfully shortened
"""

import json
import requests

# Shopify credentials
SHOP_URL = "azffej-as.myshopify.com"
ACCESS_TOKEN = "***REMOVED***"
API_VERSION = "2024-10"

# Headers for API requests
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Product IDs that were fixed
PRODUCT_IDS = [
    7602148245581,  # Cervical Collar
    7602146705485,  # Hunchback Orthotic
    7631747743821,  # AirBag Massage Cushion
    7616306806861,  # Bunion Corrector Toe Separator
    7616306839629,  # Effective Bunion Corrector
    7593555984461,  # Electric Heating Leg Massager
    7602188517453,  # Electric Medical Cupping
    7616306774093,  # Electric Vibration Massager Bunion
    7631747809357,  # Ergonomic Massage Rocker
    7631747711053,  # Full Body Shiatsu Massage Chair
    7602188550221,  # Smart Electric Vacuum Cupping
    7586408890445   # Nano Steam Eye Massager
]

def verify_product_titles():
    """Verify all product titles are now under 70 characters"""
    print("=" * 80)
    print("VERIFICATION: Product Title Lengths")
    print("=" * 80)

    all_good = True

    for product_id in PRODUCT_IDS:
        url = f"https://{SHOP_URL}/admin/api/{API_VERSION}/products/{product_id}.json"

        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            product = response.json()["product"]

            title = product["title"]
            title_length = len(title)

            if title_length <= 70:
                status = "✅"
            else:
                status = "❌"
                all_good = False

            print(f"{status} ID: {product_id} | Length: {title_length} chars")
            print(f"   Title: \"{title}\"")
            print()

        except Exception as e:
            print(f"❌ Error checking product {product_id}: {e}")
            all_good = False
            print()

    print("=" * 80)
    if all_good:
        print("✅ VERIFICATION PASSED: All titles are ≤70 characters")
    else:
        print("❌ VERIFICATION FAILED: Some titles still exceed 70 characters")
    print("=" * 80)

if __name__ == "__main__":
    verify_product_titles()