#!/usr/bin/env python3
"""Test direct Apify API to verify actor IDs and formats"""

import os
import requests
import json

API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
if not API_TOKEN:
    raise ValueError("APIFY_API_TOKEN environment variable not set. Add it to .env file")
API_BASE = "https://api.apify.com/v2"

# Test 1: List my recent runs
print("=" * 70)
print("TEST 1: Checking recent actor runs")
print("=" * 70)

url = f"{API_BASE}/actor-runs?token={API_TOKEN}&limit=5"
response = requests.get(url)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    runs = data.get('data', {}).get('items', [])
    print(f"Recent runs: {len(runs)}")
    for run in runs[:3]:
        print(f"  - {run.get('actId')}: {run.get('status')}")

# Test 2: Try Google Maps actor with correct format
print("\n" + "=" * 70)
print("TEST 2: Starting Google Maps actor (compass~crawler-google-places)")
print("=" * 70)

actor_id = "compass~crawler-google-places"
run_url = f"{API_BASE}/acts/{actor_id}/runs?token={API_TOKEN}"

actor_input = {
    "searchStringsArray": ["physical therapy in Los Angeles, CA"],
    "maxCrawledPlaces": 3,
    "language": "en"
}

headers = {
    "Content-Type": "application/json"
}

print(f"URL: {run_url}")
print(f"Input: {json.dumps(actor_input, indent=2)}")

response = requests.post(run_url, json=actor_input, headers=headers)
print(f"\nStatus: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)[:500]}")

if response.status_code == 201:
    print("\n✅ SUCCESS! Actor started")
    run_data = response.json()['data']
    print(f"Run ID: {run_data['id']}")
    print(f"Status: {run_data['status']}")
else:
    print(f"\n❌ FAILED: {response.text}")

# Test 3: Try Instagram Hashtag Scraper
print("\n" + "=" * 70)
print("TEST 3: Starting Instagram Hashtag actor (apify~instagram-hashtag-scraper)")
print("=" * 70)

actor_id = "apify~instagram-hashtag-scraper"
run_url = f"{API_BASE}/acts/{actor_id}/runs?token={API_TOKEN}"

actor_input = {
    "hashtags": ["arthritis"],
    "resultsLimit": 3
}

response = requests.post(run_url, json=actor_input, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 201:
    print("✅ SUCCESS! Actor started")
    run_data = response.json()['data']
    print(f"Run ID: {run_data['id']}")
else:
    print(f"❌ FAILED: {response.text[:500]}")
