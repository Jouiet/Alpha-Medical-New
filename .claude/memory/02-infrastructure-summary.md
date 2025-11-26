# INFRASTRUCTURE SUMMARY - TECHNICAL CONTEXT

> **Level 2 Memory - LOADED WHEN: Technical tasks, automation, debugging**

---

## 🚨 CRITICAL BLOCKERS (15 MIN - BLOCKS $55K+ REVENUE)

### BLOQUEUR #1: Google Sheets API Credentials (10 min)
**Status:** ❌ NOT created
**Impact:** Blocks ALL lead scraping automation (2,100-4,500 leads/month)
**Guide:** `market-analysis/SETUP_GOOGLE_SHEETS_API.md`

**Steps:**
1. Go to https://console.cloud.google.com/
2. Create project: "Alpha Medical Automation"
3. Enable Google Sheets API
4. Create service account
5. Download JSON credentials
6. Share Google Sheet with service account email
7. Copy JSON to GitHub Secret: GOOGLE_CREDENTIALS_JSON

### BLOQUEUR #2: GitHub Secrets (5 min)
**Status:** ❌ 0/4 configured
**Impact:** Blocks 8/9 GitHub Actions workflows

**Required Secrets:**
- APIFY_API_TOKEN (from console.apify.com/account/integrations)
- SHOPIFY_API_KEY (from .env.admin file)
- SHOPIFY_PASSWORD (from .env.admin file)
- GOOGLE_CREDENTIALS_JSON (from Bloqueur #1)

**Helper:** `market-analysis/setup_github_secrets_helper.sh`

---

## 📊 INFRASTRUCTURE STATE (2025-11-26)

### ✅ WHAT WORKS (15%)

**Tracking Stack (100% ACTIVE):**
```yaml
GTM Container: GTM-WFPH2KZP
├── GA4: Via GTM tags ✅
├── Meta Pixel: Via GTM tags ✅
├── TikTok Pixel: Via GTM tags ✅
└── Google Ads Conversion: AW-17749024238 ✅

Location: layout/theme.liquid:461
Status: All firing correctly
Performance: 95/100
```

**Shopify Flow (4/7 workflows ACTIVE):**
```yaml
Active Workflows:
├── "New Loyalty Tier Tagging (Automatic)" ✅
├── "Convert abandoned product browse" ✅
├── "Recover abandoned cart" ✅
└── "Recover abandoned checkout" ✅

Inactive Workflows (CRITICAL):
├── "Thank customers after they purchase" ❌ (2 min to activate)
└── "Welcome new subscribers..." (duplicates) ❌ (3 min to fix)
```

**Shopify Email (4/7 automations ACTIVE):**
```yaml
Active Automations:
├── "We're happy to see you again" ✅
├── "Did something catch your eye?" ✅
├── "You left items in your cart" ✅
└── "You left items at checkout" ✅

Draft Automations (SHOULD BE ACTIVE):
├── "Thank you!" ❌
└── "Welcome with discount" (duplicates) ❌
```

**Apps Installed (7/7):**
- Shopify Email ✅
- Klaviyo ✅ (plan $30/mo ACTIVE, 0/7 flows configured)
- Shopify Flow ✅
- Loox Reviews ✅
- DSers ✅
- Translate & Adapt ✅
- Alpha Medical New (theme) ✅

### ❌ WHAT'S BLOCKED (85%)

**Lead Generation:**
- Apify scraping: ❌ Scripts ready, blocked by GitHub Secrets
- Google Sheets sync: ❌ Blocked by API credentials
- 9 GitHub Actions workflows: ❌ 8/9 blocked by secrets

**Email Automation:**
- Klaviyo flows: ❌ 0/7 created (plan $30/mo active, flows NOT configured)
- Shopify Flow: ❌ "Thank customers" INACTIVE (CRITICAL)
- Shopify Email: ❌ "Thank you!" in DRAFT (CRITICAL)

**Paid Ads:**
- Google Ads: ⏳ Conversion tracking ready, 0 campaigns
- Facebook/IG Ads: ⏳ Pixel active, 0 campaigns
- TikTok Ads: ⏳ Pixel active, 0 campaigns

---

## 🏗️ PROJECT STRUCTURE

```
Alpha-Medical/
├── .github/workflows/       # 9 GitHub Actions (8 blocked by secrets)
│   ├── daily-scraping.yml            ❌ Blocked
│   ├── sync-typeform-leads.yml       ❌ Blocked
│   ├── sync-facebook-leads.yml       ❌ Blocked
│   ├── sync-klaviyo-leads.yml        ❌ Blocked
│   ├── clean-segment-leads.yml       ❌ Blocked
│   ├── shopify-backup.yml            ❌ Blocked
│   ├── health-check.yml              ❌ Blocked
│   ├── tests.yml                     ✅ Executable
│   └── update-llms-txt.yml           ✅ Active
│
├── market-analysis/         # Lead generation + automation scripts
│   ├── lead_generation_scraper.py        # Apify scraping
│   ├── sync_leads_to_sheets.py           # Google Sheets sync
│   ├── daily_lead_scraping.sh            # Cron automation
│   ├── setup_github_secrets_helper.sh    # Secrets setup
│   └── SETUP_GOOGLE_SHEETS_API.md        # Bloqueur #1 guide
│
├── assets/                  # JS/CSS (39 JS, 68 CSS files)
├── layout/                  # Theme layout files
│   └── theme.liquid        # GTM at line 461
├── sections/                # Shopify sections (66 files)
├── snippets/                # Reusable components (70 files)
│   ├── welcome-popup.liquid       # 10% OFF popup
│   └── exit-intent-popup.liquid   # 15% OFF exit intent
├── templates/               # Page templates (32 files)
│
└── .claude/                 # Claude Code memory system
    ├── memory/              # Progressive disclosure context
    ├── hooks/               # Automation hooks
    └── agents/              # Specialized agents
```

---

## 💻 KEY COMMANDS

### Development
```bash
# View theme files
cat layout/theme.liquid | grep -A5 GTM

# Check GitHub Actions status
gh workflow list

# View GitHub Secrets
gh secret list
```

### Testing & Verification
```bash
# Test lead scraping
cd market-analysis
python3 lead_generation_scraper.py --instagram --hashtag "arthritis" --max-results 10

# Verify store status
python3 verify_store_infrastructure.py

# Check Klaviyo status
python3 verify_klaviyo_status.py
```

### Automation Setup
```bash
# Setup GitHub Secrets (helper)
cd market-analysis
./setup_github_secrets_helper.sh

# Pre-launch validation
./pre_launch_validation.sh
```

### Git Workflow
```bash
# Current branch: main
# Remote: https://github.com/Jouiet/Alpha-Medical-New.git

git status
git add <files>
git commit -m "type(scope): description

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin main
```

---

## 🎯 CURRENT PRIORITIES

### Priority 1: Resolve Critical Blockers (15 min)
1. Google Sheets API credentials → `SETUP_GOOGLE_SHEETS_API.md`
2. GitHub Secrets → `setup_github_secrets_helper.sh`

### Priority 2: Activate Critical Workflows (7 min)
1. Shopify Flow: Activate "Thank customers after they purchase" (2 min)
2. Shopify Email: Activate "Thank you!" automation (2 min)
3. Resolve "Welcome with discount" duplicates (3 min)

### Priority 3: Email Automation (20h)
1. ✅ Klaviyo Plan: ACTIVE $30/mo (1,000 profiles, 10K emails/mo)
2. ❌ Deploy 7 Klaviyo flows: Welcome, Abandoned Cart, Browse, Post-Purchase, Win-Back
3. Expected lift: $8K-12K Month 1, $80K-120K Year 1

---

## 💰 FINANCIAL CONTEXT

**Costs:**
- Shopify Basic: $29/mo
- Klaviyo: $30/mo ACTIVE
- Apps: Cost TBD (Loox verified)
- Apify: $0/mo (free tier)

**ROI Projections:**
- Klaviyo: 19-29× ROI Year 1
- Lead scraping: 40-800× cheaper than paid ads
- Email automation: 27-30% of revenue (industry benchmark)

**Revenue Blocked:** $55,000+ Year 1 by 15 minutes of work

---

## 🔄 SESSION CONTINUITY

**Last Updated:** 2025-11-26 Session 54

**Recent Changes:**
- ✅ Google Ads Conversion tracking verified (AW-17749024238)
- ✅ Shopify Flow/Email states documented
- ✅ Documentation updated (INFRASTRUCTURE, AUTOMATION)
- ✅ Progressive disclosure memory system implemented

**Blockers Status:**
- ✅ Klaviyo plan: RESOLVED - $30/mo active (Session 49)
- ❌ Google Sheets API: Still not created
- ❌ GitHub Secrets: Still 0/4 configured

---

**Token Cost:** ~1,200 tokens (Level 2 - loaded when technical tasks)
**Full Reference:** `@INFRASTRUCTURE_AUDIT_CHECKLIST.md` (2,184 lines)
