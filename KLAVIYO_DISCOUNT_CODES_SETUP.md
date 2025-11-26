# KLAVIYO FLOWS - DISCOUNT CODES SETUP
## Pre-requisites for 4 Flows Deployment

**Date:** 2025-11-26 Session 56+
**Objective:** Create 2 discount codes for Klaviyo flows (WINBACK15, REVIEW10)

---

## ✅ EXISTING DISCOUNT CODE

### WELCOME10 (Already Created)
```yaml
Code: WELCOME10
Type: Percentage
Value: 10% OFF
Usage: Welcome Series flow (Shopify Email + Klaviyo)
Status: ✅ ACTIVE
Created: 2025-11-26 Session 56
```

---

## 📋 NEW DISCOUNT CODES TO CREATE (2)

### 1. WINBACK15 - Customer Winback Flow

**Purpose:** Re-activate lapsed customers (60+ days no purchase)

**Shopify Settings:**
```yaml
Discount Code: WINBACK15
Discount Type: Percentage
Percentage: 15%

Applies to:
  ☑ Entire order (all products)

Minimum Requirements:
  ○ None (no minimum purchase)
  Reason: Remove friction for lapsed customers

Customer Eligibility:
  ☑ All customers
  Note: Klaviyo flow will target "Opportunités de reconquête" segment only

Usage Limits:
  ☑ Limit number of times this discount can be used in total: 1000
  Reason: Control budget (max $15,000 discount impact if all used)

  ☑ Limit to one use per customer: YES
  Reason: One-time winback incentive per customer

Active Dates:
  Start date: 2025-11-27 (tomorrow - flow deployment day)
  End date: None (ongoing)
  Reason: Always available for winback flow

Combinations:
  ☐ Can't combine with other discounts
  Reason: Single discount for winback clarity
```

**Usage in Klaviyo Flow:**
```
Flow: "Customer Winback - Standard (Email & SMS)"
Placement: Email 1 (Day 60) - "We miss you! Here's 15% OFF"
Message: "Use code WINBACK15 at checkout for 15% off your entire order"
CTA: "Claim Your 15% OFF"
```

---

### 2. REVIEW10 - Product Review Incentive Flow

**Purpose:** Encourage product reviews + repeat purchase after first order

**Shopify Settings:**
```yaml
Discount Code: REVIEW10
Discount Type: Percentage
Percentage: 10%

Applies to:
  ☑ Entire order (all products)

Minimum Requirements:
  ○ None (no minimum purchase)
  Reason: Incentive for review, not sales threshold

Customer Eligibility:
  ☑ All customers
  Note: Klaviyo flow will target "Placed Order" event only

Usage Limits:
  ☑ Limit number of times this discount can be used in total: 2000
  Reason: Control budget (max $10,000 discount impact if all used)

  ☑ Limit to one use per customer: YES
  Reason: One-time review incentive per customer

Active Dates:
  Start date: 2025-11-27 (tomorrow - flow deployment day)
  End date: None (ongoing)
  Reason: Always available for review flow

Combinations:
  ☐ Can't combine with other discounts
  Reason: Single discount for review clarity
```

**Usage in Klaviyo Flow:**
```
Flow: "Product Review / Cross-Sell - Standard (Email & SMS)"
Placement: Email 1 (7-10 days after purchase) - Review request
Message: "Leave a 5-star review and get 10% OFF your next order with code REVIEW10"
CTA: "Write a Review & Get 10% OFF"
```

---

## 🔧 MANUAL CREATION STEPS (Shopify Admin)

### Step 1: Navigate to Discounts
```
1. Shopify Admin: https://admin.shopify.com/store/azffej-as
2. Left menu: Discounts
3. Click: "Create discount"
```

### Step 2: Create WINBACK15
```
1. Select: "Discount code"
2. Discount code: WINBACK15
3. Type: Percentage
4. Value: 15
5. Applies to: Entire order
6. Minimum requirements: None
7. Customer eligibility: All customers
8. Usage limits:
   ☑ Limit number of times: 1000
   ☑ Limit to one use per customer: YES
9. Active dates:
   Start: 2025-11-27
   End: (leave blank)
10. Click: "Save discount"
```

### Step 3: Create REVIEW10
```
1. Discounts → "Create discount"
2. Select: "Discount code"
3. Discount code: REVIEW10
4. Type: Percentage
5. Value: 10
6. Applies to: Entire order
7. Minimum requirements: None
8. Customer eligibility: All customers
9. Usage limits:
   ☑ Limit number of times: 2000
   ☑ Limit to one use per customer: YES
10. Active dates:
    Start: 2025-11-27
    End: (leave blank)
11. Click: "Save discount"
```

### Step 4: Verify Codes Created
```
1. Shopify Admin → Discounts
2. Verify list shows:
   - WELCOME10 ✅ (existing)
   - WINBACK15 ✅ (new)
   - REVIEW10 ✅ (new)
3. Test each code:
   - Add product to cart
   - Apply discount code at checkout
   - Verify discount applies correctly
```

---

## 🤖 ALTERNATIVE: API CREATION (Script)

**If you prefer automated creation via Shopify API:**

