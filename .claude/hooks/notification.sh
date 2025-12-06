#!/bin/bash

# NOTIFICATION HOOK - LOGGING
# Purpose: Log all notifications for debugging
# Pattern: github.com/disler/claude-code-hooks-mastery

NOTIFICATION="$1"
LOG_FILE=".claude/logs/notifications.json"

# Create logs directory if not exists
mkdir -p .claude/logs 2>/dev/null

# Append notification to log
TIMESTAMP=$(date -Iseconds 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")
echo "{\"timestamp\": \"$TIMESTAMP\", \"notification\": \"$NOTIFICATION\"}" >> "$LOG_FILE" 2>/dev/null

# Optional: TTS for critical notifications (macOS only, commented out by default)
# if [[ "$NOTIFICATION" =~ (error|failed|critical|blocked) ]]; then
#     say "Alert: $NOTIFICATION" &
# fi

exit 0
