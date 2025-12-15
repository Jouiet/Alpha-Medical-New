#!/usr/bin/env python3
"""
KLAVIYO FLOWS EMPIRICAL VERIFICATION - SESSION 83
Date: 2025-12-06
Updated: 2025-12-16 (Session 100 - standardized API key)
Purpose: Verify which Klaviyo flows actually exist in live account
Method: Klaviyo API direct verification (REST API v2024-10-15)
API Docs: https://developers.klaviyo.com/en/reference/get_flows
"""

import requests
import json
import os
from typing import List, Dict
from dotenv import load_dotenv

def verify_klaviyo_flows() -> Dict:
    """
    Verify actual Klaviyo flows via API

    Returns:
        Dict with flow counts, statuses, and details
    """
    print("\n" + "="*70)
    print("KLAVIYO FLOWS EMPIRICAL VERIFICATION")
    print("="*70 + "\n")

    # Load API key from .env (standardized to KLAVIYO_PRIVATE_API_KEY)
    load_dotenv()
    api_key = os.getenv('KLAVIYO_PRIVATE_API_KEY')

    if not api_key:
        raise ValueError("KLAVIYO_PRIVATE_API_KEY not found in .env")

    print(f"✅ API Key loaded: {api_key[:10]}...{api_key[-4:]}\n")

    # Klaviyo API v2024-10-15 - Get Flows
    url = "https://a.klaviyo.com/api/flows/"
    headers = {
        "Authorization": f"Klaviyo-API-Key {api_key}",
        "revision": "2024-10-15",
        "Accept": "application/json"
    }

    print(f"🔍 Fetching flows from Klaviyo API...")
    print(f"   URL: {url}")
    print(f"   Revision: 2024-10-15\n")

    try:
        response = requests.get(url, headers=headers, timeout=30)

        print(f"📡 API Response Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            flows = data.get('data', [])
            total_flows = len(flows)

            print(f"✅ SUCCESS - Found {total_flows} flows\n")
            print("="*70)
            print("FLOWS INVENTORY (LIVE ACCOUNT)")
            print("="*70 + "\n")

            results = {
                'total_flows': total_flows,
                'flows': [],
                'status_breakdown': {'LIVE': 0, 'DRAFT': 0, 'MANUAL': 0},
                'timestamp': '2025-12-06',
                'method': 'Klaviyo REST API v2024-10-15'
            }

            for idx, flow in enumerate(flows, 1):
                flow_id = flow.get('id', 'N/A')
                attributes = flow.get('attributes', {})

                flow_name = attributes.get('name', 'Unnamed')
                flow_status = attributes.get('status', 'UNKNOWN')
                trigger_type = attributes.get('trigger_type', 'N/A')
                created = attributes.get('created', 'N/A')
                updated = attributes.get('updated', 'N/A')

                # Count status
                if flow_status in results['status_breakdown']:
                    results['status_breakdown'][flow_status] += 1

                flow_info = {
                    'id': flow_id,
                    'name': flow_name,
                    'status': flow_status,
                    'trigger_type': trigger_type,
                    'created': created,
                    'updated': updated
                }

                results['flows'].append(flow_info)

                print(f"Flow #{idx}:")
                print(f"  Name: {flow_name}")
                print(f"  ID: {flow_id}")
                print(f"  Status: {flow_status}")
                print(f"  Trigger: {trigger_type}")
                print(f"  Created: {created}")
                print(f"  Updated: {updated}")
                print()

            print("="*70)
            print("STATUS BREAKDOWN")
            print("="*70)
            for status, count in results['status_breakdown'].items():
                print(f"  {status}: {count}")
            print()

            # Save results to JSON
            output_file = "/Users/mac/Desktop/Alpha-Medical/klaviyo_flows_verification_2025-12-06.json"
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)

            print(f"✅ Results saved to: {output_file}\n")

            return results

        elif response.status_code == 401:
            print(f"❌ AUTHENTICATION FAILED")
            print(f"   Error: Invalid API key")
            print(f"   Response: {response.text}\n")
            return {'error': 'Authentication failed', 'status_code': 401}

        elif response.status_code == 403:
            print(f"❌ FORBIDDEN")
            print(f"   Error: API key lacks required permissions")
            print(f"   Response: {response.text}\n")
            return {'error': 'Forbidden', 'status_code': 403}

        else:
            print(f"❌ API ERROR")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}\n")
            return {'error': 'API error', 'status_code': response.status_code}

    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST FAILED")
        print(f"   Error: {str(e)}\n")
        return {'error': str(e)}


if __name__ == "__main__":
    try:
        results = verify_klaviyo_flows()

        if 'error' not in results:
            print("="*70)
            print("✅ VERIFICATION COMPLETE")
            print("="*70)
            print(f"Total Flows: {results['total_flows']}")
            print(f"Method: {results['method']}")
            print(f"Confidence: 100% (API-verified)")
            print(f"Bullshit Level: 0%")
            print()
        else:
            print("="*70)
            print("❌ VERIFICATION FAILED")
            print("="*70)
            print(f"Error: {results.get('error')}")
            print()

    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}\n")
        raise
