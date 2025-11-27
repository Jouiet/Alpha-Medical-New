# IMPLEMENTATION PLAN - 3 PHASES COMPLETE
## Alpha Medical B2C Lead Architecture (11 sources)

**Created:** 2025-11-25 02:30 UTC
**Approach:** Build ALL infrastructure now, test immediately, deploy phased
**Total Sources:** 11 (3 Phase 1 + 7 Phase 2 + 1 Phase 3)
**Total Timeline:** 12 weeks (infrastructure) + phased deployment (52 weeks)

---

## 🎯 EXECUTIVE SUMMARY

**Stratégie:** Build complete infrastructure for all 3 phases NOW, then deploy sources in phased timeline based on business readiness (not technical readiness).

**Why Build All Now?**
- Unified architecture (no technical debt from rushed Phase 2-3 implementations)
- Test all integrations end-to-end before launch
- Flexibility to activate sources earlier if opportunity arises
- Code review & optimization across all sources (not piecemeal)

**Deployment Strategy:**
- **Infrastructure:** 12 weeks (all 11 sources coded + tested)
- **PHASE 1 Activation:** Week 13 (Nov 2025) - 3 sources
- **PHASE 2 Activation:** Week 26 (Month 1-3 post-launch) - 7 sources
- **PHASE 3 Activation:** Week 39 (Month 4-12 post-launch) - 1 source

---

## 📊 INFRASTRUCTURE BUILD (Weeks 1-12)

### Week 1-2: Architecture & Foundation
**Goal:** Setup unified data pipeline for all 11 sources

#### Tasks:
1. **Google Sheet Structure (2h)**
   - Create "Raw Leads" sheet (20 columns for all sources)
   - Create "Qualified Leads" sheet (18 columns)
   - Create "Analytics" dashboard (4 tabs: Overview, By Source, By Persona, Performance)
   - Add formulas, conditional formatting, data validation
   - Test: Manual data entry → Clean → Qualified

2. **Central Processing Script Enhancement (4h)**
   - Update `clean_and_segment_leads.py` to handle all 11 sources
   - Add source-specific validation rules
   - Add quality scoring for all source types
   - Add persona detection (15 keywords → 5 personas)
   - Test: Mock data from all 11 sources → Cleaning → Output validation

3. **GitHub Actions Infrastructure (2h)**
   - Create workflows folder structure (11 workflows)
   - Setup secrets management (plan for 15+ secrets)
   - Create reusable workflow templates
   - Test: Workflow syntax validation

**Deliverables:**
- ✅ Google Sheet ready for all sources
- ✅ Enhanced cleaning script (handles 11 sources)
- ✅ Workflow infrastructure ready

**Timeline:** 8 hours (Week 1-2)

---

### Week 3-4: PHASE 1 Sources (3 sources)

#### Source 1: Contest/Giveaway (Typeform)

**API Research (30min):**
- Typeform API: `https://api.typeform.com/forms/{form_id}/responses`
- Authentication: Bearer token (Personal Access Token)
- Rate limit: 600 requests/day
- Webhook option: Real-time push (better than polling)

**Tasks:**
1. **Create sync_typeform_to_sheet.py (3h)**
   - Fetch responses from Typeform API (last N hours)
   - Parse form fields (email, name, phone, custom questions)
   - Validate & clean data
   - Append to Google Sheet "Raw Leads"
   - Handle duplicates, errors, logging
   - Test: Mock Typeform response → Sheet

2. **Create workflow sync-typeform-leads.yml (1h)**
   - Schedule: Hourly 8 AM - 8 PM UTC (cron: `0 8-20 * * *`)
   - Environment: Python 3.11, dependencies: requests, gspread
   - Secrets: TYPEFORM_API_TOKEN, GOOGLE_SHEETS_CREDENTIALS
   - Test: Manual workflow dispatch

3. **Setup Typeform Contest Form (2h - USER ACTION)**
   - Create form with fields: email, name, phone, location, preferences
   - Get form ID
   - Generate Personal Access Token
   - Test form submission → API response

**Code Estimate:** 150 lines Python + 40 lines YAML
**Timeline:** 4 hours coding + 2 hours user setup = 6 hours total

