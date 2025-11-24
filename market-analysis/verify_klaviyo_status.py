#!/usr/bin/env python3
"""
Verify Klaviyo integration status and configuration.
FACTUAL verification using API.
"""

import os
import sys
import json
from pathlib import Path

# Load environment variables
env_file = Path(__file__).parent.parent / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

KLAVIYO_PRIVATE_KEY = os.getenv('KLAVIYO_PRIVATE_API_KEY')

if not KLAVIYO_PRIVATE_KEY:
    print("❌ KLAVIYO_PRIVATE_API_KEY not found in .env")
    sys.exit(1)

print("🔍 KLAVIYO INTEGRATION VERIFICATION\n")
print("=" * 60)

try:
    import requests
except ImportError:
    print("❌ requests module not installed. Run: pip install requests")
    sys.exit(1)

headers = {
    'Authorization': f'Klaviyo-API-Key {KLAVIYO_PRIVATE_KEY}',
    'revision': '2024-10-15',
    'Accept': 'application/json'
}

# 1. Verify API connection
print("\n📊 API CONNECTION:")
try:
    response = requests.get('https://a.klaviyo.com/api/accounts/', headers=headers)
    if response.status_code == 200:
        account = response.json()['data'][0]
        print(f"  ✅ Connected to Klaviyo account")
        print(f"  Account ID: {account['id']}")
        print(f"  Test mode: {account['attributes'].get('test_account', False)}")
    else:
        print(f"  ❌ API connection failed: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# 2. Check lists
print("\n📋 LISTS:")
try:
    response = requests.get('https://a.klaviyo.com/api/lists/', headers=headers)
    if response.status_code == 200:
        lists_data = response.json()
        lists = lists_data.get('data', [])
        print(f"  Total lists: {len(lists)}")
        for lst in lists[:5]:  # Show first 5
            name = lst['attributes']['name']
            profile_count = lst['attributes'].get('profile_count', 0)
            print(f"    - {name}: {profile_count} profiles")
    else:
        print(f"  ⚠️  Could not fetch lists: {response.status_code}")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 3. Check flows
print("\n🔄 FLOWS (Email Automation):")
try:
    response = requests.get('https://a.klaviyo.com/api/flows/', headers=headers)
    if response.status_code == 200:
        flows_data = response.json()
        flows = flows_data.get('data', [])
        print(f"  Total flows: {len(flows)}")
        for flow in flows:
            name = flow['attributes']['name']
            status = flow['attributes']['status']
            trigger = flow['attributes'].get('trigger_type', 'N/A')
            print(f"    - {name}: {status} (trigger: {trigger})")
    else:
        print(f"  ⚠️  Could not fetch flows: {response.status_code}")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 4. Check segments
print("\n👥 SEGMENTS:")
try:
    response = requests.get('https://a.klaviyo.com/api/segments/', headers=headers)
    if response.status_code == 200:
        segments_data = response.json()
        segments = segments_data.get('data', [])
        print(f"  Total segments: {len(segments)}")
        for segment in segments[:5]:  # Show first 5
            name = segment['attributes']['name']
            profile_count = segment['attributes'].get('profile_count', 0)
            print(f"    - {name}: {profile_count} profiles")
    else:
        print(f"  ⚠️  Could not fetch segments: {response.status_code}")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 5. Check integrations
print("\n🔌 INTEGRATIONS:")
try:
    response = requests.get('https://a.klaviyo.com/api/integrations/', headers=headers)
    if response.status_code == 200:
        integrations_data = response.json()
        integrations = integrations_data.get('data', [])
        print(f"  Total integrations: {len(integrations)}")
        for integration in integrations:
            name = integration['attributes'].get('name', 'Unknown')
            category = integration['attributes'].get('category', 'Unknown')
            print(f"    - {name} ({category})")

        # Check specifically for Shopify
        shopify_integration = [i for i in integrations if 'shopify' in i['attributes'].get('name', '').lower()]
        if shopify_integration:
            print(f"\n  ✅ Shopify integration ACTIVE")
        else:
            print(f"\n  ⚠️  Shopify integration NOT found in API response")
            print(f"     (May require manual verification in Klaviyo dashboard)")
    else:
        print(f"  ⚠️  Could not fetch integrations: {response.status_code}")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

# 6. Check campaigns
print("\n📧 CAMPAIGNS:")
try:
    response = requests.get('https://a.klaviyo.com/api/campaigns/', headers=headers)
    if response.status_code == 200:
        campaigns_data = response.json()
        campaigns = campaigns_data.get('data', [])
        print(f"  Total campaigns: {len(campaigns)}")

        # Group by status
        statuses = {}
        for campaign in campaigns:
            status = campaign['attributes']['status']
            statuses[status] = statuses.get(status, 0) + 1

        for status, count in statuses.items():
            print(f"    {status}: {count}")
    else:
        print(f"  ⚠️  Could not fetch campaigns: {response.status_code}")
except Exception as e:
    print(f"  ⚠️  Error: {e}")

print("\n" + "=" * 60)
print("\n✅ KLAVIYO VERIFICATION COMPLETE")
print("\nFACTUAL STATUS:")
print("  - API credentials: ✅ Valid and working")
print("  - Account connection: ✅ Active")
print("  - Lists, Flows, Segments: See counts above")
print("  - Shopify integration: See integrations section above")
