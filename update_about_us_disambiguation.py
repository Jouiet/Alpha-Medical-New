#!/usr/bin/env python3
"""
UPDATE ABOUT US PAGE - Add Brand Disambiguation
Modifies existing About Us page to clarify: NOT Hello Alpha, NOT AlphaMedicalStore
"""

import os
import json
import requests

# Load credentials
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"

try:
    with open('.env.admin', 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except:
    print("❌ Failed to load credentials from .env.admin")
    exit(1)

API_VERSION = "2025-10"
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

def rest_request(method, endpoint, data=None):
    """Execute REST API request"""
    url = f"{REST_URL}{endpoint}"
    if method == "GET":
        response = requests.get(url, headers=HEADERS)
    elif method == "PUT":
        response = requests.put(url, headers=HEADERS, json=data)
    elif method == "POST":
        response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code not in [200, 201]:
        print(f"❌ API Error: {response.status_code}")
        print(response.text)
        return None
    return response.json()

# STEP 1: Get all pages to find About Us
print("🔍 Finding About Us page...")
pages_response = rest_request("GET", "/pages.json")
if not pages_response:
    exit(1)

about_page = None
for page in pages_response.get('pages', []):
    if 'about' in page.get('handle', '').lower():
        about_page = page
        print(f"✅ Found: {page['title']} (ID: {page['id']}, Handle: {page['handle']})")
        break

if not about_page:
    print("❌ About Us page not found!")
    exit(1)

# STEP 2: Updated content with brand disambiguation
NEW_CONTENT = """
<h1>About Alpha Medical Care</h1>

<div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
  <h2 style="margin-top: 0;">⚠️ Important Brand Clarification</h2>
  <p><strong>Alpha Medical Care</strong> (alphamedical.shop) is a Canadian medical equipment retailer specializing in orthopedic products and recovery devices.</p>

  <h3>We Are NOT:</h3>
  <ul>
    <li>❌ <strong>Hello Alpha</strong> (helloalpha.com) - a telemedicine provider offering online consultations</li>
    <li>❌ <strong>AlphaMedicalStore.com</strong> - a fraudulent website selling illegal pharmaceuticals</li>
    <li>❌ Any other "Alpha Medical" entities</li>
  </ul>

  <h3>We ARE:</h3>
  <ul>
    <li>✅ A legitimate Shopify-based e-commerce store</li>
    <li>✅ Specializing in FDA-compliant orthopedic equipment</li>
    <li>✅ Focused on helping office workers, athletes, and individuals with chronic pain</li>
    <li>✅ Based in Canada, serving customers internationally</li>
  </ul>
</div>

<h2>Our Mission</h2>
<p>Founded in 2025 with a passion for improving lives, Alpha Medical Care has become a trusted provider of medical support equipment. Our mission is to make professional-grade orthopedic and therapeutic solutions accessible to everyone who needs them.</p>

<p>We believe that quality medical equipment shouldn't be reserved for clinical settings. Whether you're an office worker dealing with desk pain, an athlete recovering from injury, or someone managing chronic conditions, you deserve access to the same high-quality support products used by professionals.</p>

<h2>What We Sell</h2>

<h3>Orthopedic Support</h3>
<ul>
  <li>Knee braces and supports</li>
  <li>Ankle braces</li>
  <li>Wrist and carpal tunnel braces</li>
  <li>Back and posture correctors</li>
  <li>Cervical neck traction devices</li>
  <li>Elbow supports</li>
</ul>

<h3>Therapy & Recovery Equipment</h3>
<ul>
  <li>LED light therapy masks</li>
  <li>EMS (electrical muscle stimulation) devices</li>
  <li>Cupping therapy sets</li>
  <li>Massage and percussion devices</li>
  <li>Compression therapy boots</li>
</ul>

<h3>All Products Feature:</h3>
<ul>
  <li>FDA-compliant materials</li>
  <li>Medical-grade construction</li>
  <li>Adjustable, customizable fit</li>
  <li>Breathable, comfortable designs</li>
  <li>Clinical effectiveness backed by research</li>
</ul>

<h2>What We DON'T Sell</h2>
<p>To avoid any confusion:</p>
<ul>
  <li>❌ <strong>NO prescription medications</strong> (we are NOT a pharmacy)</li>
  <li>❌ <strong>NO pharmaceutical drugs</strong> of any kind</li>
  <li>❌ <strong>NO telemedicine consultations</strong> (we are NOT Hello Alpha)</li>
  <li>❌ <strong>NO controlled substances</strong></li>
</ul>
<p>We sell <strong>physical medical equipment only</strong> - braces, supports, and therapeutic devices.</p>

<h2>Our Guarantee</h2>
<p>Every product comes with:</p>
<ul>
  <li>✅ 30-day money-back guarantee</li>
  <li>✅ Quality assurance</li>
  <li>✅ Secure Shopify checkout</li>
  <li>✅ Responsive customer support</li>
</ul>

<h2>Contact Us</h2>
<p><strong>Email:</strong> support@alphamedical.shop<br>
<strong>Hours:</strong> Monday - Friday, 9:00 AM - 6:00 PM EST<br>
<strong>Platform:</strong> Shopify (secure checkout)<br>
<strong>Location:</strong> Canada</p>

<p><strong>Website:</strong> <a href="https://www.alphamedical.shop">https://www.alphamedical.shop</a><br>
<strong>Shopify Store ID:</strong> azffej-as</p>

<h2>Follow Us</h2>
<p>Stay connected for product updates, health tips, and exclusive offers:</p>
<ul>
  <li>Instagram: @alphamedical</li>
  <li>TikTok: @alphamedical</li>
  <li>Facebook: Alpha Medical Care</li>
</ul>

<hr>
<p><em>Alpha Medical Care is an independent medical equipment retailer. We are not affiliated with, endorsed by, or connected to Hello Alpha, AlphaMedicalStore.com, or any other similarly-named entities.</em></p>
""".strip()

# STEP 3: Update the page
print(f"\n🔄 Updating About Us page (ID: {about_page['id']})...")
update_data = {
    "page": {
        "id": about_page['id'],
        "body_html": NEW_CONTENT,
        "published": True
    }
}

result = rest_request("PUT", f"/pages/{about_page['id']}.json", update_data)

if result:
    print("✅ About Us page updated successfully!")
    print(f"📄 URL: https://www.alphamedical.shop/pages/{about_page['handle']}")
    print("\n📊 Changes made:")
    print("  ✅ Added brand disambiguation section (top of page)")
    print("  ✅ Clarified: NOT Hello Alpha")
    print("  ✅ Clarified: NOT AlphaMedicalStore.com")
    print("  ✅ Added 'What we DON'T sell' section")
    print("  ✅ Added Shopify Store ID")
    print("  ✅ Updated contact information")
else:
    print("❌ Failed to update page!")
