#!/bin/bash

# STOP HOOK - BUILD/TEST VALIDATION
# Purpose: Prevent completion if tests/builds fail
# Pattern: github.com/disler/claude-code-hooks-mastery
# Exit 2 with JSON = block completion

# Check if working on critical files
CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null)

if [ -z "$CHANGED_FILES" ]; then
    # No changes, allow completion
    exit 0
fi

# Python files changed → run syntax check
if echo "$CHANGED_FILES" | grep -qE "\.py$"; then
    echo "Validating Python syntax..." >&2

    for file in $(echo "$CHANGED_FILES" | grep "\.py$"); do
        if [ -f "$file" ]; then
            if ! python3 -m py_compile "$file" 2>/dev/null; then
                echo '{"decision": "block", "stopReason": "Python syntax errors in '"$file"'", "suppressOutput": false}' >&2
                exit 2
            fi
        fi
    done
fi

# TypeScript/JavaScript files changed → run type checking (if tsc available)
if echo "$CHANGED_FILES" | grep -qE "\.(ts|tsx)$"; then
    if command -v npx &> /dev/null && [ -f "tsconfig.json" ]; then
        echo "Validating TypeScript..." >&2

        if ! npx tsc --noEmit 2>/dev/null; then
            echo '{"decision": "block", "stopReason": "TypeScript errors detected", "suppressOutput": false}' >&2
            exit 2
        fi
    fi
fi

# Liquid template files changed → basic validation
if echo "$CHANGED_FILES" | grep -qE "\.liquid$"; then
    echo "Validating Liquid templates..." >&2

    for file in $(echo "$CHANGED_FILES" | grep "\.liquid$"); do
        if [ -f "$file" ]; then
            # Check for common syntax errors (unclosed tags)
            if grep -qE "\{\{[^}]*$|\{%[^%]*$" "$file"; then
                echo '{"decision": "block", "stopReason": "Unclosed Liquid tag in '"$file"'", "suppressOutput": false}' >&2
                exit 2
            fi
        fi
    done
fi

# All checks passed
echo "✅ Validation passed" >&2
exit 0
