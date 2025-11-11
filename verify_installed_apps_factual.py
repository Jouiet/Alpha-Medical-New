#!/usr/bin/env python3
"""
VERIFY INSTALLED APPS - FACTUAL - Alpha Medical Care
Extract actual installed apps from live store HTML
"""

import requests
import re
import json
from datetime import datetime

print("=" * 80)
print("INSTALLED APPS - FACTUAL VERIFICATION - ALPHA MEDICAL CARE")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("=" * 80)

# Fetch homepage
url = "https://www.alphamedical.shop/"
response = requests.get(url, timeout=10)
html = response.text

print(f"\n1. GOOGLE TAG MANAGER:")
gtm_matches = re.findall(r'GTM-[A-Z0-9]+', html)
if gtm_matches:
    print(f"   ✅ GTM Container: {set(gtm_matches)}")
else:
    print(f"   ❌ NOT FOUND")

print(f"\n2. GOOGLE ANALYTICS 4:")
ga4_matches = re.findall(r'G-[A-Z0-9]+|GT-[A-Z0-9]+', html)
if ga4_matches:
    print(f"   ✅ GA4 Measurement IDs: {set(ga4_matches)}")

    # Check for Conversios
    if "Conversios" in html:
        print(f"   ✅ Installed via: Conversios app")
        conversios_date = re.search(r'Conversios.*?:.*?(\d{1,2}.*?20\d{2})', html)
        if conversios_date:
            print(f"   Date: {conversios_date.group(1)}")
else:
    print(f"   ❌ NOT FOUND")

print(f"\n3. GOOGLE MERCHANT CENTER:")
mc_matches = re.findall(r'MC-[A-Z0-9]+', html)
if mc_matches:
    print(f"   ✅ Merchant Center IDs: {set(mc_matches)}")
else:
    print(f"   ❌ NOT FOUND")

print(f"\n4. FACEBOOK PIXEL:")
fb_matches = re.findall(r'fbq\s*\(|facebook\.com/tr|connect\.facebook\.net', html)
if fb_matches:
    print(f"   ✅ FOUND ({len(fb_matches)} references)")
else:
    print(f"   ❌ NOT FOUND")

print(f"\n5. TIKTOK PIXEL:")
tt_matches = re.findall(r'ttq\s*\(|analytics\.tiktok\.com', html)
if tt_matches:
    print(f"   ✅ FOUND ({len(tt_matches)} references)")
else:
    print(f"   ❌ NOT FOUND")

print(f"\n6. WEB PIXELS MANAGER:")
web_pixels_match = re.search(r'webPixelsConfigList\s*:\s*\[(.*?)\]', html, re.DOTALL)
if web_pixels_match:
    try:
        # Extract pixel configs
        pixels_str = "[" + web_pixels_match.group(1) + "]"
        # Count configured pixels
        pixel_count = pixels_str.count('"id"')
        print(f"   ✅ Web Pixels Configured: {pixel_count}")

        # Extract app IDs
        app_ids = re.findall(r'"id":"(\d+)"', pixels_str)
        print(f"   App Pixel IDs:")
        for app_id in app_ids:
            print(f"      - {app_id}")

        # Extract account IDs
        account_ids = re.findall(r'"accountID":"([^"]+)"', pixels_str)
        if account_ids:
            print(f"   Account IDs:")
            for acc_id in account_ids:
                print(f"      - {acc_id}")

    except Exception as e:
        print(f"   ⚠️ Parse error: {e}")
else:
    print(f"   ❌ NOT FOUND")

print(f"\n7. SHOPIFY APP PIXEL:")
if 'shopify-app-pixel' in html:
    print(f"   ✅ PRESENT")
else:
    print(f"   ❌ NOT FOUND")

print(f"\n8. SHOPIFY CUSTOM PIXEL:")
if 'shopify-custom-pixel' in html:
    print(f"   ✅ PRESENT")
else:
    print(f"   ❌ NOT FOUND")

print("\n" + "=" * 80)
print("SUMMARY - INSTALLED TRACKING")
print("=" * 80)

installed = []
missing = []

if gtm_matches:
    installed.append("Google Tag Manager (GTM)")
else:
    missing.append("Google Tag Manager (GTM)")

if ga4_matches:
    installed.append("Google Analytics 4 (GA4)")
else:
    missing.append("Google Analytics 4 (GA4)")

if mc_matches:
    installed.append("Google Merchant Center")
else:
    missing.append("Google Merchant Center")

if fb_matches:
    installed.append("Facebook Pixel")
else:
    missing.append("Facebook Pixel")

if tt_matches:
    installed.append("TikTok Pixel")
else:
    missing.append("TikTok Pixel")

print(f"\n✅ INSTALLED ({len(installed)}):")
for item in installed:
    print(f"   - {item}")

print(f"\n❌ MISSING ({len(missing)}):")
for item in missing:
    print(f"   - {item}")

print("\n" + "=" * 80)
