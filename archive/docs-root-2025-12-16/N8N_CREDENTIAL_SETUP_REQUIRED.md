# N8N WORKFLOW ACTIVATION - CREDENTIAL SETUP REQUIRED
**Date:** 2025-12-02
**Issue:** Credential with ID "htidcOV6hR8kh9tB" does not exist
**Status:** ⚠️ ACTION REQUIRED

---

## PROBLEM DIAGNOSIS

**Error Message:**
```
Workflow could not be activated:
There was a problem activating the workflow:
"Credential with ID "htidcOV6hR8kh9tB" does not exist for type "googleDriveOAuth2Api"."
```

**Root Cause:**
The workflow JSON contains credential IDs that don't exist in your N8N instance. This means:

1. The credentials were never created, OR
2. The credentials were deleted, OR
3. The workflow JSON came from a different N8N instance

**Solution:** Create the 3 required Google credentials in N8N UI, then update workflow nodes.

---

## REQUIRED CREDENTIALS (3)

You need to create these 3 Google credentials in N8N:

### 1. Google Drive OAuth2 Credential
- **Type:** Google Drive OAuth2 API
- **Name:** "Google Drive account" (or any name you prefer)
- **Purpose:** Access Input/Output folders for image files

### 2. Google Sheets OAuth2 Credential
- **Type:** Google Sheets OAuth2 API
- **Name:** "Google Sheets account" (or any name you prefer)
- **Purpose:** Update tracking spreadsheet with processing status

### 3. Google Gemini (PaLM) API Credential
- **Type:** Google PaLM API (or Google Gemini API)
- **Name:** "Google Gemini API account" (or any name you prefer)
- **Purpose:** AI image enhancement processing

---

## STEP-BY-STEP SETUP (15 minutes)

### PHASE 1: Create Google Credentials in N8N (10 minutes)

**1. Login to N8N:**
```
URL: https://n8n.srv1168256.hstgr.cloud
```

**2. Navigate to Credentials:**
- Click **"Credentials"** in left sidebar
- OR go to: https://n8n.srv1168256.hstgr.cloud/credentials

**3. Create Google Drive OAuth2 Credential:**
- Click **"+ Add Credential"**
- Search for **"Google Drive"**
- Select **"Google Drive OAuth2 API"**
- Click **"Connect my account"** or **"OAuth2"** button
- Follow Google OAuth flow:
  - Select your Google account
  - Grant permissions to access Google Drive
- **IMPORTANT:** After creation, **COPY THE CREDENTIAL ID**
  - It will look like: `abc123XYZ456def789`
- Click **"Save"**

**4. Create Google Sheets OAuth2 Credential:**
- Click **"+ Add Credential"** again
- Search for **"Google Sheets"**
- Select **"Google Sheets OAuth2 API"**
- Click **"Connect my account"** or **"OAuth2"** button
- Follow Google OAuth flow:
  - Select your Google account (same as before)
  - Grant permissions to access Google Sheets
- **IMPORTANT:** After creation, **COPY THE CREDENTIAL ID**
- Click **"Save"**

**5. Create Google Gemini (PaLM) API Credential:**
- Click **"+ Add Credential"** again
- Search for **"Google Gemini"** or **"Google PaLM"**
- Select the API credential type
- Enter your **Google AI Studio API Key**
  - Get key from: https://aistudio.google.com/app/apikey
  - Create new project if needed
  - Copy API key
- **IMPORTANT:** After creation, **COPY THE CREDENTIAL ID**
- Click **"Save"**

**Result:** You now have 3 credentials with new IDs.

---

### PHASE 2: Update Workflow Nodes (5 minutes)

**6. Open the Workflow:**
```
Direct URL: https://n8n.srv1168256.hstgr.cloud/workflow/q0kyXyhCUq5gjmG2
```
Or:
- Click **"Workflows"** in sidebar
- Find **"Enhance Product Photos with Google Gemini AI..."**
- Click to open

**7. Update Credential in "File Created" Node:**
- Click on **"File Created"** node (trigger node)
- Find **"Credential to connect with"** dropdown
- Select your **Google Drive OAuth2** credential
- Click outside node to save

**8. Update Credential in "File Updated" Node:**
- Click on **"File Updated"** node
- Find **"Credential to connect with"** dropdown
- Select your **Google Drive OAuth2** credential (same as above)
- Click outside node to save

**9. Update Credential in ALL Google Drive Nodes:**
Look for these nodes and update credentials:
- **"Download File"** → Google Drive credential
- **"Save image"** → Google Drive credential
- Any other Google Drive nodes → Google Drive credential

**10. Update Credential in Google Sheets Nodes:**
Look for these nodes and update credentials:
- **"Add Row"** or **"Update Sheet"** → Google Sheets credential
- Any Google Sheets nodes → Google Sheets credential

**11. Update Credential in Google Gemini Node:**
- Click on **"Edit Image"** or **"Gemini"** node
- Find **"Credential to connect with"** dropdown
- Select your **Google Gemini API** credential
- Click outside node to save

