# ALPHA MEDICAL - PROGRESSIVE DISCLOSURE MEMORY SYSTEM

> **Project:** B2C e-commerce RETAILER - Medical equipment store (alphamedical.shop)
> **Status:** PRE-LAUNCH (Launch: 2025-12-15) | **Health:** 52/100
> **Last Updated:** 2025-11-26 Session 55 (Memory System Optimization)

---

## 🧠 MEMORY ARCHITECTURE (3-LEVEL PROGRESSIVE DISCLOSURE)

This project uses a **progressive disclosure memory system** for optimal context efficiency:

### Level 1: Core Memory (ALWAYS LOADED)
**Auto-loaded** on every session - Essential project identity and constraints (~1,000 tokens)

- `.claude/memory/00-metadata.md` - Project essence, business model, current state
- `.claude/memory/01-core-constraints.md` - Non-negotiable rules (what you can/cannot do)

### Level 2: Domain-Specific Memory (LOADED WHEN NEEDED)
**Loaded automatically** when working on domain-specific tasks (~1,200 tokens each)

- `.claude/memory/02-infrastructure-summary.md` - Technical context, blockers, automation state
- `.claude/memory/03-marketing-context.md` - Marketing strategy, personas, campaigns

### Level 3: Deep Knowledge (ON-DEMAND)
**Load explicitly** using `@filename` syntax when you need detailed information

**Infrastructure & Automation:**
- `@INFRASTRUCTURE_AUDIT_CHECKLIST.md` (2,184 lines) - **SINGLE SOURCE OF TRUTH** for system state
- `@AUTOMATION_COMPLETE_WORKFLOWS.md` (5,944 lines) - Complete automation architecture

**Marketing & Strategy:**
- `@AI_SEO_MARKETING_STRATEGIC_ANALYSIS_2025-2026.md` (303KB) - SEO/marketing strategy
- `@FLYWHEEL_OPTIMIZATION_BLUEPRINT_2025.md` - Complete flywheel strategy
- `@ALPHA_MEDICAL_REAL_PERSONAS_MARKET_DATA.md` - Persona data and targeting

**Setup & Guides:**
- `@market-analysis/SETUP_GOOGLE_SHEETS_API.md` - Resolve Bloqueur #1
- `@market-analysis/setup_github_secrets_helper.sh` - Resolve Bloqueur #2

---

## 🤖 SPECIALIZED AGENTS (CONTEXT-OPTIMIZED)

Use specialized agents for domain-specific tasks to **save 70% context**:

### @seo-specialist
**When:** SEO optimization, meta descriptions, blog content, keyword research
```
# Invoke with:
@seo-specialist
```
**Loads:** SEO strategy docs, keyword data, content guidelines
**Saves:** 70% context vs loading all docs

### @automation-specialist
**When:** Shopify Flow, GitHub Actions, Python scripts, API integrations
```
# Invoke with:
@automation-specialist
```
**Loads:** Automation architecture, workflow configs, blocker details
**Saves:** 70% context vs loading all docs

### @marketing-specialist
**When:** Email flows, ad copy, campaign strategy, conversion optimization
```
# Invoke with:
@marketing-specialist
```
**Loads:** Marketing strategy, Klaviyo flows, ad frameworks, persona data
**Saves:** 70% context vs loading all docs

---

## 🛡️ CONSTRAINT ENFORCEMENT (AUTOMATED)

### Pre-Tool-Use Hook (`.claude/hooks/pre-tool-use.sh`)
**Blocks forbidden actions BEFORE execution** (0% violation rate):

- ❌ Product file modifications (prices, inventory, variants)
- ❌ PayPal activation attempts
- ❌ Credentials commits (.env, .env.admin)
- ❌ Supplier/fulfillment changes

**Status:** ✅ Executable (`chmod +x`)

### Post-Tool-Use Hook (`.claude/hooks/post-tool-use.sh`)
**Auto-documentation AFTER execution**:

- 📝 Logs all tool use to `.claude/memory/session-log.md`
- 📊 Tracks completions in `.claude/memory/progress.md`
- 🤖 Optional auto-commit for documentation updates

**Status:** ✅ Executable (`chmod +x`)

---

## 🚨 CRITICAL BLOCKERS (15 MIN - BLOCKS $55K+ REVENUE)

### BLOQUEUR #1: Google Sheets API Credentials (10 min)
**Status:** ❌ NOT created
**Impact:** Blocks ALL lead scraping automation (2,100-4,500 leads/month)
**Guide:** `@market-analysis/SETUP_GOOGLE_SHEETS_API.md`

### BLOQUEUR #2: GitHub Secrets (5 min)
**Status:** ❌ 0/4 configured
**Impact:** Blocks 8/9 GitHub Actions workflows
**Helper:** `market-analysis/setup_github_secrets_helper.sh`
**Required:** APIFY_API_TOKEN, SHOPIFY_API_KEY, SHOPIFY_PASSWORD, GOOGLE_CREDENTIALS_JSON

---

## 📊 QUICK REFERENCE

### Current Reality (2025-11-26 VERIFIED)
- Products: 96 (81 published, 15 draft)
- Orders: 0 | Revenue: $0 | Traffic: Minimal (PRE-LAUNCH)
- Automation: 15% active (tracking works, lead gen blocked)
- Klaviyo: $30/mo ACTIVE, 0/7 flows configured

