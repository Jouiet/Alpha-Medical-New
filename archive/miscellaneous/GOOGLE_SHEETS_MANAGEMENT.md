# GOOGLE SHEETS MANAGEMENT - Alpha Medical

## 📊 Overview

Google Sheet: **"Alpha Medical - Lead Management"**
- Tab 1: **Raw Leads** - All scraped leads with deduplication
- Tab 2: **Qualified Leads** - Manually qualified leads
- Tab 3: **Dashboard** - Analytics and metrics

---

## 🛠️ Tools

### 1. `sync_leads_to_sheets.py` - Smart Lead Sync

**Automatic duplicate prevention** - Never adds the same lead twice!

**Usage:**
```bash
python3 sync_leads_to_sheets.py leads/general/leads_general_instagram_20251122.json
```

**Features:**
- ✅ Prevents duplicates automatically (checks name + contact + location)
- ✅ Validates headers structure (12 columns)
- ✅ Shows skip count for duplicates
- ✅ Maintains data quality

**Output Example:**
```
✅ Loaded 17 leads from file
✅ Found 10 existing leads in sheet
   [1/17] ✅ New Lead (score: 8.5)
   [2/17] ⏭️  Existing Lead (duplicate - skipped)
   ...
✅ Successfully synced: 7/17 leads
⏭️  Skipped duplicates: 10/17 leads
```

---

### 2. `cleanup_sheets.py` - Sheet Reorganization

**Cleanup and reorganize** your Google Sheet when it gets messy.

**Usage:**
```bash
python3 cleanup_sheets.py
```

**What it does:**
1. ✅ Fixes headers (ensures 12 columns: timestamp, platform, type, name, contact, location, engagement, rating, review_count, quality_score, persona_match, lead_url)
2. ✅ Removes duplicate leads
3. ✅ Sorts by quality score (highest first)
4. ✅ Cleans extra columns

**When to use:**
- Headers are missing or incorrect
- Data is duplicated
- Sheet has extra empty columns
- Leads are not sorted by quality

---

## 📋 Sheet Structure

### Columns (12 total):

| Column | Description | Example |
|--------|-------------|---------|
| A - timestamp | When lead was added | 2025-11-26T18:13:17 |
| B - platform | Source platform | instagram, facebook, tiktok, google_maps |
| C - type | Lead type | b2c, b2b, competitor |
| D - name | Lead name | "John's Fitness Center" |
| E - contact | Email/phone/website | john@example.com |
| F - location | Address or location | "123 Main St, Miami, FL" |
| G - engagement | Engagement metrics (Instagram) | "1.2K followers" |
| H - rating | Google rating | 4.8 |
| I - review_count | Number of reviews | 147 |
| J - quality_score | AI quality score (0-20) | 11.856 |
| K - persona_match | Detected persona | seniors, athletes, workers |
| L - lead_url | URL to lead profile | https://... |

---

## 🔄 Workflow

### Daily Automated Flow (GitHub Actions):
1. **Scrape leads** (Instagram, Facebook, TikTok) → JSON files
2. **Auto-sync to Google Sheets** → Duplicates skipped automatically
3. **Sheet stays organized** → No manual cleanup needed

### Manual Cleanup (if needed):
```bash
# If sheet gets messy, run cleanup
python3 cleanup_sheets.py

# Then verify with a test sync
python3 sync_leads_to_sheets.py leads/general/latest_leads.json
```

---

## ✅ Current Status (Session 56)

**Google Sheets API:**
- ✅ Fully configured and tested
- ✅ Service Account: `lead-sync-automation@alpha-medical-lead-management.iam.gserviceaccount.com`
- ✅ Credentials: `google_credentials.json` (secured)

**Current Data:**
- ✅ 17 leads synced (Google Maps - Senior Centers)
- ✅ 0 duplicates
- ✅ Headers verified correct
- ✅ Sorted by quality score

**GitHub Actions:**
- ✅ Daily scraping workflow active
- ✅ Auto-sync to Google Sheets enabled
- ✅ Duplicate prevention active

---

## 🚨 Troubleshooting

### "Headers incorrect or missing"
```bash
python3 cleanup_sheets.py
```

### "Too many duplicates in sheet"
```bash
python3 cleanup_sheets.py
```

### "Permission denied"
- Make sure sheet is shared with: `lead-sync-automation@alpha-medical-lead-management.iam.gserviceaccount.com`
- Give "Editor" access

### "Credentials file not found"
- Check file exists: `ls -la google_credentials.json`
- Should be in: `/Users/mac/Desktop/Alpha-Medical/market-analysis/`

---

**Last Updated:** 2025-11-26 Session 56
**Status:** ✅ Fully operational - No issues
