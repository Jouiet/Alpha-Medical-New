#!/usr/bin/env python3
"""
FIX ALL ALPHA MEDICAL BRAND COLORS
Corrects incorrect colors in all snippet files

Old colors (INCORRECT):
- #4A90E2 (light blue)
- #7FCCC9 (turquoise)
- #2c3e50 (gray-blue)
- #ff4444 (bright red)

New colors (ALPHA MEDICAL OFFICIAL):
- #4770db (Primary Blue)
- #0e1b4d (Deep Navy)
- #e32402 (Coral Red)
- #eff0f5 (Light Background)
"""

import re
import os
import glob

# Color mappings
COLOR_REPLACEMENTS = {
    # Primary blue replacements
    '#4A90E2': '#4770db',
    'rgba(74, 144, 226,': 'rgba(71, 112, 219,',
    'rgb(74, 144, 226)': 'rgb(71, 112, 219)',

    # Navy text replacements
    '#2c3e50': '#0e1b4d',

    # Turquoise to Navy gradient replacements
    '#7FCCC9': '#4770db',  # Second part of gradient becomes bright blue

    # Red badge replacements
    '#ff4444': '#e32402',

    # Background hover replacements
    '#f0f7ff': 'rgba(71, 112, 219, 0.1)',  # Old blue hover
    '#f8f9fa': '#eff0f5',  # Light gray to Alpha Medical light bg
}

# Special case: Gradients need to be Navy → Blue
GRADIENT_PATTERN = r'linear-gradient\(135deg,\s*#4A90E2\s+0%,\s*#7FCCC9\s+100%\)'
GRADIENT_REPLACEMENT = 'linear-gradient(135deg, #0e1b4d 0%, #4770db 100%)'

def fix_colors_in_file(filepath):
    """Fix all color references in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Fix gradients first (specific pattern)
        content = re.sub(GRADIENT_PATTERN, GRADIENT_REPLACEMENT, content)

        # Fix individual colors
        for old_color, new_color in COLOR_REPLACEMENTS.items():
            content = content.replace(old_color, new_color)

        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    except Exception as e:
        print(f"  ❌ Error processing {filepath}: {e}")
        return False

def main():
    print("=" * 80)
    print("FIXING ALL ALPHA MEDICAL BRAND COLORS")
    print("=" * 80)
    print()

    snippets_dir = '/Users/mac/Desktop/Alpha-Medical/snippets'
    pattern = os.path.join(snippets_dir, '*.liquid')
    snippet_files = glob.glob(pattern)

    print(f"Found {len(snippet_files)} snippet files")
    print()

    fixed_count = 0
    total_count = 0

    for filepath in snippet_files:
        filename = os.path.basename(filepath)

        # Check if file contains old colors
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        needs_fix = False
        for old_color in COLOR_REPLACEMENTS.keys():
            if old_color in content:
                needs_fix = True
                break

        if not needs_fix and '#4A90E2' not in content and '#7FCCC9' not in content:
            continue

        total_count += 1
        print(f"Processing: {filename}")

        if fix_colors_in_file(filepath):
            print(f"  ✅ Fixed colors in {filename}")
            fixed_count += 1
        else:
            print(f"  ℹ️  No changes needed in {filename}")

    print()
    print("=" * 80)
    print(f"COMPLETE: Fixed {fixed_count}/{total_count} files")
    print("=" * 80)
    print()
    print("COLOR CORRECTIONS APPLIED:")
    print("  ✅ #4A90E2 → #4770db (Primary Blue)")
    print("  ✅ #7FCCC9 → #4770db (in gradients)")
    print("  ✅ #2c3e50 → #0e1b4d (Deep Navy)")
    print("  ✅ #ff4444 → #e32402 (Coral Red)")
    print("  ✅ Gradients: #0e1b4d → #4770db (Navy to Blue)")
    print()

if __name__ == '__main__':
    main()
