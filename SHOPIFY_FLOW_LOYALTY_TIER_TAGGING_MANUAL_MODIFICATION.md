# SHOPIFY FLOW - Loyalty Tier Tagging Manual Modification Guide

**Status:** REQUIRES MANUAL UI CONFIGURATION (Shopify Flow has no public API)
**Task:** Add "Remove customer tag" actions to prevent tag accumulation
**Workflow:** "New Loyalty Tier Tagging (Automatic)"
**Date Created:** 2025-12-03
**Estimated Time:** 10 minutes

---

## Problem Statement

**Current Behavior:**
- When a customer upgrades from Bronze → Silver → Gold, old tier tags (bronze, silver) are NOT removed
- Customer accumulates ALL tier tags: `bronze`, `silver`, `gold`
- Creates segmentation issues in email marketing (customer receives emails for multiple tiers)

**Desired Behavior:**
- Only ONE tier tag per customer at any time
- Old tier tag is REMOVED before new tier tag is added
- Customer profile shows only current tier: `gold` (not `bronze, silver, gold`)

---

## Current Workflow Structure

**Workflow Name:** New Loyalty Tier Tagging (Automatic)
**Trigger:** Order paid
**Current Actions:**
1. Check customer's total spend
2. **If spend ≥ $1000:** Add tag `gold`
3. **Else if spend ≥ $500:** Add tag `silver`
4. **Else if spend ≥ $100:** Add tag `bronze`

**Problem:** No removal of previous tier tags before adding new one.

---

## Required Modification Steps

### Step 1: Navigate to Workflow Editor
1. Go to: Shopify Admin → Apps → **Flow**
2. Click on workflow: **"New Loyalty Tier Tagging (Automatic)"**
3. You will see the workflow canvas with trigger and actions

### Step 2: Locate Existing "Add customer tag" Actions
- There should be 3 conditional branches (Bronze, Silver, Gold)
- Each branch has an **"Add customer tag"** action

### Step 3: Add "Remove customer tag" Actions BEFORE Each "Add" Action

#### For GOLD Tier (≥$1000 spent):
**BEFORE** the existing "Add customer tag: gold" action, insert:
1. Action: **Remove customer tag**
   - Tag to remove: `bronze`
2. Action: **Remove customer tag**
   - Tag to remove: `silver`
3. **THEN** existing action: **Add customer tag: gold**

#### For SILVER Tier ($500-$999 spent):
**BEFORE** the existing "Add customer tag: silver" action, insert:
1. Action: **Remove customer tag**
   - Tag to remove: `bronze`
2. Action: **Remove customer tag**
   - Tag to remove: `gold` (in case of downgrade)
3. **THEN** existing action: **Add customer tag: silver**

#### For BRONZE Tier ($100-$499 spent):
**BEFORE** the existing "Add customer tag: bronze" action, insert:
1. Action: **Remove customer tag**
   - Tag to remove: `silver` (in case of downgrade)
2. Action: **Remove customer tag**
   - Tag to remove: `gold` (in case of downgrade)
3. **THEN** existing action: **Add customer tag: bronze**

### Step 4: Save Workflow
1. Click **"Save"** in top-right corner
2. Workflow will remain **Active** (no need to reactivate)
3. Changes take effect immediately for next order

---

## Modified Workflow Logic

```
Trigger: Order paid
├─ Get customer's total spend
├─ Condition: If spend ≥ $1000
│   ├─ Remove customer tag: bronze
│   ├─ Remove customer tag: silver
│   └─ Add customer tag: gold
├─ Condition: Else if spend ≥ $500
│   ├─ Remove customer tag: bronze
│   ├─ Remove customer tag: gold
│   └─ Add customer tag: silver
└─ Condition: Else if spend ≥ $100
    ├─ Remove customer tag: silver
    ├─ Remove customer tag: gold
    └─ Add customer tag: bronze
```

---

## Verification Steps

### Test Scenario 1: Customer Upgrade (Bronze → Silver)
1. Create test customer with tag `bronze`
2. Place order that brings total spend to $550
3. **Expected result:** Customer has ONLY `silver` tag (no `bronze`)

### Test Scenario 2: Customer Upgrade (Silver → Gold)
1. Create test customer with tag `silver`
2. Place order that brings total spend to $1,200
3. **Expected result:** Customer has ONLY `gold` tag (no `silver`)

### Test Scenario 3: New Customer (Direct to Gold)
1. Create new customer with no tags
2. Place order worth $1,500
3. **Expected result:** Customer has ONLY `gold` tag

---

## Technical Notes

### Why Manual Configuration?
- **Shopify Flow has NO public API** for workflow configuration
- All workflow modifications must be done via Shopify Admin UI
- Cannot be scripted or automated via API calls

### Alternative Approaches Considered
1. **Shopify Admin API (GraphQL):** Can add/remove tags directly via API, but requires:
   - Scheduled script running every day
   - More complex than native Flow workflow
   - Duplicates logic that Flow already handles
2. **Third-party automation tools:** Require additional apps (violates "no new apps" constraint)

### Why This is the Best Solution
- ✅ Native Shopify Flow (already activated, zero cost)
- ✅ Real-time execution on every order
- ✅ Zero maintenance after setup
- ✅ No additional dependencies

---

## Impact Assessment

**Before Modification:**
- Customer with $1,200 lifetime spend has tags: `bronze, silver, gold`
- Receives 3 separate email campaigns (Bronze welcome, Silver perks, Gold benefits)
- Creates confusion and potential unsubscribes

**After Modification:**
- Same customer has ONLY tag: `gold`
- Receives ONLY Gold tier email campaigns
- Clear segmentation for marketing automation

---

## Additional Resources

- [Shopify Flow Documentation: Remove customer tag](https://help.shopify.com/en/manual/shopify-flow/actions#remove-a-customer-tag)
- [Shopify Flow: Customer Segmentation Best Practices](https://help.shopify.com/en/manual/customers/customer-segmentation)

---

**Created by:** Claude Code Session 75
**Reason for Manual Configuration:** Shopify Flow API limitation (UI-only configuration)
**Priority:** MEDIUM (affects email segmentation quality, not critical for pre-launch)
