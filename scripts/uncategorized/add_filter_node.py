#!/usr/bin/env python3
"""
Add IF filter node to prevent reprocessing files with '_clean' in name
"""

import requests
import json

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("AJOUTER FILTRE POUR ÉVITER BOUCLE INFINIE")
print("=" * 80)
print()

response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    exit(1)

workflow = response.json()

# Check if filter already exists
filter_exists = False
for node in workflow['nodes']:
    if 'Filter' in node['name'] or 'IF' in node['name']:
        if 'clean' in str(node.get('parameters', {})):
            filter_exists = True
            print(f"✅ Filter node already exists: {node['name']}")
            print("   No need to add another one.")
            exit(0)

print("📋 Adding IF filter node to prevent reprocessing '_clean' files...")
print()

# Find "Set File ID" node position
set_file_id_node = None
for node in workflow['nodes']:
    if node['name'] == 'Set File ID':
        set_file_id_node = node
        break

if not set_file_id_node:
    print("❌ Cannot find 'Set File ID' node")
    exit(1)

# Create new IF node
new_if_node = {
    "name": "Filter Already Processed",
    "type": "n8n-nodes-base.if",
    "typeVersion": 2,
    "position": [
        set_file_id_node['position'][0] + 300,  # 300px to the right
        set_file_id_node['position'][1]
    ],
    "parameters": {
        "conditions": {
            "options": {
                "caseSensitive": True,
                "leftValue": "",
                "typeValidation": "strict"
            },
            "conditions": [
                {
                    "id": "1234567890",
                    "leftValue": "={{ $json.input_file_name }}",
                    "rightValue": "_clean",
                    "operator": {
                        "type": "string",
                        "operation": "contains",
                        "name": "filter.operator.contains"
                    }
                }
            ],
            "combinator": "and"
        },
        "options": {}
    }
}

# Add the new node
workflow['nodes'].append(new_if_node)

print(f"✅ Created new IF node: {new_if_node['name']}")
print(f"   Position: {new_if_node['position']}")
print()

# Update connections
# Current: Set File ID → Workflow Configuration
# New: Set File ID → Filter Already Processed → (FALSE) → Workflow Configuration
#                                           → (TRUE) → Stop (no connection)

print("📋 Updating connections...")

# Find the connection from "Set File ID"
if 'Set File ID' not in workflow['connections']:
    workflow['connections']['Set File ID'] = {"main": []}

# Save old connection
old_connections = workflow['connections']['Set File ID']['main'][0] if workflow['connections']['Set File ID']['main'] else []

# New connection: Set File ID → Filter Already Processed
workflow['connections']['Set File ID']['main'] = [[{
    "node": "Filter Already Processed",
    "type": "main",
    "index": 0
}]]

# New connection: Filter Already Processed (FALSE) → old connections
workflow['connections']['Filter Already Processed'] = {
    "main": [
        [],  # TRUE path = empty (stop processing)
        old_connections  # FALSE path = continue to old connections
    ]
}

print("✅ Connections updated:")
print("   Set File ID → Filter Already Processed")
print("   Filter Already Processed (FALSE) → Continue workflow")
print("   Filter Already Processed (TRUE) → Stop")
print()

# Save workflow
print("💾 Saving workflow...")

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
    print("✅ Workflow updated!")
    print()
    print("🔄 Reactivating workflow...")

    response = requests.post(f'{N8N_URL}/workflows/{WORKFLOW_ID}/activate', headers=headers)

    if response.status_code == 200:
        print("✅ WORKFLOW REACTIVATED!")
        print()
        print("=" * 80)
        print("🎉 FILTRE AJOUTÉ AVEC SUCCÈS!")
        print("=" * 80)
        print()
        print("✅ Le workflow ignorera maintenant tous les fichiers avec '_clean' dans le nom")
        print()
        print("Comportement:")
        print("  • 5-lifestyle.jpg → TRAITÉ ✅")
        print("  • 5-lifestyle_clean.png → IGNORÉ ✅")
        print("  • product.jpg → TRAITÉ ✅")
        print("  • product_clean.png → IGNORÉ ✅")
        print()
        print("🛡️ Boucle infinie = ÉVITÉE!")
        print()
    else:
        print(f"⚠️ Activation error: {response.status_code}")
else:
    print(f"❌ Update error: {response.status_code}")
    print(response.text)

print("=" * 80)