---

#### Source 2: Facebook Lead Ads

**Status:** ✅ Code exists (`sync_facebook_leads_to_sheet.py`)

**Tasks:**
1. **Review & Test Existing Code (1h)**
   - Verify Meta API compatibility (Graph API v18.0+)
   - Test with dummy lead form
   - Verify error handling

2. **Setup FB Lead Form (3h - USER ACTION)**
   - Create FB Ads campaign
   - Create Lead Ads with Instant Form
   - Get form ID, ad account ID
   - Generate access token (90-day validity, plan for refresh)
   - Test form submission → API response

**Timeline:** 1 hour review + 3 hours user setup = 4 hours total

---

#### Source 3: Import Externes

**Status:** ✅ Code exists (`import_leads_to_sheet.py`)

**Tasks:**
1. **Enhance for JSON Support (1h)**
   - Current: xlsx, csv
   - Add: json, jsonl support
   - Test with sample files (xlsx, csv, json)

**Timeline:** 1 hour enhancement

---

**PHASE 1 TOTAL:** 11 hours (coding + enhancements)

---

### Week 5-8: PHASE 2 Sources (7 sources)

#### Source 4: Google Ads Campaigns

**API Research (30min):**
- Google Ads API: Lead form extensions
- Authentication: OAuth 2.0 (service account)
- API: `https://googleads.googleapis.com/v15/customers/{customer_id}/leadFormSubmissions`

**Tasks:**
1. **Create sync_google_ads_to_sheet.py (4h)**
   - Authenticate with Google Ads API (OAuth 2.0)
   - Fetch lead form submissions (last N hours)
   - Parse fields (similar to FB leads)
   - Quality score: 8.5 (paid search high intent)
   - Append to Sheet with source: "google_ads"
   - Test: Mock API response → Sheet

2. **Create workflow sync-google-ads-leads.yml (1h)**
   - Schedule: Every 6 hours (same as FB)
   - Secrets: GOOGLE_ADS_CLIENT_ID, GOOGLE_ADS_CLIENT_SECRET, GOOGLE_ADS_REFRESH_TOKEN, GOOGLE_ADS_CUSTOMER_ID
   - Test: Manual dispatch

3. **Setup Google Ads Campaign (4h - USER ACTION)**
   - Create Search + Display campaigns
   - Add Lead Form extensions
   - Get customer ID, setup OAuth
   - Test form submission

**Code Estimate:** 180 lines Python + 40 lines YAML
**Timeline:** 5 hours coding + 4 hours user setup = 9 hours total

---

#### Source 5: On-Site Newsletter/Contact Forms

**Integration Options (30min research):**
- **Option A:** Shopify Form Apps (e.g., Klaviyo, Mailchimp forms)
- **Option B:** Shopify webhook on customer creation
- **Option C:** Custom form with Shopify API

**Recommended:** Option B (Shopify webhook → catches all form submissions)

**Tasks:**
1. **Create Shopify webhook handler (3h)**
   - Create endpoint (Flask app or Shopify Function)
   - Webhook: `customers/create`, `customers/update`
   - Parse customer data (email, name, phone, tags)
   - Push to Google Sheet
   - Deploy: Vercel/Railway (free tier) or GitHub Pages (static webhook catcher)

2. **Create sync_shopify_forms_to_sheet.py (2h)**
   - Fallback: Shopify Admin API polling (if webhook fails)
   - Fetch customers created in last N hours
   - Filter by tags (e.g., "newsletter_subscriber")
   - Quality score: 8.0
   - Test: Create test customer → Sheet

3. **Create workflow sync-shopify-forms.yml (1h)**
   - Schedule: Every 4 hours (frequent for on-site forms)
   - Secrets: SHOPIFY_API_KEY, SHOPIFY_API_SECRET, SHOPIFY_SHOP_URL
   - Test: Manual dispatch

4. **Setup Shopify Forms (2h - USER ACTION)**
   - Install/configure form app or use native Shopify forms
   - Setup webhook endpoint
   - Test form submission

