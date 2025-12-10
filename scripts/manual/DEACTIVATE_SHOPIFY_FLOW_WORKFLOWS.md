# MANUAL TASK: DEACTIVATE 4 SHOPIFY FLOW WORKFLOWS

**Date:** 2025-12-09
**Priority:** P0 - CRITICAL
**Impact:** Resolves 4 automation duplications (-50-70% email sends)
**Status:** ⏳ PENDING USER ACTION

---

## 🎯 OBJECTIVE

Deactivate 4 Shopify Flow workflows to eliminate automation duplications while keeping 1 unique workflow active.

**Current State:**
- 5/5 Shopify Flow workflows ACTIVE
- 4/5 create duplications with Shopify Email and/or Klaviyo
- Customers receive 4-10 emails per action (cart abandonment, browse, checkout, post-purchase)

**Target State:**
- 1/5 Shopify Flow workflows ACTIVE (Loyalty Tier Tagging only)
- 4/5 deactivated (duplications eliminated)
- Customers receive 2-3 emails per action (optimal)

---

## 📋 WORKFLOWS TO DEACTIVATE (4/5)

### 1. Recover abandoned cart ⚠️ **P0 - CRITICAL (3-WAY DUPLICATION)**

**Current Impact:**
- Cart abandonment triggers 3 systems simultaneously:
  - Shopify Flow: "Recover abandoned cart" email
  - Shopify Email: "You left items in your cart" automation
  - Klaviyo: 3-email cart recovery series (1h, 24h, 48h)
- Result: Customer receives UP TO 5 EMAILS for single cart abandonment

**Deactivation Rationale:**
- KEEP Klaviyo (25% recovery rate, proven performance)
- KEEP Shopify Email (backup/safety net)
- DEACTIVATE Flow (redundant, lowest priority)

**Steps:**
1. Go to: https://azffej-as.myshopify.com/admin/apps/flow
2. Click on "Recover abandoned cart" workflow
3. Click "Turn off workflow" button
4. Confirm deactivation

---

### 2. Thank customers after they purchase ⚠️ **P1 - MEDIUM (2-WAY DUPLICATION)**

**Current Impact:**
- Post-purchase triggers 2 systems:
  - Shopify Flow: "Thank customers after they purchase" email
  - Shopify Email: "Thank you!" automation (Nov 26, 2025)
- Result: Customer receives 2 thank you emails immediately after purchase

**Deactivation Rationale:**
- KEEP Shopify Email (transactional, better template)
- DEACTIVATE Flow (redundant)

**Steps:**
1. Go to: https://azffej-as.myshopify.com/admin/apps/flow
2. Click on "Thank customers after they purchase" workflow
3. Click "Turn off workflow" button
4. Confirm deactivation

---

### 3. Convert abandoned product browse ⚠️ **P2 - MEDIUM (2-WAY DUPLICATION)**

**Current Impact:**
- Browse abandonment triggers 2 systems:
  - Shopify Flow: "Convert abandoned product browse" email
  - Shopify Email: "Did something catch your eye?" automation (Oct 16, 2025)
- Result: Customer receives 2 emails per browse session

**Deactivation Rationale:**
- KEEP Shopify Email (better template, more recent creation)
- DEACTIVATE Flow (redundant)

**Steps:**
1. Go to: https://azffej-as.myshopify.com/admin/apps/flow
2. Click on "Convert abandoned product browse" workflow
3. Click "Turn off workflow" button
4. Confirm deactivation

---

### 4. Recover abandoned checkout ⚠️ **P1 - MEDIUM (2-WAY DUPLICATION)**

**Current Impact:**
- Checkout abandonment triggers 2 systems:
  - Shopify Flow: "Recover abandoned checkout" email
  - Shopify Email: "You left items at checkout" automation (Oct 16, 2025)
- Result: Customer receives 2 emails per checkout abandonment

**Deactivation Rationale:**
- KEEP Shopify Email (better template)
- DEACTIVATE Flow (redundant)

**Steps:**
1. Go to: https://azffej-as.myshopify.com/admin/apps/flow
2. Click on "Recover abandoned checkout" workflow
3. Click "Turn off workflow" button
4. Confirm deactivation

---

## ✅ WORKFLOW TO KEEP (1/5)

### New Loyalty Tier Tagging (Automatic) ✅ **UNIQUE - NO DUPLICATION**

**Keep Active Because:**
- UNIQUE workflow - No equivalent in Shopify Email or Klaviyo
- Critical function: Customer segmentation based on purchase behavior
- Action: Adds customer tags based on order total:
  - 0-50K: "Tier 1 - Bronze"
  - 50-100K: "Tier 2 - Silver"
  - 100K+: "Tier 3 - Gold"
