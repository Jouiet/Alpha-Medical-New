# TIDIO AUTOMATION - FINAL IMPLEMENTATION SUMMARY
**Alpha Medical (alphamedical.shop) - Support Flows ONLY**
**Date:** 2025-11-29
**Total Implementation Time:** 57 minutes
**Role:** SUPPORT automation (ZERO marketing overlap)

---

## STRATEGIC POSITIONING

### ✅ TIDIO HANDLES (Support Automation)
- Real-time FAQ automation during browsing
- Welcome message - support focus (no discount)
- Product questions (sizing, compatibility, features)
- Order tracking (Shopify integration)
- Support routing (shipping, returns, warranty)
- Review management (Judge.me integration)

### ❌ TIDIO DOES NOT HANDLE (Marketing - Already Covered)
- Cart abandonment ➜ Shopify Email handles
- Email capture popups ➜ Shopify Forms (2 popups active)
- Welcome discounts ➜ Klaviyo Welcome Series handles
- Post-purchase nurture ➜ Shopify Email + Klaviyo handle
- Product recommendations ➜ Klaviyo Cross-Sell flow handles

**Result:** ZERO overlap, ZERO customer fatigue

---

## IMPLEMENTATION PLAN (6 FLOWS)

### Flow #1: FAQ for Online Store
**Status:** ✅ ALREADY CONFIGURED
**Template:** "FAQ for Online Store" (9.4K uses)
**Action Required:** Verification only (2 minutes)

**Verification Checklist:**
- [ ] Navigate to Tidio → Chatbots → Flows
- [ ] Confirm "FAQ for Online Store" is active
- [ ] Test on website: type common questions ("shipping", "return", "warranty")
- [ ] Verify responses match your 7 existing macros

---

### Flow #2: Reactive Welcome Message
**Template:** "Reactive Welcome Message" (6.5K uses)
**Time:** 10 minutes
**Purpose:** Support-focused greeting (NOT discount offer)

**Setup Steps:**
1. Tidio Panel → Chatbots → Flows → + Add Flow
2. Select "Reactive Welcome Message" template
3. Configure trigger:
   - Delay: 5 seconds after page load
   - Frequency: Once per session
   - Pages: All pages
4. Edit message text:
   ```
   Bienvenue sur Alpha Medical. Besoin d'aide pour trouver l'équipement
   de soulagement de la douleur ou de récupération adapté ? Je suis là
   pour répondre à vos questions.
   ```
5. Configure 3 buttons:
   - "Questions produit" → Close or link to FAQ
   - "Guide des tailles" → Link to macro "Product Fit Guide"
   - "Je parcours, merci" → Close chat
6. Save and activate

**Expected Impact:** 15-20% visitors engage, 40-50% of those find answers without agent

---

### Flow #3: Product Questions (Custom Build)
**Template:** None (custom build - no appropriate template)
**Time:** 15 minutes
**Purpose:** Proactive support on product pages

**Setup Steps:**
1. Tidio Panel → Chatbots → Flows → + Create from scratch
2. Configure trigger:
   - Trigger type: "Time on page" (60 seconds) OR "Scroll depth" (50%)
   - Frequency: Once per visitor
   - Pages: Product pages only (URL contains /products/)
3. Message text:
   ```
   Je vois que vous consultez [Product Name]. Des questions sur les tailles,
   la compatibilité ou les fonctionnalités ? Je suis là pour vous aider.
   ```
   Use variable: {{product.name}} if available in Tidio Shopify integration
4. Configure 4 buttons:
   - "Guide des tailles" → Link to macro or /pages/size-guide
   - "Comparer les modèles" → Ask "Quels modèles voulez-vous comparer ?"
   - "Voir les avis clients" → Scroll to #reviews (Judge.me section)
   - "Ça va, merci" → Close chat
5. Save and activate

**Expected Impact:** 8-12% engagement on product pages, reduces sizing returns

---

### Flow #4: Support Routing + Track Order
**Templates:** "Track Your Order (Shopify)" + Custom routing
**Time:** 20 minutes
**Purpose:** Centralized support menu + order tracking

**Setup Steps:**
1. Tidio Panel → Chatbots → Flows → + Add Flow
2. Select "Track Your Order (Shopify)" template
3. Configure trigger:
   - Pages: Contact page (/pages/contact) OR
   - Keywords: "shipping", "return", "warranty", "order", "track"
