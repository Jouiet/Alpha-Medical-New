#!/bin/bash
# Setup daily cron job for investor metrics auto-update

SCRIPT_PATH="/Users/mac/Desktop/Alpha-Medical/scripts/deployment/update_investor_metrics.py"
LOG_PATH="/Users/mac/Desktop/Alpha-Medical/logs/investor_metrics.log"

# Create logs directory if doesn't exist
mkdir -p "$(dirname "$LOG_PATH")"

# Check if cron job already exists
CRON_CMD="0 2 * * * /usr/bin/python3 $SCRIPT_PATH >> $LOG_PATH 2>&1"

if crontab -l 2>/dev/null | grep -q "$SCRIPT_PATH"; then
    echo "✅ Cron job already exists"
    echo "Current cron jobs:"
    crontab -l | grep "$SCRIPT_PATH"
else
    # Add cron job
    (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
    echo "✅ Cron job added successfully!"
    echo ""
    echo "Schedule: Daily at 2:00 AM"
    echo "Script: $SCRIPT_PATH"
    echo "Logs: $LOG_PATH"
    echo ""
    echo "To view cron jobs: crontab -l"
    echo "To remove cron job: crontab -e (then delete the line)"
fi

echo ""
echo "Manual execution test:"
/usr/bin/python3 "$SCRIPT_PATH"
