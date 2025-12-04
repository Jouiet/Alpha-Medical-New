#!/usr/bin/env python3
"""
Fix N8N Image Processing workflow activation by assigning credentials
"""

import requests
import json

# N8N API config
N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 70)
print("FIX N8N IMAGE PROCESSING WORKFLOW")
print("=" * 70)
print()

# Step 1: Get workflow first to see what we're dealing with
print("📋 STEP 1: Getting workflow to check status...")
print("-" * 70)

# Step 2: Get workflow details
print("📋 STEP 2: Getting workflow details...")
print("-" * 70)

response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Error getting workflow: {response.status_code}")
    print(response.text)
    exit(1)

workflow = response.json()
print(f"✅ Workflow: {workflow['name']}")
print(f"   Nodes: {len(workflow['nodes'])}")
print(f"   Active: {workflow['active']}")
print()

# Step 3: Check which nodes need credentials
print("📋 STEP 3: Checking nodes that need credentials...")
print("-" * 70)

nodes_needing_creds = []
for node in workflow['nodes']:
    if 'credentials' in node and node['credentials']:
        for cred_type, cred_info in node['credentials'].items():
            print(f"   Node '{node['name']}' needs: {cred_type}")

            # Check if credential ID is assigned
            if 'id' not in cred_info or not cred_info['id']:
                nodes_needing_creds.append({
                    'node': node['name'],
                    'type': cred_type,
                    'current_id': cred_info.get('id', None)
                })
                print(f"      ⚠️ Missing credential ID!")
            else:
                print(f"      ✅ Assigned: {cred_info['id']}")

print()

if not nodes_needing_creds:
    print("✅ All nodes have credentials assigned!")
    print()
    print("📋 STEP 4: Activating workflow...")
    print("-" * 70)

    # Try to activate
    workflow['active'] = True
    response = requests.put(
        f'{N8N_URL}/workflows/{WORKFLOW_ID}',
        json=workflow,
        headers=headers
    )

    if response.status_code == 200:
        print("✅ Workflow activated successfully!")
    else:
        print(f"❌ Error activating workflow: {response.status_code}")
        print(response.text)
else:
    print(f"⚠️ {len(nodes_needing_creds)} nodes need credential assignment:")
    for item in nodes_needing_creds:
        print(f"   - {item['node']}: {item['type']}")

    print()
    print("📋 STEP 4: Assigning credentials to nodes...")
    print("-" * 70)

    # Assign credentials
    updated = False
    for node in workflow['nodes']:
        if 'credentials' in node and node['credentials']:
            for cred_type, cred_info in node['credentials'].items():
                if 'id' not in cred_info or not cred_info['id']:
                    # Try to find matching credential
                    if cred_type in cred_map:
                        old_id = cred_info.get('id', 'None')
                        cred_info['id'] = cred_map[cred_type]
                        print(f"   ✅ Assigned '{node['name']}' → {cred_type}: {cred_map[cred_type]}")
                        updated = True
                    else:
                        print(f"   ❌ No credential found for type: {cred_type}")

    if updated:
        print()
        print("📋 STEP 5: Saving updated workflow...")
        print("-" * 70)

        response = requests.put(
            f'{N8N_URL}/workflows/{WORKFLOW_ID}',
            json=workflow,
            headers=headers
        )

        if response.status_code == 200:
            print("✅ Workflow updated with credentials!")

            print()
            print("📋 STEP 6: Activating workflow...")
            print("-" * 70)

            # Now activate
            workflow['active'] = True
            response = requests.put(
                f'{N8N_URL}/workflows/{WORKFLOW_ID}',
                json=workflow,
                headers=headers
            )

            if response.status_code == 200:
                print("✅ Workflow activated successfully!")
            else:
                print(f"⚠️ Could not activate: {response.status_code}")
                print(response.text)
                print()
                print("This is likely because the trigger node needs data to validate.")
                print("Upload 1 test image to Google Drive folder and try activating manually.")
        else:
            print(f"❌ Error updating workflow: {response.status_code}")
            print(response.text)
    else:
        print("❌ No credentials could be assigned")

print()
print("=" * 70)
print("DONE")
print("=" * 70)
