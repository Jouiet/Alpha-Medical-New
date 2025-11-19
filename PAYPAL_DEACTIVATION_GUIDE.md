# PayPal Désactivation - Guide Manuel

**Date:** 2025-11-19  
**Requirement:** "PAS de PayPal!!" (only Shopify Payments: Stripe + Google Pay + Apple Pay)  
**Status:** ⚠️ ACTION MANUELLE REQUISE

---

## 🚨 CRITICAL REQUIREMENT VIOLATION

**Current State:** PayPal V4 is ACTIVE on the store  
**Required State:** PayPal DISABLED (only Shopify Payments + portable wallets)

**Evidence (from forensic audit 2025-10-30):**
```javascript
window.ShopifyPaypalV4VisibilityTracking = true;
// Source: Homepage HTML inspection
```

---

## WHY MANUAL ACTION IS REQUIRED

**Technical Limitation:** Payment provider settings are **NOT accessible via Shopify Admin REST API**.

**API Capabilities:**
- ✅ Can READ payment gateway list (limited info)
- ❌ CANNOT modify payment settings
- ❌ CANNOT enable/disable PayPal
- ❌ CANNOT configure provider settings

**Only Solution:** Manual configuration via Shopify Admin UI

---

## STEP-BY-STEP DEACTIVATION PROCESS

### Step 1: Access Payment Settings

1. **Login to Shopify Admin:** https://admin.shopify.com/store/azffej-as
2. **Navigate:** Settings (bottom left) → Payments
3. **Expected view:** Payment providers section showing:
   - Shopify Payments (active)
   - PayPal (active)
   - Other payment methods (if any)

---

### Step 2: Locate PayPal Provider

**Look for section titled:**
- "Third-party providers" OR
- "Alternative payment methods" OR
- "Additional payment methods"

**PayPal entry will show:**
- Provider name: "PayPal" or "PayPal Express Checkout"
- Status: Active (green dot or "Active" label)
- Actions: "Manage" or "Deactivate" button

---

### Step 3: Deactivate PayPal

**Option A: If "Deactivate" button is visible**
1. Click "Deactivate" button next to PayPal
2. Confirmation modal appears: "Are you sure you want to deactivate PayPal?"
3. Click "Deactivate" to confirm
4. Wait for success message: "PayPal has been deactivated"

**Option B: If "Manage" button is shown**
1. Click "Manage" button next to PayPal
2. In settings panel, find "Status" or "Activation" toggle
3. Set toggle to "Inactive" or "Disabled"
4. Click "Save" at bottom of panel
5. Wait for success message

---

### Step 4: Verify Deactivation

**Verification Steps:**

1. **In Shopify Admin (Settings → Payments):**
   - ✅ PayPal should show "Inactive" or be removed from list
   - ✅ Only Shopify Payments should be active under "Payment providers"

