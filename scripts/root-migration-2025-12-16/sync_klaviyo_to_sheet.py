#!/usr/bin/env python3
"""
SYNC KLAVIYO CONTEST LEADS TO GOOGLE SHEET
Sync contest/giveaway form submissions from Klaviyo → Google Sheet centralisé

Sources:
- Klaviyo List: "Pre-Launch Contest Participants"
- Klaviyo List: "Newsletter Subscribers" (general opt-ins)
- Klaviyo List: Custom lists (any list you specify)

Process:
1. Fetch profiles from Klaviyo list (created in last 24h)
2. Extract: email, name, phone, consent data
3. Append to Google Sheet "Raw Leads"
4. Tag source: "contest_prelaunch" or "klaviyo_optin"

Usage:
    # Contest leads (default)
    python3 sync_klaviyo_to_sheet.py

    # Specific list
    python3 sync_klaviyo_to_sheet.py --list-id "XYZ123"

    # All new profiles (last 24h)
    python3 sync_klaviyo_to_sheet.py --all-new

Requirements:
    pip install klaviyo-api gspread oauth2client python-dotenv

Setup:
    1. .env file with KLAVIYO_PRIVATE_API_KEY
    2. Google credentials: google_credentials.json
    3. Klaviyo list exists: "Pre-Launch Contest Participants"
"""

import os
import sys
import gspread
import argparse
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Configuration
KLAVIYO_PRIVATE_KEY = os.getenv('KLAVIYO_PRIVATE_API_KEY')
CREDENTIALS_FILE = Path(__file__).parent / "google_credentials.json"
if not CREDENTIALS_FILE.exists():
    CREDENTIALS_FILE = Path(__file__).parent / "market-analysis" / "google_credentials.json"

SHEET_NAME = "Alpha Medical - Lead Management"
WORKSHEET_NAME = "Raw Leads"

# Default list name for contest
DEFAULT_CONTEST_LIST = "Pre-Launch Contest Participants"

def fetch_klaviyo_profiles(list_name=None, hours_ago=24):
    """
    Fetch profiles from Klaviyo list created in last X hours

    NOTE: Klaviyo API v2024-10-15 uses different endpoint structure
    This uses klaviyo-api SDK (pip install klaviyo-api)
    """
    try:
        from klaviyo_api import KlaviyoAPI
    except ImportError:
        print(f"❌ ERROR: klaviyo-api not installed")
        print(f"   Run: pip install klaviyo-api")
        return []

    if not KLAVIYO_PRIVATE_KEY:
        print(f"❌ ERROR: KLAVIYO_PRIVATE_API_KEY not found in .env")
        return []

    print(f"🔐 Authenticating with Klaviyo...")
    try:
        client = KlaviyoAPI(KLAVIYO_PRIVATE_KEY)
        print(f"✅ Authenticated with Klaviyo API")
    except Exception as e:
        print(f"❌ ERROR authenticating: {e}")
        return []

    # Get list ID by name
    print(f"📋 Finding list: '{list_name or DEFAULT_CONTEST_LIST}'...")
    try:
        lists_response = client.Lists.get_lists()
        target_list = None

        for lst in lists_response['data']:
            if lst['attributes']['name'] == (list_name or DEFAULT_CONTEST_LIST):
                target_list = lst
                break

        if not target_list:
            print(f"❌ ERROR: List '{list_name or DEFAULT_CONTEST_LIST}' not found in Klaviyo")
            print(f"   Available lists:")
            for lst in lists_response['data'][:10]:
                print(f"   - {lst['attributes']['name']}")
            return []

        list_id = target_list['id']
        print(f"✅ Found list ID: {list_id}")
    except Exception as e:
        print(f"❌ ERROR fetching lists: {e}")
        return []

    # Fetch profiles from list (created in last X hours)
    print(f"👥 Fetching profiles created in last {hours_ago} hours...")
    try:
        cutoff_time = datetime.now() - timedelta(hours=hours_ago)

        # Get profiles in list
        profiles_response = client.Lists.get_list_profiles(list_id)
        all_profiles = profiles_response['data']

        # Filter by created date
        new_profiles = []
        for profile in all_profiles:
            created = profile['attributes'].get('created')
            if created:
                created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                if created_dt >= cutoff_time:
                    new_profiles.append(profile)

        print(f"✅ Found {len(new_profiles)} new profiles")
        return new_profiles

    except Exception as e:
        print(f"❌ ERROR fetching profiles: {e}")
        return []

