#!/usr/bin/env python3
"""
Check which Google APIs are enabled and accessible
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

CREDENTIALS_FILE = '/Users/mac/Desktop/Alpha-Medical/google_credentials.json'

print("=" * 70)
print("CHECKING GOOGLE API STATUS")
print("=" * 70)

# Load credentials to get project info
with open(CREDENTIALS_FILE, 'r') as f:
    creds_data = json.load(f)
    project_id = creds_data['project_id']
    service_email = creds_data['client_email']

print(f"\nService Account: {service_email}")
print(f"Project ID: {project_id}")

# Test authentication
print("\n[1/3] Testing Google Sheets API authentication...")
try:
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE, scope
    )
    client = gspread.authorize(creds)
    print("✅ Google Sheets API: Accessible")
except Exception as e:
    print(f"❌ Google Sheets API: Failed - {e}")

# Test Drive API access
print("\n[2/3] Testing Google Drive API access...")
try:
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE, scope
    )
    client = gspread.authorize(creds)

    # Try to list spreadsheets (requires Drive API)
    spreadsheets = client.openall()
    print(f"✅ Google Drive API: Accessible")
    print(f"   Found {len(spreadsheets)} existing spreadsheets")

    if spreadsheets:
        print("\n   Existing spreadsheets:")
        for sheet in spreadsheets[:5]:
            print(f"     - {sheet.title} ({sheet.id})")
except Exception as e:
    error_str = str(e)
    if "403" in error_str and "drive.googleapis.com" in error_str:
        print("❌ Google Drive API: Not enabled on project")
        print(f"   Error: {error_str[:200]}")
        print(f"\n   Enable at: https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project={project_id}")
    else:
        print(f"❌ Google Drive API: Failed - {error_str[:200]}")

# Test creating a spreadsheet
print("\n[3/3] Testing spreadsheet creation...")
try:
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE, scope
    )
    client = gspread.authorize(creds)

    # Try to create a test spreadsheet
    test_sheet = client.create('API_TEST_DELETE_ME')
    print(f"✅ Spreadsheet creation: Working")
    print(f"   Test sheet created: {test_sheet.url}")
    print(f"   You can delete this test sheet manually")

    # Clean up
    try:
        client.del_spreadsheet(test_sheet.id)
        print(f"   ✅ Test sheet deleted automatically")
    except:
        print(f"   ⚠️  Could not auto-delete test sheet")
except Exception as e:
    error_str = str(e)
    print(f"❌ Spreadsheet creation: Failed")
    print(f"   Error: {error_str[:200]}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print("\nIf Google Drive API is not enabled, please:")
print("1. Open the URL shown above")
print("2. Click 'ENABLE' button")
print("3. Wait 1-2 minutes for propagation")
print("4. Run setup_google_sheet.py again")