4. Edit to create support menu with 8 options:
   ```
   Comment puis-je vous aider aujourd'hui ?
   ```
   Buttons:
   - "📦 Suivre ma commande" → Track Order flow (Shopify API)
   - "🚚 Frais de livraison" → Macro: Shipping
   - "↩️ Retours et échanges" → Macro: Returns
   - "🛡️ Garantie produit" → Macro: Warranty
   - "📏 Guide des tailles" → Macro: Sizing
   - "⚙️ Caractéristiques" → Macro: Features
   - "💳 Paiement sécurisé" → Macro: Payment
   - "❓ Autre question" → Text input → Live agent OR email capture

5. Configure Shopify integration for Track Order:
   - Tidio → Settings → Integrations → Shopify
   - Enable order tracking API
   - Test with real order number

6. Link each button to corresponding macro (already created)
7. Save and activate

**Expected Impact:** 60-70% self-service rate, reduces support tickets by 40%

---

### Flow #5: Judge.me - Rating Protector
**Template:** "Judge.me - Rating Protector" (808 uses)
**Time:** 5 minutes
**Purpose:** Intercept low ratings BEFORE publication

**Prerequisites:**
- Judge.me app installed ✅
- Judge.me review collection active
- Tidio-Judge.me integration enabled

**Setup Steps:**
1. Tidio Panel → Chatbots → Flows → + Add Flow
2. Select "Judge.me - Rating Protector" template
3. Configure trigger:
   - Event: Customer submits 1-3 star rating via Judge.me
   - Timing: BEFORE review published (critical!)
4. Message text (template provides, customize):
   ```
   Bonjour [Customer Name], j'ai remarqué que vous avez attribué une note
   inférieure à nos attentes pour votre récent achat. Je suis vraiment
   désolé d'apprendre cela. Pouvez-vous me dire ce qui n'a pas fonctionné ?
   Je veux arranger les choses.
   ```
5. Configure 4 buttons:
   - "Le produit ne convenait pas" → Offer exchange/refund
   - "Produit défectueux" → Offer replacement/refund
   - "Problème de livraison" → Apologize + 10% discount code
   - "Autre problème" → Route to live agent (email: contact@alphamedical.shop)
6. Enable Judge.me integration:
   - Tidio → Settings → Integrations → Judge.me
   - Authorize connection
7. Save and activate

**Expected Impact:** 30-40% of low ratings converted to 4-5 stars after issue resolution

---

### Flow #6: Judge.me - Thank Positive Reviews
**Template:** "Judge.me - thank for positive review" (311 uses)
**Time:** 5 minutes
**Purpose:** Build loyalty with 4-5 star reviewers

**Setup Steps:**
1. Tidio Panel → Chatbots → Flows → + Add Flow
2. Select "Judge.me - thank for positive review" template
3. Configure trigger:
   - Event: Customer posts 4-5 star review via Judge.me
   - Timing: Immediately after publication
4. Message text (template provides, customize):
   ```
   Bonjour [Customer Name] ! 🙏 Merci beaucoup pour votre avis [Rating] étoiles
   sur [Product Name]. Nous sommes ravis qu'il vous aide dans votre soulagement
   de la douleur. En remerciement, voici 10% de réduction sur votre prochaine
   commande : REVIEW10
   ```
5. Configure 3 buttons:
   - "Acheter des produits similaires" → Cross-sell (link to collection)
   - "Partager mon expérience" → Social share (Facebook/Twitter)
   - "Fermer" → End chat
6. Optional: Create Shopify customer tag
   - When flow triggers, tag customer "positive_reviewer"
   - Use in Klaviyo for VIP segment
7. Create discount code in Shopify:
   - Shopify → Discounts → Create discount code
   - Code: REVIEW10
   - Type: Percentage
   - Value: 10%
   - Usage: One use per customer
8. Save and activate

**Expected Impact:** 20-30% repeat purchase rate from positive reviewers

---

## IMPLEMENTATION OPTIONS

### Option A: Immediate Implementation (57 minutes)
- **Timeline:** Today (2025-11-29)
- **Method:** All 6 flows in single session
- **Pros:** Instant support improvement, test before Lyro AI upgrade
- **Cons:** Learning curve, potential for minor errors

### Option B: Progressive Implementation (3-4 days)
- **Day 1:** Flow #1 verification + Flow #2 (12 min)
- **Day 2:** Flow #3 (15 min) + monitor engagement
- **Day 3:** Flow #4 (20 min) + test with real customer
- **Day 4:** Flow #5 + #6 (10 min total) once reviews imported
- **Pros:** Gradual learning, easier troubleshooting
- **Cons:** Delayed full benefit

### Option C: Wait for Lyro AI Upgrade (30.01.2026)
- **Timeline:** Wait 2 months for $39/mo plan
- **Method:** Implement all flows + Lyro AI in single day (1.5 hours)
- **Pros:** 60-70% automation rate with AI, future-proof
- **Cons:** No support automation for 2 months

