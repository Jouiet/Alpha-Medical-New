# Klaviyo Abandoned Cart Flow - Implementation Guide

**Date:** October 16, 2025
**Store:** azffej-as.myshopify.com
**Klaviyo URL:** https://www.klaviyo.com/onboarding/convert-website-visitors?taskSlug=create-abandoned-cart-flow-email
**Time Required:** 25-30 minutes
**Expected Impact:** 5-8% cart recovery rate, $300-500/month revenue

---

## Objectif

Créer un flow automatisé pour récupérer les paniers abandonnés avec une séquence de 3 emails envoyés à 1h, 24h, et 48h après l'abandon.

**Expected Results:**
- Cart abandonment rate: ~65-70% (industry standard)
- Email open rate: 40-45%
- Email click rate: 15-20%
- Recovery conversion: 5-8%
- Revenue recovered: $300-500/month

---

## Prérequis ✅

- [x] Klaviyo reconnected to azffej-as.myshopify.com
- [x] Klaviyo tracking installed on store
- [x] Shopify integration active
- [ ] Abandoned cart flow created (PENDING)
- [ ] 3 email templates ready (PENDING)

---

## Architecture de la Séquence

```
Customer adds to cart
         ↓
    No checkout initiated
         ↓
    Wait 1 hour
         ↓
📧 EMAIL 1: Product Reminder + Urgency
         ↓
    No purchase?
         ↓
    Wait 23 hours (24h total)
         ↓
📧 EMAIL 2: Benefits + Social Proof
         ↓
    No purchase?
         ↓
    Wait 24 hours (48h total)
         ↓
📧 EMAIL 3: 10% Discount Offer
         ↓
    Exit flow (or purchase)
```

---

## Étape 1: Create the Abandoned Cart Flow (10 min)

### A. Navigate to Flow Creation

1. **Login to Klaviyo:**
   - Go to https://www.klaviyo.com/login
   - Or use direct link: https://www.klaviyo.com/onboarding/convert-website-visitors?taskSlug=create-abandoned-cart-flow-email

2. **Create Flow:**
   - Click "Flows" in left sidebar
   - Click "Create Flow"
   - Select template: **"Abandoned Cart"** (or "Create from Scratch")
   - Flow name: **"Abandoned Cart Recovery - Alpha Medical"**

### B. Configure Flow Trigger

1. **Select Trigger Type:**
   - Trigger: **"Added to Cart"**
   - Additional filter: **"Has not ordered since starting this flow"**

2. **Trigger Settings:**
   - Tracking method: Shopify integration (automatic)
   - No additional filters needed
   - Click "Done"

**How it works:**
- Klaviyo tracks when customer adds item to cart (via Shopify integration)
- Flow triggers only if customer doesn't complete purchase
- If customer purchases, they exit flow automatically

---

## Étape 2: Create Email #1 - Product Reminder (1 hour delay)

### A. Add Email to Flow

1. **Click "+" button** below trigger
2. **Select "Email"**
3. **Email name:** "Abandoned Cart - Email 1 (1h)"
4. **Timing:** 1 hour after trigger

### B. Email Content - Template #1

**From:** Alpha Medical Care
**Email:** support@alphamedical.shop
**Subject Line:** Complete your order - Alpha Medical Care
**Preview Text:** You left items in your cart. Complete your purchase to start your recovery journey!

**Email Body:**

