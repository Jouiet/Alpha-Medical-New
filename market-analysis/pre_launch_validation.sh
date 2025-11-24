#!/bin/bash
#
# Pre-Launch Validation Script - Alpha Medical Flywheel System
# Validates ALL prerequisites before system activation
#
# Returns exit code 0 if ready for launch, 1 if blockers exist
#
# Usage: ./pre_launch_validation.sh

set -e

echo "🚀 ALPHA MEDICAL - PRE-LAUNCH VALIDATION"
echo "========================================="
echo ""
echo "This script validates ALL prerequisites for Flywheel automation."
echo "It checks infrastructure, credentials, workflows, and manual tasks."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BLOCKERS=0
WARNINGS=0
READY=0

section() {
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

check() {
    local status=$1
    local message=$2
    local details=$3

    if [ "$status" = "PASS" ]; then
        echo -e "  ${GREEN}✅ $message${NC}"
        ((READY++))
    elif [ "$status" = "WARN" ]; then
        echo -e "  ${YELLOW}⚠️  $message${NC}"
        if [ -n "$details" ]; then
            echo -e "     ${YELLOW}$details${NC}"
        fi
        ((WARNINGS++))
    else
        echo -e "  ${RED}❌ $message${NC}"
        if [ -n "$details" ]; then
            echo -e "     ${RED}$details${NC}"
        fi
        ((BLOCKERS++))
    fi
}

section "1. GITHUB ACTIONS WORKFLOWS"

# Check if workflows exist
if [ -d ".github/workflows" ]; then
    WORKFLOW_COUNT=$(ls -1 .github/workflows/*.yml 2>/dev/null | wc -l | tr -d ' ')
    if [ "$WORKFLOW_COUNT" -ge 4 ]; then
        check "PASS" "Workflows created ($WORKFLOW_COUNT files)"
    else
        check "FAIL" "Workflows incomplete" "Expected 4+ workflows, found $WORKFLOW_COUNT"
    fi
else
    check "FAIL" "Workflows directory missing" ".github/workflows/ not found"
fi

# Check if workflows are active
if command -v gh &> /dev/null; then
    if gh auth status &> /dev/null 2>&1; then
        ACTIVE_WORKFLOWS=$(gh workflow list 2>/dev/null | grep -c "active" || echo "0")
        if [ "$ACTIVE_WORKFLOWS" -ge 4 ]; then
            check "PASS" "Workflows active on GitHub ($ACTIVE_WORKFLOWS active)"
        else
            check "WARN" "Some workflows may not be active" "Only $ACTIVE_WORKFLOWS workflows active"
        fi
    else
        check "WARN" "Cannot verify workflow status" "gh CLI not authenticated"
    fi
else
    check "WARN" "Cannot verify workflow status" "gh CLI not installed"
fi

section "2. GITHUB SECRETS (CRITICAL BLOCKERS)"

if command -v gh &> /dev/null && gh auth status &> /dev/null 2>&1; then
    SECRETS=$(gh secret list 2>&1 || echo "")

    if echo "$SECRETS" | grep -q "APIFY_API_TOKEN"; then
        check "PASS" "APIFY_API_TOKEN configured"
    else
        check "FAIL" "APIFY_API_TOKEN missing" "Run: gh secret set APIFY_API_TOKEN"
    fi

    if echo "$SECRETS" | grep -q "SHOPIFY_API_KEY"; then
        check "PASS" "SHOPIFY_API_KEY configured"
    else
        check "FAIL" "SHOPIFY_API_KEY missing" "Get from: Shopify Admin → Apps → Develop apps"
    fi

    if echo "$SECRETS" | grep -q "SHOPIFY_PASSWORD"; then
        check "PASS" "SHOPIFY_PASSWORD configured"
    else
        check "FAIL" "SHOPIFY_PASSWORD missing" "Admin API access token"
    fi

    if echo "$SECRETS" | grep -q "GOOGLE_CREDENTIALS_JSON"; then
        check "PASS" "GOOGLE_CREDENTIALS_JSON configured"
    else
        check "FAIL" "GOOGLE_CREDENTIALS_JSON missing" "Follow: market-analysis/SETUP_GOOGLE_SHEETS_API.md"
    fi
else
    check "WARN" "Cannot verify secrets" "gh CLI not available or not authenticated"
fi

section "3. GOOGLE SHEETS SETUP"

# Check if SETUP_GOOGLE_SHEETS_API.md exists
if [ -f "market-analysis/SETUP_GOOGLE_SHEETS_API.md" ]; then
    check "PASS" "Google Sheets setup guide exists"
else
    check "WARN" "Google Sheets setup guide missing"
fi

# Check if Google Sheet ID is in docs
SHEET_ID="1KyE_H8OPLLJfgRjehNZLS_RcMJToHRQ9gny1Sgoa_JE"
if grep -r "$SHEET_ID" . --include="*.md" &> /dev/null; then
    check "PASS" "Google Sheet ID documented ($SHEET_ID)"
else
    check "WARN" "Google Sheet ID not found in docs"
fi

section "4. PYTHON SCRIPTS & DEPENDENCIES"

# Check if Python is available
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    check "PASS" "Python 3 installed ($PYTHON_VERSION)"
else
    check "FAIL" "Python 3 not installed" "Required for scraping scripts"
fi

# Check if requirements.txt exists
if [ -f "market-analysis/requirements.txt" ]; then
    check "PASS" "requirements.txt exists"

    # Check if key modules are installed
    if python3 -c "import apify; import gspread; import shopify" 2>/dev/null; then
        check "PASS" "Python dependencies installed"
    else
        check "WARN" "Some Python dependencies missing" "Run: pip install -r market-analysis/requirements.txt"
    fi
else
    check "FAIL" "requirements.txt missing" "market-analysis/requirements.txt not found"
fi

section "5. KLAVIYO SETUP (CONVERSION BLOCKER)"

# Klaviyo is external - cannot verify via API without credentials
check "WARN" "Klaviyo plan selection" "MANUAL: Select Email-Only 20K tier ($300-350/mo)"
check "WARN" "Klaviyo Shopify integration" "MANUAL: Verify in Klaviyo dashboard"

section "6. SHOPIFY CONFIGURATION (MANUAL TASKS)"

# These are manual checks - documented as warnings
check "WARN" "Customer segments creation" "MANUAL: Create Seniors/Workers/Athletes segments (10 min)"
check "WARN" "Shopify Flow workflows" "MANUAL: Configure 4 flows (55 min) - See SHOPIFY_FLOW_CONFIGURATION_GUIDE.md"
check "WARN" "PayPal status verification" "MANUAL: Verify PayPal is DISABLED (Settings → Payments)"

section "7. DOCUMENTATION COMPLETENESS"

REQUIRED_DOCS=(
    "AI_SEO_MARKETING_STRATEGIC_ANALYSIS_2025-2026.md"
    "market-analysis/AUTOMATION_COMPLETE_WORKFLOWS.md"
    "SEO_MARKETING_FORENSIC_ANALYSIS.md"
    "SHOPIFY_FLOW_CONFIGURATION_GUIDE.md"
    "LOYALTY_SYSTEM_SETUP_GUIDE.md"
    "TOP5_PERCENT_NATIVE_IMPLEMENTATION_PLAN.md"
)

DOCS_FOUND=0
for doc in "${REQUIRED_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        ((DOCS_FOUND++))
    fi
done

if [ "$DOCS_FOUND" -eq "${#REQUIRED_DOCS[@]}" ]; then
    check "PASS" "All documentation files present ($DOCS_FOUND/${#REQUIRED_DOCS[@]})"
else
    check "WARN" "Some documentation missing" "$DOCS_FOUND/${#REQUIRED_DOCS[@]} docs found"
fi

section "8. INFRASTRUCTURE READINESS"

# Check .env file (should exist but not contain secrets)
if [ -f ".env" ]; then
    check "PASS" ".env file exists"
else
    check "WARN" ".env file missing" "Local environment config recommended"
fi

# Check GitHub repo connection
if git remote -v | grep -q "github.com"; then
    check "PASS" "GitHub repository connected"
else
    check "FAIL" "GitHub repository not connected" "Cannot push/pull workflows"
fi

# Summary
echo ""
echo "========================================="
echo -e "${BLUE}VALIDATION SUMMARY${NC}"
echo "========================================="
echo ""
echo -e "  ${GREEN}Ready:${NC}    $READY"
echo -e "  ${YELLOW}Warnings:${NC} $WARNINGS"
echo -e "  ${RED}Blockers:${NC} $BLOCKERS"
echo ""

if [ "$BLOCKERS" -eq 0 ]; then
    echo -e "${GREEN}✅ SYSTEM READY FOR LAUNCH!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Test first workflow run:"
    echo "     gh workflow run \"Daily Multi-Platform Lead Scraping\""
    echo ""
    echo "  2. Complete manual tasks ($WARNINGS warnings):"
    echo "     - Klaviyo plan selection (5 min)"
    echo "     - Shopify customer segments (10 min)"
    echo "     - Shopify Flow configuration (55 min)"
    echo "     - PayPal verification (5 min)"
    echo ""
    echo "  3. Monitor first scraping run (validate 700 leads Month 1)"
    echo ""
    exit 0
else
    echo -e "${RED}❌ CRITICAL BLOCKERS PREVENT LAUNCH${NC}"
    echo ""
    echo "Resolve $BLOCKERS blocker(s) before proceeding:"
    echo ""
    echo "  Priority 1: GitHub Secrets (15 min total)"
    echo "    Run: ./market-analysis/setup_github_secrets_helper.sh"
    echo ""
    echo "  Priority 2: Google Sheets credentials (10 min)"
    echo "    Guide: market-analysis/SETUP_GOOGLE_SHEETS_API.md"
    echo ""
    echo "After resolving blockers, re-run this validation:"
    echo "  ./pre_launch_validation.sh"
    echo ""
    exit 1
fi
