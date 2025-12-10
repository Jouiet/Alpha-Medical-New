#!/usr/bin/env python3
"""
ARCHIVAGE AUTOMATIQUE - SCRIPTS REDONDANTS
Archive 57 scripts redondants/obsolètes identifiés par analyse factuelle
Approche: Bottom-up sûre (0% regression)
"""

import json
import os
import shutil
from pathlib import Path
from datetime import datetime

# Load elimination plan
with open('OPTIMIZATION_ELIMINATION_PLAN.json', 'r') as f:
    plan = json.load(f)

print("="*80)
print("ARCHIVAGE AUTOMATIQUE - SCRIPTS REDONDANTS")
print("="*80)
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Méthode: Archive safe (preserve all scripts)")
print()

# Create archive directories
archive_base = "archive/optimization_2025-12-09"
archive_redundant = f"{archive_base}/redundant"
archive_obsolete = f"{archive_base}/obsolete"

os.makedirs(archive_redundant, exist_ok=True)
os.makedirs(archive_obsolete, exist_ok=True)

print(f"📁 Archive directories created:")
print(f"   {archive_redundant}")
print(f"   {archive_obsolete}")
print()

# Separate redundant vs obsolete
redundant_scripts = []
obsolete_scripts = []

for item in plan['elimination_plan']:
    script_path = item['script']
    if item['group'] == 'obsolete':
        obsolete_scripts.append(script_path)
    else:
        redundant_scripts.append(script_path)

print("="*80)
print(f"SCRIPTS À ARCHIVER: {len(plan['elimination_plan'])}")
print("="*80)
print(f"   Redondants: {len(redundant_scripts)}")
print(f"   Obsolètes: {len(obsolete_scripts)}")
print()

# Archive redundant scripts
print("="*80)
print("ARCHIVAGE SCRIPTS REDONDANTS")
print("="*80)

archived_count = 0
skipped_count = 0

for script in redundant_scripts:
    if not os.path.exists(script):
        print(f"⚠️  SKIP: {script} (not found)")
        skipped_count += 1
        continue

    # Preserve directory structure
    rel_path = script.lstrip('./')
    dest_path = os.path.join(archive_redundant, rel_path)

    # Create parent directories
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Move script
    shutil.move(script, dest_path)
    print(f"✅ {script} → {dest_path}")
    archived_count += 1

print(f"\n✅ Archived {archived_count}/{len(redundant_scripts)} redundant scripts")

# Archive obsolete scripts
print(f"\n{'='*80}")
print("ARCHIVAGE SCRIPTS OBSOLÈTES")
print("="*80)

obsolete_archived = 0
obsolete_skipped = 0

for script in obsolete_scripts:
    if not os.path.exists(script):
        print(f"⚠️  SKIP: {script} (not found)")
        obsolete_skipped += 1
        continue

    # Preserve directory structure
    rel_path = script.lstrip('./')
    dest_path = os.path.join(archive_obsolete, rel_path)

    # Create parent directories
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Move script
    shutil.move(script, dest_path)
    print(f"✅ {script} → {dest_path}")
    obsolete_archived += 1

print(f"\n✅ Archived {obsolete_archived}/{len(obsolete_scripts)} obsolete scripts")

# Summary
print(f"\n{'='*80}")
print("RÉSUMÉ ARCHIVAGE")
print("="*80)

total_archived = archived_count + obsolete_archived
total_skipped = skipped_count + obsolete_skipped

print(f"\n📊 SCRIPTS ARCHIVÉS: {total_archived}/{len(plan['elimination_plan'])}")
print(f"   Redondants: {archived_count}")
print(f"   Obsolètes: {obsolete_archived}")
print(f"   Skipped (not found): {total_skipped}")

print(f"\n📁 ARCHIVE LOCATION: {archive_base}/")

# Create restoration script
restore_script = f"{archive_base}/RESTORE.sh"
with open(restore_script, 'w') as f:
    f.write("#!/bin/bash\n")
    f.write("# RESTORATION SCRIPT - Restore archived scripts\n")
    f.write(f"# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    f.write("echo 'RESTORING ARCHIVED SCRIPTS...'\n\n")

    # Redundant scripts
    f.write("echo 'Restoring redundant scripts...'\n")
    for script in redundant_scripts:
        if os.path.exists(os.path.join(archive_redundant, script.lstrip('./'))):
            f.write(f"mv {archive_redundant}/{script.lstrip('./')} {script}\n")

    # Obsolete scripts
    f.write("\necho 'Restoring obsolete scripts...'\n")
    for script in obsolete_scripts:
        if os.path.exists(os.path.join(archive_obsolete, script.lstrip('./'))):
            f.write(f"mv {archive_obsolete}/{script.lstrip('./')} {script}\n")

    f.write("\necho 'RESTORATION COMPLETE'\n")

os.chmod(restore_script, 0o755)

print(f"🔄 Restoration script created: {restore_script}")

# Create manifest
manifest = {
    'date': datetime.now().isoformat(),
    'total_archived': total_archived,
    'redundant_archived': archived_count,
    'obsolete_archived': obsolete_archived,
    'skipped': total_skipped,
    'redundant_scripts': redundant_scripts,
    'obsolete_scripts': obsolete_scripts
}

manifest_path = f"{archive_base}/MANIFEST.json"
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"📄 Manifest created: {manifest_path}")

print(f"\n{'='*80}")
print("NEXT STEPS")
print("="*80)
print(f"\n1. Re-test flywheel ecosystem")
print(f"2. Verify 0% regression")
print(f"3. If OK: git commit")
print(f"4. If NOT OK: Run {restore_script}")

print(f"\n✅ ARCHIVAGE COMPLÉTÉ")
