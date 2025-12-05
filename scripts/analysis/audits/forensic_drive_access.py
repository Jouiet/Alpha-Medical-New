#!/usr/bin/env python3
"""
FORENSIC ANALYSIS: Test Google Drive API access directly
"""

import requests
import json

# Get workflow to extract OAuth token info
N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
FOLDER_ID = '1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 70)
print("FORENSIC ANALYSIS: GOOGLE DRIVE ACCESS")
print("=" * 70)
print()

# Problem: N8N API doesn't expose OAuth tokens
# We need to test directly through N8N workflow execution

print("📋 TEST 1: Execute workflow node manually")
print("-" * 70)

# Create a test execution payload to manually trigger the Google Drive node
test_workflow = {
    "name": "Test Drive Access",
    "nodes": [
        {
            "parameters": {
                "resource": "file",
                "operation": "list",
                "folderId": {
                    "__rl": True,
                    "mode": "id",
                    "value": FOLDER_ID
                },
                "limit": 10
            },
            "name": "List Files",
            "type": "n8n-nodes-base.googleDrive",
            "typeVersion": 3,
            "position": [250, 300],
            "credentials": {
                "googleDriveOAuth2Api": {
                    "id": "RNAn3iOxS7ylrWcI",
                    "name": "Google Drive account"
                }
            }
        }
    ],
    "connections": {},
    "active": False,
    "settings": {},
    "staticData": None
}

# Create temporary test workflow
response = requests.post(f'{N8N_URL}/workflows', json=test_workflow, headers=headers)

if response.status_code in [200, 201]:
    test_wf = response.json()
    test_wf_id = test_wf['id']
    print(f"✅ Created test workflow: {test_wf_id}")

    # Execute it
    print()
    print("📋 TEST 2: Execute test workflow to list files")
    print("-" * 70)

    exec_response = requests.post(
        f'{N8N_URL}/workflows/{test_wf_id}/test',
        json={},
        headers=headers
    )

    if exec_response.status_code == 200:
        result = exec_response.json()
        print("✅ Execution successful!")
        print()

        # Check if files were found
        if 'data' in result:
            if 'resultData' in result['data']:
                runs = result['data']['resultData'].get('runData', {})
                if 'List Files' in runs:
                    file_data = runs['List Files'][0].get('data', {})
                    main_data = file_data.get('main', [])

                    if main_data and len(main_data) > 0:
                        files = main_data[0]
                        print(f"✅ FOUND {len(files)} FILES IN FOLDER!")
                        print()
                        for i, file_info in enumerate(files[:5], 1):
                            if 'json' in file_info:
                                file_json = file_info['json']
                                print(f"   {i}. {file_json.get('name', 'Unknown')}")
                                print(f"      ID: {file_json.get('id', 'N/A')}")
                                print(f"      Type: {file_json.get('mimeType', 'N/A')}")
                                print()
                    else:
                        print("❌ FOLDER IS EMPTY (from API perspective)")
                        print()
                        print("💡 POSSIBLE CAUSES:")
                        print("   1. Credential account doesn't have access to this folder")
                        print("   2. Folder ID is incorrect")
                        print("   3. Files are in a subfolder")
    else:
        print(f"❌ Execution failed: {exec_response.status_code}")
        print(exec_response.text)

    # Cleanup: delete test workflow
    requests.delete(f'{N8N_URL}/workflows/{test_wf_id}', headers=headers)
    print()
    print("🗑️ Test workflow deleted")

else:
    print(f"❌ Failed to create test workflow: {response.status_code}")
    print(response.text)

print()
print("=" * 70)
print()
print("📋 NEXT STEPS BASED ON RESULTS:")
print()
print("IF FILES FOUND:")
print("   → Credential has access, trigger configuration issue")
print("   → Solution: Change trigger from 'File Created' to 'File Created or Updated'")
print()
print("IF NO FILES FOUND:")
print("   → Credential doesn't have access to folder")
print("   → Solution: Share folder with jouiet.hat@gmail.com")
print()
print("=" * 70)
