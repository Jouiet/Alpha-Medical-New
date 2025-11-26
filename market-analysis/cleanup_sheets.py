#!/usr/bin/env python3
"""
CLEANUP & REORGANIZE GOOGLE SHEETS
Fixes headers, removes duplicates, sorts by quality score

Usage:
    python3 cleanup_sheets.py
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

# Configuration
CREDENTIALS_FILE = Path(__file__).parent / "google_credentials.json"
SHEET_NAME = "Alpha Medical - Lead Management"
WORKSHEET_NAME = "Raw Leads"

# Correct headers (12 columns)
CORRECT_HEADERS = [
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

def cleanup_and_organize():
    """Clean up and reorganize Google Sheet"""

    print("🧹 GOOGLE SHEETS CLEANUP & REORGANIZATION")
    print("=" * 70)

    # Authenticate
    try:
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(str(CREDENTIALS_FILE), scope)
        client = gspread.authorize(creds)
        print("✅ Authenticated with Google Sheets API")
    except Exception as e:
        print(f"❌ ERROR authenticating: {e}")
        return False

    # Open sheet
    try:
        spreadsheet = client.open(SHEET_NAME)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        print(f"✅ Opened sheet: {SHEET_NAME} → {WORKSHEET_NAME}")
    except Exception as e:
        print(f"❌ ERROR opening sheet: {e}")
        return False

    # Get all data
    try:
        all_data = worksheet.get_all_values()
        print(f"✅ Fetched {len(all_data)} rows")
    except Exception as e:
        print(f"❌ ERROR fetching data: {e}")
        return False

    if not all_data:
        print("⚠️  Sheet is empty")
        return False

    # Step 1: Fix headers
    print("\n📋 Step 1: Checking headers...")
    current_headers = all_data[0] if all_data else []

    if current_headers != CORRECT_HEADERS:
        print(f"⚠️  Headers incorrect or missing")
        print(f"   Current: {current_headers}")
        print(f"   Correct: {CORRECT_HEADERS}")

        # Update headers
        worksheet.update([CORRECT_HEADERS], 'A1:L1')
        print("✅ Headers fixed!")
    else:
        print("✅ Headers already correct")

    # Step 2: Remove duplicates
    print("\n🔍 Step 2: Removing duplicates...")

    if len(all_data) <= 1:
        print("⚠️  No data rows to process")
        return True

    data_rows = all_data[1:]  # Skip header
    seen = set()
    unique_rows = []
    duplicates = 0

    for row in data_rows:
        # Truncate row to exactly 12 columns
        truncated_row = row[:12]

        # Pad with empty strings if less than 12 columns
        while len(truncated_row) < 12:
            truncated_row.append('')

        # Create unique key from name + contact + location
        if len(truncated_row) >= 6:
            key = f"{truncated_row[3]}|{truncated_row[4]}|{truncated_row[5]}".lower()  # name|contact|location

            if key not in seen and truncated_row[3].strip():  # Only add if name is not empty
                seen.add(key)
                unique_rows.append(truncated_row)
            else:
                duplicates += 1

    print(f"   Original rows: {len(data_rows)}")
    print(f"   Unique rows: {len(unique_rows)}")
    print(f"   Duplicates removed: {duplicates}")

    # Step 3: Sort by quality score (descending)
    print("\n📊 Step 3: Sorting by quality score...")

    def get_quality_score(row):
        """Extract quality score for sorting"""
        try:
            if len(row) >= 10 and row[9]:  # quality_score is column 10 (index 9)
                return float(row[9])
        except (ValueError, IndexError):
            pass
        return 0.0

    sorted_rows = sorted(unique_rows, key=get_quality_score, reverse=True)
    print(f"✅ Sorted {len(sorted_rows)} rows by quality score")

    # Step 4: Clear and rewrite sheet
    print("\n🔄 Step 4: Rewriting sheet...")

    try:
        # Clear all data (keep headers)
        worksheet.clear()

        # Write headers
        worksheet.update([CORRECT_HEADERS], 'A1:L1')

        # Write sorted unique data (in batches for performance)
        if sorted_rows:
            # gspread has a limit, so batch updates
            batch_size = 100
            for i in range(0, len(sorted_rows), batch_size):
                batch = sorted_rows[i:i+batch_size]
                start_row = i + 2  # +2 because row 1 is headers, and rows are 1-indexed
                end_row = start_row + len(batch) - 1

                worksheet.update(batch, f'A{start_row}:L{end_row}')
                print(f"   ✅ Wrote rows {start_row}-{end_row}")

        print(f"✅ Sheet reorganized successfully!")

    except Exception as e:
        print(f"❌ ERROR rewriting sheet: {e}")
        return False

    # Summary
    print("\n" + "=" * 70)
    print("CLEANUP COMPLETE")
    print("=" * 70)
    print(f"✅ Total unique leads: {len(sorted_rows)}")
    print(f"✅ Duplicates removed: {duplicates}")
    print(f"✅ Headers fixed: {CORRECT_HEADERS}")
    print(f"✅ Sorted by quality score (highest first)")
    print("\n🎉 Google Sheet is now organized!")

    return True

if __name__ == "__main__":
    success = cleanup_and_organize()
    exit(0 if success else 1)
