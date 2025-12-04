#!/usr/bin/env python3
"""
Fix Workflow Configuration node - dest_folder_id
"""

import requests

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

INPUT_FOLDER = '1O1PrZoTDweXQx8ImVLXlJArei9hdvizn'
OUTPUT_FOLDER = '1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("FIX WORKFLOW CONFIGURATION - dest_folder_id")
print("=" * 80)
print()
print("🐛 PROBLEM FOUND:")
print(f"   Current dest_folder_id: {INPUT_FOLDER} (INPUT - WRONG!)")
print(f"   Should be: {OUTPUT_FOLDER} (OUTPUT - CORRECT!)")
print()

response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    exit(1)

workflow = response.json()

# Find Workflow Configuration node
config_node = None
for node in workflow['nodes']:
    if node['name'] == 'Workflow Configuration':
        config_node = node
        break

if not config_node:
    print("❌ Workflow Configuration node not found!")
    exit(1)

print("📋 Found 'Workflow Configuration' node")

params = config_node.get('parameters', {})
assignments = params.get('assignments', {}).get('assignments', [])

print(f"   Current assignments: {len(assignments)}")
print()

# Find and fix dest_folder_id
fixed = False
for assignment in assignments:
    if assignment.get('name') == 'dest_folder_id':
        old_value = assignment.get('value')
        print(f"✅ Found dest_folder_id assignment")
        print(f"   Old value: {old_value}")

        if old_value == INPUT_FOLDER:
            assignment['value'] = OUTPUT_FOLDER
            print(f"   ✅ FIXED → {OUTPUT_FOLDER}")
            fixed = True
        elif old_value == OUTPUT_FOLDER:
            print(f"   ✅ Already correct!")
        else:
            print(f"   ⚠️ Unexpected value: {old_value}")

if not fixed:
    print("⚠️ No fix needed - already correct")
    exit(0)

print()
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
        print("🎉 DEST_FOLDER_ID FIXED!")
        print("=" * 80)
        print()
        print("✅ SOLUTION:")
        print("   'Workflow Configuration' node now has:")
        print(f"   dest_folder_id = {OUTPUT_FOLDER} (OUTPUT folder)")
        print()
        print("   'Save image' node will now save to OUTPUT folder!")
        print()
        print("NEXT STEPS:")
        print("1. Upload new test image to INPUT folder")
        print("2. Wait 5 minutes for workflow to trigger")
        print("3. Check OUTPUT folder - processed image should appear there!")
        print()
    else:
        print(f"⚠️ Activation error: {response.status_code}")
else:
    print(f"❌ Update error: {response.status_code}")
    print(response.text)

print("=" * 80)
