#!/bin/bash
###############################################################################
# DAILY LEAD SCRAPING AUTOMATION - Alpha Medical
#
# Schedule: 9:00 AM daily via cron
# Add to crontab: 0 9 * * * /Users/mac/Desktop/Alpha-Medical/market-analysis/daily_lead_scraping.sh
#
# What it does:
#   1. Scrapes Instagram leads (hashtags)
#   2. Scrapes Google Maps B2B leads (multiple locations)
#   3. Syncs to Google Sheets (if credentials available)
#   4. Exports Shopify CSV
#   5. Logs results
###############################################################################

# Configuration
SCRIPT_DIR="/Users/mac/Desktop/Alpha-Medical/market-analysis"
LOG_FILE="$SCRIPT_DIR/scraping_log.txt"
DATE=$(date +%Y%m%d)
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Change to script directory
cd "$SCRIPT_DIR" || exit 1

# Log start
echo "======================================================================" >> "$LOG_FILE"
echo "SCRAPING RUN: $TIMESTAMP" >> "$LOG_FILE"
echo "======================================================================" >> "$LOG_FILE"

###############################################################################
# PHASE 1: INSTAGRAM SCRAPING
###############################################################################

echo "PHASE 1: Instagram Hashtag Scraping..." >> "$LOG_FILE"

# Hashtags par persona
INSTAGRAM_HASHTAGS=(
    "arthritis"          # seniors
    "jointpain"          # seniors
    "backpain"           # seniors + workers
    "kneepain"           # seniors + athletes
    "seniorfitness"      # seniors
    "deskpain"           # workers
    "posturecorrection"  # workers
)

INSTAGRAM_RESULTS=0

for hashtag in "${INSTAGRAM_HASHTAGS[@]}"; do
    echo "  → Scraping #$hashtag..." >> "$LOG_FILE"

    python3 lead_generation_scraper.py \
        --instagram \
        --hashtag "$hashtag" \
        --max-results 50 \
        >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        INSTAGRAM_RESULTS=$((INSTAGRAM_RESULTS + 1))
        echo "    ✅ #$hashtag done" >> "$LOG_FILE"
    else
        echo "    ❌ #$hashtag failed" >> "$LOG_FILE"
    fi

    # Rate limit: Wait 10 seconds between hashtags
    sleep 10
done

echo "Instagram scraping complete: $INSTAGRAM_RESULTS/${#INSTAGRAM_HASHTAGS[@]} hashtags successful" >> "$LOG_FILE"

###############################################################################
# PHASE 2: TIKTOK CONSUMER INTELLIGENCE SCRAPING
###############################################################################

echo "" >> "$LOG_FILE"
echo "PHASE 2: TikTok Consumer Intelligence Scraping..." >> "$LOG_FILE"

# Same hashtags as Instagram for cross-platform consumer intelligence
TIKTOK_HASHTAGS=(
    "arthritis"
    "jointpain"
    "backpain"
    "kneepain"
    "seniorfitness"
    "deskpain"
    "posturecorrection"
)

TIKTOK_RESULTS=0

for hashtag in "${TIKTOK_HASHTAGS[@]}"; do
    echo "  → Scraping TikTok #$hashtag..." >> "$LOG_FILE"

    python3 lead_generation_scraper.py \
        --tiktok \
        --hashtag "$hashtag" \
        >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        TIKTOK_RESULTS=$((TIKTOK_RESULTS + 1))
        echo "    ✅ TikTok #$hashtag done" >> "$LOG_FILE"
    else
        echo "    ❌ TikTok #$hashtag failed" >> "$LOG_FILE"
    fi

    # Rate limit: Wait 10 seconds between hashtags
    sleep 10
done

echo "TikTok scraping complete: $TIKTOK_RESULTS/${#TIKTOK_HASHTAGS[@]} hashtags successful" >> "$LOG_FILE"