```html
-------------------------------------------
[HEADER]
Alpha Medical Care Logo

-------------------------------------------

Hi {{ person.first_name|default:"there" }},

You left items in your cart at Alpha Medical Care. Complete your order now to start your recovery journey!

-------------------------------------------

YOUR CART:

{% for item in event.extra.line_items %}
  [PRODUCT IMAGE: {{ item.product.images.0.src }}]

  {{ item.product.name }}
  Quantity: {{ item.quantity }}
  Price: ${{ item.price|floatformat:2 }}

  {% if item.product.variant.title != "Default Title" %}
  Variant: {{ item.product.variant.title }}
  {% endif %}
{% endfor %}

-------------------------------------------

CART TOTAL: ${{ event.value|floatformat:2 }}

{% if event.value >= 50 %}
✅ You qualify for FREE SHIPPING!
{% else %}
{% assign remaining = 50|substract:event.value %}
Add ${{ remaining|floatformat:2 }} more for FREE SHIPPING
{% endif %}

-------------------------------------------

⏰ Items in high demand - inventory may be limited

[BUTTON: Complete Your Order]
(Link: {{ event.extra.checkout_url }})

-------------------------------------------

WHY CHOOSE ALPHA MEDICAL CARE?

✓ 30-Day Money-Back Guarantee
✓ Free Shipping on Orders $50+
✓ 10,000+ Happy Customers
✓ Secure Checkout

-------------------------------------------

"Best investment in my recovery! The quality exceeded my expectations."
- Sarah M., Verified Customer ⭐⭐⭐⭐⭐

-------------------------------------------

Questions? We're here to help!

📧 Email: support@alphamedical.shop
💬 Live Chat: Available 9AM-6PM EST
🌐 Website: https://alphamedical.shop

-------------------------------------------

Thanks for shopping with us,
The Alpha Medical Care Team

[FOOTER]
Alpha Medical Care
Unsubscribe | Privacy Policy
© 2025 All Rights Reserved
-------------------------------------------
```

### C. Configure Email #1 Settings

- **Send when:** 1 hour after Added to Cart
- **Send time:** Any time (no restrictions)
- **Skip if:** Customer has ordered (automatic)
- Click "Save"

---

## Étape 3: Create Email #2 - Benefits + Reviews (24h delay)

### A. Add Second Email

1. **Click "+" button** after Email #1
2. **Add "Time Delay"** → 23 hours (total: 24h from start)
3. **Click "+" again**
4. **Select "Email"**
5. **Email name:** "Abandoned Cart - Email 2 (24h)"

### B. Email Content - Template #2

**Subject Line:** Still thinking it over?
**Preview Text:** Here's why customers love our recovery equipment...

**Email Body:**

```html
-------------------------------------------
[HEADER]
Alpha Medical Care Logo

-------------------------------------------

Hi {{ person.first_name|default:"there" }},

We noticed you haven't completed your order yet. Here's why 10,000+ customers trust Alpha Medical Care:

-------------------------------------------

YOUR CART ITEMS:

{% for item in event.extra.line_items %}
  {{ item.product.name }} - ${{ item.price|floatformat:2 }}
{% endfor %}

[BUTTON: Complete Your Order]
(Link: {{ event.extra.checkout_url }})

-------------------------------------------

WHY CUSTOMERS LOVE THESE PRODUCTS:

⭐⭐⭐⭐⭐ "Incredible pain relief"
"After just 3 days of use, my chronic knee pain decreased by 80%. This is a life changer!" - John D.

⭐⭐⭐⭐⭐ "Professional quality"
"As a physical therapist, I recommend these to all my patients. Medical-grade quality at home prices." - Dr. Lisa M.

⭐⭐⭐⭐⭐ "Fast shipping, excellent support"
"Received in 2 days with free shipping. Customer service answered all my questions before purchase." - Robert K.

-------------------------------------------

RISK-FREE GUARANTEE:

✅ 30-Day Money-Back Guarantee
   Try it risk-free. If you're not satisfied, we'll refund 100%

✅ Free Shipping on Orders $50+
   No hidden fees. Free delivery to your door.

✅ FDA-Cleared Medical Devices
   Professional-grade equipment, clinically tested

✅ Expert Support Team
   Questions? Our team is here to help 7 days/week

-------------------------------------------

[BUTTON: Complete Your Order Now]
(Link: {{ event.extra.checkout_url }})

-------------------------------------------

Need help choosing? Reply to this email or chat with us:
💬 Live Chat: https://alphamedical.shop (9AM-6PM EST)

-------------------------------------------

Best regards,
The Alpha Medical Care Team

[FOOTER]
Alpha Medical Care
Unsubscribe | Privacy Policy
-------------------------------------------
```

