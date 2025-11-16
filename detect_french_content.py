#!/usr/bin/env python3
"""
FRENCH CONTENT DETECTION SCRIPT
Purpose: Detect ALL French text in theme files (liquid, json)
Methodology: ONE script for ONE problem (French detection ONLY)
Author: Claude Code
Date: 2025-11-16
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

# French keywords to detect (unambiguous French words)
FRENCH_KEYWORDS = [
    # Common French words that are NOT English
    'livraison', 'gratuite', 'commandes', 'tous', 'toutes',
    'pour', 'sous', 'avec', 'sans', 'dans', 'sur',
    'prix', 'produit', 'produits', 'article', 'articles',
    'panier', 'ajouter', 'acheter', 'commander',
    'livré', 'expédition', 'délai', 'jours',
    'retour', 'retours', 'garantie', 'remboursement',
    'paiement', 'sécurisé', 'carte', 'crédit',
    'client', 'clients', 'service', 'contactez',
    'nous', 'notre', 'nos', 'votre', 'vos',
    'tout', 'tous', 'toute', 'toutes',
    'mais', 'très', 'plus', 'moins', 'aussi',
    'si', 'comment', 'pourquoi', 'quand',
    'bienvenue', 'merci', 'svp', 's\'il vous plaît',
    'et', 'ou', 'ni', 'car', 'donc',
    'de', 'du', 'des', 'le', 'la', 'les',
    'un', 'une', 'aux', 'au',
    'est', 'sont', 'a', 'ont', 'était',
    'ce', 'cette', 'ces', 'cet',
    'à', 'où', 'ça', 'là',
    'en', 'y', 'ne', 'pas',
    # Specific to e-commerce
    'avis', 'étoiles', 'note', 'notation',
    'taille', 'tailles', 'couleur', 'couleurs',
    'disponible', 'disponibles', 'stock',
    'nouveau', 'nouveaux', 'nouvelle', 'nouvelles',
    'meilleur', 'meilleurs', 'meilleure', 'meilleures',
    'offre', 'offres', 'promotion', 'promotions',
    'réduction', 'rabais', 'solde', 'soldes',
    'livraison', 'expédition', 'frais',
    'gratuit', 'gratuite', 'gratuites',
]

# Directories to scan (theme files only)
SCAN_DIRS = [
    'layout',
    'sections',
    'snippets',
    'templates',
    'assets',  # CSS/JS may contain French
]

# File extensions to scan
SCAN_EXTENSIONS = ['.liquid', '.json', '.css', '.js']

# Paths to exclude
EXCLUDE_PATTERNS = [
    'node_modules',
    '.git',
    'llms.txt',  # Documentation file, not customer-facing
    'llms-full.txt',
    '.md',  # Markdown docs are OK to have French
    '.py',  # Python scripts are OK
    'README',
]


def should_scan_file(file_path: str) -> bool:
    """Check if file should be scanned."""
    file_path_lower = file_path.lower()

    # Exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in file_path_lower:
            return False

    # Check extension
    ext = Path(file_path).suffix
    return ext in SCAN_EXTENSIONS


def detect_french_in_line(line: str, line_num: int) -> List[Tuple[str, int]]:
    """
    Detect French keywords in a line.
    Returns list of (keyword, position) tuples.
    """
    matches = []
    line_lower = line.lower()

    for keyword in FRENCH_KEYWORDS:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(keyword) + r'\b'
        for match in re.finditer(pattern, line_lower):
            matches.append((keyword, match.start()))

    return matches


def scan_file(file_path: str) -> Dict:
    """
    Scan a single file for French content.
    Returns dict with findings.
    """
    findings = {
        'file': file_path,
        'french_detected': False,
        'lines': [],
        'total_occurrences': 0,
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                # Skip comments
                if line.strip().startswith('//') or line.strip().startswith('#'):
                    continue
                if line.strip().startswith('/*') or line.strip().startswith('*'):
                    continue

                # Detect French
                matches = detect_french_in_line(line, line_num)
                if matches:
                    findings['french_detected'] = True
                    findings['total_occurrences'] += len(matches)
                    findings['lines'].append({
                        'line_num': line_num,
                        'content': line.rstrip(),
                        'keywords_found': [m[0] for m in matches],
                    })

    except Exception as e:
        findings['error'] = str(e)

    return findings


def scan_all_theme_files() -> List[Dict]:
    """
    Scan all theme files for French content.
    Returns list of findings.
    """
    base_path = Path('/Users/mac/Desktop/Alpha-Medical')
    all_findings = []

    for scan_dir in SCAN_DIRS:
        dir_path = base_path / scan_dir
        if not dir_path.exists():
            continue

        for file_path in dir_path.rglob('*'):
            if file_path.is_file() and should_scan_file(str(file_path)):
                findings = scan_file(str(file_path))
                if findings['french_detected']:
                    all_findings.append(findings)

    return all_findings


def generate_report(findings: List[Dict]) -> str:
    """Generate detailed forensic report."""
    report = []
    report.append("=" * 80)
    report.append("FRENCH CONTENT DETECTION - FORENSIC AUDIT REPORT")
    report.append("=" * 80)
    report.append("")
    report.append(f"Total files with French detected: {len(findings)}")
    report.append("")

    if not findings:
        report.append("✅ RESULT: 100% ENGLISH COMPLIANCE")
        report.append("")
        report.append("No French content detected in any theme files.")
        report.append("Site is 100% English only.")
    else:
        report.append("❌ RESULT: FRENCH CONTENT DETECTED")
        report.append("")
        report.append("VIOLATIONS:")
        report.append("-" * 80)

        for i, finding in enumerate(findings, start=1):
            report.append("")
            report.append(f"VIOLATION #{i}: {finding['file']}")
            report.append(f"Total occurrences: {finding['total_occurrences']}")
            report.append("")

            for line_info in finding['lines']:
                report.append(f"  Line {line_info['line_num']}:")
                report.append(f"    Content: {line_info['content']}")
                report.append(f"    French keywords: {', '.join(line_info['keywords_found'])}")
                report.append("")

    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    return "\n".join(report)


def main():
    """Main execution."""
    print("🔍 FRENCH CONTENT DETECTION - STARTING...")
    print("")
    print("Scanning theme files:")
    for scan_dir in SCAN_DIRS:
        print(f"  - {scan_dir}/")
    print("")

    # Scan all files
    findings = scan_all_theme_files()

    # Generate report
    report = generate_report(findings)

    # Print report
    print(report)

    # Save report to file
    report_file = '/Users/mac/Desktop/Alpha-Medical/french_detection_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print("")
    print(f"📄 Report saved to: {report_file}")

    # Save findings as JSON
    json_file = '/Users/mac/Desktop/Alpha-Medical/french_detection_findings.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)

    print(f"📊 Findings saved to: {json_file}")
    print("")

    # Exit code
    if findings:
        print("❌ FAILED: French content detected")
        return 1
    else:
        print("✅ SUCCESS: 100% English compliance")
        return 0


if __name__ == '__main__':
    exit(main())
