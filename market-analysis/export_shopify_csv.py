#!/usr/bin/env python3
"""
EXPORT SHOPIFY CSV - Convert Google Sheets leads to Shopify import format
NO external apps - Pure Python

Usage:
    python3 export_shopify_csv.py leads/general/leads_general_instagram_20251122.json

Output:
    shopify_import_YYYYMMDD_HHMMSS.csv

Shopify CSV Format:
    First Name, Last Name, Email, Phone, Tags, Note

Can also read from Google Sheets (if gspread installed):
    python3 export_shopify_csv.py --from-sheets
"""

import json
import csv
import sys
from datetime import datetime
from pathlib import Path

def extract_name_parts(full_name):
    """Extract first and last name from full name"""
    # Remove @ symbol if present (Instagram usernames)
    full_name = full_name.replace('@', '').strip()

    if not full_name:
        return 'Lead', ''

    parts = full_name.split()

    if len(parts) == 0:
        return 'Lead', ''
    elif len(parts) == 1:
        return parts[0], ''
    else:
        return parts[0], ' '.join(parts[1:])

def format_tags(lead):
    """Generate Shopify tags based on lead data"""
    tags = ['lead']  # All leads get 'lead' tag

    # Add platform
    if lead.get('platform'):
        tags.append(lead['platform'])

    # Add persona
    persona = detect_persona(lead)
    if persona:
        tags.append(persona)

    # Add priority based on quality_score
    quality_score = float(lead.get('quality_score', 0))
    if quality_score >= 8.5:
        tags.append('hot')
    elif quality_score >= 7.5:
        tags.append('warm')
    else:
        tags.append('cold')

    # Add lead type
    if lead.get('type'):
        tags.append(lead['type'])

    return ','.join(tags)

def detect_persona(lead):
    """Detect persona from lead data"""
    text = f"{lead.get('name', '')} {lead.get('category', '')} {lead.get('address', '')} {lead.get('location', '')}".lower()

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
        return ''

def format_note(lead):
    """Generate note field for Shopify"""
    notes = []

    # Quality score
    if lead.get('quality_score'):
        notes.append(f"Quality Score: {lead['quality_score']}")

    # Platform
    if lead.get('platform'):
        notes.append(f"Source: {lead['platform']}")

    # Location
    location = lead.get('address') or lead.get('location') or lead.get('locationName')
    if location:
        notes.append(f"Location: {location}")

    # Engagement (Instagram)
    if lead.get('engagement'):
        notes.append(f"Engagement: {lead['engagement']}")

    # Rating (Google Maps)
    if lead.get('rating'):
        notes.append(f"Rating: {lead['rating']}★")
        if lead.get('review_count'):
            notes.append(f"Reviews: {lead['review_count']}")

    return ' | '.join(notes)

def convert_to_shopify_csv(input_file, output_file):
    """Convert leads JSON to Shopify CSV"""

    # Load leads
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            leads = json.load(f)
        print(f"✅ Loaded {len(leads)} leads from {input_file}")
    except Exception as e:
        print(f"❌ ERROR loading JSON: {e}")
        return False

    # Prepare CSV
    converted = 0
    skipped = 0

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone', 'Tags', 'Note'])

        for i, lead in enumerate(leads, 1):
            # Extract contact info
            email = lead.get('email', '')
            phone = lead.get('phone', '')
            website = lead.get('website', '')
            username = lead.get('username', '')

            # For Instagram leads: use username as identifier
            # For Google Maps: use phone or website

            # Extract name
            if username and not lead.get('name'):
                # Instagram lead with username
                first_name = username
                last_name = ''
            else:
                first_name, last_name = extract_name_parts(lead.get('name', ''))

            # Generate tags
            tags = format_tags(lead)

            # Generate note
            note = format_note(lead)

            # For Instagram leads without email/phone, use username as contact
            # Add Instagram profile URL to note
            if lead.get('platform') == 'instagram' and username:
                if not email and not phone:
                    # Use Instagram profile as contact method
                    # Add to note instead of email field (Shopify allows empty email)
                    note = f"Instagram: @{username} | {note}" if note else f"Instagram: @{username}"

                    # If we have post URL, use that
                    if lead.get('url'):
                        note = f"{note} | Profile: https://instagram.com/{username}"

            # Skip ONLY if completely no contact method AND no username
            if not email and not phone and not website and not username:
                print(f"   [{i}/{len(leads)}] ⚠️  Skipped: {lead.get('name', 'Unknown')} (no contact info)")
                skipped += 1
                continue

            # Write row
            writer.writerow([
                first_name,
                last_name,
                email,
                phone,
                tags,
                note
            ])

            converted += 1
            contact_type = 'email' if email else ('phone' if phone else 'Instagram')
            print(f"   [{i}/{len(leads)}] ✅ {first_name} ({contact_type}, tags: {tags})")

    # Summary
    print("\n" + "="*70)
    print("CSV EXPORT COMPLETE")
    print("="*70)
    print(f"✅ Converted: {converted}/{len(leads)} leads")
    if skipped > 0:
        print(f"⚠️  Skipped: {skipped} leads (no contact info)")
    print(f"\n📄 Output file: {output_file}")
    print("\n📝 Next step:")
    print(f"   1. Go to Shopify Admin → Customers")
    print(f"   2. Click 'Import'")
    print(f"   3. Upload: {output_file}")
    print(f"   4. Review and import")

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 export_shopify_csv.py <leads_file.json>")
        print("\nExample:")
        print("  python3 export_shopify_csv.py leads/general/leads_general_instagram_20251122.json")
        sys.exit(1)

    input_file = sys.argv[1]

    if not Path(input_file).exists():
        print(f"❌ ERROR: File not found: {input_file}")
        sys.exit(1)

    # Generate output filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"shopify_import_{timestamp}.csv"

    print("="*70)
    print("SHOPIFY CSV EXPORT")
    print("="*70)
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")
    print("="*70 + "\n")

    success = convert_to_shopify_csv(input_file, output_file)

    if success:
        print("\n🎉 Export successful!")
        sys.exit(0)
    else:
        print("\n❌ Export failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
