# GMAIL APPS SCRIPT SETUP - EMAIL AUTOMATION

**Purpose:** Automate personalized lead nurturing emails sent daily from Google Sheets

**Time Required:** 5 minutes (one-time setup)

---

## PREREQUISITES

✅ Google Sheet created: "Alpha Medical - Lead Management"
✅ Service account email configured
✅ Sheet ID saved to .env file

**NOTE:** This step can only be completed AFTER you create the Google Sheet manually.

---

## STEP-BY-STEP INSTRUCTIONS

### Step 1: Open Your Google Sheet (30 seconds)

1. Open your Google Sheet: "Alpha Medical - Lead Management"
   (The one you just created in the previous step)

### Step 2: Open Apps Script Editor (1 min)

2. Click **Extensions** (menu bar)
3. Click **Apps Script**
4. This opens the Apps Script editor in a new tab

### Step 3: Delete Default Code (30 seconds)

5. You'll see default function `myFunction() { }`
6. **Select all code** (Cmd+A or Ctrl+A)
7. **Delete it**

### Step 4: Paste Lead Nurturing Script (1 min)

8. Open this file on your computer:
   ```
   /Users/mac/Desktop/Alpha-Medical/market-analysis/Gmail_Lead_Nurturing.gs
   ```

9. **Copy all contents** of that file

10. **Paste into Apps Script editor**

### Step 5: Save & Authorize (2 min)

11. Click **💾 Save** (or Cmd+S)

12. Rename project:
    - Click "Untitled project" at top
    - Change to: `Gmail Lead Nurturing`
    - Press Enter

13. Click **▶️ Run** button (to test)

14. You'll see popup: **"Authorization required"**
    - Click **Review permissions**
    - Select your Google account
    - Click **Advanced**
    - Click **"Go to Gmail Lead Nurturing (unsafe)"**
    - Click **Allow**

    **NOTE:** This is your own script, it's safe. Google shows this warning for all custom scripts.

### Step 6: Setup Daily Trigger (1 min)

15. Click **⏰ Triggers** (left sidebar - clock icon)

16. Click **+ Add Trigger** (bottom right)

17. Configure trigger:
    - **Function:** `sendLeadEmails`
    - **Event source:** `Time-driven`
    - **Type of time based trigger:** `Day timer`
    - **Time of day:** `10am to 11am`

18. Click **Save**

19. You may need to authorize again (same process as step 14)

---

## VERIFICATION

### Test Manual Run (Optional)

1. Go back to Apps Script editor
2. Select function: `sendLeadEmails`
3. Click **▶️ Run**
4. Check **Execution log** (bottom of screen)
5. Should see: "✅ Email campaign complete"

### Check Trigger Status

1. Click **⏰ Triggers** (left sidebar)
2. You should see:
   ```
   sendLeadEmails | Head | Time-driven | Day timer | 10am-11am
   ```
3. Status should be **Active** (no errors)

---

## WHAT HAPPENS DAILY

**Every day at 10 AM:**

1. Script reads "Qualified Leads" sheet
2. Finds leads with status = "New"
3. Sends personalized email based on:
   - Persona (seniors, workers, athletes)
   - Quality score (hot/warm/cold lead)
   - Business name
4. Updates status to "Contacted"
5. Adds timestamp to "Last Contact" column
6. Respects Gmail rate limits (50 emails/run max)

**Email Templates:**
- **Hot leads (score ≥ 8.5):** Aggressive offer (25% discount)
- **Warm leads (score 7.5-8.4):** Educational content + soft CTA
- **Cold leads (score < 7.5):** Pure value content, no hard sell

---

## GMAIL RATE LIMITS

**Free Gmail Account:**
- 100 emails/day maximum
- Script configured to send max 50/run

**Google Workspace:**
- 2,000 emails/day maximum
- Can increase script limit to 100+/run

**Rate Limiting Protection:**
- 2-second delay between emails
- Automatic daily quota tracking
- Stops if limit reached

---

## CUSTOMIZATION

