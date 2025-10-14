#!/usr/bin/env python3
"""
Upload 15 PNG Hero images vers Shopify Files
"""

import requests
import json
import time
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

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
API_VERSION = "2025-01"

headers = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# 15 images PNG à uploader
PNG_IMAGES = [
    ("1.png", "Alpha Medical Care - Professional Medical Equipment"),
    ("Design sans titre.png", "Alpha Medical Care - Pain Relief Solutions"),
    ("Design sans titre10.png", "Alpha Medical Care - Posture Support"),
    ("Design sans titre11.png", "Alpha Medical Care - Therapy & Wellness"),
    ("Design sans titre12.png", "Alpha Medical Care - Recovery Solutions"),
    ("Design sans titre13.png", "Alpha Medical Care - Orthopedic Braces"),
    ("Design sans titre14.png", "Alpha Medical Care - LED Therapy Devices"),
    ("Design sans titre15.png", "Alpha Medical Care - Massage Equipment"),
    ("Design sans titre3.png", "Alpha Medical Care - Compression Support"),
    ("Design sans titre4.png", "Alpha Medical Care - Cervical Support"),
    ("Design sans titre5.png", "Alpha Medical Care - Wellness Products"),
    ("Design sans titre6.png", "Alpha Medical Care - Home Therapy"),
    ("Design sans titre7.png", "Alpha Medical Care - Professional Grade"),
    ("Design sans titre9.png", "Alpha Medical Care - Trusted Worldwide"),
    ("1 copy.png", "Alpha Medical Care - Quality Assured")
]

def upload_png_to_shopify(filename, png_content, alt_text):
    """Upload PNG file to Shopify Files via GraphQL API"""

    graphql_url = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

    # Step 1: Stage upload
    stage_mutation = """
    mutation {
      stagedUploadsCreate(input: [
        {
          resource: IMAGE,
          filename: "%s",
          mimeType: "image/png",
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
        print(f"  ❌ Error staging: {response.status_code}")
        return None

    data = response.json()

    if 'errors' in data or data['data']['stagedUploadsCreate']['userErrors']:
        print(f"  ❌ Staging errors")
        return None

    staged_target = data['data']['stagedUploadsCreate']['stagedTargets'][0]
    upload_url = staged_target['url']
    resource_url = staged_target['resourceUrl']
    parameters = {p['name']: p['value'] for p in staged_target['parameters']}

    # Step 2: Upload PNG file
    files = {'file': (filename, png_content, 'image/png')}
    upload_response = requests.post(upload_url, data=parameters, files=files)

    if upload_response.status_code not in [200, 201, 204]:
        print(f"  ❌ Error uploading: {upload_response.status_code}")
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
            alt
            image {
              url
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
        return None

    create_data = create_response.json()

    if 'errors' in create_data or create_data['data']['fileCreate']['userErrors']:
        print(f"  ❌ Create errors")
        return None

    # Wait for processing
    time.sleep(2)

    files = create_data['data']['fileCreate']['files']
    if files and len(files) > 0:
        file_info = files[0]
        file_id = file_info['id']

        # Re-query to get the processed URL
        query_file = """
        query {
          node(id: "%s") {
            ... on MediaImage {
              id
              image {
                url
              }
            }
          }
        }
        """ % file_id

        retry_count = 0
        while retry_count < 5:
            query_response = requests.post(
                graphql_url,
                headers=headers,
                json={"query": query_file}
            )

            if query_response.status_code == 200:
                query_data = query_response.json()
                node = query_data.get('data', {}).get('node', {})

                if node and 'image' in node and node['image'] and 'url' in node['image']:
                    return {
                        'id': file_id,
                        'url': node['image']['url']
                    }

            time.sleep(3)
            retry_count += 1

    return None

def main():
    print("=" * 70)
    print("🖼️  UPLOAD 15 IMAGES PNG HERO VERS SHOPIFY FILES")
    print("=" * 70)
    print()

    images_dir = Path(__file__).parent / "Images" / "Hero-PNG"

    success_count = 0
    fail_count = 0
    uploaded_images = []

    for i, (img_filename, alt_text) in enumerate(PNG_IMAGES, 1):
        print(f"{i}/{len(PNG_IMAGES)}. Upload {img_filename}...")

        img_path = images_dir / img_filename

        if not img_path.exists():
            print(f"  ❌ File not found: {img_path}")
            fail_count += 1
            continue

        # Read PNG content
        with open(img_path, 'rb') as f:
            png_content = f.read()

        # Upload to Shopify Files
        result = upload_png_to_shopify(f"hero-slide-{i}.png", png_content, alt_text)

        if result:
            print(f"  ✅ SUCCESS")
            print(f"     URL: {result['url']}")
            success_count += 1
            uploaded_images.append({
                'index': i,
                'url': result['url'],
                'filename': img_filename
            })
        else:
            print(f"  ❌ FAILED")
            fail_count += 1

        print()

    print("=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    print(f"✅ Images uploadées: {success_count}/{len(PNG_IMAGES)}")
    print(f"❌ Échecs: {fail_count}/{len(PNG_IMAGES)}")
    print()

    if success_count > 0:
        print("🎉 IMAGES PNG UPLOADÉES!")
        print()
        print("URLs des images:")
        for img in uploaded_images:
            print(f"  {img['index']}. {img['url']}")
        print()

        # Save URLs to file for template config
        with open('hero_image_urls.json', 'w') as f:
            json.dump(uploaded_images, f, indent=2)
        print("✅ URLs sauvegardées dans hero_image_urls.json")

    print()

if __name__ == "__main__":
    main()
