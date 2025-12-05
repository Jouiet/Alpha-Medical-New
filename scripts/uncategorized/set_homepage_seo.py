#!/usr/bin/env python3
"""
SET HOMEPAGE SEO - Alpha Medical
Set homepage title and description via Shopify Admin API
"""

import requests
import json
from datetime import datetime

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials")
    exit(1)

API_VERSION = "2025-10"

print("="*80)
print("SET HOMEPAGE SEO - ALPHA MEDICAL")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/shop.json"
headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# Optimal SEO values
homepage_title = "Professional Medical Equipment You Can Trust - FDA-Compliant | 30-Day Guarantee | Alpha Medical Care"
homepage_description = "Professional medical support equipment & orthopedic braces. Shop knee braces, ankle supports, posture correctors, LED therapy devices & massage tools. Free shipping over $50."

print(f"\n📝 Setting Homepage SEO:")
print(f"   Title ({len(homepage_title)} chars): {homepage_title[:80]}...")
print(f"   Description ({len(homepage_description)} chars): {homepage_description[:80]}...")

payload = {
    "shop": {
        "meta_title": homepage_title,
        "meta_description": homepage_description
    }
}

try:
    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 200:
        shop = response.json().get("shop", {})
        print(f"\n✅ SUCCESS")
        print(f"   Homepage Title: {shop.get('meta_title', 'NOT SET')[:80]}...")
        print(f"   Homepage Description: {shop.get('meta_description', 'NOT SET')[:80]}...")
    else:
        print(f"\n❌ FAILED - Status {response.status_code}")
        print(f"   Response: {response.text[:200]}")

except Exception as e:
    print(f"\n❌ Exception: {e}")

print("\n🎯 NEXT STEPS:")
print("1. Wait 30 seconds for Shopify to apply changes")
print("2. Clear browser cache and reload homepage")
print("3. Re-run comprehensive_seo_validation.py")

print("\n" + "="*80)
