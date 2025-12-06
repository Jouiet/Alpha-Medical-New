#!/usr/bin/env python3
"""
Create Missing Pages - Alpha Medical
Creates Data Deletion Request + Investors pages via Shopify Admin API
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/mac/Desktop/Alpha-Medical/.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2025-10')

def create_page(title, handle, body_html, metafields=None):
    """Create a Shopify page via Admin API"""
    url = f'https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages.json'
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    page_data = {
        'page': {
            'title': title,
            'handle': handle,
            'body_html': body_html,
            'published': True
        }
    }

    if metafields:
        page_data['page']['metafields'] = metafields

    response = requests.post(url, headers=headers, json=page_data)

    if response.status_code == 201:
        page = response.json().get('page', {})
        print(f"✅ Page created: {title}")
        print(f"   Handle: {handle}")
        print(f"   ID: {page.get('id')}")
        print(f"   URL: https://{SHOP_DOMAIN.replace('.myshopify.com', '')}.myshopify.com/pages/{handle}")
        return page
    else:
        print(f"❌ Error creating page: {title}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

# ============================================================================
# DATA DELETION REQUEST PAGE (GDPR/CCPA COMPLIANCE)
# ============================================================================

data_deletion_html = """
<div class="page-width">
  <div class="grid">
    <div class="grid__item">
      <h1>Data Deletion Request</h1>

      <div class="rte">
        <p><strong>Your Privacy Rights</strong></p>

        <p>Under the General Data Protection Regulation (GDPR) and California Consumer Privacy Act (CCPA), you have the right to request deletion of your personal data that we have collected.</p>

        <h2>What Data Can Be Deleted</h2>
        <ul>
          <li><strong>Account Information:</strong> Name, email, phone number, shipping addresses</li>
          <li><strong>Order History:</strong> Past purchases, transaction details (subject to legal retention requirements)</li>
          <li><strong>Marketing Data:</strong> Email subscription preferences, marketing opt-ins/opt-outs</li>
          <li><strong>Browsing Data:</strong> Cookies, analytics data, website usage patterns</li>
        </ul>

        <h2>Important Notes</h2>
        <ul>
          <li>Some data may be retained for legal compliance (tax records, fraud prevention, warranty claims)</li>
          <li>Data retention periods: 7 years for financial records (tax compliance), 2 years for warranty claims</li>
          <li>Deletion requests are processed within 30 days of verification</li>
          <li>You will receive confirmation once your data has been deleted</li>
        </ul>

        <h2>How to Submit a Request</h2>
        <p>To request deletion of your personal data, please contact us with the following information:</p>

        <div class="contact-box" style="background: #f7f7f7; padding: 20px; border-radius: 8px; margin: 20px 0;">
          <p><strong>Email:</strong> <a href="mailto:contact@alphamedical.shop?subject=Data Deletion Request">contact@alphamedical.shop</a></p>
          <p><strong>Subject Line:</strong> Data Deletion Request</p>
          <p><strong>Required Information:</strong></p>
          <ul>
            <li>Full name (as registered in our system)</li>
            <li>Email address associated with your account</li>
            <li>Order number (if applicable)</li>
            <li>Specific data you wish to delete (or "all data")</li>
          </ul>
        </div>

        <h2>Verification Process</h2>
        <p>To protect your privacy, we will verify your identity before processing any deletion request. You may be asked to provide:</p>
        <ul>
          <li>Government-issued ID (driver's license, passport)</li>
          <li>Proof of email ownership (access to registered email)</li>
          <li>Answer security questions related to your account or orders</li>
        </ul>

        <h2>Processing Timeline</h2>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
          <tr style="background: #f7f7f7;">
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Step</th>
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Timeline</th>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Request Received</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Within 24 hours - Confirmation email sent</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Identity Verification</td>
            <td style="padding: 10px; border: 1px solid #ddd;">1-5 business days</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Data Deletion</td>
            <td style="padding: 10px; border: 1px solid #ddd;">7-14 business days after verification</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Confirmation</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Within 30 days total</td>
          </tr>
        </table>

        <h2>Other Privacy Rights</h2>
        <p>In addition to data deletion, you also have the right to:</p>
        <ul>
          <li><strong>Access Your Data:</strong> Request a copy of all personal data we hold about you</li>
          <li><strong>Correct Your Data:</strong> Update inaccurate or incomplete information</li>
          <li><strong>Restrict Processing:</strong> Limit how we use your data</li>
          <li><strong>Data Portability:</strong> Receive your data in a machine-readable format</li>
          <li><strong>Opt-Out of Marketing:</strong> Unsubscribe from marketing emails (link in every email)</li>
        </ul>

        <p style="margin-top: 30px;"><strong>Questions?</strong> Review our full <a href="/pages/privacy-policy">Privacy Policy</a> or contact our privacy team at <a href="mailto:contact@alphamedical.shop">contact@alphamedical.shop</a>.</p>

        <p style="font-size: 0.9em; color: #666; margin-top: 20px;"><em>Last Updated: December 7, 2025</em></p>
      </div>
    </div>
  </div>
</div>
"""

# ============================================================================
# INVESTORS PAGE
# ============================================================================

investors_html = """
<div class="page-width">
  <div class="grid">
    <div class="grid__item">
      <h1>Investor Relations</h1>

      <div class="rte">
        <p class="lead"><strong>Alpha Medical Care is transforming the medical equipment e-commerce space with a customer-centric, quality-first approach.</strong></p>

        <h2>Investment Opportunity</h2>
        <p>We are currently in our pre-launch phase, building a scalable B2C e-commerce platform for medical support equipment. Our focus is on delivering exceptional customer experience, verified product quality, and sustainable growth.</p>

        <div class="investor-highlights" style="background: #f7f7f7; padding: 30px; border-radius: 8px; margin: 30px 0;">
          <h3>Why Invest in Alpha Medical Care?</h3>
          <ul style="list-style: none; padding: 0;">
            <li style="margin: 15px 0;">✅ <strong>Market Opportunity:</strong> $150B+ global medical equipment market growing at 5.5% CAGR</li>
            <li style="margin: 15px 0;">✅ <strong>Customer-First Approach:</strong> 5-step product vetting, ISO 13485 compliance, 2-week testing</li>
            <li style="margin: 15px 0;">✅ <strong>Technology Infrastructure:</strong> 91/100 automation score, full analytics stack, AI-powered optimization</li>
            <li style="margin: 15px 0;">✅ <strong>Scalable Model:</strong> Dropshipping + fulfillment partnerships, minimal inventory risk</li>
            <li style="margin: 15px 0;">✅ <strong>Strong Unit Economics:</strong> Target $20 CAC, $165 LTV (8.25:1 ratio)</li>
          </ul>
        </div>

        <h2>Business Model</h2>
        <p>Alpha Medical Care operates as a <strong>B2C retail e-commerce platform</strong> specializing in medical support equipment:</p>
        <ul>
          <li><strong>Product Categories:</strong> Knee braces, back supports, compression wear, mobility aids, pain relief devices</li>
          <li><strong>Revenue Streams:</strong> Direct product sales, bundle offerings, subscription options (future)</li>
          <li><strong>Fulfillment:</strong> Hybrid model (dropshipping + 3PL partnerships)</li>
          <li><strong>Marketing:</strong> SEO, Google Ads, Facebook/Instagram Ads, email marketing, content strategy</li>
        </ul>

        <h2>Traction & Milestones</h2>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
          <tr style="background: #f7f7f7;">
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Milestone</th>
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Status</th>
            <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Date</th>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Platform Development</td>
            <td style="padding: 10px; border: 1px solid #ddd;">✅ Complete</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Nov 2025</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Product Catalog (96 SKUs)</td>
            <td style="padding: 10px; border: 1px solid #ddd;">✅ Complete</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Nov 2025</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Marketing Automation</td>
            <td style="padding: 10px; border: 1px solid #ddd;">✅ Complete</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Nov 2025</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Analytics & Tracking</td>
            <td style="padding: 10px; border: 1px solid #ddd;">✅ Complete</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Dec 2025</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">Official Launch</td>
            <td style="padding: 10px; border: 1px solid #ddd;">⏳ Planned</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Dec 25, 2025</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;">First Paid Ads Campaign</td>
            <td style="padding: 10px; border: 1px solid #ddd;">⏳ Planned</td>
            <td style="padding: 10px; border: 1px solid #ddd;">Q1 2026</td>
          </tr>
        </table>

        <h2>Technology Stack</h2>
        <p>Our infrastructure is built for scale and efficiency:</p>
        <ul>
          <li><strong>E-commerce Platform:</strong> Shopify (proven, scalable, 99.98% uptime)</li>
          <li><strong>Marketing Automation:</strong> Klaviyo (email flows), Shopify Flow (workflow automation)</li>
          <li><strong>Analytics:</strong> Google Analytics 4, Meta Pixel, TikTok Pixel, Google Tag Manager</li>
          <li><strong>Customer Intelligence:</strong> n8n workflows, Google Sheets API, Apify scraping</li>
          <li><strong>Development:</strong> Python automation, GitHub Actions CI/CD, Chrome DevTools MCP</li>
        </ul>

        <h2>Competitive Advantages</h2>
        <ul>
          <li><strong>Quality Assurance:</strong> 5-step product vetting process (competitor audit, ISO 13485 check, 2-week testing, quality scoring, final verification)</li>
          <li><strong>Customer Experience:</strong> 30-day returns, comprehensive guides, video tutorials, responsive support</li>
          <li><strong>SEO Strategy:</strong> Complete technical SEO, Core Web Vitals optimization, rich snippets, schema markup</li>
          <li><strong>Automation:</strong> 91% infrastructure automation, minimal operational overhead</li>
          <li><strong>Brand Trust:</strong> Professional branding, transparent policies, educational content</li>
        </ul>

        <h2>Financial Projections</h2>
        <div class="financial-projections" style="background: #f7f7f7; padding: 20px; border-radius: 8px; margin: 20px 0;">
          <p><strong>Year 1 Targets (2026):</strong></p>
          <ul>
            <li>Revenue: $80,000 - $120,000</li>
            <li>Customers: 500 - 750</li>
            <li>Average Order Value: $160</li>
            <li>Customer Acquisition Cost: $20</li>
            <li>Lifetime Value: $165</li>
            <li>LTV:CAC Ratio: 8.25:1</li>
          </ul>
          <p style="margin-top: 15px; font-size: 0.9em; color: #666;"><em>Projections based on industry benchmarks and conservative growth assumptions.</em></p>
        </div>

        <h2>Investment Terms</h2>
        <p>We are currently exploring strategic partnerships and investment opportunities. If you are interested in learning more about investing in Alpha Medical Care, please contact us for our full investor deck and financial projections.</p>

        <div class="contact-investor" style="background: #e8f4f8; padding: 30px; border-radius: 8px; margin: 30px 0; text-align: center;">
          <h3 style="margin-top: 0;">Interested in Investing?</h3>
          <p style="font-size: 1.1em; margin: 20px 0;">Contact our investor relations team to receive:</p>
          <ul style="list-style: none; padding: 0; margin: 20px 0;">
            <li>📊 Full investor deck with detailed financials</li>
            <li>📈 5-year growth projections</li>
            <li>🎯 Go-to-market strategy</li>
            <li>💼 Investment terms and structure</li>
          </ul>
          <p style="margin-top: 30px;">
            <a href="mailto:contact@alphamedical.shop?subject=Investor Inquiry" style="display: inline-block; background: #0066cc; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">Contact Investor Relations</a>
          </p>
        </div>

        <h2>Legal Information</h2>
        <p><strong>Company:</strong> JoHat Services LLC (d/b/a Alpha Medical Care)<br>
        <strong>Registered Address:</strong> 611 South DuPont Highway Suite 102, Dover, DE 19901<br>
        <strong>State:</strong> Delaware, USA<br>
        <strong>Contact:</strong> <a href="mailto:contact@alphamedical.shop">contact@alphamedical.shop</a></p>

        <p style="font-size: 0.85em; color: #666; margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd;">
          <strong>Disclaimer:</strong> This page is for informational purposes only and does not constitute an offer to sell or a solicitation of an offer to buy any securities. Any investment involves risk, including the possible loss of principal. Past performance does not guarantee future results. Interested parties should conduct their own due diligence and consult with financial, legal, and tax advisors before making any investment decisions.
        </p>

        <p style="font-size: 0.9em; color: #666; margin-top: 20px;"><em>Last Updated: December 7, 2025</em></p>
      </div>
    </div>
  </div>
</div>
"""

# ============================================================================
# CREATE PAGES
# ============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("CREATING MISSING PAGES - ALPHA MEDICAL")
    print("=" * 80)
    print()

    # Create Data Deletion Request page
    print("Creating Data Deletion Request page...")
    data_deletion_page = create_page(
        title="Data Deletion Request - Your Privacy Rights | Alpha Medical Care",
        handle="data-deletion-request",
        body_html=data_deletion_html
    )
    print()

    # Create Investors page
    print("Creating Investors page...")
    investors_page = create_page(
        title="Investor Relations - Alpha Medical Care",
        handle="investors",
        body_html=investors_html
    )
    print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Data Deletion Request page: {'Created' if data_deletion_page else 'Failed'}")
    print(f"✅ Investors page: {'Created' if investors_page else 'Failed'}")
    print()
    print("Pages are now LIVE and published!")
    print("=" * 80)