**Code Estimate:** 150 lines Python (webhook) + 120 lines Python (fallback) + 40 lines YAML
**Timeline:** 6 hours coding + 2 hours user setup = 8 hours total

---

#### Source 6: Blog Content Marketing

**Integration:** Blog post forms (Shopify blog + embedded forms)

**Tasks:**
1. **Reuse On-Site Form Integration (0h)**
   - Same Shopify webhook/API as Source 5
   - Tag customers with "blog_subscriber" or "lead_magnet"
   - Quality score: 7.5 (content-qualified)

2. **Create Lead Magnet Download Tracker (2h)**
   - Track downloads of PDFs/guides
   - Log email + resource downloaded
   - Append to Sheet with source: "blog_content"
   - Implementation: Shopify metafields or custom API

**Timeline:** 2 hours (lead magnet tracking only, form reuses Source 5)

---

#### Source 7: Instagram/TikTok Organic

**Integration:** Bio link clicks → Landing page → Form submission

**Tasks:**
1. **Create Link Tracker (3h)**
   - Use UTM parameters (e.g., `?utm_source=instagram&utm_campaign=bio_link`)
   - Capture UTM params when form submitted (Shopify or Typeform)
   - Enrich leads in Sheet with UTM data
   - Quality score: 7.0 (Instagram), 6.5 (TikTok)

2. **Update Existing Form Integrations (1h)**
   - Modify `sync_typeform_to_sheet.py` to capture UTM params
   - Modify `sync_shopify_forms_to_sheet.py` to capture UTM params
   - Map UTM source → Lead source column

3. **Create Landing Pages (2h - USER ACTION)**
   - Create Shopify pages for bio links (e.g., `/pages/instagram-exclusive`)
   - Embed forms (Typeform or Shopify)
   - Test: Click bio link → Submit form → Check UTM in Sheet

**Timeline:** 4 hours coding + 2 hours user setup = 6 hours total

---

#### Source 8: Customer Referral Program

**Integration:** Referral app (ReferralCandy, Smile.io, or custom)

**Tasks:**
1. **Research Referral App APIs (1h)**
   - ReferralCandy API: `https://api.referralcandy.com/v1/referrals`
   - Smile.io API: `https://api.smile.io/v1/customers/{customer_id}/referrals`
   - Authentication: API key

2. **Create sync_referrals_to_sheet.py (3h)**
   - Fetch referrals (last N hours)
   - Parse referee email + referrer email
   - Quality score: 8.5 (referred by customer)
   - Append to Sheet with source: "referral_program"
   - Test: Mock referral data → Sheet

3. **Create workflow sync-referrals.yml (1h)**
   - Schedule: Daily (referrals are less frequent)
   - Secrets: REFERRAL_APP_API_KEY
   - Test: Manual dispatch

4. **Setup Referral App (2h - USER ACTION)**
   - Choose app (ReferralCandy $49/mo or Smile.io $49/mo)
   - Configure rewards, install Shopify app
   - Get API credentials
   - Test referral flow

**Code Estimate:** 140 lines Python + 40 lines YAML
**Timeline:** 5 hours coding + 2 hours user setup = 7 hours total

---

#### Source 9: Email/Facebook Retargeting

**Integration:** Klaviyo + Facebook Pixel

**Tasks:**
1. **Create sync_klaviyo_engagement_to_sheet.py (3h)**
   - Track email engagement (opens, clicks) → NEW leads from engagement
   - Klaviyo API: Fetch profiles who engaged but not yet in DB
   - Quality score: 7.5 (warm leads)
   - Append with source: "email_retargeting"

2. **Create sync_facebook_retargeting_to_sheet.py (2h)**
   - Facebook Custom Audiences API (if accessible)
   - Or: Manual export of retargeting conversions → Import externes
   - Quality score: 7.5

3. **Create workflows (1h)**
   - `sync-klaviyo-engagement.yml` - Daily
   - `sync-facebook-retargeting.yml` - Daily
   - Test: Manual dispatch

4. **Setup Retargeting (3h - USER ACTION)**
   - Klaviyo: Create engagement segments
   - Facebook: Setup retargeting campaigns
   - Test: Engage with email → Check if tracked

