#!/usr/bin/env python3
"""
Identify Obsolete Scripts - Factual Analysis
Alpha Medical - P0-DAY3 Cleanup Task
Date: 2025-12-05

Analyzes Python scripts to identify which are:
- CRITICAL: Must keep (used in automation, workflows)
- USEFUL: Keep for maintenance
- OBSOLETE: Can be safely removed
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

# Scripts referenced in GitHub Actions (CRITICAL - NEVER DELETE)
WORKFLOW_SCRIPTS = {
    'clean_and_segment_leads.py',
    'export_shopify_csv.py',
    'generate_llms_full.py',
    'generate_llms_txt.py',
    'sync_facebook_leads_to_sheet.py',
    'sync_klaviyo_to_sheet.py',
    'sync_leads_to_sheets.py',
    'sync_shopify_forms_to_sheet.py',
    'validate_llms_txt.py'
}

# Utility/infrastructure scripts (CRITICAL - KEEP)
INFRASTRUCTURE_SCRIPTS = {
    'audit_forensic_complete_v2.py',
    'audit_infrastructure.py',
    'verify_store_infrastructure.py',
    'standardize_api_versions.py',
    'categorize_scripts.py',
    'migrate_scripts_safe.py',
    'identify_obsolete_scripts.py'
}

# One-time deployment patterns (likely OBSOLETE if old)
ONE_TIME_PATTERNS = [
    r'^deploy_.*_fix\.py$',  # deploy_confetti_fix.py
    r'^deploy_.*_phase\d\.py$',  # deploy_bundle_ctas_phase1.py
    r'^push_.*\.py$',  # push_slideshow_liquid.py
    r'^upload_.*\.py$',  # upload_hero_images.py
]

# Debugging/investigation patterns (OBSOLETE after issue resolved)
DEBUG_PATTERNS = [
    r'^diagnose_.*\.py$',
    r'^investigate_.*\.py$',
    r'^check_.*_issue\.py$',
    r'^fix_n8n.*\.py$',
    r'^analyze_execution.*\.py$'
]

# N8N workflow troubleshooting (OBSOLETE if workflow working)
N8N_TROUBLESHOOT_PATTERNS = [
    r'^.*n8n.*\.py$',
    r'^.*workflow.*fix.*\.py$',
    r'^.*workflow.*activate.*\.py$',
    r'^monitor_.*\.py$'
]

# One-time fixes (OBSOLETE after successful execution)
FIX_PATTERNS = [
    r'^fix_.*_missing_.*\.py$',
    r'^fix_.*_descriptions?\.py$',
    r'^fix_.*_assignments?\.py$',
    r'^create_missing_.*\.py$'
]

def is_match_pattern(filename: str, patterns: list) -> bool:
    """Check if filename matches any pattern."""
    return any(re.match(pattern, filename) for pattern in patterns)

def get_file_age_days(filepath: Path) -> int:
    """Get file age in days."""
    mtime = os.path.getmtime(filepath)
    file_date = datetime.fromtimestamp(mtime)
    age = datetime.now() - file_date
    return age.days

def analyze_script_content(filepath: Path) -> dict:
    """Analyze script content for indicators."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            'has_main': 'if __name__ == "__main__"' in content,
            'is_one_time': 'ONE-TIME' in content.upper() or 'ONCE' in content.upper(),
            'is_deprecated': 'DEPRECATED' in content.upper() or 'OBSOLETE' in content.upper(),
            'has_api_call': 'requests.post' in content or 'requests.get' in content,
            'has_shopify_api': 'shopify' in content.lower() and 'admin/api' in content,
            'lines': len(content.split('\n'))
        }
    except:
        return {}

