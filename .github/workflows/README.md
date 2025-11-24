# GitHub Actions Workflows - Alpha Medical

This directory contains automated workflows for Alpha Medical e-commerce operations.

## 🚀 Active Workflows

### 1. **Daily Multi-Platform Lead Scraping** (`daily-scraping.yml`)

**Schedule:** 9:00 AM UTC daily (replaces local cron job)

**Purpose:** Scrapes consumer intelligence from Instagram, Facebook, TikTok

**Volumes (Progressive):**
- Month 1: 2,100 leads/month (700 per platform)
- Month 2: 3,000 leads/month (1,000 per platform)
- Month 3+: 4,500 leads/month (1,500 per platform)

**Features:**
- Parallel platform execution for speed
- Automatic volume adjustment based on launch date
- Google Sheets sync integration
- Artifact upload (30 days retention)

**Manual Trigger:** Available via workflow_dispatch

### 2. **Weekly Shopify Backup** (`shopify-backup.yml`)

**Schedule:** Every Sunday at midnight UTC

**Purpose:** Backup Shopify products, collections, metafields

**Features:**
- Exports all products as JSON
- Commits backups to repository
- 90-day artifact retention
- Version control for recovery

### 3. **API Health Check** (`health-check.yml`)

**Schedule:** Every 6 hours

**Purpose:** Monitor API availability and create alerts

**Monitors:**
- Shopify store (https://alphamedical.shop)
- Apify API
- Google Sheets API (if configured)
- GA4/GTM tags presence

**Features:**
- Auto-creates GitHub issue on failure
- Detailed health summary
- 24/7 monitoring

### 4. **Python Tests & Code Quality** (`tests.yml`)

**Trigger:** Push to main branch or manual

**Purpose:** Quality assurance for Python scripts

**Checks:**
- Flake8 linting
- Syntax validation
- Import tests
- Code quality metrics

---

## 🔐 Required GitHub Secrets

To enable all workflows, configure these secrets in **Settings → Secrets and variables → Actions**:

### **APIFY_API_TOKEN** (Required)
- **Description:** Apify API token for scraping
- **Where to get:** https://console.apify.com/account/integrations
- **Used by:** `daily-scraping.yml`, `health-check.yml`

### **SHOPIFY_API_KEY** (Required for backup)
- **Description:** Shopify Admin API key
- **Where to get:** Shopify Admin → Apps → Develop apps
- **Used by:** `shopify-backup.yml`

### **SHOPIFY_PASSWORD** (Required for backup)
- **Description:** Shopify Admin API password/token
- **Where to get:** Same as API key
- **Used by:** `shopify-backup.yml`

### **GOOGLE_CREDENTIALS_JSON** (Optional)
- **Description:** Google Sheets service account credentials (JSON format)
- **Where to get:** Follow `market-analysis/SETUP_GOOGLE_SHEETS_API.md`
- **Used by:** `daily-scraping.yml`, `health-check.yml`

---

## 📋 Setup Instructions

### Step 1: Add Secrets

1. Go to: **https://github.com/Jouiet/Alpha-Medical-New/settings/secrets/actions**
2. Click **"New repository secret"**
3. Add each secret listed above

### Step 2: Update Launch Date

Edit `.github/workflows/daily-scraping.yml` and update:

```yaml
LAUNCH_DATE="2025-12-15"  # Update with actual launch date
```

### Step 3: Enable Workflows

Workflows are automatically enabled. First run will be:
- Daily scraping: Next 9:00 AM UTC
- Weekly backup: Next Sunday midnight UTC
- Health check: Within 6 hours
- Tests: On next push to main

### Step 4: Manual Testing

Test workflows manually before scheduled runs:

1. Go to: **Actions tab** in GitHub
2. Select workflow (e.g., "Daily Multi-Platform Lead Scraping")
3. Click **"Run workflow"**
4. Select options and click **"Run workflow"**

---

## 💰 Cost & Limits

**GitHub Actions Free Tier:**
- **Public repos:** Unlimited minutes ✅
- **Private repos:** 2,000 minutes/month
- **Storage:** 500 MB artifacts

**Estimated Usage (Alpha Medical):**
- Daily scraping: ~15 min/day = 450 min/month
- Weekly backup: ~5 min/week = 20 min/month
- Health checks: ~2 min × 4/day = 240 min/month
- Tests: ~5 min × 20/month = 100 min/month
- **Total: ~810 min/month** (well under 2,000 limit)

---

## 📊 Monitoring & Logs

### View Workflow Runs

**URL:** https://github.com/Jouiet/Alpha-Medical-New/actions

**What you'll see:**
- Real-time execution status
- Detailed logs per step
- Success/failure history
- Execution time metrics

### Download Artifacts

Artifacts are available for download after each run:
- Scraped leads: 30 days retention
- Shopify backups: 90 days retention

### Health Check Alerts

Failed health checks automatically create GitHub issues with label `health-check`.

---

## 🔄 Migration from Local Cron

**Before (Local Cron):**
```bash
# Runs on your machine at 9:00 AM
0 9 * * * /Users/mac/Desktop/Alpha-Medical/market-analysis/daily_lead_scraping.sh
```

**After (GitHub Actions):**
- Runs in GitHub cloud (more reliable)
- No dependency on local machine
- Automatic logs and artifact storage
- Built-in failure notifications

**To Disable Local Cron:**
```bash
crontab -e
# Comment out or delete the Alpha Medical cron line
```

---

## ✅ Advantages vs Local Cron

| Feature | Local Cron | GitHub Actions |
|---------|------------|----------------|
| **Reliability** | Depends on local machine | Cloud-based (99.9% uptime) |
| **Logs** | Manual | Automatic + searchable |
| **Notifications** | None | Auto-create issues on failure |
| **Artifacts** | Local files | Cloud storage (90 days) |
| **Version Control** | No | Yes (workflows in Git) |
| **Cost** | $0 | $0 (free tier) |
| **Monitoring** | Manual | Built-in dashboards |

---

## 🛠️ Troubleshooting

### Workflow Failed with "Secret not found"

**Solution:** Add the required secret in repository settings

### Scraping Returns 0 Leads

**Check:**
1. APIFY_API_TOKEN is valid
2. Apify account has credits
3. Check workflow logs for API errors

### Google Sheets Sync Failed

**Check:**
1. GOOGLE_CREDENTIALS_JSON is correctly formatted
2. Service account has access to sheet
3. Sheet name matches: "Alpha Medical - Lead Management"

### Shopify Backup Failed

**Check:**
1. SHOPIFY_API_KEY and SHOPIFY_PASSWORD are correct
2. API credentials have read access
3. Shopify admin API is enabled

---

## 📝 Workflow File Structure

```
.github/workflows/
├── daily-scraping.yml       # Multi-platform lead scraping
├── shopify-backup.yml       # Weekly Shopify data backup
├── health-check.yml         # API monitoring every 6h
├── tests.yml                # Python code quality checks
└── README.md                # This file
```

---

## 🎯 Next Steps

1. ✅ **Add GitHub Secrets** (required before first run)
2. ✅ **Update launch date** in daily-scraping.yml
3. ✅ **Test workflows manually** before scheduled runs
4. ✅ **Monitor first runs** in Actions tab
5. ✅ **Disable local cron** once GitHub Actions proven working

---

**GitHub Actions Status:** ✅ Ready for production
**Repository:** https://github.com/Jouiet/Alpha-Medical-New
**Documentation:** Complete
**Cost:** $0 (free tier sufficient)
