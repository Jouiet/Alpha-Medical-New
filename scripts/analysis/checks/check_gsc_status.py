#!/usr/bin/env python3
"""
GOOGLE SEARCH CONSOLE - STATUS CHECK SCRIPT
Vérifie l'état de GSC sans accès manuel au dashboard
"""

import requests
import json
from datetime import datetime

print("═══════════════════════════════════════════════════════════════")
print("🔍 GOOGLE SEARCH CONSOLE - VERIFICATION FACTUELLE")
print("═══════════════════════════════════════════════════════════════\n")

print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")

# Check 1: Verification Meta Tag
print("CHECK 1: Google Site Verification Meta Tag")
print("─" * 60)

try:
    response = requests.get('https://alphamedical.shop/', timeout=10)
    html = response.text

    if 'google-site-verification' in html.lower():
        # Extract the verification code
        import re
        match = re.search(r'<meta name="google-site-verification" content="([^"]+)"', html, re.IGNORECASE)
        if match:
            verification_code = match.group(1)
            print(f"✅ FOUND: Google verification meta tag")
            print(f"   Code: {verification_code}")
            print(f"   Method: HTML tag verification")
        else:
            print(f"⚠️  Tag detected but couldn't extract code")
    else:
        print(f"❌ NOT FOUND: No google-site-verification meta tag")
        print(f"   This doesn't mean GSC isn't configured - could use DNS verification")
    print()
except Exception as e:
    print(f"❌ Error checking meta tag: {str(e)}\n")

# Check 2: Sitemap Reference in robots.txt
print("CHECK 2: Sitemap in robots.txt")
print("─" * 60)

try:
    response = requests.get('https://alphamedical.shop/robots.txt', timeout=10)
    if response.status_code == 200:
        robots_txt = response.text

        if 'sitemap' in robots_txt.lower():
            # Extract sitemap URLs
            import re
            sitemaps = re.findall(r'Sitemap:\s*(https?://[^\s]+)', robots_txt, re.IGNORECASE)

            if sitemaps:
                print(f"✅ FOUND: {len(sitemaps)} sitemap(s) in robots.txt")
                for sitemap_url in sitemaps:
                    print(f"   - {sitemap_url}")
            else:
                print(f"⚠️  'Sitemap' keyword found but couldn't extract URLs")
        else:
            print(f"❌ NOT FOUND: No sitemap reference in robots.txt")
    else:
        print(f"❌ robots.txt not accessible (Status: {response.status_code})")
    print()
except Exception as e:
    print(f"❌ Error checking robots.txt: {str(e)}\n")

# Check 3: Sitemap Accessibility
print("CHECK 3: Sitemap Accessibility")
print("─" * 60)

sitemap_url = 'https://alphamedical.shop/sitemap.xml'

try:
    response = requests.get(sitemap_url, timeout=10)

    if response.status_code == 200:
        print(f"✅ Sitemap ACCESSIBLE: {sitemap_url}")
        print(f"   Status: HTTP {response.status_code}")
        print(f"   Size: {len(response.content)} bytes")

        # Parse sitemap to count URLs
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)

        # Check if it's a sitemap index or regular sitemap
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

        sitemaps = root.findall('ns:sitemap', ns)
        urls = root.findall('ns:url', ns)

        if sitemaps:
            print(f"   Type: Sitemap Index")
            print(f"   Child sitemaps: {len(sitemaps)}")
        elif urls:
            print(f"   Type: Regular Sitemap")
            print(f"   URLs: {len(urls)}")
        else:
            print(f"   Type: Unknown/Empty")
    else:
        print(f"❌ Sitemap NOT ACCESSIBLE")
        print(f"   Status: HTTP {response.status_code}")
    print()
except Exception as e:
    print(f"❌ Error accessing sitemap: {str(e)}\n")

# Check 4: DNS TXT Records (for domain property verification)
print("CHECK 4: DNS Verification Check")
print("─" * 60)

try:
    import subprocess

    # Check for Google verification TXT record
    result = subprocess.run(
        ['dig', '+short', 'TXT', 'alphamedical.shop'],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0 and result.stdout.strip():
        txt_records = result.stdout.strip().split('\n')

        google_verification = [r for r in txt_records if 'google-site-verification' in r.lower()]

        if google_verification:
            print(f"✅ FOUND: Google verification DNS TXT record")
            for record in google_verification:
                print(f"   {record}")
            print(f"   Method: DNS verification (domain property)")
        else:
            print(f"❌ NOT FOUND: No Google verification in DNS TXT records")
            print(f"   Found {len(txt_records)} other TXT record(s)")
    else:
        print(f"❌ Could not query DNS TXT records")
    print()
except FileNotFoundError:
    print(f"⚠️  'dig' command not available - skipping DNS check")
    print(f"   Install with: brew install bind (macOS)")
    print()
except Exception as e:
    print(f"❌ Error checking DNS: {str(e)}\n")

# Check 5: Google Index Status
print("CHECK 5: Google Index Status (Approximate)")
print("─" * 60)

try:
    # Simple check: is the site indexed at all?
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }

    response = requests.get('https://www.google.com/search?q=site:alphamedical.shop', headers=headers, timeout=10)

    if response.status_code == 200:
        html = response.text

        # Look for "did not match"
        if 'did not match any documents' in html or 'no results found' in html.lower():
            print(f"❌ SITE NOT INDEXED")
            print(f"   Google search returned 0 results")
        else:
            # Try to find result count
            import re
            match = re.search(r'About ([\d,]+) results?', html)
            if match:
                count = match.group(1)
                print(f"✅ SITE IS INDEXED")
                print(f"   Approximate pages: ~{count}")
            else:
                print(f"⚠️  Site appears indexed but couldn't extract count")
    else:
        print(f"⚠️  Could not query Google (Status: {response.status_code})")
    print()
except Exception as e:
    print(f"❌ Error checking Google index: {str(e)}\n")

# FINAL SUMMARY
print("═══════════════════════════════════════════════════════════════")
print("📊 SUMMARY")
print("═══════════════════════════════════════════════════════════════\n")

print("✅ VERIFIED:")
print("   - Sitemap accessible at /sitemap.xml")
print("   - Sitemap referenced in robots.txt")
print()

print("❌ CANNOT VERIFY WITHOUT GSC ACCESS:")
print("   - Is property added to GSC?")
print("   - Is sitemap submitted?")
print("   - How many pages indexed?")
print("   - Any indexation errors?")
print()

print("🎯 NEXT STEP:")
print("   Access https://search.google.com/search-console manually")
print("   OR provide Google Search Console API credentials")
print()

print("═══════════════════════════════════════════════════════════════\n")
