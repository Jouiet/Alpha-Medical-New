#!/usr/bin/env python3
"""
Test Klaviyo API Access
Verifies Private API key works for automation
"""

import os
import requests
from dotenv import load_dotenv

# Load .env credentials
load_dotenv('.env')

PRIVATE_KEY = os.getenv('KLAVIYO_PRIVATE_API_KEY')

if not PRIVATE_KEY:
    print("❌ Missing KLAVIYO_PRIVATE_API_KEY in .env")
    exit(1)

# Test Klaviyo API v2023-10-15 (latest stable)
url = "https://a.klaviyo.com/api/accounts/"
headers = {
    "Authorization": f"Klaviyo-API-Key {PRIVATE_KEY}",
    "revision": "2023-10-15",
    "Accept": "application/json"
}

try:
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
        accounts = data.get('data', [])

        if accounts:
            account = accounts[0]['attributes']
            print("✅ Klaviyo API Access: SUCCESS")
            print(f"   Account Name: {account.get('test_account', {}).get('name', 'N/A')}")
            print(f"   Account ID: {accounts[0]['id'][:20]}...")
            print(f"   Public Key: {account.get('public_api_key', 'N/A')[:20]}...")

            # Test lists endpoint
            lists_url = "https://a.klaviyo.com/api/lists/"
            lists_response = requests.get(lists_url, headers=headers, timeout=10)
            if lists_response.status_code == 200:
                lists_data = lists_response.json()
                lists_count = len(lists_data.get('data', []))
                print(f"   Lists: {lists_count} found")

            exit(0)
        else:
            print("⚠️  No accounts found")
            exit(1)
    else:
        print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
        exit(1)

except Exception as e:
    print(f"❌ Connection error: {e}")
    exit(1)