**Code Estimate:** 150 lines Python (Klaviyo) + 100 lines Python (FB) + 80 lines YAML
**Timeline:** 6 hours coding + 3 hours user setup = 9 hours total

---

#### Source 10: Social Shares

**Integration:** Track social share buttons → New visitors → Form submissions

**Tasks:**
1. **Create Social Share Tracking (2h)**
   - Add social share buttons (AddThis, ShareThis, or custom)
   - Track share events → Google Analytics
   - Enrich form submissions with "referred by share" flag
   - Quality score: 6.5

2. **Integrate with Form Submissions (1h)**
   - Add hidden field to forms: `referral_source=social_share`
   - Capture in all form sync scripts
   - Append with source: "social_share"

**Timeline:** 3 hours coding (no user setup needed if using existing forms)

---

**PHASE 2 TOTAL:** 48 hours (coding + user setups)

---

### Week 9-10: PHASE 3 Source (1 source)

#### Source 11: YouTube Content

**Integration:** Video description links → Landing page → Form submissions

**Tasks:**
1. **Reuse UTM Tracking (0h)**
   - Same as Instagram/TikTok organic (Source 7)
   - UTM params: `?utm_source=youtube&utm_campaign=video_{video_id}`
   - Quality score: 7.5 (video engagement)

2. **YouTube Analytics Integration (Optional - 3h)**
   - YouTube Data API: Track video engagement
   - Correlate video views → Form submissions
   - Create dashboard: Video performance vs leads
   - NOT critical for lead capture, but useful for attribution

3. **Create Video Landing Pages (2h - USER ACTION)**
   - Create Shopify pages for video CTAs
   - Embed forms (Typeform or Shopify)
   - Test: Click video link → Submit form

**Timeline:** 3 hours coding (optional analytics) + 2 hours user setup = 5 hours total

---

**PHASE 3 TOTAL:** 5 hours

---

### Week 11-12: Testing & Optimization

#### End-to-End Testing (16 hours)

**Test Plan:**

1. **Integration Tests (8h)**
   - Test each of 11 sources individually
   - Mock API responses → Verify Sheet updates
   - Test error handling (API failures, rate limits)
   - Test duplicate detection across sources

2. **Workflow Tests (4h)**
   - Test all 11 GitHub Actions workflows
   - Verify cron schedules
   - Verify secrets access
   - Test manual dispatch for all workflows

3. **Performance Tests (2h)**
   - Test Sheet API rate limits (100 requests/100 seconds)
   - Test with high volume (1000+ leads/day)
   - Optimize batch operations if needed

4. **User Acceptance Tests (2h)**
   - Test manual import (xlsx, csv, json)
   - Test data quality (clean, segment, persona detection)
   - Test Analytics dashboard (charts update correctly)

**Test Deliverables:**
- ✅ Test report (pass/fail for each source)
- ✅ Integration test suite (pytest)
- ✅ Performance benchmarks

**Timeline:** 16 hours testing

---

## 📁 CODE STRUCTURE (All 11 Sources)