**12. Save Workflow:**
- Click **"Save"** button (top right)
- Verify: "Workflow saved" confirmation

---

### PHASE 3: Activate Workflow (1 minute)

**13. Activate the Workflow:**
- Toggle **"Active"** switch at top → **ON**
- Switch should turn blue/green
- Click **"Save"** again

**14. Enable MCP Access (Optional):**
- Click **⚙️ "Workflow Settings"** button
- Scroll to **"MCP Access"** section
- Toggle **"Enable workflow access in MCP"** → **ON**
- Click **"Save"**

---

## VERIFICATION (5 minutes)

**Test the Workflow:**

1. **Upload Test Image:**
   - Go to Google Drive Input folder: https://drive.google.com/drive/folders/1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox
   - Upload 1 product image (JPG or PNG)

2. **Wait 5 Minutes:**
   - Workflow polls every 5 minutes for new files
   - First trigger will take up to 5 minutes

3. **Check Execution:**
   - Navigate to **"Executions"** in N8N
   - Status should show: ✅ **"Success"**
   - If error, click on execution to see error details

4. **Verify Output:**
   - **Google Sheet:** https://docs.google.com/spreadsheets/d/1Q5ujL0LQEz-kgGkg-oMzCutcpUnznpDPpRkqh1hUBUw/edit
     - Check "Photos" tab
     - New row: Filename, "Completed" status, timestamps, file links
   - **Output Folder:** https://drive.google.com/drive/folders/1O1PrZoTDweXQx8ImVLXlJArei9hadv izn
     - Enhanced image with `_clean` suffix should appear

---

## ALTERNATIVE: API CREDENTIAL VERIFICATION (ADVANCED)

If you want to verify credentials exist before manual setup:

**Method 1: Check via N8N UI**
- Go to: https://n8n.srv1168256.hstgr.cloud/credentials
- Count Google Drive, Sheets, Gemini credentials
- Note their IDs (hover over credential, ID in URL)

**Method 2: Via Workflow Editor**
- Open workflow
- Click any Google Drive node
- Check if credential dropdown shows any options
- If empty = No credentials created yet

---

## WHY THIS HAPPENED

**Credential IDs in Original Workflow JSON:**
```json
{
  "Google Drive": "htidcOV6hR8kh9tB",
  "Google Sheets": "HTAGRgrsWTF0cfU2",
  "Google Gemini": "7tlny7NnnrQIfupF"
}
```

These IDs were in the workflow JSON you provided, but they don't exist in your current N8N instance.

**Possible Reasons:**
1. The workflow JSON was exported from a different N8N instance
2. Credentials were deleted from your instance
3. Credentials were never created

**Solution:** Create fresh credentials, update workflow nodes.

---

## TROUBLESHOOTING

**Issue: "OAuth callback URL mismatch"**
- **Solution:** Add N8N OAuth callback URL to Google Cloud Console
- **URL:** `https://n8n.srv1168256.hstgr.cloud/rest/oauth2-credential/callback`

**Issue: "Google API not enabled"**
- **Solution:** Enable APIs in Google Cloud Console:
  - Google Drive API
  - Google Sheets API
  - Generative Language API (Gemini)

**Issue: "Insufficient permissions"**
- **Solution:** Grant required scopes during OAuth:
  - Drive: Full access (read/write files)
  - Sheets: Full access (read/write spreadsheets)

**Issue: "Gemini API key invalid"**
- **Solution:** Generate new API key at https://aistudio.google.com/app/apikey

---

## ESTIMATED TIME

- **Credential Creation:** 10 minutes (3 credentials × ~3 min each)
- **Node Updates:** 5 minutes (6-8 nodes to update)
- **Activation:** 1 minute (toggle + save)
- **Testing:** 5 minutes (upload + wait + verify)

**Total:** ~20 minutes

---

## AFTER SETUP COMPLETE

Once all credentials are configured and workflow is activated:

**Batch Processing:**
1. Upload remaining 99 product images to Input folder
2. Workflow processes automatically every 5 minutes
3. ~30-60 seconds per image processing time
4. Total automation: 50-100 minutes
5. Monitor progress in Google Sheet "Photos" tab

**Cost:**
- ~$0.01-0.05 per image (Google Gemini API)
- Total for 100 images: $1-5
- vs Manual editing: $500-2000 (100x-400x savings)

---

## SUPPORT

**N8N Documentation:**
- OAuth2 Credentials: https://docs.n8n.io/credentials/
- Google Drive Node: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googledrive/
- Google Sheets Node: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlesheets/

**Google AI Studio:**
- API Keys: https://aistudio.google.com/app/apikey
- Gemini API Docs: https://ai.google.dev/docs

---

**Workflow ID:** q0kyXyhCUq5gjmG2
**Workflow URL:** https://n8n.srv1168256.hstgr.cloud/workflow/q0kyXyhCUq5gjmG2

**Status:** ⏳ WAITING FOR CREDENTIAL SETUP
