#!/bin/bash
# POWER BI QUICK START - Alpha Medical
# Helper script pour démarrer apprentissage Power BI Free tier

set -e

echo "========================================================================"
echo "POWER BI QUICK START - Alpha Medical"
echo "========================================================================"
echo ""

# Check if .env.powerbi is configured
if [ ! -f ".env.powerbi" ]; then
    echo "❌ Error: .env.powerbi not found"
    echo "Run: cat .env.powerbi.template > .env.powerbi"
    exit 1
fi

# Check if credentials are filled
if grep -q 'AZURE_TENANT_ID=""' .env.powerbi; then
    echo "⚠️  WARNING: .env.powerbi credentials not configured yet"
    echo ""
    echo "📝 Next steps:"
    echo "1. Create Azure AD App Registration:"
    echo "   → https://portal.azure.com"
    echo "   → Azure Active Directory → App registrations → New"
    echo ""
    echo "2. Fill .env.powerbi with:"
    echo "   - AZURE_TENANT_ID (Directory ID)"
    echo "   - AZURE_CLIENT_ID (Application ID)"
    echo "   - AZURE_CLIENT_SECRET (Client secret value)"
    echo ""
    echo "3. Enable Power BI REST API:"
    echo "   → https://app.powerbi.com/admin-portal/tenantSettings"
    echo "   → Developer settings → Dataset Execute Queries REST API → Enable"
    echo ""
    echo "4. Re-run this script: ./powerbi_quick_start.sh"
    echo ""
    exit 0
fi

# Load credentials
echo "🔐 Loading credentials from .env.powerbi..."
export $(grep -v '^#' .env.powerbi | grep -v '^$' | xargs)

# Check Python packages
echo ""
echo "📦 Checking Python dependencies..."
if ! python3 -c "import pbipy" 2>/dev/null; then
    echo "Installing pbipy..."
    pip3 install pbipy msal --quiet
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed (pbipy, msal)"
fi

# Test connection
echo ""
echo "🧪 Testing Power BI connection..."
echo ""
python3 powerbi_connection_test.py

# Success
echo ""
echo "========================================================================"
echo "✅ POWER BI SETUP COMPLETE"
echo "========================================================================"
echo ""
echo "📚 Next steps - Learning Path:"
echo ""
echo "1. Read learning guide:"
echo "   cat POWER_BI_LEARNING_PATH.md | less"
echo ""
echo "2. Open Power BI Service:"
echo "   open https://app.powerbi.com"
echo ""
echo "3. Start Microsoft Learn tutorial:"
echo "   open https://learn.microsoft.com/training/paths/get-started-power-bi/"
echo ""
echo "4. Practice with test script:"
echo "   python3 powerbi_connection_test.py"
echo ""
echo "📊 Your learning timeline:"
echo "   Week 1-2:  Power BI fundamentals"
echo "   Week 3-4:  Connect Shopify/GA4/Google Sheets"
echo "   Week 5-8:  Learn DAX (analytics language)"
echo "   Week 9-12: Build flywheel dashboards"
echo ""
echo "💡 Free tier = Perfect for 3-6 months learning"
echo "   Upgrade to Pro ($10/mo) when revenue > $10K/month"
echo ""

