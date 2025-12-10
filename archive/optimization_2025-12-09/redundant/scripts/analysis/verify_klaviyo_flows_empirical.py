#!/usr/bin/env python3
"""
KLAVIYO FLOWS EMPIRICAL VERIFICATION
Date: 2025-12-06
Purpose: Verify Klaviyo flows status, triggers, and actions via API
Method: Direct API calls to Klaviyo (no assumptions)
Bullshit Level: 0% (API verification only)
"""

import os
import requests
import json
from typing import Dict, List

# Load Klaviyo API key from .env.admin
def load_klaviyo_api_key() -> str:
    """Load Klaviyo API key from .env.admin."""
    env_file = "/Users/mac/Desktop/Alpha-Medical/.env.admin"

    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('KLAVIYO_API_KEY='):
                return line.strip().split('=', 1)[1].strip('"')

    raise ValueError("KLAVIYO_API_KEY not found in .env.admin")


def get_klaviyo_flows(api_key: str) -> List[Dict]:
    """
    Get all Klaviyo flows via API.
    Endpoint: https://a.klaviyo.com/api/flows
    """
    url = "https://a.klaviyo.com/api/flows"
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": "2024-10-15",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Klaviyo API error: {response.status_code} - {response.text}")

    data = response.json()
    return data.get('data', [])


def analyze_flow_details(flow: Dict) -> Dict:
    """Analyze a single flow's details."""
    attributes = flow.get('attributes', {})

    return {
        'id': flow.get('id'),
        'name': attributes.get('name'),
        'status': attributes.get('status'),  # 'live', 'draft', 'manual'
        'trigger_type': attributes.get('trigger_type'),
        'created': attributes.get('created'),
        'updated': attributes.get('updated'),
    }


def generate_report(flows: List[Dict]) -> str:
    """Generate empirical verification report."""

    report = []
    report.append("=" * 100)
    report.append("KLAVIYO FLOWS EMPIRICAL VERIFICATION")
    report.append("=" * 100)
    report.append(f"Date: 2025-12-06")
    report.append(f"Total Flows Found: {len(flows)}")
    report.append("Method: Direct Klaviyo API v2024-10-15")
    report.append("=" * 100)
    report.append("")

    # Analyze each flow
    live_flows = []
    draft_flows = []
    manual_flows = []

    for flow in flows:
        details = analyze_flow_details(flow)

        if details['status'] == 'live':
            live_flows.append(details)
        elif details['status'] == 'draft':
            draft_flows.append(details)
        elif details['status'] == 'manual':
            manual_flows.append(details)

    # Summary
    report.append("SUMMARY:")
    report.append(f"  LIVE Flows: {len(live_flows)}")
    report.append(f"  DRAFT Flows: {len(draft_flows)}")
    report.append(f"  MANUAL Flows: {len(manual_flows)}")
    report.append("")

    # LIVE flows details
    report.append("=" * 100)
    report.append(f"LIVE FLOWS ({len(live_flows)}):")
    report.append("=" * 100)

    for flow in live_flows:
        report.append(f"\nFlow ID: {flow['id']}")
        report.append(f"Name: {flow['name']}")
        report.append(f"Status: {flow['status'].upper()}")
        report.append(f"Trigger Type: {flow['trigger_type']}")
        report.append(f"Created: {flow['created']}")
        report.append(f"Updated: {flow['updated']}")

    # DRAFT flows details
    if draft_flows:
        report.append("\n\n" + "=" * 100)
        report.append(f"DRAFT FLOWS ({len(draft_flows)}):")
        report.append("=" * 100)

        for flow in draft_flows:
            report.append(f"\nFlow ID: {flow['id']}")
            report.append(f"Name: {flow['name']}")
            report.append(f"Status: {flow['status'].upper()}")
            report.append(f"Trigger Type: {flow['trigger_type']}")

    # MANUAL flows details
    if manual_flows:
        report.append("\n\n" + "=" * 100)
        report.append(f"MANUAL FLOWS ({len(manual_flows)}):")
        report.append("=" * 100)

        for flow in manual_flows:
            report.append(f"\nFlow ID: {flow['id']}")
            report.append(f"Name: {flow['name']}")
            report.append(f"Status: {flow['status'].upper()}")

    # Verification against expected flows
    report.append("\n\n" + "=" * 100)
    report.append("VERIFICATION AGAINST INFRASTRUCTURE_AUDIT_CHECKLIST.md:")
    report.append("=" * 100)

    expected_flows = {
        "Welcome Series": False,
        "Abandoned Cart": False,
        "Post-Purchase": False,
        "Win-Back": False,
    }

    for flow in live_flows:
        name = flow['name'].lower()
        if 'welcome' in name:
            expected_flows["Welcome Series"] = True
        elif 'abandon' in name or 'cart' in name:
            expected_flows["Abandoned Cart"] = True
        elif 'post' in name or 'purchase' in name:
            expected_flows["Post-Purchase"] = True
        elif 'win' in name or 'back' in name:
            expected_flows["Win-Back"] = True

    report.append("")
    for flow_name, verified in expected_flows.items():
        status = "✅ VERIFIED" if verified else "❌ NOT FOUND"
        report.append(f"  {flow_name}: {status}")

    all_verified = all(expected_flows.values())
    report.append("")
    if all_verified:
        report.append("✅ ALL 4 EXPECTED FLOWS VERIFIED AS LIVE")
    else:
        missing = [name for name, verified in expected_flows.items() if not verified]
        report.append(f"❌ MISSING FLOWS: {', '.join(missing)}")

    return "\n".join(report)


def main():
    """Main execution."""
    print("Starting Klaviyo flows empirical verification...")
    print("Loading API key from .env.admin...")

    try:
        api_key = load_klaviyo_api_key()
        print(f"✅ API key loaded ({len(api_key)} characters)")

        print("Fetching flows from Klaviyo API...")
        flows = get_klaviyo_flows(api_key)
        print(f"✅ Retrieved {len(flows)} flows")

        print("Analyzing flow details...")
        report = generate_report(flows)

        # Save report
        output_file = "/Users/mac/Desktop/Alpha-Medical/KLAVIYO_FLOWS_EMPIRICAL_VERIFICATION_2025-12-06.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print("")
        print(f"✅ Verification complete!")
        print(f"Report saved to: {output_file}")
        print("")

        # Print summary
        live_count = sum(1 for f in flows if analyze_flow_details(f)['status'] == 'live')
        print(f"SUMMARY:")
        print(f"  Total flows: {len(flows)}")
        print(f"  LIVE flows: {live_count}")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        raise


if __name__ == "__main__":
    main()
