#!/usr/bin/env python3
"""
FIX: Swap INPUT and OUTPUT folder IDs in workflow
"""

import requests

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

# CORRECT IDs
CORRECT_INPUT_ID = '1O1PrZoTDweXQx8ImVLXlJArei9hdvizn'
CORRECT_OUTPUT_ID = '1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox'

print("=" * 70)
print("FIX FOLDER IDs SWAP")
print("=" * 70)
print()
print("CORRECT MAPPING:")
print(f"  INPUT:  {CORRECT_INPUT_ID} (Alpha Medical Input)")
print(f"  OUTPUT: {CORRECT_OUTPUT_ID} (Alpha Medical Output)")
print()

# Get workflow
response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    exit(1)

workflow = response.json()

# Fix folder IDs
updated_count = 0

for node in workflow['nodes']:
    params = node.get('parameters', {})

    # Check for folder configuration
    if 'folderId' in params:
        old_id = params['folderId']
        if old_id == CORRECT_OUTPUT_ID:
            # This is using OUTPUT as INPUT - swap it
            params['folderId'] = CORRECT_INPUT_ID
            print(f"✅ Fixed node '{node['name']}': folderId")
            updated_count += 1

    if 'folderToWatch' in params:
        folder_config = params['folderToWatch']
        if isinstance(folder_config, dict) and 'value' in folder_config:
            old_id = folder_config['value']
            if old_id == CORRECT_OUTPUT_ID:
                # Trigger watching OUTPUT instead of INPUT - swap it
                folder_config['value'] = CORRECT_INPUT_ID
                print(f"✅ Fixed node '{node['name']}': folderToWatch → INPUT")
                updated_count += 1

    # Check for destination folder (should be OUTPUT)
    if 'driveId' in params or 'folderId' in params:
        # For nodes that SAVE/UPLOAD, we want OUTPUT
        if node['name'] in ['Save image', 'Upload', 'Move to Output']:
            if 'folderId' in params:
                old_id = params['folderId']
                if old_id == CORRECT_INPUT_ID:
                    params['folderId'] = CORRECT_OUTPUT_ID
                    print(f"✅ Fixed node '{node['name']}': folderId → OUTPUT")
                    updated_count += 1

print()
print(f"Total fixes: {updated_count}")
print()

if updated_count > 0:
    # Save workflow
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

        # Reactivate
        response = requests.post(f'{N8N_URL}/workflows/{WORKFLOW_ID}/activate', headers=headers)

        if response.status_code == 200:
            print("✅ WORKFLOW REACTIVATED!")
            print()
            print("🎉 FOLDER IDs NOW CORRECT!")
            print()
            print("Next: Upload new image to INPUT folder and wait 5 min")
        else:
            print(f"⚠️ Activation status: {response.status_code}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
else:
    print("✅ No fixes needed - folder IDs already correct")

print()
print("=" * 70)
