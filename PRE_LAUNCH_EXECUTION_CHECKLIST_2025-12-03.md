# PRE-LAUNCH EXECUTION CHECKLIST - ALPHA MEDICAL
**Date:** 2025-12-03
**Launch Date:** 2025-12-25 (22 jours restants)
**Objectif:** 98/100 → 100/100 holistique

---

## ⚡ SPRINT 1: COMPLIANCE URGENT (JOUR 1 - 3h)

### ☐ TÂCHE #2: Créer Accessibility Statement (15 min)
**Méthode:**
1. Shopify Admin → Online Store → Pages → Add page
2. Title: "Accessibility Statement"
3. URL handle: /pages/accessibility
4. Content (copier template):
```
# Accessibility Statement

Alpha Medical Care is committed to ensuring digital accessibility for people with disabilities. We are continually improving the user experience for everyone and applying the relevant accessibility standards.

## Conformance Status
We are committed to WCAG 2.1 Level AA conformance.

## Features
- Keyboard navigation support
- Screen reader compatibility
- Alt text for all images
- Clear heading structure
- Sufficient color contrast

## Feedback
If you experience any difficulty accessing our site, please contact us:
- Email: accessibility@alphamedical.shop
- Phone: 1-888-XXX-XXXX (TBD)

Last updated: December 2025
```
5. Save and publish
6. **Vérification:** Visit /pages/accessibility → Page displays correctly

---

### ☐ TÂCHE #1: Ajouter Footer Policy Links (10 min)
**Méthode:**
1. Shopify Admin → Online Store → Navigation → Footer menu
2. Add menu items (in order):
   - Privacy Policy → /policies/privacy-policy
   - Terms of Service → /policies/terms-of-service
   - Refund Policy → /policies/refund-policy
   - Shipping Policy → /pages/shipping-delivery
   - Accessibility → /pages/accessibility
3. Save changes
4. **Vérification:** Browser → Footer shows 5 policy links clickable

---

### ☐ TÂCHE #6: Terms Age Restriction (30 min)
**Méthode:**
1. Shopify Admin → Settings → Legal → Terms of Service
2. Add new section after "Acceptance of Terms":
```
## Eligibility

You must be at least 18 years of age to use this website and purchase products. By using this site, you represent and warrant that you are at least 18 years old. If you are under 18, you may only use this site with the involvement of a parent or guardian.
```
3. Save changes
4. **Vérification:** /policies/terms-of-service contains "18 years"

---

### ☐ TÂCHE #3: Cookie Consent Banner (1h CookieYes OU 4h Native)
**Décision Requise:** CookieYes (recommandé PRE-LAUNCH) vs Native Shopify

**Option A: CookieYes (1h) - RECOMMANDÉ**
1. Sign up: cookieyes.com (free tier)
2. Add domain: alphamedical.shop
3. Configure categories:
   - Necessary: Shopify session, cart
   - Analytics: GA4, GTM
   - Advertisement: Meta Pixel, TikTok, Google Ads
4. Copy script snippet
5. Shopify Admin → Online Store → Themes → Edit code
6. Open: layout/theme.liquid
7. Paste before `</head>`:
```liquid
<!-- CookieYes Banner -->
<script id="cookieyes" type="text/javascript" src="https://cdn-cookieyes.com/client_data/YOUR_ID/script.js"></script>
```
8. Save
9. **Vérification:** Browser → Banner appears, Accept/Reject buttons work

**Option B: Native (4h)**
1. Create: sections/cookie-banner.liquid
2. Add schema + Liquid logic
3. Integrate with GTM Consent Mode v2
4. Test accept/reject functionality
(Not detailing here - use Option A for speed)

---

## 📋 SPRINT 2: POLICY COMPLETION (JOUR 2 - 3h)

### ☐ TÂCHE #4: Privacy Policy CCPA Section (2h)
**Méthode:**
1. Shopify Admin → Settings → Legal → Privacy Policy
2. Add new section before "Contact Information":
```
## California Consumer Privacy Act (CCPA) Rights

If you are a California resident, you have the following rights under the California Consumer Privacy Act:

### Right to Know
You have the right to request what personal information we have collected about you in the past 12 months, including:
- Categories of personal information collected
- Sources of personal information
- Business purpose for collecting information
- Categories of third parties we share information with

### Right to Delete
You have the right to request deletion of your personal information, subject to certain exceptions.

### Right to Opt-Out of Sale
We do not sell your personal information. However, you have the right to opt-out of any future sale of your information.

### Non-Discrimination
We will not discriminate against you for exercising your CCPA rights.

### How to Exercise Your Rights
To exercise your CCPA rights, please contact us at:
- Email: privacy@alphamedical.shop
- Response time: Within 45 days of request

### Verification
We may require verification of your identity before processing your request to protect your personal information.
```
3. Save changes
4. **Vérification:** /policies/privacy-policy contains "CCPA" section