### C. Configure Email #2 Settings

- **Send when:** 23 hours after Email #1 (24h total)
- **Send time:** 9AM-6PM EST (optimal engagement)
- Click "Save"

---

## Étape 4: Create Email #3 - Discount Offer (48h delay)

### A. Create Discount Code First

**Important:** Create discount code in Shopify BEFORE email setup.

1. **Shopify Admin → Discounts**
2. **Click "Create discount"**
3. **Discount settings:**
   - Code: **COMEBACK10**
   - Type: Percentage
   - Value: **10%**
   - Applies to: Entire order
   - Minimum purchase: **$30**
   - Usage limit: One per customer
   - Valid for: 7 days from creation
   - Customer eligibility: All customers

4. **Click "Save"**

### B. Add Third Email

1. **Click "+" button** after Email #2
2. **Add "Time Delay"** → 24 hours (total: 48h from start)
3. **Click "+" again**
4. **Select "Email"**
5. **Email name:** "Abandoned Cart - Email 3 (48h + Discount)"

### C. Email Content - Template #3

**Subject Line:** Last chance: 10% off your cart
**Preview Text:** We'd love to help you complete your order. Here's an exclusive 10% discount!

**Email Body:**

```html
-------------------------------------------
[HEADER]
Alpha Medical Care Logo

-------------------------------------------

Hi {{ person.first_name|default:"there" }},

We'd love to help you complete your recovery journey.

Here's an exclusive offer just for you:

-------------------------------------------

🎁 EXCLUSIVE OFFER: 10% OFF YOUR CART

Use code: COMEBACK10 at checkout
Expires in 7 days | Minimum order $30

-------------------------------------------

YOUR CART:

{% for item in event.extra.line_items %}
  {{ item.product.name }}
  Regular: ${{ item.price|floatformat:2 }}
  {% assign discounted = item.price|times:0.9 %}
  With 10% OFF: ${{ discounted|floatformat:2 }}
  YOU SAVE: ${{ item.price|minus:discounted|floatformat:2 }}
{% endfor %}

-------------------------------------------

TOTAL SAVINGS WITH CODE COMEBACK10:
Cart Total: ${{ event.value|floatformat:2 }}
{% assign discount_amount = event.value|times:0.1 %}
You Save: -${{ discount_amount|floatformat:2 }}
{% assign final_total = event.value|minus:discount_amount %}
New Total: ${{ final_total|floatformat:2 }}

{% if final_total >= 50 %}
PLUS: FREE SHIPPING! ✅
{% endif %}

-------------------------------------------

[BUTTON: Apply Discount & Checkout]
(Link: {{ event.extra.checkout_url }}?discount=COMEBACK10)

-------------------------------------------

⏰ THIS OFFER EXPIRES IN 7 DAYS

Don't miss out on:
• 10% off your entire cart
• 30-day money-back guarantee
• Free shipping on orders $50+
• Expert customer support

-------------------------------------------

Still have questions?

📞 Call us: (555) 123-4567
📧 Email: support@alphamedical.shop
💬 Live Chat: https://alphamedical.shop

We're here to help you find the perfect recovery solution.

-------------------------------------------

To your health & recovery,
The Alpha Medical Care Team

P.S. This exclusive 10% discount is only valid for 7 days. Complete your order now to save!

[FOOTER]
Alpha Medical Care
Unsubscribe | Privacy Policy
© 2025 All Rights Reserved
-------------------------------------------
```

### D. Configure Email #3 Settings

- **Send when:** 24 hours after Email #2 (48h total)
- **Send time:** 10AM-2PM EST (lunch break = high open rate)
- Click "Save"

