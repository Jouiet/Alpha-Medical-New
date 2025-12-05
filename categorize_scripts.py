#!/usr/bin/env python3
"""
Categorize Python Scripts for Repository Restructure
Alpha Medical - P0-DAY3 Task
Date: 2025-12-05

Analyzes Python files in root directory and proposes organized structure.
"""

import os
from pathlib import Path
from collections import defaultdict
import re

def categorize_file(filename: str) -> str:
    """Determine category based on filename patterns."""

    # Forensic and audit scripts
    if any(x in filename for x in ['forensic', 'audit_', 'comprehensive_validation']):
        return 'analysis/audits'

    # Verification scripts
    if filename.startswith('verify_'):
        return 'analysis/verification'

    # Check scripts
    if filename.startswith('check_'):
        return 'analysis/checks'

    # Deployment scripts
    if filename.startswith('deploy_'):
        return 'deployment'

    # Fix and repair scripts
    if filename.startswith('fix_'):
        return 'maintenance/fixes'

    # Update scripts
    if filename.startswith('update_'):
        return 'maintenance/updates'

    # Creation scripts
    if filename.startswith('create_'):
        return 'automation/creation'

    # Generation scripts
    if filename.startswith('generate_'):
        return 'automation/generation'

    # Optimization scripts
    if 'optimize' in filename:
        return 'optimization'

    # Loyalty program scripts
    if 'loyalty' in filename:
        return 'features/loyalty'

    # Bundle-related scripts
    if 'bundle' in filename:
        return 'features/bundles'

    # Analytics and tracking
    if any(x in filename for x in ['tracking', 'analytics', 'extract_', 'analyze_']):
        return 'analytics'

    # Migration and data scripts
    if any(x in filename for x in ['migrate', 'import_', 'export_']):
        return 'data'

    # Test scripts
    if filename.startswith('test_'):
        return 'tests'

    # Configuration and setup
    if any(x in filename for x in ['setup', 'config', 'install']):
        return 'setup'

    # Utilities (generic scripts)
    if any(x in filename for x in ['util', 'helper', 'tool']):
        return 'utils'

    # Market analysis (already has directory)
    if filename.startswith('market'):
        return 'KEEP_IN_MARKET_ANALYSIS'

    # Default category for uncategorized
    return 'uncategorized'

def main():
    """Main execution function."""
    print("=" * 80)
    print("PYTHON SCRIPT CATEGORIZATION ANALYSIS")
    print("=" * 80)
    print()

    # Find all Python files in root
    root_files = [f for f in os.listdir('.') if f.endswith('.py') and os.path.isfile(f)]

    # Categorize files
    categories = defaultdict(list)
    for filename in sorted(root_files):
        category = categorize_file(filename)
        categories[category].append(filename)

    # Display results
    total_files = len(root_files)
    print(f"📊 Total Python files in root: {total_files}")
    print()

    print("=" * 80)
    print("PROPOSED DIRECTORY STRUCTURE")
    print("=" * 80)
    print()

    for category in sorted(categories.keys()):
        files = categories[category]
        print(f"📁 scripts/{category}/ ({len(files)} files)")

        # Show first 5 files as examples
        for filename in files[:5]:
            print(f"   - {filename}")

        if len(files) > 5:
            print(f"   ... and {len(files) - 5} more")

        print()

    print("=" * 80)
    print("SUMMARY BY CATEGORY")
    print("=" * 80)
    print()

    for category in sorted(categories.keys(), key=lambda x: len(categories[x]), reverse=True):
        count = len(categories[category])
        percentage = (count / total_files) * 100
        print(f"{category:30s} : {count:3d} files ({percentage:5.1f}%)")

    print()
    print("=" * 80)
    print("PROPOSED STRUCTURE:")
    print("=" * 80)
    print()
    print("/scripts/")
    print("  ├── analysis/")
    print("  │   ├── audits/          # Comprehensive audits and forensic analysis")
    print("  │   ├── verification/    # Verify deployments, configurations, data")
    print("  │   └── checks/          # Quick status checks")
    print("  ├── automation/")
    print("  │   ├── creation/        # Create products, collections, pages")
    print("  │   └── generation/      # Generate assets, content, configs")
    print("  ├── deployment/          # Deploy changes to Shopify")
    print("  ├── maintenance/")
    print("  │   ├── fixes/           # Fix bugs, correct data")
    print("  │   └── updates/         # Update existing resources")
    print("  ├── features/")
    print("  │   ├── bundles/         # Bundle product management")
    print("  │   └── loyalty/         # Loyalty program scripts")
    print("  ├── analytics/           # Tracking, analysis, data extraction")
    print("  ├── optimization/        # Performance and SEO optimization")
    print("  ├── data/                # Data migration and import/export")
    print("  ├── tests/               # Test scripts")
    print("  ├── setup/               # Configuration and installation")
    print("  ├── utils/               # Utility scripts and helpers")
    print("  └── uncategorized/       # To be categorized later")
    print()

if __name__ == "__main__":
    main()
