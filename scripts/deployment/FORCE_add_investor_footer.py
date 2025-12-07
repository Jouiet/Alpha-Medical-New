#!/usr/bin/env python3
"""
FORCE ADD INVESTOR LINK TO FOOTER - HARDCODE IT
Modifie footer.liquid pour ajouter hardcodé le lien Investor Relations
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

theme_id = 140069830733

def get_footer():
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    response = requests.get(url, headers=headers, params={'asset[key]': 'sections/footer.liquid'})
    return response.json()['asset']['value']

def update_footer(content):
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    data = {'asset': {'key': 'sections/footer.liquid', 'value': content}}
    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200

# Get footer
footer = get_footer()

# Find where to inject - right before the copyright section
injection_point = footer.find('&copy; {{ \'now\' | date: \'%Y\' }}')

if injection_point == -1:
    print("❌ Could not find copyright section")
    exit(1)

# Create investor link HTML
investor_html = '''
        <div class="footer__column footer__localization isolate">
          <div class="footer__item">
            <h2 class="footer-block__heading inline-richtext">Investors</h2>
            <ul class="footer-block__details-content list-unstyled">
              <li>
                <a href="/pages/investors" class="link link--text list-menu__item">Investor Relations</a>
              </li>
            </ul>
          </div>
        </div>
'''

# Find the grid wrapper to add column
grid_end = footer.rfind('</div>', 0, injection_point)
if grid_end != -1:
    new_footer = footer[:grid_end] + investor_html + footer[grid_end:]

    if update_footer(new_footer):
        print("✅ DONE: Investor Relations link added to footer")
        print("   Location: New 'Investors' column in footer")
        print("   Link: /pages/investors")
        print()
        print("Verify at: https://alphamedical.shop (scroll to footer)")
    else:
        print("❌ Failed to update footer")
else:
    print("❌ Could not find insertion point")
