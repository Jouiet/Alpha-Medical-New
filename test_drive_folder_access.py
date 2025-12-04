#!/usr/bin/env python3
"""
Test if N8N credential can access Google Drive folder and list files
"""

import requests

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 70)
print("GOOGLE DRIVE FOLDER ACCESS TEST")
print("=" * 70)
print()

# Get workflow to see File Created node configuration
response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)

if response.status_code == 200:
    workflow = response.json()

    # Find File Created node
    for node in workflow['nodes']:
        if 'File Created' in node['name'] or node['type'] == 'n8n-nodes-base.googleDriveTrigger':
            print(f"📋 Found trigger node: {node['name']}")
            print(f"   Type: {node['type']}")
            print()
            print("⚙️ CONFIGURATION:")
            print("-" * 70)

            params = node.get('parameters', {})

            # Check folder configuration
            if 'folderId' in params:
                folder_id = params['folderId']
                print(f"✅ Folder ID: {folder_id}")
            elif 'folderToWatch' in params:
                print(f"✅ Folder to Watch: {params['folderToWatch']}")
            else:
                print("⚠️ NO FOLDER CONFIGURED!")
                print(f"   Parameters: {list(params.keys())}")

            # Check trigger settings
            if 'triggerOn' in params:
                print(f"✅ Trigger On: {params['triggerOn']}")

            # Check filters/options
            if 'options' in params:
                print(f"✅ Options: {params['options']}")

            # Check credential
            if 'credentials' in node:
                creds = node['credentials']
                print()
                print("🔐 CREDENTIAL:")
                print("-" * 70)
                for cred_type, cred_info in creds.items():
                    print(f"   Type: {cred_type}")
                    print(f"   ID: {cred_info.get('id', 'N/A')}")

            print()
            print("=" * 70)
            print()
            print("💡 EXPECTED FOLDER ID: 1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox")
            print()

            # Check if folder ID matches
            if 'folderId' in params:
                if params['folderId'] == '1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox':
                    print("✅ Folder ID matches!")
                else:
                    print(f"❌ FOLDER ID MISMATCH!")
                    print(f"   Expected: 1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox")
                    print(f"   Actual:   {params['folderId']}")

            break
    else:
        print("❌ Could not find File Created node")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print()
print("=" * 70)
