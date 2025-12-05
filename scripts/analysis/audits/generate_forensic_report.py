#!/usr/bin/env python3
"""
GÉNÉRATEUR DE RAPPORT FORENSIQUE ULTRA-DÉTAILLÉ
Crée un document Markdown exhaustif avec toutes les données de l'analyse
"""

import json
from datetime import datetime
from typing import Dict, List

def load_data() -> Dict:
    """Charge les données forensiques"""
    with open('forensic_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_executive_summary(data: Dict) -> str:
    """Génère le résumé exécutif"""
    md = "# 🚨 RAPPORT FORENSIQUE - ANALYSE PRODUITS SHOPIFY\n\n"
    md += f"**Store:** Alpha Medical (azffej-as.myshopify.com)  \n"
    md += f"**Date d'analyse:** {data['metadata']['analysis_date']}  \n"
    md += f"**Total produits:** {data['metadata']['total_products']}  \n"
    md += f"**Total collections:** {data['metadata']['total_collections']}  \n\n"

    md += "---\n\n"
    md += "## ⚠️ RÉSUMÉ EXÉCUTIF - VIOLATIONS CRITIQUES\n\n"

    # Statistiques des violations
    multi_col_count = data['multi_collection_analysis']['count']
    duplicate_count = len(data['duplicates']['similar_title_duplicates'])
    sku_duplicate_count = data['duplicates']['sku_duplicates_count']

    md += "### 🔴 VIOLATIONS MAJEURES IDENTIFIÉES\n\n"
    md += f"| Violation | Nombre | Gravité |\n"
    md += f"|-----------|--------|--------|\n"
    md += f"| **Produits dans plusieurs collections** | **{multi_col_count}** | 🔴 CRITIQUE |\n"
    md += f"| **Doublons de produits** | **{duplicate_count}** | 🔴 CRITIQUE |\n"
    md += f"| **Doublons SKU** | **{sku_duplicate_count}** | 🟡 MOYEN |\n\n"

    md += "### 📊 IMPACT\n\n"
    md += f"- **{multi_col_count}/{data['metadata']['total_products']}** produits ({multi_col_count*100//data['metadata']['total_products']}%) violent la règle d'unicité de collection\n"
    md += f"- **{duplicate_count}** groupes de doublons nécessitent une suppression\n"
    md += f"- **{sku_duplicate_count}** SKU dupliqués peuvent causer des problèmes d'inventaire\n\n"

    md += "### ✅ CONFORMITÉ\n\n"
    conforming = data['metadata']['total_products'] - multi_col_count
    md += f"- **{conforming}** produits respectent la règle d'unicité de collection\n"
    md += f"- **{data['metadata']['total_collections']}** collections identifiées\n\n"

    return md

def generate_violations_detail(data: Dict) -> str:
    """Génère la section détaillée des violations"""
    md = "---\n\n"
    md += "## 🔍 SECTION 1: VIOLATIONS MULTI-COLLECTIONS\n\n"
    md += "### ⚠️ RÈGLE VIOLÉE\n\n"
    md += "> **EXIGENCE STRICTE NON NÉGOCIABLE:** Un produit ne peut apparaître que dans UNE seule collection.  \n"
    md += "> **Réalité actuelle:** 33 produits apparaissent dans 2 ou 3 collections.\n\n"

    md += f"### 📋 LISTE COMPLÈTE DES {data['multi_collection_analysis']['count']} PRODUITS EN VIOLATION\n\n"

    # Trier par nombre de collections (descendant)
    products = sorted(
        data['multi_collection_analysis']['products'],
        key=lambda x: x['collection_count'],
        reverse=True
    )

    for i, product in enumerate(products, 1):
        md += f"#### {i}. {product['title']}\n\n"
        md += f"- **ID:** `{product['id']}`\n"
        md += f"- **Handle:** `{product['handle']}`\n"
        md += f"- **Nombre de collections:** {product['collection_count']}\n"
        md += f"- **Collections actuelles:**\n"
        for col in product['collections']:
            md += f"  - {col}\n"

        # Recommandation
        md += f"- **⚠️ ACTION REQUISE:** Retirer ce produit de {product['collection_count'] - 1} collection(s)\n"

        # Analyser quelle collection garder
        if "New Arrivals" in product['collections']:
            md += f"- **💡 RECOMMANDATION:** Garder dans `{[c for c in product['collections'] if c != 'New Arrivals'][0] if len(product['collections']) > 1 else product['collections'][0]}`, retirer de `New Arrivals`\n"

        md += "\n"

    return md

def generate_duplicates_detail(data: Dict) -> str:
    """Génère la section des doublons"""
    md = "---\n\n"
    md += "## 🔍 SECTION 2: DOUBLONS DE PRODUITS\n\n"
    md += "### ⚠️ RÈGLE VIOLÉE\n\n"
    md += "> **EXIGENCE STRICTE NON NÉGOCIABLE:** Pas de produits en double sur tout le site.  \n"
    md += "> **Réalité actuelle:** 1 groupe de doublons identifié.\n\n"

    # Doublons exacts
    md += "### 📋 DOUBLONS EXACTS (MÊME TITRE)\n\n"

    for title, products in data['duplicates']['exact_title_duplicates'].items():
        md += f"#### Titre: \"{title}\"\n\n"
        md += f"**Nombre d'occurrences:** {len(products)}\n\n"
        md += "| # | ID Produit | Handle | Action |\n"
        md += "|---|-----------|---------|--------|\n"

        for i, product in enumerate(products, 1):
            action = "🟢 GARDER" if i == 1 else "🔴 SUPPRIMER"
            md += f"| {i} | `{product['id']}` | `{product['handle']}` | **{action}** |\n"

        md += "\n"

    # Recommandations de nettoyage
    if data['cleanup_recommendations']:
        md += "### 🧹 PLAN DE NETTOYAGE DÉTAILLÉ\n\n"

        for i, rec in enumerate(data['cleanup_recommendations'], 1):
            md += f"#### Groupe {i}: {rec['normalized_title']}\n\n"
            md += f"**Nombre de doublons:** {rec['duplicate_count']}\n\n"

            md += "##### 🟢 PRODUIT À GARDER (Prix le plus bas)\n\n"
            keep = rec['keep']
            md += f"- **Titre:** {keep['title']}\n"
            md += f"- **ID:** `{keep['id']}`\n"
            md += f"- **Handle:** `{keep['handle']}`\n"
            md += f"- **Prix:** ${keep['price']}\n\n"

            md += "##### 🔴 PRODUITS À SUPPRIMER\n\n"
            for j, delete in enumerate(rec['delete'], 1):
                md += f"**{j}. {delete['title']}**\n"
                md += f"- **ID:** `{delete['id']}`\n"
                md += f"- **Handle:** `{delete['handle']}`\n"
                md += f"- **Prix:** ${delete['price']} (${delete['price_difference']:.2f} plus cher)\n"
                md += f"- **Commande de suppression:**\n"
                md += f"  ```bash\n"
                md += f"  # Via Admin API\n"
                md += f"  DELETE /admin/api/2024-10/products/{delete['id'].split('/')[-1]}.json\n"
                md += f"  ```\n\n"

    return md

def generate_sku_analysis(data: Dict) -> str:
    """Génère l'analyse des SKU"""
    md = "---\n\n"
    md += "## 🔍 SECTION 3: ANALYSE DES SKU\n\n"
    md += f"### ⚠️ DOUBLONS SKU DÉTECTÉS: {data['duplicates']['sku_duplicates_count']}\n\n"
    md += "> Les SKU dupliqués peuvent causer des problèmes d'inventaire et de gestion des stocks.\n\n"
    md += "**Note:** Cette section nécessite une analyse approfondie des variantes.  \n"
    md += "**Action recommandée:** Réviser le système de génération des SKU pour éviter les doublons.\n\n"

    return md

def generate_price_matrix_section(data: Dict) -> str:
    """Génère la section de la matrice de prix"""
    md = "---\n\n"
    md += "## 🔍 SECTION 4: MATRICE COMPLÈTE PRIX & COLLECTIONS\n\n"
    md += f"### 📊 VUE D'ENSEMBLE - {len(data['price_matrix'])} PRODUITS\n\n"

    # Statistiques globales
    total_variants = sum(p['variant_count'] for p in data['price_matrix'])
    avg_price = sum(p['min_price'] for p in data['price_matrix']) / len(data['price_matrix'])

    md += f"- **Total variantes:** {total_variants}\n"
    md += f"- **Prix moyen (min):** ${avg_price:.2f}\n\n"

    md += "### 📋 MATRICE DÉTAILLÉE\n\n"
    md += "| # | Produit | Prix Min | Prix Max | Variantes | Collections | Multi-Col |\n"
    md += "|---|---------|----------|----------|-----------|-------------|------------|\n"

    for i, product in enumerate(data['price_matrix'], 1):
        multi_col_flag = "🔴" if product['collection_count'] > 1 else "🟢"
        collections_str = ", ".join(product['collections'][:2])
        if len(product['collections']) > 2:
            collections_str += f" +{len(product['collections']) - 2}"

        md += f"| {i} | {product['product_title'][:40]}{'...' if len(product['product_title']) > 40 else ''} | "
        md += f"${product['min_price']:.2f} | ${product['max_price']:.2f} | "
        md += f"{product['variant_count']} | {collections_str} | {multi_col_flag} |\n"

    md += "\n"

    return md

def generate_collections_breakdown(data: Dict) -> str:
    """Génère la répartition par collection"""
    md = "---\n\n"
    md += "## 🔍 SECTION 5: RÉPARTITION PAR COLLECTION\n\n"

    # Compter les produits par collection
    collection_counts = {}
    for product in data['price_matrix']:
        for col in product['collections']:
            if col not in collection_counts:
                collection_counts[col] = 0
            collection_counts[col] += 1

    # Trier par nombre de produits
    sorted_collections = sorted(collection_counts.items(), key=lambda x: x[1], reverse=True)

    md += "### 📊 NOMBRE DE PRODUITS PAR COLLECTION\n\n"
    md += "| Collection | Nombre de Produits | % du Total |\n"
    md += "|------------|-------------------|------------|\n"

    total_products = data['metadata']['total_products']
    for col_name, count in sorted_collections:
        percentage = (count / total_products) * 100
        md += f"| {col_name} | {count} | {percentage:.1f}% |\n"

    md += "\n"

    # Détail de chaque collection
    collections_from_api = data['collections']

    md += "### 📋 DÉTAIL PAR COLLECTION\n\n"
    for collection in collections_from_api:
        product_count = len(collection['products']['edges'])
        md += f"#### {collection['title']}\n\n"
        md += f"- **ID:** `{collection['id']}`\n"
        md += f"- **Handle:** `{collection['handle']}`\n"
        md += f"- **Nombre de produits:** {product_count}\n"

        if collection['description']:
            md += f"- **Description:** {collection['description'][:100]}{'...' if len(collection['description']) > 100 else ''}\n"

        md += "\n**Liste des produits:**\n\n"
        for i, prod_edge in enumerate(collection['products']['edges'][:10], 1):
            prod = prod_edge['node']
            md += f"{i}. {prod['title']}\n"

        if product_count > 10:
            md += f"... et {product_count - 10} autres produits\n"

        md += "\n"

    return md

def generate_action_plan(data: Dict) -> str:
    """Génère le plan d'action"""
    md = "---\n\n"
    md += "## 🎯 SECTION 6: PLAN D'ACTION EXHAUSTIF\n\n"
    md += "### ⚠️ PRIORITÉS CRITIQUES\n\n"

    multi_col_count = data['multi_collection_analysis']['count']
    duplicate_count = len(data['cleanup_recommendations'])

    md += "#### 🔴 PRIORITÉ 1: CORRIGER LES VIOLATIONS MULTI-COLLECTIONS\n\n"
    md += f"**Nombre de produits à corriger:** {multi_col_count}\n\n"
    md += "**Actions:**\n\n"
    md += "1. **Décider de la collection principale pour chaque produit**\n"
    md += "   - Analyser la pertinence de chaque produit pour chaque collection\n"
    md += "   - Retirer tous les produits de \"New Arrivals\" (sauf si c'est leur seule collection pertinente)\n"
    md += "   - Garder chaque produit dans UNE seule collection thématique\n\n"

    md += "2. **Méthode de correction:**\n"
    md += "   ```bash\n"
    md += "   # Via Admin API - Retirer un produit d'une collection\n"
    md += "   DELETE /admin/api/2024-10/collections/{collection_id}/products/{product_id}.json\n"
    md += "   ```\n\n"

    md += "3. **Script de correction automatique** (voir Section 7)\n\n"

    md += "#### 🔴 PRIORITÉ 2: SUPPRIMER LES DOUBLONS\n\n"
    md += f"**Nombre de produits à supprimer:** {sum(len(r['delete']) for r in data['cleanup_recommendations'])}\n\n"
    md += "**Actions:**\n\n"
    md += "1. **Vérifier manuellement chaque doublon avant suppression**\n"
    md += "2. **Sauvegarder les données avant suppression**\n"
    md += "3. **Supprimer les produits identifiés en Section 2**\n\n"

    md += "   ```bash\n"
    md += "   # Via Admin API\n"
    md += "   DELETE /admin/api/2024-10/products/{product_id}.json\n"
    md += "   ```\n\n"

    md += "#### 🟡 PRIORITÉ 3: RÉVISER LE SYSTÈME DE SKU\n\n"
    md += f"**Doublons SKU détectés:** {data['duplicates']['sku_duplicates_count']}\n\n"
    md += "**Actions:**\n\n"
    md += "1. **Analyser le pattern de génération des SKU**\n"
    md += "2. **Créer un système de SKU unique et cohérent**\n"
    md += "3. **Mettre à jour les SKU dupliqués**\n\n"

    md += "### 📅 TIMELINE RECOMMANDÉ\n\n"
    md += "| Phase | Action | Durée estimée | Statut |\n"
    md += "|-------|--------|--------------|--------|\n"
    md += "| 1 | Révision manuelle des violations multi-collections | 2-3 heures | ⏳ À faire |\n"
    md += "| 2 | Correction des multi-collections (retirer de collections) | 1 heure | ⏳ À faire |\n"
    md += "| 3 | Vérification des doublons | 30 min | ⏳ À faire |\n"
    md += "| 4 | Suppression des doublons | 15 min | ⏳ À faire |\n"
    md += "| 5 | Révision du système de SKU | 1-2 heures | ⏳ À faire |\n"
    md += "| 6 | Vérification finale et tests | 1 heure | ⏳ À faire |\n\n"

    return md

def generate_scripts_section(data: Dict) -> str:
    """Génère les scripts de correction"""
    md = "---\n\n"
    md += "## 🔧 SECTION 7: SCRIPTS DE CORRECTION AUTOMATIQUE\n\n"

    md += "### Script 1: Retirer produits de 'New Arrivals'\n\n"
    md += "```python\n"
    md += "# script_remove_from_new_arrivals.py\n"
    md += 'import requests\n\n'
    md += 'SHOPIFY_STORE_DOMAIN = "azffej-as.myshopify.com"\n'
    md += 'SHOPIFY_ADMIN_ACCESS_TOKEN = "YOUR_TOKEN_HERE"\n\n'
    md += '# Produits à retirer de New Arrivals\n'
    md += 'products_to_fix = [\n'

    # Générer la liste des produits à retirer de New Arrivals
    count = 0
    for product in data['multi_collection_analysis']['products'][:5]:
        if "New Arrivals" in product['collections'] and len(product['collections']) > 1:
            md += f'    {{"product_id": "{product["id"]}", "title": "{product["title"]}"}},\n'
            count += 1

    md += "    # ... (voir forensic_data.json pour la liste complète)\n"
    md += "]\n\n"
    md += "# TODO: Implémenter la logique de suppression\n"
    md += "```\n\n"

    md += "### Script 2: Supprimer les doublons\n\n"
    md += "```python\n"
    md += "# script_delete_duplicates.py\n"
    md += "# Liste des produits à supprimer (voir Section 2)\n"
    md += "products_to_delete = [\n"

    for rec in data['cleanup_recommendations']:
        for delete in rec['delete']:
            md += f'    "{delete["id"]}",  # {delete["title"]}\n'

    md += "]\n"
    md += "# TODO: Implémenter la logique de suppression avec confirmation\n"
    md += "```\n\n"

    return md

def generate_verification_checklist(data: Dict) -> str:
    """Génère la checklist de vérification"""
    md = "---\n\n"
    md += "## ✅ SECTION 8: CHECKLIST DE VÉRIFICATION POST-CORRECTION\n\n"
    md += "### Avant de commencer\n\n"
    md += "- [ ] Backup complet de la base de données Shopify\n"
    md += "- [ ] Liste des corrections à effectuer validée\n"
    md += "- [ ] Scripts de correction testés en environnement de développement\n\n"

    md += "### Pendant les corrections\n\n"
    md += "- [ ] Retirer les produits des collections supplémentaires (multi-collections)\n"
    md += "- [ ] Vérifier que chaque produit n'est plus que dans UNE collection\n"
    md += "- [ ] Supprimer les produits en double\n"
    md += "- [ ] Vérifier que les produits conservés sont bien les moins chers\n\n"

    md += "### Après les corrections\n\n"
    md += "- [ ] Relancer l'analyse forensique pour vérifier 0 violation\n"
    md += "- [ ] Tester la navigation sur le site\n"
    md += "- [ ] Vérifier que tous les liens produits fonctionnent\n"
    md += "- [ ] Vérifier l'inventaire et les SKU\n"
    md += "- [ ] Mettre à jour la documentation\n\n"

    md += "### Métriques de succès\n\n"
    md += "| Métrique | Avant | Cible Après | Statut |\n"
    md += "|----------|-------|-------------|--------|\n"
    md += f"| Produits multi-collections | {data['multi_collection_analysis']['count']} | 0 | ⏳ |\n"
    md += f"| Doublons de produits | {len(data['cleanup_recommendations'])} | 0 | ⏳ |\n"
    md += f"| Doublons SKU | {data['duplicates']['sku_duplicates_count']} | 0 | ⏳ |\n"
    md += f"| Total produits | {data['metadata']['total_products']} | {data['metadata']['total_products'] - sum(len(r['delete']) for r in data['cleanup_recommendations'])} | ⏳ |\n\n"

    return md

def generate_appendix(data: Dict) -> str:
    """Génère les annexes"""
    md = "---\n\n"
    md += "## 📎 ANNEXES\n\n"
    md += "### Annexe A: Métadonnées de l'analyse\n\n"
    md += f"- **Date:** {data['metadata']['analysis_date']}\n"
    md += f"- **Total produits analysés:** {data['metadata']['total_products']}\n"
    md += f"- **Total collections analysées:** {data['metadata']['total_collections']}\n"
    md += "- **Fichier de données brutes:** `forensic_data.json`\n"
    md += "- **Script d'analyse:** `forensic_analysis.py`\n\n"

    md += "### Annexe B: Références API Shopify\n\n"
    md += "- **GraphQL Admin API:** https://shopify.dev/docs/api/admin-graphql\n"
    md += "- **REST Admin API:** https://shopify.dev/docs/api/admin-rest\n"
    md += "- **Collection API:** https://shopify.dev/docs/api/admin-rest/2024-10/resources/collection\n"
    md += "- **Product API:** https://shopify.dev/docs/api/admin-rest/2024-10/resources/product\n\n"

    md += "### Annexe C: Contacts et Support\n\n"
    md += "Pour toute question concernant ce rapport:\n"
    md += "- Analyste: Claude (Anthropic)\n"
    md += "- Store: Alpha Medical\n"
    md += "- Domain: azffej-as.myshopify.com\n\n"

    md += "---\n\n"
    md += "**FIN DU RAPPORT FORENSIQUE**\n\n"
    md += f"*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    return md

def main():
    """Génère le rapport complet"""
    print("🔍 Chargement des données forensiques...")
    data = load_data()

    print("📝 Génération du rapport Markdown...")

    report = ""
    report += generate_executive_summary(data)
    report += generate_violations_detail(data)
    report += generate_duplicates_detail(data)
    report += generate_sku_analysis(data)
    report += generate_price_matrix_section(data)
    report += generate_collections_breakdown(data)
    report += generate_action_plan(data)
    report += generate_scripts_section(data)
    report += generate_verification_checklist(data)
    report += generate_appendix(data)

    # Sauvegarder
    filename = "FORENSIC_ANALYSIS_REPORT.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ Rapport généré: {filename}")
    print(f"   Taille: {len(report)} caractères")
    print(f"   Sections: 8 principales + annexes")

if __name__ == "__main__":
    main()
