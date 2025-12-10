#!/usr/bin/env python3
"""
TEST COMPLET ÉCOSYSTÈME FLYWHEEL - VÉRIFICATION EMPIRIQUE
Teste TOUS les scripts critiques du flywheel de manière factuelle
Approche: Exécuter → Vérifier → Documenter → Corriger → Itérer
"""

import os
import subprocess
import sys
from datetime import datetime
from collections import defaultdict

# Scripts critiques par catégorie flywheel
FLYWHEEL_SCRIPTS = {
    "TRACKING_ANALYTICS": [
        "scripts/analysis/checks/check_gtm_status.py",
        "scripts/analysis/checks/check_theme_pixels.py",
        "scripts/analysis/verification/verify_google_tags_live.py",
        "scripts/analysis/verification/verify_shopify_pixels.py",
        "scripts/analytics/extract_alpha_tracking_ids.py",
    ],
    "LEAD_GENERATION": [
        "market-analysis/lead_generation_scraper.py",
        "market-analysis/sync_leads_to_sheets.py",
        "sync_shopify_forms_to_sheet.py",
        "sync_klaviyo_to_sheet.py",
        "sync_facebook_leads_to_sheet.py",
    ],
    "EMAIL_AUTOMATION": [
        "market-analysis/verify_klaviyo_status.py",
        "scripts/analysis/verify_klaviyo_flows_live.py",
        "scripts/tests/test_klaviyo_api.py",
        "scripts/setup/configure_shopify_email.py",
    ],
    "LOYALTY_SYSTEM": [
        "scripts/features/loyalty/loyalty_manager.py",
        "scripts/features/loyalty/loyalty_setup.py",
        "scripts/analysis/verification/verify_loyalty_snippet_deployment.py",
    ],
    "BUNDLES": [
        "scripts/features/bundles/final_bundle_audit.py",
        "scripts/analysis/verification/verify_bundle_pricing.py",
        "scripts/analysis/audits/audit_bundles_missing_images.py",
    ],
    "STORE_STATUS": [
        "verify_store_infrastructure.py",
        "market-analysis/verify_shopify_state.py",
        "scripts/analysis/verify_prelaunch_readiness.py",
    ],
    "WORKFLOW_AUTOMATION": [
        "scripts/analysis/checks/check_workflow_execution.py",
        "scripts/analysis/verification/verify_n8n_workflow.py",
        "scripts/analysis/verification/verify_flow_execution.py",
    ],
}

def run_script(script_path, timeout=120):
    """Execute un script et retourne le résultat"""
    if not os.path.exists(script_path):
        return {
            "status": "FILE_NOT_FOUND",
            "returncode": -1,
            "stdout": "",
            "stderr": f"File not found: {script_path}",
            "execution_time": 0
        }

    start_time = datetime.now()

    try:
        # Détermine l'exécuteur basé sur l'extension
        if script_path.endswith('.py'):
            cmd = ["python3", script_path]
        elif script_path.endswith('.js'):
            cmd = ["node", script_path]
        elif script_path.endswith('.gs'):
            return {
                "status": "GOOGLE_APPS_SCRIPT",
                "returncode": 0,
                "stdout": "Google Apps Script - Cannot execute locally",
                "stderr": "",
                "execution_time": 0
            }
        else:
            return {
                "status": "UNKNOWN_TYPE",
                "returncode": -1,
                "stdout": "",
                "stderr": f"Unknown file type: {script_path}",
                "execution_time": 0
            }

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.getcwd()
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        # Détermine le statut basé sur le returncode et le contenu
        if result.returncode == 0:
            status = "SUCCESS"
        elif "ModuleNotFoundError" in result.stderr or "ImportError" in result.stderr:
            status = "MISSING_DEPENDENCY"
        elif "FileNotFoundError" in result.stderr:
            status = "MISSING_FILE"
        elif "401" in result.stderr or "403" in result.stderr or "Unauthorized" in result.stderr:
            status = "AUTH_ERROR"
        elif "404" in result.stderr:
            status = "API_ERROR"
        elif "Connection" in result.stderr or "Timeout" in result.stderr:
            status = "NETWORK_ERROR"
        else:
            status = "EXECUTION_ERROR"

        return {
            "status": status,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "execution_time": execution_time
        }

    except subprocess.TimeoutExpired:
        execution_time = (datetime.now() - start_time).total_seconds()
        return {
            "status": "TIMEOUT",
            "returncode": -1,
            "stdout": "",
            "stderr": f"Script timed out after {timeout} seconds",
            "execution_time": execution_time
        }
    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return {
            "status": "EXCEPTION",
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "execution_time": execution_time
        }

def test_category(category_name, scripts):
    """Teste tous les scripts d'une catégorie"""
    print(f"\n{'='*70}")
    print(f"📦 CATEGORY: {category_name}")
    print(f"{'='*70}")

    results = []

    for script in scripts:
        print(f"\n🧪 Testing: {script}")
        result = run_script(script)

        results.append({
            "script": script,
            **result
        })

        # Affiche le résultat immédiatement
        status_emoji = {
            "SUCCESS": "✅",
            "FILE_NOT_FOUND": "❌",
            "MISSING_DEPENDENCY": "⚠️",
            "AUTH_ERROR": "🔑",
            "API_ERROR": "🌐",
            "NETWORK_ERROR": "📡",
            "EXECUTION_ERROR": "❌",
            "TIMEOUT": "⏱️",
            "GOOGLE_APPS_SCRIPT": "☁️",
            "UNKNOWN_TYPE": "❓",
            "MISSING_FILE": "📁"
        }

        emoji = status_emoji.get(result["status"], "❓")
        print(f"  {emoji} Status: {result['status']}")
        print(f"  ⏱️  Time: {result['execution_time']:.2f}s")

        if result["status"] not in ["SUCCESS", "GOOGLE_APPS_SCRIPT"]:
            # Affiche les erreurs critiques
            if result["stderr"]:
                error_lines = result["stderr"].split('\n')[:3]  # First 3 lines
                for line in error_lines:
                    if line.strip():
                        print(f"  ⚠️  {line.strip()[:100]}")

    return results

