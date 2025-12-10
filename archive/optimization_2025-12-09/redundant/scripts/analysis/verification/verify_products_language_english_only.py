#!/usr/bin/env python3
"""
FORENSIC AUDIT: 100% English Language Verification
Verify EVERY product has NO French content (titles, descriptions, tags)
NO TRUST - Check every single product individually
"""

import requests
import re
from datetime import datetime

print("═══════════════════════════════════════════════════════════════")
print("🔬 FORENSIC AUDIT: 100% ENGLISH LANGUAGE VERIFICATION")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("═══════════════════════════════════════════════════════════════\n")

# French keywords to detect
FRENCH_KEYWORDS = [
    'genouillère', 'orthèse', 'correcteur', 'dispositif', 'appareil', 
    'thérapie', 'traitement', 'soulagement', 'douleur', 'réglable', 
    'ajustable', 'confortable', 'efficace', 'professionnel', 'médical', 
    'orthopédique', 'compression', 'protection', 'récupération',
    'cervicale', 'lombaire', 'épaule', 'genou', 'pied', 'cheville',
    'nouveau', 'nouvelle', 'meilleur', 'meilleure', 'électrique',
    'de la', 'de le', 'à la', 'au ', 'aux ', 'avec ', 'pour ', 'dans ',
]

# Fetch products from live site
response = requests.get('https://www.alphamedical.shop/products.json', timeout=10)
if response.status_code != 200:
    print(f"❌ Failed to fetch products: HTTP {response.status_code}")
    exit(1)

import json
data = json.loads(response.text)
products = data.get('products', [])

print(f"✅ Fetched {len(products)} products from live site\n")

print("═══════════════════════════════════════════════════════════════")
print("🔍 PRODUCT-BY-PRODUCT LANGUAGE AUDIT")
print("═══════════════════════════════════════════════════════════════\n")

french_violations = []
english_ok = []

for i, product in enumerate(products, 1):
    product_title = product.get('title', '')
    product_handle = product.get('handle', '')
    body_html = product.get('body_html', '')
    tags = ' '.join(product.get('tags', []))

    # Combine all text fields
    full_text = f"{product_title} {body_html} {tags}".lower()

    # Check for French keywords
    found_french = []
    for keyword in FRENCH_KEYWORDS:
        if keyword in full_text:
            found_french.append(keyword.strip())

    print(f"[{i}/{len(products)}] {product_title[:60]}")

    if found_french:
        print(f"   ❌ FRENCH DETECTED: {set(found_french)}")
        french_violations.append({
            'title': product_title,
            'handle': product_handle,
            'french_words': list(set(found_french))
        })
    else:
        print(f"   ✅ ENGLISH ONLY")
        english_ok.append(product_title)

print()

# FINAL REPORT
print("═══════════════════════════════════════════════════════════════")
print("📊 LANGUAGE AUDIT REPORT")
print("═══════════════════════════════════════════════════════════════\n")

print(f"✅ Products in English: {len(english_ok)}/{len(products)} ({len(english_ok)/len(products)*100:.1f}%)")
print(f"❌ Products with French: {len(french_violations)}/{len(products)} ({len(french_violations)/len(products)*100:.1f}%)")
print()

if french_violations:
    print("❌ FRENCH VIOLATIONS (First 10):")
    for violation in french_violations[:10]:
        print(f"   - {violation['title'][:50]}: {violation['french_words'][:3]}")
    if len(french_violations) > 10:
        print(f"   ... and {len(french_violations) - 10} more")
    print()

# VERDICT
if len(french_violations) == 0:
    print("🎉 VERDICT: 100% ENGLISH COMPLIANCE\n")
    exit(0)
else:
    print(f"❌ VERDICT: {len(french_violations)} products contain French\n")
    exit(1)
