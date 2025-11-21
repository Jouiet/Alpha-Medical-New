#!/usr/bin/env python3
"""
Install Google Ads Conversion Tracking Pixel
Installs gtag.js with conversion tracking for Alpha Medical Care
Customer ID: 128-734-6786
"""

import sys
import os
import re

# Check command line argument
if len(sys.argv) != 2:
    print("=" * 80)
    print("ERREUR: Conversion ID manquant")
    print("=" * 80)
    print("\nUsage: python3 install_google_ads_pixel.py AW-XXXXXXXXXX")
    print("\nExemple: python3 install_google_ads_pixel.py AW-1234567890")
    print("\nPour obtenir votre Conversion ID:")
    print("1. Allez sur https://ads.google.com/")
    print("2. Compte: Alpha Medical Care (128-734-6786)")
    print("3. Outils et paramètres → Mesure → Conversions")
    print("4. Cliquez sur votre conversion → Installer le tag")
    print("5. Copiez le code AW-XXXXXXXXXX")
    print("=" * 80)
    sys.exit(1)

conversion_id = sys.argv[1]

# Validate format
if not re.match(r'^AW-\d{10,12}$', conversion_id):
    print(f"❌ ERREUR: Format invalide '{conversion_id}'")
    print(f"   Format attendu: AW-XXXXXXXXXX (10-12 chiffres)")
    print(f"   Exemple valide: AW-1234567890")
    sys.exit(1)

print("=" * 80)
print("INSTALLATION GOOGLE ADS CONVERSION TRACKING PIXEL")
print("=" * 80)
print(f"\n✅ Conversion ID validé: {conversion_id}")
print(f"   Compte Google Ads: Alpha Medical Care (128-734-6786)")

# Read theme.liquid
theme_liquid_path = 'layout/theme.liquid'

if not os.path.exists(theme_liquid_path):
    print(f"\n❌ ERREUR: {theme_liquid_path} introuvable")
    print("   Assurez-vous d'être dans le dossier Alpha-Medical/")
    sys.exit(1)

with open(theme_liquid_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if already installed
if conversion_id in content:
    print(f"\n⚠️  Le pixel {conversion_id} est DÉJÀ installé dans theme.liquid")
    print("   Aucune modification nécessaire.")
    sys.exit(0)

# Check if any Google Ads pixel exists
if 'AW-' in content:
    existing_ids = re.findall(r'AW-\d{10,12}', content)
    print(f"\n⚠️  ATTENTION: Pixel Google Ads existant détecté: {existing_ids}")
    print("   Le nouveau pixel sera ajouté (pas de remplacement)")

# Create Google Ads gtag.js snippet
google_ads_snippet = f"""
<!-- Google Ads Conversion Tracking - Alpha Medical Care -->
<!-- Customer ID: 128-734-6786 | Conversion ID: {conversion_id} -->
<script async src="https://www.googletagmanager.com/gtag/js?id={conversion_id}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', '{conversion_id}');
</script>
<!-- End Google Ads Conversion Tracking -->
"""

# Find </head> tag and insert before it
if '</head>' not in content:
    print("\n❌ ERREUR: Balise </head> introuvable dans theme.liquid")
    sys.exit(1)

# Insert before </head>
new_content = content.replace('</head>', f'{google_ads_snippet}\n</head>')

# Backup original
backup_path = 'layout/theme.liquid.backup_google_ads'
with open(backup_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Backup créé: {backup_path}")

# Write new content
with open(theme_liquid_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Pixel Google Ads installé dans {theme_liquid_path}")

# Create conversion tracking snippets for Shopify
print("\n" + "-" * 80)
print("CRÉATION DES SNIPPETS DE CONVERSION SHOPIFY")
print("-" * 80)

# Purchase conversion (Order confirmation page)
purchase_snippet = f"""<!-- Google Ads Purchase Conversion -->
<script>
  gtag('event', 'conversion', {{
    'send_to': '{conversion_id}/CONVERSION_LABEL',
    'value': {'{{'}}{{{{ order.total_price | money_without_currency }}}}{{'}}'}},
    'currency': '{'{{'}}{{{{ order.currency }}}}{{'}}'}},
    'transaction_id': '{'{{'}}{{{{ order.order_number }}}}{{'}}'}}'
  }});
</script>"""

# Add to cart conversion (optional)
add_to_cart_snippet = f"""<!-- Google Ads Add to Cart Event -->
<script>
  gtag('event', 'add_to_cart', {{
    'send_to': '{conversion_id}'
  }});
</script>"""

# Save snippets to files
snippets_dir = 'snippets'
if not os.path.exists(snippets_dir):
    os.makedirs(snippets_dir)

# Save purchase conversion snippet
purchase_snippet_path = f'{snippets_dir}/google-ads-purchase-conversion.liquid'
with open(purchase_snippet_path, 'w', encoding='utf-8') as f:
    f.write(purchase_snippet)

print(f"\n✅ Snippet créé: {purchase_snippet_path}")
print(f"   Usage: {{% render 'google-ads-purchase-conversion' %}}")
print(f"   Emplacement: templates/checkout-confirmation.liquid ou order-status page")

# Save add to cart snippet
add_to_cart_snippet_path = f'{snippets_dir}/google-ads-add-to-cart.liquid'
with open(add_to_cart_snippet_path, 'w', encoding='utf-8') as f:
    f.write(add_to_cart_snippet)

print(f"\n✅ Snippet créé: {add_to_cart_snippet_path}")
print(f"   Usage: Ajouter JavaScript listener sur boutons 'Add to Cart'")

# Final instructions
print("\n" + "=" * 80)
print("📋 ÉTAPES SUIVANTES REQUISES")
print("=" * 80)
print("""
1. ⚠️  OBTENIR LE CONVERSION LABEL:
   - Allez sur https://ads.google.com/
   - Outils et paramètres → Conversions
   - Cliquez sur votre conversion "Purchase"
   - Dans le code tag, cherchez: 'send_to': 'AW-XXXXXXXXXX/YYYYYYYYY'
   - Copiez la partie après le / (YYYYYYYYY = Conversion Label)

2. ÉDITER LE SNIPPET:
   - Ouvrez: snippets/google-ads-purchase-conversion.liquid
   - Remplacez CONVERSION_LABEL par le label obtenu (étape 1)

3. AJOUTER LE SNIPPET À LA PAGE DE CONFIRMATION:
   Option A (Shopify Plus):
   - Éditez: templates/checkout-confirmation.liquid
   - Ajoutez: {% render 'google-ads-purchase-conversion' %}

   Option B (Shopify Standard):
   - Settings → Checkout → Additional scripts
   - Collez le code du snippet (sans les balises Liquid)

4. TESTER:
   - Créez une commande test
   - Vérifiez dans Google Ads → Conversions → Activité récente
   - Délai: 24-48h pour voir les premières données

5. GIT COMMIT:
   git add layout/theme.liquid snippets/google-ads-*.liquid
   git commit -m "feat(google-ads): Install conversion tracking pixel"
   git push origin main
""")

print("=" * 80)
print(f"✅ Installation du pixel {conversion_id} TERMINÉE")
print("   Suivez les étapes ci-dessus pour compléter la configuration")
print("=" * 80)
