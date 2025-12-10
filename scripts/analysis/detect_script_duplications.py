#!/usr/bin/env python3
"""
DÉTECTION DE DOUBLURES ET REDONDANCES - SCRIPTS FLYWHEEL
Identifie scripts qui font la même chose (doublures de tâches)
Approche: Bottom-up factuelle basée sur analyse de code
"""

import os
import json
from pathlib import Path
from collections import defaultdict
import re

def analyze_script_purpose(script_path):
    """Analyse le but d'un script basé sur son nom et contenu"""

    if not os.path.exists(script_path):
        return None

    # Extract key info from filename
    filename = Path(script_path).stem

    # Read first 50 lines to understand purpose
    try:
        with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [f.readline() for _ in range(50)]
            content = ''.join(lines).lower()
    except:
        content = ""

    # Detect purpose patterns
    purpose = {
        'action': None,      # verify, check, audit, fix, create, deploy, etc.
        'target': None,      # products, collections, bundles, klaviyo, etc.
        'api_calls': [],     # Shopify, Klaviyo, Google, etc.
        'keywords': []       # Key functionality keywords
    }

    # Detect action
    actions = ['verify', 'check', 'audit', 'fix', 'create', 'deploy', 'update', 'sync', 'analyze', 'generate', 'test']
    for action in actions:
        if action in filename.lower():
            purpose['action'] = action
            break

    # Detect target
    targets = [
        'product', 'collection', 'bundle', 'klaviyo', 'email', 'flow', 'workflow',
        'loyalty', 'seo', 'pixel', 'tracking', 'gtm', 'customer', 'lead', 'form'
    ]
    for target in targets:
        if target in filename.lower():
            purpose['target'] = target
            break

    # Detect API calls
    api_patterns = {
        'shopify': r'shopify.*api|admin/api|graphql',
        'klaviyo': r'klaviyo.*api|klaviyo\.com',
        'google_sheets': r'gspread|google.*sheets',
        'google_ads': r'google.*ads|adwords',
        'facebook': r'facebook.*api|graph\.facebook',
        'apify': r'apify.*api|apify\.com',
        'n8n': r'n8n.*api|webhook.*n8n'
    }

    for api, pattern in api_patterns.items():
        if re.search(pattern, content):
            purpose['api_calls'].append(api)

    # Extract key keywords from docstring/comments
    docstring_match = re.search(r'"""(.+?)"""', content, re.DOTALL)
    if docstring_match:
        docstring = docstring_match.group(1).lower()
        purpose['keywords'] = [
            word for word in docstring.split()
            if len(word) > 5 and word.isalpha()
        ][:10]

    return purpose

def find_duplications():
    """Trouve les scripts qui font la même chose"""

    print("="*80)
    print("DÉTECTION DE DOUBLURES - SCRIPTS FLYWHEEL")
    print("="*80)
    print("Méthode: Analyse nom + contenu + APIs appelées")
    print()

    # Get all scripts
    scripts = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in [".git", "node_modules", ".venv", "__pycache__", "archive"]]
        for file in files:
            if file.endswith(".py"):
                scripts.append(os.path.join(root, file))

    print(f"📊 Analysing {len(scripts)} scripts...\n")

    # Analyze all scripts
    script_purposes = {}
    for script in scripts:
        purpose = analyze_script_purpose(script)
        if purpose:
            script_purposes[script] = purpose

    # Group by action + target
    groups = defaultdict(list)
    for script, purpose in script_purposes.items():
        if purpose['action'] and purpose['target']:
            key = f"{purpose['action']}_{purpose['target']}"
            groups[key].append({
                'script': script,
                'apis': purpose['api_calls'],
                'keywords': purpose['keywords']
            })

    # Find potential duplications
    duplications = []
    for key, scripts_in_group in groups.items():
        if len(scripts_in_group) > 1:
            duplications.append({
                'type': key,
                'count': len(scripts_in_group),
                'scripts': scripts_in_group
            })

    # Sort by count
    duplications.sort(key=lambda x: x['count'], reverse=True)

    print("="*80)
    print(f"DOUBLURES DÉTECTÉES: {len(duplications)} groupes")
    print("="*80)

    total_redundant = 0

    for i, dup in enumerate(duplications[:20], 1):  # Show top 20
        action, target = dup['type'].split('_', 1)
        print(f"\n{i}. {action.upper()} {target.upper()} - {dup['count']} scripts")

        for j, script_info in enumerate(dup['scripts'], 1):
            script = script_info['script']
            # Check if obsolete
            is_obsolete = any(marker in script.lower() for marker in ['_old', '_backup', '_v1', '_v2', '_deprecated', '_test'])
            obsolete_marker = " ⚠️ OBSOLÈTE" if is_obsolete else ""

            print(f"   {j}. {script}{obsolete_marker}")
            if script_info['apis']:
                print(f"      APIs: {', '.join(script_info['apis'])}")

        # Count potential redundants (all but 1)
        total_redundant += (dup['count'] - 1)

    if len(duplications) > 20:
        print(f"\n... et {len(duplications) - 20} autres groupes de doublures")

    print("\n" + "="*80)
    print("SCRIPTS OBSOLÈTES DÉTECTÉS")
    print("="*80)

    obsolete_patterns = ['_old', '_backup', '_v1', '_v2', '_deprecated', '_test', 'old_', 'backup_']
    obsolete_scripts = []

    for script in scripts:
        if any(pattern in script.lower() for pattern in obsolete_patterns):
            obsolete_scripts.append(script)

    print(f"\n📦 Scripts avec marqueurs d'obsolescence: {len(obsolete_scripts)}")
    for script in sorted(obsolete_scripts)[:30]:  # Show first 30
        print(f"   • {script}")

    if len(obsolete_scripts) > 30:
        print(f"   ... et {len(obsolete_scripts) - 30} autres")

    print("\n" + "="*80)
    print("RÉSUMÉ FACTUEL")
    print("="*80)

    print(f"\n📊 TOTAL SCRIPTS ANALYSÉS: {len(scripts)}")
    print(f"🔄 GROUPES DE DOUBLURES: {len(duplications)}")
    print(f"⚠️  SCRIPTS POTENTIELLEMENT REDONDANTS: {total_redundant}")
    print(f"🗑️  SCRIPTS OBSOLÈTES: {len(obsolete_scripts)}")

    print(f"\n💡 OPTIMISATION POSSIBLE:")
    print(f"   Éliminer {total_redundant} scripts redondants")
    print(f"   Archiver {len(obsolete_scripts)} scripts obsolètes")
    print(f"   Réduction totale: {total_redundant + len(obsolete_scripts)} scripts ({(total_redundant + len(obsolete_scripts))/len(scripts)*100:.1f}%)")

    # Save detailed results
    results = {
        'total_scripts': len(scripts),
        'duplications': duplications,
        'obsolete_scripts': obsolete_scripts,
        'total_redundant': total_redundant
    }

    with open('script_duplications_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Résultats détaillés: script_duplications_analysis.json")

    return results

if __name__ == "__main__":
    find_duplications()
