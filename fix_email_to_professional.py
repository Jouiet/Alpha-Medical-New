#!/usr/bin/env python3
"""
FIX CRITICAL: Replace personal email with professional Alpha Medical email
jouiet.hat@gmail.com → contact@alphamedical.shop
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
API_VERSION = '2024-01'
BASE_URL = f'https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}'
GRAPHQL_URL = f'{BASE_URL}/graphql.json'

HEADERS = {
    'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
    'Content-Type': 'application/json'
}

PROFESSIONAL_EMAIL = 'contact@alphamedical.shop'

def update_terms_of_service():
    """Update Terms of Service with professional email"""

    terms_content = f"""# Terms of Service

**Last Updated:** December 2025

## Agreement to Terms

Welcome to Alpha Medical Care ("Company", "we", "our", "us"). By accessing our website at alphamedical.shop and purchasing our products, you agree to be bound by these Terms of Service and all applicable laws and regulations.

## Eligibility

You must be at least 18 years of age to use this website and purchase our products. By using this site, you represent and warrant that you are at least 18 years old.

## Products and Services

Alpha Medical Care specializes in medical equipment including knee braces, posture correctors, and therapy devices. All products are described with accuracy to the best of our ability. We reserve the right to:

- Refuse or cancel any order
- Limit quantities purchased
- Discontinue products at any time
- Change prices without notice

## Use of Website

You agree to use our website only for lawful purposes. You must not:

- Use the site in any way that violates any applicable law or regulation
- Transmit any viruses, malware, or harmful code
- Attempt to gain unauthorized access to our systems
- Impersonate any person or entity
- Interfere with the proper functioning of the website

## Intellectual Property

All content on this website, including text, graphics, logos, images, and software, is the property of Alpha Medical Care and protected by copyright and trademark laws. You may not reproduce, distribute, or create derivative works without our express written permission.

## Product Information and Pricing

We strive to provide accurate product descriptions and pricing. However:

- Prices are subject to change without notice
- We are not responsible for typographical errors
- Product images are for illustration purposes
- Actual products may vary slightly from images

## Orders and Payment

When you place an order, you agree to:

- Provide accurate and complete information
- Promptly update account information
- Authorize us to charge your payment method
- Pay all charges at posted prices, including shipping and taxes

We accept major credit cards through our secure payment processor. Payment information is encrypted and processed securely.

## Shipping and Delivery

Please refer to our Shipping Policy for detailed information about:

- Processing times (1-2 business days)
- Delivery timeframes (5-7 business days standard, 2-3 express)
- Shipping costs
- International shipping restrictions
- Tracking information

## Returns and Refunds

Please see our Refund Policy for complete details on:

- 30-day return window
- Unopened products requirement
- Hygiene products (non-returnable)
- Refund processing (5-7 business days)
- Return shipping costs

## Medical Disclaimer

**IMPORTANT:** The products sold on this website are NOT intended to diagnose, treat, cure, or prevent any disease. Our products are designed to provide support and comfort.

You should:

- Consult with a healthcare professional before using our products
- Not use our products as a substitute for professional medical advice
- Discontinue use and seek medical attention if you experience adverse effects
- Read all product instructions and warnings carefully

We are not liable for any health issues arising from product use.

## Limitation of Liability

To the maximum extent permitted by law:

- We are not liable for any indirect, incidental, special, or consequential damages
- Our total liability shall not exceed the amount you paid for the product
- We are not responsible for delays or failures due to circumstances beyond our control
- We do not guarantee uninterrupted or error-free website operation

## Indemnification

You agree to indemnify and hold harmless Alpha Medical Care, its officers, directors, employees, and agents from any claims, losses, damages, liabilities, and expenses (including legal fees) arising from:

- Your use of the website
- Your violation of these Terms
- Your violation of any rights of another party
- Your use or misuse of our products

## Privacy and Data Protection

Your privacy is important to us. Please review our Privacy Policy to understand how we collect, use, and protect your personal information. By using our website, you consent to our data practices as described in our Privacy Policy.

## Dispute Resolution

**Governing Law:** These Terms are governed by the laws of Delaware, United States, without regard to conflict of law principles.

**Arbitration Agreement:** Any dispute arising from these Terms or your use of our website shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association. You waive your right to participate in class action lawsuits.

**Jurisdiction:** If arbitration is not applicable, you agree to exclusive jurisdiction in the state and federal courts located in Delaware.

## Modifications to Terms

We reserve the right to modify these Terms of Service at any time. Changes become effective immediately upon posting to the website. Your continued use of the website after changes constitutes acceptance of the modified Terms.

We will update the "Last Updated" date at the top of this page when we make changes.

## Termination

We may terminate or suspend your access to our website immediately, without prior notice, for any reason, including:

