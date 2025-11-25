#!/usr/bin/env python3
"""
SYNC FACEBOOK LEAD ADS TO GOOGLE SHEET
Fetch leads from Facebook Lead Ads forms → Google Sheet centralisé

Process:
1. Connect to Facebook Marketing API
2. Fetch leads from specified form(s) (created in last 24h)
3. Extract: name, email, phone, custom questions
4. Append to Google Sheet "Raw Leads"
5. Tag source: "facebook_lead_ads"

Usage:
    # Sync specific form
    python3 sync_facebook_leads_to_sheet.py --form-id 123456789

    # Sync all forms from ad account
    python3 sync_facebook_leads_to_sheet.py --all-forms

Requirements:
    pip install facebook-business gspread oauth2client python-dotenv

Setup:
    1. Facebook Developer App: https://developers.facebook.com/apps/
    2. Ad Account access token (with leads_retrieval permission)
    3. .env file with:
       - FACEBOOK_ACCESS_TOKEN=<your_token>
       - FACEBOOK_AD_ACCOUNT_ID=act_<your_account_id>
    4. Google credentials: google_credentials.json
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
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_AD_ACCOUNT_ID = os.getenv('FACEBOOK_AD_ACCOUNT_ID')

CREDENTIALS_FILE = Path(__file__).parent / "google_credentials.json"
if not CREDENTIALS_FILE.exists():
    CREDENTIALS_FILE = Path(__file__).parent / "market-analysis" / "google_credentials.json"

SHEET_NAME = "Alpha Medical - Lead Management"
WORKSHEET_NAME = "Raw Leads"

def fetch_facebook_leads(form_id=None, hours_ago=24):
    """Fetch leads from Facebook Lead Ads form"""

    try:
        from facebook_business.api import FacebookAdsApi
        from facebook_business.adobjects.leadgenform import LeadgenForm
        from facebook_business.adobjects.lead import Lead
    except ImportError:
        print(f"❌ ERROR: facebook-business SDK not installed")
        print(f"   Run: pip install facebook-business")
        return []

    # Check credentials
    if not FACEBOOK_ACCESS_TOKEN:
        print(f"❌ ERROR: FACEBOOK_ACCESS_TOKEN not found in .env")
        print(f"   Get token: https://developers.facebook.com/tools/explorer/")
        print(f"   Required permissions: ads_read, leads_retrieval")
        return []

    # Initialize API
    print(f"🔐 Authenticating with Facebook Marketing API...")
    try:
        FacebookAdsApi.init(access_token=FACEBOOK_ACCESS_TOKEN)
        print(f"✅ Authenticated")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return []

    # Get form
    if not form_id:
        print(f"❌ ERROR: No form ID specified")
        print(f"   Usage: python3 sync_facebook_leads_to_sheet.py --form-id YOUR_FORM_ID")
        print(f"\n   To find form ID:")
        print(f"   1. Facebook Ads Manager → Forms Library")
        print(f"   2. Click on form → URL contains form ID")
        return []

    print(f"📋 Fetching leads from form: {form_id}...")

    try:
        form = LeadgenForm(form_id)

        # Calculate time filter (last X hours)
        cutoff_timestamp = int((datetime.now() - timedelta(hours=hours_ago)).timestamp())

        # Fetch leads
        leads = form.get_leads(
            fields=[
                Lead.Field.id,
                Lead.Field.created_time,
                Lead.Field.field_data,
            ],
            params={
                'filtering': [{'field': 'time_created', 'operator': 'GREATER_THAN', 'value': cutoff_timestamp}]
            }
        )

        print(f"✅ Found {len(leads)} new leads (last {hours_ago}h)")
        return leads

    except Exception as e:
        print(f"❌ ERROR fetching leads: {e}")
        return []

def parse_lead_data(lead):
    """Parse Facebook lead data into structured format"""

    lead_data = {
        'fb_lead_id': lead.get('id', ''),
        'created_time': lead.get('created_time', ''),
        'name': '',
        'email': '',
        'phone': '',
        'location': '',
        'custom_fields': {}
    }

    # Parse field_data (form responses)
    field_data = lead.get('field_data', [])

    for field in field_data:
        field_name = field.get('name', '').lower()
        field_values = field.get('values', [])
        field_value = field_values[0] if field_values else ''

        # Map standard fields
        if field_name in ['email', 'e-mail']:
            lead_data['email'] = field_value
        elif field_name in ['full_name', 'name']:
            lead_data['name'] = field_value
        elif field_name in ['phone_number', 'phone', 'mobile']:
            lead_data['phone'] = field_value
        elif field_name in ['first_name']:
            lead_data['name'] = field_value + ' ' + lead_data['name']
        elif field_name in ['last_name']:
            lead_data['name'] = lead_data['name'] + ' ' + field_value
        elif field_name in ['city', 'state', 'zip_code', 'location']:
            lead_data['location'] += ' ' + field_value
        else:
            # Custom field
            lead_data['custom_fields'][field_name] = field_value

    # Clean name
    lead_data['name'] = lead_data['name'].strip()
    lead_data['location'] = lead_data['location'].strip()

    return lead_data

def sync_to_sheets(leads, source_tag="facebook_lead_ads"):
    """Sync Facebook leads to Google Sheet"""

    if len(leads) == 0:
        print(f"ℹ️  No leads to sync")
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
        print(f"❌ ERROR: {e}")
        return False

    # Sync each lead
    print(f"\n📤 Syncing {len(leads)} leads to Google Sheet...")
    synced_count = 0

    for i, lead in enumerate(leads, 1):
        try:
            # Parse lead data
            data = parse_lead_data(lead)

            # Validate email
            if not data['email']:
                print(f"   [{i}] ⚠️  Skipped: No email")
                continue

            # Prepare row (match Raw Leads structure)
            row = [
                datetime.now().isoformat(),  # A: Timestamp
                source_tag,                  # B: Platform (facebook_lead_ads)
                'opt-in',                    # C: Type
                data['name'],                # D: Name
                data['email'],               # E: Email
                data['phone'],               # F: Phone
                data['location'],            # G: Location
                '',                          # H: Engagement (N/A)
                '',                          # I: Rating (N/A)
                '',                          # J: Review Count (N/A)
                9.0,                         # K: Quality Score (VERY HIGH - paid ads + opt-in)
                '',                          # L: Persona Match (filled by clean script)
                '',                          # M: Lead URL (N/A)
                f"Facebook Lead Ad #{data['fb_lead_id']}",  # N: Source Original
                '',                          # O: File Name (N/A)
                str(data['custom_fields']),  # P: Notes (custom fields as string)
                'FALSE'                      # Q: Processed
            ]

            # Append to sheet
            worksheet.append_row(row, value_input_option='USER_ENTERED')
            synced_count += 1
            print(f"   [{i}/{len(leads)}] ✅ {data['name'] or data['email'][:30]}")

        except Exception as e:
            print(f"   [{i}/{len(leads)}] ❌ Error: {e}")

    # Summary
    print("\n" + "="*80)
    print(f"SYNC COMPLETE")
    print("="*80)
    print(f"✅ Synced: {synced_count}/{len(leads)} leads")
    print(f"📋 Google Sheet: {SHEET_NAME} → {WORKSHEET_NAME}")
    print(f"🏷️  Source tag: {source_tag}")
    print(f"\n📊 Next: Run clean_and_segment_leads.py to process into Qualified Leads")

    return synced_count > 0

def main():
    parser = argparse.ArgumentParser(description='Sync Facebook Lead Ads to Google Sheet')
    parser.add_argument('--form-id', required=True, help='Facebook Lead Form ID (REQUIRED)')
    parser.add_argument('--hours', type=int, default=24, help='Fetch leads from last X hours (default: 24)')
    parser.add_argument('--source-tag', default='facebook_lead_ads', help='Source tag for Google Sheet')

    args = parser.parse_args()

    print("="*80)
    print("SYNC FACEBOOK LEAD ADS TO GOOGLE SHEET")
    print("="*80)
    print(f"Form ID: {args.form_id}")
    print(f"Timeframe: Last {args.hours} hours")
    print(f"Source tag: {args.source_tag}")
    print("="*80)

    # Fetch leads
    leads = fetch_facebook_leads(args.form_id, args.hours)

    if not leads:
        print(f"\nℹ️  No new leads found in last {args.hours} hours")
        sys.exit(0)

    # Sync to sheet
    success = sync_to_sheets(leads, args.source_tag)

    if success:
        print(f"\n🎉 Sync successful!")
        sys.exit(0)
    else:
        print(f"\n⚠️  Sync failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
