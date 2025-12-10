#!/usr/bin/env python3
"""
SYNC APIFY LEADS TO GOOGLE SHEETS
No external apps - Pure Python + Google Sheets API

Usage:
    python3 sync_leads_to_sheets.py leads/general/leads_general_instagram_20251122.json

Requirements:
    pip install gspread oauth2client

Setup:
    1. Create Google Cloud Project
    2. Enable Google Sheets API
    3. Create Service Account
    4. Download credentials.json → rename to google_credentials.json
    5. Share Google Sheet with service account email
"""

import json
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path

# Configuration
CREDENTIALS_FILE = Path(__file__).parent / "google_credentials.json"
SHEET_NAME = "Alpha Medical - Lead Management"
WORKSHEET_NAME = "Raw Leads"

def detect_persona(name, category, address):
    """Detect persona based on lead data"""
    text = f"{name} {category} {address}".lower()

    if any(kw in text for kw in ['senior', 'elderly', 'aged', 'retirement', 'arthritis']):
        return 'seniors'
    elif any(kw in text for kw in ['athlete', 'fitness', 'gym', 'sport', 'runner']):
        return 'athletes'
    elif any(kw in text for kw in ['parent', 'baby', 'child', 'daycare', 'preschool']):
        return 'parents'
    elif any(kw in text for kw in ['office', 'desk', 'work', 'corporate', 'business']):
        return 'workers'
    elif any(kw in text for kw in ['travel', 'flight', 'hotel', 'tourism', 'vacation']):
        return 'travelers'
    else:
        return 'unknown'

def sync_to_sheets(leads_file):
    """Sync leads from JSON file to Google Sheets"""

    # Check if credentials file exists
    if not CREDENTIALS_FILE.exists():
        print(f"❌ ERROR: Credentials file not found: {CREDENTIALS_FILE}")
        print(f"   Please create a service account and download credentials to:")
        print(f"   {CREDENTIALS_FILE}")
        return False

    # Load leads from JSON
    try:
        with open(leads_file, 'r', encoding='utf-8') as f:
            leads = json.load(f)
        print(f"✅ Loaded {len(leads)} leads from {leads_file}")
    except Exception as e:
        print(f"❌ ERROR loading JSON: {e}")
        return False

    # Authenticate with Google Sheets
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(str(CREDENTIALS_FILE), scope)
        client = gspread.authorize(creds)
        print(f"✅ Authenticated with Google Sheets API")
    except Exception as e:
        print(f"❌ ERROR authenticating: {e}")
        return False

    # Open the sheet
    try:
        spreadsheet = client.open(SHEET_NAME)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        print(f"✅ Opened sheet: {SHEET_NAME} → {WORKSHEET_NAME}")
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ ERROR: Spreadsheet '{SHEET_NAME}' not found")
        print(f"   Please create the sheet and share it with the service account email")
        return False
    except gspread.exceptions.WorksheetNotFound:
        print(f"❌ ERROR: Worksheet '{WORKSHEET_NAME}' not found")
        print(f"   Please create a worksheet named '{WORKSHEET_NAME}'")
        return False
    except Exception as e:
        print(f"❌ ERROR opening sheet: {e}")
        return False

    # Sync each lead
    synced_count = 0
    errors = []

    for i, lead in enumerate(leads, 1):
        try:
            # Extract contact info (priority: email > phone > website)
            contact = lead.get('email') or lead.get('phone') or lead.get('website') or ''

            # Extract location
            location = lead.get('address') or lead.get('location') or lead.get('locationName') or ''

            # Detect persona
            persona = detect_persona(
                lead.get('name', ''),
                lead.get('category', ''),
                location
            )

            # Prepare row data
            row = [
                datetime.now().isoformat(),  # timestamp
                lead.get('platform', ''),     # platform
                lead.get('type', ''),         # type
                lead.get('name', ''),         # name
                contact,                      # contact
                location,                     # location
                lead.get('engagement', ''),   # engagement (Instagram)
                lead.get('rating', ''),       # rating (Google Maps)
                lead.get('review_count', ''), # review_count (Google Maps)
                lead.get('quality_score', ''),# quality_score
                persona,                      # persona_match
                lead.get('url', '') or lead.get('website', '')  # lead_url
            ]

            # Append to sheet
            worksheet.append_row(row, value_input_option='USER_ENTERED')
            synced_count += 1
            print(f"   [{i}/{len(leads)}] ✅ {lead.get('name', 'Unknown')} (score: {lead.get('quality_score', 'N/A')})")

        except Exception as e:
            error_msg = f"Lead {i}: {lead.get('name', 'Unknown')} - {str(e)}"
            errors.append(error_msg)
            print(f"   [{i}/{len(leads)}] ❌ Error: {error_msg}")

    # Summary
    print("\n" + "="*70)
    print(f"SYNC COMPLETE")
    print("="*70)
    print(f"✅ Successfully synced: {synced_count}/{len(leads)} leads")
    if errors:
        print(f"❌ Errors: {len(errors)}")
        for error in errors[:5]:  # Show first 5 errors
            print(f"   - {error}")
        if len(errors) > 5:
            print(f"   ... and {len(errors) - 5} more errors")

    return synced_count == len(leads)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 sync_leads_to_sheets.py <leads_file.json>")
        print("\nExample:")
        print("  python3 sync_leads_to_sheets.py leads/general/leads_general_instagram_20251122.json")
        sys.exit(1)

    leads_file = sys.argv[1]

    if not Path(leads_file).exists():
        print(f"❌ ERROR: File not found: {leads_file}")
        sys.exit(1)

    success = sync_to_sheets(leads_file)

    if success:
        print("\n🎉 All leads synced successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Sync completed with errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
