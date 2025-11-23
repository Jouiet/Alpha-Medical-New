# SETUP GOOGLE SHEETS API - 10 Minutes

## Étape 1: Create Google Cloud Project (2 min)

1. Go to: https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: `Alpha Medical Lead Management`
4. Click "Create"

## Étape 2: Enable Google Sheets API (1 min)

1. In Cloud Console, go to: "APIs & Services" → "Library"
2. Search: "Google Sheets API"
3. Click on it → Click "Enable"
4. Also enable: "Google Drive API"

## Étape 3: Create Service Account (3 min)

1. Go to: "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Service account name: `lead-sync-automation`
4. Click "Create and Continue"
5. Skip role assignment (click "Continue")
6. Click "Done"

## Étape 4: Generate Key (2 min)

1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON"
5. Click "Create"
6. Save the downloaded JSON file as:
   `/Users/mac/Desktop/Alpha-Medical/market-analysis/google_credentials.json`

## Étape 5: Create Google Sheet (2 min)

1. Go to: https://sheets.google.com
2. Create new sheet
3. Name: `Alpha Medical - Lead Management`
4. Create 3 tabs:
   - Tab 1: "Raw Leads"
   - Tab 2: "Qualified Leads"
   - Tab 3: "Dashboard"

## Étape 6: Add Headers to "Raw Leads" Tab

Add these headers in Row 1:

| A | B | C | D | E | F | G | H | I | J | K | L |
|---|---|---|---|---|---|---|---|---|---|---|---|
| timestamp | platform | type | name | contact | location | engagement | rating | review_count | quality_score | persona_match | lead_url |

## Étape 7: Share Sheet with Service Account

1. Open the service account JSON file (`google_credentials.json`)
2. Find the "client_email" field (looks like: `lead-sync-automation@project-id.iam.gserviceaccount.com`)
3. Copy this email
4. In Google Sheet, click "Share"
5. Paste the service account email
6. Give "Editor" access
7. Uncheck "Notify people"
8. Click "Share"

## Étape 8: Test Connection

```bash
cd /Users/mac/Desktop/Alpha-Medical/market-analysis

# Test with existing leads file
python3 sync_leads_to_sheets.py leads/general/leads_general_google_maps_20251122_213119.json
```

Expected output:
```
✅ Loaded 17 leads from leads/general/leads_general_google_maps_20251122_213119.json
✅ Authenticated with Google Sheets API
✅ Opened sheet: Alpha Medical - Lead Management → Raw Leads
   [1/17] ✅ Arcola Lakes Senior Center (score: 11.856)
   [2/17] ✅ Senior Center Adult Day Care (score: 8.35)
   ...
   [17/17] ✅ Gesu Senior Citizen Center (score: 4.08)

======================================================================
SYNC COMPLETE
======================================================================
✅ Successfully synced: 17/17 leads

🎉 All leads synced successfully!
```

## ✅ Setup Complete!

Once done, you can sync leads automatically:

```bash
# Scrape Instagram
python3 lead_generation_scraper.py --instagram --hashtag "arthritis" --max-results 50

# Sync to Google Sheets
python3 sync_leads_to_sheets.py leads/general/leads_general_instagram_*.json
```

## Troubleshooting

**Error: "Spreadsheet 'Alpha Medical - Lead Management' not found"**
- Solution: Make sure the sheet name is exactly: `Alpha Medical - Lead Management`
- Or update SHEET_NAME in sync_leads_to_sheets.py (line 25)

**Error: "Permission denied"**
- Solution: Make sure you shared the sheet with the service account email

**Error: "Credentials file not found"**
- Solution: Make sure `google_credentials.json` is in the correct path

---

**Total Time: ~10 minutes**
**Cost: $0 (Google Sheets API is free)**
