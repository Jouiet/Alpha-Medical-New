#!/usr/bin/env python3
"""
ALPHA MEDICAL - KLAVIYO FORENSIC ANALYSIS
Complete factual verification of Klaviyo automation
"""

import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load credentials
load_dotenv('.env.admin')

KLAVIYO_API_KEY = os.getenv('KLAVIYO_PRIVATE_API_KEY')

HEADERS = {
    "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
    "revision": "2024-10-15",
    "Accept": "application/json"
}

BASE_URL = "https://a.klaviyo.com/api"

def api_get(endpoint):
    """Make GET request to Klaviyo API"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    print("=" * 80)
    print("ALPHA MEDICAL - KLAVIYO FORENSIC ANALYSIS")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 80)
    print()

    # 1. ACCOUNT INFO
    print("=" * 80)
    print("1. KLAVIYO ACCOUNT INFO")
    print("=" * 80)
    account = api_get("accounts/")
    if 'data' in account:
        for acc in account['data']:
            attrs = acc.get('attributes', {})
            print(f"Account ID: {acc.get('id')}")
            print(f"Company Name: {attrs.get('company_name')}")
            print(f"Contact Email: {attrs.get('contact_information', {}).get('default_sender', {}).get('email')}")
            print(f"Timezone: {attrs.get('timezone')}")
            print(f"Currency: {attrs.get('currency')}")
    else:
        print(f"ERROR: {account}")
    print()

    # 2. FLOWS (Email Automations)
    print("=" * 80)
    print("2. FLOWS (Email Automations)")
    print("=" * 80)
    flows = api_get("flows/")
    if 'data' in flows:
        print(f"Total Flows: {len(flows['data'])}")
        for flow in flows['data']:
            attrs = flow.get('attributes', {})
            status = attrs.get('status', 'unknown')
            print(f"\n  Flow: {attrs.get('name')}")
            print(f"  - ID: {flow.get('id')}")
            print(f"  - Status: {status}")
            print(f"  - Trigger Type: {attrs.get('trigger_type')}")
            print(f"  - Created: {attrs.get('created')}")
            print(f"  - Updated: {attrs.get('updated')}")
    else:
        print(f"ERROR: {flows}")
    print()

    # 3. LISTS
    print("=" * 80)
    print("3. LISTS")
    print("=" * 80)
    lists = api_get("lists/")
    if 'data' in lists:
        print(f"Total Lists: {len(lists['data'])}")
        for lst in lists['data']:
            attrs = lst.get('attributes', {})
            print(f"\n  List: {attrs.get('name')}")
            print(f"  - ID: {lst.get('id')}")
            print(f"  - Created: {attrs.get('created')}")
            print(f"  - Updated: {attrs.get('updated')}")
    else:
        print(f"ERROR: {lists}")
    print()

    # 4. SEGMENTS
    print("=" * 80)
    print("4. SEGMENTS")
    print("=" * 80)
    segments = api_get("segments/")
    if 'data' in segments:
        print(f"Total Segments: {len(segments['data'])}")
        for seg in segments['data']:
            attrs = seg.get('attributes', {})
            print(f"\n  Segment: {attrs.get('name')}")
            print(f"  - ID: {seg.get('id')}")
            print(f"  - Created: {attrs.get('created')}")
            print(f"  - Updated: {attrs.get('updated')}")
    else:
        print(f"ERROR: {segments}")
    print()

    # 5. CAMPAIGNS
    print("=" * 80)
    print("5. CAMPAIGNS")
    print("=" * 80)
    campaigns = api_get("campaigns/")
    if 'data' in campaigns:
        print(f"Total Campaigns: {len(campaigns['data'])}")
        for camp in campaigns['data'][:10]:  # First 10
            attrs = camp.get('attributes', {})
            print(f"\n  Campaign: {attrs.get('name')}")
            print(f"  - ID: {camp.get('id')}")
            print(f"  - Status: {attrs.get('status')}")
            print(f"  - Created: {attrs.get('created_at')}")
    else:
        print(f"ERROR: {campaigns}")
    print()

    # 6. TEMPLATES
    print("=" * 80)
    print("6. TEMPLATES")
    print("=" * 80)
    templates = api_get("templates/")
    if 'data' in templates:
        print(f"Total Templates: {len(templates['data'])}")
        for tmpl in templates['data'][:10]:  # First 10
            attrs = tmpl.get('attributes', {})
            print(f"\n  Template: {attrs.get('name')}")
            print(f"  - ID: {tmpl.get('id')}")
            print(f"  - Created: {attrs.get('created')}")
            print(f"  - Updated: {attrs.get('updated')}")
    else:
        print(f"ERROR: {templates}")
    print()

    # 7. METRICS (Events)
    print("=" * 80)
    print("7. METRICS (Tracked Events)")
    print("=" * 80)
    metrics = api_get("metrics/")
    if 'data' in metrics:
        print(f"Total Metrics: {len(metrics['data'])}")
        for metric in metrics['data'][:20]:  # First 20
            attrs = metric.get('attributes', {})
            print(f"  - {attrs.get('name')}")
    else:
        print(f"ERROR: {metrics}")
    print()

    print("=" * 80)
    print("KLAVIYO FORENSIC ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main()
