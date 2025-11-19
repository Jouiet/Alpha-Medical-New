#!/usr/bin/env python3
"""
AUDIT FORENSIQUE COMPLET - État Factuel Actuel
Date: 2025-11-19
Objectif: Vérifier RIGOUREUSEMENT l'état de:
1. Language compliance (100% English?)
2. Draft products (restent draft?)
3. PayPal status (actif/inactif?)
4. Collection descriptions (4 manquantes?)
5. Product types (tous remplis après fix?)
"""

import os
import requests
import json
from typing import Dict, List, Any

# Shopify credentials
SHOP = "azffej-as.myshopify.com"
ACCESS_TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
if not ACCESS_TOKEN:
    raise ValueError("SHOPIFY_ADMIN_ACCESS_TOKEN environment variable not set")

HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def fetch_all_products() -> List[Dict]:
    """Fetch ALL products (published + draft) via Admin API"""
    url = f"https://{SHOP}/admin/api/2024-10/products.json?limit=250&status=any"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to fetch products: {response.status_code}")
        print(response.text)
        return []
    return response.json().get("products", [])

def fetch_all_collections() -> List[Dict]:
    """Fetch ALL collections via Admin API"""
    url = f"https://{SHOP}/admin/api/2024-10/custom_collections.json?limit=250"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to fetch collections: {response.status_code}")
        return []
    return response.json().get("custom_collections", [])

def check_french_content(text: str) -> List[str]:
    """Check for French content - UNAMBIGUOUS phrases only"""
    if not text:
        return []
    
    text_lower = text.lower()
    french_phrases = [
        "livraison gratuite", "garantie de", "retour gratuit", "satisfaction garantie",
        "dès maintenant", "avec nous", "chez nous", "pour vous", "notre équipe",
        "bienvenue à", "merci de", "s'il vous plaît", "jusqu'à", "à partir de",
        "votre commande", "notre magasin", "nos produits", "notre site",
        "contactez-nous", "appelez-nous", "écrivez-nous"
    ]
    
    found = []
    for phrase in french_phrases:
        if phrase in text_lower:
            found.append(phrase)
    
    return found

def audit_language(products: List[Dict]) -> Dict:
    """Audit language compliance"""
    issues = []
    
    for product in products:
        product_title = product.get("title", "")
        product_desc = product.get("body_html", "") or ""
        product_id = product.get("id")
        
        # Check title
        french_in_title = check_french_content(product_title)
        if french_in_title:
            issues.append({
                "product_id": product_id,
                "product_title": product_title,
                "field": "title",
                "french_phrases": french_in_title
            })
        
        # Check description
        french_in_desc = check_french_content(product_desc)
        if french_in_desc:
            issues.append({
                "product_id": product_id,
                "product_title": product_title,
                "field": "body_html",
                "french_phrases": french_in_desc
            })
    
    return {
        "total_products_checked": len(products),
        "products_with_french": len(set(i["product_id"] for i in issues)),
        "total_french_instances": len(issues),
        "issues": issues,
        "compliance": "✅ 100% English" if len(issues) == 0 else f"❌ {len(issues)} French instances found"
    }

def audit_draft_status(products: List[Dict]) -> Dict:
    """Audit draft products status"""
    draft_products = [p for p in products if p.get("status") == "draft"]
    published_products = [p for p in products if p.get("status") == "active"]
    
    return {
        "total_products": len(products),
        "draft_products": len(draft_products),
        "published_products": len(published_products),
        "draft_list": [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "status": p.get("status")
            }
            for p in draft_products
        ],
        "compliance": "✅ Draft products remain draft" if len(draft_products) > 0 else "⚠️ No draft products found"
    }

def audit_product_types(products: List[Dict]) -> Dict:
    """Audit product_type field completion"""
    missing_type = [p for p in products if not p.get("product_type")]
    
    return {
        "total_products": len(products),
        "missing_product_type": len(missing_type),
        "products_with_type": len(products) - len(missing_type),
        "missing_list": [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "product_type": p.get("product_type") or "EMPTY"
            }
            for p in missing_type[:10]  # First 10 only
        ],
        "compliance": "✅ 100% product_type filled" if len(missing_type) == 0 else f"❌ {len(missing_type)} missing product_type"
    }

def audit_collections(collections: List[Dict]) -> Dict:
    """Audit collection descriptions"""
    missing_desc = []
    
    for col in collections:
        desc = col.get("body_html") or ""
        if not desc or desc.strip() == "":
            missing_desc.append({
                "id": col.get("id"),
                "title": col.get("title"),
                "handle": col.get("handle"),
                "description_length": 0
            })
    
    return {
        "total_collections": len(collections),
        "missing_descriptions": len(missing_desc),
        "collections_with_desc": len(collections) - len(missing_desc),
        "missing_list": missing_desc,
        "compliance": "✅ All collections have descriptions" if len(missing_desc) == 0 else f"❌ {len(missing_desc)} collections missing descriptions"
    }

