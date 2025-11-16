#!/usr/bin/env python3
"""
EXTRACT ALPHA MEDICAL TRACKING IDs FROM LIVE SITE
Identifies GTM, GA4, Google Ads IDs to configure Trakpilot correctly
"""

import requests
import re
import json

def extract_tracking_ids():
    """Fetch and extract all Google tracking IDs from Alpha Medical"""

    url = "https://www.alphamedical.shop"

    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

        html = response.text

        print("=" * 80)
        print("ALPHA MEDICAL TRACKING IDs EXTRACTION")
        print("=" * 80)
        print(f"Source: {url}")
        print()

        # Patterns to search for
        patterns = {
            'GTM': r'GTM-[A-Z0-9]{6,8}',
            'GA4_G': r'G-[A-Z0-9]{10}',
            'GA4_GT': r'GT-[A-Z0-9]{8}',
            'Google_Ads': r'AW-[0-9]{10,12}',
            'Merchant_Center': r'MC-[A-Z0-9]{10}',
        }

        found_ids = {}

        for name, pattern in patterns.items():
            matches = re.findall(pattern, html)
            if matches:
                # Remove duplicates and sort
                unique_matches = sorted(set(matches))
                found_ids[name] = unique_matches

                print(f"✅ {name}:")
                for match in unique_matches:
                    print(f"   - {match}")
                print()

        # Search for dataLayer configurations
        print("🔍 SEARCHING FOR DATALAYER CONFIGURATIONS:")
        print("-" * 80)

        datalayer_matches = re.findall(r'dataLayer\.push\((.*?)\);', html, re.DOTALL)
        if datalayer_matches:
            print(f"Found {len(datalayer_matches)} dataLayer.push() calls")

            # Extract tracking IDs from dataLayer
            for dl in datalayer_matches[:3]:  # Show first 3
                if 'gtag' in dl or 'config' in dl:
                    print(f"Sample: {dl[:200]}...")

        print()

        # Search for gtag() calls
        print("🔍 SEARCHING FOR GTAG() CALLS:")
        print("-" * 80)

        gtag_configs = re.findall(r'gtag\(["\']config["\']\s*,\s*["\']([^"\']+)["\']', html)
        if gtag_configs:
            unique_configs = sorted(set(gtag_configs))
            print(f"Found {len(unique_configs)} gtag('config', ...) calls:")
            for config in unique_configs:
                print(f"   - {config}")

        print()

        # Summary for Trakpilot
        print("=" * 80)
        print("📋 TRAKPILOT CONFIGURATION GUIDE - ALPHA MEDICAL")
        print("=" * 80)
        print()

        print("Pour le formulaire Trakpilot, utilise:")
        print()

        if 'GTM' in found_ids:
            print(f"🏷️  Google Tag Manager Account:")
            print(f"   Cherche: Alpha Medical / {found_ids['GTM'][0]}")
            print(f"   PAS MyDealz / 6233895153 ❌")
            print()
        else:
            print("⚠️  GTM Account: Aucun GTM-XXXXXXX trouvé")
            print("   Utilise le dropdown pour chercher 'Alpha Medical'")
            print()

        if 'GA4_G' in found_ids or 'GA4_GT' in found_ids:
            print(f"📊 GA4 Measurement ID:")
            if 'GA4_G' in found_ids:
                print(f"   → {found_ids['GA4_G'][0]}")
            if 'GA4_GT' in found_ids:
                print(f"   (Alternative: {found_ids['GA4_GT'][0]})")
            print()
        else:
            print("⚠️  GA4 Measurement ID: Aucun trouvé")
            print()

        if 'Google_Ads' in found_ids:
            print(f"💰 Google Ads Account:")
            print(f"   → {found_ids['Google_Ads'][0]}")
            print()
        else:
            print("⚠️  Google Ads Account: Aucun trouvé")
            print()

        print("=" * 80)

        # Save to file
        output_file = '/Users/mac/Desktop/Alpha-Medical/alpha_tracking_ids.json'
        with open(output_file, 'w') as f:
            json.dump({
                'store': 'Alpha Medical',
                'url': url,
                'tracking_ids': found_ids,
                'gtag_configs': gtag_configs if gtag_configs else []
            }, f, indent=2)

        print(f"\n✅ Results saved to: alpha_tracking_ids.json")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    extract_tracking_ids()
