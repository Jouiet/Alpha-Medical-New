# PRIORITY SOURCES IMPLEMENTATION PLAN
## Alpha Medical - 10 Sources Prioritaires (Option B)

**Created:** 2025-11-25 03:00 UTC
**Strategy:** Build 10 high-ROI sources NOW, defer 13 others based on business needs
**Timeline:** 80 hours (10 days at 8h/day)
**Expected Volume:** 765-1,680 leads/month from priority sources only

---

## 🎯 SOURCES PRIORITAIRES (10 sources)

### Critères de priorisation:
1. **ROI élevé** - Sources avec meilleur ratio coût/lead
2. **Volume potentiel** - Sources générant le plus de leads
3. **Déjà actifs** - Sources partiellement déployées (quick wins)
4. **Coût $0** - Sources organiques (ON-SITE)
5. **Facilité technique** - API disponibles, intégration simple

---

## 📊 MATRICE DE PRIORISATION

| # | Source | Catégorie | Volume/mois | Coût | ROI | Status | Priorité |
|---|--------|-----------|-------------|------|-----|--------|----------|
| **1** | **Newsletter Signup** | ON-SITE | 50-100 | $0 | ⭐⭐⭐⭐⭐ | New | **P0** |
| **2** | **Contact Form** | ON-SITE | 10-20 | $0 | ⭐⭐⭐⭐⭐ | New | **P0** |
| **3** | **Product Waitlist** | ON-SITE | 5-10 | $0 | ⭐⭐⭐⭐⭐ | New | **P0** |
| **4** | **Cart Abandonment** | ON-SITE | 200-300 | $0 | ⭐⭐⭐⭐⭐ | ✅ Actif | **P0** |
| **5** | **Account Creation** | ON-SITE | 30-50 | $0 | ⭐⭐⭐⭐⭐ | ✅ Actif | **P0** |
| **18** | **Google Ads** | PAID ADS | 200-500 | $3-5K/mo | ⭐⭐⭐⭐ | New | **P0** |
| **19** | **Facebook/IG Ads** | PAID ADS | 300-450 | Included | ⭐⭐⭐⭐⭐ | ✅ Deployed | **P0** |
| **20** | **TikTok Ads** | PAID ADS | 50-150 | $1-3K/mo | ⭐⭐⭐⭐ | 🔧 Pixel deployed | **P0** |
| **39** | **Email Retargeting** | RETARGETING | 100-200 | $0 | ⭐⭐⭐⭐⭐ | New | **P0** |
| **40** | **Facebook Retargeting** | RETARGETING | 50-100 | Ad spend | ⭐⭐⭐⭐ | 🔧 Pixel deployed | **P0** |

**TOTAL VOLUME:** 765-1,680 leads/month
**TOTAL COST:** $0 (ON-SITE) + $4-8K/mo (Paid Ads + Retargeting)
**BLENDED CPL:** ~$5-10 per lead

---

## 💰 ANALYSE ROI - SOURCES PRIORITAIRES

### CATÉGORIE 1: ON-SITE (5 sources) - ROI MAXIMAL

**Volume:** 295-480/month
**Cost:** $0 (organic, already paying for website)
**CPL:** $0
**ROI:** UNBOUNDED (infinite ROI)

**Justification:**
- Trafic existant sur le site (0 coût marginal)
- Conversion 2-5% sur formulaires (industry standard)
- Setup 1x puis automatique
- Qualité élevée (site visitors = high intent)

**Quick Wins:**
- Cart Abandonment ✅ DÉJÀ ACTIF (Shopify native, besoin tracking seulement)
- Account Creation ✅ DÉJÀ ACTIF (Shopify native, besoin tracking seulement)

---

### CATÉGORIE 4: PAID ADS (3 sources) - ROI PROUVÉ

**Volume:** 550-1,100/month
**Cost:** $4-8K/month
**CPL:** $7-14
**ROI:** 150-300% (based on $75 AOV, 20% conversion)

**Justification:**
- Scalable (augmenter budget = augmenter volume)
- Ciblage précis (audiences qualifiées)
- Mesurable (ROAS tracking)
- FB Lead Ads ✅ DÉJÀ DEPLOYED (quick win)
- TikTok Pixel ✅ DÉJÀ DEPLOYED (ready for ads)

---

### CATÉGORIE 9: RETARGETING (2 sources) - WARM LEADS

**Volume:** 150-300/month
**Cost:** $0 (email) + ad spend (FB retargeting)
**CPL:** $2-5 (lower than cold ads)
**ROI:** 200-400% (warm leads convert better)

