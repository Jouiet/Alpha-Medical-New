#!/usr/bin/env python3
"""
Diagnose why workflow creates infinite loop
"""

import requests

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

INPUT_FOLDER = '1O1PrZoTDweXQx8ImVLXlJArei9hdvizn'
OUTPUT_FOLDER = '1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("DIAGNOSTIC: POURQUOI LE WORKFLOW CRÉE UNE BOUCLE INFINIE")
print("=" * 80)
print()

response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
workflow = response.json()

print("🔍 VÉRIFICATION 1: Workflow Configuration Node")
print("-" * 80)

for node in workflow['nodes']:
    if node['name'] == 'Workflow Configuration':
        params = node.get('parameters', {})
        assignments = params.get('assignments', {}).get('assignments', [])

        for assignment in assignments:
            if assignment.get('name') == 'dest_folder_id':
                dest_folder = assignment.get('value')
                print(f"dest_folder_id = {dest_folder}")

                if dest_folder == INPUT_FOLDER:
                    print("❌ PROBLÈME: dest_folder_id pointe vers INPUT!")
                    print("   Les fichiers output sont sauvegardés dans INPUT")
                    print("   → Le trigger les détecte → boucle infinie")
                elif dest_folder == OUTPUT_FOLDER:
                    print("✅ dest_folder_id pointe vers OUTPUT (correct)")
                else:
                    print(f"⚠️ dest_folder_id inattendu: {dest_folder}")

print()
print("🔍 VÉRIFICATION 2: Trigger Nodes (File Created & File Updated)")
print("-" * 80)

for node in workflow['nodes']:
    if node['type'] == 'n8n-nodes-base.googleDriveTrigger':
        print(f"\nNode: {node['name']}")
        params = node.get('parameters', {})

        if 'folderToWatch' in params:
            folder_config = params['folderToWatch']
            if isinstance(folder_config, dict):
                folder_id = folder_config.get('value')
            else:
                folder_id = folder_config

            print(f"  Folder surveillé: {folder_id}")

            if folder_id == INPUT_FOLDER:
                print("  ✅ Surveille INPUT (correct)")
            elif folder_id == OUTPUT_FOLDER:
                print("  ❌ PROBLÈME: Surveille OUTPUT!")
                print("     → Détecte ses propres outputs → boucle infinie")
            else:
                print(f"  ⚠️ Folder inattendu: {folder_id}")

print()
print("🔍 VÉRIFICATION 3: Save image Node")
print("-" * 80)

for node in workflow['nodes']:
    if node['name'] == 'Save image':
        print(f"\nNode: {node['name']}")
        params = node.get('parameters', {})

        if 'folderId' in params:
            folder_config = params['folderId']

            # This is an expression, need to evaluate what it uses
            if isinstance(folder_config, dict):
                value = folder_config.get('value')
                print(f"  folderId value: {value}")

                if "Workflow Configuration" in str(value):
                    print("  ✅ Utilise dest_folder_id depuis Workflow Configuration")
                    print("     → Valeur effective dépend du node 'Workflow Configuration'")

print()
print("=" * 80)
print("DIAGNOSTIC COMPLET")
print("=" * 80)
print()

print("📋 ANALYSE:")
print("   Le workflow crée une boucle car:")
print()
print("   1. Image originale uploadée dans INPUT")
print("   2. Workflow la traite → sauvegarde output dans ???")
print("   3. Si output est sauvegardé dans INPUT:")
print("      → Trigger détecte nouveau fichier")
print("      → Retraite l'image output")
print("      → Boucle infinie!")
print()
print("   OU")
print()
print("   1. Output sauvegardé dans OUTPUT (correct)")
print("   2. MAIS quelque chose copie/déplace le fichier vers INPUT")
print("   3. → Boucle infinie!")
print()
print("💡 SOLUTIONS:")
print("   A. S'assurer que dest_folder_id = OUTPUT (pas INPUT)")
print("   B. Supprimer fichiers INPUT après traitement réussi")
print("   C. Ajouter filtre: ignorer fichiers avec '_clean' dans le nom")
print()
print("=" * 80)