- Breach of these Terms
- Fraudulent activity
- At our sole discretion

Upon termination, your right to use the website ceases immediately.

## Severability

If any provision of these Terms is found to be unenforceable or invalid, that provision will be limited or eliminated to the minimum extent necessary, and the remaining provisions will remain in full force and effect.

## Entire Agreement

These Terms of Service, together with our Privacy Policy, Refund Policy, and Shipping Policy, constitute the entire agreement between you and Alpha Medical Care regarding use of our website.

## Contact Information

If you have any questions about these Terms of Service, please contact us:

**Alpha Medical Care**
- Email: {PROFESSIONAL_EMAIL}
- Address: 611 South Dupont Highway Suite 102, Harrington, DE 19901, United States
- Website: alphamedical.shop

## Acknowledgment

By using our website and purchasing our products, you acknowledge that you have read, understood, and agree to be bound by these Terms of Service.

---

**Effective Date:** December 2025
**Last Reviewed:** December 4, 2025
"""

    mutation = """
    mutation shopPolicyUpdate($shopPolicy: ShopPolicyInput!) {
      shopPolicyUpdate(shopPolicy: $shopPolicy) {
        shopPolicy {
          id
          type
          body
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "shopPolicy": {
            "type": "TERMS_OF_SERVICE",
            "body": terms_content
        }
    }

    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={'query': mutation, 'variables': variables}
    )

    result = response.json()

    if 'errors' in result:
        print(f"❌ Terms of Service GraphQL ERROR: {result['errors']}")
        return False

    data = result.get('data', {}).get('shopPolicyUpdate', {})

    if data.get('userErrors'):
        print(f"❌ Terms of Service USER ERRORS: {data['userErrors']}")
        return False

    print(f"✅ Terms of Service: UPDATED with {PROFESSIONAL_EMAIL}")
    return True


def update_shipping_policy():
    """Update Shipping Policy with professional email"""

    shipping_content = f"""# Shipping & Delivery Policy

**Last Updated:** December 2025

## Shipping Information

At Alpha Medical Care, we strive to process and ship your orders as quickly as possible to help you get the relief and support you need.

### Processing Time

- **Standard Orders:** 1-2 business days
- **Custom/Special Orders:** 3-5 business days
- Orders placed on weekends/holidays are processed the next business day

### Shipping Methods & Delivery Times

**Within the United States:**

1. **Standard Shipping** (5-7 business days)
   - FREE on orders $50 and above
   - $4.99 for orders under $50

2. **Express Shipping** (2-3 business days)
   - $9.99 flat rate

3. **Priority Shipping** (1-2 business days)
   - $19.99 flat rate

**Note:** Delivery times are estimates and not guaranteed. Delays may occur due to weather, carrier issues, or other circumstances beyond our control.

### International Shipping

Currently, we ship primarily within the United States. For international orders:

- Contact us at {PROFESSIONAL_EMAIL} for availability
- International shipping rates calculated at checkout
- Customs duties and taxes are the customer's responsibility
- Delivery times vary by destination (typically 10-21 business days)

## Order Tracking

Once your order ships, you will receive:

- Email confirmation with tracking number
- Direct link to track your package
- Carrier information (USPS, UPS, or FedEx)

Track your order anytime through:
- Your account dashboard at alphamedical.shop
- Carrier's website using your tracking number
- Email us at {PROFESSIONAL_EMAIL} for assistance

## Shipping Address

**Important:**

- Verify your shipping address before completing checkout
- We ship to the address provided at checkout
- Address changes must be requested within 1 hour of order placement
- We are not responsible for packages shipped to incorrect addresses provided by customers

**P.O. Boxes:**
- We ship to P.O. Boxes via USPS
- Express/Priority shipping not available for P.O. Boxes

## Lost or Damaged Packages

### Lost Packages

If your package shows "delivered" but you haven't received it:

1. Check with neighbors or building management
2. Verify the delivery address
3. Wait 24 hours (sometimes marked delivered early)
4. Contact us at {PROFESSIONAL_EMAIL} within 7 days

We will:
- File a claim with the carrier
- Investigate the issue
- Provide replacement or refund once claim is resolved

### Damaged Packages

If your package arrives damaged:

1. Document damage with photos (box and product)
2. Contact us at {PROFESSIONAL_EMAIL} within 48 hours
3. Provide order number and photos

We will:
- Send a replacement immediately
- Provide prepaid return label for damaged item
- Process at no additional cost to you

## Shipping Restrictions

We cannot ship to:

- APO/FPO addresses (military bases - contact us for alternatives)
- Freight forwarders
- Certain international destinations (restricted by carrier or law)

Some products have specific shipping restrictions due to size, weight, or regulations.

## Holidays and Peak Seasons

During holidays and peak seasons (Black Friday, Christmas, etc.):

- Processing times may extend to 3-5 business days
- Carrier delays are more common
- Order early to ensure timely delivery
- Check our website for holiday shipping deadlines

## Returns and Exchanges

For information about returns and exchanges, please see our Refund Policy.

**Quick Summary:**
- 30-day return window from delivery date
- Products must be unopened and unused
- Customer pays return shipping unless item is defective
- Refunds processed within 5-7 business days of receiving return

## Contact Us

Questions about shipping? We're here to help!

**Alpha Medical Care**
- Email: {PROFESSIONAL_EMAIL}
- Address: 611 South Dupont Highway Suite 102, Harrington, DE 19901, United States
- Website: alphamedical.shop

**Support Hours:**
- Monday - Friday: 9:00 AM - 6:00 PM EST
- Saturday - Sunday: Closed
- Response time: Within 24 hours on business days

---

**Note:** This shipping policy is subject to change. Please check this page for the most current information. Your order confirmation email will reflect the shipping terms in effect at the time of your purchase.

**Last Reviewed:** December 4, 2025
"""

    mutation = """
    mutation shopPolicyUpdate($shopPolicy: ShopPolicyInput!) {
      shopPolicyUpdate(shopPolicy: $shopPolicy) {
        shopPolicy {
          id
          type
          body
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "shopPolicy": {
            "type": "SHIPPING_POLICY",
            "body": shipping_content
        }
    }

    response = requests.post(
        GRAPHQL_URL,
        headers=HEADERS,
        json={'query': mutation, 'variables': variables}
    )

    result = response.json()

    if 'errors' in result:
        print(f"❌ Shipping Policy GraphQL ERROR: {result['errors']}")
        return False

    data = result.get('data', {}).get('shopPolicyUpdate', {})

    if data.get('userErrors'):
        print(f"❌ Shipping Policy USER ERRORS: {data['userErrors']}")
        return False

    print(f"✅ Shipping Policy: UPDATED with {PROFESSIONAL_EMAIL}")
    return True


def update_cancellation_policy():
    """Update Cancellation Policy page with professional email"""

    # First, get the page ID
    response = requests.get(f'{BASE_URL}/pages.json', headers=HEADERS)
    pages = response.json().get('pages', [])

    page_id = None
    for page in pages:
        if 'cancellation' in page.get('handle', '').lower():
            page_id = page['id']
            break

    if not page_id:
        print("❌ Cancellation Policy page not found")
        return False

    cancellation_content = f"""<h1>Purchase Options & Cancellation Policy</h1>

<p><strong>Last Updated:</strong> December 2025</p>

<h2>Order Cancellation</h2>

<h3>Before Shipment</h3>

<p>If your order has not yet shipped, you may cancel it for a full refund:</p>

<ul>
<li><strong>Time Window:</strong> Cancel within 24 hours of order placement for guaranteed cancellation</li>
<li><strong>How to Cancel:</strong> Email {PROFESSIONAL_EMAIL} with your order number</li>
<li><strong>Refund:</strong> Full refund to original payment method within 5-7 business days</li>
<li><strong>Processing:</strong> Once an order enters fulfillment, cancellation may not be possible</li>
</ul>

<h3>After Shipment</h3>

<p>Once your order has shipped:</p>

<ul>
<li>Cancellation is no longer available</li>
<li>You may refuse delivery and return to sender</li>
<li>Standard return policy applies (see Refund Policy)</li>
<li>Original shipping charges are non-refundable</li>
</ul>

<h2>Subscription Management</h2>

<h3>Future Feature</h3>

<p>Alpha Medical Care plans to offer subscription services for regular product deliveries. When available, subscription management will include:</p>

<ul>
<li><strong>Cancellation:</strong> Cancel anytime from your account dashboard</li>
<li><strong>Pausing:</strong> Pause subscriptions for up to 3 months</li>
<li><strong>Frequency Changes:</strong> Modify delivery frequency</li>
<li><strong>Product Swaps:</strong> Change products in your subscription</li>
<li><strong>No Penalties:</strong> No cancellation fees or penalties</li>
</ul>

<h3>Current Status</h3>

<p>Subscription services are not yet active. All current purchases are one-time orders. We will notify customers via email when subscription options become available.</p>

<h2>Refund Process</h2>

<h3>Cancellation Refunds</h3>

<p>When you successfully cancel an order before shipment:</p>

<ol>
<li><strong>Confirmation:</strong> Receive email confirmation of cancellation within 24 hours</li>
<li><strong>Processing:</strong> Refund initiated within 1-2 business days</li>
<li><strong>Timing:</strong> Refund appears in your account within 5-7 business days</li>
<li><strong>Method:</strong> Refunded to original payment method</li>
</ol>

<h3>Refund Amount</h3>

<ul>
<li><strong>Pre-Shipment Cancellation:</strong> 100% refund (all charges)</li>
<li><strong>Post-Shipment Return:</strong> Product cost only (shipping non-refundable)</li>
<li><strong>Partial Cancellations:</strong> Refund for cancelled items only</li>
</ul>

<h2>Order Modifications</h2>

<h3>Change Requests</h3>

<p>If you need to modify your order (address, product, quantity):</p>

<ul>
<li><strong>Time Window:</strong> Within 1 hour of order placement</li>
<li><strong>Contact Method:</strong> Email {PROFESSIONAL_EMAIL} immediately</li>
<li><strong>Information Needed:</strong> Order number and requested changes</li>
<li><strong>Feasibility:</strong> Changes depend on order processing status</li>
</ul>

<h3>What Can Be Changed</h3>

<ul>
<li>Shipping address (if not yet shipped)</li>
<li>Product selection (if not yet processed)</li>
<li>Quantity (subject to inventory)</li>
<li>Shipping method (may incur additional charges)</li>
</ul>

<h2>Special Circumstances</h2>

<h3>Medical Emergencies</h3>

<p>If a medical emergency prevents you from using a product:</p>

<ul>
<li>Contact us at {PROFESSIONAL_EMAIL} with documentation</li>
<li>We will work with you on a case-by-case basis</li>
<li>Extended return windows may be available</li>
<li>Doctor's note or medical documentation may be required</li>
</ul>

<h3>Defective Products</h3>

<p>For defective or damaged products:</p>

<ul>
<li>No cancellation needed - automatic replacement or refund</li>
<li>Contact us within 48 hours of delivery</li>
<li>Provide photos of defect or damage</li>
<li>Prepaid return label provided</li>
<li>Full refund including original shipping</li>
</ul>

<h2>Non-Cancellable Items</h2>

<p>The following cannot be cancelled once ordered:</p>

<ul>
<li>Custom or personalized products (if we offer them in future)</li>
<li>Products marked as "Final Sale"</li>
<li>Digital products or downloads (if applicable)</li>
<li>Products already delivered</li>
</ul>

<h2>Contact Information</h2>

<p>To cancel an order or for questions about this policy:</p>

<p><strong>Alpha Medical Care</strong></p>
<ul>
<li>Email: {PROFESSIONAL_EMAIL}</li>
<li>Address: 611 South Dupont Highway Suite 102, Harrington, DE 19901, United States</li>
<li>Website: alphamedical.shop</li>
</ul>

<p><strong>Support Hours:</strong></p>
<ul>
<li>Monday - Friday: 9:00 AM - 6:00 PM EST</li>
<li>Response time: Within 24 hours on business days</li>
</ul>

<h2>Related Policies</h2>

<p>For more information, please see:</p>

<ul>
<li><strong>Refund Policy:</strong> Complete return and refund procedures</li>
<li><strong>Shipping Policy:</strong> Delivery times and shipping methods</li>
<li><strong>Terms of Service:</strong> General terms and conditions</li>
</ul>

<hr>

<p><em>This cancellation policy is subject to change. Please check this page for the most current information.</em></p>

<p><strong>Last Reviewed:</strong> December 4, 2025</p>
"""

    page_data = {
        "page": {
            "id": page_id,
            "body_html": cancellation_content
        }
    }

    response = requests.put(
        f'{BASE_URL}/pages/{page_id}.json',
        headers=HEADERS,
        json=page_data
    )

    if response.status_code == 200:
        print(f"✅ Cancellation Policy: UPDATED with {PROFESSIONAL_EMAIL}")
        return True
    else:
        print(f"❌ Cancellation Policy UPDATE FAILED: {response.status_code}")
        print(response.text)
        return False


def main():
    print("=" * 80)
    print("FIX CRITICAL: REPLACE PERSONAL EMAIL WITH PROFESSIONAL EMAIL")
    print("=" * 80)
    print(f"\n🔄 Updating all policies: jouiet.hat@gmail.com → {PROFESSIONAL_EMAIL}\n")

    results = {
        "Terms of Service": update_terms_of_service(),
        "Shipping Policy": update_shipping_policy(),
        "Cancellation Policy": update_cancellation_policy()
    }

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    for policy, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status}: {policy}")

    if all(results.values()):
        print(f"\n✅ ALL POLICIES UPDATED with {PROFESSIONAL_EMAIL}")
        print("\n⚠️  NOTE: Shop contact email in Settings still shows personal email")
        print("   This requires manual update in Shopify Admin: Settings → Store details")
        return 0
    else:
        print("\n❌ SOME UPDATES FAILED - Please review errors above")
        return 1


if __name__ == "__main__":
    exit(main())
