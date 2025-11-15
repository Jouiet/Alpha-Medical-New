# Loyalty System - Complete Setup Guide

**Date:** 2025-11-15
**Status:** Ready for deployment (requires Shopify plan upgrade)
**Estimated Setup Time:** 2-3 hours

---

## 🚨 PREREQUISITE: SHOPIFY PLAN UPGRADE REQUIRED

**CRITICAL:** This loyalty system requires **Shopify Plan** ($79/month) or higher.

**Why:** Customer API access (required for metafields) is NOT available on Basic plan.

**Before proceeding:**
1. Upgrade plan: Shopify Admin → Settings → Plan → Upgrade to Shopify
2. Wait 5-10 minutes for API permissions to propagate
3. Then proceed with setup below

---

## 📋 SETUP CHECKLIST

- [ ] **Step 1:** Upgrade Shopify plan to Shopify ($79/month)
- [ ] **Step 2:** Run `loyalty_setup.py` (create metafield definitions)
- [ ] **Step 3:** Deploy `loyalty_webhooks.gs` to Google Apps Script
- [ ] **Step 4:** Deploy `loyalty_redemption_api.gs` to Google Apps Script
- [ ] **Step 5:** Configure Shopify webhooks
- [ ] **Step 6:** Test with test customer
- [ ] **Step 7:** Deploy to production (already done - widgets live)

---

## STEP 1: SHOPIFY PLAN UPGRADE

### Upgrade Process

1. Go to Shopify Admin: https://admin.shopify.com/store/azffej-as
2. Settings → Plan & permissions
3. Click "Change plan"
4. Select "Shopify" ($79/month)
5. Confirm upgrade
6. Wait 5-10 minutes for API permissions

### Verify Upgrade

```bash
python3 loyalty_manager.py balance loyalty.test@alphamedical.shop
```

**Expected output (BEFORE upgrade):**
```
❌ ACCESS_DENIED: Customer API not available on Basic plan
```

**Expected output (AFTER upgrade):**
```
✅ Customer found
{
  "success": true,
  "points": 0,
  "tier": "bronze",
  ...
}
```

---

## STEP 2: CREATE CUSTOMER METAFIELD DEFINITIONS

### Run Setup Script

```bash
cd /Users/mac/Desktop/Alpha-Medical
python3 loyalty_setup.py
```

### Expected Output

```
============================================================
LOYALTY SYSTEM METAFIELD SETUP
============================================================
Store: azffej-as.myshopify.com
API Version: 2024-10

✅ Created: loyalty.points (number_integer)
✅ Created: loyalty.tier (single_line_text_field)
✅ Created: loyalty.history (json)
✅ Created: loyalty.signup_bonus_claimed (boolean)
✅ Created: loyalty.lifetime_points_earned (number_integer)
✅ Created: loyalty.lifetime_points_redeemed (number_integer)

============================================================
SETUP COMPLETE
============================================================
✅ Success: 6/6
❌ Failed: 0/6

🎉 All metafield definitions created successfully!
```

### Verify in Shopify Admin

1. Go to: Settings → Custom Data → Customers
2. You should see 6 metafield definitions under namespace "loyalty":
   - `loyalty.points`
   - `loyalty.tier`
   - `loyalty.history`
   - `loyalty.signup_bonus_claimed`
   - `loyalty.lifetime_points_earned`
   - `loyalty.lifetime_points_redeemed`

---

## STEP 3: DEPLOY WEBHOOKS HANDLER (Google Apps Script)

### Create New Apps Script Project

1. Go to: https://script.google.com
2. Click "+ New project"
3. Name: "Alpha Medical - Loyalty Webhooks"
4. Copy entire contents of `loyalty_webhooks.gs`
5. Paste into Apps Script editor
6. Save (Ctrl+S)

### Deploy as Web App

1. Click "Deploy" → "New deployment"
2. Type: "Web app"
3. Description: "Loyalty webhooks handler"
4. Execute as: "Me"
5. Who has access: "Anyone"
6. Click "Deploy"
7. **COPY THE WEB APP URL** (format: `https://script.google.com/macros/s/.../exec`)

### Test Deployment

Run test function in Apps Script:
1. Select function: `testSignupBonus`
2. Click "Run"
3. Check "Execution log" for:
   ```
   ✅ Added 50 points to customer...
   ```

---

## STEP 4: DEPLOY REDEMPTION API (Google Apps Script)

### Create Second Apps Script Project

1. Go to: https://script.google.com
2. Click "+ New project"
3. Name: "Alpha Medical - Loyalty Redemption API"
4. Copy entire contents of `loyalty_redemption_api.gs`
5. Paste into Apps Script editor
6. Save (Ctrl+S)

### Deploy as Web App

1. Click "Deploy" → "New deployment"
2. Type: "Web app"
3. Description: "Loyalty redemption API"
4. Execute as: "Me"
5. Who has access: "Anyone"
6. Click "Deploy"
7. **COPY THE WEB APP URL**

