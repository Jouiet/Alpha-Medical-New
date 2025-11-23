#!/bin/bash
###############################################################################
# CRON JOB SETUP - Alpha Medical Lead Generation
#
# This script automates the setup of the daily lead scraping cron job
#
# Usage:
#   chmod +x setup_cron_job.sh
#   ./setup_cron_job.sh
#
# What it does:
#   1. Backs up existing crontab
#   2. Adds daily lead scraping job (9:00 AM)
#   3. Verifies installation
###############################################################################

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}ALPHA MEDICAL - CRON JOB SETUP${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""

# Get script directory (absolute path)
SCRIPT_DIR="/Users/mac/Desktop/Alpha-Medical/market-analysis"
DAILY_SCRIPT="$SCRIPT_DIR/daily_lead_scraping.sh"

# Check if daily script exists
if [ ! -f "$DAILY_SCRIPT" ]; then
    echo -e "${RED}❌ ERROR: daily_lead_scraping.sh not found at:${NC}"
    echo -e "${RED}   $DAILY_SCRIPT${NC}"
    exit 1
fi

# Make daily script executable
chmod +x "$DAILY_SCRIPT"
echo -e "${GREEN}✅ Made daily_lead_scraping.sh executable${NC}"

# Backup existing crontab
BACKUP_FILE="$SCRIPT_DIR/crontab_backup_$(date +%Y%m%d_%H%M%S).txt"
crontab -l > "$BACKUP_FILE" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backed up existing crontab to: $BACKUP_FILE${NC}"
else
    echo -e "${YELLOW}⚠️  No existing crontab found (this is OK if first time)${NC}"
    touch "$BACKUP_FILE"
fi

# Create new crontab entry
CRON_ENTRY="0 9 * * * $DAILY_SCRIPT >> $SCRIPT_DIR/scraping_log.txt 2>&1"

# Check if entry already exists
crontab -l 2>/dev/null | grep -F "$DAILY_SCRIPT" > /dev/null
if [ $? -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Cron job already exists. Skipping...${NC}"
    echo ""
    echo -e "${GREEN}Current cron jobs:${NC}"
    crontab -l | grep -F "$DAILY_SCRIPT"
else
    # Add new entry to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    echo -e "${GREEN}✅ Added cron job: Daily lead scraping at 9:00 AM${NC}"
fi

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}VERIFICATION${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""

# Verify crontab
echo -e "${GREEN}Current crontab (Alpha Medical entries):${NC}"
crontab -l | grep -F "$SCRIPT_DIR" || echo -e "${YELLOW}No entries found${NC}"

echo ""
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}SETUP COMPLETE!${NC}"
echo -e "${GREEN}============================================================${NC}"
echo ""
echo -e "${GREEN}Cron job configured:${NC}"
echo -e "  Schedule: 9:00 AM daily"
echo -e "  Script:   $DAILY_SCRIPT"
echo -e "  Log file: $SCRIPT_DIR/scraping_log.txt"
echo ""
echo -e "${YELLOW}To test the script manually:${NC}"
echo -e "  $DAILY_SCRIPT"
echo ""
echo -e "${YELLOW}To view cron logs:${NC}"
echo -e "  tail -f $SCRIPT_DIR/scraping_log.txt"
echo ""
echo -e "${YELLOW}To remove the cron job:${NC}"
echo -e "  crontab -e"
echo -e "  (then delete the line containing: $DAILY_SCRIPT)"
echo ""
