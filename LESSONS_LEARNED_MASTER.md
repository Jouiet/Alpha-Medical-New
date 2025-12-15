# LESSONS LEARNED - MASTER CONSOLIDATION

**Last Updated:** 2025-12-15 (Session 98)
**Purpose:** Centralized, searchable lessons learned database
**Source:** 30+ session files consolidated

---

## CATEGORY 1: VERIFICATION & VALIDATION

### L1.1: Never Trust Documentation Without Verification
**Session:** 73, 83
**Pattern:** Documentation claims ≠ actual state
**Examples:**
- Session 72 claimed 3 tasks needed → All were already done
- Docs said "not deployed" → Theme had schemas since Session 69
- Script reported success → Workflow actually inactive

**Fix:** Always verify: `grep → API call → Chrome DevTools → Then act`
**Tags:** #verification #documentation #trust

### L1.2: Bottom-Up Verification > Top-Down Trust
**Session:** 73, 82, 83
**Pattern:** Assumptions based on code/docs lead to false conclusions
**Quote:** "Vérification FACTUELLE RIGOUREUSE - pas de confiance aveugle dans les scripts"

**Process:**
1. Create scripts
2. Execute scripts
3. Empirical verification
4. Verify product by product
5. IF 100% success → next task
6. IF <100% → correct → iterate

**Tags:** #methodology #verification #factual

### L1.3: Scripts Can Report Success While Being Wrong
**Session:** 83
**Pattern:** Automation success ≠ actual system state
**Example:** AUTOMATION_COMPLEMENTARITY_MATRIX analyzed code/config, not live UI
**Fix:** Use Chrome DevTools MCP for UI-level verification

**Tags:** #automation #verification #ui

---

## CATEGORY 2: API & AUTOMATION

### L2.1: API Automation ROI is Significant
**Sessions:** 76, 81, 88
**Pattern:** API automation >> manual work
**Evidence:**
- 82 products moved: 5 min (API) vs 3+ hours (manual)
- Policy deployment: 15 sec (API) vs 8+ hours (manual)
- Schema deployment: 2 min (API) vs 1 hour (manual)

**Tags:** #automation #roi #api

### L2.2: Shopify CLI Config Can Point to Wrong Store
**Session:** 73
**Pattern:** CLI store ≠ expected store
**Example:** CLI showed 'jqp1x4-7e' instead of 'azffej-as'
**Fix:** Always verify store domain via API before deployment

**Tags:** #shopify #cli #configuration

### L2.3: Liquid Syntax Pitfalls
**Session:** 69
**Pattern:** Comment blocks in `{%- liquid -%}` tags not supported
**Fix:**
- Pre-deployment syntax validation
- Build in 2-3 min buffer for cache clearance
- Always provide fallbacks for optional objects

**Tags:** #liquid #shopify #syntax

---

## CATEGORY 3: EMAIL & COMMUNICATION

### L3.1: Personal Email Should Never Be Public
**Session:** 76
**Pattern:** Scripts can hardcode wrong email type
**Example:** Policy script used jouiet.hat@gmail.com instead of contact@alphamedical.shop
**Fix:**
- Always use contact@alphamedical.shop for public communications
- Verify email type before deployment
- Add email validation to pre-deployment checks

**Tags:** #email #privacy #professional

### L3.2: Email Automation Duplication is Dangerous
**Session:** 83, 91
**Pattern:** Multiple systems sending same emails
**Evidence:** Cart abandonment was 3-way duplicated (Shopify Flow + Shopify Email + Klaviyo)
**Impact:** Up to 5 emails per cart abandonment → +25-50% unsubscribe risk
**Fix:** Choose ONE system per trigger (Klaviyo = email marketing leader)

**Tags:** #email #duplication #klaviyo

---

## CATEGORY 4: PRODUCT & CATALOG

### L4.1: Draft Status Preservation is Critical
**Session:** 88
**Pattern:** User explicitly requires draft status preservation
**Fix:** Always verify draft products remain in draft after operations

**Tags:** #products #draft #verification