```
Alpha-Medical/
├── sync_typeform_to_sheet.py           # PHASE 1 - Contest (NEW)
├── sync_facebook_leads_to_sheet.py     # PHASE 1 - FB Ads (EXISTS)
├── import_leads_to_sheet.py            # PHASE 1 - Import (EXISTS, enhance JSON)
├── sync_google_ads_to_sheet.py         # PHASE 2 - Google Ads (NEW)
├── sync_shopify_forms_to_sheet.py      # PHASE 2 - On-site forms (NEW)
├── sync_blog_content_to_sheet.py       # PHASE 2 - Blog (reuses Shopify)
├── sync_referrals_to_sheet.py          # PHASE 2 - Referral program (NEW)
├── sync_klaviyo_engagement_to_sheet.py # PHASE 2 - Email retargeting (NEW)
├── sync_facebook_retargeting_to_sheet.py # PHASE 2 - FB retargeting (NEW)
├── track_social_shares.py              # PHASE 2 - Social shares (NEW)
├── track_youtube_links.py              # PHASE 3 - YouTube (reuses UTM tracking)
├── clean_and_segment_leads.py          # CENTRAL - Cleaning (EXISTS, enhance)
├── .github/workflows/
│   ├── sync-typeform-leads.yml         # Hourly 8AM-8PM
│   ├── sync-facebook-leads.yml         # Every 6h (EXISTS)
│   ├── sync-google-ads-leads.yml       # Every 6h
│   ├── sync-shopify-forms.yml          # Every 4h
│   ├── sync-referrals.yml              # Daily
│   ├── sync-klaviyo-engagement.yml     # Daily
│   ├── sync-facebook-retargeting.yml   # Daily
│   └── clean-segment-leads.yml         # Daily 10AM (EXISTS)
├── tests/
│   ├── test_typeform_integration.py
│   ├── test_facebook_integration.py
│   ├── test_google_ads_integration.py
│   ├── test_shopify_integration.py
│   ├── test_referral_integration.py
│   ├── test_retargeting_integration.py
│   ├── test_cleaning_script.py
│   └── test_end_to_end.py
└── IMPLEMENTATION_PLAN_3_PHASES.md     # This file
```

**Total Files:**
- 11 Python scripts (7 new, 4 existing/enhanced)
- 8 GitHub Actions workflows (5 new, 3 existing)
- 8 Test files (all new)
- **27 files total**

---

## ⏱️ TIMELINE SUMMARY

| Phase | Duration | Tasks | Deliverables |
|-------|----------|-------|--------------|
| **Week 1-2: Foundation** | 8h | Architecture, Sheet, Central script | ✅ Infrastructure ready |
| **Week 3-4: Phase 1** | 11h | Typeform, FB, Import | ✅ 3 sources coded |
| **Week 5-8: Phase 2** | 48h | Google Ads, Shopify, Blog, Social, Referral, Retargeting | ✅ 7 sources coded |
| **Week 9-10: Phase 3** | 5h | YouTube | ✅ 1 source coded |
| **Week 11-12: Testing** | 16h | Integration tests, E2E tests | ✅ All sources tested |
| **TOTAL BUILD** | **88 hours** | 27 files | ✅ Complete infrastructure |

**Infrastructure Readiness:** Week 13 (end of Week 12 + 1 week buffer)

---

## 🚀 DEPLOYMENT TIMELINE (Phased Activation)

### PHASE 1: PRE-LAUNCH (Week 13 - Nov 2025)

**Activate:** 3 sources (Typeform, FB Ads, Import)

**User Actions:**
1. Create Typeform contest form (2h)
2. Launch FB Ads campaign (3h)
3. Prepare import files (1h)
4. Enable workflows in GitHub Actions (30min)

**Testing Period:** 1 week (Week 13)
- Monitor: 500-1000 test leads
- Verify: Data quality, no errors, analytics accurate

**Go-Live:** Week 14 (contest launch)

**Timeline:** Week 13-14 (2 weeks)

---

### PHASE 2: POST-LAUNCH (Week 26 - Month 1-3 after launch)

**Activate:** 7 sources (Google Ads, Shopify, Blog, Social, Referral, Retargeting, Social shares)

**Prerequisites:**
- ✅ Store launched (revenue > $10K/month)
- ✅ 1,500+ leads from Phase 1
- ✅ Budget approved for Google Ads ($3-5K/month)

**User Actions:**
1. Launch Google Ads campaigns (4h)
2. Install referral app (ReferralCandy/Smile) (2h)
3. Configure on-site forms (2h)
4. Setup retargeting campaigns (3h)
5. Create blog content with lead magnets (ongoing)
6. Enable 7 workflows (1h)

**Testing Period:** 2 weeks (Week 26-27)
- Monitor: 1000+ leads/month from new sources
- Verify: Source attribution accurate, no conflicts

**Timeline:** Week 26-28 (3 weeks)

---

### PHASE 3: SCALE (Week 39 - Month 4-12 after launch)

**Activate:** 1 source (YouTube)

**Prerequisites:**
- ✅ 5,000+ total leads
- ✅ Content team ready (video production)