**Justification:**
- Visitors déjà familiers avec la marque
- Conversion 2-3x higher than cold traffic
- FB Pixel ✅ DÉJÀ DEPLOYED (quick win)
- Email retargeting = $0 cost (Klaviyo/Shopify existing)

---

## 🏗️ PLAN D'IMPLÉMENTATION - 10 SOURCES (80 hours)

### WEEK 1: ON-SITE CATEGORY (5 sources) - 32 hours

#### Day 1-2: Shopify Integration Foundation (16h)

**Source 1-2: Cart Abandonment + Account Creation (Quick Wins)**
- Status: ✅ Already active in Shopify
- Task: Add tracking to Google Sheet
- Time: 4h

**Approach:**
- Shopify webhook: `carts/update`, `customers/create`
- OR: Shopify Admin API polling (fallback)
- Reuse existing Shopify customer data
- Map to Google Sheet "Raw Leads"

**Deliverable:** `sync_shopify_native_to_sheet.py`

---

**Source 3-5: Newsletter + Contact + Waitlist**
- Task: Create form tracking system
- Time: 12h

**Approach:**
- Option A: Shopify Forms app (native)
- Option B: Typeform embedded forms (reuse existing integration)
- Option C: Custom Shopify form + webhook

**Recommended:** Option A (Shopify Forms app)
- Built-in Shopify
- No additional cost
- Easy webhook integration

**Deliverables:**
- `sync_shopify_forms_to_sheet.py` (handles all 3 form types)
- `.github/workflows/sync-shopify-forms.yml` (every 4h)

---

#### Day 3-4: Testing + Documentation (16h)

- Test all 5 ON-SITE sources end-to-end
- Create form templates (Newsletter, Contact, Waitlist)
- User setup guide (Shopify app installation)
- Verify data quality in Google Sheet

**Deliverables:**
- `tests/test_shopify_integration.py`
- `SETUP_GUIDE_ONSITE_SOURCES.md`

---

### WEEK 2: PAID ADS CATEGORY (3 sources) - 24 hours

#### Day 5-6: Google Ads Integration (12h)

**Source 18: Google Ads (Search + Display + Shopping)**
- Status: Not deployed (ready to launch)
- Task: Lead Form extensions integration
- Time: 12h

**Approach:**
- Google Ads API (Lead Form extension submissions)
- OAuth 2.0 authentication
- Fetch submissions every 6h
- Quality score: 9.0 (paid search, high intent)

**Deliverables:**
- `sync_google_ads_to_sheet.py` (180 lines)
- `.github/workflows/sync-google-ads-leads.yml`
- User setup guide (Google Ads campaign + Lead Forms)

---

#### Day 7: Facebook/TikTok Ads (Quick Wins) (12h)

**Source 19: Facebook/Instagram Ads**
- Status: ✅ Lead Ads DEPLOYED (quick win)
- Task: Verify existing integration works
- Time: 2h (testing only)

**Source 20: TikTok Ads**
- Status: 🔧 Pixel deployed, need Lead Ads integration
- Task: TikTok Lead Generation API integration
- Time: 10h

**Approach (TikTok):**
- TikTok Marketing API (Lead Generation)
- Similar to FB Lead Ads
- Fetch submissions every 6h
- Quality score: 8.0

**Deliverables:**
- `sync_tiktok_ads_to_sheet.py` (150 lines)
- `.github/workflows/sync-tiktok-leads.yml`

---

### WEEK 3: RETARGETING CATEGORY (2 sources) - 16 hours

#### Day 8: Email Retargeting (Browse Abandonment) (8h)

**Source 39: Email Retargeting**
- Status: New (but Klaviyo already active)
- Task: Track browse abandonment → capture new leads
- Time: 8h

**Approach:**
- Klaviyo API: Fetch profiles who received "Browse Abandonment" email
- Filter: NOT yet in database (new leads from retargeting)
- Quality score: 8.0 (warm leads)

**Deliverables:**
- `sync_klaviyo_retargeting_to_sheet.py` (120 lines)
- `.github/workflows/sync-klaviyo-retargeting.yml` (daily)

---

#### Day 9: Facebook Retargeting (8h)

**Source 40: Facebook Retargeting**
- Status: 🔧 Pixel deployed (quick win)
- Task: Track retargeting conversions → capture leads
- Time: 8h

**Approach:**
- Facebook Custom Audiences API (if accessible)
- OR: Manual export + Import tool (xlsx)
- Track pixel events → form submissions
- Quality score: 8.0

**Deliverables:**
- `sync_facebook_retargeting_to_sheet.py` (100 lines)
- OR: Documentation for manual export process

---

### WEEK 4: TESTING + DOCUMENTATION (8 hours)

