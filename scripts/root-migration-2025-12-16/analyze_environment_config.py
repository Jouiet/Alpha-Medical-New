#!/usr/bin/env python3
"""
Analyze .env Files Structure
Alpha Medical - P0-DAY3 Task
Date: 2025-12-05

Analyzes .env files to propose consolidation strategy WITHOUT exposing secrets.
"""

import re
from pathlib import Path
from collections import defaultdict

ENV_FILES = [
    '.env',
    '.env.admin',
    '.env.n8n',
    '.env.powerbi',
    '.env.tidio'
]

def analyze_env_file(filepath):
    """Analyze .env file structure (keys only, not values)."""
    if not Path(filepath).exists():
        return {'lines': 0, 'keys': [], 'comments': 0, 'empty': 0}

    with open(filepath, 'r') as f:
        lines = f.readlines()

    keys = []
    comments = 0
    empty = 0

    for line in lines:
        line = line.strip()
        if not line:
            empty += 1
        elif line.startswith('#'):
            comments += 1
        elif '=' in line:
            # Extract key (before =)
            key = line.split('=')[0].strip()
            keys.append(key)

    return {
        'lines': len(lines),
        'keys': keys,
        'comments': comments,
        'empty': empty
    }

def categorize_key(key):
    """Categorize environment variable by purpose."""
    key_lower = key.lower()

    if any(x in key_lower for x in ['shopify', 'shop_']):
        return 'SHOPIFY'
    if any(x in key_lower for x in ['klaviyo', 'klav']):
        return 'KLAVIYO'
    if any(x in key_lower for x in ['n8n', 'workflow']):
        return 'N8N'
    if any(x in key_lower for x in ['powerbi', 'power_bi', 'bi_']):
        return 'POWERBI'
    if any(x in key_lower for x in ['tidio', 'chat']):
        return 'TIDIO'
    if any(x in key_lower for x in ['google', 'gcp', 'sheets', 'drive']):
        return 'GOOGLE'
    if any(x in key_lower for x in ['facebook', 'meta', 'fb_']):
        return 'FACEBOOK'
    if any(x in key_lower for x in ['apify']):
        return 'APIFY'
    if any(x in key_lower for x in ['github', 'gh_']):
        return 'GITHUB'
    return 'OTHER'

def main():
    print("=" * 80)
    print(".ENV FILES ANALYSIS (Structure Only - No Secret Exposure)")
    print("=" * 80)
    print()

    # Analyze each file
    analyses = {}
    all_keys = set()
    key_sources = defaultdict(list)

    for env_file in ENV_FILES:
        analysis = analyze_env_file(env_file)
        analyses[env_file] = analysis

        for key in analysis['keys']:
            all_keys.add(key)
            key_sources[key].append(env_file)

    # Display file summaries
    print("FILE SUMMARIES:")
    print()
    for env_file in ENV_FILES:
        analysis = analyses[env_file]
        print(f"{env_file:20s}: {analysis['lines']:3d} lines, {len(analysis['keys']):2d} keys, {analysis['comments']:2d} comments")

    print()
    print("=" * 80)
    print("KEY DISTRIBUTION BY CATEGORY")
    print("=" * 80)
    print()

    # Group keys by category
    by_category = defaultdict(list)
    for key in sorted(all_keys):
        category = categorize_key(key)
        by_category[category].append(key)

    for category in sorted(by_category.keys()):
        keys = by_category[category]
        print(f"{category:15s}: {len(keys):2d} keys")
        for key in sorted(keys):
            sources = key_sources[key]
            source_str = ', '.join(sources) if len(sources) <= 2 else f"{sources[0]} +{len(sources)-1} more"
            print(f"  - {key:40s} (in: {source_str})")
        print()

    # Check for duplicates
    duplicates = {k: v for k, v in key_sources.items() if len(v) > 1}

    if duplicates:
        print("=" * 80)
        print(f"⚠️  DUPLICATE KEYS FOUND: {len(duplicates)} keys in multiple files")
        print("=" * 80)
        print()
        for key in sorted(duplicates.keys()):
            files = duplicates[key]
            print(f"  - {key:40s} → {', '.join(files)}")
        print()

    # Propose consolidated structure
    print("=" * 80)
    print("PROPOSED CONSOLIDATED STRUCTURE")
    print("=" * 80)
    print()
    print("Single file: .env.unified")
    print()
    print("# ========================================")
    print("# ALPHA MEDICAL - UNIFIED CONFIGURATION")
    print("# Last updated: 2025-12-05")
    print("# ========================================")
    print()

    for category in sorted(by_category.keys()):
        keys = by_category[category]
        print(f"# [{category}] ({len(keys)} keys)")
        for key in sorted(keys):
            sources = key_sources[key]
            if len(sources) > 1:
                print(f"{key}=<value>  # WARNING: Duplicate in {', '.join(sources)}")
            else:
                print(f"{key}=<value>  # From {sources[0]}")
        print()

    print("=" * 80)
    print("CONSOLIDATION STRATEGY")
    print("=" * 80)
    print()
    print("OPTION A: Single .env file (recommended)")
    print("  ✅ Pros: Simple, no confusion, single source of truth")
    print("  ⚠️  Cons: Large file, all secrets in one place")
    print()
    print("OPTION B: Multiple .env files by service")
    print("  .env.shopify  - Shopify store credentials")
    print("  .env.marketing - Klaviyo, Facebook, Google Ads")
    print("  .env.automation - N8N, GitHub Actions")
    print("  .env.analytics - PowerBI, Google Sheets")
    print("  .env.support - Tidio chat")
    print("  ✅ Pros: Logical separation, easier to manage per service")
    print("  ⚠️  Cons: Scripts need to load multiple files")
    print()
    print("OPTION C: Keep current structure")
    print("  ✅ Pros: No changes needed, already working")
    print("  ⚠️  Cons: 5 files, potential duplicates, harder to maintain")
    print()

    print("=" * 80)
    print("RECOMMENDATION: OPTION B (Multiple .env by service)")
    print("=" * 80)
    print()
    print("REASONING:")
    print("- Each service has distinct credentials")
    print("- Easier to rotate secrets per service")
    print("- Better security (limit exposure if one file compromised)")
    print("- Clearer organization for team members")
    print("- Scripts can load only what they need")
    print()

    print("NEXT STEPS:")
    print("1. Review key distribution above")
    print("2. Choose consolidation strategy")
    print("3. Create migration script if needed")
    print("4. Update scripts to use new structure")
    print()

if __name__ == "__main__":
    main()
