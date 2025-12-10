#!/usr/bin/env python3
"""Verify N8N workflow status via REST API"""

import requests
import json

# Configuration
WORKFLOW_ID = "q0kyXyhCUq5gjmG2"
N8N_URL = "https://n8n.srv1168256.hstgr.cloud"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo"

def verify_workflow():
    """Verify workflow exists and check configuration"""
    url = f"{N8N_URL}/api/v1/workflows/{WORKFLOW_ID}"
    headers = {
        "X-N8N-API-KEY": API_KEY,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ API Error: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False

        data = response.json()

        print("=" * 60)
        print("✅ N8N WORKFLOW VERIFICATION")
        print("=" * 60)
        print(f"ID: {data.get('id')}")
        print(f"Name: {data.get('name')}")
        print(f"Status: {'🟢 ACTIVE' if data.get('active') else '🔴 INACTIVE'}")
        print(f"Nodes: {len(data.get('nodes', []))}")
        print(f"Created: {data.get('createdAt')}")
        print(f"Updated: {data.get('updatedAt')}")
        print()

        # Verify key node configurations
        print("=" * 60)
        print("NODE CONFIGURATION VERIFICATION")
        print("=" * 60)

        nodes = data.get('nodes', [])
        nodes_to_check = {
            'File Created': 'folderToWatch',
            'File Updated': 'folderToWatch',
            'Workflow Configuration': 'assignments'
        }

        configured_count = 0

        for node in nodes:
            node_name = node.get('name')
            if node_name in nodes_to_check:
                params = node.get('parameters', {})

                if node_name in ['File Created', 'File Updated']:
                    folder_id = params.get('folderToWatch', {}).get('value', '')
                    status = '✅' if folder_id else '❌'
                    print(f"{status} {node_name}: Folder ID = {folder_id or 'NOT SET'}")
                    if folder_id:
                        configured_count += 1

                elif node_name == 'Workflow Configuration':
                    assignments = params.get('assignments', {}).get('assignments', [])
                    for assign in assignments:
                        if assign.get('name') in ['google_sheet_id', 'dest_folder_id']:
                            value = assign.get('value', '')
                            status = '✅' if value else '❌'
                            print(f"{status} {node_name}: {assign['name']} = {value or 'NOT SET'}")
                            if value:
                                configured_count += 1

        print()
        print("=" * 60)
        print(f"Configuration Status: {configured_count}/4 nodes configured")
        print(f"Activation Status: {'ACTIVE - Ready to process' if data.get('active') else 'INACTIVE - Requires manual toggle'}")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    verify_workflow()
