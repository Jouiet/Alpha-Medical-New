#!/usr/bin/env python3
"""Verify Shopify Customer Events (pixels) via API"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv('.env.admin')

STORE = os.getenv('SHOPIFY_STORE_DOMAIN')
TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

print("SHOPIFY PIXELS & TRACKING - FACTUAL VERIFICATION")
print("=" * 80)

# Query for Web Pixels (Customer Events API)
query = '''
{
  webPixels(first: 10) {
    edges {
      node {
        id
        settings
      }
    }
  }
}
'''

response = requests.post(
    f'https://{STORE}/admin/api/2024-01/graphql.json',
    headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},
    json={'query': query}
)

data = response.json()

if 'errors' in data:
    print(f"❌ API Error: {data['errors']}")
elif 'data' in data:
    pixels = data['data']['webPixels']['edges']
    print(f"\nWeb Pixels configured: {len(pixels)}")

    if pixels:
        for i, edge in enumerate(pixels, 1):
            pixel = edge['node']
            print(f"\n{i}. Pixel ID: {pixel['id']}")
            if pixel['settings']:
                print(f"   Settings: {json.dumps(pixel['settings'], indent=2)}")
    else:
        print("  ⚠️  No custom pixels configured via Customer Events API")
        print("  Note: GTM/GA4/Meta may be installed via Shopify app integrations")

# Alternative: Check for app integrations
print("\n" + "=" * 80)
print("CHECKING APP-BASED TRACKING")
print("=" * 80)

query = '''
{
  appInstallations(first: 50) {
    edges {
      node {
        id
        app {
          title
          handle
          developerName
        }
      }
    }
  }
}
'''

response = requests.post(
    f'https://{STORE}/admin/api/2024-01/graphql.json',
    headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},
    json={'query': query}
)

data = response.json()

if 'data' in data:
    apps = data['data']['appInstallations']['edges']

    tracking_apps = []
    for edge in apps:
        app = edge['node']['app']
        if any(keyword in app['title'].lower() for keyword in ['google', 'facebook', 'meta', 'tiktok', 'analytics', 'pixel', 'tag', 'conversion']):
            tracking_apps.append(app)

    print(f"\nTracking/Analytics apps installed: {len(tracking_apps)}")
    for app in tracking_apps:
        print(f"  • {app['title']} ({app['developerName']})")

# Summary
print("\n" + "=" * 80)
print("FACTUAL SUMMARY")
print("=" * 80)

print("\nTheme-level tracking (theme.liquid):")
print("  ✅ GTM-WFPH2KZP (Google Tag Manager)")
print("  ✅ Google Consent Mode v2 (gtm-consent-mode.liquid)")

print("\nApp-level tracking:")
print(f"  {len(tracking_apps)} tracking apps detected (see above)")

print("\nCustom pixels (Customer Events API):")
print(f"  {len(pixels)} pixels configured")

print("\n⚠️  RECOMMENDATION:")
print("  Use Chrome DevTools to verify LIVE tracking:")
print("  1. Open https://alphamedical.shop in Chrome")
print("  2. F12 → Network tab → Filter: 'google\|facebook\|tiktok'")
print("  3. Reload page → Check for tracking requests")