def generate_summary(all_results):
    """Génère un résumé complet des tests"""
    print(f"\n{'='*70}")
    print(f"📊 TEST SUMMARY - FLYWHEEL ECOSYSTEM")
    print(f"{'='*70}")

    total_scripts = sum(len(results) for results in all_results.values())

    # Compte par statut
    status_counts = defaultdict(int)
    for category_results in all_results.values():
        for result in category_results:
            status_counts[result["status"]] += 1

    print(f"\n📦 TOTAL SCRIPTS TESTED: {total_scripts}")
    print(f"\n📈 STATUS BREAKDOWN:")

    status_order = ["SUCCESS", "GOOGLE_APPS_SCRIPT", "MISSING_DEPENDENCY", "AUTH_ERROR",
                   "FILE_NOT_FOUND", "API_ERROR", "NETWORK_ERROR", "EXECUTION_ERROR",
                   "TIMEOUT", "UNKNOWN_TYPE", "MISSING_FILE"]

    for status in status_order:
        if status in status_counts:
            count = status_counts[status]
            percentage = (count / total_scripts) * 100
            emoji = {
                "SUCCESS": "✅",
                "FILE_NOT_FOUND": "❌",
                "MISSING_DEPENDENCY": "⚠️",
                "AUTH_ERROR": "🔑",
                "API_ERROR": "🌐",
                "NETWORK_ERROR": "📡",
                "EXECUTION_ERROR": "❌",
                "TIMEOUT": "⏱️",
                "GOOGLE_APPS_SCRIPT": "☁️",
                "UNKNOWN_TYPE": "❓",
                "MISSING_FILE": "📁"
            }.get(status, "❓")
            print(f"  {emoji} {status}: {count}/{total_scripts} ({percentage:.1f}%)")

    # Calcule le taux de succès
    success_count = status_counts.get("SUCCESS", 0) + status_counts.get("GOOGLE_APPS_SCRIPT", 0)
    success_rate = (success_count / total_scripts) * 100 if total_scripts > 0 else 0

    print(f"\n🎯 SUCCESS RATE: {success_rate:.1f}% ({success_count}/{total_scripts})")

    # Scripts qui nécessitent une action
    needs_fix = []
    for category, category_results in all_results.items():
        for result in category_results:
            if result["status"] not in ["SUCCESS", "GOOGLE_APPS_SCRIPT"]:
                needs_fix.append({
                    "category": category,
                    "script": result["script"],
                    "status": result["status"],
                    "error": result["stderr"][:200] if result["stderr"] else "No error details"
                })

    if needs_fix:
        print(f"\n⚠️  SCRIPTS NEEDING ATTENTION: {len(needs_fix)}")
        print(f"\n📋 DETAILED ISSUES:")

        for i, issue in enumerate(needs_fix[:10], 1):  # Show first 10
            print(f"\n{i}. {issue['script']}")
            print(f"   Category: {issue['category']}")
            print(f"   Status: {issue['status']}")
            print(f"   Error: {issue['error']}")

        if len(needs_fix) > 10:
            print(f"\n... and {len(needs_fix) - 10} more issues")
    else:
        print(f"\n✅ ALL SCRIPTS FUNCTIONAL!")

    return {
        "total_scripts": total_scripts,
        "success_count": success_count,
        "success_rate": success_rate,
        "status_counts": dict(status_counts),
        "needs_fix": needs_fix
    }

def main():
    print("="*70)
    print("🔬 FLYWHEEL ECOSYSTEM - EMPIRICAL VERIFICATION")
    print("="*70)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Method: Execute → Verify → Document → Iterate")
    print(f"Approach: Bottom-up factual, 0% assumptions")

    all_results = {}

    # Teste chaque catégorie
    for category, scripts in FLYWHEEL_SCRIPTS.items():
        results = test_category(category, scripts)
        all_results[category] = results

    # Génère le résumé
    summary = generate_summary(all_results)

    print(f"\n{'='*70}")
    print(f"✅ TESTING COMPLETE")
    print(f"{'='*70}")

    # Détermine le succès global
    if summary["success_rate"] == 100:
        print(f"\n🎉 SUCCESS: All flywheel scripts are functional!")
        sys.exit(0)
    elif summary["success_rate"] >= 80:
        print(f"\n⚠️  PARTIAL SUCCESS: {summary['success_rate']:.1f}% functional")
        print(f"   {len(summary['needs_fix'])} scripts need attention")
        sys.exit(1)
    else:
        print(f"\n❌ FAILURE: Only {summary['success_rate']:.1f}% functional")
        print(f"   {len(summary['needs_fix'])} scripts need fixing")
        sys.exit(2)

if __name__ == "__main__":
    main()