**User Actions:**
1. Create YouTube channel (if not exists) (1h)
2. Upload first 3-5 videos with CTAs (ongoing)
3. Create video landing pages (2h)
4. Enable UTM tracking (already active from Phase 2)

**Timeline:** Week 39-40 (2 weeks)

---

## 💰 COST BREAKDOWN (Infrastructure + Operations)

### Infrastructure Build (One-Time)

| Item | Hours | Rate | Cost |
|------|-------|------|------|
| **Development (88h)** | 88h | $0 (in-house) | $0 |
| **Testing** | 16h | $0 (in-house) | $0 |
| **User Setups** | 30h | $0 (internal) | $0 |
| **TOTAL BUILD** | 118h | - | **$0** |

---

### Operational Costs (Monthly)

#### PHASE 1 (Active - Nov-Dec 2025)
- Typeform: $0 (free tier up to 100 responses/month) or $25/mo (Pro plan)
- Facebook Ads: $6,000 (one-time 20-day campaign)
- Import: $0
- Apify (insights): $97.80/mo
- **TOTAL PHASE 1:** $97.80/mo + $6,000 one-time

#### PHASE 2 (Month 1-3)
- Google Ads: $3,000-5,000/mo
- Referral App: $49-99/mo (ReferralCandy/Smile)
- Shopify Forms: $0 (native)
- Blog: $0 (organic)
- Retargeting: Variable (included in ad spend)
- Social shares: $0 (organic)
- **TOTAL PHASE 2:** +$3,049-5,099/mo

#### PHASE 3 (Month 4-12)
- YouTube: $0 (organic)
- **TOTAL PHASE 3:** +$0/mo

**Cumulative Monthly Cost:**
- Month 0 (build): $0
- Month 1-2 (Phase 1): $97.80/mo
- Month 3-5 (Phase 2): $3,146.80-5,196.80/mo
- Month 6-12 (Phase 3): $3,146.80-5,196.80/mo (same)

---

## 🎯 SUCCESS METRICS (Testing Phase)

### Infrastructure Testing (Week 11-12)

| Metric | Target | Test Method |
|--------|--------|-------------|
| **API Success Rate** | >99% | 1000 API calls per source |
| **Data Accuracy** | 100% | Compare API response vs Sheet data |
| **Duplicate Detection** | 100% | Submit 50 duplicate leads |
| **Error Handling** | 0 crashes | Simulate API failures (5 per source) |
| **Workflow Reliability** | 100% | Run all workflows 10 times |
| **Sheet Performance** | <5s per batch | Batch insert 100 leads |

### Phase 1 Testing (Week 13)

| Metric | Target | Monitoring |
|--------|--------|------------|
| **Typeform Sync** | 100% of submissions | Check Sheet vs Typeform responses |
| **FB Ads Sync** | 100% of leads | Check Sheet vs FB Ads Manager |
| **Import Success** | 100% of files | Test 10 files (xlsx, csv, json) |
| **Data Quality** | >95% valid emails | Check email validation results |
| **Cleaning Script** | 0 errors | Monitor daily logs |

### Phase 2 Testing (Week 26-27)

| Metric | Target | Monitoring |
|--------|--------|------------|
| **Google Ads Sync** | 100% of submissions | Check Sheet vs Google Ads |
| **Shopify Forms** | 100% of submissions | Check Sheet vs Shopify customers |
| **Referral Tracking** | 100% of referrals | Check Sheet vs Referral app |
| **UTM Attribution** | 100% accuracy | Test 50 links with UTM params |
| **Source Conflicts** | 0 conflicts | Check no duplicate syncs |

---

## 🛠️ DEVELOPMENT PRIORITY (Next Steps)

### Immediate (This Session)
1. **Create sync_typeform_to_sheet.py** (3h)
2. **Create sync-typeform-leads.yml** (1h)
3. **Enhance import_leads_to_sheet.py for JSON** (1h)
4. **Update clean_and_segment_leads.py for 11 sources** (2h)

**Session Goal:** Complete Phase 1 code (7 hours)

---

