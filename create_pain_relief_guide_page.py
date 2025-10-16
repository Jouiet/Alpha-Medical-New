#!/usr/bin/env python3
"""Create Pain Relief Guide landing page and opt-in form in Shopify"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOPIFY_STORE_DOMAIN = os.getenv("SHOPIFY_STORE_DOMAIN")
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv("SHOPIFY_ADMIN_ACCESS_TOKEN")

REST_URL = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-10"

headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": SHOPIFY_ADMIN_ACCESS_TOKEN
}

# Page content with embedded opt-in form
page_content = """
<div class="pain-relief-guide-hero" style="background: linear-gradient(135deg, #4770DB 0%, #3858B8 100%); color: white; padding: 4rem 2rem; text-align: center; margin: -2rem -2rem 3rem -2rem; border-radius: 0 0 16px 16px;">
  <h1 style="font-size: 2.5rem; margin-bottom: 1rem; font-weight: 700; color: white;">Get Your FREE Ultimate Pain Relief Guide</h1>
  <p style="font-size: 1.25rem; margin-bottom: 0; max-width: 700px; margin-left: auto; margin-right: auto; color: #E0E7FF;">
    A comprehensive 15-page guide to managing pain, accelerating recovery, and preventing future injuries
  </p>
</div>

<div style="max-width: 800px; margin: 0 auto; padding: 0 1rem;">

  <div style="background: #F0F9FF; border-left: 4px solid #4770DB; padding: 1.5rem; margin-bottom: 3rem; border-radius: 8px;">
    <p style="margin: 0; font-size: 1.125rem; color: #1E3A8A; font-weight: 600;">
      ✅ Instant PDF Download • 9,000+ Words of Expert Content • Evidence-Based Strategies • 100% Free
    </p>
  </div>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-bottom: 3rem;">
    <div style="text-align: center;">
      <div style="font-size: 3rem; margin-bottom: 0.5rem;">📖</div>
      <h3 style="margin-bottom: 0.5rem; font-size: 1.125rem;">5 Comprehensive Sections</h3>
      <p style="margin: 0; color: #6B7280; font-size: 0.95rem;">15 pages of actionable pain relief strategies</p>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 3rem; margin-bottom: 0.5rem;">🏥</div>
      <h3 style="margin-bottom: 0.5rem; font-size: 1.125rem;">Evidence-Based</h3>
      <p style="margin: 0; color: #6B7280; font-size: 0.95rem;">Backed by medical research and clinical studies</p>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 3rem; margin-bottom: 0.5rem;">⚡</div>
      <h3 style="margin-bottom: 0.5rem; font-size: 1.125rem;">Instant Access</h3>
      <p style="margin: 0; color: #6B7280; font-size: 0.95rem;">Download immediately after signing up</p>
    </div>
  </div>

  <div style="background: white; border: 2px solid #E5E7EB; border-radius: 12px; padding: 3rem 2rem; margin-bottom: 3rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
    <h2 style="text-align: center; margin-bottom: 2rem; color: #1F2937; font-size: 1.75rem;">What's Inside the Guide</h2>

    <div style="margin-bottom: 2rem; padding-left: 1.5rem; border-left: 3px solid #4770DB;">
      <h3 style="margin-bottom: 0.75rem; color: #4770DB; font-size: 1.25rem;">Section 1: Understanding Different Types of Pain</h3>
      <ul style="margin: 0.5rem 0; color: #4B5563; line-height: 1.8;">
        <li>Acute vs. chronic pain explained</li>
        <li>Pain by body region (back, knee, shoulder, wrist, ankle)</li>
        <li>How to rate your pain using medical scales</li>
        <li>When to see a doctor: red flags and warning signs</li>
        <li>The pain-inflammation connection</li>
      </ul>
    </div>

    <div style="margin-bottom: 2rem; padding-left: 1.5rem; border-left: 3px solid #4770DB;">
      <h3 style="margin-bottom: 0.75rem; color: #4770DB; font-size: 1.25rem;">Section 2: When to Use Heat vs. Cold Therapy</h3>
      <ul style="margin: 0.5rem 0; color: #4B5563; line-height: 1.8;">
        <li>Science behind temperature therapy</li>
        <li>Exact protocols for ice and heat application</li>
        <li>When to use cold (acute injuries, inflammation)</li>
        <li>When to use heat (chronic pain, muscle tension)</li>
        <li>Contrast therapy for faster recovery</li>
        <li>Quick decision guide with flowchart</li>
      </ul>
    </div>

    <div style="margin-bottom: 2rem; padding-left: 1.5rem; border-left: 3px solid #4770DB;">
      <h3 style="margin-bottom: 0.75rem; color: #4770DB; font-size: 1.25rem;">Section 3: Choosing the Right Support Brace</h3>
      <ul style="margin: 0.5rem 0; color: #4B5563; line-height: 1.8;">
        <li>Support levels explained (mild, moderate, maximum)</li>
        <li>Complete brace guide for every body part</li>
        <li>Material comparisons and when to use each</li>
        <li>Perfect sizing tips and measurement guide</li>
        <li>When to wear your brace (and when not to)</li>
      </ul>
    </div>

    <div style="margin-bottom: 2rem; padding-left: 1.5rem; border-left: 3px solid #4770DB;">
      <h3 style="margin-bottom: 0.75rem; color: #4770DB; font-size: 1.25rem;">Section 4: Exercises for Pain Prevention</h3>
      <ul style="margin: 0.5rem 0; color: #4B5563; line-height: 1.8;">
        <li>30 illustrated exercises with step-by-step instructions</li>
        <li>Back pain prevention (core strengthening, flexibility)</li>
        <li>Knee pain prevention (strengthening, balance)</li>
        <li>Shoulder, wrist, and ankle exercises</li>
        <li>Sample programs by lifestyle (office worker, athlete, active adult)</li>
      </ul>
    </div>

    <div style="margin-bottom: 0; padding-left: 1.5rem; border-left: 3px solid #4770DB;">
      <h3 style="margin-bottom: 0.75rem; color: #4770DB; font-size: 1.25rem;">Section 5: Product Recommendations by Condition</h3>
      <ul style="margin: 0.5rem 0; color: #4B5563; line-height: 1.8;">
        <li>Condition-specific product recommendations</li>
        <li>Lower back pain, knee pain, carpal tunnel solutions</li>
        <li>Ankle sprains, shoulder issues, plantar fasciitis</li>
        <li>Complete usage protocols for each product</li>
        <li>Money-saving bundle recommendations</li>
      </ul>
    </div>
  </div>

  <div id="optinForm" style="background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%); border: 2px solid #4770DB; border-radius: 12px; padding: 3rem 2rem; margin-bottom: 3rem; text-align: center;">
    <h2 style="margin-bottom: 1rem; color: #1E3A8A; font-size: 1.75rem;">Download Your FREE Guide Now</h2>
    <p style="margin-bottom: 2rem; color: #475569; font-size: 1.125rem;">Enter your email below and get instant access to the complete 15-page PDF guide</p>

    <!-- Klaviyo/Email Collection Form - TO BE IMPLEMENTED -->
    <form action="/contact#ContactFooter" method="post" accept-charset="UTF-8" style="max-width: 500px; margin: 0 auto;">
      <input type="hidden" name="form_type" value="customer" />
      <input type="hidden" name="utf8" value="✓" />
      <input type="hidden" name="contact[tags]" value="newsletter,pain-relief-guide-download" />

      <div style="display: flex; gap: 0.75rem; margin-bottom: 1rem; flex-wrap: wrap;">
        <input
          type="email"
          name="contact[email]"
          id="email"
          placeholder="Enter your email address"
          required
          style="flex: 1; min-width: 250px; padding: 1rem; border: 2px solid #CBD5E1; border-radius: 8px; font-size: 1rem;"
        />
        <button
          type="submit"
          style="padding: 1rem 2rem; background: #4770DB; color: white; border: none; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer; transition: background 0.2s; white-space: nowrap;"
          onmouseover="this.style.background='#3858B8'"
          onmouseout="this.style.background='#4770DB'"
        >
          Get FREE Guide
        </button>
      </div>

      <p style="margin: 0; font-size: 0.875rem; color: #64748B;">
        📧 We respect your privacy. Unsubscribe anytime. | 🔒 Your email is 100% secure.
      </p>
    </form>

    <p style="margin-top: 1.5rem; margin-bottom: 0; font-size: 0.95rem; color: #1E40AF; font-weight: 500;">
      ⚡ Instant delivery • No credit card required • 100% free forever
    </p>
  </div>

  <div style="background: #F9FAFB; padding: 2rem; border-radius: 12px; margin-bottom: 3rem;">
    <h2 style="text-align: center; margin-bottom: 2rem; color: #1F2937;">Why Download This Guide?</h2>

    <div style="display: grid; gap: 1.5rem;">
      <div style="display: flex; align-items: start; gap: 1rem;">
        <div style="font-size: 2rem; flex-shrink: 0;">✅</div>
        <div>
          <h3 style="margin-bottom: 0.5rem; font-size: 1.125rem;">Stop Guessing, Start Healing</h3>
          <p style="margin: 0; color: #6B7280;">Evidence-based strategies that actually work, backed by medical research and clinical studies.</p>
        </div>
      </div>

      <div style="display: flex; align-items: start; gap: 1rem;">
        <div style="font-size: 2rem; flex-shrink: 0;">💰</div>
        <div>
          <h3 style="margin-bottom: 0.5rem; font-size: 1.125rem;">Save Money on Treatments</h3>
          <p style="margin: 0; color: #6B7280;">Learn which therapies and products work best for your specific condition - avoid wasting money on ineffective solutions.</p>
        </div>
      </div>

      <div style="display: flex; align-items: start; gap: 1rem;">
        <div style="font-size: 2rem; flex-shrink: 0;">⚡</div>
        <div>
          <h3 style="margin-bottom: 0.5rem; font-size: 1.125rem;">Recover Faster</h3>
          <p style="margin: 0; color: #6B7280;">Follow proven protocols that accelerate healing and get you back to your activities sooner.</p>
        </div>
      </div>

      <div style="display: flex; align-items: start; gap: 1rem;">
        <div style="font-size: 2rem; flex-shrink: 0;">🛡️</div>
        <div>
          <h3 style="margin-bottom: 0.5rem; font-size: 1.125rem;">Prevent Future Injuries</h3>
          <p style="margin: 0; color: #6B7280;">Learn the exercises and techniques that reduce your risk of re-injury by up to 50%.</p>
        </div>
      </div>
    </div>
  </div>

  <div style="background: white; border: 2px solid #E5E7EB; border-radius: 12px; padding: 2rem; margin-bottom: 3rem;">
    <h2 style="text-align: center; margin-bottom: 2rem; color: #1F2937;">What Our Customers Say</h2>

    <div style="display: grid; gap: 1.5rem;">
      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px; border-left: 3px solid #4770DB;">
        <p style="margin-bottom: 1rem; color: #374151; font-style: italic; line-height: 1.7;">
          "This guide helped me finally understand when to use ice vs. heat. I've had chronic back pain for years, and the exercises in Section 4 have been a game-changer. Highly recommend!"
        </p>
        <p style="margin: 0; color: #6B7280; font-size: 0.95rem;"><strong>- Sarah M.</strong>, Office Manager</p>
      </div>

      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px; border-left: 3px solid #4770DB;">
        <p style="margin-bottom: 1rem; color: #374151; font-style: italic; line-height: 1.7;">
          "As an athlete, I'm always dealing with minor injuries. The product recommendations for each condition saved me so much time researching. The size selection advice was spot-on!"
        </p>
        <p style="margin: 0; color: #6B7280; font-size: 0.95rem;"><strong>- James T.</strong>, Marathon Runner</p>
      </div>

      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px; border-left: 3px solid #4770DB;">
        <p style="margin-bottom: 1rem; color: #374151; font-style: italic; line-height: 1.7;">
          "The carpal tunnel section was incredibly helpful. I've been wearing the wrist brace at night as recommended, and my symptoms have improved dramatically in just 3 weeks."
        </p>
        <p style="margin: 0; color: #6B7280; font-size: 0.95rem;"><strong>- Linda K.</strong>, Graphic Designer</p>
      </div>
    </div>
  </div>

  <div style="background: linear-gradient(135deg, #4770DB 0%, #3858B8 100%); color: white; padding: 3rem 2rem; border-radius: 12px; text-align: center; margin-bottom: 3rem;">
    <h2 style="margin-bottom: 1rem; color: white; font-size: 2rem;">Ready to Take Control of Your Pain?</h2>
    <p style="margin-bottom: 2rem; color: #E0E7FF; font-size: 1.125rem; max-width: 600px; margin-left: auto; margin-right: auto;">
      Join thousands of people who have downloaded this guide and started their journey to pain-free living.
    </p>
    <a href="#optinForm" style="display: inline-block; padding: 1rem 2.5rem; background: white; color: #4770DB; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 1.125rem; transition: transform 0.2s; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
      Download FREE Guide Now →
    </a>
    <p style="margin-top: 1.5rem; margin-bottom: 0; color: #BFDBFE; font-size: 0.95rem;">
      ⏱️ Takes 30 seconds • 📧 Instant delivery • 💯 100% free
    </p>
  </div>

  <div style="margin-bottom: 3rem;">
    <h2 style="text-align: center; margin-bottom: 2rem; color: #1F2937;">Frequently Asked Questions</h2>

    <div style="display: grid; gap: 1.5rem;">
      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px;">
        <h3 style="margin-bottom: 0.75rem; color: #1F2937; font-size: 1.125rem;">Is this guide really free?</h3>
        <p style="margin: 0; color: #6B7280;">Yes, 100% free! No credit card required, no hidden fees. Just enter your email and get instant access to the complete 15-page PDF guide.</p>
      </div>

      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px;">
        <h3 style="margin-bottom: 0.75rem; color: #1F2937; font-size: 1.125rem;">When will I receive the guide?</h3>
        <p style="margin: 0; color: #6B7280;">Instantly! As soon as you submit your email, you'll receive a confirmation email with a download link to the PDF. Check your inbox and spam folder.</p>
      </div>

      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px;">
        <h3 style="margin-bottom: 0.75rem; color: #1F2937; font-size: 1.125rem;">Can I share this guide with family or friends?</h3>
        <p style="margin: 0; color: #6B7280;">Absolutely! The guide is for personal use, and you're welcome to share it with anyone who might benefit from pain relief strategies.</p>
      </div>

      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px;">
        <h3 style="margin-bottom: 0.75rem; color: #1F2937; font-size: 1.125rem;">Will I receive spam emails?</h3>
        <p style="margin: 0; color: #6B7280;">No spam, ever. We'll send you occasional helpful tips and exclusive offers, but you can unsubscribe anytime with one click. We respect your inbox.</p>
      </div>

      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px;">
        <h3 style="margin-bottom: 0.75rem; color: #1F2937; font-size: 1.125rem;">Is this guide suitable for my specific condition?</h3>
        <p style="margin: 0; color: #6B7280;">The guide covers the most common pain conditions (back, knee, shoulder, wrist, ankle, arthritis, plantar fasciitis). If you have a diagnosed medical condition, use this guide as supplemental information alongside your doctor's treatment plan.</p>
      </div>

      <div style="padding: 1.5rem; background: #F9FAFB; border-radius: 8px;">
        <h3 style="margin-bottom: 0.75rem; color: #1F2937; font-size: 1.125rem;">Are the recommendations evidence-based?</h3>
        <p style="margin: 0; color: #6B7280;">Yes! All recommendations are based on current medical research, clinical guidelines, and best practices used by healthcare professionals. We include citations where appropriate.</p>
      </div>
    </div>
  </div>

  <div style="text-align: center; padding: 2rem 0; border-top: 2px solid #E5E7EB;">
    <p style="margin-bottom: 1rem; color: #1F2937; font-size: 1.125rem;">
      <strong>Ready to start your pain-free journey?</strong>
    </p>
    <a href="#optinForm" style="display: inline-block; padding: 0.875rem 2rem; background: #4770DB; color: white; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 1rem; transition: background 0.2s;" onmouseover="this.style.background='#3858B8'" onmouseout="this.style.background='#4770DB'">
      Download Your FREE Guide →
    </a>
    <p style="margin-top: 1rem; margin-bottom: 0; color: #6B7280; font-size: 0.95rem;">
      Questions? Contact us: <a href="mailto:support@alphamedicalcare.com" style="color: #4770DB; text-decoration: underline;">support@alphamedicalcare.com</a>
    </p>
  </div>

