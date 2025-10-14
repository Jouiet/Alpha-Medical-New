#!/usr/bin/env python3
"""
Script pour uploader les images Hero SVG vers Shopify Theme Assets
"""

import requests
import base64
import json
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

# Upload SVG image as theme asset
def upload_theme_asset(theme_id, filename, svg_content):
    """Upload SVG file as theme asset"""
    url = f"{BASE_URL}/themes/{theme_id}/assets.json"

    # Encode SVG content to base64
    svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')

    data = {
        "asset": {
            "key": f"assets/{filename}",
            "attachment": svg_base64
        }
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        return True
    else:
        print(f"  ❌ Error uploading {filename}: {response.status_code}")
        print(f"  {response.text}")
        return False

def main():
    print("=" * 70)
    print("🖼️  UPLOAD IMAGES HERO VERS SHOPIFY THEME ASSETS")
    print("=" * 70)
    print()

    # Get active theme
    print("📥 Récupération du thème actif...")
    theme_id = get_active_theme()

    if not theme_id:
        print("❌ Impossible de trouver le thème actif")
        return

    print(f"✅ Thème actif trouvé: ID {theme_id}\n")

    # Select top 5 SVG images to upload
    hero_images = [
        "1.svg",                    # 2.2M - main image
        "Design sans titre.svg",    # 1.9M
        "Design sans titre10.svg",  # 1.4M
        "Design sans titre4.svg",   # 713K
        "Design sans titre5.svg"    # 524K
    ]

    images_dir = Path(__file__).parent / "Images" / "Hero"

    success_count = 0
    fail_count = 0

    for i, img_filename in enumerate(hero_images, 1):
        print(f"{i}/{len(hero_images)}. Upload {img_filename}...")

        img_path = images_dir / img_filename

        if not img_path.exists():
            print(f"  ❌ File not found: {img_path}")
            fail_count += 1
            continue

        # Read SVG content
        with open(img_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()

        # Generate clean filename for Shopify
        clean_filename = f"hero-slide-{i}.svg"

        # Upload to Shopify
        success = upload_theme_asset(theme_id, clean_filename, svg_content)

        if success:
            print(f"  ✅ SUCCESS: {clean_filename}")
            success_count += 1
        else:
            fail_count += 1

        print()

    print("=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    print(f"✅ Images uploadées: {success_count}/{len(hero_images)}")
    print(f"❌ Échecs: {fail_count}/{len(hero_images)}")
    print()

    if success_count == len(hero_images):
        print("🎉 TOUS LES UPLOADS RÉUSSIS!")
        print()
        print("Images disponibles dans le thème:")
        for i in range(1, len(hero_images) + 1):
            print(f"  - hero-slide-{i}.svg")

    print()

if __name__ == "__main__":
    main()
