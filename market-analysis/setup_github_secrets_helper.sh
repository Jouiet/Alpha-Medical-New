#!/bin/bash
#
# GitHub Secrets Setup Helper for Alpha Medical Automation
# This script validates and guides GitHub Secrets configuration (BLOQUEUR #2)
#
# DOES NOT set secrets automatically (requires manual gh CLI auth + permissions)
# DOES validate that secrets are configured correctly
#
# Usage: ./setup_github_secrets_helper.sh

set -e

echo "🔐 GITHUB SECRETS SETUP HELPER"
echo "================================"
echo ""
echo "This script helps you configure the 4 required GitHub Secrets"
echo "for Alpha Medical automation workflows."
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) not installed${NC}"
    echo ""
    echo "Install it:"
    echo "  macOS: brew install gh"
    echo "  Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ GitHub CLI installed${NC}"

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}❌ Not authenticated with GitHub${NC}"
    echo ""
    echo "Run: gh auth login"
    echo "Then re-run this script"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Authenticated with GitHub${NC}"
echo ""

# Check current secrets
echo "📋 Checking current GitHub Secrets..."
echo ""

SECRETS=$(gh secret list 2>&1 || echo "")

check_secret() {
    local SECRET_NAME=$1
    local DESCRIPTION=$2
    local WHERE_TO_GET=$3

    if echo "$SECRETS" | grep -q "^$SECRET_NAME"; then
        echo -e "  ${GREEN}✅ $SECRET_NAME${NC} - Configured"
        return 0
    else
        echo -e "  ${RED}❌ $SECRET_NAME${NC} - Missing"
        echo "     Description: $DESCRIPTION"
        echo "     Where to get: $WHERE_TO_GET"
        echo ""
        return 1
    fi
}

MISSING=0

# Check each required secret
check_secret "APIFY_API_TOKEN" \
    "Apify API token for scraping automation" \
    "https://console.apify.com/account/integrations" || ((MISSING++))

check_secret "SHOPIFY_API_KEY" \
    "Shopify Admin API key" \
    "Shopify Admin → Apps → Develop apps → Create app → API credentials" || ((MISSING++))

check_secret "SHOPIFY_PASSWORD" \
    "Shopify Admin API access token" \
    "Same location as SHOPIFY_API_KEY (Admin API access token)" || ((MISSING++))

check_secret "GOOGLE_CREDENTIALS_JSON" \
    "Google Sheets API service account JSON" \
    "Follow: market-analysis/SETUP_GOOGLE_SHEETS_API.md (10 min)" || ((MISSING++))

echo ""
echo "================================"
echo ""

if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}✅ ALL SECRETS CONFIGURED!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Test workflows manually:"
    echo "     gh workflow run \"Daily Multi-Platform Lead Scraping\""
    echo ""
    echo "  2. Check workflow run status:"
    echo "     gh run list --limit 5"
    echo ""
    echo "  3. View workflow logs if needed:"
    echo "     gh run view <run-id> --log"
    echo ""
    exit 0
else
    echo -e "${YELLOW}⚠️  $MISSING SECRET(S) MISSING${NC}"
    echo ""
    echo "To configure a secret, use:"
    echo "  gh secret set SECRET_NAME"
    echo ""
    echo "Then paste the value when prompted (input is hidden)"
    echo ""
    echo "================================"
    echo ""
    echo "📝 STEP-BY-STEP GUIDE:"
    echo ""

    if ! echo "$SECRETS" | grep -q "^APIFY_API_TOKEN"; then
        echo "1️⃣  APIFY_API_TOKEN (Required for scraping)"
        echo "   Get it: https://console.apify.com/account/integrations"
        echo "   Set it: gh secret set APIFY_API_TOKEN"
        echo "   Paste your Apify API token when prompted"
        echo ""
    fi

    if ! echo "$SECRETS" | grep -q "^SHOPIFY_API_KEY"; then
        echo "2️⃣  SHOPIFY_API_KEY (Required for backup workflow)"
        echo "   Get it:"
        echo "     1. Shopify Admin → Apps → App development → Create an app"
        echo "     2. Name: \"Alpha Medical Automation\""
        echo "     3. Configure → Admin API scopes:"
        echo "        - read_products, write_products"
        echo "        - read_customers, write_customers"
        echo "        - read_orders"
        echo "     4. Install app → Copy API key"
        echo "   Set it: gh secret set SHOPIFY_API_KEY"
        echo ""
    fi

    if ! echo "$SECRETS" | grep -q "^SHOPIFY_PASSWORD"; then
        echo "3️⃣  SHOPIFY_PASSWORD (Admin API access token)"
        echo "   Get it: Same app as SHOPIFY_API_KEY → API credentials → Admin API access token"
        echo "   Set it: gh secret set SHOPIFY_PASSWORD"
        echo ""
    fi

    if ! echo "$SECRETS" | grep -q "^GOOGLE_CREDENTIALS_JSON"; then
        echo "4️⃣  GOOGLE_CREDENTIALS_JSON (Required for lead sync)"
        echo "   Get it:"
        echo "     Follow: market-analysis/SETUP_GOOGLE_SHEETS_API.md (10 min guide)"
        echo "     Result: credentials.json file with service account key"
        echo "   Set it:"
        echo "     cat credentials.json | gh secret set GOOGLE_CREDENTIALS_JSON"
        echo ""
        echo "   ⚠️  Paste the ENTIRE JSON content (including { } braces)"
        echo ""
    fi

    echo "================================"
    echo ""
    echo "After configuring all secrets, re-run this script to verify:"
    echo "  ./setup_github_secrets_helper.sh"
    echo ""
    exit 1
fi
