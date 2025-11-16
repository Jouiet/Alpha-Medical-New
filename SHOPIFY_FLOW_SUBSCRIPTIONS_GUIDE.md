# SHOPIFY FLOW - SUBSCRIPTIONS AUTOMATION GUIDE

**Date:** 2025-11-16
**Status:** MANUAL SETUP REQUIRED
**Cost:** $0 (Shopify native features)
**Effort:** 3-4 hours
**Prerequisites:** Selling plans created, products assigned

---

## OVERVIEW

This guide provides step-by-step instructions to create 4 Shopify Flows for automating subscription email notifications.

**Shopify Admin URL:** https://admin.shopify.com/store/azffej-as/flow

---

## FLOW 1: SUBSCRIPTION CREATED - WELCOME EMAIL

**Purpose:** Send welcome email when customer creates a new subscription

### CONFIGURATION

**Trigger:** Subscription contract created
**Conditions:** None (all new subscriptions)
**Actions:**
1. Send email to customer
2. Add customer tag: `subscription-active`

### EMAIL TEMPLATE

**Subject:** Welcome to Subscribe & Save! 🎉

**Body:**
```
Hi {{ customer.first_name }},

Thank you for subscribing to {{ subscription.product.title }}!

Your Subscription Details:
- Delivery Frequency: Every {{ subscription.delivery_interval }} days
- Discount: {{ subscription.discount_percentage }}% OFF
- Next Delivery: {{ subscription.next_billing_date | date: "%B %d, %Y" }}
- Price per order: {{ subscription.price | money }}

What You Can Do:
✅ Pause your subscription anytime
✅ Skip a delivery if needed
✅ Cancel without penalty
✅ Update payment method

Manage your subscription here:
https://www.alphamedical.shop/tools/recurring/portal

Questions? Reply to this email or contact us at [email protected]

Best regards,
Alpha Medical Care Team

---
This is an automated email. Please do not reply directly to this message.
```

### SETUP STEPS

1. Go to Shopify Admin → Settings → Apps and sales channels → Flow
2. Click "Create workflow"
3. **Trigger:** Search "subscription" → Select "Subscription contract created"
4. **Condition:** (None - apply to all)
5. **Action 1:** Search "send email" → Select "Send internal or customer email"
   - To: `{{ trigger.subscriptionContract.customer.email }}`
   - From: `[email protected]`
   - Subject: (copy from template above)
   - Body: (copy from template above)
6. **Action 2:** Search "tag" → Select "Add customer tag"
   - Tag: `subscription-active`
7. Click "Turn on workflow"

---

## FLOW 2: SUBSCRIPTION UPCOMING - REMINDER EMAIL (3 DAYS BEFORE)

**Purpose:** Send reminder email 3 days before next subscription charge

### CONFIGURATION

**Trigger:** Subscription billing attempt upcoming (3 days)
**Conditions:** Subscription status = Active
**Actions:**
1. Send reminder email to customer

### EMAIL TEMPLATE

**Subject:** Your {{ product.title }} delivery is coming soon 📦

**Body:**
```
Hi {{ customer.first_name }},

Your subscription delivery is scheduled for {{ subscription.next_billing_date | date: "%B %d, %Y" }} (in 3 days).

Order Details:
- Product: {{ subscription.product.title }}
- Price: {{ subscription.price | money }} ({{ subscription.discount_percentage }}% OFF)
- Payment Method: {{ subscription.payment_method_last4 }}

Need to make changes?
- Skip this delivery: https://www.alphamedical.shop/tools/recurring/portal
- Pause subscription: https://www.alphamedical.shop/tools/recurring/portal
- Update payment: https://www.alphamedical.shop/tools/recurring/portal

Your order will be processed automatically in 3 days.

Questions? Contact us at [email protected]

Best regards,
Alpha Medical Care Team

---
To manage your subscription, visit: https://www.alphamedical.shop/tools/recurring/portal
```

### SETUP STEPS

1. Go to Shopify Admin → Settings → Apps and sales channels → Flow
2. Click "Create workflow"
3. **Trigger:** Search "subscription" → Select "Subscription billing attempt upcoming"
   - Set reminder: 3 days before
4. **Condition:** Add condition → Subscription contract status = ACTIVE
5. **Action:** Send email (copy template above)
6. Click "Turn on workflow"

### LIMITATION (HONEST)