---

### ☐ TÂCHE #5: Data Retention + Cookie Types (1h)
**Méthode:**
1. Same Privacy Policy page
2. Add section "Data Retention":
```
## How Long We Keep Your Information

We retain your personal information for as long as necessary to:
- Fulfill the purposes outlined in this policy
- Comply with legal obligations
- Resolve disputes and enforce agreements

Specific retention periods:
- Order data: 3 years after purchase (accounting requirements)
- Marketing data: Until you opt-out or unsubscribe
- Analytics data: 14-26 months (Google Analytics default)
- Account data: Until account deletion requested

After the retention period, we securely delete or anonymize your information.
```

3. Add section "Cookie Types":
```
## Types of Cookies We Use

### Necessary Cookies (Required)
These cookies are essential for the website to function:
- Shopify session cookies: Maintain your cart and login
- Security cookies: Prevent fraud and abuse
Duration: Session or up to 30 days

### Analytics Cookies (Optional)
These help us understand how visitors use our site:
- Google Analytics (GA4): Traffic analysis and conversion tracking
- Google Tag Manager: Manage tracking tags
Duration: 14-26 months

### Marketing Cookies (Optional)
These enable personalized advertising:
- Meta Pixel: Facebook/Instagram ad targeting
- TikTok Pixel: TikTok ad targeting
- Google Ads: Google advertising
Duration: Up to 24 months

You can control cookie preferences through our cookie consent banner.
```

4. Save changes
5. **Vérification:** Sections present in privacy policy

---

## 🤖 SPRINT 3: AUTOMATION + TRACKING (JOUR 3-4 - 5h)

### ☐ TÂCHE #9: Contact Form Shopify Flow (30 min)
**Méthode:**
1. Shopify Admin → Apps → Flow → Create workflow
2. Name: "Contact Form Auto-Response"
3. Trigger: "Contact form submitted"
4. Action 1: "Add customer tag"
   - Tag: contact_form_inquiry
5. Action 2: "Send email"
   - To: support@alphamedical.shop
   - Subject: New contact form submission
   - Body: Customer details + message
6. Save and activate
7. **Vérification:** Submit test form → Tag applied + email received

---

### ☐ TÂCHE #10: Newsletter Signup Flow (30 min)
**Méthode:**
1. Shopify Flow → Create workflow
2. Name: "Newsletter Signup Welcome"
3. Trigger: "Customer tags changed"
4. Condition: "Tag contains newsletter_subscriber"
5. Action 1: "Send email" (Shopify Email automation)
   - Template: Welcome new subscribers (already exists)
6. Action 2 (Optional): "Add to Klaviyo list"
   - Requires Klaviyo integration check
7. Save and activate
8. **Vérification:** Test signup → Welcome email received

---

### ☐ TÂCHE #14: Remove Previous Tier Tags (10 min)
**Méthode:**
1. Shopify Flow → Open "Loyalty Tier Tagging"
2. Before "Add customer tag" action:
3. Add action: "Remove customer tag"
   - If: Customer has tag "bronze" → Remove tag "bronze"
   - If: Customer has tag "silver" → Remove tag "silver"
   - If: Customer has tag "gold" → Remove tag "gold"
4. Then: Existing "Add customer tag" action
5. Save
6. **Vérification:** Test customer upgrade → Old tag removed

---

### ☐ TÂCHE #7: Enhanced Ecommerce Testing (2h)
**Méthode:**
1. Enable test mode: Shopify Admin → Settings → Payments → Test mode
2. Browser → Open product page
3. DevTools → Network tab → Filter: "collect" (GA4 requests)
4. Add product to cart
   - **Verify:** add_to_cart event fired with product_id, value
5. Click "Checkout"
   - **Verify:** begin_checkout event fired with cart value
6. Complete test purchase (use Shopify test card 4242 4242 4242 4242)
   - **Verify:** purchase event fired with transaction_id, revenue
7. GA4 Real-Time report → Events
   - **Verify:** All 5 events visible:
     * view_item
     * add_to_cart
     * begin_checkout
     * purchase
     * (5th enhanced ecommerce event)
8. Document results: Screenshot GA4 Real-Time
9. Disable test mode
10. **Vérification:** All events tracked correctly

---

