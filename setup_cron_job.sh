#!/bin/bash
###############################################################################
# SETUP CRON JOB FOR DAILY LEAD SCRAPING
# Adds automated daily scraping at 9:00 AM
###############################################################################

echo "======================================================================"
echo "ALPHA MEDICAL - CRON JOB SETUP"
echo "======================================================================"

# Configuration
CRON_SCRIPT="/Users/mac/Desktop/Alpha-Medical/market-analysis/daily_lead_scraping.sh"
CRON_TIME="0 9 * * *"  # 9:00 AM daily
CRON_ENTRY="$CRON_TIME $CRON_SCRIPT"

# Verify script exists
echo ""
echo "[1/4] Verifying scraping script exists..."
if [ ! -f "$CRON_SCRIPT" ]; then
    echo "❌ Script not found: $CRON_SCRIPT"
    exit 1
fi
echo "✅ Script found: $CRON_SCRIPT"

# Make script executable
echo ""
echo "[2/4] Making script executable..."
chmod +x "$CRON_SCRIPT"
if [ -x "$CRON_SCRIPT" ]; then
    echo "✅ Script is now executable"
else
    echo "❌ Failed to make script executable"
    exit 1
fi

# Check if cron entry already exists
echo ""
echo "[3/4] Checking existing crontab..."
EXISTING_CRON=$(crontab -l 2>/dev/null | grep -F "$CRON_SCRIPT")

if [ -n "$EXISTING_CRON" ]; then
    echo "⚠️  Cron job already exists:"
    echo "   $EXISTING_CRON"
    echo ""
    read -p "Do you want to replace it? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Cancelled. No changes made."
        exit 0
    fi

    # Remove existing entry
    crontab -l 2>/dev/null | grep -v -F "$CRON_SCRIPT" | crontab -
    echo "✅ Removed old cron entry"
fi

# Add new cron entry
echo ""
echo "[4/4] Adding new cron job..."

# Get current crontab
CURRENT_CRON=$(crontab -l 2>/dev/null)

# Add new entry
(echo "$CURRENT_CRON"; echo "$CRON_ENTRY") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job added successfully"
else
    echo "❌ Failed to add cron job"
    exit 1
fi

# Verify installation
echo ""
echo "======================================================================"
echo "VERIFICATION"
echo "======================================================================"
echo ""
echo "Current crontab entries:"
crontab -l

echo ""
echo "======================================================================"
echo "SETUP COMPLETE"
echo "======================================================================"
echo ""
echo "Cron Job Details:"
echo "  Schedule: $CRON_TIME (9:00 AM daily)"
echo "  Script:   $CRON_SCRIPT"
echo ""
echo "What happens daily at 9 AM:"
echo "  1. Scrapes Instagram hashtags (7 hashtags × 50 results each)"
echo "  2. Scrapes Google Maps B2B leads (6 queries × 20 results each)"
echo "  3. Syncs to Google Sheets (if configured)"
echo "  4. Exports Shopify CSV files"
echo "  5. Logs everything to: market-analysis/scraping_log.txt"
echo ""
echo "Expected daily output:"
echo "  - ~350 Instagram leads"
echo "  - ~120 B2B leads"
echo "  - ~470 total leads per day"
echo ""
echo "View logs:"
echo "  tail -f /Users/mac/Desktop/Alpha-Medical/market-analysis/scraping_log.txt"
echo ""
echo "Test manually:"
echo "  $CRON_SCRIPT"
echo ""
echo "Remove cron job:"
echo "  crontab -e  (then delete the line)"
echo ""
echo "✅ CRON JOB READY!"

exit 0
