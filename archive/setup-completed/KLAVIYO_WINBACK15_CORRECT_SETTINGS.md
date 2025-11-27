# WINBACK15 - CORRECTIONS CONFIGURATION

**Current Settings (INCORRECT):**
```yaml
❌ Applies to: Specific collections (empty - NO collections selected)
❌ Maximum discount uses: No usage limits
```

**Problem:**
- "Specific collections" but NONE selected = Code will NOT work on ANY product
- No usage limits = Unlimited discount budget risk

---

## ✅ CORRECT SETTINGS FOR WINBACK15

### Change #1: Applies to
```yaml
BEFORE: ○ Specific collections (none selected) ❌
AFTER:  ● All products ✅

Action: Click "All products" radio button
Reason: Winback should apply to entire order (all products)
```

### Change #2: Maximum discount uses
```yaml
BEFORE: No usage limits ❌
AFTER:
  ☑ Limit number of times this discount can be used in total: 1000
  ☑ Limit to one use per customer: YES ✅

Action:
  1. Check "Limit number of times this discount can be used in total"
  2. Enter: 1000
  3. Check "Limit to one use per customer"

Reason:
  - Budget control: Max 1000 uses = ~$15,000 discount impact max
  - One per customer: Prevents abuse, true "winback" incentive
```

### Change #3: Start Date (Optional but recommended)
```yaml
CURRENT: 2025-11-26 (today) 3:49 PM EST
RECOMMENDED: 2025-11-27 (tomorrow) 12:00 AM EST

Reason: Start when Klaviyo flow is deployed (not before)
Action: Change start date to 2025-11-27, time to 12:00 AM
```

---

## ✅ COMPLETE CORRECT CONFIGURATION

```yaml
Discount Code: WINBACK15

Discount value:
  Type: Percentage
  Value: 15%

Applies to:
  ● All products ✅ (CHANGE THIS - currently wrong)

Purchase type:
  ● One-time purchase ✅ (correct)

Eligibility:
  ● All customers ✅ (correct)

Minimum purchase requirements:
  ● No minimum requirements ✅ (correct)

Maximum discount uses:
  ☑ Limit number of times: 1000 ✅ (ADD THIS)
  ☑ Limit to one use per customer: YES ✅ (ADD THIS)

Combinations:
  ☐ Can't combine with other discounts ✅ (correct)

Active dates:
  Start: 2025-11-27 12:00 AM EST (recommended)
  End: (no end date) ✅ (correct)
```

---

## 🔧 QUICK FIX STEPS

1. **Fix "Applies to":**
   - Click radio button: **"All products"**
   - Remove "Specific collections" selection

2. **Add usage limits:**
   - Check: ☑ "Limit number of times this discount can be used in total"
   - Enter: **1000**
   - Check: ☑ "Limit to one use per customer"

3. **(Optional) Adjust start date:**
   - Change to: **2025-11-27**
   - Time: **12:00 AM EST**

4. **Save:**
   - Click "Save discount" button

---

## ✅ VERIFICATION

After saving, summary should show:
```
WINBACK15
Code

Type: Amount off products
Details:
  - All customers
  - 15% off all products ✅ (not "collections")
  - Applies to one-time purchases
  - No minimum purchase requirement
  - Limit: 1000 uses, once per customer ✅
  - Can't combine with other discounts
  - Active from Nov 27, 2025
```

---

**CRITICAL:** Sans ces corrections, le code WINBACK15 ne fonctionnera sur AUCUN produit (collections vides = 0 products).

**Time to fix:** 30 seconds
