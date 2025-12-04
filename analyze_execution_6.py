#!/usr/bin/env python3
"""
Analyze execution #6 in detail
"""

import requests
import json

N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 70)
print("EXECUTION #6 DETAILED ANALYSIS")
print("=" * 70)
print()

response = requests.get(f'{N8N_URL}/executions/6', headers=headers)

if response.status_code == 200:
    exec_data = response.json()

    print(f"Status: {exec_data['status']}")
    print(f"Mode: {exec_data['mode']}")
    print(f"Started: {exec_data['startedAt']}")
    print(f"Stopped: {exec_data.get('stoppedAt', 'N/A')}")
    print()

    if 'data' in exec_data and 'resultData' in exec_data['data']:
        result = exec_data['data']['resultData']

        print("📋 NODES EXECUTED:")
        print("-" * 70)

        if 'runData' in result:
            for node_name, node_runs in result['runData'].items():
                print(f"\n🔹 {node_name}:")

                for i, run in enumerate(node_runs, 1):
                    print(f"   Run #{i}:")

                    # Check for data
                    if 'data' in run:
                        main_data = run['data'].get('main', [])
                        if main_data:
                            for j, data_array in enumerate(main_data):
                                print(f"      Output {j}: {len(data_array)} items")
                                if len(data_array) > 0:
                                    # Show first item keys
                                    if 'json' in data_array[0]:
                                        keys = list(data_array[0]['json'].keys())[:5]
                                        print(f"         Sample keys: {keys}")
                        else:
                            print(f"      ⚠️ NO OUTPUT DATA")

                    # Check for error
                    if 'error' in run:
                        print(f"      ❌ ERROR: {run['error'].get('message', 'Unknown')}")

        print()
        print("=" * 70)
        print()

        # Summary
        if 'runData' in result and len(result['runData']) == 0:
            print("❌ PROBLEM: Workflow executed but NO NODES RAN!")
            print()
            print("This means:")
            print("  - Mode was 'manual' but workflow is trigger-based")
            print("  - Manual execution of trigger workflows doesn't work like this")
            print()
            print("SOLUTION:")
            print("  Upload a NEW image NOW and wait 5 minutes")
            print("  The automatic trigger will detect it")
        elif 'runData' in result and 'File Created' in result['runData']:
            file_created_data = result['runData']['File Created'][0].get('data', {})
            main = file_created_data.get('main', [[]])[0]
            if len(main) == 0:
                print("❌ PROBLEM: 'File Created' node ran but found NO FILES")
                print()
                print("Possible causes:")
                print("  1. Image was uploaded BEFORE workflow was fixed")
                print("  2. Trigger only detects NEW files after activation")
                print()
                print("SOLUTION:")
                print("  Upload a BRAND NEW image to INPUT folder NOW")
                print("  Wait 5 minutes for automatic detection")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)

print()
print("=" * 70)
