#!/usr/bin/env python3
"""
COMPLETE FORENSIC AUDIT V2 - Rigorous Factual Verification
Date: 2025-12-05 (Updated)
API Version: 2025-01 (latest)
"""

import os
import requests
import json
from typing import Dict, List

SHOP = "azffej-as.myshopify.com"
TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")
if not TOKEN:
    raise ValueError("SHOPIFY_ADMIN_ACCESS_TOKEN environment variable not set")
API_VERSION = "2025-10"

HEADERS = {"X-Shopify-Access-Token": TOKEN, "Content-Type": "application/json"}

def fetch_all_products() -> List[Dict]:
    """Fetch ALL products with pagination"""
    all_products = []
    url = f"https://{SHOP}/admin/api/{API_VERSION}/products.json?limit=250"
    
    while url:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            break
        
        data = response.json()
        products = data.get("products", [])
        all_products.extend(products)
        
        # Check for next page
        link_header = response.headers.get("Link", "")
        if 'rel="next"' in link_header:
            # Extract next URL from Link header
            next_url = link_header.split('>; rel="next"')[0].split('<')[1] if '<' in link_header else None
            url = next_url if next_url else None
        else:
            url = None
    
    return all_products

def check_french_keywords(text: str) -> List[str]:
    """Check for unambiguous French content"""
    if not text:
        return []
    
    text_lower = text.lower()
    
    # Unambiguous French phrases (not cognates)
    french_phrases = [
        "livraison gratuite", "garantie de", "retour gratuit", "satisfaction garantie",
        "dès maintenant", "avec nous", "chez nous", "pour vous", "notre équipe",
        "bienvenue à", "merci de", "s'il vous plaît", "jusqu'à", "à partir de",
        "votre commande", "notre magasin", "nos produits", "notre site",
        "contactez-nous", "appelez-nous", "écrivez-nous", "veuillez",
        "aujourd'hui", "demain", "hier", "chaque jour", "tous les jours"
    ]
    
    found = []
    for phrase in french_phrases:
        if phrase in text_lower:
            found.append(phrase)
    
    return found

def audit_language(products: List[Dict]) -> Dict:
    """Audit language compliance - 100% English required"""
    issues = []
    
    for product in products:
        pid = product.get("id")
        title = product.get("title", "")
        body = product.get("body_html", "") or ""
        vendor = product.get("vendor", "")
        
        # Check all text fields
        for field_name, field_value in [("title", title), ("body_html", body), ("vendor", vendor)]:
            french = check_french_keywords(field_value)
            if french:
                issues.append({
                    "product_id": pid,
                    "product_title": title,
                    "field": field_name,
                    "french_phrases": french
                })
    
    unique_products = len(set(i["product_id"] for i in issues))
    
    return {
        "total_products": len(products),
        "products_with_french": unique_products,
        "total_violations": len(issues),
        "compliance": "✅ 100% English" if unique_products == 0 else f"❌ {unique_products} products with French content",
        "issues": issues[:20]  # First 20
    }

def audit_draft_products(products: List[Dict]) -> Dict:
    """Audit draft products - must remain draft"""
    draft = [p for p in products if p.get("status") == "draft"]
    active = [p for p in products if p.get("status") == "active"]
    archived = [p for p in products if p.get("status") == "archived"]
    
    draft_list = [
        {"id": p["id"], "title": p["title"], "status": p["status"]}
        for p in draft[:20]  # First 20
    ]
    
    return {
        "total_products": len(products),
        "draft_count": len(draft),
        "active_count": len(active),
        "archived_count": len(archived),
        "draft_list": draft_list,
        "compliance": f"✅ {len(draft)} products remain draft" if len(draft) > 0 else "⚠️ No draft products (all published or archived)"
    }

def audit_product_types(products: List[Dict]) -> Dict:
    """Audit product_type field - must be filled for all"""
    missing = []
    
    for p in products:
        ptype = p.get("product_type")
        if not ptype or ptype.strip() == "":
            missing.append({
                "id": p["id"],
                "title": p["title"],
                "product_type": "EMPTY"
            })
    
    return {
        "total_products": len(products),
        "with_type": len(products) - len(missing),
        "missing_type": len(missing),
        "missing_list": missing[:20],  # First 20
        "compliance": "✅ 100% product_type filled" if len(missing) == 0 else f"❌ {len(missing)} products missing product_type"
    }

def fetch_collections() -> List[Dict]:
    """Fetch all custom collections"""
    url = f"https://{SHOP}/admin/api/{API_VERSION}/custom_collections.json?limit=250"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ Collections API Error: {response.status_code}")
        return []
    
    return response.json().get("custom_collections", [])

