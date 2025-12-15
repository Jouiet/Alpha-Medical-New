#!/usr/bin/env python3
"""
Safe Repository Migration - Phase 1
Alpha Medical - P0-DAY3 Task
Date: 2025-12-05

Migrates Python scripts to organized /scripts/ structure while keeping
workflow-critical scripts in root to avoid GitHub Actions regressions.

SAFETY STRATEGY:
- Keep 10 GitHub Actions workflow scripts in root
- Move 272 other scripts to categorized directories
- Create migration log for rollback if needed
- No import path changes (scripts stay independent)
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict
import json

# Scripts that MUST stay in root (referenced in GitHub Actions)
WORKFLOW_CRITICAL_SCRIPTS = {
    'clean_and_segment_leads.py',
    'export_shopify_csv.py',
    'generate_llms_full.py',
    'generate_llms_txt.py',
    'sync_facebook_leads_to_sheet.py',
    'sync_klaviyo_to_sheet.py',
    'sync_leads_to_sheets.py',
    'sync_shopify_forms_to_sheet.py',
    'validate_llms_txt.py',
    # Keep migration/categorization scripts in root temporarily
    'categorize_scripts.py',
    'migrate_scripts_safe.py',
    'standardize_api_versions.py'
}

# Keep market-analysis scripts in their existing directory
EXCLUDE_PATTERNS = ['market-analysis/', 'scripts/', '.git/', 'venv/', '__pycache__']

def categorize_file(filename: str) -> str:
    """Determine category based on filename patterns."""
    if any(x in filename for x in ['forensic', 'audit_', 'comprehensive_validation']):
        return 'analysis/audits'
    if filename.startswith('verify_'):
        return 'analysis/verification'
    if filename.startswith('check_'):
        return 'analysis/checks'
    if filename.startswith('deploy_'):
        return 'deployment'
    if filename.startswith('fix_'):
        return 'maintenance/fixes'
    if filename.startswith('update_'):
        return 'maintenance/updates'
    if filename.startswith('create_'):
        return 'automation/creation'
    if filename.startswith('generate_'):
        return 'automation/generation'
    if 'optimize' in filename:
        return 'optimization'
    if 'loyalty' in filename:
        return 'features/loyalty'
    if 'bundle' in filename:
        return 'features/bundles'
    if any(x in filename for x in ['tracking', 'analytics', 'extract_', 'analyze_']):
        return 'analytics'
    if any(x in filename for x in ['migrate', 'import_', 'export_']):
        return 'data'
    if filename.startswith('test_'):
        return 'tests'
    if any(x in filename for x in ['setup', 'config', 'install', 'configure_']):
        return 'setup'
    return 'uncategorized'

def create_directory_structure():
    """Create the /scripts/ directory structure."""
    base_dirs = [
        'scripts/analysis/audits',
        'scripts/analysis/verification',
        'scripts/analysis/checks',
        'scripts/automation/creation',
        'scripts/automation/generation',
        'scripts/deployment',
        'scripts/maintenance/fixes',
        'scripts/maintenance/updates',
        'scripts/features/bundles',
        'scripts/features/loyalty',
        'scripts/analytics',
        'scripts/optimization',
        'scripts/data',
        'scripts/tests',
        'scripts/setup',
        'scripts/utils',
        'scripts/uncategorized'
    ]

    for dir_path in base_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {dir_path}/")

def migrate_files():
    """Migrate Python files to organized structure."""
    # Find all Python files in root
    root_files = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]

    # Track migration
    migration_log = {
        'kept_in_root': [],
        'migrated': [],
        'skipped': [],
        'errors': []
    }

    files_moved = 0
    files_kept = 0

    print()
    print("=" * 80)
    print("MIGRATING PYTHON SCRIPTS")
    print("=" * 80)
    print()

    for filename in sorted(root_files):
        # Skip workflow-critical scripts
        if filename in WORKFLOW_CRITICAL_SCRIPTS:
            migration_log['kept_in_root'].append(filename)
            files_kept += 1
            print(f"⏭️  KEPT IN ROOT (workflow-critical): {filename}")
            continue

        # Categorize and move
        category = categorize_file(filename)
        target_dir = f"scripts/{category}"
        target_path = Path(target_dir) / filename

        try:
            # Move file
            shutil.move(filename, target_path)
            migration_log['migrated'].append({
                'file': filename,
                'from': '.',
                'to': target_dir,
                'category': category
            })
            files_moved += 1
            print(f"✅ MOVED: {filename} → {target_dir}/")

        except Exception as e:
            migration_log['errors'].append({
                'file': filename,
                'error': str(e)
            })
            print(f"❌ ERROR: {filename} - {e}")

    return migration_log, files_moved, files_kept

def create_readme_files():
    """Create README.md files in each category directory."""
    readmes = {
        'scripts/analysis/audits': """# Audit Scripts