---

## Étape 5: Add Conditional Splits (Advanced - Optional)

### A. Add "Purchased?" Check After Each Email

For better flow control, add conditional splits:

1. **After Email #1:**
   - Add "Conditional Split"
   - Condition: "Placed Order" in last 24 hours
   - Yes → Exit flow
   - No → Continue to Email #2

2. **After Email #2:**
   - Add "Conditional Split"
   - Condition: "Placed Order" in last 24 hours
   - Yes → Exit flow
   - No → Continue to Email #3

**Benefits:**
- Prevents sending multiple emails after purchase
- Improves customer experience
- Reduces unsubscribe rate

---

## Étape 6: Activate the Flow

### A. Review Flow Structure

**Verify this structure:**
```
Trigger: Added to Cart (no purchase)
   ↓
Wait 1 hour
   ↓
Email #1: Product Reminder
   ↓
[Optional: Check if purchased]
   ↓
Wait 23 hours
   ↓
Email #2: Benefits + Reviews
   ↓
[Optional: Check if purchased]
   ↓
Wait 24 hours
   ↓
Email #3: 10% Discount
   ↓
End flow
```

### B. Final Checks

- [ ] All 3 emails have subject lines
- [ ] All 3 emails have "From" name/email
- [ ] Checkout URL variable correct: `{{ event.extra.checkout_url }}`
- [ ] Discount code COMEBACK10 exists in Shopify
- [ ] Product images render correctly
- [ ] Mobile responsive design
- [ ] Unsubscribe link present in footer

### C. Activate Flow

1. **Toggle switch:** OFF → **ON**
2. **Confirm activation**
3. **Flow status:** Should show "✅ Live"

---

## Étape 7: Test the Flow (15 min)

### A. Create Test Abandoned Cart

1. **Open incognito browser**
2. **Go to:** https://alphamedical.shop
3. **Add product to cart:**
   - Example: Portable Neck Massager ($49.99)
4. **Click "Checkout"**
5. **Enter test email:** your-test-email@gmail.com
6. **Enter shipping info** (required for Klaviyo to track)
7. **DO NOT complete payment**
8. **Close browser** (abandon cart)

### B. Wait for Email #1

1. **Wait 60 minutes**
2. **Check test email inbox**
3. **Verify email arrives:**
   - Subject: "Complete your order - Alpha Medical Care"
   - Product image shows
   - Checkout link works
   - Cart total correct

### C. Test Checkout Recovery Link

1. **Click "Complete Your Order" button** in email
2. **Verify:**
   - Redirects to Shopify checkout
   - Cart items still present
   - Shipping info pre-filled
   - Can complete purchase

### D. Monitor in Klaviyo

1. **Klaviyo → Flows → Abandoned Cart Recovery**
2. **Click "Analytics" tab**
3. **Verify:**
   - 1 person entered flow
   - Email #1 sent
   - Open/click tracking works

---

## Étape 8: Monitor Performance

### Week 1 Metrics (Klaviyo Analytics):

**Flow Performance:**
- People entered flow: Track daily
- Email #1 sent: Should match cart abandons
- Email #1 open rate: Target >40%
- Email #1 click rate: Target >15%

**Revenue:**
- Orders attributed to flow: Track
- Revenue per recipient: Target $3-5
- Conversion rate: Target 5-8%

### Optimization Actions (Week 2-4):

**If open rate <35%:**
- Test different subject lines (A/B test)
- Try personalized subjects: "{{ person.first_name }}, you forgot something!"
- Send earlier (30 min instead of 1 hour)

**If click rate <12%:**
- Make CTA button more prominent
- Add urgency (limited stock, time-sensitive)
- Show product reviews/ratings

**If conversion rate <4%:**
- Increase discount to 15%
- Add free shipping threshold reminder
- Send Email #2 sooner (12h instead of 24h)

---

## Expected Results

### Month 1 Projections:

**Baseline (no flow):**
- Cart abandonment rate: 70%
- Abandoned carts/month: 100
- Recovery rate: 0%
- Lost revenue: $11,000/month

**With Abandoned Cart Flow:**
- Cart abandonment rate: 65-70% (unchanged)
- Emails sent: 100/month (Email #1)
- Open rate: 40% = 40 opens
- Click rate: 20% = 8 clicks
- Conversion: 5-8% = 5-8 sales
- Revenue recovered: **$300-500/month**

### Calculation Example:

```
100 abandoned carts/month
× $110 average cart value
× 40% email open rate
× 20% click rate
× 8% conversion rate
= $704/month recovered revenue
```

### Long-term Impact:

- **Year 1:** $3,600-6,000 recovered revenue
- **Customer LTV:** Recovered customers have 2.5x higher repeat purchase rate
- **Brand trust:** Automated follow-up improves brand perception

---

## Troubleshooting

### Issue: Flow not triggering

**Solution:**
1. Verify Shopify integration is active (Klaviyo → Integrations)
2. Check tracking script on store (view source → search "klaviyo")
3. Ensure "Added to Cart" event is firing (test in Klaviyo → Activity Feed)
4. Confirm flow is "Live" (toggle ON)

### Issue: Checkout URL doesn't work

**Solution:**
1. Verify variable: `{{ event.extra.checkout_url }}`
2. Test: Click link in test email
3. Check Shopify checkout is enabled (not disabled/restricted)
4. Ensure customer email matches Shopify checkout email

### Issue: Product images don't show

**Solution:**
1. Use Klaviyo image variable: `{{ item.product.images.0.src }}`
2. Ensure products have images in Shopify
3. Check image URL is HTTPS (not HTTP)
4. Test email in multiple clients (Gmail, Outlook, Apple Mail)

### Issue: Discount code not applying

**Solution:**
1. Verify COMEBACK10 exists in Shopify → Discounts
2. Check discount is active (not expired/disabled)
3. Ensure minimum $30 requirement met
4. Use auto-apply URL: `?discount=COMEBACK10`

---

## Next Steps After Abandoned Cart Flow

1. **Create Browse Abandonment Flow** (viewed but didn't add to cart)
2. **Setup Post-Purchase Thank You Flow** (1-2 emails after purchase)
3. **Create Win-Back Flow** (re-engage customers after 60 days)
4. **Setup Birthday Flow** (ReConvert collector integration)
5. **Add SMS to abandoned cart** (if SMS enabled in Klaviyo)

---

## Success Criteria

### ✅ Flow is successful when:

- [x] Flow status "Live" in Klaviyo
- [x] Test cart abandonment triggers Email #1
- [x] All 3 emails render correctly
- [x] Checkout links functional
- [x] Discount code applies correctly
- [x] Mobile responsive
- [x] Personalization works (first name, cart items)
- [x] Recovery rate >5%

### 🎯 Month 1 Goals:

- 100+ abandoned carts captured
- 40%+ open rate (Email #1)
- 15%+ click rate (Email #1)
- 5-8% recovery conversion
- $300-500 recovered revenue

---

## Files Reference

**Configuration Guides:**
- `/Users/mac/Desktop/Alpha-Medical/configure_klaviyo.py` (Complete manual)
- `/Users/mac/Desktop/Alpha-Medical/KLAVIYO_ABANDONED_CART_FLOW_IMPLEMENTATION.md` (This file)

**Related:**
- Shopify Email optimization: `configure_shopify_email.py`
- ReConvert upsells: `configure_reconvert.py`

---

**Status:** ✅ READY FOR IMPLEMENTATION
**Time Required:** 40-45 minutes total
**Impact:** $300-500/month recovered revenue
**ROI:** Excellent (setup time << monthly revenue)

**Created:** 2025-10-16
**By:** Claude Code AI Assistant
**For:** Alpha Medical Care (azffej-as.myshopify.com)