def categorize_script(filename: str, age_days: int, content_info: dict) -> tuple:
    """
    Categorize script as CRITICAL, USEFUL, or OBSOLETE.

    Returns: (category, reason)
    """
    # CRITICAL: Workflow scripts
    if filename in WORKFLOW_SCRIPTS:
        return ('CRITICAL', 'GitHub Actions workflow')

    # CRITICAL: Infrastructure scripts
    if filename in INFRASTRUCTURE_SCRIPTS:
        return ('CRITICAL', 'Infrastructure/audit tool')

    # CRITICAL: Recent active scripts with Shopify API
    if age_days <= 7 and content_info.get('has_shopify_api'):
        return ('USEFUL', 'Recently used Shopify API script')

    # OBSOLETE: Old debugging scripts
    if is_match_pattern(filename, DEBUG_PATTERNS) and age_days > 7:
        return ('OBSOLETE', 'Old debugging script')

    # OBSOLETE: Old N8N troubleshooting
    if is_match_pattern(filename, N8N_TROUBLESHOOT_PATTERNS) and age_days > 7:
        return ('OBSOLETE', 'Old N8N troubleshooting script')

    # OBSOLETE: Old one-time deployments
    if is_match_pattern(filename, ONE_TIME_PATTERNS) and age_days > 14:
        return ('OBSOLETE', 'Old deployment script')

    # OBSOLETE: Old one-time fixes
    if is_match_pattern(filename, FIX_PATTERNS) and age_days > 14:
        return ('OBSOLETE', 'Old one-time fix')

    # OBSOLETE: Explicitly marked deprecated
    if content_info.get('is_deprecated'):
        return ('OBSOLETE', 'Marked as deprecated')

    # USEFUL: Recent scripts
    if age_days <= 7:
        return ('USEFUL', 'Recently modified')

    # USEFUL: Scripts with Shopify API (might be needed)
    if content_info.get('has_shopify_api'):
        return ('USEFUL', 'Contains Shopify API logic')

    # DEFAULT: Keep if unsure (prefer false negative over false positive)
    return ('USEFUL', 'Uncertain - keep for safety')

def main():
    """Main execution function."""
    print("=" * 80)
    print("OBSOLETE SCRIPT IDENTIFICATION - FACTUAL ANALYSIS")
    print("=" * 80)
    print()

    # Find all Python files in root
    root_files = [Path(f) for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]

    # Analyze each file
    categories = defaultdict(list)

    for filepath in sorted(root_files):
        filename = filepath.name
        age_days = get_file_age_days(filepath)
        content_info = analyze_script_content(filepath)

        category, reason = categorize_script(filename, age_days, content_info)

        categories[category].append({
            'file': filename,
            'age_days': age_days,
            'reason': reason,
            'size_kb': os.path.getsize(filepath) / 1024,
            'lines': content_info.get('lines', 0)
        })

    # Display results
    print(f"📊 Total Python files analyzed: {len(root_files)}")
    print()

    for category in ['CRITICAL', 'USEFUL', 'OBSOLETE']:
        scripts = categories[category]
        print("=" * 80)
        print(f"{category} SCRIPTS: {len(scripts)} files")
        print("=" * 80)
        print()

        for item in sorted(scripts, key=lambda x: x['age_days']):
            age_str = f"{item['age_days']}d ago" if item['age_days'] > 0 else "today"
            print(f"  - {item['file']:<50s} ({age_str:>10s}) - {item['reason']}")

        print()

    # Summary statistics
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    total = len(root_files)
    critical = len(categories['CRITICAL'])
    useful = len(categories['USEFUL'])
    obsolete = len(categories['OBSOLETE'])

    print(f"CRITICAL (must keep):           {critical:3d} files ({critical/total*100:5.1f}%)")
    print(f"USEFUL (keep for maintenance):  {useful:3d} files ({useful/total*100:5.1f}%)")
    print(f"OBSOLETE (safe to remove):      {obsolete:3d} files ({obsolete/total*100:5.1f}%)")
    print()

    if obsolete > 0:
        print("=" * 80)
        print("PROPOSED CLEANUP ACTION")
        print("=" * 80)
        print()
        print(f"Create archive directory: ./archive/obsolete-scripts-2025-12-05/")
        print(f"Move {obsolete} obsolete scripts to archive")
        print(f"Reduce root from {total} to {critical + useful} scripts ({(critical+useful)/total*100:.0f}%)")
        print()
        print("BENEFITS:")
        print(f"  - Cleaner repository ({obsolete} fewer files in root)")
        print(f"  - Faster script discovery")
        print(f"  - No risk of running wrong/old scripts")
        print(f"  - Scripts preserved in archive (can restore if needed)")
        print()

    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print()
    print("1. Review OBSOLETE list above")
    print("2. If approved, run: python3 archive_obsolete_scripts.py")
    print("3. Test critical workflows: gh workflow list")
    print("4. Commit cleanup with descriptive message")
    print()

if __name__ == "__main__":
    main()