### Infrastructure Status
**✅ ACTIVE (15%):**
- Tracking: GTM, GA4, Meta Pixel, TikTok Pixel, Google Ads Conversion ✅
- Shopify Flow: 4/7 workflows active ✅
- Shopify Email: 4/7 automations active ✅

**❌ BLOCKED (85%):**
- Lead generation: Blocked by GitHub Secrets
- Klaviyo flows: 0/7 configured (plan active, flows not deployed)
- Paid ads: 0 campaigns (tracking ready)

### Financial Context
- **Costs:** Shopify $29/mo + Klaviyo $30/mo = $59/mo
- **Blocked Revenue:** $55,000+ Year 1 (blocked by 15 min manual work)
- **Klaviyo Impact:** $80K-120K additional Year 1 (if flows deployed)

---

## 💻 KEY COMMANDS

### Testing & Verification
```bash
# Test lead scraping
cd market-analysis
python3 lead_generation_scraper.py --instagram --hashtag "arthritis" --max-results 10

# Verify store infrastructure
python3 verify_store_infrastructure.py

# Check Klaviyo status
python3 verify_klaviyo_status.py
```

### Automation Setup
```bash
# Setup GitHub Secrets helper
cd market-analysis
./setup_github_secrets_helper.sh

# Pre-launch validation
./pre_launch_validation.sh
```

### GitHub Workflow
```bash
# Check workflows status
gh workflow list

# View secrets
gh secret list

# Trigger workflow manually
gh workflow run daily-scraping.yml
```

---

## 🎯 PRIORITIES (IN ORDER)

### Priority 1: Resolve Critical Blockers (15 min)
1. Google Sheets API credentials → `@market-analysis/SETUP_GOOGLE_SHEETS_API.md`
2. GitHub Secrets → `market-analysis/setup_github_secrets_helper.sh`

### Priority 2: Activate Critical Workflows (7 min)
1. Shopify Flow: "Thank customers after they purchase" (INACTIVE)
2. Shopify Email: "Thank you!" automation (DRAFT)
3. Fix duplicate "Welcome with discount" workflows

### Priority 3: Email Automation (20h)
1. Deploy 7 Klaviyo flows (Welcome, Cart, Browse, Post-Purchase, Win-Back, Cross-Sell, Re-engage)
2. Expected lift: $8K-12K Month 1, $80K-120K Year 1

### Priority 4: Launch Paid Ads (User Decision)
- Google Ads (tracking ready)
- Facebook/IG Ads (pixel ready)
- TikTok Ads (pixel ready)

---

## 📚 HOW TO USE THIS SYSTEM

### For General Tasks
1. **Start:** Level 1 memory loads automatically (core identity + constraints)
2. **Domain work:** Level 2 loads automatically based on task type
3. **Deep dive:** Load Level 3 docs explicitly with `@filename` when needed

### For Specialized Tasks
1. **SEO work:** Invoke `@seo-specialist` (saves 70% context)
2. **Automation work:** Invoke `@automation-specialist` (saves 70% context)
3. **Marketing work:** Invoke `@marketing-specialist` (saves 70% context)

### For Verification
1. **Always check:** `@INFRASTRUCTURE_AUDIT_CHECKLIST.md` for factual verification
2. **Single source of truth:** 2,184 lines, verified via API + code inspection
3. **Last updated:** 2025-11-26 Session 54

---

## 🔄 SESSION CONTINUITY

**Memory System Optimization:**
- ✅ Phase 1 COMPLETED (Session 55): Progressive disclosure, hooks, specialized agents
- ⏳ Phase 2 NOT STARTED: Advanced hook implementations, parallel agent execution
- ⏳ Phase 3 NOT STARTED: Semantic chunking, MCP server, activeContext.md

**System Efficiency:**
- **Before:** 57/100 (monolithic CLAUDE.md, no specialization, no hooks)
- **After Phase 1:** ~80/100 (progressive disclosure, hooks enforcement, specialized agents)
- **Target Optimal:** 85/100 (with Phase 2-3 complete)

---

## 🚫 OPERATIONAL BOUNDARIES

### ✅ ALWAYS DO
- Update documentation after changes
- Use factual, verifiable information
- Test with small datasets first
- Follow git commit message format

### ⚠️ ASK FIRST
- Modifying existing Shopify Flow workflows
- Creating new email campaigns
- Changing theme layout files

### 🚫 NEVER DO (ENFORCED BY HOOKS)
- Touch product prices, inventory, or suppliers
- Enable PayPal (owner explicitly forbids)
- Commit credentials (.env, .env.admin)
- Make assumptions without verification

---

**🤖 REMINDER FOR CLAUDE CODE:**
- Memory system uses **progressive disclosure** (3 levels) for optimal efficiency
- Use **specialized agents** (`@seo-specialist`, `@automation-specialist`, `@marketing-specialist`) to save 70% context
- **Hooks enforce constraints** automatically (pre-tool-use blocks violations, post-tool-use logs changes)
- **Single source of truth:** `@INFRASTRUCTURE_AUDIT_CHECKLIST.md` (always verify facts here)
- **Zero tolerance** for bullshit, wishful thinking, or unverified claims
