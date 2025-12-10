#!/usr/bin/env python3
"""
Monitor clean test with single image
"""

import requests
from datetime import datetime
import time

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("🧪 TEST PROPRE - MONITORING")
print("=" * 80)
print()
print("Setup:")
print("  ✅ INPUT: 1 image seulement")
print("  ✅ OUTPUT: vide")
print("  ✅ Filtre anti-boucle: activé")
print()
print(f"⏰ Heure actuelle: {datetime.now().strftime('%H:%M:%S')}")
print()
print("Attente de la prochaine exécution (trigger every 5 min)...")
print()

# Get baseline execution count
response = requests.get(f'{N8N_URL}/executions', headers=headers, params={'workflowId': WORKFLOW_ID})
baseline_executions = response.json()['data']
baseline_count = len(baseline_executions)
latest_exec_id = baseline_executions[0]['id'] if baseline_executions else 0

print(f"📊 Baseline: {baseline_count} executions au total")
print(f"   Latest execution ID: #{latest_exec_id}")
print()

# Monitor for new executions
print("🔍 Monitoring en cours...")
print("-" * 80)
print()

check_count = 0
max_checks = 12  # 12 checks × 30 sec = 6 minutes

while check_count < max_checks:
    check_count += 1

    # Get current executions
    response = requests.get(f'{N8N_URL}/executions', headers=headers, params={'workflowId': WORKFLOW_ID})
    current_executions = response.json()['data']

    # Check for new executions
    new_executions = [e for e in current_executions if e['id'] > latest_exec_id]

    if new_executions:
        print(f"\n🎉 NOUVELLE EXÉCUTION DÉTECTÉE!")
        print("-" * 80)

        for exec in new_executions:
            exec_id = exec['id']
            status = exec['status']
            started = exec['startedAt']
            stopped = exec.get('stoppedAt', 'En cours...')

            print(f"\nExecution #{exec_id}:")
            print(f"  Status: {status.upper()}")
            print(f"  Started: {started}")

            if stopped != 'En cours...':
                start_dt = datetime.fromisoformat(started.replace('Z', '+00:00'))
                stop_dt = datetime.fromisoformat(stopped.replace('Z', '+00:00'))
                duration = (stop_dt - start_dt).total_seconds()
                print(f"  Duration: {duration:.0f} seconds")

            # Get execution details
            response = requests.get(f'{N8N_URL}/executions/{exec_id}?includeData=true', headers=headers)

            if response.status_code == 200:
                data = response.json()

                if 'data' in data and 'resultData' in data['data'] and 'runData' in data['data']['resultData']:
                    runData = data['data']['resultData']['runData']

                    # Check if filter stopped it
                    if 'Filter Already Processed' in runData:
                        filter_output = runData['Filter Already Processed'][0]['data']
                        print(f"\n  🔍 Filtre:")

                        # Check which path was taken
                        if filter_output.get('main'):
                            if filter_output['main'][0]:  # TRUE path
                                print(f"     ✋ FICHIER IGNORÉ (contient '_clean')")
                            elif len(filter_output['main']) > 1 and filter_output['main'][1]:  # FALSE path
                                print(f"     ✅ FICHIER TRAITÉ (pas de '_clean')")

                    # Check file processed
                    if 'Set File ID' in runData:
                        file_data = runData['Set File ID'][0]['data']['main'][0]
                        if file_data and len(file_data) > 0:
                            input_file = file_data[0]['json'].get('input_file_name', 'Unknown')
                            print(f"\n  📄 Input: {input_file}")

                    # Check output saved
                    if 'Save image' in runData:
                        save_data = runData['Save image'][0]['data']['main'][0]
                        if save_data and len(save_data) > 0:
                            output_file = save_data[0]['json'].get('name', 'Unknown')
                            output_id = save_data[0]['json'].get('id', 'Unknown')
                            print(f"  💾 Output: {output_file}")
                            print(f"  🆔 File ID: {output_id}")

        latest_exec_id = new_executions[0]['id']

        print()
        print("=" * 80)
        print("✅ TEST TERMINÉ - VÉRIFIEZ:")
        print("=" * 80)
        print()
        print("1. Dossier OUTPUT:")
        print("   https://drive.google.com/drive/folders/1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox")
        print("   → Devrait contenir 1 fichier avec '_clean'")
        print()
        print("2. Google Sheet:")
        print("   https://docs.google.com/spreadsheets/d/1Q5ujL0LQEz-kgGkg-oMzCutcpUnznpDPpRkqh1hUBUw/edit")
        print("   → Devrait avoir 1 nouvelle ligne avec status 'Completed'")
        print()
        print("3. Attendre 5 minutes de plus:")
        print("   → Le workflow NE DEVRAIT PAS retraiter le fichier output!")
        print("   → Le filtre devrait l'ignorer!")
        print()

        break

    # Wait 30 seconds before next check
    if check_count < max_checks:
        time.sleep(30)
        print(f"Check #{check_count}/{max_checks} - {datetime.now().strftime('%H:%M:%S')} - Aucune nouvelle exécution...")

if check_count == max_checks:
    print()
    print("⏰ Timeout atteint (6 minutes)")
    print()
    print("💡 Le trigger se déclenche toutes les 5 minutes.")
    print("   Si aucune exécution n'a été détectée:")
    print("   1. Vérifiez que le fichier est bien dans INPUT")
    print("   2. Vérifiez que le workflow est ACTIVE")
    print("   3. Attendez encore 5 minutes")

print()