###############################################################################
# PHASE 3: FACEBOOK CONSUMER INTELLIGENCE SCRAPING
###############################################################################

echo "" >> "$LOG_FILE"
echo "PHASE 3: Facebook Consumer Intelligence Scraping..." >> "$LOG_FILE"

# Top Facebook pages for pain/health topics (public pages with high engagement)
declare -a FACEBOOK_PAGES=(
    "https://www.facebook.com/ArthritisFoundation"
    "https://www.facebook.com/BackPainReliefClinic"
    "https://www.facebook.com/KneeHealthMatters"
    "https://www.facebook.com/ChronicPainSupport"
    "https://www.facebook.com/SeniorFitnessAndWellness"
)

FACEBOOK_RESULTS=0

for page_url in "${FACEBOOK_PAGES[@]}"; do
    echo "  → Scraping Facebook page: $page_url..." >> "$LOG_FILE"

    # Extract page name from URL for logging
    page_name=$(echo "$page_url" | sed 's/.*facebook\.com\///' | sed 's/\/.*//')

    python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from lead_generation_scraper import ApifyLeadScraper, LeadAnalyzer
import os

scraper = ApifyLeadScraper(os.getenv('APIFY_API_TOKEN'))
analyzer = LeadAnalyzer('$SCRIPT_DIR/leads')

posts = scraper.scrape_facebook_pages(['$page_url'], max_posts=30)
print(f'✅ Scraped {len(posts)} Facebook posts from $page_name')

# Save raw data
analyzer.save_leads(posts, 'general', 'facebook')
" >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        FACEBOOK_RESULTS=$((FACEBOOK_RESULTS + 1))
        echo "    ✅ Facebook page $page_name done" >> "$LOG_FILE"
    else
        echo "    ❌ Facebook page $page_name failed" >> "$LOG_FILE"
    fi

    # Rate limit: Wait 15 seconds between pages
    sleep 15
done

echo "Facebook scraping complete: $FACEBOOK_RESULTS/${#FACEBOOK_PAGES[@]} pages successful" >> "$LOG_FILE"

###############################################################################
# PHASE 4: COMPETITOR INTELLIGENCE SCRAPING
###############################################################################

echo "" >> "$LOG_FILE"
echo "PHASE 4: Competitor Intelligence Scraping..." >> "$LOG_FILE"

# D2C Competitor research (market intelligence, not B2B leads)
declare -a GMAPS_QUERIES=(
    "orthopedic supply store:Miami, FL"
    "medical supply store:Los Angeles, CA"
    "physical therapy equipment:New York, NY"
    "orthopedic store:Chicago, IL"
    "medical equipment store:Houston, TX"
    "sports medicine store:San Francisco, CA"
)

GMAPS_RESULTS=0

for query_location in "${GMAPS_QUERIES[@]}"; do
    # Split query:location
    IFS=':' read -r query location <<< "$query_location"

    echo "  → Scraping '$query' in $location..." >> "$LOG_FILE"

    python3 lead_generation_scraper.py \
        --google-maps \
        --query "$query" \
        --location "$location" \
        --max-results 20 \
        >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        GMAPS_RESULTS=$((GMAPS_RESULTS + 1))
        echo "    ✅ '$query' in $location done" >> "$LOG_FILE"
    else
        echo "    ❌ '$query' in $location failed" >> "$LOG_FILE"
    fi

    # Rate limit: Wait 15 seconds between queries
    sleep 15
done

echo "Google Maps scraping complete: $GMAPS_RESULTS/${#GMAPS_QUERIES[@]} queries successful" >> "$LOG_FILE"

###############################################################################
# PHASE 3: SYNC TO GOOGLE SHEETS (if credentials available)
###############################################################################

echo "" >> "$LOG_FILE"
echo "PHASE 3: Syncing to Google Sheets..." >> "$LOG_FILE"

