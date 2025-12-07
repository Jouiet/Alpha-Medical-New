#!/usr/bin/env python3
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

theme_id = 140069830733

# Get theme settings_data.json
url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
headers = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

params = {'asset[key]': 'config/settings_data.json'}

response = requests.get(url, headers=headers, params=params)
settings = json.loads(response.json()['asset']['value'])

print("="*70)
print("FOOTER CONFIGURATION")
print("="*70)

# Find footer section
for section_id, section_data in settings['current'].get('sections', {}).items():
    if 'footer' in section_id.lower():
        print(f"\n📦 Section: {section_id}")
        print(f"Type: {section_data.get('type')}")

        if 'blocks' in section_data:
            print(f"\nBlocks ({len(section_data['blocks'])} total):")
            for block_id, block_data in section_data['blocks'].items():
                block_type = block_data.get('type')
                print(f"\n  Block: {block_id}")
                print(f"    Type: {block_type}")

                if block_type == 'link_list':
                    menu = block_data.get('settings', {}).get('menu')
                    heading = block_data.get('settings', {}).get('heading')
                    print(f"    Heading: {heading}")
                    print(f"    Menu: {menu}")
                    print(f"    → ADD 'Investor Relations' HERE if heading contains 'Company' or 'About'")
