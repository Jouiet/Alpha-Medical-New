#!/usr/bin/env python3
"""
FIX GTM-MW2FN7MQ INCORRECT REFERENCES IN DOCUMENTATION
Replaces false GTM container ID with correct Shopify Channel App info
"""

import re

files_to_fix = [
    '/Users/mac/Desktop/Alpha-Medical/EMAIL_MARKETING_AUTOMATION_AUDIT.md',
    '/Users/mac/Desktop/Alpha-Medical/SEO_MARKETING_FORENSIC_ANALYSIS.md',
    '/Users/mac/Desktop/Alpha-Medical/SESSION_2025-11-11_PART6_SUMMARY.md'
]

# Replacement patterns
replacements = [
    # Pattern 1: GTM container ID references
    (
        r'GTM-MW2FN7MQ',
        'GT-NC6L8G55 (Shopify Channel App - NATIVE, not GTM)'
    ),
    # Pattern 2: "Google Tag Manager (GTM-MW2FN7MQ)"
    (
        r'Google Tag Manager.*\(GTM-MW2FN7MQ\)',
        'Shopify Google Channel (GT-NC6L8G55)'
    ),
    # Pattern 3: References to GTM Container
    (
        r'GTM Container.*GTM-MW2FN7MQ',
        'Shopify Google Tag: GT-NC6L8G55 (native integration)'
    ),
    # Pattern 4: "✅ INSTALLED (GTM-MW2FN7MQ)"
    (
        r'✅ INSTALLED \(GTM-MW2FN7MQ\)',
        '✅ Shopify Channel App (GT-NC6L8G55 - NATIVE)'
    ),
    # Pattern 5: "Container ID: GTM-MW2FN7MQ"
    (
        r'Container ID:.*GTM-MW2FN7MQ',
        'Google Tag ID: GT-NC6L8G55 (Shopify Channel App)'
    )
]

def fix_file(filepath):
    """Fix GTM references in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Apply all replacements
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                changes_made += len(re.findall(pattern, content, flags=re.IGNORECASE))
                content = new_content

        if changes_made > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        else:
            return False, 0

    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("FIXING INCORRECT GTM-MW2FN7MQ REFERENCES IN DOCUMENTATION")
    print("=" * 80)
    print()
    print("CORRECTION:")
    print("  ❌ INCORRECT: GTM-MW2FN7MQ (does not exist on Alpha Medical)")
    print("  ✅ CORRECT: GT-NC6L8G55 (Shopify Channel App - NATIVE integration)")
    print()
    print("=" * 80)
    print()

    total_changes = 0
    files_modified = 0

    for filepath in files_to_fix:
        filename = filepath.split('/')[-1]
        print(f"Processing: {filename}...", end=" ")

        success, result = fix_file(filepath)

        if success and result > 0:
            print(f"✅ Fixed {result} references")
            files_modified += 1
            total_changes += result
        elif success and result == 0:
            print("⚠️  No GTM-MW2FN7MQ references found")
        else:
            print(f"❌ Error: {result}")

    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Files modified: {files_modified}/{len(files_to_fix)}")
    print(f"✅ Total corrections: {total_changes}")
    print()
    print("DOCUMENTATION NOW REFLECTS FACTUAL REALITY:")
    print("  - Alpha Medical uses Shopify Channel App (native)")
    print("  - Tracking ID: GT-NC6L8G55 (Google Tag format)")
    print("  - NO Google Tag Manager container")
    print("  - NO Trakpilot (uninstalled)")
    print("  - NO Bundler.app (uninstalled)")
    print("=" * 80)

if __name__ == '__main__':
    main()
