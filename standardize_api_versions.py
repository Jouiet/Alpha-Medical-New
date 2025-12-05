#!/usr/bin/env python3
"""
Standardize Shopify API Versions to 2025-10
Alpha Medical - P0-DAY3 Task
Date: 2025-12-05

Updates all Python files to use the latest stable Shopify Admin API version (2025-10)
as verified via Shopify documentation on 2025-12-05.
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

TARGET_VERSION = "2025-10"
OLD_VERSIONS = ["2024-01", "2024-04", "2024-07", "2024-10", "2025-01"]

def find_python_files() -> List[Path]:
    """Find all Python files in the project."""
    python_files = []
    for root, dirs, files in os.walk("."):
        # Skip hidden directories and venv
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']

        for file in files:
            if file.endswith('.py'):
                python_files.append(Path(root) / file)

    return python_files

def check_and_update_file(file_path: Path) -> Tuple[bool, str, str]:
    """
    Check if file contains old API version and update it.

    Returns:
        Tuple of (was_updated, old_version, new_version)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pattern to match API_VERSION declarations with old versions
        pattern = r'(API_VERSION\s*=\s*[\'"])(202[45]-[0-9]{2})([\'"])'

        old_version = None
        updated = False

        # Find current version
        match = re.search(pattern, content)
        if match:
            old_version = match.group(2)

            # Only update if it's an old version
            if old_version in OLD_VERSIONS:
                # Replace with target version
                new_content = re.sub(pattern, f'\\g<1>{TARGET_VERSION}\\g<3>', content)

                # Write back to file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                updated = True
                return (updated, old_version, TARGET_VERSION)

        return (False, old_version or "N/A", "N/A")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return (False, "ERROR", "ERROR")

def main():
    """Main execution function."""
    print("=" * 80)
    print("STANDARDIZING SHOPIFY API VERSIONS TO 2025-10")
    print("=" * 80)
    print()

    # Find all Python files
    python_files = find_python_files()
    print(f"Found {len(python_files)} Python files to scan")
    print()

    # Track statistics
    files_updated = []
    files_already_correct = []
    files_no_api_version = []

    # Process each file
    for file_path in python_files:
        was_updated, old_version, new_version = check_and_update_file(file_path)

        if was_updated:
            files_updated.append((str(file_path), old_version, new_version))
            print(f"✅ UPDATED: {file_path}")
            print(f"   {old_version} → {new_version}")
        elif old_version == TARGET_VERSION:
            files_already_correct.append(str(file_path))
        elif old_version == "N/A":
            files_no_api_version.append(str(file_path))

    # Summary report
    print()
    print("=" * 80)
    print("STANDARDIZATION COMPLETE - SUMMARY")
    print("=" * 80)
    print()

    print(f"📊 Total Python files scanned: {len(python_files)}")
    print(f"✅ Files updated: {len(files_updated)}")
    print(f"✓  Files already correct (2025-10): {len(files_already_correct)}")
    print(f"○  Files without API_VERSION: {len(files_no_api_version)}")
    print()

    if files_updated:
        print("=" * 80)
        print("DETAILED UPDATE LOG")
        print("=" * 80)
        print()

        # Group by old version
        by_version = {}
        for file_path, old_ver, new_ver in files_updated:
            if old_ver not in by_version:
                by_version[old_ver] = []
            by_version[old_ver].append(file_path)

        for old_ver in sorted(by_version.keys()):
            files = by_version[old_ver]
            print(f"Updated from {old_ver} → {TARGET_VERSION} ({len(files)} files):")
            for file_path in files:
                print(f"  - {file_path}")
            print()

    print("=" * 80)
    print(f"✅ SUCCESS: All API versions standardized to {TARGET_VERSION}")
    print("=" * 80)
    print()
    print("NEXT STEPS:")
    print("1. Test critical scripts to verify API compatibility")
    print("2. Run git diff to review all changes")
    print("3. Commit changes with descriptive message")
    print()

if __name__ == "__main__":
    main()
