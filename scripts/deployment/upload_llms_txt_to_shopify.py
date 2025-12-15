#!/usr/bin/env python3
"""
UPLOAD LLMS.TXT TO SHOPIFY FILES
Alpha Medical - Session 98 CONTINUED
AEO (Answer Engine Optimization) Fix

This script uploads llms.txt to Shopify Files via GraphQL API,
making it accessible via CDN URL for AI crawlers.
"""

import os
import sys
import requests
import json
import base64

# Load credentials
def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '../../.env.admin')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

load_env()

STORE = os.environ.get('SHOPIFY_STORE_DOMAIN', 'azffej-as.myshopify.com')
TOKEN = os.environ.get('SHOPIFY_ADMIN_ACCESS_TOKEN')
GRAPHQL_URL = f'https://{STORE}/admin/api/2025-01/graphql.json'
HEADERS = {
    'X-Shopify-Access-Token': TOKEN,
    'Content-Type': 'application/json'
}

def graphql_request(query, variables=None):
    """Execute GraphQL request"""
    payload = {'query': query}
    if variables:
        payload['variables'] = variables

    resp = requests.post(GRAPHQL_URL, headers=HEADERS, json=payload)
    if resp.status_code != 200:
        print(f"❌ API Error: {resp.status_code}")
        print(resp.text[:500])
        return None

    data = resp.json()
    if 'errors' in data:
        print(f"❌ GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
        return None

    return data

def get_staged_upload_url(filename, file_size, mime_type):
    """Get a staged upload URL from Shopify"""
    query = """
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets {
          url
          resourceUrl
          parameters {
            name
            value
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "input": [{
            "filename": filename,
            "mimeType": mime_type,
            "resource": "FILE",
            "fileSize": str(file_size),
            "httpMethod": "POST"
        }]
    }

    result = graphql_request(query, variables)
    if not result:
        return None, None

    data = result.get('data', {}).get('stagedUploadsCreate', {})
    errors = data.get('userErrors', [])
    if errors:
        print(f"❌ User Errors: {errors}")
        return None, None

    targets = data.get('stagedTargets', [])
    if not targets:
        print("❌ No staged targets returned")
        return None, None

    return targets[0]['url'], targets[0]['parameters'], targets[0]['resourceUrl']

def upload_file_to_staged_url(url, parameters, file_path):
    """Upload file to the staged URL"""
    with open(file_path, 'rb') as f:
        file_content = f.read()

    # Build form data from parameters
    files = {}
    data = {}
    for param in parameters:
        data[param['name']] = param['value']

    files['file'] = (os.path.basename(file_path), file_content, 'text/plain')

    resp = requests.post(url, data=data, files=files)

    if resp.status_code in [200, 201, 204]:
        print(f"✅ File uploaded to staged URL successfully")
        return True
    else:
        print(f"❌ Upload failed: {resp.status_code}")
        print(resp.text[:500])
        return False

def create_file_from_staged(resource_url, filename):
    """Create the actual file in Shopify from the staged upload"""
    query = """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files {
          ... on GenericFile {
            id
            url
            alt
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "files": [{
            "originalSource": resource_url,
            "filename": filename,
            "alt": "Alpha Medical llms.txt - AI Discovery Documentation"
        }]
    }

    result = graphql_request(query, variables)
    if not result:
        return None

    data = result.get('data', {}).get('fileCreate', {})
    errors = data.get('userErrors', [])
    if errors:
        print(f"❌ File Create Errors: {errors}")
        return None

    files = data.get('files', [])
    if files and files[0]:
        return files[0]

    return None

def main():
    print("=" * 60)
    print("UPLOAD LLMS.TXT TO SHOPIFY FILES")
    print("=" * 60)
    print()

    # Find llms.txt
    llms_path = os.path.join(os.path.dirname(__file__), '../../llms.txt')
    if not os.path.exists(llms_path):
        print(f"❌ llms.txt not found at: {llms_path}")
        return False

    file_size = os.path.getsize(llms_path)
    print(f"📄 Found llms.txt: {file_size} bytes")

    # Step 1: Get staged upload URL
    print("\n📤 Step 1: Getting staged upload URL...")
    url, params, resource_url = get_staged_upload_url('llms.txt', file_size, 'text/plain')
    if not url:
        print("❌ Failed to get staged upload URL")
        return False
    print(f"✅ Staged URL obtained")
    print(f"   Resource URL: {resource_url}")

    # Step 2: Upload file to staged URL
    print("\n📤 Step 2: Uploading file to staged URL...")
    if not upload_file_to_staged_url(url, params, llms_path):
        print("❌ Failed to upload file")
        return False

    # Step 3: Create file in Shopify
    print("\n📤 Step 3: Creating file in Shopify...")
    file_data = create_file_from_staged(resource_url, 'llms.txt')
    if not file_data:
        print("❌ Failed to create file in Shopify")
        return False

    print(f"✅ File created successfully!")
    print(f"   ID: {file_data.get('id')}")
    print(f"   URL: {file_data.get('url')}")

    # Step 4: Verify file is accessible
    print("\n🔍 Step 4: Verifying file accessibility...")
    cdn_url = file_data.get('url')
    if cdn_url:
        # Sometimes the URL needs a moment to propagate
        import time
        time.sleep(2)

        verify_resp = requests.head(cdn_url)
        if verify_resp.status_code == 200:
            print(f"✅ File is accessible!")
            print(f"   Status: {verify_resp.status_code}")
            print(f"   Content-Type: {verify_resp.headers.get('Content-Type', 'N/A')}")
        else:
            print(f"⚠️  File not immediately accessible (may take a few seconds)")
            print(f"   Status: {verify_resp.status_code}")

    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"""
✅ llms.txt uploaded to Shopify Files
   CDN URL: {file_data.get('url')}

NEXT STEPS:
1. Add meta tag to theme: <link rel="llms" href="{file_data.get('url')}">
2. Optionally mention in robots.txt
3. Verify with: curl -I "{file_data.get('url')}"
""")

    return file_data.get('url')

if __name__ == '__main__':
    result = main()
    sys.exit(0 if result else 1)