### Change Email Templates

1. Open Apps Script editor
2. Scroll to `getEmailTemplate()` function (line 40)
3. Edit HTML templates:
   - `seniors.hot` - Hot lead template for seniors
   - `seniors.warm` - Warm lead template
   - `workers.hot` - Hot lead template for office workers
   - etc.
4. Click **💾 Save**

### Change Trigger Time

1. Click **⏰ Triggers**
2. Click **⋮** (three dots) next to trigger
3. Click **Edit trigger**
4. Change time range
5. Click **Save**

### Test Mode (Send No Emails)

1. Open Apps Script editor
2. Find line 34:
   ```javascript
   TEST_MODE: false
   ```
3. Change to:
   ```javascript
   TEST_MODE: true
   ```
4. Click **💾 Save**
5. Run manually to test without sending real emails

---

## TROUBLESHOOTING

### Error: "Cannot read property 'Qualified Leads'"

**Cause:** Sheet name doesn't match
**Fix:** Ensure worksheet is named exactly `Qualified Leads` (case-sensitive)

### Error: "Service invoked too many times"

**Cause:** Hit Gmail daily limit
**Fix:** Wait 24 hours, reduce MAX_EMAILS_PER_RUN to 25

### No Emails Sent

**Cause:** No leads with status = "New"
**Fix:** Check "Qualified Leads" sheet, ensure Status column has "New" values

### Emails Not Personalized

**Cause:** Missing data in Business Name or Email columns
**Fix:** Ensure lead scraping populated all required columns

---

## MONITORING

### View Execution History

1. Apps Script editor
2. Click **Executions** (left sidebar)
3. Shows:
   - Timestamp of each run
   - Success/Failure status
   - Duration
   - Error messages (if any)

### View Sent Emails

1. Open Gmail
2. Go to **Sent** folder
3. Emails sent by script will appear here

### Track in Google Sheet

1. Open "Qualified Leads" sheet
2. Check columns:
   - **Status:** Should change from "New" to "Contacted"
   - **Last Contact:** Should have today's date
   - **Next Action:** Auto-populated with follow-up date

---

## INTEGRATION WITH LEAD SCRAPING

**Full Automation Flow:**

1. **9:00 AM:** Cron job scrapes leads (Instagram + Google Maps)
2. **9:30 AM:** Leads synced to Google Sheets "Raw Leads"
3. **Manual/Flow:** Qualify leads → move to "Qualified Leads" sheet
4. **10:00 AM:** Apps Script sends nurturing emails to new qualified leads
5. **Ongoing:** Monitor responses, update lead status

---

## METRICS TO TRACK

**In Analytics Sheet:**

- Total emails sent (daily)
- Open rate (requires UTM tracking)
- Response rate
- Conversion to customer

**Add to Analytics sheet:**
```
Metric: Emails Sent Daily
Value: [count from Apps Script log]
Target: 50
Status: On Track
```

---

## NEXT STEPS AFTER SETUP

1. ✅ Verify trigger is active
2. ✅ Add sample qualified lead to test
3. ✅ Run manual test (click Run button)
4. ✅ Check Gmail sent folder for test email
5. ✅ Wait for daily trigger (next day 10 AM)
6. ✅ Monitor execution logs

---

## QUICK REFERENCE

**Script Location:**
- File: `/Users/mac/Desktop/Alpha-Medical/market-analysis/Gmail_Lead_Nurturing.gs`
- Apps Script: Extensions → Apps Script

**Key Functions:**
- `sendLeadEmails()` - Main function (triggered daily)
- `getEmailTemplate()` - Email templates by persona/priority
- `updateLeadStatus()` - Updates sheet after sending

**Trigger:**
- Daily at 10-11 AM
- Function: `sendLeadEmails`

**Rate Limits:**
- Free Gmail: 100 emails/day
- Script limit: 50 emails/run
- Delay: 2 seconds between emails

---

✅ **READY!** Once you complete these 6 steps, email automation will run daily at 10 AM.