### ☐ TÂCHE #17: Data Layer Validation (1h) - JOUR 4
**Méthode:**
1. Browser → Homepage
2. DevTools → Console → Type: `dataLayer`
3. **Verify:** Array exists with GTM events
4. Navigate: Product page
5. **Verify:** ecommerce object present with:
   - currency_code: "USD"
   - value: [product_price]
   - items: [{product details}]
6. Add to cart
7. **Verify:** add_to_cart event structure correct
8. Test all pages: Homepage, Collection, Product, Cart, Checkout
9. Document: Screenshot each dataLayer object
10. **Vérification:** All dataLayer events valid JSON structure

---

### ☐ TÂCHE #8: Klaviyo A/B Test Config (1h) - JOUR 4
**Méthode:**
1. Klaviyo → Flows → "Welcome Series - Final Email Discount"
2. Click Email #1
3. Click "Create A/B Test"
4. Configure:
   - Variant A (Control): Current subject line
   - Variant B: "Your [Pain Point] Solution Awaits - 10% Off Inside"
   - Metric: Open rate
   - Split: 50/50
   - Duration: 30 days (activate post-launch)
5. Save (don't activate yet - need traffic)
6. **Vérification:** Flow shows "A/B Test Configured"
7. **Note:** Activate after 500+ subscribers (post-launch)

---

## 🎨 SPRINT 4: CONTENT AUTOMATION (JOUR 5 - 2h)

### ☐ TÂCHE #12: N8N Blog Workflow Setup (2h)
**Prérequis:** N8N instance https://n8n.srv1168256.hstgr.cloud

**ÉTAPE 1: Import JSON (5 min)**
1. N8N UI → Workflows → Import from File
2. Select: n8n-blog-automation-template.json (Session 74)
3. Workflow imported: 22 nodes visible

**ÉTAPE 2: Configure Credentials (10 min)**
1. Nodes requiring credentials (3):
   - Google Gemini API
   - Shopify Admin API
   - Google Sheets OAuth2

2. Google Gemini:
   - Credential: GoogleGeminiApi
   - API Key: AIzaSyCqHDFQnaBL4hGiVWWMkqEOeFpkj7FkKJ4
   - Status: ✅ READY (exists from Workflow #1)

3. Shopify Admin API:
   - Credential: ShopifyApi
   - Shop: azffej-as.myshopify.com
   - Access Token: [from .env.admin shpat_xxx]
   - API Version: 2024-10

4. Google Sheets:
   - Credential: GoogleSheetsOAuth2
   - Status: ✅ READY (exists from Workflow #1)

**ÉTAPE 3: Create Google Sheets (15 min)**
1. Google Sheets → Create: "Alpha Medical - Blog Automation Tracking"
2. Onglet 1: "raw_data"
   - Headers: product_id | title | description | handle | Images
3. Onglet 2: "refined_input"
   - Headers: product_id | blog_id | blog_status | title | description | handle | Image_1 | Image_2 | Image_3 | Image_4
   - Add column: blog_status (values: unused, used, posted)
4. Onglet 3: "blog_post"
   - Headers: product_id | blog_title | content | excerpt | page_title | meta_description | URL_handle | blog_status | article_id
5. Share sheet with: Service account email (from Google credentials)
6. Copy Sheet ID from URL: https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit

**ÉTAPE 4: Find Blog ID (5 min)**
1. Shopify Admin → Online Store → Blog Posts
2. Click existing blog (or create if none)
3. URL format: /admin/blogs/[BLOG_ID]
4. Copy BLOG_ID

**ÉTAPE 5: Customize Prompt (45 min)**
1. N8N → Node "Magic Room (AI Agent)"
2. Replace prompt:
```
You are a medical equipment content specialist writing educational blog articles for Alpha Medical Care.

CONTEXT:
- Brand: Alpha Medical Care (B2C retailer)
- Products: Medical equipment (knee braces, posture correctors, therapy devices)
- Audience: US consumers with pain relief needs (seniors, office workers, athletes)
- Tone: Educational, empathetic, wellness-focused (NOT sales-heavy)

PRODUCT DETAILS:
- Title: {{$json.title}}
- Description: {{$json.description}}
- Category: {{$json.product_type}}

ARTICLE REQUIREMENTS:
1. Length: 2000-2500 words
2. Structure:
   - Introduction (150 words): Problem statement + empathy
   - Section 1: Understanding [Condition/Pain Point] (400 words)
   - Section 2: How [Product Category] Helps (500 words)
   - Section 3: Choosing the Right [Product] (400 words)
   - Section 4: Best Practices & Usage Tips (300 words)
   - Section 5: FAQs (200 words, 3-5 Q&As)
   - Conclusion (100 words): Call-to-action (NOT pushy)
3. SEO: Primary keyword = [pain relief + product type]
4. Internal links: 2-3 references to related product categories
5. Author attribution: Dr. Sarah Mitchell, Medical Content Specialist
6. Medical disclaimer: Add at bottom

COMPLIANCE:
- AVOID: Medical claims, diagnosis language, treatment promises
- USE: Educational information, general wellness guidance
- Disclaimer: "This content is for educational purposes only..."

OUTPUT FORMAT:
- blog_title: SEO-optimized (60 chars max)
- content: Full article HTML (p, h2, h3, ul, li tags)
- excerpt: Meta description (150 chars)
- page_title: [Product Category] Guide | Alpha Medical Care
- meta_description: SEO meta (155 chars)
- URL_handle: seo-friendly-slug
```

3. Node "Output Parser":
   - Verify JSON structure: blog_title, content, excerpt, page_title, meta_description, URL_handle

4. Node "Workflow Configuration":
   - Update: google_sheet_id = [SHEET_ID from ÉTAPE 3]
   - Update: dest_folder_id = (not applicable for blog)

**ÉTAPE 6: Test First Article (30 min)**
1. N8N → Manual trigger
2. Select test product (e.g., "Knee Brace")
3. Execute workflow
4. Monitor execution:
   - Node "Get All Product Details": SUCCESS (products fetched)
   - Node "Magic Room": SUCCESS (article generated)
   - Node "Blog Creation": SUCCESS (POST to Shopify)
5. Shopify Admin → Blog Posts
   - **Verify:** New article created
   - Check: Title, content, meta description
6. Review article quality:
   - Length: 2000-2500 words ✓
   - Medical disclaimer present ✓
   - Internal links present ✓
   - Tone: Educational ✓
7. If quality OK: Activate workflow
8. **Vérification:** N8N execution log SUCCESS + blog post published

---

## 🎨 SPRINT 5: UX OPTIMIZATION (JOUR 6-7 - 3.5h)

### ☐ TÂCHE #15: Footer Redesign (2h 25min) - JOUR 6
**Structure fournie par l'utilisateur:**

**COLUMN 1: SHOP**
```
Shop All → /collections/all
Bestsellers → /collections/bestsellers
New Arrivals → /collections/new-arrivals
```

**COLUMN 2: CUSTOMER SERVICE**
```
About Us → /pages/about-us
Shipping & Delivery → /pages/shipping-delivery
Returns & Exchanges → /pages/returns-exchanges
Product Warranty → /pages/product-warranty
FAQ → /pages/faq
```

**COLUMN 3: COMPANY**
```
About Us → /pages/about-us
Our Quality Promise → /pages/quality-promise
Healthcare Professionals → /pages/healthcare-professionals
```

**COLUMN 4: LEGAL**
```
Privacy Policy → /policies/privacy-policy
Terms of Service → /policies/terms-of-service
Refund Policy → /policies/refund-policy
Shipping Policy → /pages/shipping-delivery
Accessibility → /pages/accessibility
```

**COLUMN 5: CONNECT**
```
Contact Us → /pages/contact
Facebook → [URL]
Instagram → [URL]
TikTok → [URL]
```

**Méthode:**
1. Shopify Admin → Online Store → Themes → Customize
2. Footer section → Edit
3. Change to 5 columns layout
4. Configure each column with links above
5. Bottom row:
   - Payment icons: Visa, Mastercard, Amex, Apple Pay, Google Pay, Shop Pay
   - Contact: contact@alphamedical.shop
   - Social icons
6. Save and preview
7. **Vérification:** Footer displays 5 columns, all links work

---

### ☐ TÂCHE #16: Header Navigation (15 min) - JOUR 7
**Méthode:**
1. Shopify Admin → Online Store → Navigation → Main menu
2. Add menu items (after "Products"):
   - Bundle Creator → /pages/bundle-builder
   - Bestsellers → /collections/bestsellers
3. Add mega menu "Shop by Need":
   - Knee Support → /collections/knee-support
   - Back Pain → /collections/back-pain
   - Posture → /collections/posture
   - Mobility → /collections/mobility
4. Save changes
5. **Vérification:** Header shows new links

---

### ☐ TÂCHE #11: Klaviyo Segmentation (1h) - JOUR 7
**Méthode:**
1. Klaviyo → Lists & Segments → Create Segment
2. Segment 1: "VIP Customers"
   - Conditions:
     * Customer has tag "VIP" (from Shopify Flow)
     * OR Placed order at least 3 times
   - Save
3. Segment 2: "At-Risk Loyal"
   - Conditions:
     * Customer has tag "loyal"
     * AND Last placed order before 90 days ago
   - Save
4. Segment 3: "New Customers"
   - Conditions:
     * Customer has tag "new"
     * AND Placed order exactly 1 time
   - Save
5. Segment 4: "High AOV"
   - Conditions:
     * Average order value greater than $80
   - Save
6. **Vérification:** All 4 segments created
7. **Note:** Segments will populate post-launch with orders

---

## 🎯 SPRINT 6: N8N YOUTUBE DECISION (JOUR 8)

### ☐ TÂCHE #13: YouTube Workflow Deployment Decision
**Status:** ⏳ AWAITING USER DECISIONS

**Questions à résoudre:**

1. **Budget approval:**
   - Option A: Long-form videos (~$50/video)
   - Option B: Short-form videos (~$0.45/short)
   - Question: Quel budget mensuel? $50-200/month?

2. **Content mix:**
   - Option A: 100% long-form (1-2/month)
   - Option B: 100% shorts (10-20/month)
   - Option C: Mix (1 long + 5 shorts/month)
   - Question: Quelle stratégie?

3. **Production volume:**
   - Option A: Conservative (1-2 videos/month)
   - Option B: Aggressive (3-4 videos/month)
   - Question: Quel rythme de publication?

4. **Timing:**
   - Option A: Deploy now (Dec 2025)
   - Option B: Defer to Q1 2026 (Jan-Mar)
   - Question: Quand lancer?

5. **Google Cloud authorization:**
   - Vertex AI billing required for Gemini API
   - Question: Autoriser Google Cloud billing?

**Impact si déployé:**
- Content automation: 66% → 100% ✅
- Lead generation: +50-100 leads/month (YouTube)
- Cost: $600-2,400/year (depending on choices)
- ROI: HIGH (organic lead gen = $0 CPL after setup)

**Impact si déféré:**
- Content automation: Remains 66%
- Deploy in Q1 2026 when ready

**Action:** USER DECISION REQUIRED ⏸️

---

## ✅ POST-SPRINT VALIDATION

### JOUR 9-16: BUFFER & TESTING
- Test all workflows end-to-end
- Browser validation (Chrome DevTools)
- Mobile responsiveness check
- Load testing (if needed)
- Documentation updates

### JOUR 17-23: FINAL PREP
- Update llms.txt (auto-generated)
- Review all automations status
- Pre-launch checklist verification
- Backup all data (Shopify backup workflow)

### JOUR 24-25: LAUNCH
- 🎄 Christmas Eve: Final systems check
- 🎉 Dec 25, 2025: **LAUNCH**

---

## 📊 SUCCESS METRICS

**Infrastructure Score Progression:**
```
Before: 96/100 (PRE-LAUNCH excellent)
After Sprint 1-2: 98/100 (compliance complete)
After Sprint 3-4: 100/100 (automation + content)
After Sprint 5: 100/100 (UX optimized)
```

**Content Automation:**
```
Before: 33% (N8N #1 only)
After Sprint 4: 66% (N8N #1 + #3)
After Sprint 6 (if deployed): 100% (all 3 workflows)
```

**Holistic Score:**
```
Before: 98/100 NEAR-PERFECT
After execution: 100/100 🏆 PERFECT
```

---

## 🚨 RISK MANAGEMENT

**Blockers Potentiels:**

1. **Cookie Consent Decision:** Native vs CookieYes
   - Mitigation: Recommandation CookieYes (1h vs 4h)
   - Backup: Native option documented if needed

2. **Enhanced Ecommerce Test Payment:**
   - Mitigation: Use Shopify test mode (card 4242...)
   - Backup: Manual transaction if test mode fails

3. **N8N Blog Workflow Complexity:**
   - Mitigation: Template ready, step-by-step guide
   - Backup: Deploy without prompt customization (use default)

4. **YouTube Workflow User Decisions:**
   - Mitigation: Decision can be deferred to Q1 2026
   - Impact: No blocker for 98→100/100 (YouTube not required)

**Time Overruns:**
- Total planned: 18.5h execution
- Buffer: 10.5 days (Jour 9-16) for overruns
- Contingency: Can skip TÂCHE #15 (footer) if time-constrained

---

**STATUS:** ✅ CHECKLIST COMPLET ET ACTIONABLE
**NEXT:** Exécution Sprint 1 (Jour 1 - 3h)
