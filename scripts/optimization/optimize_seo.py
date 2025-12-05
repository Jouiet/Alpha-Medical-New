#!/usr/bin/env python3
"""
Script d'optimisation SEO automatique pour Alpha Medical Care
Utilise Shopify Admin API pour mettre à jour les meta descriptions et titles
"""

import requests
import json
import time

# Configuration
import os
from pathlib import Path

# Load token from .env.admin file
env_file = Path(__file__).parent / '.env.admin'
ACCESS_TOKEN = None

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                ACCESS_TOKEN = line.split('=', 1)[1].strip()
                break

if not ACCESS_TOKEN:
    print("❌ ERROR: SHOPIFY_ADMIN_ACCESS_TOKEN not found in .env.admin")
    print("Please create .env.admin file with your token.")
    exit(1)

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-10"

BASE_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Meta descriptions optimisées pour chaque page
SEO_OPTIMIZATIONS = {
    "faq": {
        "title": "FAQ - Alpha Medical Care | Medical Support Products Questions",
        "metafield_description": "Common questions about Alpha Medical Care products, shipping, returns & sizing. Expert answers on medical braces, supports & therapy equipment. Shop with confidence."
    },
    "shipping-delivery": {
        "title": "Shipping & Delivery - Fast Medical Support Product Delivery | Alpha Medical",
        "metafield_description": "Free shipping over $50. Fast delivery (3-14 days) to USA & worldwide. Track your medical support products order. Expert packaging & handling."
    },
    "returns-exchanges": {
        "title": "Easy Returns & Exchanges - 30 Day Guarantee | Alpha Medical Care",
        "metafield_description": "Hassle-free 30-day returns on medical support products. Free return shipping on defects. Easy exchange process. Read our complete return policy."
    },
    "terms-of-service": {
        "title": "Terms of Service - Alpha Medical Care Legal Terms & Conditions",
        "metafield_description": "Read Alpha Medical Care's terms of service, return policy, medical disclaimer & user agreement. Updated October 2025. Shop with confidence."
    },
    "bestsellers": {
        "title": "Bestsellers - Top Medical Support Products | Alpha Medical Care",
        "metafield_description": "Shop our most popular medical braces, supports & therapy equipment. Trusted by thousands. Free shipping over $50. 30-day money-back guarantee."
    },
    "black-friday": {
        "title": "Black Friday Deals - Up to 50% Off Medical Support Products",
        "metafield_description": "Huge Black Friday savings on knee braces, back supports, therapy equipment & more. Limited time offers. Free shipping. Shop Alpha Medical Care deals now!"
    },
    "new-arrivals": {
        "title": "New Arrivals - Latest Medical Support Products | Alpha Medical Care",
        "metafield_description": "Discover our newest medical braces, posture correctors & therapy equipment. Latest innovations in pain relief & recovery. Free shipping over $50."
    },
    "warranty-guarantee": {
        "title": "Product Warranty & Guarantee - Alpha Medical Care Quality Promise",
        "metafield_description": "90-day warranty on all medical support products. 1-year extended warranty available. Defect protection & satisfaction guarantee. Read warranty terms."
    },
    "product-registration": {
        "title": "Register Your Product - Extended Warranty | Alpha Medical Care",
        "metafield_description": "Register your medical support product for 30-day warranty extension, priority support & exclusive discounts. Quick & easy registration process."
    },
    "medical-disclaimer": {
        "title": "Medical Disclaimer - Alpha Medical Care Product Safety Information",
        "metafield_description": "Important medical disclaimer for Alpha Medical Care products. Safety warnings, contraindications & usage guidelines. Always consult your doctor."
    },
    "help-center": {
        "title": "Help Center - Medical Support Product Guides | Alpha Medical Care",
        "metafield_description": "Get help with your medical support products. Usage guides, sizing charts, troubleshooting & customer support. Expert advice available 24/7."
    },
    "how-to-use": {
        "title": "How to Use Medical Support Products - Video Guides & Instructions",
        "metafield_description": "Step-by-step guides for using knee braces, back supports, therapy equipment & more. Video tutorials, fitting instructions & expert tips."
    },
    "refer-a-friend": {
        "title": "Refer a Friend - Get $10 Off Medical Support Products | Alpha Medical",
        "metafield_description": "Refer friends & earn $10 credit per referral. Share Alpha Medical Care & save together. Join our VIP referral program with exclusive rewards."
    },
    "customer-reviews": {
        "title": "Customer Reviews - Real Testimonials | Alpha Medical Care",
        "metafield_description": "Read real customer reviews & success stories. 4.8/5 star rating. Thousands of satisfied customers trust Alpha Medical Care for pain relief & recovery."
    },
    "about-us": {
        "title": "About Us - Alpha Medical Care | Medical Support Equipment Experts",
        "metafield_description": "Learn about Alpha Medical Care's mission to provide professional-grade orthopedic & therapeutic solutions. Quality medical support products since 2025."
    },
    "contact": {
        "title": "Contact Us - Alpha Medical Care Customer Support",
        "metafield_description": "Contact Alpha Medical Care support team. Email, phone & live chat available. Mon-Fri 9AM-6PM EST. Fast response to all inquiries."
    }
}