if [ -f "$SCRIPT_DIR/google_credentials.json" ]; then
    # Find all lead files from today
    LEAD_FILES=$(find "$SCRIPT_DIR/leads/general" -name "leads_general_*_${DATE}*.json" -type f)

    SYNCED_COUNT=0
    for lead_file in $LEAD_FILES; do
        echo "  → Syncing $lead_file..." >> "$LOG_FILE"

        python3 sync_leads_to_sheets.py "$lead_file" >> "$LOG_FILE" 2>&1

        if [ $? -eq 0 ]; then
            SYNCED_COUNT=$((SYNCED_COUNT + 1))
            echo "    ✅ Synced" >> "$LOG_FILE"
        else
            echo "    ❌ Sync failed" >> "$LOG_FILE"
        fi
    done

    echo "Google Sheets sync complete: $SYNCED_COUNT files synced" >> "$LOG_FILE"
else
    echo "  ⚠️  Google Sheets credentials not found - skipping sync" >> "$LOG_FILE"
    echo "  Setup guide: SETUP_GOOGLE_SHEETS_API.md" >> "$LOG_FILE"
fi

###############################################################################
# PHASE 4: EXPORT SHOPIFY CSV
###############################################################################

echo "" >> "$LOG_FILE"
echo "PHASE 4: Exporting Shopify CSV..." >> "$LOG_FILE"

# Find all lead files from today
LEAD_FILES=$(find "$SCRIPT_DIR/leads/general" -name "leads_general_*_${DATE}*.json" -type f)

if [ -z "$LEAD_FILES" ]; then
    echo "  ⚠️  No lead files found for today" >> "$LOG_FILE"
else
    # Merge all leads into one CSV
    # For now, export each separately (can be improved)

    for lead_file in $LEAD_FILES; do
        echo "  → Exporting $lead_file to CSV..." >> "$LOG_FILE"

        python3 export_shopify_csv.py "$lead_file" >> "$LOG_FILE" 2>&1

        if [ $? -eq 0 ]; then
            echo "    ✅ CSV exported" >> "$LOG_FILE"
        else
            echo "    ❌ CSV export failed" >> "$LOG_FILE"
        fi
    done
fi

###############################################################################
# PHASE 5: SUMMARY & CLEANUP
###############################################################################

echo "" >> "$LOG_FILE"
echo "======================================================================" >> "$LOG_FILE"
echo "SUMMARY - MULTI-PLATFORM CONSUMER INTELLIGENCE" >> "$LOG_FILE"
echo "======================================================================" >> "$LOG_FILE"
echo "CONSUMER INTELLIGENCE (75-80%):" >> "$LOG_FILE"
echo "  Instagram hashtags scraped: $INSTAGRAM_RESULTS/${#INSTAGRAM_HASHTAGS[@]}" >> "$LOG_FILE"
echo "  TikTok hashtags scraped: $TIKTOK_RESULTS/${#TIKTOK_HASHTAGS[@]}" >> "$LOG_FILE"
echo "  Facebook pages scraped: $FACEBOOK_RESULTS/${#FACEBOOK_PAGES[@]}" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "COMPETITOR INTELLIGENCE (20-25%):" >> "$LOG_FILE"
echo "  Google Maps queries scraped: $GMAPS_RESULTS/${#GMAPS_QUERIES[@]}" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "Completed: $TIMESTAMP" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Count total leads scraped today
TOTAL_LEADS=$(find "$SCRIPT_DIR/leads/general" -name "leads_general_*_${DATE}*.json" -type f -exec cat {} \; | grep -o '"platform"' | wc -l)
echo "✅ Total leads scraped today: $TOTAL_LEADS" >> "$LOG_FILE"

# Notification (optional - can add email/Slack later)
echo "📝 Shopify CSV files ready for import:" >> "$LOG_FILE"
find . -name "shopify_import_${DATE}*.csv" -type f >> "$LOG_FILE"

echo "" >> "$LOG_FILE"

# Exit
echo "🎉 Daily scraping complete!" >> "$LOG_FILE"
exit 0
