#!/usr/bin/env python3
"""
REMOVE the filter I added and restore workflow to working state
"""

import requests

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("ROLLBACK: SUPPRIMER LE FILTRE ET RESTAURER WORKFLOW")
print("=" * 80)
print()

response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
workflow = response.json()

# Find and remove the filter node
filter_node_index = None
for i, node in enumerate(workflow['nodes']):
    if 'Filter Already Processed' in node['name']:
        filter_node_index = i
        break

if filter_node_index is None:
    print("✅ Pas de filtre à supprimer")
    exit(0)

print(f"🗑️ Suppression du node 'Filter Already Processed'...")
del workflow['nodes'][filter_node_index]
print("✅ Node supprimé")
print()

# Restore connections: Set File ID → Workflow Configuration (direct)
print("🔗 Restauration des connexions...")

# Get what the filter was connecting to (FALSE path)
old_filter_connections = workflow['connections'].get('Filter Already Processed', {}).get('main', [[],[]])
false_path_connections = old_filter_connections[1] if len(old_filter_connections) > 1 else []

# Restore direct connection
workflow['connections']['Set File ID'] = {
    "main": [false_path_connections]
}

# Remove filter connections
if 'Filter Already Processed' in workflow['connections']:
    del workflow['connections']['Filter Already Processed']

print("✅ Connexions restaurées: Set File ID → Workflow Configuration (direct)")
print()

# Save workflow
print("💾 Sauvegarde du workflow...")

workflow_update = {
    'name': workflow['name'],
    'nodes': workflow['nodes'],
    'connections': workflow['connections'],
    'settings': workflow.get('settings', {}),
    'staticData': workflow.get('staticData', None)
}

response = requests.put(
    f'{N8N_URL}/workflows/{WORKFLOW_ID}',
    json=workflow_update,
    headers=headers
)

if response.status_code == 200:
    print("✅ Workflow sauvegardé!")
    print()

    print("🔄 Réactivation du workflow...")
    response = requests.post(f'{N8N_URL}/workflows/{WORKFLOW_ID}/activate', headers=headers)

    if response.status_code == 200:
        print("✅ WORKFLOW RÉACTIVÉ!")
        print()
        print("=" * 80)
        print("🎉 WORKFLOW RESTAURÉ À L'ÉTAT FONCTIONNEL")
        print("=" * 80)
        print()
        print("✅ Le filtre problématique a été supprimé")
        print("✅ Les connexions sont restaurées")
        print("✅ Le workflow devrait se déclencher normalement maintenant")
        print()
        print("⏰ Prochaine vérification du dossier INPUT: dans 5 minutes max")
        print()
        print("⚠️ NOTE: Pour éviter la boucle infinie:")
        print("   - Ne PAS copier les fichiers *_clean* dans INPUT")
        print("   - Supprimer les fichiers INPUT après traitement")
        print("   - OU ajouter le filtre manuellement via l'interface N8N")
        print()
    else:
        print(f"⚠️ Erreur d'activation: {response.status_code}")
else:
    print(f"❌ Erreur de sauvegarde: {response.status_code}")
    print(response.text)

print("=" * 80)