### Update Frontend

Edit `snippets/loyalty-redemption-form.liquid`:

Find line ~75:
```liquid
const response = await fetch('/apps/loyalty/redeem', {
```

Replace with:
```liquid
const response = await fetch('PASTE_YOUR_APPS_SCRIPT_URL_HERE', {
```

---

## STEP 5: CONFIGURE SHOPIFY WEBHOOKS

### Webhook 1: Customer Create (Signup Bonus)

1. Go to: Shopify Admin → Settings → Notifications → Webhooks
2. Click "Create webhook"
3. Event: "Customer creation"
4. Format: "JSON"
5. URL: `[YOUR_WEBHOOKS_HANDLER_URL]?topic=customers/create`
6. API version: "2024-10"
7. Click "Save"

### Webhook 2: Order Paid (Purchase Points)

1. Click "Create webhook"
2. Event: "Order payment"
3. Format: "JSON"
4. URL: `[YOUR_WEBHOOKS_HANDLER_URL]?topic=orders/paid`
5. API version: "2024-10"
6. Click "Save"

### Test Webhooks

**Test Customer Create:**
1. Create test customer in Shopify Admin
2. Check Apps Script execution log
3. Verify 50 points awarded

**Test Order Paid:**
1. Create test order ($150) for test customer
2. Mark order as paid
3. Check Apps Script execution log
4. Verify 150 points awarded

---

## STEP 6: TEST COMPLETE FLOW

### Test Scenario 1: New Customer Signup

```bash
# 1. Create test customer via API
python3 -c "
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv('.env.admin')

url = 'https://azffej-as.myshopify.com/admin/api/2024-10/graphql.json'
headers = {
    'X-Shopify-Access-Token': os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN'),
    'Content-Type': 'application/json'
}

mutation = '''
mutation {
  customerCreate(input: {
    email: \"test.loyalty@example.com\"
    firstName: \"Test\"
    lastName: \"Loyalty\"
  }) {
    customer { id email }
  }
}
'''

response = requests.post(url, headers=headers, json={'query': mutation})
print(json.dumps(response.json(), indent=2))
"

# 2. Check points balance
python3 loyalty_manager.py balance test.loyalty@example.com

# Expected: 50 points (signup bonus)
```

### Test Scenario 2: Purchase Points

```bash
# Award 150 points for $150 purchase
python3 loyalty_manager.py add test.loyalty@example.com 150 purchase

# Check balance
python3 loyalty_manager.py balance test.loyalty@example.com

# Expected: 200 points (50 signup + 150 purchase)
```

### Test Scenario 3: Tier Upgrade

```bash
# Add 350 more points (total = 550 → Silver tier)
python3 loyalty_manager.py add test.loyalty@example.com 350 purchase

# Check balance
python3 loyalty_manager.py balance test.loyalty@example.com

# Expected: 550 points, Silver tier
```

### Test Scenario 4: Redemption

```bash
# Redeem 100 points
python3 loyalty_manager.py redeem test.loyalty@example.com 100

# Expected output:
# ✅ Redemption complete!
# Code: LOYALTY100-XXXXXXX
# Value: $5 OFF
# New balance: 450 points
```

### Test Scenario 5: Transaction History

```bash
# Get history
python3 loyalty_manager.py history test.loyalty@example.com

# Expected: 4 transactions
# 1. Signup bonus (+50)
# 2. Purchase (+150)
# 3. Purchase (+350)
# 4. Redemption (-100)
```

---

## STEP 7: PRODUCTION DEPLOYMENT (DONE)

### Files Already Deployed

✅ **Liquid Templates:**
- `snippets/loyalty-points-widget.liquid` - Full dashboard
- `snippets/loyalty-points-badge.liquid` - Cart drawer compact
- `snippets/loyalty-redemption-form.liquid` - Redemption UI
- `snippets/loyalty-history.liquid` - Transaction history
- `sections/main-account.liquid` - Integration (lines 28-29)
- `snippets/cart-drawer.liquid` - Integration (line 80)

✅ **Python Scripts:**
- `loyalty_setup.py` - One-time metafield setup
- `loyalty_manager.py` - CLI management tool

✅ **Google Apps Scripts:**
- `loyalty_webhooks.gs` - Webhook handlers (needs deployment)
- `loyalty_redemption_api.gs` - Redemption API (needs deployment)

### Pages Live

- Account page: https://www.alphamedical.shop/account
  - Full loyalty dashboard
  - Redemption form
  - Transaction history

- Cart drawer: (opens when adding to cart)
  - Compact points badge
  - Tier display

---

## 📊 EARNING RULES SUMMARY

| Action | Points | Auto/Manual |
|--------|--------|-------------|
| Account signup | 50 | Auto (webhook) |
| Purchase | 1 per $1 | Auto (webhook) |
| Product review | 100 | Manual* |
| Referral | 200 | Manual* |

*Requires additional webhook setup (Loox integration for reviews, referral tracking)

