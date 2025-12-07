#!/usr/bin/env python3
"""
REMOVE duplicate Investor Relations section at bottom of footer
Keep: Conditional link in COMPANY column (lines 104-108)
Remove: Isolated "Investors" section at bottom (lines 288-291)
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'
theme_id = 140069830733

def get_footer():
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    response = requests.get(url, headers=headers, params={'asset[key]': 'sections/footer.liquid'})
    return response.json()['asset']['value']

def update_footer(content):
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    data = {'asset': {'key': 'sections/footer.liquid', 'value': content}}
    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200

# Get footer
footer = get_footer()

print("Searching for isolated 'Investors' section to remove...")

# Find the isolated Investors section (the one at the bottom)
# Pattern: <div> with "Investors" heading and "Investor Relations" link
# This is the section that appears around line 288

# Strategy: Find the exact block structure
# Look for the pattern that starts with opening div and has "Investors" heading

lines = footer.split('\n')
start_line = None
end_line = None

for i, line in enumerate(lines):
    # Look for the isolated Investors heading (not the one in COMPANY column)
    if 'Investors</h2>' in line and 'footer-block__heading' in line:
        # This is line 288, the heading
        # Now go backwards to find the opening div
        for j in range(i, max(0, i-10), -1):
            if '<div' in lines[j] and 'footer' in lines[j]:
                start_line = j
                break

        # Go forward to find the closing divs
        if start_line is not None:
            # Find matching closing tags
            div_count = 0
            for k in range(start_line, len(lines)):
                if '<div' in lines[k]:
                    div_count += 1
                if '</div>' in lines[k]:
                    div_count -= 1
                    if div_count == 0:
                        end_line = k
                        break
        break

if start_line is not None and end_line is not None:
    print(f"\n✅ Found isolated 'Investors' section:")
    print(f"   Lines {start_line+1} to {end_line+1}")
    print(f"\nContent to remove:")
    for i in range(start_line, min(end_line+1, start_line+15)):
        print(f"   {i+1}: {lines[i][:80]}")

    # Remove the section
    # Join all lines except the ones we want to remove
    new_lines = lines[:start_line] + lines[end_line+1:]
    footer = '\n'.join(new_lines)

    # Verify removal
    if 'Investors</h2>' not in footer:
        print("\n✅ Section removed from content")

        # Count remaining "Investor" occurrences
        import re
        remaining = []
        for i, line in enumerate(footer.split('\n'), 1):
            if re.search(r'investor', line, re.IGNORECASE):
                remaining.append((i, line.strip()[:60]))

        print(f"\nRemaining 'investor' occurrences: {len(remaining)}")
        for line_num, text in remaining:
            print(f"   Line {line_num}: {text}")

        if len(remaining) <= 3:  # Should only be the COMPANY column link (3 lines: comment + link + text)
            print("\n✅ Verification passed - only COMPANY column link remains")

            # Save preview
            with open('/tmp/footer_no_duplicate.liquid', 'w') as f:
                f.write(footer)

            # Update Shopify
            print("\nUpdating Shopify...")
            if update_footer(footer):
                print("\n" + "="*70)
                print("✅ DUPLICATION REMOVED - Footer cleaned")
                print("="*70)
                print("\nResult:")
                print("  ❌ Removed: Isolated 'Investors' section at bottom")
                print("  ✅ Kept: 'Investor Relations' link in COMPANY column")
                print("\nFooter now has only ONE instance of Investor Relations:")
                print("  → COMPANY column (4th item)")
                print("\nVerify: https://alphamedical.shop")
            else:
                print("\n❌ Failed to update Shopify")
        else:
            print(f"\n⚠️ Warning: Found {len(remaining)} occurrences (expected ≤3)")
            print("Review /tmp/footer_no_duplicate.liquid before deploying")
    else:
        print("\n❌ Section still present after removal attempt")
else:
    print("\n❌ Could not locate isolated 'Investors' section")
    print("\nManual inspection required")
