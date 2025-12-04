#!/usr/bin/env python3
"""
Update Google Sheet configuration in workflow
"""

import requests

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

# CORRECT SHEET CONFIGURATION
CORRECT_SPREADSHEET_ID = '1Q5ujL0LQEz-kgGkg-oMzCutcpUnznpDPpRkqh1hUBUw'
CORRECT_SHEET_ID = 0  # gid=0 from URL

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 70)
print("UPDATE GOOGLE SHEET CONFIGURATION")
print("=" * 70)
print()
print("CORRECT CONFIGURATION:")
print(f"  Spreadsheet ID: {CORRECT_SPREADSHEET_ID}")
print(f"  Sheet ID: {CORRECT_SHEET_ID}")
print()

# Get workflow
response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    exit(1)

workflow = response.json()

print("📋 Updating Google Sheets nodes...")
print("-" * 70)

updated_count = 0

for node in workflow['nodes']:
    if node['type'] == 'n8n-nodes-base.googleSheets':
        params = node.get('parameters', {})

        # Update documentId (Spreadsheet ID)
        if 'documentId' in params:
            old_doc_id = params['documentId']
            if isinstance(old_doc_id, dict) and 'value' in old_doc_id:
                old_doc_id = old_doc_id['value']

            if old_doc_id != CORRECT_SPREADSHEET_ID:
                # Update the documentId structure
                params['documentId'] = {
                    '__rl': True,
                    'mode': 'list',
                    'value': CORRECT_SPREADSHEET_ID
                }
                print(f"   ✅ Updated '{node['name']}' → Spreadsheet ID")
                updated_count += 1

        # Update sheetName (Sheet ID/gid)
        if 'sheetName' in params:
            sheet_config = params['sheetName']
            if isinstance(sheet_config, dict):
                old_sheet_id = sheet_config.get('value')

                if old_sheet_id != CORRECT_SHEET_ID:
                    sheet_config['value'] = CORRECT_SHEET_ID
                    sheet_config['cachedResultUrl'] = f'https://docs.google.com/spreadsheets/d/{CORRECT_SPREADSHEET_ID}/edit#gid={CORRECT_SHEET_ID}'
                    sheet_config['cachedResultName'] = 'Photos'
                    print(f"   ✅ Updated '{node['name']}' → Sheet ID")
                    updated_count += 1

print()
print(f"Total updates: {updated_count}")
print()

if updated_count > 0:
    print("📋 Saving updated workflow...")

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
            print("🎉 GOOGLE SHEET CONFIGURATION FIXED!")
            print()
            print("Next: Upload new image and wait 5 min")
        else:
            print(f"⚠️ Activation: {response.status_code}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
else:
    print("✅ No updates needed - configuration already correct")

print()
print("=" * 70)