---

## 💰 REDEMPTION TIERS

| Points | Discount | Bonus | Total Value |
|--------|----------|-------|-------------|
| 100 | $5 | $0 | $5 |
| 200 | $12 | **+$2** | $12 |
| 500 | $35 | **+$10** | $35 |
| 1000 | $80 | **+$20** | $80 |

---

## 🏆 TIER SYSTEM

### Bronze (0-500 points)
- Birthday reward
- Exclusive deals

### Silver (501-1,500 points)
- All Bronze benefits
- Early access to new products
- Free shipping on all orders

### Gold (1,501+ points)
- All Silver benefits
- VIP support (priority response)
- 2x points on purchases

---

## 🔧 TROUBLESHOOTING

### Issue: "Customer not found" error

**Cause:** Customer API access denied (Basic plan)
**Fix:** Upgrade to Shopify plan ($79/month)

### Issue: Metafields not showing in Liquid

**Cause:** Metafield definitions not created
**Fix:** Run `python3 loyalty_setup.py`

### Issue: Signup bonus not awarded

**Cause:** Webhook not configured or failing
**Fix:**
1. Check webhook status in Shopify Admin
2. Check Apps Script execution log for errors
3. Verify webhook URL is correct

### Issue: Points not updating

**Cause:** Webhook handler error
**Fix:**
1. Check Apps Script execution log
2. Verify Admin API token is valid
3. Test manually: `python3 loyalty_manager.py add EMAIL POINTS ACTION`

### Issue: Redemption button does nothing

**Cause:** Apps Script URL not configured
**Fix:** Update URL in `snippets/loyalty-redemption-form.liquid` (line 75)

---

## 📈 MONITORING & ANALYTICS

### Check Loyalty Stats

```bash
# Get all loyalty data for customer
python3 loyalty_manager.py balance customer@example.com

# View transaction history
python3 loyalty_manager.py history customer@example.com 50
```

### Apps Script Execution Log

1. Go to: Apps Script project → Executions
2. View real-time webhook processing
3. Check for errors

### Shopify Webhook Status

1. Go to: Settings → Notifications → Webhooks
2. Click on webhook
3. View "Recent deliveries"
4. Check response codes (200 = success)

---

## 🚀 NEXT STEPS (Optional Enhancements)

### Email Notifications (Klaviyo)

**Tier Upgrade Email:**
- Trigger: When tier changes (silver/gold)
- Template: Congratulations email
- Integration: Add Klaviyo call to `loyalty_webhooks.gs`

**Redemption Confirmation:**
- Trigger: After successful redemption
- Template: Discount code + instructions
- Integration: Add to `loyalty_redemption_api.gs`

### Product Review Points

**Setup:**
1. Install Loox app (if not already)
2. Configure Loox webhook: https://YOUR_APPS_SCRIPT_URL?topic=reviews/create
3. Update `loyalty_webhooks.gs` with review handler

### Referral Points

**Setup:**
1. Create referral tracking (discount codes with tags)
2. Configure Shopify Flow:
   - Trigger: Order created with referral tag
   - Action: HTTP request to loyalty_manager.py

### Admin Dashboard

**Features:**
- Total loyalty program metrics
- Points issued/redeemed
- Tier distribution
- Top customers

**Implementation:** Google Sheets + Apps Script data aggregation

---

## 💰 COST ANALYSIS

| Item | Cost | Frequency |
|------|------|-----------|
| Shopify Plan Upgrade | +$50 | Monthly |
| Google Apps Script | $0 | Free tier |
| Development Time | 0h | Already done |
| **Total** | **$50/month** | **$600/year** |

**vs App Alternative:**
- Smile.io: $49-$599/month ($588-$7,188/year)
- **Savings:** $538-$6,588/year with custom system

**Additional Benefits of Shopify Plan:**
- Professional reports
- Staff accounts (5)
- International domains
- Better shipping rates

---

## ✅ VERIFICATION CHECKLIST

After setup complete, verify:

- [ ] Customer metafields visible in Shopify Admin
- [ ] Signup bonus awarded to new customers (50 points)
- [ ] Purchase points awarded on paid orders (1pt/$1)
- [ ] Account page shows loyalty dashboard
- [ ] Cart drawer shows points badge
- [ ] Tier calculation accurate
- [ ] Redemption creates discount codes
- [ ] Discount codes work at checkout
- [ ] Transaction history displays correctly
- [ ] Webhooks processing successfully

---

## 📞 SUPPORT

**Issues?** Check:
1. This guide (troubleshooting section)
2. Apps Script execution logs
3. Shopify webhook delivery logs
4. Test with CLI: `python3 loyalty_manager.py`

**All files location:** `/Users/mac/Desktop/Alpha-Medical/`

---

**SETUP GUIDE VERSION:** 1.0
**LAST UPDATED:** 2025-11-15
**STATUS:** ✅ Ready for deployment (after plan upgrade)