Comprehensive audits and forensic analysis of store infrastructure, products, and configurations.

**Examples:**
- `audit_forensic_complete_v2.py` - Complete store forensic audit
- `audit_infrastructure.py` - Infrastructure health check
- `comprehensive_validation_audit_2025.py` - Full validation audit
""",
        'scripts/analysis/verification': """# Verification Scripts

Verify deployments, configurations, data integrity, and system state.

**Examples:**
- `verify_english_only_forensic_v2.py` - Verify English-only content
- `verify_store_infrastructure.py` - Verify infrastructure setup
- `verify_collection_fixes.py` - Verify collection assignments
""",
        'scripts/analysis/checks': """# Check Scripts

Quick status checks and health monitoring.

**Examples:**
- `check_footer_menu.py` - Check footer menu configuration
- `check_theme_pixels.py` - Check tracking pixel installation
- `check_special_offers_products.py` - Check special offers status
""",
        'scripts/deployment': """# Deployment Scripts

Deploy changes, updates, and configurations to Shopify store.

**Examples:**
- `deploy_bundle_builder.py` - Deploy bundle builder functionality
- `deploy_all_corrected_snippets.py` - Deploy corrected theme snippets
- `deploy_theme_liquid.py` - Deploy theme.liquid updates
""",
        'scripts/maintenance/fixes': """# Fix Scripts

Bug fixes, data corrections, and repair operations.

**Examples:**
- `fix_missing_collections.py` - Fix products missing collection assignments
- `fix_bundle_metafields.py` - Fix bundle product metafields
- `fix_email_to_professional.py` - Fix email addresses to professional format
""",
        'scripts/automation': """# Automation Scripts

Automated creation and generation of content, products, and configurations.

**Subdirectories:**
- `creation/` - Create products, collections, pages
- `generation/` - Generate assets, content, matrices
"""
    }

    for dir_path, content in readmes.items():
        readme_path = Path(dir_path) / 'README.md'
        if not readme_path.exists():
            with open(readme_path, 'w') as f:
                f.write(content)
            print(f"📝 Created: {readme_path}")

def main():
    """Main execution function."""
    print("=" * 80)
    print("SAFE REPOSITORY MIGRATION - PHASE 1")
    print("=" * 80)
    print()
    print("STRATEGY:")
    print("- Keep 13 workflow-critical scripts in root (no GitHub Actions changes)")
    print("- Move ~270 other scripts to organized /scripts/ structure")
    print("- Create migration log for audit trail")
    print()

    # Create directory structure
    print("=" * 80)
    print("CREATING DIRECTORY STRUCTURE")
    print("=" * 80)
    print()
    create_directory_structure()

    # Migrate files
    migration_log, files_moved, files_kept = migrate_files()

    # Create README files
    print()
    print("=" * 80)
    print("CREATING README FILES")
    print("=" * 80)
    print()
    create_readme_files()

    # Save migration log
    log_path = 'MIGRATION_LOG_2025-12-05.json'
    with open(log_path, 'w') as f:
        json.dump(migration_log, f, indent=2)

    # Summary report
    print()
    print("=" * 80)
    print("MIGRATION COMPLETE - SUMMARY")
    print("=" * 80)
    print()
    print(f"📊 Files migrated to /scripts/: {files_moved}")
    print(f"⏭️  Files kept in root (workflow-critical): {files_kept}")
    print(f"❌ Errors: {len(migration_log['errors'])}")
    print()

    if migration_log['kept_in_root']:
        print("=" * 80)
        print("SCRIPTS KEPT IN ROOT (DO NOT MOVE)")
        print("=" * 80)
        print()
        for filename in sorted(migration_log['kept_in_root']):
            print(f"  - {filename}")
        print()
        print("These scripts are referenced in GitHub Actions workflows.")
        print("Moving them would break automated processes.")
        print()

    print("=" * 80)
    print(f"✅ SUCCESS: Repository structure organized")
    print("=" * 80)
    print()
    print("NEXT STEPS:")
    print("1. Review migrated files: ls -R scripts/")
    print("2. Test critical workflows: gh workflow list")
    print("3. Update .gitignore if needed")
    print(f"4. Review migration log: cat {log_path}")
    print("5. Commit changes with descriptive message")
    print()

if __name__ == "__main__":
    main()