⚠️ **Shopify Flow Basic limitation:** "Subscription billing attempt upcoming" trigger may not be available on Basic plan. If unavailable, this flow cannot be automated natively ($0 cost). Alternative:
- Use Klaviyo (paid app, ~$20-60/mo)
- Manual email reminders (not scalable)
- Upgrade to Shopify plan ($79/mo)

**Verdict:** Skip this flow if trigger unavailable. Focus on Flows 1, 3, 4 instead.

---

## FLOW 3: SUBSCRIPTION PAYMENT FAILED - RETRY NOTICE

**Purpose:** Send email when subscription payment fails, prompting customer to update payment method

### CONFIGURATION

**Trigger:** Subscription billing attempt failure
**Conditions:** None (all failed payments)
**Actions:**
1. Send payment failure email to customer
2. Add customer tag: `subscription-payment-issue`

### EMAIL TEMPLATE

**Subject:** Action Required: Update Your Payment Method 🔴

**Body:**
```
Hi {{ customer.first_name }},

We attempted to process your subscription payment for {{ subscription.product.title }}, but the payment failed.

Issue Details:
- Subscription: {{ subscription.product.title }}
- Amount: {{ subscription.price | money }}
- Failed on: {{ "now" | date: "%B %d, %Y" }}
- Reason: {{ billing_attempt.error_message }}

Action Required:
Please update your payment method to continue your subscription benefits.

Update Payment Method:
https://www.alphamedical.shop/tools/recurring/portal

We'll automatically retry your payment in 24 hours. If the issue persists, your subscription may be paused.

Questions? Contact us immediately at [email protected]

Best regards,
Alpha Medical Care Team

---
IMPORTANT: Your subscription will be paused after 3 failed payment attempts.
```

### SETUP STEPS

1. Go to Shopify Admin → Settings → Apps and sales channels → Flow
2. Click "Create workflow"
3. **Trigger:** Search "subscription" → Select "Subscription billing attempt failure"
4. **Condition:** (None - apply to all)
5. **Action 1:** Send email (copy template above)
6. **Action 2:** Add customer tag: `subscription-payment-issue`
7. Click "Turn on workflow"

---

## FLOW 4: SUBSCRIPTION CANCELLED - FEEDBACK REQUEST

**Purpose:** Send email when customer cancels subscription, request feedback

### CONFIGURATION

**Trigger:** Subscription contract updated (status changed to cancelled)
**Conditions:** New status = Cancelled
**Actions:**
1. Send cancellation confirmation email
2. Remove tag: `subscription-active`
3. Add tag: `subscription-cancelled`

### EMAIL TEMPLATE

**Subject:** We're sorry to see you go 😢

**Body:**
```
Hi {{ customer.first_name }},

We've confirmed the cancellation of your subscription for {{ subscription.product.title }}.

Cancellation Details:
- Cancelled on: {{ "now" | date: "%B %d, %Y" }}
- Final delivery: {{ subscription.next_billing_date | date: "%B %d, %Y" }} (if already shipped)

We'd Love Your Feedback:
Help us improve by answering one question: Why did you cancel?

[Survey Link - Optional: Create Google Form]

Special Offer - Come Back Anytime:
Use code COMEBACK15 for 15% OFF your next order (valid 90 days)

We hope to serve you again soon!

Best regards,
Alpha Medical Care Team

P.S. You can always restart your subscription: https://www.alphamedical.shop/collections/all

---
Need help? Contact us at [email protected]
```

### SETUP STEPS

1. Go to Shopify Admin → Settings → Apps and sales channels → Flow
2. Click "Create workflow"
3. **Trigger:** Search "subscription" → Select "Subscription contract updated"
4. **Condition:** Add condition → "Status changed from" = ACTIVE → "Status changed to" = CANCELLED
5. **Action 1:** Send email (copy template above)
6. **Action 2:** Remove customer tag: `subscription-active`
7. **Action 3:** Add customer tag: `subscription-cancelled`
8. Click "Turn on workflow"

---

## OPTIONAL: FLOW 5 - SUBSCRIPTION PAUSED (BONUS)

**Purpose:** Confirm when customer pauses subscription

### EMAIL TEMPLATE (BRIEF)

**Subject:** Subscription Paused - We'll Be Here When You're Ready

