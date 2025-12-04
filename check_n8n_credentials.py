#!/usr/bin/env python3
"""Check N8N credentials to diagnose workflow activation issue"""

import requests
import json

# Configuration
N8N_URL = "https://n8n.srv1168256.hstgr.cloud"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo"

def list_credentials():
    """List all credentials in N8N instance"""
    url = f"{N8N_URL}/api/v1/credentials"
    headers = {
        "X-N8N-API-KEY": API_KEY,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ API Error: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return

        data = response.json()

        print("=" * 70)
        print("N8N CREDENTIALS INVENTORY")
        print("=" * 70)

        if 'data' not in data:
            print("⚠️  No credentials data in response")
            print(json.dumps(data, indent=2))
            return

        credentials = data['data']

        if not credentials:
            print("❌ NO CREDENTIALS FOUND")
            print()
            print("This explains the activation error!")
            print()
            print("REQUIRED ACTIONS:")
            print("1. Create Google Drive OAuth2 credential in N8N UI")
            print("2. Create Google Sheets OAuth2 credential in N8N UI")
            print("3. Create Google Gemini (PaLM) API credential in N8N UI")
            print()
            print("Then update workflow nodes with new credential IDs")
            return

        print(f"Total Credentials: {len(credentials)}")
        print()

        # Group by type
        google_drive = []
        google_sheets = []
        google_gemini = []
        other = []

        for cred in credentials:
            cred_type = cred.get('type', '')
            if 'drive' in cred_type.lower():
                google_drive.append(cred)
            elif 'sheet' in cred_type.lower():
                google_sheets.append(cred)
            elif 'gemini' in cred_type.lower() or 'palm' in cred_type.lower():
                google_gemini.append(cred)
            else:
                other.append(cred)

        # Display Google Drive credentials
        print("=" * 70)
        print("GOOGLE DRIVE CREDENTIALS")
        print("=" * 70)
        if google_drive:
            for cred in google_drive:
                print(f"✅ ID: {cred.get('id')}")
                print(f"   Name: {cred.get('name')}")
                print(f"   Type: {cred.get('type')}")
                print()
        else:
            print("❌ NO GOOGLE DRIVE CREDENTIALS")
            print()

        # Display Google Sheets credentials
        print("=" * 70)
        print("GOOGLE SHEETS CREDENTIALS")
        print("=" * 70)
        if google_sheets:
            for cred in google_sheets:
                print(f"✅ ID: {cred.get('id')}")
                print(f"   Name: {cred.get('name')}")
                print(f"   Type: {cred.get('type')}")
                print()
        else:
            print("❌ NO GOOGLE SHEETS CREDENTIALS")
            print()

        # Display Google Gemini credentials
        print("=" * 70)
        print("GOOGLE GEMINI (PALM) CREDENTIALS")
        print("=" * 70)
        if google_gemini:
            for cred in google_gemini:
                print(f"✅ ID: {cred.get('id')}")
                print(f"   Name: {cred.get('name')}")
                print(f"   Type: {cred.get('type')}")
                print()
        else:
            print("❌ NO GOOGLE GEMINI CREDENTIALS")
            print()

        # Display other credentials
        if other:
            print("=" * 70)
            print("OTHER CREDENTIALS")
            print("=" * 70)
            for cred in other:
                print(f"ID: {cred.get('id')}")
                print(f"   Name: {cred.get('name')}")
                print(f"   Type: {cred.get('type')}")
                print()

        # Analysis
        print("=" * 70)
        print("DIAGNOSIS")
        print("=" * 70)

        expected_ids = {
            'Google Drive': 'htidcOV6hR8kh9tB',
            'Google Sheets': 'HTAGRgrsWTF0cfU2',
            'Google Gemini': '7tlny7NnnrQIfupF'
        }

        print("Expected Credential IDs (from workflow JSON):")
        for name, cred_id in expected_ids.items():
            exists = any(c['id'] == cred_id for c in credentials)
            status = "✅ EXISTS" if exists else "❌ MISSING"
            print(f"  {status} {name}: {cred_id}")

        print()
        print("=" * 70)

        # Check if credentials exist with different IDs
        if google_drive and not any(c['id'] == expected_ids['Google Drive'] for c in credentials):
            print("⚠️  Google Drive credentials exist but with DIFFERENT IDs")
            print("   Workflow needs updating with correct credential IDs")

        if google_sheets and not any(c['id'] == expected_ids['Google Sheets'] for c in credentials):
            print("⚠️  Google Sheets credentials exist but with DIFFERENT IDs")
            print("   Workflow needs updating with correct credential IDs")

        if google_gemini and not any(c['id'] == expected_ids['Google Gemini'] for c in credentials):
            print("⚠️  Google Gemini credentials exist but with DIFFERENT IDs")
            print("   Workflow needs updating with correct credential IDs")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_credentials()