2. **On Live Store (https://www.alphamedical.shop):**
   - Add product to cart
   - Go to checkout: `/checkout`
   - **Expected:** Only see:
     - Credit/Debit card fields (Shopify Payments/Stripe)
     - Google Pay button (if wallet enabled)
     - Apple Pay button (if wallet enabled)
   - **NOT Expected:**
     - ❌ NO PayPal button
     - ❌ NO "Pay with PayPal" option

3. **In Browser DevTools (Console):**
   ```javascript
   // Check for PayPal tracking variable
   console.log(window.ShopifyPaypalV4VisibilityTracking);
   // Expected: undefined (or false)
   // NOT: true
   ```

4. **In Page Source (View Source):**
   - Search for: "paypal" (case-insensitive)
   - **Expected:** NO matches or only historical references
   - **NOT Expected:** Active PayPal scripts or tracking

---

## VERIFICATION CHECKLIST

After deactivation, verify ALL of the following:

- [ ] Shopify Admin → Settings → Payments shows PayPal as "Inactive"
- [ ] Live checkout page shows NO PayPal button
- [ ] Live checkout page ONLY shows:
  - [ ] Credit/Debit card fields
  - [ ] Google Pay button (optional)
  - [ ] Apple Pay button (optional)
- [ ] Browser console shows `ShopifyPaypalV4VisibilityTracking = undefined` (not `true`)
- [ ] Page source has NO active PayPal scripts

---

## TROUBLESHOOTING

### Issue 1: "Deactivate" button is grayed out

**Cause:** PayPal might be set as default payment method

**Solution:**
1. Go to Settings → Payments
2. Find "Default payment method" section
3. Change default to "Shopify Payments"
4. Save changes
5. Return to PayPal and try deactivating again

---

### Issue 2: PayPal still appears on checkout after deactivation

**Cause:** Browser cache or Shopify cache not cleared

**Solution:**
1. Clear browser cache (Ctrl+Shift+Del / Cmd+Shift+Del)
2. Open checkout in **Incognito/Private window**
3. If still shows: Wait 5-10 minutes for Shopify cache to clear
4. If persists after 1 hour: Contact Shopify Support

---

### Issue 3: Cannot find PayPal in Payment Settings

**Possible Reasons:**
- PayPal might already be deactivated (check checkout to confirm)
- PayPal might be under different section (check "Alternative methods")
- Different plan might organize settings differently

**Verification:**
1. Test checkout as customer
2. If PayPal button shows → It's still active (contact Shopify Support)
3. If NO PayPal button → Already deactivated (✅ done)

---

## POST-DEACTIVATION ACTIONS

### 1. Update Payment Policy Page

**File:** `templates/page.refund-policy.liquid` or similar

**Find and remove/update:**
```html
<!-- Remove PayPal-specific refund policies -->
<p>PayPal refunds processed within 5-7 business days...</p>
```

**Replace with:**
```html
<p>Refunds processed to original payment method (credit/debit card) within 5-7 business days after approval.</p>
```

---

### 2. Update FAQ/Support Pages

**Search for PayPal mentions in:**
- FAQ page
- Shipping & Returns policy
- Contact us page
- Email templates

**Update to reference only:**
- Credit/Debit cards (Visa, Mastercard, Amex, etc.)
- Google Pay
- Apple Pay

---

### 3. Email Customer Service

**If you receive PayPal-related customer inquiries after deactivation:**

**Email Template:**
```
Subject: Payment Methods Update - Alpha Medical Care

Dear [Customer Name],

Thank you for your inquiry about PayPal payments.

As of [Deactivation Date], Alpha Medical Care no longer accepts PayPal as a payment method. We now exclusively use Shopify Payments for all transactions, which provides:

✅ Faster checkout process
✅ Enhanced security (256-bit SSL encryption)
✅ Support for Google Pay and Apple Pay
✅ All major credit and debit cards accepted

We apologize for any inconvenience. If you have concerns about this change, please don't hesitate to reach out.

Best regards,
Alpha Medical Care Support Team
```

---

## COMPLIANCE VERIFICATION

**Requirement:** "shopify payment: stripe + Google Pay + Apple Pay). (PAS de PayPal!!)"

**Final Check:**
- ✅ Shopify Payments active (uses Stripe backend)
- ✅ Google Pay enabled (via portable wallets)
- ✅ Apple Pay enabled (via portable wallets)
- ❌ PayPal DISABLED (no longer visible)

**Status:** ✅ COMPLIANT once PayPal deactivated

---

## DOCUMENTATION UPDATE

After completing deactivation, update the following documentation:

1. `SEO_MARKETING_FORENSIC_ANALYSIS.md`:
   - Change line ~186: `| **Payment - PayPal** | ❌ ACTIVE | ... | ❌ VIOLATION |`
   - To: `| **Payment - PayPal** | ✅ DISABLED | Deactivated 2025-11-XX | ✅ COMPLIANT |`

2. Create verification script (optional):
   - File: `verify_paypal_disabled.py`
   - Fetch homepage HTML
   - Check for `ShopifyPaypalV4VisibilityTracking`
   - Report: DISABLED if `undefined`, ACTIVE if `true`

---

## ESTIMATED TIME

- **Deactivation:** 2-5 minutes (manual UI)
- **Verification:** 5-10 minutes (checkout test + source check)
- **Documentation update:** 5 minutes
- **Total:** ~15-20 minutes

---

## SUPPORT CONTACT

If you encounter issues not covered in this guide:

**Shopify Support:**
- URL: https://help.shopify.com/en/support
- Chat: Available in Shopify Admin bottom right corner
- Phone: 1-855-816-3857 (US toll-free)

**Issue to Report:** "Need help deactivating PayPal payment provider"

---

**Status:** ⏳ MANUAL ACTION REQUIRED  
**Priority:** 🔴 CRITICAL (requirement violation)  
**Blocker:** Cannot be automated via API

**Last Updated:** 2025-11-19
