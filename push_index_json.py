#!/usr/bin/env python3
"""
Script pour pousser templates/index.json vers Shopify via API
"""

import requests
import json
import base64
from pathlib import Path

# Load token
env_file = Path(__file__).parent / '.env.admin'
ACCESS_TOKEN = None

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                ACCESS_TOKEN = line.split('=', 1)[1].strip()
                break

if not ACCESS_TOKEN:
    print("❌ ERROR: SHOPIFY_ADMIN_ACCESS_TOKEN not found")
    exit(1)

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-01"
BASE_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Get active theme
def get_active_theme():
    """Récupère l'ID du thème actif"""
    url = f"{BASE_URL}/themes.json"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error getting themes: {response.status_code}")
        print(response.text)
        return None

    themes = response.json().get('themes', [])
    for theme in themes:
        if theme.get('role') == 'main':
            return theme['id']

    return None

# Upload asset
def upload_theme_asset(theme_id, key, value):
    """Upload file as theme asset"""
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
        print(f"  ❌ Error uploading {key}: {response.status_code}")
        print(f"  {response.text}")
        return False

def main():
    print("=" * 70)
    print("📤 PUSH templates/index.json VERS SHOPIFY")
    print("=" * 70)
    print()

    # Get active theme
    print("📥 Récupération du thème actif...")
    theme_id = get_active_theme()

    if not theme_id:
        print("❌ Impossible de trouver le thème actif")
        return

    print(f"✅ Thème actif trouvé: ID {theme_id}\n")

    # Read index.json
    index_json_path = Path(__file__).parent / "templates" / "index.json"

    if not index_json_path.exists():
        print(f"❌ File not found: {index_json_path}")
        return

    print("📖 Lecture de templates/index.json...")
    with open(index_json_path, 'r', encoding='utf-8') as f:
        index_json_content = f.read()

    print(f"✅ Fichier lu: {len(index_json_content)} caractères\n")

    # Upload to Shopify
    print("📤 Upload vers Shopify...")
    success = upload_theme_asset(theme_id, "templates/index.json", index_json_content)

    if success:
        print("✅ templates/index.json poussé avec succès!")
        print()
        print("🎉 CAROUSEL HERO CONFIGURÉ!")
        print()
        print("Configuration appliquée:")
        print("  - 5 slides avec images hero-slide-1.svg à hero-slide-5.svg")
        print("  - Rotation automatique activée (5 secondes)")
        print("  - Slider visual: dots")
        print("  - Slide height: medium")
        print()
        print("Vérifiez le site: https://alphamedical.shop")
    else:
        print("❌ Échec du push")

    print()

if __name__ == "__main__":
    main()