```python
#!/usr/bin/env python3
# File: create_klaviyo_discount_codes.py

import requests
import json
from datetime import datetime, timedelta

# Load from .env.admin
with open('.env.admin', 'r') as f:
    for line in f:
        if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
            SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
        elif line.startswith('SHOPIFY_STORE_DOMAIN='):
            SHOPIFY_STORE = line.split('=', 1)[1].strip()

SHOPIFY_API = f"https://{SHOPIFY_STORE}/admin/api/2024-10"
headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# Tomorrow's date for start
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

# Discount Code #1: WINBACK15
winback_data = {
    "price_rule": {
        "title": "WINBACK15 - Customer Winback 15% OFF",
        "target_type": "line_item",
        "target_selection": "all",
        "allocation_method": "across",
        "value_type": "percentage",
        "value": "-15.0",
        "customer_selection": "all",
        "starts_at": f"{tomorrow}T00:00:00Z",
        "usage_limit": 1000,
        "once_per_customer": True
    }
}

print("Creating WINBACK15 price rule...")
r = requests.post(f"{SHOPIFY_API}/price_rules.json",
                  headers=headers,
                  data=json.dumps(winback_data))

if r.status_code == 201:
    price_rule_id = r.json()['price_rule']['id']
    print(f"✅ Price rule created: {price_rule_id}")

    # Create discount code
    code_data = {
        "discount_code": {
            "code": "WINBACK15"
        }
    }

    r2 = requests.post(f"{SHOPIFY_API}/price_rules/{price_rule_id}/discount_codes.json",
                       headers=headers,
                       data=json.dumps(code_data))

    if r2.status_code == 201:
        print(f"✅ WINBACK15 code created successfully")
    else:
        print(f"❌ Error creating code: {r2.status_code} - {r2.text}")
else:
    print(f"❌ Error creating price rule: {r.status_code} - {r.text}")

print("\n" + "="*50 + "\n")

# Discount Code #2: REVIEW10
review_data = {
    "price_rule": {
        "title": "REVIEW10 - Product Review 10% OFF",
        "target_type": "line_item",
        "target_selection": "all",
        "allocation_method": "across",
        "value_type": "percentage",
        "value": "-10.0",
        "customer_selection": "all",
        "starts_at": f"{tomorrow}T00:00:00Z",
        "usage_limit": 2000,
        "once_per_customer": True
    }
}

print("Creating REVIEW10 price rule...")
r = requests.post(f"{SHOPIFY_API}/price_rules.json",
                  headers=headers,
                  data=json.dumps(review_data))

if r.status_code == 201:
    price_rule_id = r.json()['price_rule']['id']
    print(f"✅ Price rule created: {price_rule_id}")

    # Create discount code
    code_data = {
        "discount_code": {
            "code": "REVIEW10"
        }
    }

    r2 = requests.post(f"{SHOPIFY_API}/price_rules/{price_rule_id}/discount_codes.json",
                       headers=headers,
                       data=json.dumps(code_data))

    if r2.status_code == 201:
        print(f"✅ REVIEW10 code created successfully")
    else:
        print(f"❌ Error creating code: {r2.status_code} - {r2.text}")
else:
    print(f"❌ Error creating price rule: {r.status_code} - {r.text}")

print("\n" + "="*50)
print("Summary:")
print("- WINBACK15: 15% OFF, limit 1000 uses, once per customer")
print("- REVIEW10: 10% OFF, limit 2000 uses, once per customer")
print("="*50)
```

**To run script:**
```bash
chmod +x create_klaviyo_discount_codes.py
python3 create_klaviyo_discount_codes.py
```

---

## 📊 DISCOUNT CODES SUMMARY

```yaml
Total Codes for Klaviyo Flows: 3

1. WELCOME10 (Existing):
   - Flow: Welcome Series - Final Email Discount
   - Value: 10% OFF
   - Usage: Unlimited
   - Status: ✅ ACTIVE

2. WINBACK15 (New):
   - Flow: Customer Winback - Standard (Email & SMS)
   - Value: 15% OFF
   - Usage: 1000 max, once per customer
   - Budget Impact: Max $15,000 if all used
   - Status: ⏳ TO CREATE

3. REVIEW10 (New):
   - Flow: Product Review / Cross-Sell - Standard (Email & SMS)
   - Value: 10% OFF
   - Usage: 2000 max, once per customer
   - Budget Impact: Max $10,000 if all used
   - Status: ⏳ TO CREATE
```

---

## ✅ VERIFICATION CHECKLIST

After creating codes:

- [ ] WINBACK15 appears in Shopify Admin → Discounts
- [ ] REVIEW10 appears in Shopify Admin → Discounts
- [ ] Test WINBACK15: Add product to cart, apply code, verify 15% discount
- [ ] Test REVIEW10: Add product to cart, apply code, verify 10% discount
- [ ] Codes visible in Klaviyo discount code selector (when creating flows)
- [ ] Document creation in INFRASTRUCTURE_AUDIT_CHECKLIST.md

**Time Required:** 5 minutes (manual) OR 2 minutes (script)

---

**Created:** 2025-11-26 Session 56+
**Ready for:** Klaviyo flows deployment (3-4h after codes created)
