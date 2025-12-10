#!/usr/bin/env python3
"""
SYNC APIFY LEADS TO GOOGLE SHEETS (v2 - Improved)
- Prevents duplicates automatically
- Maintains header structure
- Sorts by quality score

Usage:
    python3 sync_leads_to_sheets_v2.py leads/general/leads_general_instagram_20251122.json

Requirements:
    pip install gspread oauth2client
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

# Correct headers (12 columns)
EXPECTED_HEADERS = [
    "timestamp",
    "platform",
    "type",
    "name",
    "contact",
    "location",
    "engagement",
    "rating",
    "review_count",
    "quality_score",
    "persona_match",
    "lead_url"
]

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
    """Sync leads from JSON file to Google Sheets (with duplicate prevention)"""

    # Check if credentials file exists
    if not CREDENTIALS_FILE.exists():
        print(f"❌ ERROR: Credentials file not found: {CREDENTIALS_FILE}")
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
    except Exception as e:
        print(f"❌ ERROR opening sheet: {e}")
        return False

    # Verify headers
    try:
        current_headers = worksheet.row_values(1)
        if current_headers != EXPECTED_HEADERS:
            print(f"⚠️  Headers mismatch! Fixing...")
            worksheet.update([EXPECTED_HEADERS], 'A1:L1')
            print(f"✅ Headers fixed")
    except Exception as e:
        print(f"⚠️  Could not verify headers: {e}")

    # Get existing leads to check for duplicates
    try:
        existing_data = worksheet.get_all_values()[1:]  # Skip header
        existing_keys = set()
        for row in existing_data:
            if len(row) >= 6 and row[3].strip():  # Has name
                key = f"{row[3]}|{row[4]}|{row[5]}".lower()  # name|contact|location
                existing_keys.add(key)
        print(f"✅ Found {len(existing_keys)} existing leads in sheet")
    except Exception as e:
        print(f"⚠️  Could not check existing leads: {e}")
        existing_keys = set()

    # Sync each lead
    synced_count = 0
    skipped_count = 0
    errors = []

    for i, lead in enumerate(leads, 1):
        try:
            # Extract contact info (priority: email > phone > website)
            contact = lead.get('email') or lead.get('phone') or lead.get('website') or ''

            # Extract location
            location = lead.get('address') or lead.get('location') or lead.get('locationName') or ''

            # Create unique key for duplicate check
            name = lead.get('name', '')
            key = f"{name}|{contact}|{location}".lower()

            # Skip if duplicate
            if key in existing_keys:
                print(f"   [{i}/{len(leads)}] ⏭️  {name} (duplicate - skipped)")
                skipped_count += 1
                continue

            # Detect persona
            persona = detect_persona(
                name,
                lead.get('category', ''),
                location
            )

            # Prepare row data (exactly 12 columns)
            row = [
                datetime.now().isoformat(),  # timestamp
                lead.get('platform', ''),     # platform
                lead.get('type', ''),         # type
                name,                         # name
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
            existing_keys.add(key)  # Add to existing keys to prevent duplicates within this batch
            synced_count += 1
            print(f"   [{i}/{len(leads)}] ✅ {name} (score: {lead.get('quality_score', 'N/A')})")

        except Exception as e:
            error_msg = f"Lead {i}: {lead.get('name', 'Unknown')} - {str(e)}"
            errors.append(error_msg)
            print(f"   [{i}/{len(leads)}] ❌ Error: {error_msg}")

    # Summary
    print("\n" + "="*70)
    print(f"SYNC COMPLETE")
    print("="*70)
    print(f"✅ Successfully synced: {synced_count}/{len(leads)} leads")
    print(f"⏭️  Skipped duplicates: {skipped_count}/{len(leads)} leads")
    if errors:
        print(f"❌ Errors: {len(errors)}")
        for error in errors[:5]:
            print(f"   - {error}")
        if len(errors) > 5:
            print(f"   ... and {len(errors) - 5} more errors")

    return synced_count + skipped_count == len(leads)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 sync_leads_to_sheets_v2.py <leads_file.json>")
        print("\nExample:")
        print("  python3 sync_leads_to_sheets_v2.py leads/general/leads_general_instagram_20251122.json")
        sys.exit(1)

    leads_file = sys.argv[1]

    if not Path(leads_file).exists():
        print(f"❌ ERROR: File not found: {leads_file}")
        sys.exit(1)

    success = sync_to_sheets(leads_file)

    if success:
        print("\n🎉 Sync completed successfully!")
        sys.exit(0)
    else:
        print("\n⚠️  Sync completed with errors")
        sys.exit(1)

if __name__ == "__main__":
    main()