### Week 2-4 (Next 2 Weeks)
1. Create Phase 2 scripts (7 sources) - 35h
2. Create Phase 2 workflows (7 workflows) - 7h
3. Build test suite (8 test files) - 12h

**Goal:** All code ready for testing

---

### Week 5-6 (Testing)
1. Integration tests (8h)
2. Workflow tests (4h)
3. Performance tests (2h)
4. UAT (2h)

**Goal:** All tests passing, ready for Phase 1 deployment

---

## 📋 DEPENDENCIES & BLOCKERS

### Critical Path

```
Week 1-2: Foundation
    ↓
Week 3-4: Phase 1 Code → BLOCKS → Phase 1 Testing (Week 13)
    ↓
Week 5-8: Phase 2 Code → BLOCKS → Phase 2 Testing (Week 26)
    ↓
Week 9-10: Phase 3 Code → BLOCKS → Phase 3 Testing (Week 39)
    ↓
Week 11-12: All Testing → BLOCKS → Production Deployment
```

### External Dependencies

1. **Typeform Form** - USER must create (blocks Week 13 testing)
2. **FB Ads Campaign** - USER must launch (blocks Week 13 testing)
3. **Google Ads Campaign** - USER must launch (blocks Week 26 testing)
4. **Referral App** - USER must install (blocks Week 26 testing)
5. **Google Sheets** - Already exists (no blocker)

### Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| API rate limits | Medium | Implement exponential backoff, caching |
| Sheet API quota exceeded | High | Batch operations, optimize writes |
| Workflow failures | Medium | Retry logic, error notifications |
| User setup delays | High | Provide detailed setup guides + videos |
| Budget constraints (Phase 2) | Medium | Phase 2 can start with fewer sources |

---

## ✅ ACCEPTANCE CRITERIA

### Infrastructure Complete (Week 12)

- [ ] All 11 Python scripts written + documented
- [ ] All 8 GitHub Actions workflows configured
- [ ] All 8 test files passing (100% coverage)
- [ ] Google Sheet structure complete with formulas
- [ ] Setup guides written for all 11 sources
- [ ] Test environment validated (mock data works)

### Phase 1 Ready (Week 13)

- [ ] Typeform form created + tested
- [ ] FB Ads campaign launched + tested
- [ ] Import script tested with real files
- [ ] 100+ test leads processed successfully
- [ ] Analytics dashboard showing accurate data
- [ ] No errors in logs for 7 consecutive days

### Phase 2 Ready (Week 26)

- [ ] Google Ads campaign launched
- [ ] Referral app installed + configured
- [ ] Shopify forms capturing submissions
- [ ] Blog lead magnets tracking downloads
- [ ] UTM tracking working for social sources
- [ ] Retargeting campaigns active
- [ ] 1000+ leads/month from new sources

### Phase 3 Ready (Week 39)

- [ ] YouTube channel active with 5+ videos
- [ ] Video landing pages created
- [ ] UTM tracking for YouTube working
- [ ] 200+ leads/month from YouTube

---

## 📖 NEXT ACTIONS (Ordered Priority)

**NOW (This Session):**
1. Create `sync_typeform_to_sheet.py`
2. Create `.github/workflows/sync-typeform-leads.yml`
3. Enhance `import_leads_to_sheet.py` (add JSON support)
4. Update `clean_and_segment_leads.py` (handle 11 sources)

**THIS WEEK:**
5. Create test suite for Phase 1 (3 tests)
6. Document setup guides for Typeform + FB Ads

**NEXT WEEK:**
7. Start Phase 2 scripts (Google Ads first)
8. Create Shopify integration
9. Build referral program integration

**WEEK 3:**
10. Complete remaining Phase 2 integrations
11. Build Phase 3 (YouTube tracking)
12. Full test suite for all sources

**WEEK 4:**
13. End-to-end testing (all 11 sources)
14. Performance optimization
15. User acceptance testing prep

---

**Ready to start building. Commençons par Phase 1?**

1. Créer `sync_typeform_to_sheet.py` maintenant?
2. Ou préférez-vous voir d'abord un autre script (ex: Google Ads)?
3. Ou créer les tests d'abord?

Quelle est votre priorité immédiate?
