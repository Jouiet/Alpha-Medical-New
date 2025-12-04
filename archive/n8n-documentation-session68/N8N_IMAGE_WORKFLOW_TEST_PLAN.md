# N8N IMAGE PROCESSING WORKFLOW - TEST PLAN
## Alpha Medical Product Photo Enhancement
## Date: 2025-12-01

---

## ✅ SETUP STATUS

### Phase 1: MCP Configuration ✅ COMPLETE
- ✅ N8N credentials stored in `.n8n-credentials.env`
- ✅ MCP config created at `~/.config/claude-code/mcp.json`
- ✅ N8N instance connectivity verified (https://n8n.srv1168256.hstgr.cloud)
- ✅ MCP Access Token configured
- ✅ N8N Public API Key available

---

## 🎯 NEXT STEPS TO TEST WORKFLOW

### Phase 2: Google Drive Setup (5 minutes)

**Action Required:** Create folder structure in Google Drive

1. **Navigate to Google Drive:**
   - Login: https://drive.google.com
   - Use the same Google account configured in n8n

2. **Create Input Folder:**
   - Click "New" → "Folder"
   - Name: **"Alpha Medical - Product Photos Input"**
   - Open folder → Copy URL
   - Extract Folder ID from URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - **Save Input Folder ID:** `_________________`

3. **Create Output Folder:**
   - Click "New" → "Folder"
   - Name: **"Alpha Medical - Product Photos Output"**
   - Open folder → Copy URL
   - Extract Folder ID from URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - **Save Output Folder ID:** `_________________`

---

### Phase 3: Google Sheets Setup (5 minutes)

**Action Required:** Create tracking spreadsheet

1. **Create New Google Sheet:**
   - Go to https://sheets.google.com
   - Click "Blank" spreadsheet
   - Name: **"Alpha Medical - Product Image Processing"**

2. **Create "Photos" Sheet Tab:**
   - Rename "Sheet1" to **"Photos"** (exact name required)

3. **Add Required Headers (Row 1):**
   ```
   Column A: File name
   Column B: Status
   Column C: Start Time
   Column D: End Time
   Column E: Input File
   Column F: Output File
   Column G: Notes
   ```

4. **Get Sheet ID:**
   - Copy URL: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
   - Extract Sheet ID from URL
   - **Save Sheet ID:** `_________________`

5. **Verify Permissions:**
   - Ensure n8n account email has **Editor** access
   - Share sheet if needed

---

### Phase 4: Configure Credentials in n8n (10 minutes)

**Action Required:** Setup 3 credentials in n8n

1. **Login to n8n:**
   - URL: https://n8n.srv1168256.hstgr.cloud
   - Navigate to: Settings → Credentials

2. **Add Google Drive OAuth2 API:**
   - Click "Add Credential"
   - Select "Google Drive OAuth2 API"
   - Follow OAuth flow
   - Grant access to Google Drive
   - Save credential

3. **Add Google Sheets OAuth2 API:**
   - Click "Add Credential"
   - Select "Google Sheets OAuth2 API"
   - Follow OAuth flow
   - Grant access to Google Sheets
   - Save credential

4. **Add Google Gemini (PaLM) API:**
   - Get API key from: https://ai.google.dev/
   - Click "Add Credential"
   - Select "Google Gemini(PaLM) API"
   - Paste API key
   - Save credential

---

### Phase 5: Import Workflow to n8n (5 minutes)

**Status:** ⏳ PENDING - Need workflow JSON file

**Action Required:**
1. Get the complete workflow JSON from n8n community or export
2. In n8n: Workflows → Create New Workflow
3. Click ⋮ (three dots) → Import from JSON
4. Paste workflow JSON
5. Click Import

**Alternative if JSON not available:**
- Build workflow manually following architecture in `N8N_WORKFLOW_IMAGE_PROCESSING.md`

---

### Phase 6: Configure Workflow Nodes (10 minutes)

**Action Required:** Update workflow with your IDs

**Nodes to Configure:**

**1. File Created Trigger:**
```
Trigger: On
Folder to Watch: [Select Input Folder or paste Folder ID]
Poll Time: Every 5 minutes
Credential: Google Drive OAuth2 API
```

**2. File Updated Trigger:**
```
Trigger: On
Folder to Watch: [Select Input Folder or paste Folder ID]
Poll Time: Every 5 minutes
Credential: Google Drive OAuth2 API
```

**3. Workflow Configuration Node:**
```javascript
{
  "google_sheet_id": "PASTE_YOUR_SHEET_ID_HERE",
  "dest_folder_id": "PASTE_YOUR_OUTPUT_FOLDER_ID_HERE",
  "text_prompt": "Transform this product photo into a high-quality, studio-style image. - Background: Remove the original background completely and replace it with a clean, light gray gradient (e.g., #f0f0f0 to #e0e0e0). - Lighting: Apply soft, diffused, and balanced lighting to eliminate harsh shadows and highlight the product's details. The lighting should feel natural and professional. - Color & Realism: Perform subtle color correction to enhance vibrancy and ensure colors are true-to-life. Do not oversaturate. - Integrity: Keep the product's shape, texture, and all original details perfectly intact. Do not add, remove, or alter any part of the product itself. If the product contains any text, especially ensure that the text is readable and identical in the new image. - Final Look: The result should be a crisp, modern, and professional image suitable for a high-end e-commerce catalog."
}
```

**4. All Google Drive Nodes (2 nodes):**
- Download Image → Select Google Drive credential
- Save image → Select Google Drive credential

**5. All Google Sheets Nodes (3 nodes):**
- Create Entry → Select Google Sheets credential
- Update Entry to Done → Select Google Sheets credential
- Update Entry to Error → Select Google Sheets credential

**6. Edit Image Node:**
- Select Google Gemini (PaLM) API credential

---

### Phase 7: Enable MCP Access (2 minutes)

**Action Required:** Make workflow accessible to Claude Code

1. In n8n workflow editor
2. Click "Workflow Settings" (gear icon)
3. Scroll to "MCP Access" section
4. Toggle **"Enable workflow access in MCP"** to ON
5. Click Save

---

### Phase 8: Test Workflow (15 minutes)

**Preparation:**

1. **Select Test Image:**
   - Choose 1 product photo from Alpha Medical catalog
   - Recommended: Lower quality image to see improvement
   - File format: JPG or PNG
   - Size: < 20MB

2. **Upload to Input Folder:**
   - Navigate to "Alpha Medical - Product Photos Input" folder
   - Upload test image
   - Wait 5 minutes (trigger poll time)

**Verification Checklist:**

- [ ] **n8n Execution Log:**
  - Navigate: Executions → View latest execution
  - Status: Should be "Success" (green)
  - Review each node execution

- [ ] **Google Sheets Entry:**
  - Open "Photos" sheet
  - New row should appear with:
    - File name: [your test image name]
    - Status: "Completed"
    - Start Time: [timestamp]
    - End Time: [timestamp]
    - Input File: [link to original]
    - Output File: [link to enhanced image]

- [ ] **Output Folder:**
  - Navigate to "Alpha Medical - Product Photos Output" folder
  - Enhanced image should exist
  - File name format: `{original_name}_clean.{ext}`

- [ ] **Image Quality:**
  - Download enhanced image
  - Compare with original
  - Verify:
    - Background removed/replaced ✅
    - Professional lighting ✅
    - Product details preserved ✅
    - Text readable ✅

**If Error Occurs:**

1. Check n8n execution log for error message
2. Common issues:
   - API quota exceeded (Gemini)
   - Invalid credentials
   - Folder permissions
   - Image format not supported

3. Review troubleshooting section in `N8N_WORKFLOW_IMAGE_PROCESSING.md:379-420`

---

### Phase 9: Batch Test (Optional - 30 minutes)

**After successful single test:**

1. **Upload 5 Product Images:**
   - Different product types (massage chair, therapeutic device, etc.)
   - Various backgrounds
   - Upload all at once to Input folder

2. **Monitor Processing:**
   - Watch Google Sheets for new entries
   - Check n8n executions
   - Track processing time per image

3. **Quality Review:**
   - Compare all 5 enhanced images
   - Verify consistency
   - Note any issues

4. **Adjust Prompt if Needed:**
   - If backgrounds not ideal → modify prompt
   - Test different options from `N8N_WORKFLOW_IMAGE_PROCESSING.md:139-155`

---

## 🎯 SUCCESS CRITERIA

### Minimum Viable Test (Phase 8):
- [ ] 1 image successfully processed
- [ ] Google Sheets tracking works
- [ ] Output image quality acceptable
- [ ] No errors in n8n execution

### Full Test (Phase 9):
- [ ] 5 images successfully processed
- [ ] All tracked in Google Sheets
- [ ] Consistent quality across images
- [ ] Processing time < 2 minutes per image
- [ ] Ready to process all 100 Alpha Medical products

---

## 📊 ESTIMATED TIMELINE

- **Setup (Phases 2-6):** 35 minutes
- **Enable MCP (Phase 7):** 2 minutes
- **Single Test (Phase 8):** 15 minutes
- **Batch Test (Phase 9):** 30 minutes (optional)

**Total:** ~52 minutes (82 minutes with batch test)

---

## 🚀 AFTER SUCCESSFUL TEST

### Next Actions:

1. **Process All Alpha Medical Products:**
   - Upload all 100 product images to Input folder
   - Monitor processing in Google Sheets
   - Estimated time: ~50-100 minutes (automatic)
   - Estimated cost: ~$1-5 (Google Gemini API)

2. **Update Shopify Product Images:**
   - Download enhanced images from Output folder
   - Upload to Shopify products
   - Replace existing product images

3. **Document Results:**
   - Before/after examples
   - Processing metrics
   - Quality assessment

4. **Integrate with Claude Code via MCP:**
   - Test: "Can you list available n8n workflows?"
   - Execute: "Run the product image processing workflow"
   - Monitor: "Check status of image processing workflow"

---

## 📝 NOTES

### Google Gemini API Costs:
- Current pricing: ~$0.01-0.05 per image
- 100 images: ~$1-5 total
- Check latest pricing: https://ai.google.dev/pricing

### Image Requirements:
- **Recommended:** 1500x1500px minimum
- **Formats:** JPG, PNG
- **Max size:** 20MB
- **Best results:** Clear product visibility, minimal background clutter

### Customization Options:
See `N8N_WORKFLOW_IMAGE_PROCESSING.md:496-511` for product-specific prompt variations:
- Massage Chairs: Luxury showroom style
- Therapeutic Devices: Clinical medical catalog
- Bundles/Kits: Product bundle presentation

---

## 🔗 RELATED DOCUMENTATION

- **Setup Guide:** `N8N_WORKFLOW_IMAGE_PROCESSING.md`
- **MCP Configuration:** `N8N_MCP_CONFIGURATION_GUIDE.md`
- **Credentials:** `.n8n-credentials.env` (secured in .gitignore)

---

**Status:** Phase 1 Complete ✅ | Phases 2-9 Pending ⏳
**Ready to Test:** YES (after completing Phases 2-7)
**Estimated Setup Time Remaining:** ~35 minutes

**Last Updated:** 2025-12-01
**Created By:** Claude Code - Session 68