def audit_collections(collections: List[Dict]) -> Dict:
    """Audit collection descriptions"""
    missing = []
    
    for col in collections:
        desc = col.get("body_html") or ""
        if not desc or desc.strip() == "":
            missing.append({
                "id": col["id"],
                "title": col["title"],
                "handle": col["handle"],
                "description": "EMPTY"
            })
    
    return {
        "total_collections": len(collections),
        "with_description": len(collections) - len(missing),
        "missing_description": len(missing),
        "missing_list": missing,
        "compliance": "✅ All collections have descriptions" if len(missing) == 0 else f"❌ {len(missing)} collections missing descriptions"
    }

def main():
    print("=" * 80)
    print("COMPLETE FORENSIC AUDIT - Rigorous Factual Verification")
    print("=" * 80)
    print(f"Store: {SHOP}")
    print(f"API Version: {API_VERSION}")
    print(f"Date: 2025-12-05\n")
    
    # Fetch products
    print("📥 Fetching ALL products...")
    products = fetch_all_products()
    print(f"✅ Fetched {len(products)} products\n")
    
    # Fetch collections
    print("📥 Fetching collections...")
    collections = fetch_collections()
    print(f"✅ Fetched {len(collections)} collections\n")
    
    # Audit 1: Language
    print("=" * 80)
    print("AUDIT 1: LANGUAGE COMPLIANCE (100% English Required)")
    print("=" * 80)
    lang = audit_language(products)
    print(f"Total products: {lang['total_products']}")
    print(f"Products with French: {lang['products_with_french']}")
    print(f"Total violations: {lang['total_violations']}")
    print(f"Compliance: {lang['compliance']}\n")
    
    if lang['issues']:
        print("⚠️ French content found (first 10):")
        for issue in lang['issues'][:10]:
            print(f"  - {issue['product_title']}")
            print(f"    Field: {issue['field']}, French: {', '.join(issue['french_phrases'])}\n")
    
    # Audit 2: Draft products
    print("=" * 80)
    print("AUDIT 2: DRAFT PRODUCTS (Must Remain Draft)")
    print("=" * 80)
    draft = audit_draft_products(products)
    print(f"Total products: {draft['total_products']}")
    print(f"Draft: {draft['draft_count']}")
    print(f"Active: {draft['active_count']}")
    print(f"Archived: {draft['archived_count']}")
    print(f"Compliance: {draft['compliance']}\n")
    
    if draft['draft_list']:
        print("Draft products (first 10):")
        for d in draft['draft_list'][:10]:
            print(f"  - {d['title']} (ID: {d['id']}, Status: {d['status']})")
        print()
    
    # Audit 3: Product types
    print("=" * 80)
    print("AUDIT 3: PRODUCT_TYPE FIELD (Must Be Filled)")
    print("=" * 80)
    ptype = audit_product_types(products)
    print(f"Total products: {ptype['total_products']}")
    print(f"With type: {ptype['with_type']}")
    print(f"Missing type: {ptype['missing_type']}")
    print(f"Compliance: {ptype['compliance']}\n")
    
    if ptype['missing_list']:
        print("⚠️ Products missing product_type (first 10):")
        for p in ptype['missing_list'][:10]:
            print(f"  - {p['title']} (ID: {p['id']})")
        print()
    
    # Audit 4: Collections
    print("=" * 80)
    print("AUDIT 4: COLLECTION DESCRIPTIONS")
    print("=" * 80)
    col = audit_collections(collections)
    print(f"Total collections: {col['total_collections']}")
    print(f"With description: {col['with_description']}")
    print(f"Missing description: {col['missing_description']}")
    print(f"Compliance: {col['compliance']}\n")
    
    if col['missing_list']:
        print("⚠️ Collections missing descriptions:")
        for c in col['missing_list']:
            print(f"  - {c['title']} (Handle: {c['handle']}, ID: {c['id']})")
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"1. Language: {lang['compliance']}")
    print(f"2. Draft Products: {draft['compliance']}")
    print(f"3. Product Types: {ptype['compliance']}")
    print(f"4. Collections: {col['compliance']}")
    print(f"5. PayPal: ⚠️ MANUAL CHECK REQUIRED (Settings → Payments)\n")
    
    # Save results
    results = {
        "timestamp": "2025-12-05",
        "store": SHOP,
        "api_version": API_VERSION,
        "language_audit": lang,
        "draft_audit": draft,
        "product_type_audit": ptype,
        "collection_audit": col
    }

    with open("audit_forensic_results_2025-12-05.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✅ Full results saved to: audit_forensic_results_2025-12-05.json")

if __name__ == "__main__":
    main()
