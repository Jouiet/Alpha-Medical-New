#!/usr/bin/env python3
"""
Execute Safe Repository Migration
Alpha Medical - P0-DAY3 Task
Date: 2025-12-05
"""

import os
import shutil
from pathlib import Path
import re

# CRITICAL: Must stay in root (GitHub Actions workflows)
KEEP_IN_ROOT = {
    'clean_and_segment_leads.py',
    'export_shopify_csv.py',
    'generate_llms_full.py',
    'generate_llms_txt.py',
    'sync_facebook_leads_to_sheet.py',
    'sync_klaviyo_to_sheet.py',
    'sync_leads_to_sheets.py',
    'sync_shopify_forms_to_sheet.py',
    'validate_llms_txt.py',
    # Infrastructure/migration scripts
    'audit_forensic_complete_v2.py',
    'audit_infrastructure.py',
    'verify_store_infrastructure.py',
    'standardize_api_versions.py',
    'categorize_scripts.py',
    'migrate_scripts_safe.py',
    'identify_obsolete_scripts.py',
    'execute_migration.py'
}

def categorize(filename):
    """Determine target directory."""
    # Audits
    if any(x in filename for x in ['forensic', 'audit_', 'comprehensive_validation']):
        return 'analysis/audits'
    # Verification
    if filename.startswith('verify_'):
        return 'analysis/verification'
    # Checks
    if filename.startswith('check_'):
        return 'analysis/checks'
    # Deployment
    if filename.startswith('deploy_'):
        return 'deployment'
    # Fixes
    if filename.startswith('fix_'):
        return 'maintenance/fixes'
    # Updates
    if filename.startswith('update_'):
        return 'maintenance/updates'
    # Creation
    if filename.startswith('create_'):
        return 'automation/creation'
    # Generation
    if filename.startswith('generate_'):
        return 'automation/generation'
    # Optimization
    if 'optimize' in filename:
        return 'optimization'
    # Loyalty
    if 'loyalty' in filename:
        return 'features/loyalty'
    # Bundles
    if 'bundle' in filename:
        return 'features/bundles'
    # Analytics
    if any(x in filename for x in ['tracking', 'analytics', 'extract_', 'analyze_']):
        return 'analytics'
    # Data
    if any(x in filename for x in ['migrate', 'import_', 'export_', 'sync_']):
        return 'data'
    # Tests
    if filename.startswith('test_'):
        return 'tests'
    # Setup/config
    if any(x in filename for x in ['setup', 'config', 'install', 'configure_']):
        return 'setup'
    # Default
    return 'uncategorized'

def main():
    print("=" * 80)
    print("EXECUTING REPOSITORY MIGRATION")
    print("=" * 80)
    print()

    # Find all Python files in root
    root_files = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]

    moved = 0
    kept = 0
    errors = []

    for filename in sorted(root_files):
        # Skip CRITICAL scripts
        if filename in KEEP_IN_ROOT:
            kept += 1
            print(f"⏭️  KEEP: {filename}")
            continue

        # Determine target
        category = categorize(filename)
        target_dir = f"scripts/{category}"
        target_path = Path(target_dir) / filename

        try:
            shutil.move(filename, target_path)
            moved += 1
            print(f"✅ MOVE: {filename} → {target_dir}/")
        except Exception as e:
            errors.append((filename, str(e)))
            print(f"❌ ERROR: {filename} - {e}")

    print()
    print("=" * 80)
    print("MIGRATION COMPLETE")
    print("=" * 80)
    print()
    print(f"✅ Moved: {moved} files")
    print(f"⏭️  Kept in root: {kept} files")
    print(f"❌ Errors: {len(errors)} files")
    print()

    if errors:
        print("ERRORS:")
        for filename, error in errors:
            print(f"  - {filename}: {error}")
        print()

    # Count by category
    print("FILES BY CATEGORY:")
    for category in sorted(os.listdir('scripts/')):
        cat_path = Path('scripts') / category
        if cat_path.is_dir():
            count = len([f for f in cat_path.rglob('*.py')])
            if count > 0:
                print(f"  - {category:30s}: {count:3d} files")
    print()

if __name__ == "__main__":
    main()
