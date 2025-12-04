#!/usr/bin/env python3
"""
Fix Save image node to use correct OUTPUT folder
"""

import requests
import json

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

# CORRECT FOLDER IDs
INPUT_FOLDER = '1O1PrZoTDweXQx8ImVLXlJArei9hdvizn'
OUTPUT_FOLDER = '1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("FIX SAVE IMAGE NODE - OUTPUT FOLDER")
print("=" * 80)
print()
print(f"INPUT Folder (Alpha Medical Input):  {INPUT_FOLDER}")
print(f"OUTPUT Folder (Alpha Medical Output): {OUTPUT_FOLDER}")
print()

# Get workflow
response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    exit(1)

workflow = response.json()

print("📋 Checking nodes that save/upload files...")
print("-" * 80)
print()

fixed_count = 0
issues_found = []

for node in workflow['nodes']:
    node_name = node['name']
    node_type = node['type']
    params = node.get('parameters', {})

    # Look for Google Drive upload/save nodes
    if 'googleDrive' in node_type.lower():
        operation = params.get('operation', '')

        # Check if it's an upload operation
        if operation == 'upload' or 'save' in node_name.lower() or 'upload' in node_name.lower():
            print(f"🔍 Found: {node_name}")
            print(f"   Type: {node_type}")
            print(f"   Operation: {operation}")

            # Check folderId parameter
            if 'folderId' in params:
                folder_config = params['folderId']

                if isinstance(folder_config, dict):
                    current_folder = folder_config.get('value')
                else:
                    current_folder = folder_config

                print(f"   Current Folder: {current_folder}")

                # Check if it's pointing to INPUT instead of OUTPUT
                if current_folder == INPUT_FOLDER:
                    print(f"   ❌ WRONG! This should point to OUTPUT folder!")
                    issues_found.append({
                        'node': node_name,
                        'current': current_folder,
                        'expected': OUTPUT_FOLDER
                    })

                    # Fix it
                    if isinstance(folder_config, dict):
                        folder_config['value'] = OUTPUT_FOLDER
                    else:
                        params['folderId'] = {
                            '__rl': True,
                            'mode': 'list',
                            'value': OUTPUT_FOLDER,
                            'cachedResultName': 'Alpha Medical Output',
                            'cachedResultUrl': f'https://drive.google.com/drive/folders/{OUTPUT_FOLDER}'
                        }

                    print(f"   ✅ Fixed → {OUTPUT_FOLDER}")
                    fixed_count += 1

                elif current_folder == OUTPUT_FOLDER:
                    print(f"   ✅ Already correct (OUTPUT folder)")

                else:
                    print(f"   ⚠️ Unknown folder: {current_folder}")

            # Also check 'parent' parameter (some nodes use this)
            if 'parent' in params:
                parent_config = params['parent']
                if isinstance(parent_config, dict):
                    current_parent = parent_config.get('value')
                else:
                    current_parent = parent_config

                print(f"   Parent: {current_parent}")

                if current_parent == INPUT_FOLDER:
                    print(f"   ❌ WRONG! Parent should be OUTPUT!")
                    if isinstance(parent_config, dict):
                        parent_config['value'] = OUTPUT_FOLDER
                    else:
                        params['parent'] = OUTPUT_FOLDER
                    print(f"   ✅ Fixed parent → {OUTPUT_FOLDER}")
                    fixed_count += 1

            print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

if issues_found:
    print(f"❌ Found {len(issues_found)} configuration issues:")
    print()
    for issue in issues_found:
        print(f"  • {issue['node']}")
        print(f"    Was: {issue['current']} (INPUT - WRONG)")
        print(f"    Now: {issue['expected']} (OUTPUT - CORRECT)")
        print()

    print(f"Total fixes applied: {fixed_count}")
    print()

    if fixed_count > 0:
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
                print("🎉 OUTPUT FOLDER CONFIGURATION FIXED!")
                print("=" * 80)
                print()
                print("Next steps:")
                print("1. Upload new test image to INPUT folder")
                print("2. Wait 5 minutes for workflow to trigger")
                print("3. Check OUTPUT folder - processed image should appear there")
                print()
            else:
                print(f"⚠️ Activation error: {response.status_code}")
        else:
            print(f"❌ Update error: {response.status_code}")
            print(response.text)
    else:
        print("⚠️ No fixes were applied")
else:
    print("✅ No issues found - all save/upload nodes already point to OUTPUT folder")
    print()
    print("🤔 This is strange - if configuration is correct but files still")
    print("   go to INPUT folder, there might be a different issue:")
    print()
    print("   • Check workflow execution logs")
    print("   • Check if there's a 'Move' operation that moves files back to INPUT")
    print("   • Check node connections - maybe output goes through wrong path")

print()
print("=" * 80)
