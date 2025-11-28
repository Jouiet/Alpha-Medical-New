#!/usr/bin/env python3
"""
SYNC SHOPIFY FORMS TO GOOGLE SHEET
Sync contest/giveaway form submissions from Shopify Forms → Google Sheet centralisé

Sources:
- Shopify Forms app native submissions
- Via Shopify Admin API

Process:
1. Fetch form submissions from Shopify Forms (last N hours)
2. Extract: email, name, phone, consent data
3. Append to Google Sheet "Raw Leads"
4. Tag source: "contest_shopify_forms"

Usage:
    python3 sync_shopify_forms_to_sheet.py --hours 1

Requirements:
    pip install requests gspread oauth2client python-dotenv

Author: Claude Code
Date: 2025-11-28
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
import ssl
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN', 'azffej-as.myshopify.com')
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'Alpha Medical - Lead Management')
CREDENTIALS_FILE = Path(__file__).parent / "google_credentials.json"
RAW_LEADS_TAB = "Raw Leads"

# Quality score for contest leads (high - explicit opt-in)
QUALITY_SCORE = 8.5

# SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_google_sheet():
    """Connect to Google Sheet and return worksheet"""
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            str(CREDENTIALS_FILE), scope
        )
        client = gspread.authorize(creds)
        sheet = client.open(GOOGLE_SHEET_NAME)
        worksheet = sheet.worksheet(RAW_LEADS_TAB)
        return worksheet
    except Exception as e:
        print(f"❌ ERROR: Failed to connect to Google Sheet: {e}")
        sys.exit(1)


def fetch_shopify_forms_submissions(hours_ago=24):
    """
    Fetch Shopify Forms submissions via Admin API

    NOTE: Shopify Forms submissions are stored as customer metafields
    or in a specific submissions endpoint (depends on API version)

    Args:
        hours_ago: Fetch submissions from last N hours

    Returns:
        List of submission dictionaries
    """
    print(f"🔍 Fetching Shopify Forms submissions from last {hours_ago} hours...")

    if not SHOPIFY_TOKEN:
        print(f"❌ ERROR: SHOPIFY_ADMIN_ACCESS_TOKEN not set")
        return []

    # Calculate since timestamp
    since = (datetime.utcnow() - timedelta(hours=hours_ago)).isoformat() + "Z"

    # Shopify Forms submissions can be accessed via:
    # 1. Customer metafields (if form creates customer)
    # 2. Marketing events API
    # 3. Custom app endpoints

    # For now, we'll check for customers created in timeframe with form-related metafields
    url = f'https://{SHOPIFY_DOMAIN}/admin/api/2024-10/customers.json'
    url += f'?created_at_min={since}&limit=250'

    headers = {
        'X-Shopify-Access-Token': SHOPIFY_TOKEN,
        'Content-Type': 'application/json'
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read())
            customers = data.get('customers', [])

            print(f"   Found {len(customers)} new customers in timeframe")

            # Filter for form submissions
            # Shopify Forms tags customers with form source
            form_submissions = []
            for customer in customers:
                tags = customer.get('tags', '').lower()

                # Check if customer came from a form
                if 'form' in tags or 'contest' in tags or 'giveaway' in tags:
                    submission = {
                        'email': customer.get('email'),
                        'first_name': customer.get('first_name', ''),
                        'last_name': customer.get('last_name', ''),
                        'phone': customer.get('phone', ''),
                        'created_at': customer.get('created_at'),
                        'tags': customer.get('tags'),
                        'accepts_marketing': customer.get('accepts_marketing', False)
                    }
                    form_submissions.append(submission)

            print(f"   ✅ Found {len(form_submissions)} form submissions")
            return form_submissions

    except Exception as e:
        print(f"❌ ERROR fetching Shopify Forms submissions: {e}")
        return []


def append_to_sheet(worksheet, submissions, source_tag):
    """Append submissions to Google Sheet"""

    if not submissions:
        print("ℹ️  No new submissions to sync")
        return 0

    print(f"📝 Appending {len(submissions)} submissions to Google Sheet...")

    # Get current timestamp
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

    synced_count = 0
    for submission in submissions:
        # Prepare row data
        row = [
            submission.get('email', ''),
            submission.get('first_name', '') + ' ' + submission.get('last_name', '').strip(),
            submission.get('phone', ''),
            source_tag,
            QUALITY_SCORE,
            submission.get('created_at', now),
            now,  # synced_at
            'Yes' if submission.get('accepts_marketing') else 'No',
            submission.get('tags', '')
        ]

        try:
            worksheet.append_row(row)
            synced_count += 1
            print(f"   ✅ Synced: {submission.get('email')}")
        except Exception as e:
            print(f"   ❌ Failed to sync {submission.get('email')}: {e}")

    print(f"\n📊 Sync complete: {synced_count}/{len(submissions)} submissions synced")
    return synced_count


def main():
    parser = argparse.ArgumentParser(description='Sync Shopify Forms submissions to Google Sheet')
    parser.add_argument('--hours', type=int, default=1, help='Fetch submissions from last N hours')
    parser.add_argument('--source-tag', type=str, default='contest_shopify_forms', help='Source tag for submissions')
    args = parser.parse_args()

    print("🔄 SHOPIFY FORMS → GOOGLE SHEET SYNC")
    print("=" * 60)
    print(f"Store: {SHOPIFY_DOMAIN}")
    print(f"Sheet: {GOOGLE_SHEET_NAME}")
    print(f"Timeframe: Last {args.hours} hour(s)")
    print("")

    # Validate environment
    if not SHOPIFY_TOKEN:
        print("❌ ERROR: SHOPIFY_ADMIN_ACCESS_TOKEN not set")
        sys.exit(1)

    if not CREDENTIALS_FILE.exists():
        print(f"❌ ERROR: Google credentials file not found: {CREDENTIALS_FILE}")
        sys.exit(1)

    # Connect to Google Sheet
    worksheet = get_google_sheet()
    print(f"✅ Connected to Google Sheet: {GOOGLE_SHEET_NAME}")
    print("")

    # Fetch Shopify Forms submissions
    submissions = fetch_shopify_forms_submissions(args.hours)

    # Append to sheet
    if submissions:
        synced = append_to_sheet(worksheet, submissions, args.source_tag)

        print("")
        print("=" * 60)
        print(f"✅ SUCCESS: {synced} form submissions synced")
        sys.exit(0)
    else:
        print("")
        print("=" * 60)
        print("ℹ️  No new form submissions to sync")
        sys.exit(0)


if __name__ == '__main__':
    main()
