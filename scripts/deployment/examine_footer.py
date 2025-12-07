#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

theme_id = 140069830733

url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
headers = {
    'X-Shopify-Access-Token': ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

params = {'asset[key]': 'sections/footer.liquid'}

response = requests.get(url, headers=headers, params=params)
content = response.json()['asset']['value']

# Save to file for examination
with open('/tmp/footer.liquid', 'w') as f:
    f.write(content)

# Look for menu blocks
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'menu' in line.lower() or 'link' in line.lower() or 'pages/about' in line.lower():
        print(f"{i:4d}: {line}")
