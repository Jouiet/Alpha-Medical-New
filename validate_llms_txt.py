#!/usr/bin/env python3
"""
Alpha Medical - llms.txt Validator
Validates llms.txt and llms-full.txt against the official specification

Usage:
    python3 validate_llms_txt.py

Checks:
- File exists
- Valid markdown format
- Required H1 header present
- Link format correctness
- File references are valid
- Character encoding
- Size recommendations
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).parent

# Colors for terminal output
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'


class LLMSTxtValidator:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.content = ""
        self.lines = []
        self.errors = []
        self.warnings = []
        self.info = []

    def validate(self) -> bool:
        """Run all validation checks"""
        print(f"\n{BOLD}Validating: {self.file_path.name}{RESET}")
        print("=" * 60)

        # Check file exists
        if not self.file_path.exists():
            self.errors.append(f"File does not exist: {self.file_path}")
            return False

        # Read file
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
        except UnicodeDecodeError:
            self.errors.append("File is not valid UTF-8")
            return False
        except Exception as e:
            self.errors.append(f"Error reading file: {str(e)}")
            return False

        # Run checks
        self.check_required_h1()
        self.check_markdown_format()
        self.check_links()
        self.check_file_size()
        self.check_structure()

        # Print results
        self.print_results()

        return len(self.errors) == 0

    def check_required_h1(self):
        """Check if file has required H1 header"""
        h1_pattern = r'^# .+$'
        found_h1 = False

        for line in self.lines[:10]:  # Check first 10 lines
            if re.match(h1_pattern, line):
                found_h1 = True
                self.info.append(f"✓ H1 header found: {line}")
                break

        if not found_h1:
            self.errors.append("Missing required H1 header (# Project Name)")

    def check_markdown_format(self):
        """Check basic markdown syntax"""
        # Check for common markdown issues
        issues = []

        for i, line in enumerate(self.lines, 1):
            # Check for unescaped special characters in links
            if '[' in line and ']' in line:
                # Basic link format check
                link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
                matches = re.findall(link_pattern, line)

                for title, url in matches:
                    # Check for spaces in URLs (should be encoded)
                    if ' ' in url and not url.startswith('http'):
                        self.warnings.append(f"Line {i}: URL contains spaces: {url}")

        if not issues:
            self.info.append("✓ Basic markdown format OK")

    def check_links(self):
        """Validate all markdown links"""
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, self.content)

        total_links = len(links)
        valid_links = 0
        broken_links = 0

        for title, url in links:
            # Skip external URLs
            if url.startswith(('http://', 'https://', '#')):
                valid_links += 1
                continue

            # Check if referenced file exists
            referenced_file = PROJECT_ROOT / url

            if referenced_file.exists():
                valid_links += 1
            else:
                broken_links += 1
                self.warnings.append(f"Broken link: [{title}]({url}) - file not found")

        self.info.append(f"✓ Links: {total_links} total, {valid_links} valid, {broken_links} broken")

        if broken_links > 0:
            self.warnings.append(f"{broken_links} broken file references found")

    def check_file_size(self):
        """Check file size and estimate tokens"""
        size_bytes = len(self.content.encode('utf-8'))
        size_kb = size_bytes / 1024
        estimated_tokens = len(self.content) // 4  # Rough estimate

        self.info.append(f"✓ File size: {size_kb:.1f} KB ({size_bytes:,} bytes)")
        self.info.append(f"✓ Estimated tokens: ~{estimated_tokens:,}")

        # Size recommendations
        if self.file_path.name == 'llms.txt':
            if size_kb > 50:
                self.warnings.append(f"llms.txt is large ({size_kb:.1f} KB). Consider keeping it under 50 KB")
            if estimated_tokens > 10000:
                self.warnings.append(f"High token count ({estimated_tokens:,}). Consider using llms-full.txt for detailed content")

        if self.file_path.name == 'llms-full.txt':
            if estimated_tokens > 500000:
                self.warnings.append(f"Very large file ({estimated_tokens:,} tokens). May exceed most AI context windows")
            elif estimated_tokens > 200000:
                self.info.append("⚠️  Large file - requires models with extended context (Claude, GPT-4, Gemini 1.5)")

    def check_structure(self):
        """Check recommended structure"""
        has_blockquote = any(line.strip().startswith('>') for line in self.lines[:20])
        has_h2_sections = any(line.strip().startswith('## ') for line in self.lines)

        if has_blockquote:
            self.info.append("✓ Project description (blockquote) found")
        else:
            self.warnings.append("Consider adding a blockquote description after H1")

        if has_h2_sections:
            self.info.append("✓ Section headers (H2) found")
        else:
            self.warnings.append("Consider organizing content with H2 section headers")

    def print_results(self):
        """Print validation results"""
        print()

        # Info messages
        if self.info:
            for msg in self.info:
                print(f"{GREEN}{msg}{RESET}")

        # Warnings
        if self.warnings:
            print()
            for msg in self.warnings:
                print(f"{YELLOW}⚠️  {msg}{RESET}")

        # Errors
        if self.errors:
            print()
            for msg in self.errors:
                print(f"{RED}❌ {msg}{RESET}")

        # Summary
        print()
        print("=" * 60)
        if len(self.errors) == 0:
            if len(self.warnings) == 0:
                print(f"{GREEN}{BOLD}✅ VALIDATION PASSED - No errors or warnings{RESET}")
            else:
                print(f"{YELLOW}{BOLD}✅ VALIDATION PASSED - {len(self.warnings)} warnings{RESET}")
        else:
            print(f"{RED}{BOLD}❌ VALIDATION FAILED - {len(self.errors)} errors{RESET}")


def main():
    """Main validation function"""
    print(f"\n{BOLD}🔍 Alpha Medical - llms.txt Validator{RESET}")
    print("=" * 60)

    all_valid = True

    # Validate llms.txt
    llms_txt = PROJECT_ROOT / 'llms.txt'
    validator = LLMSTxtValidator(llms_txt)
    if not validator.validate():
        all_valid = False

    # Validate llms-full.txt if it exists
    llms_full = PROJECT_ROOT / 'llms-full.txt'
    if llms_full.exists():
        validator_full = LLMSTxtValidator(llms_full)
        if not validator_full.validate():
            all_valid = False

    # Final summary
    print(f"\n{BOLD}{'='*60}{RESET}")
    if all_valid:
        print(f"{GREEN}{BOLD}🎉 All validations passed!{RESET}")
        print(f"\n{GREEN}Your llms.txt files are ready for AI models.{RESET}")
    else:
        print(f"{RED}{BOLD}❌ Some validations failed{RESET}")
        print(f"\n{YELLOW}Please fix the errors above before deploying.{RESET}")

    print()
    return 0 if all_valid else 1


if __name__ == '__main__':
    exit(main())