### L4.2: External Widgets Have Limitations
**Session:** 88
**Pattern:** Cannot control CDN-injected elements
**Example:** 4th popup (Klaviyo/Omnisend CDN) out of theme control
**Fix:** Document limitations, don't promise what can't be delivered

**Tags:** #widgets #cdn #limitations

---

## CATEGORY 5: TECHNICAL ARCHITECTURE

### L5.1: GTM Architecture Changes Annually
**Session:** 65
**Pattern:** Previous year's configuration can become obsolete
**Evidence:** Pre-2025: 1 tag sufficient → 2025: 3 tags required (Base + Linker + Conversion)
**Fix:** Check GTM best practices each year (Q1)

**Tags:** #gtm #google #architecture

### L5.2: CDN Caching Requires Wait Time
**Session:** 69
**Pattern:** Changes not immediately visible
**Evidence:** 2-3 min delay required between deploy and verification
**Fix:** Build buffer time into deployment scripts

**Tags:** #cdn #caching #deployment

### L5.3: Schema Validation Strategy
**Session:** 69, 73
**Pattern:** DOM inspection ≠ Google validation
**Evidence:** 7 JSON-LD scripts present → Google confirmed 8 valid items
**Fix:** Use Rich Results Test for ground truth, not DOM inspection

**Tags:** #schema #seo #validation

---

## CATEGORY 6: PROCESS & METHODOLOGY

### L6.1: Documentation Lag is Dangerous
**Session:** 73
**Pattern:** Docs don't reflect current state
**Example:** Docs said "not deployed" but theme had schemas since Session 69
**Fix:** Update docs ONLY after empirical verification, not assumptions

**Tags:** #documentation #process #lag

### L6.2: Iterative Refinement Works
**Session:** 88
**Pattern:** User feedback → corrections → improvement
**Example:** 3 products reclassified based on user corrections
**Fix:** Build feedback loops into all processes

**Tags:** #iteration #feedback #refinement

### L6.3: Ask for Assets/Requirements Upfront
**Session:** Various
**Pattern:** Assumptions lead to rework
**Fixes:**
- Ask for asset location upfront
- Present multiple options (A/B choice)
- Confirm positioning/sizing before finalizing

**Tags:** #requirements #communication #upfront

---

## CATEGORY 7: DESIGN & CONTENT

### L7.1: Real Photography > Generic Designs
**Session:** Various
**Pattern:** Generic designs get rejected
**Evidence:** Rejected 3 times before using real product photos
**Fix:**
- JPEG for photos (84.9% smaller than PNG)
- SVG for vector logos
- Real products >> stock images

**Tags:** #design #photography #format

---

## QUICK REFERENCE - BY SESSION

| Session | Key Lesson |
|---------|------------|
| 65 | GTM architecture requires 3 tags (2025) |
| 69 | Liquid syntax pitfalls + cache delays |
| 73 | Never trust docs, verify empirically |
| 76 | Personal email must never be public |
| 81 | Memory system optimization (+90% efficiency) |
| 82 | Bottom-up verification methodology |
| 83 | Email automation duplication danger |
| 88 | API automation ROI + iterative refinement |
| 91 | Email consolidation (Klaviyo only) |
| 98 | Feedback loops are NOT operational |

---

## SEARCH INDEX

**#verification:** L1.1, L1.2, L1.3, L4.1
**#automation:** L1.3, L2.1, L3.2
**#api:** L2.1, L2.2
**#shopify:** L2.2, L2.3, L4.1
**#email:** L3.1, L3.2
**#documentation:** L1.1, L6.1
**#methodology:** L1.2, L6.2
**#gtm:** L5.1
**#schema:** L5.3

---

## HOW TO USE THIS DOCUMENT

1. **Before starting a task:** Search for relevant tags
2. **After completing a task:** Add new lessons following the format
3. **When debugging:** Check Category 1 (Verification)
4. **When automating:** Check Category 2 (API & Automation)
5. **Monthly:** Review and consolidate new lessons

---

**Document Status:** LIVING DOCUMENT
**Maintainer:** Claude Code sessions
**Format:** Standard lesson structure (Session, Pattern, Example, Fix, Tags)
