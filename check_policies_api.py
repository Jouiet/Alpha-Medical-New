#!/usr/bin/env python3
import os, requests
from dotenv import load_dotenv
load_dotenv('.env.admin')

query = '''{
  shop {
    privacyPolicy { title url }
    refundPolicy { title url }
    shippingPolicy { title url }
    termsOfService { title url }
  }
}'''

r = requests.post(
    f'https://{os.getenv("SHOPIFY_STORE_DOMAIN")}/admin/api/2024-01/graphql.json',
    headers={'X-Shopify-Access-Token': os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN'), 'Content-Type': 'application/json'},
    json={'query': query}
)

data = r.json()
if 'data' in data:
    shop = data['data']['shop']
    for policy, value in shop.items():
        if value:
            print(f'✅ {policy}: {value["title"]} → {value["url"]}')
        else:
            print(f'❌ {policy}: NOT PUBLISHED')
