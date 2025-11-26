# KLAVIYO FLOWS DEPLOYMENT GUIDE
## 4 Complementary Flows - Step-by-Step Configuration

**Date:** 2025-11-26
**Prerequisites Status:** ✅ 100% READY
**Estimated Time:** 3-4 hours (45/45/60/45 min per flow)
**Access:** https://www.klaviyo.com/flows/create

---

## ✅ PREREQUISITES (ALL COMPLETE)

**Klaviyo Account:**
- Status: ✅ ACTIVE ($30/mo, 1,000 profiles tier)
- Account ID: WTx7Jb
- API Key: Configured in .env.admin

**Shopify Integration:**
- Status: ✅ CONNECTED
- Metrics: 6 configured
  - Placed Order
  - Checkout Started
  - Ordered Product
  - Fulfilled Order
  - Cancelled Order
  - Refunded Order

**Segments:**
- ✅ 10 configured (5 Shopify RFM + 5 engagement)
- Key segments:
  - "Opportunités de reconquête (Shopify)" - For Winback flow
  - "Nouveaux abonnés" - For Welcome flow
  - "Clients VIP (Shopify)" - For Repeat Purchase flow

**Discount Codes:**
- ✅ WELCOME10: ACTIVE (10% OFF, Welcome flow)
- ✅ WINBACK15: ACTIVE (15% OFF, 1000 uses, Winback flow)
- ✅ REVIEW10: ACTIVE (10% OFF, 2000 uses, Review flow)

---

## FLOW #1: CUSTOMER WINBACK - STANDARD (EMAIL & SMS)

**Time:** 45 minutes
**Template:** Customer Winback - Standard (Email & SMS)
**URL:** https://www.klaviyo.com/flows/create → Search "Customer Winback"

### Configuration

**Trigger:**
- Type: Segment
- Segment: "Opportunités de reconquête (Shopify)"
- Frequency: Once per profile

**Flow Steps:**

1. **Wait 60 Days (Auto-configured)**
   - Already part of segment definition

2. **Email #1: "We Miss You" (Day 60)**
   - Subject: "We miss you at Alpha Medical - 15% off your next order"
   - Preview: "Come back and save 15% on medical support equipment"
   - Discount Code: WINBACK15
   - CTA: "Claim Your 15% OFF"
   - Personalization:
     - {% if person.first_name %}Hi {{ person.first_name }}{% else %}Hi there{% endif %}
     - Last purchased: {{ event.OrderedProduct.ProductName|default:"medical equipment" }}

3. **Wait 7 Days**

4. **Email #2: "Last Chance" (Day 67)**
   - Subject: "Last chance: 15% OFF expires soon"
   - Preview: "Don't miss out on your exclusive comeback offer"
   - Discount Code: WINBACK15
   - CTA: "Shop Now - 15% OFF"

5. **SMS (Optional - Day 60)**
   - Message: "We miss you! Get 15% OFF at Alpha Medical with code WINBACK15. Shop now: alphamedical.shop"
   - Trigger: Same as Email #1

### Settings
- Status: Set to LIVE after review
- Smart Sending: ON (suppress if opened recent campaign)
- Quiet Hours: 9 PM - 9 AM local time

**ROI Projection:** +$10K-15K Year 1

---

## FLOW #2: WELCOME SERIES - FINAL EMAIL DISCOUNT

**Time:** 45 minutes
**Template:** Welcome Series (Multi-email)
**URL:** https://www.klaviyo.com/flows/create → Search "Welcome Series"

### Configuration

**Trigger:**
- Type: List
- List: "Liste d'adresses e-mail" (main email list)
- Trigger: When someone subscribes to list
- Frequency: Once per profile

**Conditional Exit:**
- Exit flow if: Placed Order (at any point)

**Flow Steps:**

1. **Email #1: Welcome (Day 0 - Immediate)**
   - Subject: "Welcome to Alpha Medical - Here's 10% OFF"
   - Preview: "Professional medical equipment you can trust"
   - Discount Code: WELCOME10
   - CTA: "Shop Now - Get 10% OFF"
   - Content:
     - Introduction to brand
     - FDA-compliant equipment
     - Free shipping over $50
     - 30-day satisfaction guarantee

