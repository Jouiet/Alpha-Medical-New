#!/usr/bin/env python3
"""
FRENCH CONTENT DETECTION SCRIPT V2 - UNAMBIGUOUS FRENCH ONLY
Purpose: Detect ONLY unambiguous French text (no false positives)
Methodology: ONE script for ONE problem (French detection ONLY)
Author: Claude Code
Date: 2025-11-16
Version: 2.0
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple

# UNAMBIGUOUS French phrases (multi-word = more accurate)
FRENCH_PHRASES = [
    # Shipping/Delivery
    'livraison gratuite',
    'frais de livraison',
    'livraison offerte',
    'livré sous',
    'délai de livraison',
    'expédition gratuite',

    # Orders/Cart
    'votre panier',
    'mon panier',
    'ajouter au panier',
    'passer commande',
    'vos commandes',
    'mes commandes',
    'commande en cours',

    # Products
    'nos produits',
    'tous nos produits',
    'voir tous les produits',
    'en stock',
    'rupture de stock',
    'disponible sous',

    # Customer service
    'service client',
    'contactez-nous',
    'nous contacter',
    'besoin d\'aide',

    # Payment/Pricing
    'prix total',
    'prix ttc',
    'paiement sécurisé',
    'mode de paiement',
    'moyens de paiement',

    # Returns/Guarantee
    'politique de retour',
    'satisfait ou remboursé',
    'garantie satisfait',
    'retour gratuit',

    # Common French sentences
    'bienvenue sur',
    'merci pour votre',
    'n\'hésitez pas',
    's\'il vous plaît',
    'veuillez',
]

# UNAMBIGUOUS single French words (NOT English homophones)
FRENCH_KEYWORDS = [
    # Accented words (definitely French)
    'français', 'française', 'européen', 'européenne',
    'qualité', 'sécurisé', 'sécurisée', 'livré', 'livrée',
    'créé', 'créée', 'déjà', 'où', 'là',
    'été', 'année', 'après', 'grâce',

    # Shipping/Delivery
    'livraison', 'expédition', 'livré', 'expédié',

    # Cart/Order
    'panier', 'commandes', 'commander',

    # French pronouns (very specific)
    'nous', 'vous', 'votre', 'vos', 'notre', 'nos',
    'leur', 'leurs',

    # French verbs (specific forms)
    'ajouter', 'acheter', 'choisir', 'découvrir',
    'contactez', 'veuillez', 'merci', 'bienvenue',

    # French articles/prepositions (in specific contexts)
    'avec', 'sans', 'sous', 'sur', 'dans',
    'tout', 'tous', 'toute', 'toutes',
    'pour', 'mais', 'donc', 'car',

    # French quantifiers
    'plusieurs', 'quelques', 'chaque', 'aucun', 'aucune',

    # E-commerce French
    'gratuite', 'gratuit', 'offert', 'offerte',
    'disponible', 'disponibles',
    'taille', 'tailles', 'couleur', 'couleurs',
    'retour', 'retours', 'échange', 'échanges',
    'soldes', 'promotion', 'réduction', 'rabais',
]

# Directories to scan (theme files only)
SCAN_DIRS = [
    'layout',
    'sections',
    'snippets',
    'templates',
]

# File extensions to scan (only customer-facing files)
SCAN_EXTENSIONS = ['.liquid', '.json']

# Paths to exclude
EXCLUDE_PATTERNS = [
    'node_modules',
    '.git',
    'llms.txt',
    'llms-full.txt',
    '.md',
    '.py',
    'README',
    '.css',  # CSS classes with "article", "note" etc are OK
    '.js',   # JS variables are OK
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


def clean_line_for_detection(line: str) -> str:
    """
    Remove Liquid syntax and HTML tags to avoid false positives.
    """
    # Remove Liquid comments
    line = re.sub(r'{%\s*comment\s*%}.*?{%\s*endcomment\s*%}', '', line, flags=re.IGNORECASE)

    # Remove Liquid tags
    line = re.sub(r'{%.*?%}', '', line)
    line = re.sub(r'{{.*?}}', '', line)

    # Remove HTML tags
    line = re.sub(r'<[^>]+>', '', line)

    # Remove CSS selectors like .article, #note, etc
    line = re.sub(r'[\.#][a-zA-Z0-9_-]+', '', line)

    # Remove JavaScript variable names (const x, let y, var z)
    line = re.sub(r'\b(const|let|var)\s+[a-zA-Z0-9_]+\b', '', line)

    return line


def detect_french_phrases(text: str) -> List[str]:
    """Detect French phrases in text."""
    matches = []
    text_lower = text.lower()

    for phrase in FRENCH_PHRASES:
        if phrase in text_lower:
            matches.append(phrase)

    return matches


def detect_french_keywords(text: str) -> List[str]:
    """Detect French keywords in text."""
    matches = []
    text_lower = text.lower()

    for keyword in FRENCH_KEYWORDS:
        # Use word boundaries
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text_lower):
            matches.append(keyword)

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
                # Skip pure comments
                if line.strip().startswith('//') or line.strip().startswith('#'):
                    continue

                # Clean line
                cleaned_line = clean_line_for_detection(line)

                # Detect French phrases (higher priority)
                phrase_matches = detect_french_phrases(cleaned_line)

                # Detect French keywords
                keyword_matches = detect_french_keywords(cleaned_line)

                # Combine matches
                all_matches = phrase_matches + keyword_matches

                if all_matches:
                    findings['french_detected'] = True
                    findings['total_occurrences'] += len(all_matches)
                    findings['lines'].append({
                        'line_num': line_num,
                        'content': line.rstrip(),
                        'french_found': list(set(all_matches)),  # Remove duplicates
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
    report.append("FRENCH CONTENT DETECTION V2 - UNAMBIGUOUS FRENCH ONLY")
    report.append("FORENSIC AUDIT REPORT")
    report.append("=" * 80)
    report.append("")
    report.append(f"Total files with French detected: {len(findings)}")
    report.append("")

    if not findings:
        report.append("✅ RESULT: 100% ENGLISH COMPLIANCE")
        report.append("")
        report.append("No French content detected in customer-facing theme files.")
        report.append("Site is 100% English only.")
    else:
        report.append("❌ RESULT: FRENCH CONTENT DETECTED")
        report.append("")
        report.append("VIOLATIONS (REAL FRENCH CONTENT):")
        report.append("-" * 80)

        for i, finding in enumerate(findings, start=1):
            report.append("")
            report.append(f"VIOLATION #{i}: {finding['file']}")
            report.append(f"Total occurrences: {finding['total_occurrences']}")
            report.append("")

            for line_info in finding['lines']:
                report.append(f"  Line {line_info['line_num']}:")
                report.append(f"    Content: {line_info['content']}")
                report.append(f"    French detected: {', '.join(line_info['french_found'])}")
                report.append("")

    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)

    return "\n".join(report)


def main():
    """Main execution."""
    print("🔍 FRENCH CONTENT DETECTION V2 - UNAMBIGUOUS FRENCH ONLY")
    print("")
    print("Scanning customer-facing theme files (.liquid, .json):")
    for scan_dir in SCAN_DIRS:
        print(f"  - {scan_dir}/")
    print("")
    print("Filtering out:")
    print("  - Liquid syntax ({% comment %}, {{ ... }})")
    print("  - HTML tags (<a>, <div>, etc.)")
    print("  - CSS classes (.article, .note, etc.)")
    print("  - English homophones (articles, note, a, plus, etc.)")
    print("")

    # Scan all files
    findings = scan_all_theme_files()

    # Generate report
    report = generate_report(findings)

    # Print report
    print(report)

    # Save report to file
    report_file = '/Users/mac/Desktop/Alpha-Medical/french_detection_v2_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print("")
    print(f"📄 Report saved to: {report_file}")

    # Save findings as JSON
    json_file = '/Users/mac/Desktop/Alpha-Medical/french_detection_v2_findings.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)

    print(f"📊 Findings saved to: {json_file}")
    print("")

    # Exit code
    if findings:
        print(f"❌ FAILED: {len(findings)} file(s) with French content")
        return 1
    else:
        print("✅ SUCCESS: 100% English compliance")
        return 0


if __name__ == '__main__':
    exit(main())
