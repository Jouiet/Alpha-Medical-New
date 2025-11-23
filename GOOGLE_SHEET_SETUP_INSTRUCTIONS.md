# GOOGLE SHEET SETUP - MANUAL CREATION REQUIRED

**Status:** Service account has storage quota exceeded. Need to create sheet under your personal Google account.

**Time Required:** 3 minutes

---

## STEP-BY-STEP INSTRUCTIONS

### Step 1: Create New Google Sheet (1 min)

1. **Open this URL:** https://sheets.google.com/create

2. **Rename the sheet:**
   - Click "Untitled spreadsheet" at top
   - Change name to: `Alpha Medical - Lead Management`
   - Press Enter

### Step 2: Share with Service Account (1 min)

3. **Click "Share" button** (top right corner)

4. **Add service account email:**
   ```
   ecom-317@astute-quarter-476613-h3.iam.gserviceaccount.com
   ```

5. **Set permissions to "Editor"**

6. **Click "Send"**

### Step 3: Copy Sheet ID (30 seconds)

7. **Look at the URL in your browser:**
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```

8. **Copy the SHEET_ID** (between `/d/` and `/edit`)
   - Example: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

### Step 4: Run Configuration Script (30 seconds)

9. **Open Terminal and run:**
   ```bash
   cd /Users/mac/Desktop/Alpha-Medical
   python3 configure_existing_sheet.py YOUR_SHEET_ID_HERE
   ```

   Replace `YOUR_SHEET_ID_HERE` with the actual ID from step 8.

---

## EXPECTED OUTPUT

When you run the configuration script, you should see:

```
======================================================================
CONFIGURING EXISTING GOOGLE SHEET
======================================================================

Sheet ID: 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms

[1/4] Authenticating...
✅ Authenticated

[2/4] Opening spreadsheet...
✅ Opened: Alpha Medical - Lead Management
   URL: https://docs.google.com/spreadsheets/d/...

[3/4] Setting up worksheets...
✅ Created 3 worksheets:
   - Raw Leads
   - Qualified Leads
   - Analytics

[4/4] Adding headers and formatting...
✅ Headers configured and formatted

======================================================================
CONFIGURATION COMPLETE
======================================================================

✅ Sheet ID saved to .env file
✅ READY FOR AUTOMATION!
```

---

## WHAT THE SCRIPT DOES

The configuration script will automatically:

1. ✅ Rename "Sheet1" to "Raw Leads"
2. ✅ Create "Qualified Leads" worksheet
3. ✅ Create "Analytics" worksheet
4. ✅ Add column headers to all sheets
5. ✅ Format headers (bold, colored backgrounds)
6. ✅ Freeze header rows
7. ✅ Add initial analytics tracking metrics
8. ✅ Save Sheet ID to `.env` file

---

## TROUBLESHOOTING

### Error: "Failed to open spreadsheet"
**Cause:** Sheet not shared with service account
**Fix:** Make sure you shared with exact email (copy-paste to avoid typos):
```
ecom-317@astute-quarter-476613-h3.iam.gserviceaccount.com
```

### Error: "Authentication failed"
**Cause:** `google_credentials.json` file missing or corrupted
**Fix:** Verify file exists:
```bash
ls -lh /Users/mac/Desktop/Alpha-Medical/google_credentials.json
```
Should show: `-rw-r--r-- ... 2.3K ... google_credentials.json`

### Error: Wrong Sheet ID
**Cause:** Copied wrong part of URL
**Example URL:**
```
https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit#gid=0
```
**Correct ID:** `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`
**Wrong:** `edit#gid=0` (don't include this part)

---

## AFTER SETUP COMPLETE

Once the Google Sheet is configured, you can:

1. **Test lead scraping:**
   ```bash
   python3 market-analysis/lead_generation_scraper.py --test
   ```

2. **View leads in Google Sheet:**
   - Open the sheet URL from script output
   - Check "Raw Leads" tab for scraped data

3. **Setup automation:**
   - See: `LEAD_MANAGEMENT_SHOPIFY_FLOWS.md`
   - Setup cron job for daily scraping
   - Setup Gmail Apps Script for nurturing

---

## QUICK REFERENCE

**Service Account Email:**
```
ecom-317@astute-quarter-476613-h3.iam.gserviceaccount.com
```

**Configuration Script:**
```bash
python3 configure_existing_sheet.py SHEET_ID
```

**Test Scraping:**
```bash
python3 market-analysis/lead_generation_scraper.py --test
```

---

**READY TO START!** Follow the 4 steps above to complete the Google Sheets setup.
