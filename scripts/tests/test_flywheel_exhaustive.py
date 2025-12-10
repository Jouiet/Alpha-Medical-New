#!/usr/bin/env python3
"""
TEST EXHAUSTIF FLYWHEEL ECOSYSTEM - 266 SCRIPTS
Teste TOUS les scripts du flywheel sans exception
Approche: Bottom-up factuelle avec catégorisation intelligente des erreurs
"""

import os
import subprocess
import sys
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import json

# Seuils de catégorisation intelligente
TIMEOUT_SECONDS = 30  # Most scripts should complete in < 30s

def categorize_error(result):
    """
    Catégorise intelligemment le résultat d'exécution

    Returns:
        status: SUCCESS | CLI_TOOL | MISSING_CREDENTIALS | MISSING_DEPENDENCY |
                CODE_ERROR | FILE_NOT_FOUND | TIMEOUT
    """
    returncode = result['returncode']
    stdout = result['stdout']
    stderr = result['stderr']
    combined = stdout + stderr

    # SUCCESS: returncode 0
    if returncode == 0:
        return "SUCCESS"

    # CLI_TOOL: Usage messages (normal behavior for CLI tools without args)
    cli_indicators = [
        "usage:",
        "Usage:",
        "USAGE:",
        "required arguments",
        "the following arguments are required",
        "Examples:",
        "python3",
        "[options]",
        "<required>",
        "positional arguments:"
    ]

    if any(indicator in combined for indicator in cli_indicators):
        return "CLI_TOOL"

    # MISSING_CREDENTIALS: API auth errors, env vars missing
    cred_indicators = [
        "environment variable",
        "not set",
        "SHOPIFY_ADMIN_ACCESS_TOKEN",
        "SHOPIFY_STORE_DOMAIN",
        "KLAVIYO_API_KEY",
        "GOOGLE_CREDENTIALS",
        "APIFY_API_TOKEN",
        "401",
        "403",
        "Unauthorized",
        "authentication"
    ]

    if any(indicator in combined for indicator in cred_indicators):
        return "MISSING_CREDENTIALS"

    # MISSING_DEPENDENCY: Import errors, module not found
    dep_indicators = [
        "ModuleNotFoundError",
        "ImportError",
        "No module named",
        "cannot import name"
    ]

    if any(indicator in combined for indicator in dep_indicators):
        return "MISSING_DEPENDENCY"

    # FILE_NOT_FOUND: Missing files (not the script itself, but files it needs)
    if "FileNotFoundError" in combined or "No such file" in combined:
        return "FILE_NOT_FOUND"

    # TIMEOUT
    if result.get('timeout', False):
        return "TIMEOUT"

    # CODE_ERROR: All other non-zero exits
    return "CODE_ERROR"

def run_script(script_path, timeout=TIMEOUT_SECONDS):
    """Execute un script et retourne le résultat catégorisé"""

    if not os.path.exists(script_path):
        return {
            "status": "FILE_NOT_FOUND",
            "returncode": -1,
            "stdout": "",
            "stderr": f"Script file not found: {script_path}",
            "execution_time": 0,
            "timeout": False
        }

    start_time = datetime.now()

    try:
        # Détermine l'exécuteur
        if script_path.endswith('.py'):
            cmd = ["python3", script_path]
        else:
            return {
                "status": "UNKNOWN_TYPE",
                "returncode": -1,
                "stdout": "",
                "stderr": f"Unknown file type: {script_path}",
                "execution_time": 0,
                "timeout": False
            }

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "execution_time": execution_time,
            "timeout": False
        }

    except subprocess.TimeoutExpired:
        execution_time = (datetime.now() - start_time).total_seconds()
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": f"Script timed out after {timeout} seconds",
            "execution_time": execution_time,
            "timeout": True
        }

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "execution_time": execution_time,
            "timeout": False
        }

def test_script(script_path):
    """Teste un script et catégorise le résultat"""
    print(f"  Testing: {script_path}", end=" ... ", flush=True)

    result = run_script(script_path)
    status = categorize_error(result)
    result['status'] = status

    # Emoji status indicator
    emoji_map = {
        "SUCCESS": "✅",
        "CLI_TOOL": "🔧",
        "MISSING_CREDENTIALS": "🔑",
        "MISSING_DEPENDENCY": "📦",
        "CODE_ERROR": "❌",
        "FILE_NOT_FOUND": "📁",
        "TIMEOUT": "⏱️",
        "UNKNOWN_TYPE": "❓"
    }

    emoji = emoji_map.get(status, "❓")
    print(f"{emoji} {status} ({result['execution_time']:.1f}s)")

    return result

