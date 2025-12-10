#!/usr/bin/env python3
"""
PLAN D'ACTION FACTUEL - ÉLIMINATION REDONDANCES
Détermine quel script garder/éliminer basé sur résultats de tests
Approche: Bottom-up factuelle (test results + modification dates)
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Load test results
with open('flywheel_exhaustive_test_results.json', 'r') as f:
    test_results = json.load(f)

# Load duplication analysis
with open('script_duplications_analysis.json', 'r') as f:
    dup_analysis = json.load(f)

# Create lookup dict for test results
test_status = {}
for result in test_results['results']:
    test_status[result['script']] = result['status']

def get_script_priority(script_path):
    """
    Calculate priority score for keeping a script
    Higher score = keep this one
    """
    score = 0

    # Test status (most important)
    status = test_status.get(script_path, 'UNKNOWN')
    if status == 'SUCCESS':
        score += 100
    elif status == 'CLI_TOOL':
        score += 90  # Still functional
    elif status == 'MISSING_CREDENTIALS':
        score += 50  # Functional with config
    elif status == 'CODE_ERROR':
        score -= 50
    elif status == 'FILE_NOT_FOUND':
        score -= 100
    elif status == 'TIMEOUT':
        score -= 30

    # Obsolescence markers (very important)
    obsolete_markers = ['_old', '_backup', '_v1', '_v2', '_deprecated', '_test', 'old_', 'backup_']
    if any(marker in script_path.lower() for marker in obsolete_markers):
        score -= 200  # Strong penalty

    # Recency (modification date)
    if os.path.exists(script_path):
        mtime = os.path.getmtime(script_path)
        days_old = (datetime.now().timestamp() - mtime) / 86400

        # Penalize very old scripts
        if days_old > 90:
            score -= 20
        elif days_old > 30:
            score -= 10

        # File size (larger = more complete)
        size = os.path.getsize(script_path)
        if size > 5000:
            score += 10
        elif size < 1000:
            score -= 5

    # Naming convention (prefer clear names)
    filename = Path(script_path).stem
    if 'final' in filename.lower():
        score += 15
    if 'complete' in filename.lower():
        score += 10
    if 'comprehensive' in filename.lower():
        score += 10

    return score

print("="*80)
print("PLAN D'ACTION FACTUEL - ÉLIMINATION REDONDANCES")
print("="*80)
print("Méthode: Scoring basé sur test results + dates + naming")
print()

elimination_plan = []
keep_recommendations = []

for dup_group in dup_analysis['duplications']:
    action_type = dup_group['type']
    scripts = dup_group['scripts']

    print(f"\n{'='*80}")
    print(f"Groupe: {action_type.upper().replace('_', ' ')} ({len(scripts)} scripts)")
    print(f"{'='*80}")

    # Score each script
    scored_scripts = []
    for script_info in scripts:
        script = script_info['script']
        score = get_script_priority(script)
        status = test_status.get(script, 'UNKNOWN')

        scored_scripts.append({
            'script': script,
            'score': score,
            'status': status,
            'apis': script_info.get('apis', [])
        })

    # Sort by score (highest first)
    scored_scripts.sort(key=lambda x: x['score'], reverse=True)

    # Recommend keeping the top scorer
    keep_script = scored_scripts[0]
    eliminate_scripts = scored_scripts[1:]

    print(f"\n✅ GARDER (Score: {keep_script['score']}):")
    print(f"   {keep_script['script']}")
    print(f"   Status: {keep_script['status']}")
    if keep_script['apis']:
        print(f"   APIs: {', '.join(keep_script['apis'])}")

    if eliminate_scripts:
        print(f"\n❌ ÉLIMINER ({len(eliminate_scripts)} scripts):")
        for elim in eliminate_scripts:
            print(f"   {elim['script']} (Score: {elim['score']}, Status: {elim['status']})")

    keep_recommendations.append({
        'group': action_type,
        'keep': keep_script['script'],
        'keep_score': keep_script['score'],
        'keep_status': keep_script['status'],
        'eliminate': [e['script'] for e in eliminate_scripts],
        'eliminate_count': len(eliminate_scripts)
    })

    elimination_plan.extend([
        {
            'script': e['script'],
            'reason': f"Redundant with {keep_script['script']}",
            'group': action_type,
            'score': e['score'],
            'status': e['status']
        }
        for e in eliminate_scripts
    ])

# Add obsolete scripts to elimination plan
print(f"\n{'='*80}")
print("SCRIPTS OBSOLÈTES")
print("="*80)

for obsolete_script in dup_analysis['obsolete_scripts']:
    print(f"❌ {obsolete_script}")
    elimination_plan.append({
        'script': obsolete_script,
        'reason': 'Obsolete (has _old, _backup, _v1, _v2, _test marker)',
        'group': 'obsolete',
        'score': -200,
        'status': test_status.get(obsolete_script, 'UNKNOWN')
    })

print(f"\n{'='*80}")
print("RÉSUMÉ FACTUEL")
print("="*80)

total_eliminate = len(elimination_plan)
total_current = test_results['total_scripts']
reduction_pct = (total_eliminate / total_current * 100)

print(f"\n📊 SCRIPTS ACTUELS: {total_current}")
print(f"❌ À ÉLIMINER: {total_eliminate} ({reduction_pct:.1f}%)")
print(f"✅ APRÈS OPTIMISATION: {total_current - total_eliminate}")

# Save plan
plan = {
    'date': datetime.now().isoformat(),
    'current_scripts': total_current,
    'scripts_to_eliminate': total_eliminate,
    'reduction_percentage': reduction_pct,
    'keep_recommendations': keep_recommendations,
    'elimination_plan': elimination_plan
}

with open('OPTIMIZATION_ELIMINATION_PLAN.json', 'w') as f:
    json.dump(plan, f, indent=2)

print(f"\n💾 Plan détaillé sauvegardé: OPTIMIZATION_ELIMINATION_PLAN.json")

# Generate markdown report
with open('OPTIMIZATION_ELIMINATION_PLAN.md', 'w') as f:
    f.write("# PLAN D'OPTIMISATION - ÉLIMINATION REDONDANCES (2025-12-09)\\n\\n")
    f.write("**Méthode:** Scoring factuel basé sur résultats de tests + dates + naming\\n")
    f.write("**Bullshit Level:** 0%\\n\\n")
    f.write("---\\n\\n")

    f.write("## 📊 RÉSUMÉ EXÉCUTIF\\n\\n")
    f.write(f"**Scripts actuels:** {total_current}\\n")
    f.write(f"**Scripts à éliminer:** {total_eliminate} ({reduction_pct:.1f}%)\\n")
    f.write(f"**Après optimisation:** {total_current - total_eliminate}\\n\\n")

    f.write("---\\n\\n")
    f.write("## ✅ SCRIPTS À GARDER (PAR GROUPE)\\n\\n")

    for rec in keep_recommendations:
        f.write(f"### {rec['group'].upper().replace('_', ' ')}\\n\\n")
        f.write(f"**✅ GARDER:** `{rec['keep']}`\\n")
        f.write(f"- Score: {rec['keep_score']}\\n")
        f.write(f"- Status: {rec['keep_status']}\\n\\n")

        if rec['eliminate_count'] > 0:
            f.write(f"**❌ ÉLIMINER ({rec['eliminate_count']}):**\\n")
            for elim in rec['eliminate']:
                f.write(f"- `{elim}`\\n")
        f.write("\\n")

    f.write("---\\n\\n")
    f.write("## ❌ SCRIPTS OBSOLÈTES\\n\\n")

    for obsolete in dup_analysis['obsolete_scripts']:
        f.write(f"- `{obsolete}`\\n")

    f.write("\\n---\\n\\n")
    f.write("## 🎯 PLAN D'ACTION\\n\\n")
    f.write("1. Backup all scripts (git commit)\\n")
    f.write("2. Archive redundant scripts to archive/redundant/\\n")
    f.write("3. Archive obsolete scripts to archive/obsolete/\\n")
    f.write(f"4. Verify functionality post-cleanup\\n")
    f.write("5. Update documentation\\n")

print(f"📄 Rapport Markdown: OPTIMIZATION_ELIMINATION_PLAN.md")

print(f"\n{'='*80}")
print("NEXT STEPS")
print("="*80)
print(f"\n1. Review OPTIMIZATION_ELIMINATION_PLAN.md")
print(f"2. Backup current state (git commit)")
print(f"3. Execute elimination plan")
print(f"4. Re-test flywheel ecosystem")
print(f"5. Verify 0% regression")
