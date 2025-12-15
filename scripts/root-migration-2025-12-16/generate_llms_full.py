#!/usr/bin/env python3
"""
Alpha Medical - llms-full.txt Generator
Generates a comprehensive llms-full.txt with complete content from all documentation files

Usage:
    python3 generate_llms_full.py

This creates llms-full.txt which includes:
- Full content of all documentation files
- Proper section dividers
- Table of contents
- Optimized for AI model context windows
"""

import os
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).parent

# Files to exclude
EXCLUDE_FILES = {
    'llms.txt',
    'llms-full.txt',
    'LLMS_TXT_README.md',
    'node_modules',
    '.git',
    '.claude',
}

# Priority documentation files (included first)
PRIORITY_FILES = [
    'SEO_MARKETING_FORENSIC_ANALYSIS.md',
    'IMPLEMENTATION_ROADMAP.md',
    'DYNAMIC_PRICING_MODEL.md',
    'README_PRICING.md',
]


def should_include_file(file_path: Path) -> bool:
    """Determine if a file should be included in llms-full.txt"""
    # Exclude specific files
    if any(exclude in str(file_path) for exclude in EXCLUDE_FILES):
        return False

    # Only include markdown files in root (not subdirectories for now)
    if file_path.suffix != '.md':
        return False

    # Exclude if in subdirectories we don't want
    try:
        relative = file_path.relative_to(PROJECT_ROOT)
        if len(relative.parts) > 1:
            return False
    except ValueError:
        return False

    return True


def read_markdown_file(file_path: Path) -> str:
    """Read markdown file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.strip()
    except Exception as e:
        return f"[Error reading {file_path.name}: {str(e)}]"


def generate_toc(files: List[Path]) -> str:
    """Generate table of contents"""
    toc = "## Table of Contents\n\n"

    for idx, file_path in enumerate(files, 1):
        filename = file_path.stem.replace('_', ' ').title()
        toc += f"{idx}. [{filename}](#{file_path.stem.lower()})\n"

    return toc


def generate_llms_full() -> str:
    """Generate complete llms-full.txt content"""

    # Header
    content = f"""# Alpha Medical Care - Complete Documentation

> This file contains the full content of all documentation files for Alpha Medical Care.
> For a quick index, see llms.txt instead.

**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
**Project:** Alpha Medical Care (https://alphamedical.shop/)
**Repository:** https://github.com/Jouiet/Alpha-Medical-New.git

---

"""

    # Collect all markdown files
    all_files = []

    # Add priority files first (if they exist)
    for priority_file in PRIORITY_FILES:
        file_path = PROJECT_ROOT / priority_file
        if file_path.exists() and should_include_file(file_path):
            all_files.append(file_path)

    # Add remaining files
    for md_file in sorted(PROJECT_ROOT.glob('*.md')):
        if should_include_file(md_file) and md_file not in all_files:
            all_files.append(md_file)

    # Generate TOC
    content += generate_toc(all_files)
    content += "\n---\n\n"

    # Add each file's content
    for idx, file_path in enumerate(all_files, 1):
        filename = file_path.stem.replace('_', ' ').title()

        content += f"\n\n# {idx}. {filename}\n\n"
        content += f"**File:** `{file_path.name}`\n"
        content += f"**Last Modified:** {datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}\n\n"
        content += "---\n\n"

        # Add file content
        file_content = read_markdown_file(file_path)
        content += file_content

        content += "\n\n---\n"

    # Footer
    content += f"""

---

## Document Information

**Total Documentation Files:** {len(all_files)}
**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
**Format:** llms-full.txt (Complete Content Version)
**Related:** See llms.txt for index-only version

**For AI Models:** This file contains the complete documentation for Alpha Medical Care.
Use llms.txt for quick navigation, or this file for comprehensive context.

**Project Status:** Production e-commerce store - handle with care
**Store URL:** https://alphamedical.shop/
"""

    return content


def main():
    """Main function"""
    print("📚 Alpha Medical - llms-full.txt Generator")
    print("=" * 60)
    print()

    print("📂 Scanning documentation files...")

    # Generate content
    content = generate_llms_full()

    # Write to file
    output_path = PROJECT_ROOT / 'llms-full.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    file_size_kb = len(content) / 1024

    print(f"✅ llms-full.txt generated successfully!")
    print(f"📍 Location: {output_path}")
    print(f"📊 Size: {file_size_kb:.1f} KB ({len(content):,} characters)")
    print()

    # Token estimate (rough: 1 token ≈ 4 characters)
    estimated_tokens = len(content) // 4
    print(f"🤖 Estimated tokens: ~{estimated_tokens:,}")

    if estimated_tokens > 100000:
        print("⚠️  WARNING: File may exceed typical AI model context windows")
        print("   Consider using llms.txt (index only) instead")
    elif estimated_tokens > 50000:
        print("⚠️  Large file - may require models with extended context")
    else:
        print("✅ File size appropriate for most AI model context windows")

    print()
    print("💡 Usage:")
    print("   - Use llms.txt for quick navigation (index only)")
    print("   - Use llms-full.txt for complete documentation in one file")
    print()


if __name__ == '__main__':
    main()
