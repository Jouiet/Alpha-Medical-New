#!/usr/bin/env python3
"""
Push sections/slideshow.liquid modifié vers Shopify
"""

import requests
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
    print("📤 PUSH sections/slideshow.liquid VERS SHOPIFY")
    print("=" * 70)
    print()

    theme_id = get_active_theme()
    if not theme_id:
        print("❌ Theme not found")
        return

    print(f"✅ Thème actif: {theme_id}\n")

    # Read slideshow.liquid
    slideshow_path = Path(__file__).parent / "sections" / "slideshow.liquid"

    if not slideshow_path.exists():
        print(f"❌ File not found: {slideshow_path}")
        return

    print("📖 Lecture de sections/slideshow.liquid...")
    with open(slideshow_path, 'r', encoding='utf-8') as f:
        slideshow_content = f.read()

    print(f"✅ Fichier lu: {len(slideshow_content)} caractères\n")

    # Push to Shopify
    print("📤 Upload vers Shopify...")
    success = upload_theme_asset(theme_id, "sections/slideshow.liquid", slideshow_content)

    if success:
        print("✅ sections/slideshow.liquid poussé avec succès!")
        print()
        print("🎉 LIMITE DE SLIDES AUGMENTÉE À 20!")
        print()
        print("⚠️  NEXT: Configurer templates/index.json avec 15 slides")
    else:
        print("❌ Échec du push")

    print()

if __name__ == "__main__":
    main()