#### Day 10: End-to-End Testing (8h)

- Integration tests for all 10 sources
- Performance tests (Sheet API limits)
- User acceptance testing
- Setup guides for all 10 sources
- Deployment checklist

**Deliverables:**
- Complete test suite (10 test files)
- User setup guide (PDF or MD)
- Deployment runbook
- Monitoring dashboard setup

---

## 📁 CODE STRUCTURE - 10 PRIORITY SOURCES

```
Alpha-Medical/
├── PHASE 1 (EXISTING - 3 sources):
│   ├── sync_typeform_to_sheet.py          ✅ Created
│   ├── sync_facebook_leads_to_sheet.py    ✅ Exists
│   └── import_leads_to_sheet.py           ✅ Enhanced
│
├── PRIORITY (NEW - 7 sources):
│   ├── sync_shopify_native_to_sheet.py    🔨 Week 1 (Cart + Account)
│   ├── sync_shopify_forms_to_sheet.py     🔨 Week 1 (Newsletter + Contact + Waitlist)
│   ├── sync_google_ads_to_sheet.py        🔨 Week 2 (Google Ads)
│   ├── sync_tiktok_ads_to_sheet.py        🔨 Week 2 (TikTok Ads)
│   ├── sync_klaviyo_retargeting_to_sheet.py 🔨 Week 3 (Email Retargeting)
│   └── sync_facebook_retargeting_to_sheet.py 🔨 Week 3 (FB Retargeting)
│
├── CENTRAL (EXISTING):
│   └── clean_and_segment_leads.py         ✅ Updated (23 sources)
│
├── .github/workflows/
│   ├── sync-typeform-leads.yml            ✅ Created
│   ├── sync-facebook-leads.yml            ✅ Exists
│   ├── sync-shopify-native.yml            🔨 Week 1
│   ├── sync-shopify-forms.yml             🔨 Week 1
│   ├── sync-google-ads-leads.yml          🔨 Week 2
│   ├── sync-tiktok-leads.yml              🔨 Week 2
│   ├── sync-klaviyo-retargeting.yml       🔨 Week 3
│   ├── sync-facebook-retargeting.yml      🔨 Week 3
│   └── clean-segment-leads.yml            ✅ Exists
│
└── tests/
    ├── test_shopify_integration.py        🔨 Week 1
    ├── test_google_ads_integration.py     🔨 Week 2
    ├── test_tiktok_integration.py         🔨 Week 2
    ├── test_retargeting_integration.py    🔨 Week 3
    └── test_priority_sources_e2e.py       🔨 Week 4
```

**Total Files:**
- 7 new Python scripts (10 sources total with existing 3)
- 7 new workflows (10 workflows total)
- 5 test files
- **19 new files** (+ 3 existing updated)

---

## ⏱️ TIMELINE DÉTAILLÉ - 80 HOURS

| Week | Focus | Sources | Hours | Deliverables |
|------|-------|---------|-------|--------------|
| **Week 1** | ON-SITE | 5 sources | 32h | 2 scripts + 2 workflows + tests |
| **Week 2** | PAID ADS | 3 sources | 24h | 2 scripts + 2 workflows + tests |
| **Week 3** | RETARGETING | 2 sources | 16h | 2 scripts + 2 workflows + tests |
| **Week 4** | TESTING | All 10 | 8h | Test suite + docs + deployment |
| **TOTAL** | - | **10 sources** | **80h** | **19 files** |

**Deployment Readiness:** End of Week 4 (10 days @ 8h/day)

---

## 💰 COÛT OPÉRATIONNEL - 10 SOURCES PRIORITAIRES

### Infrastructure (One-Time)
- Development: 80h @ $0 (in-house)
- Testing: Included
- **Total:** $0

### Monthly Operational Costs

**CATÉGORIE ON-SITE (5 sources):**
- Newsletter Signup: $0
- Contact Form: $0
- Product Waitlist: $0
- Cart Abandonment: $0 (Shopify native)
- Account Creation: $0 (Shopify native)
- **Subtotal:** $0/month

**CATÉGORIE PAID ADS (3 sources):**
- Google Ads: $3,000-5,000/month
- Facebook/IG Ads: Included in PRE-LAUNCH budget ($6K one-time)
- TikTok Ads: $1,000-3,000/month
- **Subtotal:** $4,000-8,000/month

**CATÉGORIE RETARGETING (2 sources):**
- Email Retargeting: $0 (Klaviyo existing)
- Facebook Retargeting: Included in ad spend
- **Subtotal:** $0 incremental

**TOTAL MONTHLY COST:** $4,000-8,000/month (PAID ADS only)
**Expected Volume:** 765-1,680 leads/month
**Blended CPL:** $5-10 per lead