def get_all_pages():
    """Récupère toutes les pages du store"""
    url = f"{BASE_URL}/pages.json"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()["pages"]
    else:
        print(f"❌ Erreur récupération pages: {response.status_code}")
        print(response.text)
        return []

def update_page_seo(page_id, title, metafield_description):
    """Met à jour le title et la meta description d'une page"""

    # Étape 1: Mettre à jour le title de la page
    url = f"{BASE_URL}/pages/{page_id}.json"
    data = {
        "page": {
            "id": page_id,
            "title": title
        }
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code != 200:
        print(f"  ❌ Erreur mise à jour title: {response.status_code}")
        print(f"  {response.text}")
        return False

    # Étape 2: Créer/mettre à jour le metafield pour meta description
    # Note: Shopify utilise metafields pour les meta descriptions personnalisées
    metafield_url = f"{BASE_URL}/pages/{page_id}/metafields.json"

    metafield_data = {
        "metafield": {
            "namespace": "global",
            "key": "description_tag",
            "value": metafield_description,
            "type": "single_line_text_field"
        }
    }

    response_metafield = requests.post(metafield_url, headers=headers, json=metafield_data)

    if response_metafield.status_code not in [200, 201]:
        print(f"  ⚠️ Metafield peut-être pas créé (code {response_metafield.status_code})")
        # Ce n'est pas critique, on continue

    return True

def main():
    print("=" * 70)
    print("🔍 OPTIMISATION SEO AUTOMATIQUE - ALPHA MEDICAL CARE")
    print("=" * 70)
    print()

    # Récupérer toutes les pages
    print("📥 Récupération des pages Shopify...")
    pages = get_all_pages()
    print(f"✅ {len(pages)} pages trouvées\n")

    if not pages:
        print("❌ Aucune page trouvée. Arrêt du script.")
        return

    # Optimiser chaque page
    updated_count = 0
    skipped_count = 0

    for page in pages:
        handle = page["handle"]
        current_title = page["title"]
        page_id = page["id"]

        print(f"📄 Page: {current_title} (/{handle})")

        if handle in SEO_OPTIMIZATIONS:
            opt = SEO_OPTIMIZATIONS[handle]
            new_title = opt["title"]
            meta_desc = opt["metafield_description"]

            print(f"  📝 Title actuel: {current_title}")
            print(f"  ✨ Nouveau title: {new_title}")
            print(f"  📋 Meta description: {meta_desc[:60]}...")

            # Mettre à jour
            success = update_page_seo(page_id, new_title, meta_desc)

            if success:
                print(f"  ✅ Page optimisée avec succès!\n")
                updated_count += 1
            else:
                print(f"  ❌ Échec optimisation\n")
                skipped_count += 1

            # Rate limiting: attendre 0.5 secondes entre chaque requête
            time.sleep(0.5)
        else:
            print(f"  ⏭️  Pas d'optimisation définie pour cette page\n")
            skipped_count += 1

    # Résumé
    print("=" * 70)
    print("📊 RÉSUMÉ DE L'OPTIMISATION")
    print("=" * 70)
    print(f"✅ Pages optimisées: {updated_count}")
    print(f"⏭️  Pages ignorées: {skipped_count}")
    print(f"📝 Total pages: {len(pages)}")
    print()
    print("🎉 Optimisation SEO terminée!")
    print("=" * 70)

if __name__ == "__main__":
    main()
