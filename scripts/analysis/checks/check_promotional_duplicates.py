#!/usr/bin/env python3
"""
Vérification des produits dans MULTIPLE collections promotionnelles
RÈGLE: 1 principale + MAX 1 promotionnelle (pas 2+ promotionnelles)
"""

import json

# Charger les résultats de la vérification précédente
with open('collection_duplicates_verification.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collections principales vs promotionnelles
MAIN_COLLECTIONS = {
    'pain-relief-recovery',
    'therapy-wellness',
    'posture-support'
}

PROMOTIONAL_COLLECTIONS = {
    'new-arrivals',
    'bestsellers',
    'special-offers'
}

print("=" * 80)
print("VÉRIFICATION DES VIOLATIONS RÈGLE COLLECTIONS PROMOTIONNELLES")
print("=" * 80)
print("\nRÈGLE ACCEPTABLE:")
print("  ✅ 1 collection principale + 0-1 collection promotionnelle")
print("\nRÈGLE INTERDITE:")
print("  ❌ 1 collection principale + 2+ collections promotionnelles")
print("  ❌ 2+ collections principales")
print("=" * 80)

duplicates = data['duplicates']

violations = []
acceptable = []

for dup in duplicates:
    prod_id = dup['product_id']
    prod_title = dup['product_title']
    collections = dup['collections']

    # Compter collections par type
    main_colls = []
    promo_colls = []

    for coll in collections:
        handle = coll['collection_handle']
        if handle in MAIN_COLLECTIONS:
            main_colls.append(coll)
        elif handle in PROMOTIONAL_COLLECTIONS:
            promo_colls.append(coll)

    # Vérifier violations
    violation = False
    violation_type = None

    if len(main_colls) > 1:
        violation = True
        violation_type = "MULTIPLE_MAIN"
    elif len(promo_colls) > 1:
        violation = True
        violation_type = "MULTIPLE_PROMO"

    if violation:
        violations.append({
            'product_id': prod_id,
            'product_title': prod_title,
            'violation_type': violation_type,
            'main_collections': main_colls,
            'promo_collections': promo_colls,
            'main_count': len(main_colls),
            'promo_count': len(promo_colls)
        })
    else:
        acceptable.append({
            'product_id': prod_id,
            'product_title': prod_title,
            'main_collections': main_colls,
            'promo_collections': promo_colls
        })

print(f"\n📊 RÉSULTATS ANALYSE:\n")
print(f"Total produits analysés: {len(duplicates)}")
print(f"✅ Conformes (1 principale + 0-1 promotionnelle): {len(acceptable)}")
print(f"❌ VIOLATIONS: {len(violations)}")

if violations:
    print("\n" + "=" * 80)
    print("❌ VIOLATIONS DÉTECTÉES")
    print("=" * 80)

    multi_main = [v for v in violations if v['violation_type'] == 'MULTIPLE_MAIN']
    multi_promo = [v for v in violations if v['violation_type'] == 'MULTIPLE_PROMO']

    if multi_main:
        print(f"\n🔴 VIOLATION 1: Produits dans 2+ collections PRINCIPALES ({len(multi_main)})")
        for v in multi_main:
            print(f"\n   Produit: {v['product_title']}")
            print(f"   Collections principales ({v['main_count']}):")
            for mc in v['main_collections']:
                print(f"      - {mc['collection_title']}")
            if v['promo_collections']:
                print(f"   Collections promotionnelles ({v['promo_count']}):")
                for pc in v['promo_collections']:
                    print(f"      - {pc['collection_title']}")

    if multi_promo:
        print(f"\n🔴 VIOLATION 2: Produits dans 2+ collections PROMOTIONNELLES ({len(multi_promo)})")
        for v in multi_promo:
            print(f"\n   Produit: {v['product_title']}")
            print(f"   Collection principale:")
            for mc in v['main_collections']:
                print(f"      - {mc['collection_title']}")
            print(f"   Collections promotionnelles ({v['promo_count']}):")
            for pc in v['promo_collections']:
                print(f"      - {pc['collection_title']}")
else:
    print("\n" + "=" * 80)
    print("✅ AUCUNE VIOLATION - TOUTES LES RÈGLES RESPECTÉES!")
    print("=" * 80)
    print("\nTous les produits suivent la règle:")
    print("  1 collection principale + 0-1 collection promotionnelle")

# Sauvegarder les résultats
output = {
    'timestamp': '2025-10-15T03:35:00',
    'summary': {
        'total_products_analyzed': len(duplicates),
        'acceptable': len(acceptable),
        'violations': len(violations),
        'violation_types': {
            'multiple_main_collections': len([v for v in violations if v['violation_type'] == 'MULTIPLE_MAIN']),
            'multiple_promo_collections': len([v for v in violations if v['violation_type'] == 'MULTIPLE_PROMO'])
        }
    },
    'violations': violations,
    'acceptable': acceptable
}

with open('promotional_collections_violations.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Résultats sauvegardés: promotional_collections_violations.json")
print("=" * 80)
