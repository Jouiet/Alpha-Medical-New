#!/usr/bin/env python3
"""
Push templates/index.json vers Shopify
"""

import requests
from pathlib import Path
import json

# Load token
env_file = Path(__file__).parent / '.env.admin'
ACCESS_TOKEN = None

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                ACCESS_TOKEN = line.split('=', 1)[1].strip()
                break

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-10"
BASE_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def get_active_theme():
    """Récupère l'ID du thème actif"""
    url = f"{BASE_URL}/themes.json"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        return None

    themes = response.json().get('themes', [])
    for theme in themes:
        if theme.get('role') == 'main':
            return theme['id']
    return None

def upload_theme_asset(theme_id, key, value):
    """Upload asset to theme"""
    url = f"{BASE_URL}/themes/{theme_id}/assets.json"

    data = {
        "asset": {
            "key": key,
            "value": value
        }
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        return True
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        return False

def main():
    print("=" * 70)
    print("📤 PUSH templates/index.json VERS SHOPIFY")
    print("=" * 70)
    print()

    theme_id = get_active_theme()
    if not theme_id:
        print("❌ Theme not found")
        return

    print(f"✅ Thème actif: {theme_id}\n")

    # Read index.json
    index_path = Path(__file__).parent / "templates" / "index.json"

    if not index_path.exists():
        print(f"❌ File not found: {index_path}")
        return

    print("📖 Lecture de templates/index.json...")
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    print(f"✅ Fichier lu: {len(index_content)} caractères\n")

    # Push to Shopify
    print("📤 Upload vers Shopify...")
    success = upload_theme_asset(theme_id, "templates/index.json", index_content)

    if success:
        print("✅ templates/index.json poussé avec succès!")
        print()
        print("🎉 HEADING SIZE CHANGÉ À h2 (small) POUR LES 15 SLIDES!")
    else:
        print("❌ Échec du push")

    print()

if __name__ == "__main__":
    main()
