#!/usr/bin/env python3
"""
Check N8N workflow execution status and results
"""

import requests
import time
from datetime import datetime

# N8N API config
N8N_URL = 'https://n8n.srv1168256.hstgr.cloud/api/v1'
N8N_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo'
WORKFLOW_ID = 'q0kyXyhCUq5gjmG2'

headers = {'X-N8N-API-KEY': N8N_API_KEY}

print("=" * 70)
print("N8N WORKFLOW EXECUTION MONITOR")
print("=" * 70)
print()
print(f"⏰ Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Check workflow status
print("📋 Checking workflow status...")
response = requests.get(f'{N8N_URL}/workflows/{WORKFLOW_ID}', headers=headers)

if response.status_code == 200:
    workflow = response.json()
    print(f"✅ Workflow: {workflow['name']}")
    print(f"   Status: {'🟢 ACTIVE' if workflow['active'] else '🔴 INACTIVE'}")
    print()
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
    exit(1)

# Check executions
print("📋 Checking recent executions...")
print("-" * 70)

response = requests.get(
    f'{N8N_URL}/executions',
    params={'workflowId': WORKFLOW_ID, 'limit': 5},
    headers=headers
)

if response.status_code == 200:
    executions = response.json()['data']

    if not executions:
        print("⚠️ No executions yet")
        print()
        print("💡 This means:")
        print("   - Workflow hasn't checked the folder yet (checks every 5 min)")
        print("   - OR file was uploaded after last check")
        print()
        print("⏰ Wait time remaining:")
        print("   - Max: 5 minutes until next trigger")
        print("   - Processing: ~1 minute after trigger")
        print()
        print("🔄 Run this script again in 2-3 minutes")
    else:
        print(f"✅ Found {len(executions)} recent executions:\n")

        for i, exec_data in enumerate(executions, 1):
            status = exec_data.get('status', 'unknown')
            start_time = exec_data.get('startedAt', 'N/A')
            stop_time = exec_data.get('stoppedAt', 'N/A')

            status_icon = {
                'success': '✅',
                'running': '🔄',
                'error': '❌',
                'waiting': '⏸️'
            }.get(status, '❓')

            print(f"{status_icon} Execution #{i}:")
            print(f"   ID: {exec_data.get('id')}")
            print(f"   Status: {status.upper()}")
            print(f"   Started: {start_time}")

            if stop_time != 'N/A':
                print(f"   Stopped: {stop_time}")

            # Get execution details if completed
            if status == 'success':
                exec_id = exec_data.get('id')
                detail_response = requests.get(
                    f'{N8N_URL}/executions/{exec_id}',
                    headers=headers
                )

                if detail_response.status_code == 200:
                    details = detail_response.json()
                    print(f"   Mode: {details.get('mode', 'N/A')}")

                    # Try to find output data
                    if 'data' in details and 'resultData' in details['data']:
                        runs = details['data']['resultData'].get('runData', {})
                        print(f"   Nodes executed: {len(runs)}")

            print()

        # Check for latest successful execution
        latest_success = next((e for e in executions if e.get('status') == 'success'), None)

        if latest_success:
            print("✅ LATEST SUCCESSFUL EXECUTION:")
            print(f"   Time: {latest_success.get('startedAt')}")
            print()
            print("📸 Next steps:")
            print("   1. Check output folder:")
            print("      https://drive.google.com/drive/folders/1O1PrZoTDweXQx8ImVLXlJArei9hdvizn")
            print("   2. Look for: [filename]_clean.jpg")
            print("   3. Verify Google Sheet:")
            print("      https://docs.google.com/spreadsheets/d/1Q5ujL0LQEz-kgGkg-oMzCutcpUnznpDPpRkqh1hUBUw/edit")
        else:
            print("⏳ No successful executions yet")
            print("   Either workflow hasn't run or processing failed")
else:
    print(f"❌ Error getting executions: {response.status_code}")
    print(response.text)

print()
print("=" * 70)
print("💡 TIP: Run this script periodically to monitor progress")
print("   Command: python3 check_workflow_execution.py")
print("=" * 70)
