#!/usr/bin/env python3
"""Create Size Quiz page in Shopify"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")

REST_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10"

headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN
}

# Page data
page_data = {
    "page": {
        "title": "Size Quiz - Find Your Perfect Fit",
        "body_html": """
<p>Use our interactive size quiz to find the perfect size for your medical support product. Get accurate recommendations based on your measurements and needs.</p>
<p><strong>The quiz will load below. If you don't see it, please refresh the page.</strong></p>
""",
        "handle": "size-quiz",
        "template_suffix": "size-quiz",
        "published": True,
        "metafields": [
            {
                "namespace": "custom",
                "key": "meta_title",
                "value": "Size Quiz - Find Your Perfect Fit | Alpha Medical Care",
                "type": "single_line_text_field"
            },
            {
                "namespace": "custom",
                "key": "meta_description",
                "value": "Not sure what size to order? Use our interactive sizing quiz to find the perfect fit for medical support products. Get instant recommendations in 60 seconds.",
                "type": "single_line_text_field"
            }
        ]
    }
}

# Check if page already exists
print("Checking if size-quiz page already exists...")
check_response = requests.get(
    f"{REST_URL}/pages.json?handle=size-quiz",
    headers=headers
)

if check_response.status_code == 200:
    existing_pages = check_response.json().get('pages', [])
    if existing_pages:
        page_id = existing_pages[0]['id']
        print(f"⚠️  Page already exists (ID: {page_id})")
        print(f"   Updating existing page...")

        # Update existing page
        response = requests.put(
            f"{REST_URL}/pages/{page_id}.json",
            headers=headers,
            json=page_data
        )
    else:
        print("   Page doesn't exist, creating new...")
        # Create new page
        response = requests.post(
            f"{REST_URL}/pages.json",
            headers=headers,
            json=page_data
        )
else:
    print(f"❌ Error checking for existing page: {check_response.status_code}")
    print(check_response.json())
    exit(1)

if response.status_code in [200, 201]:
    page = response.json()['page']
    print(f"\n✅ Size Quiz page {'updated' if existing_pages else 'created'} successfully!")
    print(f"   ID: {page['id']}")
    print(f"   Handle: {page['handle']}")
    print(f"   Template: page.{page.get('template_suffix', 'default')}.liquid")
    print(f"   URL: https://{SHOPIFY_STORE_DOMAIN}/pages/{page['handle']}")
    print(f"   Published: {page['published_at']}")
else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.json())
