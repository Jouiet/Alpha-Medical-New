#!/usr/bin/env python3
"""
Install Google Tag Manager (GTM) for Alpha Medical Care
Installs GTM container code in theme.liquid
"""

import sys
import os
import re

# Check command line argument
if len(sys.argv) != 2:
    print("=" * 80)
    print("ERREUR: GTM Container ID manquant")
    print("=" * 80)
    print("\nUsage: python3 install_gtm.py GTM-XXXXXXX")
    print("\nExemple: python3 install_gtm.py GTM-ABC1234")
    print("\nPour obtenir votre GTM Container ID:")
    print("1. Allez sur: https://tagmanager.google.com/")
    print("2. Créez un nouveau container:")
    print("   - Nom: Alpha Medical Care")
    print("   - Type: Web")
    print("3. Une fois créé, copiez le Container ID (format: GTM-XXXXXXX)")
    print("4. Exécutez: python3 install_gtm.py GTM-XXXXXXX")
    print("=" * 80)
    sys.exit(1)

gtm_id = sys.argv[1]

# Validate format
if not re.match(r'^GTM-[A-Z0-9]{6,8}$', gtm_id):
    print(f"❌ ERREUR: Format invalide '{gtm_id}'")
    print(f"   Format attendu: GTM-XXXXXXX (6-8 caractères alphanumériques)")
    print(f"   Exemple valide: GTM-ABC1234")
    sys.exit(1)

print("=" * 80)
print("INSTALLATION GOOGLE TAG MANAGER (GTM)")
print("=" * 80)
print(f"\n✅ GTM Container ID validé: {gtm_id}")
print(f"   Store: Alpha Medical Care (azffej-as.myshopify.com)")

# Read theme.liquid
theme_liquid_path = 'layout/theme.liquid'

if not os.path.exists(theme_liquid_path):
    print(f"\n❌ ERREUR: {theme_liquid_path} introuvable")
    print("   Assurez-vous d'être dans le dossier Alpha-Medical/")
    sys.exit(1)

with open(theme_liquid_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if already installed
if gtm_id in content:
    print(f"\n⚠️  Le GTM {gtm_id} est DÉJÀ installé dans theme.liquid")
    print("   Aucune modification nécessaire.")
    sys.exit(0)

# Check if any GTM container exists
if 'GTM-' in content:
    existing_ids = re.findall(r'GTM-[A-Z0-9]{6,8}', content)
    print(f"\n⚠️  ATTENTION: GTM Container existant détecté: {existing_ids}")
    print("   Le nouveau container sera ajouté (pas de remplacement)")

# Create GTM head snippet
gtm_head_snippet = f"""<!-- Google Tag Manager (Alpha Medical Care) -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{gtm_id}');</script>
<!-- End Google Tag Manager -->"""

# Create GTM body snippet (noscript fallback)
gtm_body_snippet = f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={gtm_id}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

# Find </head> tag and insert before it
if '</head>' not in content:
    print("\n❌ ERREUR: Balise </head> introuvable dans theme.liquid")
    sys.exit(1)

# Find <body> tag and insert after it
if '<body' not in content:
    print("\n❌ ERREUR: Balise <body> introuvable dans theme.liquid")
    sys.exit(1)

# Insert GTM head code before </head>
new_content = content.replace('</head>', f'{gtm_head_snippet}\n</head>')

# Insert GTM body code after <body> tag
# Need to handle <body> with possible attributes like <body class="...">
body_pattern = r'(<body[^>]*>)'
new_content = re.sub(body_pattern, r'\1\n' + gtm_body_snippet, new_content)

# Backup original
backup_path = 'layout/theme.liquid.backup_gtm'
with open(backup_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Backup créé: {backup_path}")

# Write new content
with open(theme_liquid_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Google Tag Manager installé dans {theme_liquid_path}")
print(f"   - Head code: Inséré avant </head>")
print(f"   - Body code: Inséré après <body>")

# Final instructions
print("\n" + "=" * 80)
print("📋 ÉTAPES SUIVANTES REQUISES")
print("=" * 80)
print(f"""
1. ✅ GTM INSTALLÉ - Vérifier l'installation:
   - Allez sur: https://www.alphamedical.shop/
   - Ouvrez la console développeur (F12)
   - Tapez: dataLayer
   - Devrait afficher un array avec des objets GTM

2. CONFIGURER GOOGLE ADS TAG DANS GTM:
   - Allez sur: https://tagmanager.google.com/
   - Sélectionnez: Container {gtm_id}
   - Créez un nouveau tag:
     * Type: Google Ads Conversion Tracking
     * Conversion ID: AW-XXXXXXXXXX (de Google Ads)
     * Conversion Label: YYYYYYYYY (de Google Ads)
     * Trigger: Toutes les pages (All Pages) pour le pixel de base

   - Créez un tag de conversion Purchase:
     * Type: Google Ads Conversion Tracking
     * Conversion ID: AW-XXXXXXXXXX
     * Conversion Label: YYYYYYYYY
     * Conversion Value: {{{{Transaction Revenue}}}}
     * Transaction ID: {{{{Transaction ID}}}}
     * Trigger: Purchase (créez un trigger custom pour page confirmation)

3. CRÉER LES VARIABLES GTM:
   - Variables → Nouvelle variable utilisateur:
     * Transaction Revenue: Variable de couche de données (purchase.value)
     * Transaction ID: Variable de couche de données (purchase.transaction_id)

4. PUBLIER LE CONTAINER:
   - Vérifiez en mode Aperçu (Preview)
   - Cliquez "Envoyer" (Submit)
   - Créez une version: "v1.0 - Google Ads Conversion Tracking"

5. TESTER:
   - Créez une commande test sur le site
   - Vérifiez dans GTM → Mode Aperçu → Tags déclenchés
   - Vérifiez dans Google Ads → Conversions → Activité récente (24-48h délai)

6. GIT COMMIT:
   git add layout/theme.liquid
   git commit -m "feat(gtm): Install Google Tag Manager {gtm_id}"
   git push origin main

7. DOCUMENTATION:
   Mettez à jour ces fichiers avec les détails de l'installation:
   - AI_SEO_MARKETING_STRATEGIC_ANALYSIS_2025-2026.md
   - SEO_MARKETING_FORENSIC_ANALYSIS.md
""")

print("=" * 80)
print(f"✅ Installation de GTM {gtm_id} TERMINÉE")
print("   Suivez les étapes ci-dessus pour compléter la configuration")
print("=" * 80)