2. **Wait 3 Days**
   - Conditional: Skip if Placed Order

3. **Email #2: Education (Day 3)**
   - Subject: "How to choose the right support equipment"
   - Preview: "Expert buying guides for your condition"
   - Content:
     - Link to blog articles (knee braces, posture correctors, etc.)
     - Product categories overview
     - Customer testimonials
   - CTA: "Browse Products"

4. **Wait 4 Days**
   - Conditional: Skip if Placed Order

5. **Email #3: Best Sellers (Day 7)**
   - Subject: "Our most popular products for pain relief"
   - Preview: "See what other customers are buying"
   - Content:
     - Top 5 best-selling products
     - Star ratings and reviews
     - Free shipping reminder
   - CTA: "Shop Best Sellers"

6. **Wait 7 Days**
   - Conditional: Skip if Placed Order

7. **Email #4: Final Discount (Day 14)**
   - Subject: "Last chance: 10% OFF expires in 48 hours"
   - Preview: "Don't miss your exclusive welcome discount"
   - Discount Code: WELCOME10
   - CTA: "Claim Your 10% OFF Now"
   - Urgency: "Offer expires in 48 hours"

### Settings
- Status: Set to LIVE after review
- Smart Sending: ON
- Duplication with Shopify Email: 25% (Day 0 reinforcement acceptable per complementarity matrix)

**ROI Projection:** +$5K-8K Year 1

---

## FLOW #3: REPEAT PURCHASE NURTURE - ORDER COUNT SPLIT

**Time:** 60 minutes
**Template:** Repeat Purchase Nurture
**URL:** https://www.klaviyo.com/flows/create → Search "Repeat Purchase"

### Configuration

**Trigger:**
- Type: Metric
- Metric: Placed Order (Shopify)
- Frequency: Every time

**Conditional Split by Order Count:**

### Branch A: First-Time Buyers (Order Count = 1)

1. **Wait 30 Days**
2. **Email: "Ready for your next order?"**
   - Subject: "How is your [product name] working for you?"
   - Preview: "We'd love to hear your feedback + special offer inside"
   - Content:
     - Ask for product feedback
     - Suggest complementary products
     - Offer: Free shipping on next order
   - CTA: "Shop Complementary Products"

### Branch B: Repeat Buyers (Order Count = 2)

1. **Wait 45 Days**
2. **Email: "VIP Customer Appreciation"**
   - Subject: "Thank you for being a valued customer"
   - Preview: "Exclusive offer for our repeat customers"
   - Content:
     - Thank you message
     - VIP benefits preview
     - Product recommendations based on purchase history
   - CTA: "Shop Your Favorites"

### Branch C: Loyal Customers (Order Count ≥ 3)

1. **Wait 60 Days**
   - Use Klaviyo's predictive analytics (CDP)
   - Trigger: 3-5 days BEFORE predicted next order date

2. **Email: "Time to Restock?"**
   - Subject: "Is it time to restock your [product category]?"
   - Preview: "We noticed you might need a refill soon"
   - Content:
     - Predictive reorder suggestion
     - "Buy again" button for previous purchases
     - Bundle discount offer (10% on 2+ items)
   - CTA: "Reorder Now"

### Settings
- Status: Set to LIVE after review
- Smart Sending: ON
- Klaviyo CDP: Enable predictive analytics (auto-configured for Order Count ≥ 3)

**ROI Projection:** +$8K-12K Year 1

---

## FLOW #4: PRODUCT REVIEW / CROSS-SELL - STANDARD

**Time:** 45 minutes
**Template:** Post-Purchase Review Request
**URL:** https://www.klaviyo.com/flows/create → Search "Review Request"

### Configuration

**Trigger:**
- Type: Metric
- Metric: Fulfilled Order (Shopify)
- Frequency: Once per order

**Timing:**
- Delay: 7-10 days after fulfillment (product received and tested)

**Flow Steps:**

1. **Wait 7 Days After Fulfillment**

2. **Email #1: Review Request**
   - Subject: "How is your {{ event.OrderedProduct.ProductName|default:"purchase" }}?"
   - Preview: "Share your experience + get 10% OFF your next order"
   - Content:
     - Thank you for purchase
     - Request honest review
     - Offer: REVIEW10 discount code for completing review
   - CTA: "Write a Review - Get 10% OFF"
   - Review Link: Direct to product page reviews section

