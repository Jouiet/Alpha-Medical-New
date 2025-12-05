#!/usr/bin/env python3
"""
Analyze workflow outputs to understand how many images were generated
"""

import requests
from datetime import datetime

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("ANALYSE DES IMAGES GÉNÉRÉES PAR LE WORKFLOW")
print("=" * 80)
print()

# Get all executions
response = requests.get(f'{N8N_URL}/executions', headers=headers, params={'workflowId': WORKFLOW_ID, 'limit': 50})
executions = response.json()['data']

# Filter successful executions only
successful = [e for e in executions if e['status'] == 'success' and e.get('mode') != 'manual']

print(f"Total executions récentes: {len(executions)}")
print(f"Executions réussies (trigger mode): {len(successful)}")
print()

print("=" * 80)
print("DÉTAIL DES EXÉCUTIONS RÉUSSIES")
print("=" * 80)
print()

images_processed = []

for i, exec in enumerate(successful, 1):
    exec_id = exec['id']
    started = exec['startedAt']
    stopped = exec.get('stoppedAt', 'N/A')

    # Calculate duration
    if stopped != 'N/A':
        start_dt = datetime.fromisoformat(started.replace('Z', '+00:00'))
        stop_dt = datetime.fromisoformat(stopped.replace('Z', '+00:00'))
        duration = (stop_dt - start_dt).total_seconds()
    else:
        duration = 0

    print(f"Execution #{exec_id}:")
    print(f"  Started: {started}")
    print(f"  Duration: {duration:.0f} seconds")

    # Get execution details to find which file was processed
    response = requests.get(f'{N8N_URL}/executions/{exec_id}?includeData=true', headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Look for file name in the execution data
        if 'data' in data and 'resultData' in data['data'] and 'runData' in data['data']['resultData']:
            runData = data['data']['resultData']['runData']

            # Check "Set File ID" node for input file name
            if 'Set File ID' in runData:
                file_data = runData['Set File ID'][0]['data']['main'][0]
                if file_data and len(file_data) > 0:
                    input_file_name = file_data[0]['json'].get('input_file_name', 'Unknown')
                    print(f"  Input File: {input_file_name}")
                    images_processed.append({
                        'exec_id': exec_id,
                        'input_file': input_file_name,
                        'duration': duration,
                        'started': started
                    })

            # Check "Save image" node for output file info
            if 'Save image' in runData:
                save_data = runData['Save image'][0]['data']['main'][0]
                if save_data and len(save_data) > 0:
                    output_file_name = save_data[0]['json'].get('name', 'Unknown')
                    output_file_id = save_data[0]['json'].get('id', 'Unknown')
                    print(f"  Output File: {output_file_name}")
                    print(f"  Output File ID: {output_file_id}")

    print()

print("=" * 80)
print("RÉSUMÉ")
print("=" * 80)
print()

print(f"Total images traitées avec succès: {len(images_processed)}")
print()

if images_processed:
    print("Liste des fichiers traités:")
    for img in images_processed:
        print(f"  • {img['input_file']} (exec #{img['exec_id']}, {img['duration']:.0f}s)")
    print()

    # Check for duplicates
    file_names = [img['input_file'] for img in images_processed]
    unique_files = set(file_names)

    print(f"Fichiers uniques: {len(unique_files)}")
    print()

    if len(file_names) != len(unique_files):
        print("⚠️ ATTENTION: Certains fichiers ont été traités PLUSIEURS FOIS!")
        print()

        # Find duplicates
        from collections import Counter
        duplicates = {name: count for name, count in Counter(file_names).items() if count > 1}

        for filename, count in duplicates.items():
            print(f"  • {filename}: traité {count} fois")

            # Show when each duplicate was processed
            duplicate_execs = [img for img in images_processed if img['input_file'] == filename]
            for dup in duplicate_execs:
                print(f"    - Execution #{dup['exec_id']} at {dup['started']}")
        print()

        print("💡 EXPLICATION POSSIBLE:")
        print("   Le workflow se déclenche toutes les 5 minutes.")
        print("   Si un fichier prend >5 min à traiter OU si le trigger détecte")
        print("   le même fichier plusieurs fois, il sera traité plusieurs fois.")
        print()
        print("   Solutions:")
        print("   1. Déplacer/supprimer les fichiers INPUT après traitement")
        print("   2. Ajouter un filtre pour éviter de retraiter les fichiers")
        print("   3. Utiliser un dossier 'processed' pour archiver les inputs")
    else:
        print("✅ Chaque fichier a été traité UNE SEULE FOIS")

print()
print("=" * 80)