def sync_to_sheets(profiles, source_tag="contest_prelaunch"):
    """Sync Klaviyo profiles to Google Sheet"""

    if len(profiles) == 0:
        print(f"ℹ️  No profiles to sync")
        return True

    # Authenticate with Google Sheets
    print(f"\n🔐 Authenticating with Google Sheets...")
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(str(CREDENTIALS_FILE), scope)
        client = gspread.authorize(creds)
        print(f"✅ Authenticated")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

    # Open sheet
    try:
        spreadsheet = client.open(SHEET_NAME)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        print(f"✅ Opened: {SHEET_NAME} → {WORKSHEET_NAME}")
    except Exception as e:
        print(f"❌ ERROR opening sheet: {e}")
        return False

    # Sync each profile
    print(f"\n📤 Syncing {len(profiles)} profiles to Google Sheet...")
    synced_count = 0

    for i, profile in enumerate(profiles, 1):
        try:
            attrs = profile['attributes']

            # Extract data
            email = attrs.get('email', '')
            first_name = attrs.get('first_name', '')
            last_name = attrs.get('last_name', '')
            name = f"{first_name} {last_name}".strip() if first_name or last_name else ''
            phone = attrs.get('phone_number', '')
            location = attrs.get('location', {}).get('city', '') if isinstance(attrs.get('location'), dict) else ''

            # Properties (custom fields)
            properties = profile.get('properties', {})

            # Prepare row (match Raw Leads structure)
            row = [
                datetime.now().isoformat(),  # A: Timestamp
                source_tag,                  # B: Platform (contest_prelaunch or klaviyo_optin)
                'opt-in',                    # C: Type
                name,                        # D: Name
                email,                       # E: Email
                phone,                       # F: Phone
                location,                    # G: Location
                '',                          # H: Engagement (N/A)
                '',                          # I: Rating (N/A)
                '',                          # J: Review Count (N/A)
                8.5,                         # K: Quality Score (HIGH - explicit opt-in)
                '',                          # L: Persona Match (will be filled by clean script)
                '',                          # M: Lead URL (N/A)
                'Klaviyo',                   # N: Source Original
                '',                          # O: File Name (N/A)
                properties,                  # P: Notes (custom properties as JSON)
                'FALSE'                      # Q: Processed
            ]

            # Append to sheet
            worksheet.append_row(row, value_input_option='USER_ENTERED')
            synced_count += 1
            print(f"   [{i}/{len(profiles)}] ✅ {name or email[:30]} (Phone: {bool(phone)})")

        except Exception as e:
            print(f"   [{i}/{len(profiles)}] ❌ Error: {e}")

    # Summary
    print("\n" + "="*80)
    print(f"SYNC COMPLETE")
    print("="*80)
    print(f"✅ Synced: {synced_count}/{len(profiles)} profiles")
    print(f"📋 Google Sheet: {SHEET_NAME} → {WORKSHEET_NAME}")
    print(f"🏷️  Source tag: {source_tag}")
    print(f"\n📊 Next: Run clean_and_segment_leads.py to process into Qualified Leads")

    return synced_count > 0

def main():
    parser = argparse.ArgumentParser(description='Sync Klaviyo contest leads to Google Sheet')
    parser.add_argument('--list-id', help='Specific Klaviyo list ID to sync')
    parser.add_argument('--list-name', default=DEFAULT_CONTEST_LIST, help='Klaviyo list name to sync')
    parser.add_argument('--hours', type=int, default=24, help='Fetch profiles created in last X hours (default: 24)')
    parser.add_argument('--source-tag', default='contest_prelaunch', help='Source tag for Google Sheet')
    parser.add_argument('--all-new', action='store_true', help='Fetch all new profiles (not from specific list)')

    args = parser.parse_args()

    print("="*80)
    print("SYNC KLAVIYO TO GOOGLE SHEET")
    print("="*80)
    print(f"List: {args.list_name}")
    print(f"Timeframe: Last {args.hours} hours")
    print(f"Source tag: {args.source_tag}")
    print("="*80)

    # Fetch profiles
    profiles = fetch_klaviyo_profiles(args.list_name, args.hours)

    if not profiles:
        print(f"\nℹ️  No new profiles found in last {args.hours} hours")
        sys.exit(0)

    # Sync to sheet
    success = sync_to_sheets(profiles, args.source_tag)

    if success:
        print(f"\n🎉 Sync successful!")
        sys.exit(0)
    else:
        print(f"\n⚠️  Sync failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
