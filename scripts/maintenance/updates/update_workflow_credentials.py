#!/usr/bin/env python3
"""
Update N8N workflow with new credential IDs
"""

import requests
import sys

# N8N API config
N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

if len(sys.argv) != 4:
    print("Usage: python3 update_workflow_credentials.py <drive_id> <sheets_id> <gemini_id>")
    print()
    print("Example:")
    print("  python3 update_workflow_credentials.py ABC123 DEF456 GHI789")
    sys.exit(1)

NEW_DRIVE_ID = sys.argv[1]
NEW_SHEETS_ID = sys.argv[2]
NEW_GEMINI_ID = sys.argv[3]

# Old IDs to replace
OLD_DRIVE_ID = 'htidcOV6hR8kh9tB'
OLD_GEMINI_ID = '7tlny7NnnrQIfupF'
OLD_SHEETS_ID = 'HTAGRgrsWTF0cfU2'

print("=" * 70)
print("UPDATE WORKFLOW CREDENTIALS")
print("=" * 70)
print()
print("REPLACEMENTS:")
print(f"  Google Drive:  {OLD_DRIVE_ID} → {NEW_DRIVE_ID}")
print(f"  Google Gemini: {OLD_GEMINI_ID} → {NEW_GEMINI_ID}")
print(f"  Google Sheets: {OLD_SHEETS_ID} → {NEW_SHEETS_ID}")
print()

# Step 1: Get workflow
print("📋 STEP 1: Getting workflow...")
response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
    sys.exit(1)

workflow = response.json()
print(f"✅ Loaded: {workflow['name']}")
print()

# Step 2: Update credential IDs in nodes
print("📋 STEP 2: Updating credential IDs...")
updated_count = 0

for node in workflow['nodes']:
    if 'credentials' in node and node['credentials']:
        for cred_type, cred_info in node['credentials'].items():
            old_id = cred_info.get('id')

            if old_id == OLD_DRIVE_ID:
                cred_info['id'] = NEW_DRIVE_ID
                print(f"   ✅ Updated '{node['name']}' → Drive: {NEW_DRIVE_ID}")
                updated_count += 1
            elif old_id == OLD_GEMINI_ID:
                cred_info['id'] = NEW_GEMINI_ID
                print(f"   ✅ Updated '{node['name']}' → Gemini: {NEW_GEMINI_ID}")
                updated_count += 1
            elif old_id == OLD_SHEETS_ID:
                cred_info['id'] = NEW_SHEETS_ID
                print(f"   ✅ Updated '{node['name']}' → Sheets: {NEW_SHEETS_ID}")
                updated_count += 1

print()
print(f"   Total updated: {updated_count} credential references")
print()

# Step 3: Save updated workflow
print("📋 STEP 3: Saving updated workflow...")

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

if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
    sys.exit(1)

print("✅ Workflow updated with new credential IDs!")
print()

# Step 4: Activate workflow
print("📋 STEP 4: Activating workflow...")

response = requests.post(f'{N8N_URL}/workflows/{WORKFLOW_ID}/activate', headers=headers)

if response.status_code == 200:
    print("✅ WORKFLOW ACTIVATED SUCCESSFULLY!")
    print()
    print("🎉 Workflow is now LIVE and monitoring Google Drive folder")
    print()
    print("Next step: Test with a sample image")
    print("  1. Upload image to: https://drive.google.com/drive/folders/1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox")
    print("  2. Wait ~5 minutes (workflow checks every 5 min)")
    print("  3. Check output: https://drive.google.com/drive/folders/1O1PrZoTDweXQx8ImVLXlJArei9hdvizn")
else:
    print(f"⚠️ Activation status: {response.status_code}")
    print(response.text)
    print()
    print("Note: You may need to manually activate in N8N UI")
    print("  Go to: https://n8n.srv1168256.hstgr.cloud/workflow/q0kyXyhCUq5gjmG2")
    print("  Toggle 'Active' switch to ON")

print()
print("=" * 70)
