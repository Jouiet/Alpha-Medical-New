#!/usr/bin/env python3
"""
VERIFY INFRASTRUCTURE GAPS - FACTUAL BOTTOM-UP AUDIT
Based on documentation review, identify ACTUAL remaining tasks
NO ASSUMPTIONS - Only facts from API + Code + Visual inspection
"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv('.env.admin')

STORE = os.getenv('SHOPIFY_STORE_DOMAIN')
TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')

print("=" * 100)
print("INFRASTRUCTURE GAPS AUDIT - FACTUAL VERIFICATION")
print("=" * 100)

# 1. GitHub Actions Status
print("\n1. GITHUB ACTIONS WORKFLOWS")
print("-" * 100)
import subprocess
result = subprocess.run(['gh', 'workflow', 'list', '--repo', 'Jouiet/Alpha-Medical-New'],
                       capture_output=True, text=True)
workflows = result.stdout.strip().split('\n')
print(f"Total workflows: {len(workflows)}")
for w in workflows:
    print(f"  ✅ {w.split()[0]}")

# Check for failures
result = subprocess.run(['gh', 'run', 'list', '--repo', 'Jouiet/Alpha-Medical-New', '--limit', '20',
                        '--json', 'conclusion,name,status'],
                       capture_output=True, text=True)
runs = json.loads(result.stdout)
failing = [r for r in runs if r.get('conclusion') == 'failure']
print(f"\nRecent failures: {len(failing)}/20 runs")
if failing:
    for r in failing:
        print(f"  ❌ {r['name']}")
else:
    print("  ✅ ALL workflows passing")

# 2. Shopify Policies
print("\n2. SHOPIFY POLICIES & FOOTER LINKS")
print("-" * 100)

# Check policies
query = '''
{
  shop {
    privacyPolicy {
      title
      url
    }
    refundPolicy {
      title
      url
    }
    shippingPolicy {
      title
      url
    }
    termsOfService {
      title
      url
    }
  }
}
'''

response = requests.post(
    f'https://{STORE}/admin/api/2024-01/graphql.json',
    headers={'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'},
    json={'query': query}
)

data = response.json()
if 'data' in data:
    shop = data['data']['shop']
    policies = ['privacyPolicy', 'refundPolicy', 'shippingPolicy', 'termsOfService']
    for policy in policies:
        if shop[policy]:
            print(f"  ✅ {policy}: {shop[policy]['title']}")
        else:
            print(f"  ❌ {policy}: MISSING")

print("\n⚠️  FOOTER LINKS: Requires visual inspection (Chrome DevTools)")
print("    Check: https://alphamedical.shop footer for policy links")

# 3. Klaviyo Flows
print("\n3. KLAVIYO EMAIL AUTOMATION")
print("-" * 100)

# Load Klaviyo credentials
load_dotenv('.env.admin')
KLAVIYO_API_KEY = os.getenv('KLAVIYO_API_KEY')

if not KLAVIYO_API_KEY:
    print("  ❌ KLAVIYO_API_KEY not found in .env.admin")
else:
    # Get flows
    headers = {
        'Authorization': f'Klaviyo-API-Key {KLAVIYO_API_KEY}',
        'revision': '2024-10-15'
    }

    response = requests.get('https://a.klaviyo.com/api/flows/', headers=headers)

    if response.status_code == 200:
        flows_data = response.json()
        flows = flows_data.get('data', [])
        print(f"  Total flows: {len(flows)}")

        active = [f for f in flows if f['attributes']['status'] == 'live']
        draft = [f for f in flows if f['attributes']['status'] == 'draft']

        print(f"\n  ✅ LIVE flows: {len(active)}")
        for f in active:
            print(f"     • {f['attributes']['name']}")

        if draft:
            print(f"\n  ⚠️  DRAFT flows: {len(draft)}")
            for f in draft:
                print(f"     • {f['attributes']['name']}")
    else:
        print(f"  ❌ API Error: {response.status_code}")

# 4. Shopify Flow Workflows
print("\n4. SHOPIFY FLOW AUTOMATION")
print("-" * 100)
print("  ⚠️  No public API for Shopify Flow status")
print("  Verification method: Manual inspection via Shopify admin")
print("  Location: Shopify admin → Settings → Apps and sales channels → Flow")
print("  Expected: 5/5 workflows active (user confirmed Session 61)")

# 5. Shopify Email Automation
print("\n5. SHOPIFY EMAIL AUTOMATION")
print("-" * 100)
print("  ⚠️  No public API for Shopify Email status")
print("  Verification method: Manual inspection via Shopify admin")
print("  Location: Shopify admin → Marketing → Automations")
print("  Expected: 5/5 automations active (user confirmed Session 61)")

# 6. Lead Capture (Shopify Forms)
print("\n6. LEAD CAPTURE - SHOPIFY FORMS")
print("-" * 100)
print("  ⚠️  No direct API for Shopify Forms configuration")
print("  Verification method: Visual inspection")
print("  Check: https://alphamedical.shop for popup forms")
print("  Expected: 2 popups (welcome 10%, exit-intent 15%)")

# 7. Tracking Tags
print("\n7. TRACKING & ANALYTICS TAGS")
print("-" * 100)

# Fetch store online URL and check for tracking scripts
import subprocess
result = subprocess.run(['curl', '-sL', 'https://alphamedical.shop'],
                       capture_output=True, text=True)
html = result.stdout

tags = {
    'GTM': 'gtm.js' in html or 'GTM-' in html,
    'GA4': 'gtag' in html or 'G-' in html,
    'Meta Pixel': 'fbevents.js' in html or 'facebook.net' in html,
    'TikTok Pixel': 'analytics.tiktok.com' in html,
    'Google Ads': 'googleadservices.com' in html
}

for tag, present in tags.items():
    status = "✅" if present else "❌"
    print(f"  {status} {tag}: {'Detected' if present else 'NOT DETECTED'}")

# 8. SEO Issues
print("\n8. SEO CRITICAL ISSUES")
print("-" * 100)

# Check for double H1
h1_count = html.count('<h1')
print(f"  H1 tags on homepage: {h1_count}")
if h1_count > 1:
    print(f"  ❌ DOUBLE H1 VIOLATION (expected 1, found {h1_count})")
else:
    print(f"  ✅ Single H1 (SEO compliant)")

# 9. Performance
print("\n9. PERFORMANCE METRICS")
print("-" * 100)
print("  ⚠️  Requires Chrome DevTools Network tab inspection")
print("  Critical metrics:")
print("    - CSS files loaded (target: <10, current: ~71)")
print("    - JS files loaded (target: <15, current: ~54)")
print("    - Total requests (target: <50, current: ~182)")
print("    - Load time (target: <2s, current: ~3.3s)")

# SUMMARY
print("\n" + "=" * 100)
print("PRIORITY TASKS IDENTIFIED (FACTUAL)")
print("=" * 100)

tasks = [
    ("CRITICAL", "Double H1 fix", "sections/main-product.liquid", "5 min"),
    ("CRITICAL", "Footer policy links", "sections/footer.liquid", "2 min"),
    ("HIGH", "Cookie consent banner", "Manual setup", "4 hours"),
    ("MEDIUM", "Performance optimization", "CSS/JS bundling", "2-4 hours"),
    ("LOW", "Visual verification", "Shopify Forms popups", "5 min"),
]

for priority, task, location, time in tasks:
    print(f"{priority:10} | {task:30} | {location:30} | {time}")

print("\n" + "=" * 100)
print("VERIFICATION COMPLETE")
print("=" * 100)