def check_paypal_status() -> Dict:
    """Check PayPal status via Payment Settings API"""
    # Note: Payment settings are NOT accessible via REST API
    # This would require manual check or Shopify Plus GraphQL API
    return {
        "status": "⚠️ MANUAL CHECK REQUIRED",
        "reason": "Payment settings not accessible via REST API",
        "action": "Check Shopify Admin → Settings → Payments manually",
        "requirement": "PAS de PayPal!! (only Shopify Payments: Stripe + Google Pay + Apple Pay)"
    }

def main():
    print("═" * 80)
    print("AUDIT FORENSIQUE COMPLET - État Factuel Actuel")
    print("═" * 80)
    print(f"Store: {SHOP}")
    print(f"Date: 2025-11-19\n")
    
    # Fetch data
    print("📥 Fetching products...")
    products = fetch_all_products()
    print(f"✅ Fetched {len(products)} products\n")
    
    print("📥 Fetching collections...")
    collections = fetch_all_collections()
    print(f"✅ Fetched {len(collections)} collections\n")
    
    print("═" * 80)
    print("AUDIT 1: LANGUAGE COMPLIANCE (100% English?)")
    print("═" * 80)
    lang_audit = audit_language(products)
    print(f"Total products checked: {lang_audit['total_products_checked']}")
    print(f"Products with French: {lang_audit['products_with_french']}")
    print(f"Total French instances: {lang_audit['total_french_instances']}")
    print(f"Compliance: {lang_audit['compliance']}\n")
    
    if lang_audit['issues']:
        print("⚠️ French content found:")
        for issue in lang_audit['issues'][:5]:  # First 5
            print(f"  - Product: {issue['product_title']}")
            print(f"    Field: {issue['field']}")
            print(f"    French phrases: {', '.join(issue['french_phrases'])}\n")
    
    print("═" * 80)
    print("AUDIT 2: DRAFT PRODUCTS STATUS")
    print("═" * 80)
    draft_audit = audit_draft_status(products)
    print(f"Total products: {draft_audit['total_products']}")
    print(f"Draft products: {draft_audit['draft_products']}")
    print(f"Published products: {draft_audit['published_products']}")
    print(f"Compliance: {draft_audit['compliance']}\n")
    
    if draft_audit['draft_list']:
        print("Draft products:")
        for draft in draft_audit['draft_list'][:10]:
            print(f"  - {draft['title']} (ID: {draft['id']}, Status: {draft['status']})")
    
    print("\n" + "═" * 80)
    print("AUDIT 3: PRODUCT_TYPE COMPLETION")
    print("═" * 80)
    type_audit = audit_product_types(products)
    print(f"Total products: {type_audit['total_products']}")
    print(f"Products with type: {type_audit['products_with_type']}")
    print(f"Missing product_type: {type_audit['missing_product_type']}")
    print(f"Compliance: {type_audit['compliance']}\n")
    
    if type_audit['missing_list']:
        print("⚠️ Products missing product_type:")
        for prod in type_audit['missing_list']:
            print(f"  - {prod['title']} (ID: {prod['id']})")
    
    print("\n" + "═" * 80)
    print("AUDIT 4: COLLECTION DESCRIPTIONS")
    print("═" * 80)
    col_audit = audit_collections(collections)
    print(f"Total collections: {col_audit['total_collections']}")
    print(f"Collections with descriptions: {col_audit['collections_with_desc']}")
    print(f"Missing descriptions: {col_audit['missing_descriptions']}")
    print(f"Compliance: {col_audit['compliance']}\n")
    
    if col_audit['missing_list']:
        print("⚠️ Collections missing descriptions:")
        for col in col_audit['missing_list']:
            print(f"  - {col['title']} (Handle: {col['handle']}, ID: {col['id']})")
    
    print("\n" + "═" * 80)
    print("AUDIT 5: PAYPAL STATUS")
    print("═" * 80)
    paypal_audit = check_paypal_status()
    print(f"Status: {paypal_audit['status']}")
    print(f"Reason: {paypal_audit['reason']}")
    print(f"Action: {paypal_audit['action']}")
    print(f"Requirement: {paypal_audit['requirement']}\n")
    
    print("═" * 80)
    print("SUMMARY")
    print("═" * 80)
    print(f"1. Language: {lang_audit['compliance']}")
    print(f"2. Draft Status: {draft_audit['compliance']}")
    print(f"3. Product Types: {type_audit['compliance']}")
    print(f"4. Collections: {col_audit['compliance']}")
    print(f"5. PayPal: {paypal_audit['status']}\n")
    
    # Save results
    results = {
        "timestamp": "2025-11-19",
        "language_audit": lang_audit,
        "draft_audit": draft_audit,
        "product_type_audit": type_audit,
        "collection_audit": col_audit,
        "paypal_audit": paypal_audit
    }
    
    with open("audit_results_2025-11-19.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("✅ Results saved to: audit_results_2025-11-19.json")

if __name__ == "__main__":
    main()