**Body:**
```
Hi {{ customer.first_name }},

Your subscription for {{ subscription.product.title }} has been paused.

What This Means:
- No charges until you resume
- Your discounts are saved
- Resume anytime with one click

Resume Your Subscription:
https://www.alphamedical.shop/tools/recurring/portal

Questions? We're here to help: [email protected]

Best regards,
Alpha Medical Care Team
```

---

## TESTING CHECKLIST

**Before Going Live:**

1. **Test Flow 1 (Subscription Created):**
   - [ ] Create test customer account
   - [ ] Subscribe to a product (use test payment method)
   - [ ] Verify welcome email received
   - [ ] Check customer tags updated (`subscription-active`)

2. **Test Flow 3 (Payment Failed):**
   - [ ] Use test payment method that fails (e.g., card 4000 0000 0000 0341)
   - [ ] Verify payment failure email received
   - [ ] Check customer tag added (`subscription-payment-issue`)

3. **Test Flow 4 (Cancelled):**
   - [ ] Cancel test subscription via customer portal
   - [ ] Verify cancellation email received
   - [ ] Check customer tags updated (removed `subscription-active`, added `subscription-cancelled`)

4. **Email Content Review:**
   - [ ] All links work (customer portal, support email)
   - [ ] Liquid variables render correctly ({{ customer.first_name }}, etc.)
   - [ ] Mobile responsive design
   - [ ] Branding matches Alpha Medical style

---

## FLOW LIMITATIONS (SHOPIFY BASIC PLAN)

### What Works:
- ✅ Flow 1: Subscription created (trigger available)
- ✅ Flow 3: Payment failed (trigger available)
- ✅ Flow 4: Cancelled (trigger available)

### What May NOT Work:
- ⚠️ Flow 2: Upcoming reminder (trigger may be Shopify plan only)

### Workaround for Flow 2:
If "Subscription billing attempt upcoming" trigger is unavailable:
1. **Option A:** Upgrade to Shopify plan ($79/mo) - only if revenue justifies
2. **Option B:** Use Klaviyo ($20-60/mo) - overkill if only for this one flow
3. **Option C:** Skip automated reminders - rely on Shopify's default emails
4. **Option D:** Manual weekly check + Mailchimp batch emails (free tier)

**Recommended:** Start with Flows 1, 3, 4 only. Add Flow 2 later if customer demand justifies cost.

---

## IMPLEMENTATION TIMELINE

### Week 1: Setup Flows
- Day 1: Create Flow 1 (Subscription Created)
- Day 2: Create Flow 3 (Payment Failed)
- Day 3: Create Flow 4 (Cancelled)
- Day 4-5: Test all flows with test subscriptions

### Week 2: Monitor & Optimize
- Monitor email open rates (Shopify Admin → Marketing)
- Track subscription conversion rate
- Collect customer feedback
- Adjust email copy based on responses

### Week 3: Advanced (Optional)
- Add Flow 2 (if trigger available)
- Create Flow 5 (Paused)
- Integrate with Klaviyo for advanced segmentation (if needed)

---

## EXPECTED IMPACT

**Email Performance Benchmarks (Industry Average):**
- Welcome email open rate: 50-60%
- Upcoming reminder open rate: 30-40%
- Payment failed open rate: 70-80% (urgent)
- Cancellation email open rate: 40-50%

**Retention Impact:**
- Automated emails improve retention by 15-25%
- Payment failure recovery rate: 30-40% (with automated retry notice)
- Win-back rate: 5-10% (from cancellation emails)

**Revenue Impact (Conservative Estimate):**
- Assume 50 subscriptions/month
- Average subscription value: $300
- Retention improvement: +15%
- Additional revenue: $2,250/month ($27k/year)

---

## NEXT STEPS

1. **Create Selling Plans:**
   - Run `python3 create_selling_plans.py`
   - Assign products to selling plan groups in Shopify Admin

2. **Deploy Subscription Widget:**
   - Run `python3 deploy_subscription_widget.py`
   - Verify widget appears on product pages

3. **Setup Shopify Flows:**
   - Follow this guide to create Flows 1, 3, 4
   - Test with test customer accounts

4. **Monitor Performance:**
   - Track subscription metrics in Shopify Admin
   - Monitor email performance
   - Adjust flows based on customer feedback

---

**DOCUMENT STATUS:** READY FOR IMPLEMENTATION
**COST:** $0 (100% native Shopify features)
**ESTIMATED EFFORT:** 3-4 hours (manual flow setup)
**EXPECTED IMPACT:** +15-25% subscription retention, +$27k/year revenue
