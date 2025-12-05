#!/usr/bin/env python3
"""
Check if the filter I added broke the workflow
"""

import requests
import json

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("VÉRIFICATION: EST-CE QUE MON FILTRE A CASSÉ LE WORKFLOW?")
print("=" * 80)
print()

response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
workflow = response.json()

# Find the filter node
filter_node = None
for node in workflow['nodes']:
    if 'Filter' in node['name'] and 'Already Processed' in node['name']:
        filter_node = node
        break

if not filter_node:
    print("✅ Pas de filtre trouvé - le workflow est comme avant")
    exit(0)

print("🔍 FILTRE TROUVÉ:")
print(f"   Name: {filter_node['name']}")
print(f"   Type: {filter_node['type']}")
print()

# Check configuration
params = filter_node.get('parameters', {})
print("Configuration du filtre:")
print(json.dumps(params, indent=2))
print()

# Check connections
print("Connexions:")
print()

# Check what connects TO the filter
for node_name, connections in workflow['connections'].items():
    if 'main' in connections:
        for outputs in connections['main']:
            if outputs:
                for conn in outputs:
                    if conn['node'] == filter_node['name']:
                        print(f"  ✅ {node_name} → Filter Already Processed")

# Check what the filter connects TO
if filter_node['name'] in workflow['connections']:
    filter_connections = workflow['connections'][filter_node['name']]
    print()
    print(f"  Filter Already Processed connections:")
    if 'main' in filter_connections:
        for i, outputs in enumerate(filter_connections['main']):
            path_name = "TRUE" if i == 0 else "FALSE"
            if outputs:
                for conn in outputs:
                    print(f"    {path_name} → {conn['node']}")
            else:
                print(f"    {path_name} → (rien / stop)")

print()
print("=" * 80)
print("DIAGNOSTIC")
print("=" * 80)
print()

# The issue is likely in how I configured the IF node
# N8N IF nodes need proper structure

# Check the parameters structure
if 'conditions' in params:
    conditions = params['conditions']
    print("Conditions du filtre:")
    print(json.dumps(conditions, indent=2))
    print()

print("❌ PROBLÈME PROBABLE:")
print("   Le format du node IF que j'ai créé via API n'est peut-être pas compatible")
print("   avec la version actuelle de N8N.")
print()
print("SOLUTION:")
print("   SUPPRIMER le filtre et laisser le workflow fonctionner comme avant.")
print("   On pourra ajouter le filtre manuellement via l'interface N8N après.")
print()
print("=" * 80)
