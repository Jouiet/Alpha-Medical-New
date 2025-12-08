#!/usr/bin/env python3
"""
VERIFICATION FACTUELLE COMPLÈTE - All 7 Investor Pages
Bottom-up verification: API check of all pages + features
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

# All 7 investor pages
PAGES = [
    {'handle': 'investors', 'title': 'Investor Relations (Main Hub)'},
    {'handle': 'investors-ai-development', 'title': 'AI Development'},
    {'handle': 'investors-automation-deployed', 'title': 'Automation Deployed'},
    {'handle': 'investors-automation-roadmap', 'title': 'Automation Roadmap'},
    {'handle': 'investors-analytics', 'title': 'Analytics'},
    {'handle': 'investors-flywheel', 'title': 'Flywheel'},
    {'handle': 'investors-technology-stack', 'title': 'Technology Stack'}
]

def get_page(handle):
    """Get page via Admin API"""
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    params = {'handle': handle}

    response = requests.get(url, headers=headers, params=params)
    pages = response.json().get('pages', [])

    return pages[0] if pages else None

def check_page_features(page_handle, page_html):
    """Check for specific features in page HTML"""
    features = {
        'password_protection': False,
        'navigation': False,
        'branding': False,
        'chartjs': False,
        'claude_role': False
    }

    html_lower = page_html.lower()

    # Check password protection (SHA-256 hash)
    if 'investorpasswordoverlay' in html_lower and 'e9a9d74a894227d131bab78a5ea1a05dc5482a614c7ac3a9d4d8f9a9c79ec887' in html_lower:
        features['password_protection'] = True

    # Check navigation
    if 'investor-breadcrumb' in html_lower or 'investor-subnav' in html_lower:
        features['navigation'] = True

    # Check branding (Alpha Medical colors)
    if '#4770db' in html_lower or 'var(--am-primary)' in html_lower:
        features['branding'] = True

    # Check Chart.js (only on analytics, flywheel, tech stack pages)
    if page_handle in ['investors-analytics', 'investors-flywheel', 'investors-technology-stack']:
        if 'chart.js' in html_lower or 'new Chart(' in page_html:
            features['chartjs'] = True

    # Check Claude role section
    if 'claude' in html_lower and ('ai development partner' in html_lower or 'sonnet' in html_lower):
        features['claude_role'] = True

    return features

print("="*70)
print("VERIFICATION FACTUELLE - ALL INVESTOR PAGES")
print("="*70)

results = []

for page_info in PAGES:
    handle = page_info['handle']
    title = page_info['title']

    print(f"\n{len(results)+1}. {title}")
    print("-" * 70)

    page = get_page(handle)

    if not page:
        print(f"  ❌ PAGE NOT FOUND")
        results.append({
            'handle': handle,
            'title': title,
            'exists': False,
            'published': False,
            'features': {}
        })
        continue

    # Check basic info
    print(f"  Page ID: {page['id']}")
    print(f"  Handle: {page['handle']}")
    print(f"  Title: {page['title']}")
    print(f"  Published: {'✅ Yes' if page.get('published_at') else '❌ No'}")
    print(f"  URL: https://alphamedical.shop/pages/{page['handle']}")

    # Check features
    features = check_page_features(handle, page.get('body_html', ''))

    print(f"\n  Features:")
    print(f"    - Password protection: {'✅' if features['password_protection'] else '❌'}")
    print(f"    - Navigation: {'✅' if features['navigation'] else '❌'}")
    print(f"    - Branding (Alpha colors): {'✅' if features['branding'] else '❌'}")

    if handle in ['investors-analytics', 'investors-flywheel', 'investors-technology-stack']:
        print(f"    - Chart.js visualizations: {'✅' if features['chartjs'] else '❌'}")

    if handle != 'investors':  # Main page doesn't need Claude role (has other sections)
        print(f"    - Claude role section: {'✅' if features['claude_role'] else '⚠️ Not required'}")

    results.append({
        'handle': handle,
        'title': title,
        'exists': True,
        'published': page.get('published_at') is not None,
        'features': features
    })

# SUMMARY
print("\n" + "="*70)
print("VERIFICATION SUMMARY")
print("="*70)

total_pages = len(PAGES)
pages_exist = sum(1 for r in results if r['exists'])
pages_published = sum(1 for r in results if r.get('published'))

print(f"\nPages:")
print(f"  Total: {total_pages}")
print(f"  Exist: {pages_exist}/{total_pages}")
print(f"  Published: {pages_published}/{total_pages}")

# Feature checks
password_protected = sum(1 for r in results if r.get('features', {}).get('password_protection'))
has_navigation = sum(1 for r in results if r.get('features', {}).get('navigation'))
has_branding = sum(1 for r in results if r.get('features', {}).get('branding'))

print(f"\nFeatures:")
print(f"  Password protection: {password_protected}/{total_pages} pages")
print(f"  Navigation: {has_navigation}/{total_pages} pages")
print(f"  Branding: {has_branding}/{total_pages} pages")

# Chart.js pages
chart_pages = [r for r in results if r['handle'] in ['investors-analytics', 'investors-flywheel', 'investors-technology-stack']]
chart_pages_with_charts = sum(1 for r in chart_pages if r.get('features', {}).get('chartjs'))
print(f"  Chart.js (3 pages): {chart_pages_with_charts}/3 pages")

# Overall status
all_published = pages_published == total_pages
all_password_protected = password_protected == total_pages
all_navigation = has_navigation == total_pages
all_branding = has_branding == total_pages
all_charts = chart_pages_with_charts == 3

print("\n" + "="*70)

if all_published and all_password_protected and all_navigation and all_branding and all_charts:
    print("✅ ALL VERIFICATIONS PASSED - INVESTOR PAGES 100% COMPLETE")
    print("="*70)
    print("\nInvestor Pages Status:")
    print("  ✅ 7/7 pages LIVE and published")
    print("  ✅ 7/7 pages password-protected (SHA-256)")
    print("  ✅ 7/7 pages with navigation (breadcrumb + menu)")
    print("  ✅ 7/7 pages with brand compliance (Alpha colors)")
    print("  ✅ 3/3 pages with Chart.js visualizations")
    print("\nAccess:")
    print("  URL: https://alphamedical.shop/pages/investors")
    print("  Password: [SHA-256 protected]")
else:
    print("⚠️  SOME VERIFICATIONS FAILED")
    print("="*70)
    print("\nIssues:")
    if not all_published:
        print(f"  ❌ Only {pages_published}/{total_pages} pages published")
    if not all_password_protected:
        print(f"  ❌ Only {password_protected}/{total_pages} pages password-protected")
    if not all_navigation:
        print(f"  ❌ Only {has_navigation}/{total_pages} pages with navigation")
    if not all_branding:
        print(f"  ❌ Only {has_branding}/{total_pages} pages with branding")
    if not all_charts:
        print(f"  ❌ Only {chart_pages_with_charts}/3 chart pages with Chart.js")

print()
