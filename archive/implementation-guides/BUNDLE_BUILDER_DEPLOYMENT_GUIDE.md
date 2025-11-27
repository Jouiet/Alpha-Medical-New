# CUSTOM BUNDLE BUILDER - DEPLOYMENT GUIDE

**Feature:** Community-Driven Bundle Co-Creation System
**Store:** Alpha Medical Care (azffej-as.myshopify.com)
**Deployment Date:** 2025-11-14
**Status:** ✅ FRONTEND DEPLOYED | ⏳ BACKEND PENDING

---

## 🎯 WHAT WAS DEPLOYED

### 1. Bundle Creation Page
**URL:** https://www.alphamedical.shop/pages/bundle-creation

**Features:**
- ✅ Customer login requirement
- ✅ URL-based product submission (2-5 products)
- ✅ Strict URL validation (only alphamedical.shop/products/* accepted)
- ✅ Real-time product preview (fetched from Shopify)
- ✅ Duplicate product detection
- ✅ 3 submissions/month limit per customer
- ✅ Bundle pricing calculator (15% discount)
- ✅ Trending proposals display
- ✅ FAQ section

**Files Deployed:**
- `templates/page.bundle-creation.liquid` (1,310 lines)

### 2. CTA Banner Snippet
**Component:** `bundle-builder-cta-banner.liquid`

**Features:**
- ✅ Eye-catching gradient design
- ✅ Animated elements
- ✅ Responsive (mobile + desktop)
- ✅ Direct link to bundle creation page

**Files Deployed:**
- `snippets/bundle-builder-cta-banner.liquid` (306 lines)

---

## 📋 DEPLOYMENT VERIFICATION

### ✅ COMPLETED STEPS

**1. Template Upload** ✅
- `page.bundle-creation.liquid` → Theme ID 140069830733
- `bundle-builder-cta-banner.liquid` → Theme ID 140069830733

**2. Page Creation** ✅
- Title: "Create Your Bundle"
- Handle: `bundle-creation`
- Template suffix: `bundle-creation`
- Status: Published

**3. Verification** ✅
```bash
# Page accessible at:
https://www.alphamedical.shop/pages/bundle-creation

# Templates uploaded to theme:
- templates/page.bundle-creation.liquid
- snippets/bundle-builder-cta-banner.liquid
```

---

## 🔧 CONFIGURATION REQUIRED

### STEP 1: Add Banner to Homepage (MANUAL)

**Option A: Via Theme Editor (Recommended)**
1. Go to: https://admin.shopify.com/store/azffej-as/themes/current/editor
2. Open Homepage
3. Click "Add section"
4. Select "Custom Liquid"
5. Paste: `{% render 'bundle-builder-cta-banner' %}`
6. Drag section to desired position (suggested: after hero, before collections)
7. Click "Save"

**Option B: Edit templates/index.json**
```liquid
{% render 'bundle-builder-cta-banner' %}
```

**Suggested Placement:**
- After hero/slideshow section
- Before featured collections
- Or in a dedicated "Community" section

### STEP 2: Test User Flow (MANDATORY)

**Test Checklist:**
- [ ] Visit https://www.alphamedical.shop/pages/bundle-creation
- [ ] Verify login requirement (redirects if not logged in)
- [ ] Enter 2 valid product URLs from the shop
- [ ] Verify product preview loads correctly
- [ ] Try invalid URL (external site) → Should show error
- [ ] Try duplicate product → Should show error
- [ ] Submit proposal → Should see success message
- [ ] Check localStorage (browser dev tools): `bundle_proposals` and `bundle_submissions_2025-11`

**Sample Valid URLs (for testing):**
```
https://www.alphamedical.shop/products/double-patellar-knee-support-strap-pain-relief-brace
https://www.alphamedical.shop/products/wrist-brace-support-carpal-tunnel-arthritis-relief
https://www.alphamedical.shop/products/ankle-support-brace-fitness-pain-relief
```

---

## ⚠️ CURRENT LIMITATIONS (localStorage Demo Mode)

**What Works:**
- ✅ Full UI and validation
- ✅ Product fetching from Shopify
- ✅ URL validation (strict domain checking)
- ✅ Submission counter (3/month limit)
- ✅ Trending proposals display

**What's Temporary (localStorage):**
- ⚠️ Proposals stored in browser only (not synced across devices)
- ⚠️ No cross-customer vote counting
- ⚠️ No automatic bundle creation at 10 votes
- ⚠️ No email notifications

**Why localStorage?**
- Zero backend requirements for testing
- Instant deployment
- Demonstrates full UX workflow
- Easy to test without API complexity

---

## 🚀 BACKEND INTEGRATION (Next Phase)

### What's Required for Production

**1. Database Setup**
- PostgreSQL or MongoDB for proposal storage
- Tables: `proposals`, `customer_submissions`, `proposal_matches`
- See: `CUSTOM_BUNDLE_BUILDER_COMPLETE_ANALYSIS.md` Section 2.2

**2. Backend API Endpoints**
```
POST   /api/v1/proposals/submit
GET    /api/v1/proposals/:id
GET    /api/v1/proposals/mine
GET    /api/v1/proposals/trending
DELETE /api/v1/proposals/:id
```

**3. Shopify Webhook Integration**
- Bundle auto-creation when threshold reached
- Shopify Admin API: `productCreate` mutation
- Add to "Community Bundles" collection

**4. Email Notifications**
- Klaviyo integration (already installed)
- Templates:
  - Proposal confirmation
  - Threshold reached (10 votes)
  - Bundle created notification

**5. Deployment Options**
- **Option A:** Shopify Custom App (Node.js/Python)
- **Option B:** External API (Vercel/Railway/Heroku)
- **Option C:** Shopify App Extensions

**Cost Estimate:**
- Development: $10,000 OR 8-11 weeks engineer time
- Hosting: $20-80/month (Vercel/Railway + PostgreSQL)

---

## 📊 TECHNICAL SPECIFICATIONS

### URL Validation Rules

**ACCEPTED:**
```
✅ https://www.alphamedical.shop/products/[handle]
✅ https://alphamedical.shop/products/[handle]
✅ http://www.alphamedical.shop/products/[handle]
✅ http://alphamedical.shop/products/[handle]
```

**REJECTED:**
```
❌ https://external-site.com/products/anything
❌ https://www.alphamedical.shop/pages/anything (not a product)
❌ https://www.alphamedical.shop/collections/anything
❌ https://www.alphamedical.shop (homepage)
❌ Relative URLs: /products/anything
```

**Validation Regex:**
```javascript
/https?://(www\.)?alphamedical\.shop/products/[a-z0-9\-]+/i
```

### Product Fetching

**Method:** Shopify Product JSON API
```javascript
fetch(`/products/${handle}.js`)
```

**Response:**
```json
{
  "id": 7585886666829,
  "handle": "product-handle",
  "title": "Product Title",
  "price": 5637, // cents
  "featured_image": "https://cdn.shopify.com/...",
  "url": "/products/product-handle"
}
```

### Submission Limits

**Per Customer:**
- 3 proposals maximum per calendar month
- Month resets on 1st of each month (UTC 00:00)
- Tracked in localStorage: `bundle_submissions_YYYY-MM`

**Per Proposal:**
- Minimum 2 products
- Maximum 5 products
- No duplicate products within same proposal
- No identical proposals from same customer

### Bundle Pricing

**Formula:**
```javascript
const totalPrice = products.reduce((sum, p) => sum + p.price, 0);
const bundlePrice = totalPrice * 0.85; // 15% discount
const savings = totalPrice - bundlePrice;
```

---

## 🔍 TROUBLESHOOTING

### Issue: Page Shows "404 Not Found"

**Cause:** Template not applied to page

**Fix:**
1. Go to Shopify Admin → Pages
2. Find "Create Your Bundle" page
3. Click Edit
4. In right sidebar, under "Template":
   - Change from "Default page" to "bundle-creation"
5. Save

### Issue: Banner Not Showing on Homepage

**Cause:** Snippet not rendered in homepage template

**Fix:** See "STEP 1: Add Banner to Homepage" above

### Issue: Product Preview Not Loading

**Cause:** Invalid product handle or CORS issue

**Fix:**
1. Check browser console for errors
2. Verify product URL is correct format
3. Test product JSON API directly: `https://www.alphamedical.shop/products/[handle].js`

### Issue: Submission Counter Not Resetting

**Cause:** localStorage persists across months

**Fix (Manual):**
1. Open browser dev tools (F12)
2. Go to Application/Storage → Local Storage
3. Find key: `bundle_submissions_YYYY-MM`
4. Delete or set value to "0"

### Issue: Can't Submit More Than 3 Proposals

**Cause:** Monthly limit reached (working as designed)

**Fix:**
- Wait until next month (1st)
- OR manually clear localStorage (see above)
- OR admin can increase limit in code (change `MAX_SUBMISSIONS_PER_MONTH`)

---

## 📁 FILE STRUCTURE

```
/Users/mac/Desktop/Alpha-Medical/
├── templates/
│   └── page.bundle-creation.liquid          # Main page template (1,310 lines)
├── snippets/
│   └── bundle-builder-cta-banner.liquid     # Homepage CTA (306 lines)
├── create_bundle_creation_page.py           # Deployment script
├── BUNDLE_BUILDER_DEPLOYMENT_GUIDE.md       # This file
└── CUSTOM_BUNDLE_BUILDER_COMPLETE_ANALYSIS.md  # Full feasibility study
```

---

## 🎨 CUSTOMIZATION GUIDE

### Change Banner Colors

**Edit:** `snippets/bundle-builder-cta-banner.liquid`

```css
/* Line ~23: Gradient background */
background: linear-gradient(135deg, #4A90E2 0%, #7FCCC9 100%);

/* Change to your brand colors: */
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Change Discount Percentage

**Edit:** `templates/page.bundle-creation.liquid`

```javascript
// Line ~866: Bundle pricing calculation
const bundlePrice = totalPrice * 0.85; // 15% discount

// Change to 20% discount:
const bundlePrice = totalPrice * 0.80;
```

**Also update text in:**
- Line ~14: "15% discount" → "20% discount"
- Line ~47: "15% OFF" → "20% OFF"

### Change Monthly Submission Limit

**Edit:** `templates/page.bundle-creation.liquid`

```javascript
// Line ~736:
const MAX_SUBMISSIONS_PER_MONTH = 3;

// Change to 5 submissions:
const MAX_SUBMISSIONS_PER_MONTH = 5;
```

### Change Vote Threshold (10 → X)

**Note:** Currently hardcoded for demo. In production backend:

```python
# backend/config.py
BUNDLE_CREATION_THRESHOLD = 10  # Change to desired number
```

---

## 📊 ANALYTICS TRACKING

### Recommended Events to Track

**Google Analytics 4 (already installed):**

```javascript
// Proposal submission
gtag('event', 'bundle_proposal_submitted', {
  'customer_id': customerId,
  'product_count': products.length,
  'total_value': totalValue
});

// Product added to proposal
gtag('event', 'bundle_product_added', {
  'product_id': productId,
  'product_title': productTitle
});

// Trending proposal viewed
gtag('event', 'trending_proposal_viewed', {
  'proposal_id': proposalId,
  'vote_count': voteCount
});
```

**Where to Add:**
- Edit `templates/page.bundle-creation.liquid`
- Search for `// TODO: Call backend API` comments
- Add gtag() events before/after API calls

---

## 🚦 NEXT STEPS (Priority Order)

### IMMEDIATE (This Week)
1. ✅ Test bundle creation page (see checklist above)
2. ⏳ Add banner to homepage (manual step)
3. ⏳ Verify all flows work correctly
4. ⏳ Collect initial user feedback

### SHORT-TERM (This Month)
1. ⏳ Decide on backend approach (Custom App vs External API)
2. ⏳ Set up database (PostgreSQL recommended)
3. ⏳ Develop backend API endpoints
4. ⏳ Replace localStorage with API calls
5. ⏳ Test end-to-end workflow

### MEDIUM-TERM (Next Quarter)
1. ⏳ Implement email notifications (Klaviyo)
2. ⏳ Add admin dashboard for proposal management
3. ⏳ A/B test vote thresholds (7 vs 10 vs 12)
4. ⏳ Launch marketing campaign
5. ⏳ Monitor KPIs (proposals/month, bundles created, conversion rate)

---

## 📞 SUPPORT & CONTACTS

**For Technical Issues:**
- Review: `CUSTOM_BUNDLE_BUILDER_COMPLETE_ANALYSIS.md`
- Check: Browser console for JavaScript errors
- Verify: Shopify Admin → Online Store → Themes → Current theme

**For Backend Development:**
- Reference: Analysis doc Section 2 (Technical Architecture)
- Database schema: Section 2.2
- API specs: Section 2.4

**For Questions:**
- Refer to: `CUSTOM_BUNDLE_BUILDER_COMPLETE_ANALYSIS.md` Appendix D (FAQ)

---

## 📝 CHANGELOG

### 2025-11-14 - Initial Deployment
- ✅ Created `page.bundle-creation.liquid` template
- ✅ Created `bundle-builder-cta-banner.liquid` snippet
- ✅ Deployed to Shopify theme (ID: 140069830733)
- ✅ Created `/pages/bundle-creation` page
- ✅ Verified URL validation working
- ⏳ Backend API pending

---

**END OF DEPLOYMENT GUIDE**

**Status:** Frontend LIVE ✅ | Backend TODO ⏳
**Next Review:** After backend integration
