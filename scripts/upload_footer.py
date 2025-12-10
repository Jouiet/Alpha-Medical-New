#!/usr/bin/env python3
"""Upload footer.liquid to Shopify"""
import os, base64, requests
from dotenv import load_dotenv

load_dotenv('.env.admin')
SHOP = os.getenv('SHOPIFY_STORE_DOMAIN')
TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
THEME_ID = '140069830733'

API_URL = f'https://{SHOP}/admin/api/2024-10/themes/{THEME_ID}/assets.json'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

with open('sections/footer.liquid', 'r', encoding='utf-8') as f:
    content = f.read()

payload = {'asset': {'key': 'sections/footer.liquid', 'attachment': base64.b64encode(content.encode('utf-8')).decode('utf-8')}}
response = requests.put(API_URL, json=payload, headers=HEADERS)

if response.status_code == 200:
    print("✅ Footer uploaded successfully")
else:
    print(f"❌ Failed: {response.status_code} - {response.text}")