---

## 📊 ROI PROJECTION - 10 SOURCES

### Scenario Conservative

**Investment:**
- Build: $0 (in-house dev)
- Monthly spend: $4,000 (ads)

**Volume:**
- 765 leads/month (low estimate)
- Conversion rate: 15% (conservative for e-commerce)
- Orders: 115/month
- AOV: $75
- Revenue: $8,625/month

**ROI:** ($8,625 - $4,000) / $4,000 = **116% ROI**

---

### Scenario Optimiste

**Investment:**
- Build: $0 (in-house dev)
- Monthly spend: $8,000 (ads)

**Volume:**
- 1,680 leads/month (high estimate)
- Conversion rate: 20% (optimistic)
- Orders: 336/month
- AOV: $75
- Revenue: $25,200/month

**ROI:** ($25,200 - $8,000) / $8,000 = **215% ROI**

---

## 🎯 SUCCESS METRICS - 10 SOURCES

### Week 1 (ON-SITE)
- [ ] 5 ON-SITE sources tracking data
- [ ] 50+ test leads processed
- [ ] 0 errors in logs (7 days)
- [ ] Forms live on website

### Week 2 (PAID ADS)
- [ ] Google Ads campaign launched
- [ ] TikTok Lead Ads launched
- [ ] 100+ paid leads captured
- [ ] CPL ≤ $15

### Week 3 (RETARGETING)
- [ ] Email retargeting tracking active
- [ ] FB retargeting tracking active
- [ ] 50+ retargeting leads captured
- [ ] CPL ≤ $5 (lower than cold ads)

### Week 4 (DEPLOYMENT)
- [ ] All 10 sources tested end-to-end
- [ ] User setup guides complete
- [ ] Workflows automated (8 workflows)
- [ ] Dashboard showing 10 source breakdown

---

## 🚫 SOURCES DIFFÉRÉES (13 sources)

Ces sources seront implémentées plus tard selon besoins business:

**CATÉGORIE 2: SOCIAL (4 sources) - DEFER**
- Instagram organic (bio link) - Volume moyen, effort élevé
- Facebook organic (messages) - Difficulté API
- TikTok organic (bio link) - Couvert par TikTok Ads
- YouTube organic - PHASE 3 (content-driven)

**CATÉGORIE 3: SEO/CONTENT (4 sources) - DEFER**
- Blog Newsletter - Besoin contenu existant d'abord
- Google Organic Search - GA4 déjà actif, tracking suffisant
- Google Shop - Volume faible (5-10/mois)
- Podcast Listeners - Pas de podcast actif

**CATÉGORIE 8: REFERRAL (3 sources) - DEFER**
- Customer Referral Program - Besoin customers existants d'abord
- Email Forwards - HubSpot native, actif
- Social Shares - Shopify native, actif

**CATÉGORIE 9: RETARGETING (2 sources implemented, 1 deferred)**
- Google RLSA - Defer (Google Ads Display priority first)

**Total Deferred:** 13 sources
**Rationale:** Focus sur quick wins + high ROI d'abord, ajouter complexity later

---

## ✅ ACCEPTANCE CRITERIA

### Infrastructure Ready
- [ ] 10 Python scripts written + documented
- [ ] 8 GitHub Actions workflows configured
- [ ] 5 test files passing
- [ ] Google Sheet columns for all 10 sources
- [ ] Setup guides for all 10 sources

### Deployment Ready
- [ ] All 10 sources tested with real data
- [ ] 100+ leads processed successfully
- [ ] No errors in logs (7 consecutive days)
- [ ] Analytics dashboard accurate
- [ ] User training complete

---

## 🚀 NEXT IMMEDIATE ACTIONS

**NOW (This Session):**
1. Create `sync_shopify_native_to_sheet.py` (Cart + Account tracking)
2. Create `sync_shopify_forms_to_sheet.py` (Newsletter + Contact + Waitlist)
3. Create workflows for Shopify integrations

**THIS WEEK:**
4. Test Shopify integrations end-to-end
5. User setup guide for Shopify forms
6. Start Google Ads integration

**NEXT WEEK:**
7. Complete Paid Ads integrations (Google + TikTok)
8. Start Retargeting integrations
9. Build test suite

---

**Ready to start building Week 1 (ON-SITE sources)?**

Commençons par:
1. **sync_shopify_native_to_sheet.py** (Cart Abandonment + Account Creation)
2. **sync_shopify_forms_to_sheet.py** (Newsletter + Contact + Waitlist)

Ou préférez-vous voir le plan final mis à jour avant de coder?
