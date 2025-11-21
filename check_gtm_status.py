#!/usr/bin/env python3
"""
Check GTM (Google Tag Manager) Status for Alpha Medical
Verifies if GTM is installed and provides next steps
"""

import requests
import re
import os

print("=" * 80)
print("VÉRIFICATION STATUT GOOGLE TAG MANAGER (GTM)")
print("=" * 80)

store_url = "https://www.alphamedical.shop"
theme_liquid_path = 'layout/theme.liquid'

# 1. Check live website
print("\n🔍 Vérification du site live...")
print(f"   URL: {store_url}")

try:
    response = requests.get(store_url, timeout=10)
    html = response.text

    # Search for GTM container ID
    gtm_matches = re.findall(r'GTM-[A-Z0-9]{6,8}', html)

    if gtm_matches:
        unique_gtm = list(set(gtm_matches))
        print(f"\n✅ GTM DÉTECTÉ sur le site:")
        for gtm_id in unique_gtm:
            count = gtm_matches.count(gtm_id)
            print(f"   - {gtm_id} ({count} occurrences)")

        # Check dataLayer
        if 'dataLayer' in html:
            print(f"\n✅ dataLayer détecté")

            # Check for dataLayer.push
            datalayer_pushes = html.count('dataLayer.push')
            if datalayer_pushes > 0:
                print(f"✅ dataLayer.push() trouvé ({datalayer_pushes} occurrences)")
        else:
            print(f"\n⚠️  dataLayer NON détecté (peut être chargé dynamiquement)")
    else:
        print(f"\n❌ AUCUN GTM détecté sur le site")
        print(f"   Pattern recherché: GTM-XXXXXXX")

except Exception as e:
    print(f"\n❌ Erreur lors de la vérification du site: {e}")

# 2. Check theme.liquid file
print("\n" + "-" * 80)
print("🔍 Vérification du fichier theme.liquid...")

if os.path.exists(theme_liquid_path):
    with open(theme_liquid_path, 'r', encoding='utf-8') as f:
        theme_content = f.read()

    # Search for GTM in theme
    gtm_in_theme = re.findall(r'GTM-[A-Z0-9]{6,8}', theme_content)

    if gtm_in_theme:
        unique_gtm_theme = list(set(gtm_in_theme))
        print(f"\n✅ GTM trouvé dans theme.liquid:")
        for gtm_id in unique_gtm_theme:
            print(f"   - {gtm_id}")

        # Check both head and body code
        has_head_code = 'googletagmanager.com/gtm.js' in theme_content
        has_body_code = 'googletagmanager.com/ns.html' in theme_content

        print(f"\nVérification de l'installation complète:")
        print(f"   {'✅' if has_head_code else '❌'} Head code (gtm.js)")
        print(f"   {'✅' if has_body_code else '❌'} Body code (noscript)")

        if has_head_code and has_body_code:
            print(f"\n✅ Installation GTM COMPLÈTE")
        else:
            print(f"\n⚠️  Installation GTM INCOMPLÈTE")
    else:
        print(f"\n❌ AUCUN GTM trouvé dans theme.liquid")
else:
    print(f"\n⚠️  Fichier {theme_liquid_path} introuvable")
    print(f"   Assurez-vous d'être dans le dossier Alpha-Medical/")

# 3. Check for backup files
print("\n" + "-" * 80)
print("🔍 Vérification des backups GTM...")

backup_files = [
    'layout/theme.liquid.backup_gtm',
    'layout/theme.liquid.backup_google_ads'
]

for backup_path in backup_files:
    if os.path.exists(backup_path):
        print(f"✅ Backup trouvé: {backup_path}")

        # Check if backup has GTM
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()

        gtm_in_backup = re.findall(r'GTM-[A-Z0-9]{6,8}', backup_content)
        if gtm_in_backup:
            print(f"   Contenait GTM: {list(set(gtm_in_backup))}")

# 4. Final status and recommendations
print("\n" + "=" * 80)
print("📋 STATUT FINAL ET PROCHAINES ÉTAPES")
print("=" * 80)

# Determine current status
site_has_gtm = len(gtm_matches) > 0 if 'gtm_matches' in locals() else False
theme_has_gtm = len(gtm_in_theme) > 0 if 'gtm_in_theme' in locals() and gtm_in_theme else False

if site_has_gtm and theme_has_gtm:
    print("\n✅ STATUT: GTM DÉJÀ INSTALLÉ ET ACTIF")
    print(f"   Container ID: {unique_gtm[0] if unique_gtm else 'INCONNU'}")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   1. Vérifiez les tags configurés dans GTM:")
    print("      → https://tagmanager.google.com/")
    print(f"      → Container: {unique_gtm[0] if unique_gtm else 'Votre GTM ID'}")
    print("\n   2. Si Google Ads tag n'est PAS configuré:")
    print("      → Suivez: GTM_SETUP_GUIDE.md ÉTAPE 4")
    print("      → Configurez: Google Ads Base Pixel + Purchase Conversion")
    print("\n   3. Testez avec mode Preview:")
    print("      → GTM → Aperçu → Connectez votre site")
    print("      → Créez une commande test")
    print("      → Vérifiez que les tags se déclenchent")

elif theme_has_gtm and not site_has_gtm:
    print("\n⚠️  STATUT: GTM INSTALLÉ MAIS NON ACTIF")
    print(f"   Container ID: {unique_gtm_theme[0]}")
    print("   Problème: Code présent dans theme.liquid mais pas chargé sur le site")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("   1. Videz le cache Shopify:")
    print("      → Admin → Online Store → Themes")
    print("      → Actions → Edit code → Ctrl+S (ou Cmd+S)")
    print("\n   2. Attendez 2-3 minutes et re-testez:")
    print("      → python3 check_gtm_status.py")
    print("\n   3. Si toujours pas actif:")
    print("      → Vérifiez bloqueurs de publicité")
    print("      → Testez en navigation privée")

else:
    print("\n❌ STATUT: GTM NON INSTALLÉ")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("\n1. CRÉER UN CONTAINER GTM:")
    print("   → Allez sur: https://tagmanager.google.com/")
    print("   → Créez un nouveau container:")
    print("     * Nom: Alpha Medical Care")
    print("     * Type: Web")
    print("   → Copiez le Container ID (format: GTM-XXXXXXX)")
    print("\n2. INSTALLER GTM:")
    print("   → Exécutez: python3 install_gtm.py GTM-XXXXXXX")
    print("   → Le script installera automatiquement GTM dans theme.liquid")
    print("\n3. VÉRIFIER L'INSTALLATION:")
    print("   → Exécutez: python3 check_gtm_status.py")
    print("   → Devrait afficher: ✅ GTM DÉJÀ INSTALLÉ ET ACTIF")
    print("\n4. CONFIGURER GOOGLE ADS:")
    print("   → Suivez: GTM_SETUP_GUIDE.md ÉTAPE 4")
    print("\n📖 GUIDE COMPLET: Consultez GTM_SETUP_GUIDE.md")

print("\n" + "=" * 80)
