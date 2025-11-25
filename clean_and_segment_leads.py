#!/usr/bin/env python3
"""
CLEAN AND SEGMENT LEADS - GOOGLE SHEET AUTOMATION
Nettoyage + Segmentation automatique des leads de TOUTES les sources

Sources traitées:
- Apify scraping (Instagram, Facebook, TikTok, Google Maps)
- Contest/Giveaway pre-launch
- Facebook Lead Ads
- Import fichiers externes (xlsx/csv)

Process:
1. Read "Raw Leads" sheet (all unprocessed leads)
2. Clean data (duplicates, validation, standardization)
3. Score leads (1-10 quality score)
4. Detect persona (seniors, athletes, workers, parents, travelers)
5. Write to "Qualified Leads" sheet
6. Mark as processed in "Raw Leads"

Usage:
    python3 clean_and_segment_leads.py

Requirements:
    pip install gspread oauth2client

Setup:
    1. Google Sheet: "Alpha Medical - Lead Management" exists
    2. Worksheets: "Raw Leads" and "Qualified Leads" exist
    3. Service account credentials: google_credentials.json
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pathlib import Path
import re

# Configuration
CREDENTIALS_FILE = Path(__file__).parent / "google_credentials.json"
if not CREDENTIALS_FILE.exists():
    CREDENTIALS_FILE = Path(__file__).parent / "market-analysis" / "google_credentials.json"

SHEET_NAME = "Alpha Medical - Lead Management"
RAW_LEADS_SHEET = "Raw Leads"
QUALIFIED_LEADS_SHEET = "Qualified Leads"

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, str(email).strip()))

def validate_phone(phone):
    """Validate US phone format"""
    if not phone:
        return False
    # US phone should have 10-11 digits
    digits = re.sub(r'\D', '', str(phone))
    return len(digits) in [10, 11]

def detect_persona(name, location, notes, source):
    """Detect persona based on lead data"""
    text = f"{name} {location} {notes} {source}".lower()

    # Scoring weights for each persona
    persona_scores = {
        'seniors': 0,
        'athletes': 0,
        'workers': 0,
        'parents': 0,
        'travelers': 0
    }

    # Seniors keywords
    seniors_kw = ['senior', 'elderly', 'aged', 'retirement', 'arthritis', 'medicare',
                  'retiree', 'grandparent', 'pension', '65+', '70+', 'aging']
    persona_scores['seniors'] = sum(1 for kw in seniors_kw if kw in text)

    # Athletes keywords
    athletes_kw = ['athlete', 'fitness', 'gym', 'sport', 'runner', 'training', 'workout',
                   'marathon', 'crossfit', 'yoga', 'cycling', 'tennis', 'basketball']
    persona_scores['athletes'] = sum(1 for kw in athletes_kw if kw in text)

    # Workers keywords
    workers_kw = ['office', 'desk', 'work', 'corporate', 'business', 'employee',
                  'workplace', 'ergonomic', 'computer', 'professional']
    persona_scores['workers'] = sum(1 for kw in workers_kw if kw in text)

    # Parents keywords
    parents_kw = ['parent', 'baby', 'child', 'daycare', 'preschool', 'mom', 'dad',
                  'family', 'kids', 'children', 'toddler']
    persona_scores['parents'] = sum(1 for kw in parents_kw if kw in text)

    # Travelers keywords
    travelers_kw = ['travel', 'flight', 'hotel', 'tourism', 'vacation', 'airport',
                    'trip', 'journey', 'destination']
    persona_scores['travelers'] = sum(1 for kw in travelers_kw if kw in text)

    # Find highest scoring persona
    max_persona = max(persona_scores, key=persona_scores.get)
    max_score = persona_scores[max_persona]

    # If no clear match, return 'unknown'
    if max_score == 0:
        return 'unknown'

    return max_persona

def calculate_quality_score(lead):
    """Calculate lead quality score (1-10)"""
    score = 5.0  # Base score

    # Email: +2 if valid (required field, so always +2)
    if lead['email']:
        score += 2.0

    # Phone: +1 if present and valid
    if lead['phone'] and validate_phone(lead['phone']):
        score += 1.0

    # Name: +1 if present
    if lead['name']:
        score += 1.0

    # Location: +0.5 if present
    if lead['location']:
        score += 0.5

    # Source quality bonus
    source_bonus = {
        'facebook_lead_ads': 1.5,      # Highest (paid ads, explicit opt-in)
        'contest_prelaunch': 1.0,      # High (explicit opt-in, brand aware)
        'import_externe': 0.5,         # Medium (depends on source quality)
        'klaviyo': 1.0,                # High (website opt-in)
        'instagram': 0.0,              # Low (scraped, no opt-in)
        'facebook': 0.0,               # Low (scraped, no opt-in)
        'tiktok': 0.0,                 # Low (scraped, no opt-in)
        'google_maps': 0.0             # Low (scraped B2B)
    }
    score += source_bonus.get(lead['platform'], 0.0)

    # Engagement bonus (for social scraping)
    if lead.get('engagement'):
        try:
            engagement = float(lead['engagement'])
            if engagement >= 5000:
                score += 1.0
            elif engagement >= 1000:
                score += 0.5
        except:
            pass

    # Cap at 10
    return min(10.0, score)

def clean_and_segment():
    """Main function: Clean and segment all unprocessed leads"""

    # Check credentials
    if not CREDENTIALS_FILE.exists():
        print(f"❌ ERROR: Credentials not found: {CREDENTIALS_FILE}")
        return False

    # Authenticate
    print(f"🔐 Authenticating with Google Sheets...")
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

    # Open sheets
    print(f"📋 Opening Google Sheet: {SHEET_NAME}...")
    try:
        spreadsheet = client.open(SHEET_NAME)
        raw_sheet = spreadsheet.worksheet(RAW_LEADS_SHEET)
        qualified_sheet = spreadsheet.worksheet(QUALIFIED_LEADS_SHEET)
        print(f"✅ Opened worksheets: {RAW_LEADS_SHEET}, {QUALIFIED_LEADS_SHEET}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

    # Read raw leads
    print(f"\n📥 Reading raw leads...")
    try:
        raw_data = raw_sheet.get_all_records()
        print(f"✅ Found {len(raw_data)} total rows in {RAW_LEADS_SHEET}")
    except Exception as e:
        print(f"❌ ERROR reading raw leads: {e}")
        return False

    # Filter unprocessed leads (no "Processed" column or empty/FALSE)
    unprocessed = []
    for idx, lead in enumerate(raw_data):
        # Check if already processed
        processed = lead.get('Processed', '').strip().upper()
        if processed not in ['TRUE', 'YES', 'PROCESSED', '✅']:
            unprocessed.append((idx + 2, lead))  # idx+2 because row 1 is header, 0-indexed

    print(f"📊 Unprocessed leads: {len(unprocessed)}")

    if len(unprocessed) == 0:
        print(f"✅ No new leads to process")
        return True

    # Read existing qualified leads (to check for duplicates)
    try:
        qualified_data = qualified_sheet.get_all_records()
        existing_emails = {str(row.get('Email', '')).strip().lower() for row in qualified_data}
        print(f"📋 Existing qualified leads: {len(existing_emails)} (for duplicate check)")
    except:
        existing_emails = set()

    # Process each unprocessed lead
    print(f"\n🔄 Processing {len(unprocessed)} leads...")
    processed_count = 0
    skipped = {'no_email': 0, 'invalid_email': 0, 'duplicate': 0}

    for row_num, lead in unprocessed:
        # Extract fields
        email = str(lead.get('Email', lead.get('Contact', ''))).strip().lower()
        name = str(lead.get('Name', '')).strip()
        phone = str(lead.get('Phone', '')).strip()
        location = str(lead.get('Location', '')).strip()
        platform = str(lead.get('Platform', '')).strip()
        lead_type = str(lead.get('Type', '')).strip()
        engagement = lead.get('Engagement', '')
        notes = str(lead.get('Notes', '')).strip()
        source_original = str(lead.get('Source Original', '')).strip()

        # Skip if no email
        if not email:
            skipped['no_email'] += 1
            continue

        # Validate email
        if not validate_email(email):
            skipped['invalid_email'] += 1
            print(f"   ⚠️  Row {row_num}: Invalid email '{email}'")
            continue

        # Skip duplicates
        if email in existing_emails:
            skipped['duplicate'] += 1
            # Mark as processed in Raw Leads (duplicate)
            try:
                raw_sheet.update_cell(row_num, 17, 'DUPLICATE')  # Column Q (Processed)
            except:
                pass
            continue

        existing_emails.add(email)  # Add to set to catch duplicates within batch

        # Build processed lead
        processed_lead = {
            'timestamp': lead.get('Timestamp', datetime.now().isoformat()),
            'platform': platform,
            'type': lead_type,
            'name': name,
            'email': email,
            'phone': phone,
            'location': location,
            'engagement': engagement,
            'source_original': source_original,
            'notes': notes
        }

        # Calculate quality score
        quality_score = calculate_quality_score(processed_lead)

        # Detect persona
        persona = detect_persona(name, location, notes, source_original)

        # Prepare row for Qualified Leads sheet
        qualified_row = [
            processed_lead['timestamp'],     # A: Timestamp
            platform,                        # B: Platform
            lead_type,                       # C: Type
            name,                            # D: Name
            email,                           # E: Email
            phone,                           # F: Phone
            location,                        # G: Location
            quality_score,                   # H: Quality Score
            persona,                         # I: Persona Match
            'new',                           # J: Status (new/contacted/converted)
            '',                              # K: Last Contact
            source_original,                 # L: Source Original
            notes,                           # M: Notes
            datetime.now().strftime('%Y-%m-%d'),  # N: Date Added
            '',                              # O: Campaign Assigned
            ''                               # P: Conversion Value
        ]

        # Append to Qualified Leads
        try:
            qualified_sheet.append_row(qualified_row, value_input_option='USER_ENTERED')
            processed_count += 1
            print(f"   [{processed_count}] ✅ {name or email[:30]} (Score: {quality_score:.1f}, Persona: {persona})")

            # Mark as processed in Raw Leads
            raw_sheet.update_cell(row_num, 17, 'TRUE')  # Column Q (Processed)

        except Exception as e:
            print(f"   ❌ Row {row_num}: Error - {e}")

    # Summary
    print("\n" + "="*80)
    print(f"CLEANING & SEGMENTATION COMPLETE")
    print("="*80)
    print(f"✅ Processed: {processed_count}/{len(unprocessed)} leads")
    print(f"⚠️  Skipped (no email): {skipped['no_email']}")
    print(f"⚠️  Skipped (invalid email): {skipped['invalid_email']}")
    print(f"⚠️  Skipped (duplicates): {skipped['duplicate']}")
    print(f"\n📋 Qualified Leads sheet updated: {processed_count} new leads")
    print(f"   View: https://docs.google.com/spreadsheets/d/1KyE_H8OPLLJfgRjehNZLS_RcMJToHRQ9gny1Sgoa_JE")

    return processed_count > 0

def main():
    print("="*80)
    print("CLEAN AND SEGMENT LEADS - AUTOMATED PIPELINE")
    print("="*80)

    success = clean_and_segment()

    if success:
        print("\n🎉 Cleaning & segmentation successful!")
        sys.exit(0)
    else:
        print("\n⚠️  No leads processed")
        sys.exit(0)  # Not an error, just no new leads

if __name__ == "__main__":
    import sys
    main()
