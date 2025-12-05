#!/usr/bin/env python3
"""
Fix Google Sheet tab ID in workflow
"""

import requests

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'
SPREADSHEET_ID = '1Q5ujL0LQEz-kgGkg-oMzCutcpUnznpDPpRkqh1hUBUw'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 70)
print("FIX GOOGLE SHEET TAB ID")
print("=" * 70)
print()

# Step 1: Get Google Sheets metadata to find "Photos" tab ID
print("📋 STEP 1: Getting Google Sheet tabs...")

# We'll use N8N to execute a Google Sheets operation to get sheet metadata
# But first, let's get the workflow and update the sheet IDs manually

# For now, we'll use a common approach: the user needs to get the gid from the URL
# when they click on the Photos tab

print("⚠️ To get the Sheet ID, you need to:")
print("1. Open: https://docs.google.com/spreadsheets/d/1Q5ujL0LQEz-kgGkg-oMzCutcpUnznpDPpRkqh1hUBUw/edit")
print("2. Click on the 'Photos' tab at the bottom")
print("3. Look at the URL - it will change to:")
print("   ...edit#gid=XXXXXXXXX")
print("4. Copy the number after 'gid='")
print()

# Alternative: Get from N8N workflow execution if we can test the sheet node
# For now, let's check the workflow and see what sheet configuration it has

response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Error getting workflow: {response.status_code}")
    exit(1)

workflow = response.json()

print("📋 STEP 2: Checking current Sheet configuration in workflow...")
print("-" * 70)

sheet_nodes = []
for node in workflow['nodes']:
    if node['type'] == 'n8n-nodes-base.googleSheets':
        params = node.get('parameters', {})
        print(f"\n🔹 Node: {node['name']}")

        if 'sheetId' in params:
            print(f"   Sheet ID: {params['sheetId']}")
            sheet_nodes.append({
                'name': node['name'],
                'current_id': params['sheetId']
            })

        # Check if it's by name or ID
        if 'sheetName' in params:
            print(f"   Sheet Name: {params['sheetName']}")

print()
print("=" * 70)
print()

if sheet_nodes:
    print(f"Found {len(sheet_nodes)} Google Sheets nodes with sheet IDs")
    print()
    print("CURRENT CONFIGURATION:")
    for node_info in sheet_nodes:
        print(f"  - {node_info['name']}: {node_info['current_id']}")

    print()
    print("=" * 70)
    print()
    print("NEXT STEP:")
    print("Run this script with the new Sheet ID as argument:")
    print()
    print("  python3 fix_sheet_id.py NEW_SHEET_ID")
    print()
    print("To get NEW_SHEET_ID:")
    print("  1. Go to Google Sheet")
    print("  2. Click 'Photos' tab")
    print("  3. URL will show: #gid=XXXXXXXXX")
    print("  4. Copy XXXXXXXXX (the number)")
    print()
else:
    print("⚠️ No Google Sheets nodes found with sheetId parameter")

print("=" * 70)
