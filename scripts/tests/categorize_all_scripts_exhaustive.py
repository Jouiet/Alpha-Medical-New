#!/usr/bin/env python3
"""
CATEGORISATION EXHAUSTIVE - TOUS LES SCRIPTS PYTHON
Catégorise tous les scripts par fonction et identifie ceux du flywheel ecosystem
Approche: Bottom-up factuelle (0% suppositions)
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Critères de catégorisation basés sur chemin + nom + patterns
CATEGORIES = {
    "FLYWHEEL_TRACKING": {
        "paths": ["analytics", "tracking", "gtm", "pixel", "ga4", "meta", "tiktok", "google_ads"],
        "names": ["track", "pixel", "gtm", "analytics", "ga4", "meta", "facebook", "tiktok", "google_ads", "conversion"],
        "description": "Acquisition measurement - Tracking & Analytics"
    },
    "FLYWHEEL_LEAD_GEN": {
        "paths": ["lead", "scraper", "apify", "typeform"],
        "names": ["lead", "scraper", "apify", "typeform", "form", "signup"],
        "description": "Acquisition - Lead Generation"
    },
    "FLYWHEEL_EMAIL": {
        "paths": ["email", "klaviyo", "shopify_email"],
        "names": ["email", "klaviyo", "campaign", "flow", "newsletter"],
        "description": "Retention - Email Automation"
    },
    "FLYWHEEL_LOYALTY": {
        "paths": ["loyalty"],
        "names": ["loyalty", "reward", "points", "tier"],
        "description": "Retention - Loyalty System"
    },
    "FLYWHEEL_BUNDLES": {
        "paths": ["bundles", "bundle"],
        "names": ["bundle", "fbt", "frequently_bought"],
        "description": "Conversion - Bundle Products"
    },
    "FLYWHEEL_SEO": {
        "paths": ["seo"],
        "names": ["seo", "meta", "schema", "sitemap", "robots"],
        "description": "Acquisition - SEO Optimization"
    },
    "FLYWHEEL_PRODUCTS": {
        "paths": ["products", "product"],
        "names": ["product", "variant", "inventory", "price", "collection"],
        "description": "Conversion - Product Management"
    },
    "FLYWHEEL_AUTOMATION": {
        "paths": ["workflow", "flow", "automation", "n8n"],
        "names": ["workflow", "flow", "automation", "n8n", "shopify_flow"],
        "description": "All stages - Workflow Automation"
    },
    "FLYWHEEL_CUSTOMER": {
        "paths": ["customer"],
        "names": ["customer", "segment", "cohort"],
        "description": "Retention - Customer Management"
    },
    "INFRASTRUCTURE_VERIFY": {
        "paths": ["verification", "verify", "check", "audit"],
        "names": ["verify", "check", "audit", "validate", "test"],
        "description": "Quality - Verification & Testing"
    },
    "INFRASTRUCTURE_SETUP": {
        "paths": ["setup", "configure", "install"],
        "names": ["setup", "configure", "install", "deploy"],
        "description": "Infrastructure - Setup & Configuration"
    },
    "INFRASTRUCTURE_FIX": {
        "paths": ["fix", "fixes", "maintenance"],
        "names": ["fix", "repair", "correct", "update"],
        "description": "Maintenance - Fixes & Updates"
    },
    "INFRASTRUCTURE_DEPLOY": {
        "paths": ["deployment", "deploy"],
        "names": ["deploy", "push", "upload", "create"],
        "description": "Infrastructure - Deployment"
    },
    "INFRASTRUCTURE_DATA": {
        "paths": ["data", "sync", "import", "export"],
        "names": ["sync", "import", "export", "sheet", "drive"],
        "description": "Data - Sync & Integration"
    },
    "ONE_TIME": {
        "paths": ["migration", "archive", "cleanup", "obsolete"],
        "names": ["migrate", "cleanup", "obsolete", "old", "legacy"],
        "description": "One-time - Migration & Cleanup"
    },
    "DOCUMENTATION": {
        "paths": ["generate", "llms"],
        "names": ["generate_llms", "documentation", "report"],
        "description": "Documentation - Generation & Reports"
    },
    "UNCATEGORIZED": {
        "paths": ["uncategorized"],
        "names": [],
        "description": "Uncategorized - Needs review"
    }
}

def categorize_script(script_path):
    """Catégorise un script basé sur son chemin et nom"""
    path_lower = script_path.lower()
    name_lower = Path(script_path).name.lower()

    matched_categories = []

    for category, criteria in CATEGORIES.items():
        # Check path patterns
        for path_pattern in criteria["paths"]:
            if path_pattern in path_lower:
                matched_categories.append(category)
                break

        # Check name patterns
        for name_pattern in criteria["names"]:
            if name_pattern in name_lower:
                matched_categories.append(category)
                break

    # If multiple matches, prioritize FLYWHEEL categories
    if matched_categories:
        flywheel_cats = [c for c in matched_categories if c.startswith("FLYWHEEL_")]
        if flywheel_cats:
            return flywheel_cats[0]
        return matched_categories[0]

    return "UNCATEGORIZED"

def is_flywheel_script(category):
    """Détermine si un script fait partie du flywheel ecosystem"""
    flywheel_categories = [
        "FLYWHEEL_TRACKING",
        "FLYWHEEL_LEAD_GEN",
        "FLYWHEEL_EMAIL",
        "FLYWHEEL_LOYALTY",
        "FLYWHEEL_BUNDLES",
        "FLYWHEEL_SEO",
        "FLYWHEEL_PRODUCTS",
        "FLYWHEEL_AUTOMATION",
        "FLYWHEEL_CUSTOMER"
    ]
    return category in flywheel_categories

def is_active_script(script_path):
    """Détermine si un script est actif (pas obsolète/archivé)"""
    path_lower = script_path.lower()

    # Scripts obsolètes/archivés
    obsolete_indicators = [
        "/archive/",
        "/old/",
        "/legacy/",
        "_old.py",
        "_backup.py",
        "_deprecated.py",
        "migrate_scripts",
        "identify_obsolete",
        "categorize_scripts.py"
    ]

    for indicator in obsolete_indicators:
        if indicator in path_lower:
            return False

    return True

def main():
    print("="*80)
    print("CATÉGORISATION EXHAUSTIVE - TOUS LES SCRIPTS PYTHON")
    print("="*80)
    print("Méthode: Bottom-up factuelle (analyse chemin + nom + patterns)")
    print()

    # Find all Python scripts
    scripts = []
    for root, dirs, files in os.walk("."):
        # Skip irrelevant directories
        dirs[:] = [d for d in dirs if d not in [".git", "node_modules", ".venv", "__pycache__"]]

        for file in files:
            if file.endswith(".py"):
                script_path = os.path.join(root, file)
                scripts.append(script_path)

    print(f"📊 TOTAL SCRIPTS TROUVÉS: {len(scripts)}\n")

    # Categorize all scripts
    categorized = defaultdict(list)

    for script in sorted(scripts):
        category = categorize_script(script)
        active = is_active_script(script)

        categorized[category].append({
            "path": script,
            "active": active,
            "is_flywheel": is_flywheel_script(category)
        })

    # Print summary by category
    print("="*80)
    print("RÉSUMÉ PAR CATÉGORIE")
    print("="*80)

    total_active = 0
    total_flywheel = 0
    total_flywheel_active = 0

    for category in sorted(CATEGORIES.keys()):
        scripts_in_cat = categorized.get(category, [])
        active_count = sum(1 for s in scripts_in_cat if s["active"])
        flywheel_count = sum(1 for s in scripts_in_cat if s["is_flywheel"])
        flywheel_active = sum(1 for s in scripts_in_cat if s["active"] and s["is_flywheel"])

        if scripts_in_cat:
            desc = CATEGORIES[category]["description"]
            emoji = "🔄" if category.startswith("FLYWHEEL_") else "🔧"

            print(f"\n{emoji} {category}")
            print(f"   {desc}")
            print(f"   Total: {len(scripts_in_cat)} | Active: {active_count} | Flywheel: {flywheel_count}")

            total_active += active_count
            total_flywheel += flywheel_count
            total_flywheel_active += flywheel_active

    # Flywheel ecosystem summary
    print("\n" + "="*80)
    print("RÉSUMÉ FLYWHEEL ECOSYSTEM")
    print("="*80)

    print(f"\n📊 SCRIPTS TOTAUX: {len(scripts)}")
    print(f"✅ SCRIPTS ACTIFS: {total_active} ({total_active/len(scripts)*100:.1f}%)")
    print(f"🔄 SCRIPTS FLYWHEEL TOTAL: {total_flywheel} ({total_flywheel/len(scripts)*100:.1f}%)")
    print(f"🎯 SCRIPTS FLYWHEEL ACTIFS: {total_flywheel_active} ({total_flywheel_active/len(scripts)*100:.1f}%)")

    # Detailed flywheel scripts list
    print("\n" + "="*80)
    print("SCRIPTS FLYWHEEL ACTIFS - LISTE EXHAUSTIVE")
    print("="*80)

    flywheel_active_scripts = []

    for category in sorted(CATEGORIES.keys()):
        if category.startswith("FLYWHEEL_"):
            scripts_in_cat = categorized.get(category, [])
            active_scripts = [s for s in scripts_in_cat if s["active"]]

            if active_scripts:
                print(f"\n{category} ({len(active_scripts)} scripts actifs):")
                for i, script in enumerate(active_scripts, 1):
                    print(f"  {i:2d}. {script['path']}")
                    flywheel_active_scripts.append(script['path'])

    # Verification scripts (critical for flywheel quality)
    verify_scripts = categorized.get("INFRASTRUCTURE_VERIFY", [])
    verify_active = [s for s in verify_scripts if s["active"]]

    print(f"\nINFRASTRUCTURE_VERIFY ({len(verify_active)} scripts actifs):")
    for i, script in enumerate(verify_active, 1):
        print(f"  {i:2d}. {script['path']}")
        flywheel_active_scripts.append(script['path'])

    # Setup scripts (critical for flywheel infrastructure)
    setup_scripts = categorized.get("INFRASTRUCTURE_SETUP", [])
    setup_active = [s for s in setup_scripts if s["active"]]

    print(f"\nINFRASTRUCTURE_SETUP ({len(setup_active)} scripts actifs):")
    for i, script in enumerate(setup_active, 1):
        print(f"  {i:2d}. {script['path']}")
        flywheel_active_scripts.append(script['path'])

    # Final count
    print("\n" + "="*80)
    print("CONCLUSION FACTUELLE")
    print("="*80)

    print(f"\n🎯 TOTAL SCRIPTS À TESTER (Flywheel Ecosystem):")
    print(f"   {len(flywheel_active_scripts)} scripts actifs")
    print(f"\n   Précédent audit: 26 scripts (7.6% du total)")
    print(f"   Audit exhaustif requis: {len(flywheel_active_scripts)} scripts ({len(flywheel_active_scripts)/len(scripts)*100:.1f}% du total)")

    # Save list to file
    output_file = "FLYWHEEL_SCRIPTS_EXHAUSTIVE_LIST.txt"
    with open(output_file, "w") as f:
        f.write("SCRIPTS FLYWHEEL ACTIFS - LISTE EXHAUSTIVE\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total scripts à tester: {len(flywheel_active_scripts)}\n")
        f.write(f"Date: {Path(__file__).stat().st_mtime}\n\n")

        for i, script in enumerate(sorted(flywheel_active_scripts), 1):
            f.write(f"{i:3d}. {script}\n")

    print(f"\n📄 Liste sauvegardée: {output_file}")

    return flywheel_active_scripts

if __name__ == "__main__":
    flywheel_scripts = main()