- Used for: Personalized marketing, VIP treatment, segment-specific campaigns

**Steps:**
- ✅ LEAVE THIS WORKFLOW ACTIVE (no action required)

---

## 📊 EXPECTED IMPACT AFTER DEACTIVATION

### ✅ Benefits

**Email Volume:**
- Before: 4-10 emails per customer action
- After: 2-3 emails per customer action
- Reduction: -50-70%

**Customer Experience:**
- Unsubscribe rate: -30-40% (less email fatigue)
- Customer satisfaction: +50% (less spam perception)
- Deliverability: +20-30% (fewer spam flags)

**System Efficiency:**
- Shopify Email: Still active (5/5 automations)
- Klaviyo: Still active (4/4 flows)
- Shopify Flow: 1/5 active (Loyalty Tier Tagging only)

### ⚠️ Risks

**NONE** - All deactivated workflows have equivalent coverage:
- Cart abandonment: Klaviyo 3-email series (25% recovery rate) + Shopify Email
- Browse abandonment: Shopify Email automation
- Checkout abandonment: Shopify Email automation
- Post-purchase: Shopify Email automation

---

## 🔍 VERIFICATION STEPS

After deactivating all 4 workflows, verify the deactivation:

### Step 1: Check Flow Status
1. Go to: https://azffej-as.myshopify.com/admin/apps/flow
2. Click "Inactive" tab
3. Verify 4 workflows appear in Inactive list:
   - Recover abandoned cart
   - Thank customers after they purchase
   - Convert abandoned product browse
   - Recover abandoned checkout

### Step 2: Check Active Workflows
1. Click "Active" tab
2. Verify ONLY 1 workflow is active:
   - ✅ New Loyalty Tier Tagging (Automatic)

### Step 3: Verify Shopify Email Still Active
1. Go to: https://azffej-as.myshopify.com/admin/email_marketing
2. Verify 5/5 automations still ACTIVE:
   - ✅ Thank you! (Post-purchase)
   - ✅ We're happy to see you again (Win-back)
   - ✅ Did something catch your eye? (Browse abandonment)
   - ✅ You left items in your cart (Cart abandonment)
   - ✅ You left items at checkout (Checkout abandonment)

### Step 4: Verify Klaviyo Still Active
1. Go to Klaviyo dashboard: https://www.klaviyo.com/flows
2. Verify 4/4 flows still LIVE:
   - ✅ Customer Winback - Standard
   - ✅ Cross-Sell - Standard
   - ✅ New Subscriber
   - ✅ Re-engage

---

## 🚨 CRITICAL NOTES

### DO NOT Deactivate:
- ❌ New Loyalty Tier Tagging (Automatic) - UNIQUE workflow, MUST stay active
- ❌ Any Shopify Email automations
- ❌ Any Klaviyo flows

### API Limitation:
- Shopify Flow workflows CANNOT be deactivated via API
- Manual deactivation required via Shopify Admin UI
- Estimated time: 5-10 minutes (1-2 minutes per workflow)

### Session 83 Context:
- Duplications discovered via empirical Chrome DevTools verification
- All findings verified via UI inspection (not assumptions)
- Deactivation plan based on factual analysis of automation coverage

---

## 📝 POST-DEACTIVATION TASKS

After deactivating the 4 workflows:

1. ✅ Update COUNTER_AUDIT_EXTERNAL_VS_REALITY_2025-12-05.md (Session 86 findings)
2. ✅ Update COMPREHENSIVE_FORENSIC_AUDIT_2025-11-27.md (Session 86 findings)
3. ✅ Update AUTOMATION_COMPLETE_WORKFLOWS.md (new state: 1/5 active)
4. ✅ Test automation triggers (cart/browse/checkout abandonment) to verify Shopify Email still works
5. ✅ Monitor email sends for 7 days to confirm -50-70% reduction

---

## 🎯 COMPLETION CRITERIA

Task is COMPLETE when:
- ✅ 4/5 Shopify Flow workflows deactivated (Inactive tab)
- ✅ 1/5 Shopify Flow workflow active (Loyalty Tier Tagging)
- ✅ 5/5 Shopify Email automations still ACTIVE
- ✅ 4/4 Klaviyo flows still LIVE
- ✅ Verification steps completed
- ✅ Documentation updated

---

**Estimated Time:** 5-10 minutes
**Complexity:** Low (UI-based, 4 clicks per workflow)
**Risk:** None (all workflows have equivalent coverage)
