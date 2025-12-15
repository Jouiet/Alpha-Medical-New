#!/usr/bin/env python3
"""
Alpha Medical - llms.txt Generator
Automatically generates and updates llms.txt file for AI model guidance

Usage:
    python3 generate_llms_txt.py

This script:
- Scans all markdown files in the project
- Categorizes them automatically
- Generates a well-structured llms.txt file
- Preserves manual customizations in the header
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Files to exclude from documentation
EXCLUDE_FILES = {
    'llms.txt',
    'llms-full.txt',
    'node_modules',
    '.git',
    '.claude',
}

# Category mappings based on file name patterns
CATEGORIES = {
    'SEO & Marketing': [
        'SEO', 'MARKETING', 'AUDIT', 'FORENSIC', 'ANALYSIS'
    ],
    'Pricing & Product Management': [
        'PRICING', 'DYNAMIC', 'DSERS', 'PRODUCT', 'OPTIMIZATION'
    ],
    'Email Marketing & Automation': [
        'KLAVIYO', 'EMAIL', 'ABANDONED', 'CART', 'CHAT', 'AUTOMATION'
    ],
    'Content & Blog': [
        'CONTENT', 'BLOG', 'CALENDAR', 'GUIDE', 'ARTICLE', 'PAIN_RELIEF'
    ],
    'Implementation & Configuration': [
        'IMPLEMENTATION', 'CONFIGURATION', 'SETUP', 'CONFIG', 'SHOPIFY', 'MANUAL'
    ],
    'Forensic Analysis & Reports': [
        'FORENSIC', 'REPORT', 'VERIFICATION', 'COLLECTION', 'OVERLAP'
    ],
}


def extract_description(file_path: Path) -> str:
    """Extract a description from the first few lines of a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            # Look for the first non-header, non-empty line
            description_lines = []
            in_frontmatter = False

            for line in lines[:50]:  # Check first 50 lines
                stripped = line.strip()

                # Skip frontmatter
                if stripped == '---':
                    in_frontmatter = not in_frontmatter
                    continue
                if in_frontmatter:
                    continue

                # Skip headers
                if stripped.startswith('#'):
                    continue

                # Skip empty lines
                if not stripped:
                    continue

                # Skip markdown lists/bullets at the start
                if stripped.startswith(('-', '*', '>', '```', '|')):
                    continue

                # Found a good description line
                description_lines.append(stripped)

                # If we have enough content, stop
                if len(' '.join(description_lines)) > 80:
                    break

            description = ' '.join(description_lines)

            # Clean up and truncate
            description = re.sub(r'\s+', ' ', description)
            description = re.sub(r'[*_`]', '', description)  # Remove markdown formatting

            if len(description) > 150:
                description = description[:147] + '...'

            return description if description else "Project documentation"

    except Exception as e:
        return f"Documentation file (error reading: {str(e)[:30]})"


def categorize_file(filename: str) -> str:
    """Categorize a file based on its name."""
    filename_upper = filename.upper()

    # Check each category
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in filename_upper:
                return category

    # Default category
    return 'Optional Resources'


def scan_markdown_files() -> Dict[str, List[Tuple[str, str, str]]]:
    """Scan project for markdown files and categorize them."""
    files_by_category: Dict[str, List[Tuple[str, str, str]]] = {}

    # Initialize all categories
    for category in CATEGORIES.keys():
        files_by_category[category] = []
    files_by_category['Optional Resources'] = []

    # Scan all .md files
    for md_file in PROJECT_ROOT.rglob('*.md'):
        # Skip excluded files/directories
        if any(exclude in str(md_file) for exclude in EXCLUDE_FILES):
            continue

        # Get relative path
        try:
            relative_path = md_file.relative_to(PROJECT_ROOT)
        except ValueError:
            continue

        # Skip if in subdirectories we don't want
        if len(relative_path.parts) > 1 and relative_path.parts[0] in {'node_modules', '.git', 'vendor'}:
            continue

        filename = md_file.name
        description = extract_description(md_file)
        category = categorize_file(filename)

        files_by_category[category].append((filename, str(relative_path), description))

    # Sort files within each category
    for category in files_by_category:
        files_by_category[category].sort(key=lambda x: x[0])

    return files_by_category


