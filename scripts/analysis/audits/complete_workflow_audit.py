#!/usr/bin/env python3
"""
COMPLETE WORKFLOW AUDIT - Find ALL problems at once
"""

import requests
import json

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

# EXPECTED CONFIGURATION
EXPECTED = {
    'input_folder': '1O1PrZoTDweXQx8ImVLXlJArei9hdvizn',
    'output_folder': '1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox',
    'spreadsheet_id': '1Q5ujL0LQEz-kgGkg-oMzCutcpUnznpDPpRkqh1hUBUw',
    'sheet_id': 0,
    'drive_cred_id': 'RNAn3iOxS7ylrWcI',
    'sheets_cred_id': '6cpCac7AwIY6KXsT',
    'gemini_cred_id': '9vTsafFRenZVzLYa'
}

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 80)
print("COMPLETE WORKFLOW AUDIT - FINDING ALL PROBLEMS")
print("=" * 80)
print()

response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)
if response.status_code != 200:
    print(f"❌ Cannot get workflow: {response.status_code}")
    exit(1)

workflow = response.json()
problems = []
fixes_needed = []

print(f"Workflow: {workflow['name']}")
print(f"Active: {workflow['active']}")
print(f"Nodes: {len(workflow['nodes'])}")
print()

print("=" * 80)
print("AUDITING EACH NODE...")
print("=" * 80)

for node in workflow['nodes']:
    node_name = node['name']
    node_type = node['type']
    params = node.get('parameters', {})
    creds = node.get('credentials', {})

    print(f"\n🔹 {node_name} ({node_type})")

    # Check credentials
    if creds:
        for cred_type, cred_info in creds.items():
            cred_id = cred_info.get('id')
            expected_id = None

            if 'googleDrive' in cred_type:
                expected_id = EXPECTED['drive_cred_id']
            elif 'googleSheets' in cred_type:
                expected_id = EXPECTED['sheets_cred_id']
            elif 'googlePalm' in cred_type or 'gemini' in cred_type.lower():
                expected_id = EXPECTED['gemini_cred_id']

            if expected_id and cred_id != expected_id:
                problems.append(f"❌ {node_name}: Wrong credential ID")
                fixes_needed.append({
                    'node': node_name,
                    'issue': f'credential {cred_type}',
                    'expected': expected_id,
                    'actual': cred_id
                })
                print(f"   ❌ Credential: {cred_id} (expected: {expected_id})")
            else:
                print(f"   ✅ Credential: {cred_id}")

    # Check Google Drive nodes
    if 'googleDrive' in node_type.lower():
        # Check folder configuration
        if 'folderId' in params:
            folder_config = params['folderId']
            if isinstance(folder_config, dict):
                folder_id = folder_config.get('value')
            else:
                folder_id = folder_config

            # Determine if this should be input or output
            if 'File Created' in node_name or 'File Updated' in node_name or 'Download' in node_name:
                expected_folder = EXPECTED['input_folder']
                folder_type = 'INPUT'
            elif 'Save' in node_name or 'Upload' in node_name:
                expected_folder = EXPECTED['output_folder']
                folder_type = 'OUTPUT'
            else:
                expected_folder = None
                folder_type = 'UNKNOWN'

            if expected_folder:
                if folder_id != expected_folder:
                    problems.append(f"❌ {node_name}: Wrong folder ({folder_type})")
                    fixes_needed.append({
                        'node': node_name,
                        'issue': f'folder ({folder_type})',
                        'expected': expected_folder,
                        'actual': folder_id
                    })
                    print(f"   ❌ Folder: {folder_id} (expected {folder_type}: {expected_folder})")
                else:
                    print(f"   ✅ Folder ({folder_type}): {folder_id}")

        if 'folderToWatch' in params:
            folder_config = params['folderToWatch']
            if isinstance(folder_config, dict):
                folder_id = folder_config.get('value')
                if folder_id != EXPECTED['input_folder']:
                    problems.append(f"❌ {node_name}: Wrong trigger folder")
                    print(f"   ❌ Trigger Folder: {folder_id}")
                else:
                    print(f"   ✅ Trigger Folder: {folder_id}")

    # Check Google Sheets nodes
    if 'googleSheets' in node_type.lower():
        # Check spreadsheet ID
        if 'documentId' in params:
            doc_config = params['documentId']
            if isinstance(doc_config, dict):
                doc_id = doc_config.get('value')
            else:
                doc_id = doc_config

            if doc_id != EXPECTED['spreadsheet_id']:
                problems.append(f"❌ {node_name}: Wrong spreadsheet ID")
                print(f"   ❌ Spreadsheet: {doc_id}")
            else:
                print(f"   ✅ Spreadsheet: {doc_id}")

        # Check sheet ID
        if 'sheetName' in params:
            sheet_config = params['sheetName']
            if isinstance(sheet_config, dict):
                sheet_id = sheet_config.get('value')
                if sheet_id != EXPECTED['sheet_id']:
                    problems.append(f"❌ {node_name}: Wrong sheet ID")
                    print(f"   ❌ Sheet: {sheet_id} (expected: {EXPECTED['sheet_id']})")
                else:
                    print(f"   ✅ Sheet: {sheet_id}")

print()
print("=" * 80)
print("AUDIT SUMMARY")
print("=" * 80)
print()

if problems:
    print(f"❌ FOUND {len(problems)} PROBLEMS:")
    print()
    for problem in problems:
        print(f"  {problem}")

    print()
    print("=" * 80)
    print("FIXES NEEDED:")
    print("=" * 80)
    print()

    # Group fixes by type
    fixes_by_type = {}
    for fix in fixes_needed:
        issue_type = fix['issue'].split()[0]
        if issue_type not in fixes_by_type:
            fixes_by_type[issue_type] = []
        fixes_by_type[issue_type].append(fix)

    for issue_type, fixes in fixes_by_type.items():
        print(f"📋 {issue_type.upper()} FIXES:")
        for fix in fixes:
            print(f"   {fix['node']}: {fix['actual']} → {fix['expected']}")
        print()

    print("=" * 80)
    print("RUN: python3 fix_all_problems.py")
    print("=" * 80)
else:
    print("✅ NO PROBLEMS FOUND!")
    print()
    print("Workflow configuration is correct.")
    print()
    print("If workflow still fails, check:")
    print("  1. Google Sheet 'Photos' tab has headers in row 1")
    print("  2. Gemini API key has quota available")
    print("  3. Images are actually in INPUT folder")

print()
