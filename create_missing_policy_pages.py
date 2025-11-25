#!/usr/bin/env python3
"""
Create Missing Policy Pages
Session 52 - Programmatic Fix

Missing pages:
1. privacy-policy
2. shipping-policy
3. refund-policy

Note: These pages MUST exist for legal compliance and customer trust
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2024-10'
BASE_URL = f'https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}'

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

def api_request(endpoint, method='GET', data=None):
    url = f'{BASE_URL}{endpoint}'
    try:
        response = requests.request(method, url, headers=HEADERS, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e), 'response': getattr(e, 'response', None)}

print("=" * 80)
print("CREATE MISSING POLICY PAGES")
print("=" * 80)

# Policy pages content (basic templates - can be customized later)
policies = {
    'privacy-policy': {
        'title': 'Privacy Policy',
        'handle': 'privacy-policy',
        'body_html': '''<h1>Privacy Policy</h1>
<p><strong>Last Updated:</strong> November 26, 2025</p>

<h2>1. Information We Collect</h2>
<p>Alpha Medical Care collects information you provide directly to us when you:</p>
<ul>
<li>Create an account</li>
<li>Place an order</li>
<li>Subscribe to our newsletter</li>
<li>Contact customer support</li>
</ul>

<h2>2. How We Use Your Information</h2>
<p>We use the information we collect to:</p>
<ul>
<li>Process and fulfill your orders</li>
<li>Communicate with you about your orders</li>
<li>Send you marketing communications (with your consent)</li>
<li>Improve our products and services</li>
</ul>

<h2>3. Information Sharing</h2>
<p>We do not sell, trade, or rent your personal information to third parties. We may share your information with:</p>
<ul>
<li>Service providers who assist with order fulfillment and payment processing</li>
<li>Law enforcement when required by law</li>
</ul>

<h2>4. Data Security</h2>
<p>We implement appropriate security measures to protect your personal information. All payment transactions are encrypted using SSL technology.</p>

<h2>5. Your Rights</h2>
<p>You have the right to:</p>
<ul>
<li>Access your personal data</li>
<li>Request correction of your data</li>
<li>Request deletion of your data</li>
<li>Opt-out of marketing communications</li>
</ul>

<h2>6. Cookies</h2>
<p>We use cookies to enhance your shopping experience. You can disable cookies in your browser settings, but this may affect site functionality.</p>

<h2>7. Contact Us</h2>
<p>For privacy-related questions, please contact us at:</p>
<p>Email: privacy@alphamedical.shop</p>

<h2>8. Changes to This Policy</h2>
<p>We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page.</p>'''
    },
    'shipping-policy': {
        'title': 'Shipping Policy',
        'handle': 'shipping-policy',
        'body_html': '''<h1>Shipping Policy</h1>
<p><strong>Last Updated:</strong> November 26, 2025</p>

<h2>1. Shipping Methods</h2>
<p>We offer the following shipping options:</p>
<ul>
<li><strong>Standard Shipping:</strong> 5-7 business days</li>
<li><strong>Expedited Shipping:</strong> 2-3 business days</li>
<li><strong>Express Shipping:</strong> 1-2 business days</li>
</ul>

<h2>2. Shipping Costs</h2>
<p>Shipping costs are calculated at checkout based on:</p>
<ul>
<li>Order weight and dimensions</li>
<li>Delivery destination</li>
<li>Selected shipping method</li>
</ul>
<p><strong>Free Shipping:</strong> Orders over $50 qualify for free standard shipping within the continental United States.</p>

<h2>3. Processing Time</h2>
<p>Orders are processed within 1-2 business days (Monday-Friday, excluding holidays). Orders placed after 2 PM EST will be processed the next business day.</p>

<h2>4. Delivery</h2>
<p>Delivery times are estimates and not guaranteed. Shipping carriers may experience delays due to weather, high volume, or other factors beyond our control.</p>

<h2>5. Tracking</h2>
<p>Once your order ships, you will receive a tracking number via email. You can track your order using this number on the carrier's website.</p>

<h2>6. International Shipping</h2>
<p>We currently ship within the United States only. International shipping will be available in the future.</p>

<h2>7. Shipping Restrictions</h2>
<p>We cannot ship to:</p>
<ul>
<li>PO Boxes (for expedited/express shipping)</li>
<li>Military APO/FPO addresses (please contact us for options)</li>
</ul>

<h2>8. Lost or Damaged Packages</h2>
<p>If your package is lost or arrives damaged, please contact us within 48 hours of expected delivery. We will work with the carrier to resolve the issue.</p>

<h2>9. Contact Us</h2>
<p>For shipping-related questions, please contact us at:</p>
<p>Email: shipping@alphamedical.shop</p>'''
    },
    'refund-policy': {
        'title': 'Refund Policy',
        'handle': 'refund-policy',
        'body_html': '''<h1>Refund Policy</h1>
<p><strong>Last Updated:</strong> November 26, 2025</p>

<h2>1. Return Period</h2>
<p>You may return most items within <strong>30 days</strong> of delivery for a full refund.</p>

<h2>2. Eligible Returns</h2>
<p>To be eligible for a return, items must:</p>
<ul>
<li>Be in original condition and packaging</li>
<li>Include all original tags and documentation</li>
<li>Not have been used or worn</li>
<li>Be returned within 30 days of delivery</li>
</ul>

<h2>3. Non-Returnable Items</h2>
<p>The following items cannot be returned:</p>
<ul>
<li>Items marked as "Final Sale"</li>
<li>Opened hygiene products (for health and safety reasons)</li>
<li>Customized or personalized items</li>
<li>Gift cards</li>
</ul>

<h2>4. Return Process</h2>
<p>To initiate a return:</p>
<ol>
<li>Contact our customer service team at returns@alphamedical.shop</li>
<li>Provide your order number and reason for return</li>
<li>Receive a Return Authorization (RA) number</li>
<li>Package the item securely with the RA number</li>
<li>Ship the item to our returns center (address provided with RA)</li>
</ol>

<h2>5. Return Shipping Costs</h2>
<ul>
<li><strong>Defective or incorrect items:</strong> We cover return shipping</li>
<li><strong>Change of mind:</strong> Customer is responsible for return shipping</li>
</ul>
<p>We recommend using a trackable shipping method. We are not responsible for lost return packages.</p>

<h2>6. Refund Processing</h2>
<p>Once we receive your return:</p>
<ul>
<li>Inspection: 2-3 business days</li>
<li>Refund processing: 3-5 business days</li>
<li>Credit to original payment method: 5-10 business days (depending on your bank)</li>
</ul>

<h2>7. Exchanges</h2>
<p>We do not offer direct exchanges. If you need a different size or product, please:</p>
<ol>
<li>Return the original item for a refund</li>
<li>Place a new order for the desired item</li>
</ol>

<h2>8. Damaged or Defective Items</h2>
<p>If you receive a damaged or defective item:</p>
<ul>
<li>Contact us within 48 hours of delivery</li>
<li>Provide photos of the damage/defect</li>
<li>We will arrange a free return and send a replacement or issue a full refund</li>
</ul>

<h2>9. Restocking Fee</h2>
<p>We do not charge restocking fees for standard returns.</p>

<h2>10. Contact Us</h2>
<p>For return or refund questions, please contact us at:</p>
<p>Email: returns@alphamedical.shop</p>
<p>Phone: Available on our Contact page</p>'''
    }
}

# Create each policy page
created = []
failed = []

for handle, policy_data in policies.items():
    print(f"\n{'='*80}")
    print(f"Creating: {policy_data['title']}")
    print(f"{'='*80}")

    # First check if page already exists
    check_result = api_request(f'/pages.json?handle={handle}')

    if 'pages' in check_result and len(check_result['pages']) > 0:
        print(f"⚠️  Page already exists (ID: {check_result['pages'][0]['id']})")
        print(f"   Skipping creation")
        created.append(handle)
        continue

    # Create page
    create_data = {
        'page': {
            'title': policy_data['title'],
            'body_html': policy_data['body_html'],
            'handle': policy_data['handle'],
            'published': True
        }
    }

    result = api_request('/pages.json', method='POST', data=create_data)

    if 'page' in result:
        page = result['page']
        print(f"✅ Created successfully")
        print(f"   ID: {page['id']}")
        print(f"   URL: https://www.alphamedical.shop/pages/{page['handle']}")
        created.append(handle)
    else:
        print(f"❌ Failed to create")
        if 'error' in result:
            print(f"   Error: {result['error']}")
        failed.append(handle)

# Final verification
print(f"\n{'='*80}")
print("FINAL VERIFICATION")
print(f"{'='*80}")

pages_result = api_request('/pages.json')
if 'pages' in pages_result:
    existing_handles = [p['handle'] for p in pages_result['pages']]

    print(f"Total pages: {len(pages_result['pages'])}")
    print(f"\nPolicy pages status:")

    for handle in ['privacy-policy', 'shipping-policy', 'refund-policy']:
        if handle in existing_handles:
            print(f"  ✅ {handle}")
        else:
            print(f"  ❌ {handle} - MISSING")

print(f"\n{'='*80}")
print("SUMMARY")
print(f"{'='*80}")
print(f"Created: {len(created)}")
print(f"Failed: {len(failed)}")

if len(failed) == 0:
    print("\n✅ ALL POLICY PAGES NOW EXIST!")
else:
    print(f"\n⚠️  Failed to create:")
    for h in failed:
        print(f"   - {h}")

print("=" * 80)