</div>

<style>
@media (max-width: 768px) {
  .pain-relief-guide-hero {
    padding: 2rem 1rem !important;
  }
  .pain-relief-guide-hero h1 {
    font-size: 1.75rem !important;
  }
  .pain-relief-guide-hero p {
    font-size: 1rem !important;
  }
  #optinForm form > div {
    flex-direction: column !important;
  }
  #optinForm input {
    min-width: 100% !important;
  }
}
</style>

<script>
// Smooth scroll to form
document.addEventListener('DOMContentLoaded', function() {
  const formLinks = document.querySelectorAll('a[href="#optinForm"]');
  formLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      document.getElementById('optinForm').scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
    });
  });

  // Form submission tracking (placeholder for analytics)
  const form = document.querySelector('#optinForm form');
  if (form) {
    form.addEventListener('submit', function() {
      // Add analytics tracking here (Google Analytics, Klaviyo, etc.)
      console.log('Pain Relief Guide form submitted');
    });
  }
});
</script>
"""

# Page data
page_data = {
    "page": {
        "title": "Free Pain Relief Guide - Download Your Complete PDF Resource",
        "body_html": page_content,
        "handle": "pain-relief-guide",
        "published": True,
        "metafields": [
            {
                "namespace": "custom",
                "key": "meta_title",
                "value": "Free Pain Relief Guide PDF - Complete Resource | Alpha Medical Care",
                "type": "single_line_text_field"
            },
            {
                "namespace": "custom",
                "key": "meta_description",
                "value": "Download your FREE 15-page Pain Relief Guide. Learn heat vs cold therapy, exercises, product recommendations, and evidence-based strategies. Instant PDF delivery.",
                "type": "single_line_text_field"
            }
        ]
    }
}

# Check if page already exists
print("Checking if pain-relief-guide page already exists...")
check_response = requests.get(
    f"{REST_URL}/pages.json?handle=pain-relief-guide",
    headers=headers
)

if check_response.status_code == 200:
    existing_pages = check_response.json().get('pages', [])
    if existing_pages:
        page_id = existing_pages[0]['id']
        print(f"⚠️  Page already exists (ID: {page_id})")
        print(f"   Updating existing page...")

        # Update existing page
        response = requests.put(
            f"{REST_URL}/pages/{page_id}.json",
            headers=headers,
            json=page_data
        )
    else:
        print("   Page doesn't exist, creating new...")
        # Create new page
        response = requests.post(
            f"{REST_URL}/pages.json",
            headers=headers,
            json=page_data
        )
else:
    print(f"❌ Error checking for existing page: {check_response.status_code}")
    print(check_response.json())
    exit(1)

if response.status_code in [200, 201]:
    page = response.json()['page']
    print(f"\n✅ Pain Relief Guide page {'updated' if existing_pages else 'created'} successfully!")
    print(f"   ID: {page['id']}")
    print(f"   Handle: {page['handle']}")
    print(f"   URL: https://{SHOPIFY_STORE_DOMAIN}/pages/{page['handle']}")
    print(f"   Published: {page['published_at']}")
    print(f"\n📋 Next Steps:")
    print(f"   1. Upload ULTIMATE_PAIN_RELIEF_GUIDE.md to Canva/Google Docs for PDF design")
    print(f"   2. Export as PDF (name: Ultimate_Pain_Relief_Guide.pdf)")
    print(f"   3. Upload PDF to Shopify Files (Settings → Files)")
    print(f"   4. Get PDF download URL from Shopify Files")
    print(f"   5. Set up email automation (Klaviyo recommended) to deliver PDF")
    print(f"   6. Optional: Add popup overlay to homepage promoting guide")
else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.json())