def generate_llms_txt() -> str:
    """Generate the complete llms.txt content."""

    # Scan files
    files_by_category = scan_markdown_files()

    # Build the content
    content = f"""# Alpha Medical Care

> Professional medical support equipment & orthopedic braces e-commerce platform. Shopify-based store specializing in pain relief, posture support, and therapy wellness products with advanced SEO, automation, and conversion optimization.

## Project Overview

Alpha Medical Care (https://alphamedical.shop/) is a comprehensive medical equipment e-commerce platform built on Shopify, featuring 148 active products across 3 main collections, with integrated marketing automation, dynamic pricing, and SEO optimization.

**Tech Stack:** Shopify, Liquid templating, Python automation scripts, Klaviyo email flows, Loox reviews, DSers dropshipping integration

**Last Updated:** {datetime.now().strftime('%B %d, %Y')}

## Core Documentation

"""

    # Add each category
    main_categories = [
        'SEO & Marketing',
        'Pricing & Product Management',
        'Email Marketing & Automation',
        'Content & Blog',
        'Implementation & Configuration',
        'Forensic Analysis & Reports'
    ]

    for category in main_categories:
        if files_by_category[category]:
            content += f"### {category}\n\n"

            for filename, filepath, description in files_by_category[category]:
                content += f"- [{filename.replace('.md', '')}]({filepath}): {description}\n"

            content += "\n"

    # Add static sections
    content += """## Theme Structure

### Liquid Templates

- `/sections/`: Shopify theme sections (slideshow, product grids, collection banners, etc.)
- `/snippets/`: Reusable Liquid components (breadcrumbs, social proof, trust badges, schema markup)
- `/layout/`: Base theme layout files (theme.liquid with meta tags and structured data)
- `/templates/`: Page templates (product, collection, article, page templates)

### Configuration Files

- `/config/`: Theme settings and configuration JSON files
- `/locales/`: Multi-language translation files

## Automation Scripts

All Python scripts located in project root for Shopify API automation:

- `configure_klaviyo.py`: Klaviyo integration setup
- `configure_shopify_email.py`: Shopify email automation configuration
- `configure_reconvert.py`: ReConvert upsell/cross-sell setup
- `configure_fbt_bundles.py`: Frequently Bought Together bundle configuration
- `create_blog_article_*.py`: Automated blog post creation and publishing
- `create_pain_relief_guide_page.py`: Custom page creation for content hubs
- `optimize_seo.py`: Bulk SEO optimization for products and collections

## HTML Content Templates

Pre-written HTML content for Shopify pages (all `.html` files in root):

- `CONTENT_FAQ.html`, `CONTENT_HELP_CENTER.html`, `CONTENT_HOW_TO_USE.html`
- `CONTENT_SHIPPING.html`, `CONTENT_RETURNS.html`, `CONTENT_WARRANTY.html`
- `CONTENT_MEDICAL_DISCLAIMER.html`, `CONTENT_CUSTOMER_REVIEWS.html`

## Key Features

### SEO & Structured Data
- BreadcrumbList schema implementation
- Product schema with reviews and ratings
- FAQ schema markup
- Meta descriptions for all collections
- H1 tag optimization across all page types

### Conversion Optimization
- Loox social proof reviews system
- Trust badges and security seals
- Urgency and scarcity indicators (ethical, inventory-based only)
- Collection-based product recommendations
- Abandoned cart recovery (Klaviyo + Shopify Email)

### Analytics Integration
- Microsoft Clarity (app: tq8st6pt37)
- Google Analytics 4 (via Conversios + SST)
- Facebook Pixel + TikTok Pixel (via Infinite app)
- Server-side tracking (SST) enabled

## Product Collections

1. **Pain Relief & Recovery**: Pain management devices and recovery equipment
2. **Posture & Support**: Orthopedic posture correctors and back support braces
3. **Therapy & Wellness**: Professional therapy devices and wellness equipment
4. **Bestsellers**: Most popular medical support products
5. **New Arrivals**: Latest additions to product catalog

## Development Workflow

### Git Repository
- **Repo**: https://github.com/Jouiet/Alpha-Medical-New.git
- **Current Branch**: main
- **Shopify CLI**: Used for theme development and deployment

### Deployment Process
```bash
# Development testing
shopify theme dev

# Preview deployment
shopify theme push --unpublished

# Production deployment
shopify theme push --live
```

### Environment Variables
- `.env.admin`: Shopify Admin API access token (gitignored)
- `.env`: General environment configuration (gitignored)

## AI Model Guidance

When assisting with this project:

1. **SEO**: Always check SEO_MARKETING_FORENSIC_ANALYSIS.md for current implementation status before suggesting changes
2. **Pricing**: Use DYNAMIC_PRICING_MODEL.md for all pricing calculations - 6-tier system with specific formulas
3. **Email Automation**: Reference Klaviyo implementation docs for flow configuration and timing
4. **Code Changes**: Follow Liquid best practices, maintain existing schema markup patterns
5. **Content Creation**: Align with Content Calendar Q1 2026 for blog topics and SEO strategy
6. **Product Data**: All product operations should respect the pricing tiers and DSers integration
7. **Testing**: Always recommend preview deployment before live push
8. **Analytics**: Verify tracking implementation before changes (Clarity, GA4, FB/TikTok pixels)

"""

    # Add optional resources
    if files_by_category['Optional Resources']:
        content += "## Optional Resources\n\n"
        for filename, filepath, description in files_by_category['Optional Resources']:
            content += f"- [{filename.replace('.md', '')}]({filepath}): {description}\n"
        content += "\n"

    # Footer
    content += """---

**For AI Models**: This is a production Shopify store. Always prioritize data integrity, test changes in preview mode, and maintain existing SEO implementations. The site has active customers and should be treated as a live e-commerce platform.

**Store URL**: https://alphamedical.shop/
**Admin Access**: https://azffej-as.myshopify.com/admin
**Last Site Audit**: October 15, 2025
**llms.txt Generated**: {datetime.now().strftime('%B %d, %Y at %H:%M UTC')}
"""

    return content


def main():
    """Main function to generate llms.txt file."""
    print("🤖 Alpha Medical - llms.txt Generator")
    print("=" * 50)
    print()

    print("📂 Scanning markdown files...")
    files_by_category = scan_markdown_files()

    total_files = sum(len(files) for files in files_by_category.values())
    print(f"✅ Found {total_files} documentation files")
    print()

    print("📝 Generating llms.txt content...")
    content = generate_llms_txt()

    # Write to file
    output_path = PROJECT_ROOT / 'llms.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ llms.txt generated successfully!")
    print(f"📍 Location: {output_path}")
    print(f"📊 Total size: {len(content)} characters")
    print()

    print("📋 Files by category:")
    for category, files in files_by_category.items():
        if files:
            print(f"  - {category}: {len(files)} files")
    print()

    print("🎉 Done! Your llms.txt is ready for AI models.")
    print()
    print("💡 Tip: Run this script whenever you add new documentation files")
    print("   to keep llms.txt up to date.")


if __name__ == '__main__':
    main()
