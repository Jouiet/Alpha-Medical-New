#!/usr/bin/env python3
"""
FORENSIC AUDIT: ACTUAL French Content Detection
Only detect REAL French sentences/phrases, not English words
"""

import requests
import json
from datetime import datetime

print("═══════════════════════════════════════════════════════════════")
print("🔬 FORENSIC AUDIT: ACTUAL FRENCH CONTENT DETECTION")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("═══════════════════════════════════════════════════════════════\n")

# Unambiguous French phrases (not English cognates)
ACTUAL_FRENCH_PHRASES = [
    # French-only phrases
    'correcteur de', 'soulagement de', 'pour la', 'pour le',
    'traitement de', 'dispositif de', 'appareil de',
    'avec le', 'avec la', 'dans le', 'dans la',
    'sur le', 'sur la', 'à la', 'au niveau',
    # French verbs
    'vous pouvez', 'il est', 'elle est', 'nous avons',
    'je suis', 'tu es', 'vous êtes',
    # French-only adjectives
    'très efficace', 'très confortable', 'plus efficace',
    'meilleur choix', 'nouvelle génération',
    # French product descriptions
    'idéal pour', 'parfait pour', 'convient pour',
    'recommandé pour', 'utilisé pour',
    'genouillère', 'cervicale', 'lombaire', 'orthèse',
    'thérapie par', 'traitement par',
]

# Fetch products
response = requests.get('https://www.alphamedical.shop/products.json', timeout=10)
if response.status_code != 200:
    print(f"❌ Failed to fetch products")
    exit(1)

data = json.loads(response.text)
products = data.get('products', [])

print(f"✅ Fetched {len(products)} products\n")

print("🔍 SCANNING FOR ACTUAL FRENCH PHRASES")
print("─" * 60)

french_found = []
english_only = []

for i, product in enumerate(products, 1):
    title = product.get('title', '')
    body = product.get('body_html', '')
    tags = ' '.join(product.get('tags', []))
    
    full_text = f"{title} {body} {tags}".lower()
    
    # Check for unambiguous French phrases
    detected_phrases = []
    for phrase in ACTUAL_FRENCH_PHRASES:
        if phrase in full_text:
            detected_phrases.append(phrase)
    
    print(f"[{i}/{len(products)}] {title[:50]}")
    
    if detected_phrases:
        print(f"   ❌ FRENCH: {detected_phrases[:3]}")
        french_found.append({
            'title': title,
            'handle': product.get('handle'),
            'phrases': detected_phrases
        })
    else:
        print(f"   ✅ ENGLISH")
        english_only.append(title)

print()

# Check if product titles/descriptions are in French
print("🔍 CHECKING TITLES FOR FRENCH WORDS")
print("─" * 60)

french_titles = []
for product in products:
    title = product.get('title', '').lower()
    
    # Check for actual French words (not in English)
    french_indicators = [
        'genouillère', 'correcteur', 'orthèse', 'cervicale',
        'lombaire', 'épaule', 'cheville', 'réglable'
    ]
    
    for word in french_indicators:
        if word in title:
            french_titles.append((product.get('title'), word))
            break

if french_titles:
    print("❌ French words in titles:")
    for title, word in french_titles[:5]:
        print(f"   - {title[:50]}: '{word}'")
    print()
else:
    print("✅ All titles in English\n")

# FINAL REPORT
print("═══════════════════════════════════════════════════════════════")
print("📊 LANGUAGE COMPLIANCE REPORT")
print("═══════════════════════════════════════════════════════════════\n")

print(f"✅ English-only products: {len(english_only)}/{len(products)} ({len(english_only)/len(products)*100:.1f}%)")
print(f"❌ Products with French: {len(french_found)}/{len(products)} ({len(french_found)/len(products)*100:.1f}%)")
print(f"⚠️  French in titles: {len(french_titles)}")
print()

if len(french_found) == 0 and len(french_titles) == 0:
    print("🎉 VERDICT: 100% ENGLISH COMPLIANCE")
    print("   All products are in English\n")
    exit(0)
else:
    print(f"❌ VERDICT: {len(french_found) + len(french_titles)} items need translation\n")
    
    if french_found:
        print("French content detected in:")
        for item in french_found[:5]:
            print(f"   - {item['title'][:50]}")
    
    exit(1)