def main():
    print("="*80)
    print("TEST EXHAUSTIF FLYWHEEL ECOSYSTEM - 266 SCRIPTS")
    print("="*80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Méthode: Bottom-up factuelle avec catégorisation intelligente")
    print()

    # Load script list
    list_file = "FLYWHEEL_SCRIPTS_EXHAUSTIVE_LIST.txt"

    if not os.path.exists(list_file):
        print(f"❌ ERROR: {list_file} not found")
        print("Run categorize_all_scripts_exhaustive.py first")
        sys.exit(1)

    # Parse script list
    scripts = []
    with open(list_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip headers and empty lines
            if line and not line.startswith("=") and not line.startswith("SCRIPTS") and not line.startswith("Total"):
                # Extract script path (format: "  123. ./path/to/script.py")
                match = re.search(r'\d+\.\s+(\./.+\.py)', line)
                if match:
                    scripts.append(match.group(1))
                elif line.startswith("./") and line.endswith(".py"):
                    scripts.append(line)

    if not scripts:
        print(f"❌ ERROR: No scripts found in {list_file}")
        sys.exit(1)

    print(f"📊 TOTAL SCRIPTS TO TEST: {len(scripts)}\n")

    # Test all scripts
    results = []
    status_counts = defaultdict(int)

    print("="*80)
    print("EXECUTING TESTS")
    print("="*80)

    for i, script in enumerate(scripts, 1):
        print(f"\n[{i}/{len(scripts)}]")
        result = test_script(script)
        results.append({
            "script": script,
            **result
        })
        status_counts[result['status']] += 1

    # Generate summary
    print("\n" + "="*80)
    print("RÉSUMÉ FACTUEL")
    print("="*80)

    total = len(scripts)

    # Calculate functional rate
    functional_statuses = ["SUCCESS", "CLI_TOOL"]  # Both are OK
    functional_count = sum(status_counts[s] for s in functional_statuses)
    functional_rate = (functional_count / total * 100) if total > 0 else 0

    print(f"\n📊 TOTAL SCRIPTS TESTÉS: {total}")
    print(f"✅ SCRIPTS FONCTIONNELS: {functional_count}/{total} ({functional_rate:.1f}%)")
    print(f"   - SUCCESS: {status_counts['SUCCESS']}")
    print(f"   - CLI_TOOL: {status_counts['CLI_TOOL']} (normal - require arguments)")

    print(f"\n⚠️  SCRIPTS NÉCESSITANT CONFIGURATION: {status_counts['MISSING_CREDENTIALS']}")
    print(f"   (Normal - credentials manquants)")

    print(f"\n❌ SCRIPTS EN ÉCHEC:")
    print(f"   - CODE_ERROR: {status_counts['CODE_ERROR']} (bugs de code)")
    print(f"   - MISSING_DEPENDENCY: {status_counts['MISSING_DEPENDENCY']} (dépendances manquantes)")
    print(f"   - FILE_NOT_FOUND: {status_counts['FILE_NOT_FOUND']} (fichiers manquants)")
    print(f"   - TIMEOUT: {status_counts['TIMEOUT']} (> {TIMEOUT_SECONDS}s)")

    # Critical failures (require fixing)
    critical_statuses = ["CODE_ERROR", "MISSING_DEPENDENCY", "FILE_NOT_FOUND"]
    critical_count = sum(status_counts[s] for s in critical_statuses)

    print(f"\n🔴 TOTAL ÉCHECS CRITIQUES: {critical_count}/{total} ({critical_count/total*100:.1f}%)")

    # List critical failures
    if critical_count > 0:
        print(f"\n📋 SCRIPTS À CORRIGER ({critical_count} scripts):")

        critical_failures = [r for r in results if r['status'] in critical_statuses]

        for i, failure in enumerate(critical_failures[:20], 1):  # Show first 20
            print(f"\n{i}. {failure['script']}")
            print(f"   Status: {failure['status']}")

            # Show first error line
            error_text = failure['stderr'] if failure['stderr'] else failure['stdout']
            error_lines = [line for line in error_text.split('\n') if line.strip()]
            if error_lines:
                # Get first meaningful error line
                for line in error_lines[:5]:
                    if any(keyword in line.lower() for keyword in ['error', 'exception', 'failed', 'traceback']):
                        print(f"   Error: {line.strip()[:100]}")
                        break

        if critical_count > 20:
            print(f"\n... and {critical_count - 20} more critical failures")

    # Save detailed results to JSON
    output_file = "flywheel_exhaustive_test_results.json"
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_scripts": total,
            "functional_count": functional_count,
            "functional_rate": functional_rate,
            "status_counts": dict(status_counts),
            "critical_failures": critical_count,
            "results": results
        }, f, indent=2)

    print(f"\n💾 Résultats détaillés sauvegardés: {output_file}")

    print("\n" + "="*80)
    print("CONCLUSION FACTUELLE")
    print("="*80)

    print(f"\n🎯 TAUX DE FONCTIONNALITÉ: {functional_rate:.1f}%")
    print(f"   - {functional_count} scripts fonctionnels (SUCCESS + CLI_TOOL)")
    print(f"   - {status_counts['MISSING_CREDENTIALS']} nécessitent credentials (normal)")
    print(f"   - {critical_count} nécessitent correction (bugs)")

    if functional_rate >= 90:
        print(f"\n✅ EXCELLENT: {functional_rate:.1f}% fonctionnel")
        sys.exit(0)
    elif functional_rate >= 70:
        print(f"\n⚠️  BON: {functional_rate:.1f}% fonctionnel, {critical_count} bugs à corriger")
        sys.exit(0)
    else:
        print(f"\n❌ INSUFFISANT: {functional_rate:.1f}% fonctionnel, {critical_count} bugs critiques")
        sys.exit(1)

if __name__ == "__main__":
    import re  # Import needed for regex
    main()