3. **Wait 3 Days**
   - Conditional: Skip if review submitted OR new order placed

4. **Email #2: Cross-Sell Recommendations**
   - Subject: "Products that complement your {{ event.OrderedProduct.ProductName }}"
   - Preview: "Complete your pain relief setup with these essentials"
   - Content:
     - AI-recommended complementary products (from recommendations matrix)
     - Based on: assets/product-recommendations-matrix.js
     - Offer: REVIEW10 still valid
   - CTA: "Shop Recommended Products"

### Product Matching Logic
```liquid
{% if event.OrderedProduct.ProductName contains "Knee" %}
  Recommend: Knee straps, compression sleeves, cold therapy
{% elsif event.OrderedProduct.ProductName contains "Back" %}
  Recommend: Lumbar supports, posture correctors, heating pads
{% elsif event.OrderedProduct.ProductName contains "Wrist" %}
  Recommend: Thumb braces, compression gloves, ergonomic tools
{% else %}
  Recommend: Best sellers from same collection
{% endif %}
```

### Settings
- Status: Set to LIVE after review
- Smart Sending: ON
- Duplication with Shopify: 0% (Shopify "Thank you" = Day 0, Klaviyo = Day 7-10)

**ROI Projection:** +$5K-8K Year 1 + social proof reviews

---

## DEPLOYMENT CHECKLIST

### Before Starting
- [ ] Login to Klaviyo: https://www.klaviyo.com/login
- [ ] Navigate to Flows: https://www.klaviyo.com/flows/create
- [ ] Verify Shopify integration active
- [ ] Confirm segments populated (check "Opportunités de reconquête" has profiles)

### During Deployment (Each Flow)
- [ ] Select correct template from library
- [ ] Configure trigger (segment/metric/list)
- [ ] Set up conditional exits (Placed Order)
- [ ] Add email content with personalization
- [ ] Insert discount codes (WELCOME10, WINBACK15, REVIEW10)
- [ ] Configure wait times
- [ ] Enable Smart Sending
- [ ] Set quiet hours (9 PM - 9 AM)
- [ ] Preview emails on mobile + desktop
- [ ] Test with test profile

### After All Flows Created
- [ ] Review flow analytics dashboard
- [ ] Verify no conflicts with Shopify Email (check complementarity matrix)
- [ ] Set all flows to LIVE (not draft)
- [ ] Monitor first 48 hours for send rates
- [ ] Check email deliverability (spam score)

---

## COMPLEMENTARITY WITH SHOPIFY EMAIL/FLOW

**Zero Duplication Strategy:**

| Shopify Email/Flow | Klaviyo Flow | Overlap | Action |
|-------------------|--------------|---------|--------|
| Welcome (Day 0) | Welcome Series (Day 0/3/7/14) | 25% Day 0 | ✅ KEEP BOTH (reinforcement acceptable) |
| Thank you (Day 0) | Review Request (Day 7-10) | 0% | ✅ KEEP BOTH (different timing) |
| Browse/Cart/Checkout abandonment | None | 0% | ✅ KEEP Shopify only |
| None | Customer Winback (Day 60+) | 0% | ✅ ADD Klaviyo (unique) |
| None | Repeat Purchase (ML-predicted) | 0% | ✅ ADD Klaviyo (unique) |

**Total Complementarity:** 93%+ (duplication <7%)

---

## VERIFICATION AFTER DEPLOYMENT

### Via Klaviyo Dashboard
1. Flows → All Flows
2. Verify status: LIVE (not draft)
3. Check metrics after 24-48h:
   - Recipients sent
   - Open rates
   - Click rates
   - Conversions

### Via Klaviyo API (Automated)
```python
import requests

headers = {
    "Authorization": "Klaviyo-API-Key pk_3055b7c6594e513a36d470d2bf8044017e",
    "revision": "2024-10-15"
}

r = requests.get("https://a.klaviyo.com/api/flows/", headers=headers)
flows = r.json()['data']

for flow in flows:
    print(f"{flow['attributes']['name']}: {flow['attributes']['status']}")
```

