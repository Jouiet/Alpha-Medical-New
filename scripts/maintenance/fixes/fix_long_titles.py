#!/usr/bin/env python3
"""
Fix Alpha Medical products with titles exceeding 70 characters
"""

import json
import time
import requests
from typing import Dict, List, Tuple

# Shopify credentials
SHOP_URL = "azffej-as.myshopify.com"
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = "2025-10"

# Headers for API requests
HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Product IDs that need fixing
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

def fetch_product(product_id: int) -> Dict:
    """Fetch full product details from Shopify"""
    url = f"https://{SHOP_URL}/admin/api/{API_VERSION}/products/{product_id}.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()["product"]
    except Exception as e:
        print(f"Error fetching product {product_id}: {e}")
        return None

def shorten_title(original_title: str, product_type: str) -> str:
    """
    Shorten title to max 70 characters following Alpha Medical conventions
    Format: [Type] [Feature] | [Benefit]
    """
    # Remove common filler words
    title = original_title.replace(" and ", " & ")

    # Specific shortening rules based on product type
    if "cervical collar" in original_title.lower():
        return "Cervical Collar | Adjustable Neck & Spine Support"

    elif "hunchback" in original_title.lower() or "posture" in original_title.lower():
        return "Posture Corrector Brace | Back & Waist Support"

    elif "airbag massage cushion" in original_title.lower():
        return "Air Massage Cushion | Electric Kneading Chair Pad"

    elif "bunion corrector toe separator" in original_title.lower():
        return "Bunion Corrector | Toe Separator & Pain Relief"

    elif "effective bunion corrector" in original_title.lower():
        return "Bunion Corrector Airbag | Hallux Valgus Treatment"

    elif "electric heating leg massager" in original_title.lower():
        return "Electric Leg Massager | Heat & Air Compression"

    elif "electric medical cupping" in original_title.lower():
        return "Electric Cupping Set | Medical Therapy & Massage"

    elif "electric vibration massager bunion" in original_title.lower():
        return "Electric Bunion Massager | Vibration Foot Therapy"

    elif "ergonomic massage rocker" in original_title.lower():
        return "Massage Recliner Chair | Heat & Vibration Therapy"

    elif "full body shiatsu massage chair" in original_title.lower():
        return "Shiatsu Massage Chair | Full Body Electric Therapy"

    elif "smart electric vacuum cupping" in original_title.lower():
        return "Smart Cupping Device | Electric Vacuum & Scraping"

    elif "nano steam eye massager" in original_title.lower():
        return "Nano Steam Eye Massager | Warm Spa Acupressure Mask"

    # Fallback: generic shortening
    words = title.split()
    short_title = ""
    for word in words:
        if len(short_title + " " + word) <= 70:
            short_title = (short_title + " " + word).strip()
        else:
            break

    return short_title if short_title else title[:70]

def update_product_title(product_id: int, new_title: str) -> Tuple[bool, int]:
    """Update product title via Shopify API"""
    url = f"https://{SHOP_URL}/admin/api/{API_VERSION}/products/{product_id}.json"
    data = {
        "product": {
            "id": product_id,
            "title": new_title
        }
    }

    try:
        response = requests.put(url, headers=HEADERS, json=data)
        return response.status_code == 200, response.status_code
    except Exception as e:
        print(f"Error updating product {product_id}: {e}")
        return False, 0

def main():
    """Main execution"""
    print("=" * 80)
    print("ALPHA MEDICAL - FIX LONG PRODUCT TITLES")
    print("=" * 80)
    print(f"Products to fix: {len(PRODUCT_IDS)}")
    print()

    results = []
    success_count = 0

    for i, product_id in enumerate(PRODUCT_IDS, 1):
        print(f"\nProcessing Product {i}/{len(PRODUCT_IDS)} (ID: {product_id})")
        print("-" * 60)

        # Fetch current product
        product = fetch_product(product_id)
        if not product:
            results.append({
                "id": product_id,
                "success": False,
                "error": "Failed to fetch product"
            })
            continue

        current_title = product["title"]
        product_type = product.get("product_type", "")

        print(f"BEFORE: \"{current_title}\" ({len(current_title)} chars)")

        # Generate shortened title
        new_title = shorten_title(current_title, product_type)
        print(f"AFTER:  \"{new_title}\" ({len(new_title)} chars)")

        # Verify new title is within limit
        if len(new_title) > 70:
            print(f"⚠️  WARNING: New title still exceeds 70 chars!")
            # Force truncate as last resort
            new_title = new_title[:67] + "..."
            print(f"FORCED: \"{new_title}\" ({len(new_title)} chars)")

        # Update product
        success, status_code = update_product_title(product_id, new_title)

        if success:
            print(f"✅ API: {status_code} - Updated successfully")
            success_count += 1
        else:
            print(f"❌ API: {status_code} - Update failed")

        results.append({
            "id": product_id,
            "success": success,
            "before_title": current_title,
            "before_length": len(current_title),
            "after_title": new_title,
            "after_length": len(new_title),
            "status_code": status_code
        })

        # Rate limiting
        if i < len(PRODUCT_IDS):
            time.sleep(0.5)

    # Final report
    print("\n" + "=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    print(f"SCRIPT RESULT: {'SUCCESS' if success_count == len(PRODUCT_IDS) else 'PARTIAL'}")
    print(f"Products Updated: {success_count}/{len(PRODUCT_IDS)}")
    print()

    for i, result in enumerate(results, 1):
        status = "✅" if result.get("success") else "❌"
        print(f"\nProduct {i} ({result['id']}):")

        if "before_title" in result:
            print(f"{status} BEFORE: \"{result['before_title']}\" ({result['before_length']} chars)")
            print(f"{status} AFTER: \"{result['after_title']}\" ({result['after_length']} chars)")
            print(f"{status} API: {result.get('status_code', 'N/A')}")
        else:
            print(f"{status} ERROR: {result.get('error', 'Unknown error')}")

    print("\n" + "=" * 80)
    if success_count == len(PRODUCT_IDS):
        print("✅ Final Verification: All 12 products now have titles ≤70 characters")
    else:
        print(f"⚠️  Final Verification: {success_count}/12 products updated successfully")
        print(f"   {len(PRODUCT_IDS) - success_count} products need manual review")
    print("=" * 80)

if __name__ == "__main__":
    main()