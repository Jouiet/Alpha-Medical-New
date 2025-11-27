# Abandoned Cart Recovery - Configuration Guide
**Store:** Alpha Medical Care (azffej-as.myshopify.com)
**Plan:** Shopify Basic
**Date:** October 16, 2025
**Implementation:** Shopify Native + ReConvert App

---

## 📋 Executive Summary

**Limitation du plan Basic:**
- ❌ Abandoned CART emails (customer added to cart but didn't checkout): NOT available
- ✅ Abandoned CHECKOUT emails (customer started checkout but didn't complete): AVAILABLE

**Solution implémentée:**
1. Optimiser l'email "Abandoned Checkout" natif Shopify
2. Utiliser ReConvert app (déjà installée) pour post-purchase upsells
3. Impact attendu: Récupération de 5-8% des checkouts abandonnés

---

## 🎯 Configuration: Abandoned Checkout Email (Shopify Native)

### Étape 1: Accéder aux paramètres
**Navigation:** Admin Shopify → Settings → Notifications → Customer notifications → Abandoned checkout

### Étape 2: Configuration optimale pour le marché US

**Subject Line Recommendations:**
```
Option A: "Complete your order - {{ shop.name }}"
Option B: "You left something behind at {{ shop.name }}"
Option C: "Your cart is waiting! Complete checkout now"
```

**Timing:**
- Default: 1 hour after abandonment
- Recommendation: Keep at 1 hour (optimal conversion window)

**Email Body - Key Elements:**

1. **Header:**
   - Alpha Medical Care logo
   - Clear subject preview

2. **Product Reminder:**
   - Show cart items with images
   - Display prices clearly
   - Include product names

3. **Urgency Element:**
   ```
   "Your items are still available, but inventory is limited!"
   ```

4. **Trust Signals:**
   - Free shipping on orders $50+ (already implemented)
   - Secure checkout badge
   - Customer reviews mention

5. **CTA Button:**
   - Text: "Complete Your Order"
   - Color: Primary brand color (#4770DB)
   - Large and prominent

6. **Support Info:**
   - "Questions? Chat with us or email support@alphamedical.shop"
   - Live chat availability

### Étape 3: Personnalisation du template

**Variables Liquid disponibles:**
- `{{ customer.first_name }}` - First name
- `{{ shop.name }}` - Store name
- `{{ checkout.line_items }}` - Cart items
- `{{ checkout.subtotal_price | money }}` - Subtotal
- `{{ checkout_url }}` - Direct link to complete checkout

**Recommended Email Structure:**
```liquid
Hi {{ customer.first_name }},

You left items in your cart at {{ shop.name }}.

[PRODUCT GRID WITH IMAGES]

Subtotal: {{ checkout.subtotal_price | money }}

Don't miss out - your items are waiting!

[COMPLETE YOUR ORDER BUTTON]

Free shipping on orders over $50!

Questions? We're here to help.
Live chat available or email support@alphamedical.shop

Best regards,
Alpha Medical Care Team
```

---

## 🔧 ReConvert App Configuration

**Status:** Installed (Free trial active)
**Purpose:** Post-purchase upsells and thank you page optimization

### Features to Enable:

1. **Thank You Page Upsells**
   - Show complementary products
   - One-click add to existing order
   - Impact: AOV +10-15%

2. **Funnel Builder**
   - Create post-purchase funnel
   - Suggest frequently bought together items
   - Example: Customer buys back brace → suggest posture corrector

3. **Birthday Collector**
   - Collect customer birthdays on thank you page
   - Enable birthday email campaigns later

### Recommended Upsell Products:

**For Pain Relief products:**
- Upsell: Heat therapy pads
- Cross-sell: Massage tools

**For Posture products:**
- Upsell: Ergonomic accessories
- Cross-sell: Back support cushions

**For Therapy products:**
- Upsell: Recovery equipment
- Cross-sell: Wellness accessories

---

## 📊 Expected Results

### Abandoned Checkout Recovery:
- **Baseline:** 0% (no optimization)
- **After implementation:** 5-8% recovery rate
- **Revenue impact:** For 100 abandoned checkouts/month at $100 avg:
  - Recovery: 5-8 orders
  - Revenue: $500-$800/month recovered

### ReConvert Upsells:
- **Post-purchase acceptance rate:** 10-15%
- **AOV increase:** +10-15%
- **Revenue impact:** For 50 orders/month at $100 avg:
  - Upsells accepted: 5-8 orders
  - Additional revenue: $500-800/month

**Total Impact:** $1,000-$1,600/month in additional revenue

---

## ✅ Implementation Checklist

### Shopify Abandoned Checkout:
- [ ] Navigate to Settings → Notifications → Customer notifications
- [ ] Click "Abandoned checkout"
- [ ] Verify email is enabled
- [ ] Customize subject line (use one of recommended options)
- [ ] Edit email body with recommended structure
- [ ] Add urgency elements
- [ ] Include free shipping mention ($50 threshold)
- [ ] Test email preview
- [ ] Save changes

### ReConvert Configuration:
- [ ] Open ReConvert app from Shopify admin
- [ ] Complete onboarding wizard
- [ ] Enable "Thank You Page Funnel"
- [ ] Select 3-5 top upsell products per category
- [ ] Configure one-click upsell settings
- [ ] Set up birthday collector widget
- [ ] Preview thank you page
- [ ] Activate funnel

### Testing:
- [ ] Create test order with valid email
- [ ] Abandon checkout (don't complete payment)
- [ ] Wait 1 hour
- [ ] Check if abandoned checkout email received
- [ ] Verify email formatting on desktop + mobile
- [ ] Test checkout URL link functionality
- [ ] Complete test purchase to see ReConvert thank you page
- [ ] Verify upsell products display correctly

---

## 🚨 Limitations & Workarounds

### Limitation: No Abandoned CART emails on Basic plan
**Problem:** Customers who add to cart but never start checkout won't receive recovery emails.

**Workarounds:**
1. **Exit Intent Popup** (Already implemented ✅)
   - Captures email before they leave
   - Offers discount to encourage checkout

2. **Klaviyo Integration** (For future upgrade)
   - If Klaviyo properly configured later
   - Can track "Added to Cart" event
   - Send abandoned cart flow (3 emails)
   - Cost: Free up to 250 contacts

3. **Shopify Plan Upgrade** ($39/month)
   - Unlocks native abandoned cart recovery
   - Full email automation
   - Advanced reporting

**Recommendation:** Start with current solution, upgrade if abandoned cart rate > 30%

---

## 📈 Monitoring & Optimization

### Weekly Check:
- Shopify Admin → Analytics → Reports → "Cart Analysis"
- Check abandoned checkout rate
- Monitor recovery email open rates
- Track conversion from recovery emails

### Monthly Review:
- Compare recovery rate to industry benchmark (5-15%)
- Analyze which products have highest abandonment
- Test different email subject lines (A/B testing)
- Optimize ReConvert upsells based on acceptance rate

### KPIs to Track:
```
✓ Abandoned checkout rate (Target: <70%)
✓ Recovery email open rate (Target: >40%)
✓ Recovery email click rate (Target: >15%)
✓ Recovery conversion rate (Target: 5-8%)
✓ ReConvert upsell acceptance (Target: 10-15%)
✓ Average order value change (Target: +10%)
```

---

## 🎓 Best Practices

### Email Timing:
- First email: 1 hour (highest conversion)
- Don't send multiple emails on Basic plan (spam risk)
- Ensure email deliverability (valid sender address)

### Email Content:
- Keep it personal (use first name)
- Show product images (visual reminder)
- Create urgency WITHOUT being pushy
- Make CTA prominent and clear
- Mobile-responsive design (60%+ open on mobile)

### ReConvert Upsells:
- Offer genuine complementary products (not random)
- Discount upsells 10-15% to incentivize
- Limit to 2-3 upsell options (avoid overwhelm)
- Use social proof ("Customers also bought...")

### Legal Compliance:
- Include unsubscribe link (Shopify auto-includes)
- Privacy policy link in footer
- CAN-SPAM compliance (US market)
- Clear sender identification

---

## 🔄 Future Enhancements

### When Klaviyo is properly connected:
1. Full abandoned cart flow (3 emails)
2. Win-back campaigns for inactive customers
3. Browse abandonment emails
4. Advanced segmentation

### When upgrading to Shopify plan ($39/mo):
1. Native abandoned cart emails
2. Multiple automated email sequences
3. Advanced analytics
4. Custom reports

### Additional Apps to Consider:
- **Privy:** Advanced popup and email capture
- **Omnisend:** All-in-one marketing automation
- **Loox:** Review request automation (already have)

---

## 📝 Documentation

**Files Modified:** None (configuration via Shopify admin UI)
**Apps Used:** Shopify native + ReConvert
**Testing Date:** [To be completed]
**Live Date:** [To be completed]

**Implementation Time:**
- Abandoned checkout email optimization: 30 minutes
- ReConvert configuration: 45 minutes
- Testing: 2-3 hours (wait time for email)
- **Total:** ~4 hours

**Status:** ⏳ PENDING MANUAL IMPLEMENTATION
**Next Step:** Access Shopify admin and follow checklist above

---

*Document created: October 16, 2025*
*Last updated: October 16, 2025*
*Created by: Claude Code*