**Expected Output (After Deployment):**
```
Customer Winback - Standard (Email & SMS): live
Welcome Series - Final Email Discount: live
Repeat Purchase Nurture - Order Count Split: live
Product Review / Cross-Sell - Standard: live
```

---

## TROUBLESHOOTING

### Issue: Flow not triggering
- Check segment has profiles: Klaviyo → Segments → View count
- Verify Shopify metrics connected: Integrations → Shopify → Metrics
- Confirm trigger conditions met (e.g., 60 days lapsed for winback)

### Issue: Emails going to spam
- Verify domain authentication: Settings → Email → Sending domains
- Check SPF/DKIM records configured
- Warm up sending (start with small segments)

### Issue: Low open rates
- A/B test subject lines
- Adjust send times (test morning vs evening)
- Check smart sending not over-suppressing

### Issue: Discount codes not working
- Verify codes active in Shopify: Admin → Discounts
- Check usage limits not exceeded
- Confirm start/end dates valid

---

## EXPECTED RESULTS (MONTH 1-12)

**Month 1 (December 2025):**
- Recipients: ~100-200 (small subscriber base)
- Revenue: +$1.5K-3K
- Attribution: Welcome + Review flows (immediate triggers)

**Month 3 (February 2026):**
- Recipients: ~500-800
- Revenue: +$6.5K-11.5K
- Attribution: Winback + Repeat Purchase kick in

**Year 1 (December 2026):**
- Total revenue attributed: +$28K-43K
- ROI: 8-12× ($30/mo cost = $360/year)
- Average order value lift: +15-20%

**Breakdown by Flow:**
1. Customer Winback: $10K-15K (16% of lapsed customers convert)
2. Welcome Series: $5K-8K (8-12% conversion rate)
3. Repeat Purchase: $8K-12K (25% of customers become repeat buyers)
4. Product Review: $5K-8K (5-8% cross-sell rate)

---

## MANUAL STEPS REQUIRED

**User Actions (3-4 hours):**

1. **Login to Klaviyo** (2 min)
   - URL: https://www.klaviyo.com/login
   - Credentials: Owner's account

2. **Create Flow #1: Customer Winback** (45 min)
   - Navigate: Flows → Create Flow → Templates → "Customer Winback"
   - Follow: Configuration section above
   - Test: Send to test profile
   - Activate: Set to LIVE

3. **Create Flow #2: Welcome Series** (45 min)
   - Template: "Welcome Series (Multi-email)"
   - Configure: 4 emails (Day 0/3/7/14)
   - Test: Send to test profile
   - Activate: Set to LIVE

4. **Create Flow #3: Repeat Purchase Nurture** (60 min)
   - Template: "Repeat Purchase Nurture"
   - Configure: 3 branches (Order Count split)
   - Enable: Klaviyo CDP predictive analytics
   - Test: Send to test profiles (simulate different order counts)
   - Activate: Set to LIVE

5. **Create Flow #4: Product Review** (45 min)
   - Template: "Post-Purchase Review Request"
   - Configure: 2 emails (review + cross-sell)
   - Link: Product recommendations matrix
   - Test: Send to test profile
   - Activate: Set to LIVE

6. **Verification** (15 min)
   - Dashboard: Check all 4 flows = LIVE status
   - API: Run verification script (provided above)
   - Monitor: First 24-48h for send rates

---

## SUPPORT RESOURCES

**Klaviyo Documentation:**
- Flows Overview: https://help.klaviyo.com/hc/en-us/sections/4408140436123
- Shopify Integration: https://help.klaviyo.com/hc/en-us/articles/115005255808
- Predictive Analytics: https://help.klaviyo.com/hc/en-us/articles/115005246828

**Internal Documentation:**
- Complementarity Matrix: KLAVIYO_SHOPIFY_COMPLEMENTARITY_MATRIX_FACTUAL.md
- Discount Codes Setup: KLAVIYO_DISCOUNT_CODES_SETUP.md
- Infrastructure Audit: INFRASTRUCTURE_AUDIT_CHECKLIST.md

---

**Guide Complete | 2025-11-26**
**Prerequisites:** ✅ 100% READY (Klaviyo active, segments configured, codes active)
**Estimated Time:** 3-4 hours manual UI work
**Expected ROI:** +$28K-43K Year 1 (8-12× return)
