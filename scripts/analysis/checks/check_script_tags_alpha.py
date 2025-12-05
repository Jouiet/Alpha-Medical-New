#!/usr/bin/env python3
"""
CHECK SCRIPT TAGS ON ALPHA MEDICAL
Identifies apps injecting tracking scripts (Conversios, Trakpilot, etc.)
"""

import requests
import json
import sys

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('/Users/mac/Desktop/Alpha-Medical/.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except Exception as e:
    print(f"❌ Failed to load credentials: {e}")
    sys.exit(1)

API_VERSION = "2025-10"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def check_script_tags():
    """Check for script tags (apps injecting JavaScript)"""
    url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/script_tags.json"

    try:
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            script_tags = response.json().get('script_tags', [])

            print("=" * 80)
            print("ALPHA MEDICAL - SCRIPT TAGS (APPS INJECTION)")
            print("=" * 80)
            print(f"Total script tags: {len(script_tags)}")
            print()

            if not script_tags:
                print("✅ No script tags found (good - native Shopify only)")
                return []

            for i, tag in enumerate(script_tags, 1):
                print(f"\n📜 SCRIPT TAG #{i}:")
                print(f"   ID: {tag.get('id')}")
                print(f"   Source: {tag.get('src')}")
                print(f"   Event: {tag.get('event')}")
                print(f"   Display Scope: {tag.get('display_scope')}")
                print(f"   Created: {tag.get('created_at')}")

                # Identify app
                src = tag.get('src', '').lower()
                if 'conversios' in src or 'tatvic' in src:
                    print("   🔍 App: Conversios (Google Analytics/Ads)")
                elif 'trakpilot' in src:
                    print("   🔍 App: Trakpilot")
                elif 'bundler' in src:
                    print("   🚨 App: BUNDLER.APP (EXTERNAL - TO REMOVE)")
                elif 'loox' in src:
                    print("   🔍 App: Loox (Reviews)")
                else:
                    print("   🔍 App: Unknown")

            return script_tags

        elif response.status_code == 404:
            print("⚠️  Script Tags API endpoint not found (404)")
            print("This might indicate limited API permissions")
            return []
        else:
            print(f"❌ Script tags API failed: {response.status_code}")
            print(response.text)
            return []

    except Exception as e:
        print(f"❌ Error fetching script tags: {e}")
        return []

def main():
    script_tags = check_script_tags()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if script_tags:
        print(f"\n⚠️  {len(script_tags)} external apps injecting scripts")
        print("\nRECOMMENDATION:")
        print("- Vérifier si Conversios/Trakpilot injecte GTM-MW2FN7MQ")
        print("- Si Bundler.app trouvé → DÉSINSTALLER (app externe)")
    else:
        print("\n✅ No external script injections OR API permission limited")

    print()

if __name__ == '__main__':
    main()
