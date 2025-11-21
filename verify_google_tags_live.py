#!/usr/bin/env python3
"""
VERIFICATION: Google Tags on Live Site
Checks what Google Ads tags are actually loading on alphamedical.shop
"""

import requests
import re
import sys

SITE_URL = "https://www.alphamedical.shop"

def check_google_tags():
    """Check what Google tags are present on live site"""

    print(f"🔍 VERIFICATION: Google Tags sur {SITE_URL}\n")
    print("=" * 70)

    try:
        # Fetch homepage
        response = requests.get(SITE_URL, timeout=10)
        html = response.text

        print(f"✅ Site accessible: {response.status_code}\n")

        # Check 1: GTM Container
        gtm_ids = re.findall(r'GTM-[A-Z0-9]{6,8}', html)
        if gtm_ids:
            print(f"✅ GTM DÉTECTÉ: {', '.join(set(gtm_ids))}")
        else:
            print("❌ GTM NON DÉTECTÉ")
            return False

        print()

        # Check 2: Google Ads Conversion ID
        # Pattern 1: gtag('config', 'AW-XXXXXXXXXX')
        config_pattern = r"gtag\(['\"]config['\"]\s*,\s*['\"]AW-(\d+)['\"]"
        config_matches = re.findall(config_pattern, html)

        # Pattern 2: gtag('event', 'conversion', {'send_to': 'AW-XXXXXXXXXX/YYYYY'})
        conversion_pattern = r"['\"]send_to['\"]\s*:\s*['\"]AW-(\d+)/([^'\"]+)['\"]"
        conversion_matches = re.findall(conversion_pattern, html)

        # Pattern 3: Google Tag directly (https://www.googletagmanager.com/gtag/js?id=AW-XXXXX)
        gtag_script_pattern = r'googletagmanager\.com/gtag/js\?id=AW-(\d+)'
        gtag_script_matches = re.findall(gtag_script_pattern, html)

        # Pattern 4: GT- tag (Google Tag format)
        gt_pattern = r'GT-[A-Z0-9]+'
        gt_matches = re.findall(gt_pattern, html)

        print("📊 ANALYSE DES TAGS GOOGLE ADS:\n")

        # Report Config tags (Base Pixel)
        if config_matches or gtag_script_matches:
            print("✅ GOOGLE TAG (BASE) DÉTECTÉ:")
            if gtag_script_matches:
                for match in set(gtag_script_matches):
                    print(f"   - Script source: AW-{match}")
            if config_matches:
                for match in set(config_matches):
                    print(f"   - Config call: AW-{match}")
            print()
        else:
            print("⚠️  GOOGLE TAG (BASE) NON DÉTECTÉ dans le HTML")
            print("   → Possible auto-loading par GTM (April 2025 feature)")
            print()

        # Report Conversion tags
        if conversion_matches:
            print("✅ GOOGLE ADS CONVERSION TAG DÉTECTÉ:")
            for conv_id, label in set(conversion_matches):
                print(f"   - Conversion ID: AW-{conv_id}")
                print(f"   - Conversion Label: {label}")
            print()
        else:
            print("❌ GOOGLE ADS CONVERSION TAG NON DÉTECTÉ")
            print()

        # Report GT tags
        if gt_matches:
            print(f"✅ GOOGLE TAG (GT-) DÉTECTÉ: {', '.join(set(gt_matches))}")
            print()

        # Check 3: dataLayer
        if 'dataLayer' in html or 'window.dataLayer' in html:
            print("✅ dataLayer DÉTECTÉ")
        else:
            print("⚠️  dataLayer NON DÉTECTÉ")

        print()
        print("=" * 70)
        print("\n📋 RÉSUMÉ:\n")

        # Summary
        has_gtm = bool(gtm_ids)
        has_base = bool(config_matches or gtag_script_matches)
        has_conversion = bool(conversion_matches)
        has_datalayer = 'dataLayer' in html

        if has_gtm and has_conversion and has_datalayer:
            print("✅ CONFIGURATION MINIMALE: OK")
            print("   - GTM installé ✅")
            print("   - Conversion tracking configuré ✅")
            print("   - dataLayer présent ✅")
            print()

            if has_base:
                print("✅ CONFIGURATION COMPLÈTE: OK")
                print("   - Google Tag (base) présent ✅")
                print()
                print("🎯 RÉSULTAT: Setup COMPLET et OPTIMAL")
            else:
                print("⚠️  Google Tag (base) NON VISIBLE dans HTML")
                print()
                print("💡 DEUX POSSIBILITÉS:")
                print("   1. GTM auto-loading actif (April 2025 feature)")
                print("   2. Tag manquant → À créer manuellement")
                print()
                print("🎯 RECOMMANDATION: Créer Google Tag (base) manuellement")
                print("   → Meilleur contrôle et performance")
                print("   → Best practice 2025")
        else:
            print("❌ CONFIGURATION INCOMPLÈTE:")
            if not has_gtm:
                print("   - GTM manquant ❌")
            if not has_conversion:
                print("   - Conversion tracking manquant ❌")
            if not has_datalayer:
                print("   - dataLayer manquant ❌")

        print()
        print("=" * 70)

        # Expected values
        print("\n📌 VALEURS ATTENDUES:\n")
        print("   Conversion ID: AW-17749024238")
        print("   Conversion Label: gm87CKudp8QbEO67so9C")
        print("   GTM Container: GTM-WFPH2KZP")
        print()

        return has_gtm and has_conversion

    except requests.RequestException as e:
        print(f"❌ ERREUR: Impossible d'accéder au site: {e}")
        return False
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        return False

if __name__ == "__main__":
    success = check_google_tags()
    sys.exit(0 if success else 1)
