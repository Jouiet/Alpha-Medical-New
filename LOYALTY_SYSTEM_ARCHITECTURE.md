# Loyalty System Architecture - Custom Build

**Date:** 2025-11-15
**Status:** In Development
**Type:** Native Shopify (Metafields + Flow + Functions)

---

## 1. CUSTOMER METAFIELDS STRUCTURE

### Namespace: `loyalty`

**Metafield Definitions (via Shopify Admin API):**

```json
{
  "metafields": [
    {
      "namespace": "loyalty",
      "key": "points",
      "type": "number_integer",
      "description": "Total loyalty points balance",
      "value": 0
    },
    {
      "namespace": "loyalty",
      "key": "tier",
      "type": "single_line_text_field",
      "description": "Customer tier: bronze, silver, gold",
      "value": "bronze"
    },
    {
      "namespace": "loyalty",
      "key": "history",
      "type": "json",
      "description": "Points transaction history",
      "value": "[]"
    },
    {
      "namespace": "loyalty",
      "key": "signup_bonus_claimed",
      "type": "boolean",
      "description": "Has customer claimed 50pt signup bonus",
      "value": false
    },
    {
      "namespace": "loyalty",
      "key": "lifetime_points_earned",
      "type": "number_integer",
      "description": "Total points earned (including redeemed)",
      "value": 0
    },
    {
      "namespace": "loyalty",
      "key": "lifetime_points_redeemed",
      "type": "number_integer",
      "description": "Total points redeemed",
      "value": 0
    }
  ]
}
```

---

## 2. EARNING RULES

### Rule 1: Signup Bonus (50 points)
**Trigger:** Customer account created
**Condition:** `loyalty.signup_bonus_claimed == false`
**Action:**
- Add 50 to `loyalty.points`
- Set `loyalty.signup_bonus_claimed = true`
- Add transaction to `loyalty.history`:
  ```json
  {
    "date": "2025-11-15T14:30:00Z",
    "action": "signup_bonus",
    "points": 50,
    "balance_after": 50
  }
  ```

**Implementation:** Shopify Flow workflow

---

### Rule 2: Purchase Points (1 point per $1 spent)
**Trigger:** Order paid (financial_status = "paid")
**Calculation:** `Math.floor(order.total_price / 100)`
**Action:**
- Add points to `loyalty.points`
- Add to `loyalty.lifetime_points_earned`
- Add transaction to `loyalty.history`:
  ```json
  {
    "date": "2025-11-15T15:45:00Z",
    "action": "purchase",
    "order_id": "#1234",
    "order_total": 15000,
    "points": 150,
    "balance_after": 200
  }
  ```

**Implementation:** Shopify Flow workflow + HTTP Request to script

---

### Rule 3: Product Review (100 points)
**Trigger:** Product review submitted (Loox webhook)
**Condition:** Review approved
**Action:**
- Add 100 to `loyalty.points`
- Add transaction to `loyalty.history`:
  ```json
  {
    "date": "2025-11-16T10:00:00Z",
    "action": "review",
    "product_id": 123456,
    "points": 100,
    "balance_after": 300
  }
  ```

**Implementation:** Webhook receiver (Google Apps Script or Shopify Function)

---

### Rule 4: Referral (200 points)
**Trigger:** Referred customer makes first purchase
**Condition:** Order contains referral tag/discount code
**Action:**
- Add 200 to referrer `loyalty.points`
- Add transaction to `loyalty.history`:
  ```json
  {
    "date": "2025-11-17T12:00:00Z",
    "action": "referral",
    "referred_customer_id": 987654,
    "points": 200,
    "balance_after": 500
  }
  ```

**Implementation:** Shopify Flow workflow (order tag detection)

---

## 3. TIER CALCULATION

**Automatic tier assignment based on points:**

```javascript
function calculateTier(points) {
  if (points >= 1501) return "gold";
  if (points >= 501) return "silver";
  return "bronze";
}
```

**Tier Benefits:**
- **Bronze (0-500):** Birthday reward, exclusive deals
- **Silver (501-1500):** + Early access, free shipping
- **Gold (1501+):** + VIP support, 2x points on purchases

**Tier Upgrade Trigger:**
- Automatically update `loyalty.tier` when points threshold crossed
- Send email notification (Klaviyo or Shopify Email)

---

## 4. REDEMPTION SYSTEM

### Redemption Tiers:
```
100 points = $5 OFF
200 points = $12 OFF (bonus $2 value)
500 points = $35 OFF (bonus $10 value)
1000 points = $80 OFF (bonus $20 value)
```

### Mechanism: Auto-Generated Discount Codes

**Workflow:**
1. Customer clicks "Redeem 100 points" on account page
2. HTTP Request to redemption script (Python/Apps Script)
3. Script:
   - Validates customer has sufficient points
   - Deducts points from `loyalty.points`
   - Creates Shopify discount code (Price Rule API):
     ```json
     {
       "price_rule": {
         "title": "LOYALTY100-CUSTOMER123",
         "target_type": "line_item",
         "target_selection": "all",
         "allocation_method": "across",
         "value_type": "fixed_amount",
         "value": "-5.00",
         "customer_selection": "prerequisite",
         "prerequisite_customer_ids": [123],
         "usage_limit": 1,
         "starts_at": "2025-11-15T00:00:00Z"
       }
     }
     ```
   - Returns discount code to customer
   - Adds redemption transaction to `loyalty.history`:
     ```json
     {
       "date": "2025-11-18T14:00:00Z",
       "action": "redemption",
       "points": -100,
       "discount_code": "LOYALTY100-CUSTOMER123",
       "discount_value": 5.00,
       "balance_after": 400
     }
     ```
