#!/bin/bash

# USER-PROMPT-SUBMIT HOOK - SKILL AUTO-ACTIVATION
# Purpose: Auto-activate skills/agents based on prompt analysis (zero-friction)
# Pattern: github.com/diet103/claude-code-infrastructure-showcase
# Exit 2 = blocking suggestion, Exit 0 = continue

PROMPT="$1"

# SEO-related tasks → seo-optimizer skill
if [[ "$PROMPT" =~ (SEO|meta|keyword|content.optimization|schema|heading|title.tag) ]]; then
    echo '{"suggested_skill": "seo-optimizer", "reason": "SEO optimization task detected"}' >&2
    exit 2
fi

# Brand-related tasks → brand-guidelines skill
if [[ "$PROMPT" =~ (brand|visual|messaging|voice|guideline|color|font|typography|logo) ]]; then
    echo '{"suggested_skill": "brand-guidelines", "reason": "Brand consistency task detected"}' >&2
    exit 2
fi

# Automation tasks → automation-specialist agent
if [[ "$PROMPT" =~ (automation|workflow|Shopify.Flow|GitHub.Action|API|integration) ]]; then
    echo '{"agent": "automation-specialist", "reason": "Automation task detected"}' >&2
    exit 2
fi

# Marketing tasks → marketing-specialist agent
if [[ "$PROMPT" =~ (marketing|email|campaign|ad.copy|Klaviyo|flow|template) ]]; then
    echo '{"agent": "marketing-specialist", "reason": "Marketing task detected"}' >&2
    exit 2
fi

# Default: continue without suggestion
exit 0
