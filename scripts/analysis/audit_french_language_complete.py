#!/usr/bin/env python3
"""
COMPLETE FRENCH LANGUAGE AUDIT - ALPHA MEDICAL
Date: 2025-12-06
Purpose: Identify ALL French text in codebase (Python, Liquid, JavaScript, Markdown)
Method: Pattern-based detection + common French keywords
Bullshit Level: 0% (empirical verification only)
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict

# French keywords to detect (common words that rarely appear in English)
FRENCH_KEYWORDS = [
    # Common French words
    r'\bde\b', r'\ble\b', r'\bla\b', r'\bdes\b', r'\bles\b', r'\bun\b', r'\bune\b',
    r'\bdu\b', r'\bau\b', r'\baux\b', r'\bpour\b', r'\bpar\b', r'\bavec\b',
    r'\bdans\b', r'\bsur\b', r'\bsous\b', r'\bentre\b', r'\bvers\b', r'\bchez\b',

    # French verbs (infinitive)
    r'\bêtre\b', r'\bavoir\b', r'\bfaire\b', r'\bdire\b', r'\baller\b', r'\bvoir\b',
    r'\bsavoir\b', r'\bpouvoir\b', r'\bvouloir\b', r'\bvenir\b', r'\bdevoir\b',

    # French specific characters/words
    r'é', r'è', r'ê', r'à', r'ù', r'ç', r'œ', r'\bqui\b', r'\bque\b', r'\bquoi\b',
    r'\bdont\b', r'\boù\b', r'\bsi\b', r'\bcomme\b', r'\bmais\b', r'\bcette\b',

    # Technical French terms
    r'\bVérification\b', r'\bAnalyse\b', r'\bRapport\b', r'\bConfiguration\b',
    r'\bDéploiement\b', r'\bMaintenance\b', r'\bOptimisation\b', r'\bCréation\b',
    r'\bMise\b', r'\bàjour\b', r'\bGestion\b', r'\bSystème\b', r'\bFichier\b',

    # Documentation French terms
    r'\bDernière\b', r'\bDate\b', r'\bMéthode\b', r'\bContexte\b', r'\bStatut\b',
    r'\bRésumé\b', r'\bObjectif\b', r'\bImpact\b', r'\bProblème\b', r'\bSolution\b',
]

# Directories to skip
SKIP_DIRS = {
    '.git', '__pycache__', 'node_modules', '.next', 'dist', 'build',
    'archive', '.claude', 'venv', 'env', '.env', 'temp', 'tmp'
}

# File extensions to audit
FILE_EXTENSIONS = {
    '.py': 'Python',
    '.liquid': 'Liquid Template',
    '.js': 'JavaScript',
    '.md': 'Markdown',
    '.html': 'HTML',
    '.css': 'CSS',
    '.json': 'JSON',
    '.txt': 'Text',
    '.sh': 'Shell Script',
}


def should_skip_directory(dir_path: str) -> bool:
    """Check if directory should be skipped."""
    parts = Path(dir_path).parts
    return any(skip_dir in parts for skip_dir in SKIP_DIRS)


def detect_french_in_line(line: str, line_number: int) -> List[Tuple[str, int]]:
    """
    Detect French keywords in a line.
    Returns list of (keyword, position) tuples.
    """
    matches = []
    for keyword_pattern in FRENCH_KEYWORDS:
        for match in re.finditer(keyword_pattern, line, re.IGNORECASE):
            matches.append((match.group(), match.start()))
    return matches


def audit_file(file_path: str) -> Dict:
    """
    Audit a single file for French text.
    Returns dict with findings.
    """
    findings = {
        'path': file_path,
        'type': Path(file_path).suffix,
        'french_lines': [],
        'total_lines': 0,
        'french_count': 0,
    }

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                findings['total_lines'] += 1

                # Detect French keywords
                matches = detect_french_in_line(line, line_num)

                if matches:
                    findings['french_lines'].append({
                        'line_number': line_num,
                        'content': line.strip()[:200],  # Limit line length
                        'matches': [m[0] for m in matches],
                    })
                    findings['french_count'] += len(matches)

    except Exception as e:
        findings['error'] = str(e)

    return findings


def scan_directory(root_dir: str) -> Dict[str, List[Dict]]:
    """
    Scan directory tree for files with French text.
    Returns dict organized by file type.
    """
    results = defaultdict(list)
    total_files = 0
    files_with_french = 0

    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if not should_skip_directory(os.path.join(root, d))]

        for file in files:
            file_path = os.path.join(root, file)
            file_ext = Path(file).suffix

            # Only audit specific file types
            if file_ext in FILE_EXTENSIONS:
                total_files += 1

                findings = audit_file(file_path)

                # Only include files with French text
                if findings['french_count'] > 0:
                    files_with_french += 1
                    file_type = FILE_EXTENSIONS.get(file_ext, 'Other')
                    results[file_type].append(findings)

                # Progress indicator
                if total_files % 100 == 0:
                    print(f"Scanned {total_files} files, found {files_with_french} with French text...")

    return dict(results), total_files, files_with_french


def generate_report(results: Dict[str, List[Dict]], total_files: int, files_with_french: int) -> str:
    """Generate comprehensive audit report."""

    report = []
    report.append("=" * 100)
    report.append("FRENCH LANGUAGE AUDIT - COMPLETE CODEBASE SCAN")
    report.append("=" * 100)
    report.append(f"Date: 2025-12-06")
    report.append(f"Total Files Scanned: {total_files}")
    report.append(f"Files with French Text: {files_with_french} ({files_with_french/total_files*100:.1f}%)")
    report.append("=" * 100)
    report.append("")

    # Summary by file type
    report.append("SUMMARY BY FILE TYPE")
    report.append("-" * 100)

    total_french_occurrences = 0
    for file_type, findings_list in sorted(results.items()):
        french_count = sum(f['french_count'] for f in findings_list)
        total_french_occurrences += french_count
        report.append(f"{file_type}: {len(findings_list)} files, {french_count} French occurrences")

    report.append("")
    report.append(f"TOTAL FRENCH OCCURRENCES: {total_french_occurrences}")
    report.append("=" * 100)
    report.append("")

    # Detailed findings by file type
    for file_type, findings_list in sorted(results.items()):
        report.append(f"\n{'=' * 100}")
        report.append(f"FILE TYPE: {file_type} ({len(findings_list)} files)")
        report.append("=" * 100)

        for finding in sorted(findings_list, key=lambda x: x['french_count'], reverse=True):
            report.append(f"\nFile: {finding['path']}")
            report.append(f"Total Lines: {finding['total_lines']}")
            report.append(f"French Occurrences: {finding['french_count']}")
            report.append(f"French Lines: {len(finding['french_lines'])}")
            report.append("")

            # Show first 10 French lines
            for french_line in finding['french_lines'][:10]:
                report.append(f"  Line {french_line['line_number']}: {french_line['content']}")
                report.append(f"    Matches: {', '.join(french_line['matches'])}")

            if len(finding['french_lines']) > 10:
                report.append(f"  ... and {len(finding['french_lines']) - 10} more lines with French text")

            report.append("")

    return "\n".join(report)


def main():
    """Main execution."""
    print("Starting French language audit...")
    print("This will scan ALL Python, Liquid, JavaScript, and Markdown files")
    print("")

    # Scan codebase
    root_dir = "/Users/mac/Desktop/Alpha-Medical"
    results, total_files, files_with_french = scan_directory(root_dir)

    # Generate report
    report = generate_report(results, total_files, files_with_french)

    # Save report
    output_file = "/Users/mac/Desktop/Alpha-Medical/FRENCH_LANGUAGE_AUDIT_2025-12-06.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print("")
    print(f"✅ Audit complete!")
    print(f"Total files scanned: {total_files}")
    print(f"Files with French text: {files_with_french}")
    print(f"Report saved to: {output_file}")
    print("")

    # Print summary
    print("SUMMARY BY FILE TYPE:")
    for file_type, findings_list in sorted(results.items()):
        french_count = sum(f['french_count'] for f in findings_list)
        print(f"  {file_type}: {len(findings_list)} files, {french_count} occurrences")


if __name__ == "__main__":
    main()