**Recommended:** Option B (progressive) - balances learning curve with immediate value

---

## POST-IMPLEMENTATION MONITORING

### Week 1: Engagement Metrics
- Chat widget appearance rate: Target 80%+ visitors see widget
- Flow trigger rate: Target 25-35% visitors trigger at least one flow
- Self-service rate: Target 50%+ questions answered without agent

### Week 2-4: Performance Optimization
- Identify most common questions → add to FAQ flow
- Monitor Flow #5 (Rating Protector) → track conversion rate
- Test different button texts if engagement <20%

### Month 2+: Prepare for Lyro AI
- Export chat transcripts (Tidio → Analytics → Conversations)
- Identify repetitive questions for AI training
- Budget upgrade to $39/mo plan (scheduled 30.01.2026)

---

## INTEGRATION CHECKLIST

### Tidio ↔ Shopify
- [x] Tidio app installed (verified via API)
- [ ] Order tracking API enabled (Flow #4)
- [ ] Product name variables working (Flow #3)
- [ ] Customer data syncing (name, email, order history)

### Tidio ↔ Judge.me
- [x] Judge.me app installed (verified via API)
- [ ] Tidio-Judge.me integration authorized (Flow #5 + #6)
- [ ] Test trigger: Submit test review → verify Tidio message
- [ ] Email notification: jouiet.hat@gmail.com

### Shopify Discount Codes
- [ ] Create REVIEW10 code (10% off, one use per customer)
- [ ] Test code redemption at checkout
- [ ] Monitor usage in Shopify → Discounts → Analytics

---

## TROUBLESHOOTING GUIDE

### Issue: Flow not triggering
**Solution:**
1. Check flow status: Active (green toggle)
2. Verify trigger conditions match page URL
3. Clear browser cache and test in incognito mode
4. Check "Frequency" setting (once per session vs. once per visitor)

### Issue: Buttons not linking correctly
**Solution:**
1. Tidio → Chatbots → Flows → Edit button
2. Verify link format:
   - Macros: Select from dropdown (don't use URL)
   - Pages: Use absolute URL (https://alphamedical.shop/pages/contact)
   - Close chat: Select "Close conversation" action

### Issue: Shopify order tracking not working
**Solution:**
1. Tidio → Settings → Integrations → Shopify → Reconnect
2. Verify permissions: "Read orders" enabled
3. Test with recent order number (last 30 days)

### Issue: Judge.me integration not triggering
**Solution:**
1. Judge.me → Settings → Integrations → Tidio → Authorize
2. Verify webhook URL is correct
3. Submit test review (4-5 stars) → check Tidio conversation log
4. Email support@judge.me if webhook fails

---

## CONTACT & RESOURCES

### Tidio Support
- Dashboard: https://www.tidio.com/panel/
- Help Center: https://help.tidio.com/
- Widget SDK: https://tidio.com/docs/widget-sdk/
- Live Chat: Available in Tidio panel

### Alpha Medical Configuration
- Store: https://alphamedical.shop
- Contact Email: contact@alphamedical.shop
- Tidio Public Key: mgbvasemhlltntquk6tstekoflejm2nt
- Chat Page: https://chatting.page/mgbvasemhlltntquk6tstekoflejm2nt

### Current Plan
- Tidio Starter: $29/mo (active)
- Planned Upgrade: Lyro AI $39/mo (30.01.2026)
- Features: 100 conversations/mo, unlimited chatbots, Shopify integration

---

## SUCCESS CRITERIA (30 Days)

### Quantitative Metrics
- [ ] 500+ chat conversations initiated (vs. 0 baseline)
- [ ] 60%+ self-service rate (no agent required)
- [ ] 30%+ low rating conversion (Flow #5)
- [ ] 25%+ positive reviewer engagement (Flow #6)
- [ ] 40% reduction in support tickets via email

### Qualitative Metrics
- [ ] Customer feedback: "Found answers quickly via chat"
- [ ] Team feedback: "Fewer repetitive questions via email"
- [ ] Review quality: More detailed feedback (positive and negative)

---

**Document Version:** 1.0 (2025-11-29)
**Last Updated:** Post Judge.me correction
**Next Review:** After implementation (Option A/B/C)
**Related Documents:**
- TIDIO_SUPPORT_FLOWS_FINAL_IMPLEMENTATION_2025-11-29.md (detailed guides)
- TIDIO_DEDUPLICATION_MATRIX_2025-11-29.md (overlap analysis)
- TIDIO_TEMPLATES_ANALYSIS_FACTUAL_2025-11-29.md (template research)