4. Display discount code on account page
5. Send email with code (Klaviyo)

---

## 5. SHOPIFY API ENDPOINTS REQUIRED

### Admin API (via Python Script or Apps Script):

**Customer Metafields:**
```graphql
mutation CreateCustomerMetafield($input: CustomerInput!) {
  customerUpdate(input: $input) {
    customer {
      id
      metafields(first: 10) {
        edges {
          node {
            namespace
            key
            value
          }
        }
      }
    }
  }
}
```

**Price Rules (Discount Codes):**
```bash
POST /admin/api/2024-10/price_rules.json
POST /admin/api/2024-10/price_rules/{price_rule_id}/discount_codes.json
```

**Customer Query:**
```graphql
query GetCustomerLoyalty($customerId: ID!) {
  customer(id: $customerId) {
    id
    email
    metafield(namespace: "loyalty", key: "points") { value }
    metafield(namespace: "loyalty", key: "tier") { value }
    metafield(namespace: "loyalty", key: "history") { value }
  }
}
```

---

## 6. IMPLEMENTATION FILES

### Python Scripts:
1. `loyalty_manager.py` - Main API wrapper
   - `add_points(customer_id, points, action, metadata)`
   - `deduct_points(customer_id, points, action)`
   - `get_balance(customer_id)`
   - `get_history(customer_id)`
   - `create_discount_code(customer_id, points_value)`

2. `loyalty_setup.py` - One-time metafield definitions
   - Create metafield definitions via Admin API

3. `loyalty_webhooks.py` - Webhook handlers (Google Apps Script)
   - Handle order paid webhook
   - Handle customer created webhook
   - Handle review submitted webhook (Loox)

### Shopify Flow Workflows:
1. `flow_signup_bonus.json` - 50 points on account creation
2. `flow_purchase_points.json` - Points on order paid
3. `flow_tier_upgrade.json` - Email notification on tier change

### Liquid Templates (Updated):
1. `snippets/loyalty-points-widget.liquid` - Read from metafields instead of `customer.total_spent`
2. `snippets/loyalty-redemption-form.liquid` - Redemption UI with discount codes
3. `snippets/loyalty-history.liquid` - Display transaction history

---

## 7. DEPLOYMENT PHASES

### Phase 1: Setup (Day 1)
- ✅ Create metafield definitions
- ✅ Deploy `loyalty_manager.py` script
- ✅ Test metafield read/write

### Phase 2: Earning Rules (Day 2)
- ✅ Shopify Flow: Signup bonus
- ✅ Shopify Flow: Purchase points
- ✅ Test earning rules with test customers

### Phase 3: Redemption (Day 3)
- ✅ Build redemption script (discount code generation)
- ✅ Update UI with redemption form
- ✅ Test redemption flow end-to-end

### Phase 4: Advanced Features (Day 4)
- ✅ Transaction history display
- ✅ Tier upgrade emails (Klaviو)
- ✅ Review & referral points (webhooks)

### Phase 5: Testing & Launch (Day 5)
- ✅ QA testing with test customers
- ✅ Documentation for admin
- ✅ Launch to production

---

## 8. SECURITY CONSIDERATIONS

**API Key Management:**
- Store Shopify Admin API token in environment variables
- Never commit API keys to GitHub
- Use `.env` file (add to `.gitignore`)

**Redemption Validation:**
- Always validate customer has sufficient points before deducting
- Prevent negative balances
- Rate limiting on redemption (1 per day max)

**Webhook Verification:**
- Verify webhook HMAC signature (Shopify security)
- Reject unauthorized requests

---

## 9. COST ANALYSIS

**Development Time:** 20-30 hours
**Ongoing Costs:**
- Shopify API calls: FREE (within rate limits)
- Hosting script: $0 (Google Apps Script) or $5/month (Python server)
- Email notifications: $0 (Shopify Email) or included in Klaviو

**vs App Cost:**
- Smile.io: $49-$599/month = $588-$7,188/year
- Custom: $0-$60/year (hosting only)
- **Savings:** $528-$7,128/year

---

## 10. TESTING PLAN

**Test Scenarios:**
1. New customer signup → Should receive 50 bonus points
2. Customer makes $150 purchase → Should receive 150 points
3. Customer redeems 100 points → Should receive $5 discount code
4. Customer crosses 501 points → Should upgrade to Silver tier
5. Transaction history → Should display all actions chronologically

**Test Customers:**
- Create 3 test customer accounts
- Simulate full lifecycle (signup → purchase → redeem → tier upgrade)

---

**STATUS:** Phase 1 - Setup in progress
**Next Step:** Create `loyalty_manager.py` script
