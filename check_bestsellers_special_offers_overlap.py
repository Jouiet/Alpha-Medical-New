#!/usr/bin/env python3
"""
Vérification de l'overlap entre Bestsellers et Special Offers
"""

import json

# Charger les données de vérification
with open('collection_duplicates_verification.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extraire les produits de chaque collection
bestsellers_products = set()
special_offers_products = set()
new_arrivals_products = set()

for coll_id, coll_data in data['collections'].items():
    handle = coll_data['handle']

    # Trouver les produits de cette collection dans les duplicates
    for dup in data['duplicates']:
        for coll in dup['collections']:
            if coll['collection_handle'] == handle:
                if handle == 'bestsellers':
                    bestsellers_products.add((dup['product_id'], dup['product_title']))
                elif handle == 'special-offers':
                    special_offers_products.add((dup['product_id'], dup['product_title']))
                elif handle == 'new-arrivals':
                    new_arrivals_products.add((dup['product_id'], dup['product_title']))

print("=" * 80)
print("VÉRIFICATION OVERLAP ENTRE COLLECTIONS PROMOTIONNELLES")
print("=" * 80)

print(f"\n📊 COMPTAGE:")
print(f"   Bestsellers: {len(bestsellers_products)} produits")
print(f"   Special Offers: {len(special_offers_products)} produits")
print(f"   New Arrivals: {len(new_arrivals_products)} produits")

# Vérifier overlap Bestsellers <-> Special Offers
overlap_best_special = bestsellers_products.intersection(special_offers_products)

# Vérifier overlap Bestsellers <-> New Arrivals
overlap_best_new = bestsellers_products.intersection(new_arrivals_products)

# Vérifier overlap Special Offers <-> New Arrivals
overlap_special_new = special_offers_products.intersection(new_arrivals_products)

print("\n" + "=" * 80)
print("ANALYSE DES OVERLAPS")
print("=" * 80)

print(f"\n🔍 Bestsellers ∩ Special Offers: {len(overlap_best_special)} produits")
if overlap_best_special:
    print("   ❌ VIOLATION DÉTECTÉE!")
    for prod_id, prod_title in sorted(overlap_best_special, key=lambda x: x[1]):
        print(f"      - {prod_title}")
else:
    print("   ✅ Aucun overlap")

print(f"\n🔍 Bestsellers ∩ New Arrivals: {len(overlap_best_new)} produits")
if overlap_best_new:
    print("   ❌ VIOLATION DÉTECTÉE!")
    for prod_id, prod_title in sorted(overlap_best_new, key=lambda x: x[1]):
        print(f"      - {prod_title}")
else:
    print("   ✅ Aucun overlap")

print(f"\n🔍 Special Offers ∩ New Arrivals: {len(overlap_special_new)} produits")
if overlap_special_new:
    print("   ❌ VIOLATION DÉTECTÉE!")
    for prod_id, prod_title in sorted(overlap_special_new, key=lambda x: x[1]):
        print(f"      - {prod_title}")
else:
    print("   ✅ Aucun overlap")

# Résumé
total_violations = len(overlap_best_special) + len(overlap_best_new) + len(overlap_special_new)

print("\n" + "=" * 80)
if total_violations > 0:
    print(f"❌ TOTAL VIOLATIONS: {total_violations} overlaps détectés")
else:
    print("✅ AUCUNE VIOLATION - Collections promotionnelles 100% séparées")
print("=" * 80)

# Sauvegarder
output = {
    'timestamp': '2025-10-15T03:40:00',
    'summary': {
        'bestsellers_count': len(bestsellers_products),
        'special_offers_count': len(special_offers_products),
        'new_arrivals_count': len(new_arrivals_products),
        'overlap_bestsellers_special': len(overlap_best_special),
        'overlap_bestsellers_new': len(overlap_best_new),
        'overlap_special_new': len(overlap_special_new),
        'total_violations': total_violations
    },
    'overlaps': {
        'bestsellers_special_offers': [{'product_id': pid, 'product_title': title} for pid, title in overlap_best_special],
        'bestsellers_new_arrivals': [{'product_id': pid, 'product_title': title} for pid, title in overlap_best_new],
        'special_offers_new_arrivals': [{'product_id': pid, 'product_title': title} for pid, title in overlap_special_new]
    }
}

with open('promotional_overlap_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Résultats sauvegardés: promotional_overlap_analysis.json")
