#!/usr/bin/env python3
"""
Script pour uploader les images Hero vers Shopify Files (pas Theme Assets)
Les images doivent être dans Files pour être référencées via shopify://shop_images/
"""

import requests
import json
import base64
from pathlib import Path

# Load token
env_file = Path(__file__).parent / '.env.admin'
ACCESS_TOKEN = None

if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                ACCESS_TOKEN = line.split('=', 1)[1].strip()
                break

if not ACCESS_TOKEN:
    print("❌ ERROR: SHOPIFY_ADMIN_ACCESS_TOKEN not found")
    exit(1)

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-01"
BASE_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

def upload_file_to_shopify(filename, file_content, alt_text):
    """Upload file to Shopify Files via GraphQL API"""

    # Step 1: Stage upload (get URL to upload to)
    graphql_url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

    stage_mutation = """
    mutation {
      stagedUploadsCreate(input: [
        {
          resource: IMAGE,
          filename: "%s",
          mimeType: "image/svg+xml",
          httpMethod: POST
        }
      ]) {
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
    """ % filename

    response = requests.post(
        graphql_url,
        headers=headers,
        json={"query": stage_mutation}
    )

    if response.status_code != 200:
        print(f"  ❌ Error staging upload: {response.status_code}")
        print(f"  {response.text}")
        return None

    data = response.json()

    if 'errors' in data:
        print(f"  ❌ GraphQL errors: {data['errors']}")
        return None

    staged_target = data['data']['stagedUploadsCreate']['stagedTargets'][0]
    upload_url = staged_target['url']
    resource_url = staged_target['resourceUrl']
    parameters = {p['name']: p['value'] for p in staged_target['parameters']}

    # Step 2: Upload file to staged URL
    files = {'file': (filename, file_content, 'image/svg+xml')}
    upload_response = requests.post(upload_url, data=parameters, files=files)

    if upload_response.status_code not in [200, 201, 204]:
        print(f"  ❌ Error uploading file: {upload_response.status_code}")
        print(f"  {upload_response.text}")
        return None

    # Step 3: Create file in Shopify
    create_mutation = """
    mutation {
      fileCreate(files: [
        {
          alt: "%s",
          contentType: IMAGE,
          originalSource: "%s"
        }
      ]) {
        files {
          ... on MediaImage {
            id
            image {
              url
              altText
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """ % (alt_text, resource_url)

    create_response = requests.post(
        graphql_url,
        headers=headers,
        json={"query": create_mutation}
    )

    if create_response.status_code != 200:
        print(f"  ❌ Error creating file: {create_response.status_code}")
        print(f"  {create_response.text}")
        return None

    create_data = create_response.json()

    if 'errors' in create_data:
        print(f"  ❌ GraphQL errors: {create_data['errors']}")
        return None

    if create_data['data']['fileCreate']['userErrors']:
        print(f"  ❌ User errors: {create_data['data']['fileCreate']['userErrors']}")
        return None

    print(f"  DEBUG: create_data = {json.dumps(create_data, indent=2)}")

    files = create_data['data']['fileCreate']['files']
    if not files or len(files) == 0:
        print(f"  ❌ No files returned from fileCreate")
        return None

    file_info = files[0]

    if not file_info or 'image' not in file_info or file_info['image'] is None:
        print(f"  ❌ File info incomplete: {file_info}")
        return None

    image_url = file_info['image']['url']
    file_id = file_info['id']

    return {
        'url': image_url,
        'id': file_id
    }

def main():
    print("=" * 70)
    print("🖼️  UPLOAD IMAGES HERO VERS SHOPIFY FILES")
    print("=" * 70)
    print()

    # Select 5 SVG images to upload
    hero_images = [
        ("1.svg", "Alpha Medical Care - Professional Medical Equipment"),
        ("Design sans titre.svg", "Alpha Medical Care - Pain Relief Solutions"),
        ("Design sans titre10.svg", "Alpha Medical Care - Posture Support"),
        ("Design sans titre4.svg", "Alpha Medical Care - Therapy & Wellness"),
        ("Design sans titre5.svg", "Alpha Medical Care - Trusted Worldwide")
    ]

    images_dir = Path(__file__).parent / "Images" / "Hero"

    success_count = 0
    fail_count = 0
    uploaded_urls = []

    for i, (img_filename, alt_text) in enumerate(hero_images, 1):
        print(f"{i}/{len(hero_images)}. Upload {img_filename}...")

        img_path = images_dir / img_filename

        if not img_path.exists():
            print(f"  ❌ File not found: {img_path}")
            fail_count += 1
            continue

        # Read SVG content
        with open(img_path, 'rb') as f:
            svg_content = f.read()

        # Upload to Shopify Files
        result = upload_file_to_shopify(f"hero-slide-{i}.svg", svg_content, alt_text)

        if result:
            print(f"  ✅ SUCCESS")
            print(f"     URL: {result['url']}")
            print(f"     ID: {result['id']}")
            success_count += 1
            uploaded_urls.append(result['url'])
        else:
            fail_count += 1

        print()

    print("=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    print(f"✅ Images uploadées: {success_count}/{len(hero_images)}")
    print(f"❌ Échecs: {fail_count}/{len(hero_images)}")
    print()

    if success_count > 0:
        print("🎉 IMAGES UPLOADÉES VERS SHOPIFY FILES!")
        print()
        print("URLs des images:")
        for i, url in enumerate(uploaded_urls, 1):
            print(f"  {i}. {url}")
        print()
        print("⚠️ NEXT STEP: Modifier templates/index.json avec ces URLs")

    print()

if __name__ == "__main__":
    main()
