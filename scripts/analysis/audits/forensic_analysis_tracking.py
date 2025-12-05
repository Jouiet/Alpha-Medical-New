#!/usr/bin/env python3
"""
ALPHA MEDICAL - TRACKING & ANALYTICS FORENSIC ANALYSIS
Verify GTM, GA4, Meta Pixel, TikTok Pixel implementation in theme
"""

import os
import re
from pathlib import Path

def scan_file_for_tracking(file_path):
    """Scan a file for tracking codes"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

            findings = {}

            # Google Tag Manager
            if 'GTM-' in content or 'googletagmanager.com' in content:
                gtm_ids = re.findall(r'GTM-[A-Z0-9]+', content)
                findings['GTM'] = list(set(gtm_ids))

            # Google Analytics 4
            if 'G-' in content or 'analytics.google.com' in content or 'gtag' in content:
                ga4_ids = re.findall(r'G-[A-Z0-9]+', content)
                findings['GA4'] = list(set(ga4_ids))

            # Meta/Facebook Pixel
            if 'facebook' in content.lower() or 'fbq' in content or 'connect.facebook.net' in content:
                fb_ids = re.findall(r'fbq\([\'"]init[\'"],\s*[\'"](\d+)[\'"]', content)
                if not fb_ids:
                    fb_ids = re.findall(r'facebook\.com/tr\?id=(\d+)', content)
                findings['Meta Pixel'] = list(set(fb_ids))

            # TikTok Pixel
            if 'tiktok' in content.lower() or 'ttq' in content or 'analytics.tiktok.com' in content:
                tt_ids = re.findall(r'ttq\.load\([\'"]([A-Z0-9]+)[\'"]', content)
                if not tt_ids:
                    tt_ids = re.findall(r'tiktok_pixel_id[\'"]?\s*[:=]\s*[\'"]([A-Z0-9]+)[\'"]', content, re.IGNORECASE)
                findings['TikTok Pixel'] = list(set(tt_ids))

            # Google Ads Conversion
            if 'google_conversion' in content.lower() or 'AW-' in content:
                gads_ids = re.findall(r'AW-[0-9]+', content)
                findings['Google Ads'] = list(set(gads_ids))

            # Klaviyo
            if 'klaviyo' in content.lower():
                findings['Klaviyo'] = ['Found']

            # Loox (Reviews)
            if 'loox' in content.lower():
                findings['Loox'] = ['Found']

            # Judge.me (Reviews)
            if 'judge.me' in content.lower() or 'judgeme' in content.lower():
                findings['Judge.me'] = ['Found']

            # Tidio (Chat)
            if 'tidio' in content.lower():
                findings['Tidio'] = ['Found']

            return findings if findings else None
    except Exception as e:
        return None

def main():
    print("=" * 80)
    print("ALPHA MEDICAL - TRACKING & ANALYTICS FORENSIC ANALYSIS")
    print("=" * 80)
    print()

    # Scan theme files
    theme_dirs = [
        './layout',
        './templates',
        './snippets',
        './sections',
        './assets'
    ]

    all_findings = {}

    for theme_dir in theme_dirs:
        if not os.path.exists(theme_dir):
            continue

        print(f"Scanning {theme_dir}/...")

        for root, dirs, files in os.walk(theme_dir):
            for file in files:
                if file.endswith(('.liquid', '.js', '.html')):
                    file_path = os.path.join(root, file)
                    findings = scan_file_for_tracking(file_path)

                    if findings:
                        rel_path = os.path.relpath(file_path)
                        for tracker, values in findings.items():
                            if tracker not in all_findings:
                                all_findings[tracker] = {}
                            if rel_path not in all_findings[tracker]:
                                all_findings[tracker][rel_path] = values

    # Print results
    print()
    print("=" * 80)
    print("TRACKING IMPLEMENTATIONS FOUND")
    print("=" * 80)

    for tracker in sorted(all_findings.keys()):
        print(f"\n{tracker}:")
        for file_path, values in all_findings[tracker].items():
            if values and values != ['Found']:
                print(f"  - {file_path}: {', '.join(values)}")
            else:
                print(f"  - {file_path}")

    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Tracking Systems Found: {len(all_findings)}")
    for tracker in sorted(all_findings.keys()):
        file_count = len(all_findings[tracker])
        print(f"  - {tracker}: {file_count} file(s)")

    print()
    print("=" * 80)
    print("FORENSIC ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
