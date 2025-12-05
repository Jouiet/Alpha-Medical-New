#!/usr/bin/env python3
"""
VÉRIFICATION DES CORRECTIONS APPLIQUÉES
"""

import os
import sys
import requests
from dotenv import load_dotenv

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
load_dotenv(os.path.join(root_dir, '.env.admin'))

DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

# Expected corrected handles
EXPECTED_HANDLES = [
    'electric-massage-cushion-full-body',
    'bunion-corrector-toe-separator',
    'ergonomic-massage-recliner-chair',
    'shiatsu-massage-chair-full-body',
    'electric-leg-massager-air-compression',
]

def check_handle_exists(handle):
    """Vérifie qu'un handle existe via API"""
    url = f'https://{DOMAIN}/admin/api/{API_VERSION}/products.json'
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    params = {'handle': handle, 'fields': 'id,title,handle,status'}

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    products = response.json()['products']
    return products[0] if products else None

def check_bundleautocreation():
    """Vérifie que BundleAutoCreation.gs n'a plus de token hardcodé"""
    filepath = os.path.join(root_dir, 'BundleAutoCreation.gs')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for hardcoded token declaration
    if "const SHOPIFY_ADMIN_ACCESS_TOKEN = 'shpat_" in content:
        return False, "❌ Token hardcodé trouvé dans la déclaration const"

    # Check for PropertiesService usage
    if 'getShopifyToken()' not in content:
        return False, "❌ getShopifyToken() non trouvé"

    if 'PropertiesService.getScriptProperties()' not in content:
        return False, "❌ PropertiesService non utilisé"

    return True, "✅ Code sécurisé (PropertiesService)"

def main():
    print("=" * 80)
    print("VÉRIFICATION DES CORRECTIONS APPLIQUÉES")
    print("=" * 80)
    print()

    # 1. Vérifier les URLs produits
    print("📋 CORRECTION #1: URLs Produits")
    print()

    urls_ok = 0
    for handle in EXPECTED_HANDLES:
        product = check_handle_exists(handle)

        if product and product['status'] == 'active':
            print(f"✅ {handle}")
            print(f"   Title: {product['title'][:60]}...")
            urls_ok += 1
        else:
            print(f"❌ {handle} - NOT FOUND or NOT PUBLISHED")

        print()

    # 2. Vérifier BundleAutoCreation.gs
    print("=" * 80)
    print("📋 CORRECTION #2: BundleAutoCreation.gs Security")
    print()

    security_ok, message = check_bundleautocreation()
    print(message)
    print()

    # 3. Résumé
    print("=" * 80)
    print("RÉSUMÉ")
    print("=" * 80)
    print(f"URLs Produits: {urls_ok}/{len(EXPECTED_HANDLES)} ✅")
    print(f"Code Security: {'✅' if security_ok else '❌'}")
    print()

    if urls_ok == len(EXPECTED_HANDLES) and security_ok:
        print("🎉 TOUTES LES CORRECTIONS VÉRIFIÉES!")
        print()
        print("📌 ACTIONS RESTANTES:")
        print("   1. Vérifier redirections 301: Shopify Admin → Navigation → URL Redirects")
        print("   2. Si déploiement Google Apps Script prévu:")
        print("      → Configurer token via File → Project properties → Script properties")
        return 0
    else:
        print("⚠️ Certaines vérifications ont échoué")
        return 1

if __name__ == '__main__':
    sys.exit(main())
