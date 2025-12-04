# N8N WORKFLOW: AUTOMATED PRODUCT IMAGE PROCESSING
## Google Gemini Image Enhancement for E-commerce
## Date: 2025-12-01

---

## 🎯 WHAT THIS WORKFLOW DOES

**Automated image processing pipeline** that transforms product photos into professional studio-quality images using Google Gemini AI.

### Key Features:
- ✅ Watches Google Drive folder for new/updated product images
- ✅ Automatically processes images with Google Gemini (Nano Banana)
- ✅ Removes backgrounds and adds professional studio lighting
- ✅ Saves enhanced images to output folder
- ✅ Tracks all processing in Google Sheets log

---

## 🔄 WORKFLOW ARCHITECTURE

```
┌─────────────────────┐
│  Google Drive       │
│  (Input Folder)     │
│  New/Updated Images │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  File Trigger       │
│  Detect Changes     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Google Sheets      │
│  Create Entry       │
│  Status: Started    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Download Image     │
│  From Google Drive  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Google Gemini      │
│  Edit Image Node    │
│  Transform Image    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Save Enhanced      │
│  Image to Output    │
│  Folder             │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Update Sheets      │
│  Status: Completed  │
│  + Output Link      │
└─────────────────────┘
```

---

## 📋 CONFIGURATION REQUIREMENTS

### 1. Google Drive Setup

**Input Folder:**
- Create folder: "Alpha Medical - Product Photos Input"
- Upload original product photos here
- Workflow monitors this folder every 5 minutes

**Output Folder:**
- Create folder: "Alpha Medical - Product Photos Output"
- Enhanced images saved here automatically
- File naming: `{original_name}_clean.{ext}`

**How to get Folder ID:**
```
1. Open folder in Google Drive
2. URL will be: https://drive.google.com/drive/folders/FOLDER_ID_HERE
3. Copy the alphanumeric string after /folders/
```

### 2. Google Sheets Setup

**Sheet Name:** `Photos` (required)

**Required Columns (Row 1):**
- **File name** – Name of input file
- **Status** – Processing status (Not Started / Completed / Error)
- **Start Time** – When processing started
- **End Time** – When processing completed
- **Input File** – Link to original image
- **Output File** – Link to enhanced image
- **Notes** – Optional notes field

**Permissions:**
- Account must have **Editor** access

**How to get Sheet ID:**
```
1. Open Google Sheet
2. URL will be: https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
3. Copy the alphanumeric string after /d/
```

### 3. Google Gemini API Setup

**Get API Key:**
1. Go to https://ai.google.dev/
2. Create account / Sign in
3. Get API Key from Google AI Studio
4. Configure in n8n as "Google Gemini(PaLM) Api" credential

---

## ⚙️ WORKFLOW CONFIGURATION

### Workflow Configuration Node Settings:

```javascript
{
  "google_sheet_id": "YOUR_GOOGLE_SHEET_ID",
  "dest_folder_id": "YOUR_OUTPUT_FOLDER_ID",
  "text_prompt": "Transform this product photo into a high-quality, studio-style image. - Background: Remove the original background completely and replace it with a clean, light gray gradient (e.g., #f0f0f0 to #e0e0e0). - Lighting: Apply soft, diffused, and balanced lighting to eliminate harsh shadows and highlight the product's details. The lighting should feel natural and professional. - Color & Realism: Perform subtle color correction to enhance vibrancy and ensure colors are true-to-life. Do not oversaturate. - Integrity: Keep the product's shape, texture, and all original details perfectly intact. Do not add, remove, or alter any part of the product itself. If the product contains any text, especially ensure that the text is readable and identical in the new image. - Final Look: The result should be a crisp, modern, and professional image suitable for a high-end e-commerce catalog."
}
```

### Customization Options:

**For Alpha Medical products, you can adjust the prompt:**

**Option 1: Medical White Background**
```
"Replace background with pure white (#FFFFFF) medical-grade studio background. Apply soft diffused lighting. Preserve all product details exactly. Enhance clarity and sharpness suitable for medical equipment catalog."
```

**Option 2: Light Blue Clinical Background**
```
"Replace background with clean light blue gradient (#E3F2FD to #BBDEFB) suitable for medical products. Soft professional lighting. Preserve product integrity completely. Enhance colors naturally for medical equipment presentation."
```

**Option 3: Dark Professional Background**
```
"Replace background with dark gray gradient (#303030 to #202020) for premium medical equipment presentation. Dramatic professional lighting highlighting product features. Perfect product preservation."
```

---

## 🔒 CREDENTIALS REQUIRED

### 1. Google Drive OAuth2 API
**Used in nodes:**
- File Created (trigger)
- File Updated (trigger)
- Download Image
- Save image

**Setup:**
1. n8n Settings → Credentials → Add Credential
2. Select "Google Drive OAuth2 API"
3. Follow OAuth flow
4. Grant access to Google Drive

### 2. Google Sheets OAuth2 API
**Used in nodes:**
- Create Entry
- Update Entry to Done
- Update Entry to Error

**Setup:**
1. n8n Settings → Credentials → Add Credential
2. Select "Google Sheets OAuth2 API"
3. Follow OAuth flow
4. Grant access to Google Sheets

### 3. Google Gemini (PaLM) API
**Used in node:**
- Edit Image

**Setup:**
1. Get API key from https://ai.google.dev/
2. n8n Settings → Credentials → Add Credential
3. Select "Google Gemini(PaLM) API"
4. Paste API key

---

## 📊 USE CASES FOR ALPHA MEDICAL

### 1. Product Photo Enhancement
**Current state:** 100 products with varying image quality
**Solution:** Batch process all product images for uniform professional appearance

**Before:**
- Mixed backgrounds
- Inconsistent lighting
- Variable quality

**After:**
- Uniform studio background
- Professional lighting
- Consistent catalog quality

### 2. New Product Onboarding
**Process:**
1. Upload new product photos to Google Drive input folder
2. Workflow automatically processes within 5 minutes
3. Enhanced images ready for Shopify upload
4. Track all changes in Google Sheets

### 3. Seasonal Updates
**Use case:** Update product images for seasonal campaigns
- Upload updated photos
- Auto-process with consistent branding
- Replace on Shopify easily

### 4. A/B Testing
**Test different backgrounds:**
- Process same image with different prompts
- Compare conversion rates
- Choose best performing style

---

## 🚀 SETUP GUIDE FOR ALPHA MEDICAL

### Step 1: Create Google Drive Folders (5 min)

```bash
# Create folder structure:
Alpha Medical - Product Images/
├── Input/           # Upload original photos here
└── Output/          # Enhanced photos saved here
```

**Get folder IDs:**
1. Create both folders
2. Copy each folder ID from URL
3. Save for configuration

### Step 2: Create Google Sheet (5 min)

**Sheet name:** "Alpha Medical - Product Image Processing"

**Add sheet named:** "Photos"

**Headers (Row 1):**
```
File name | Status | Start Time | End Time | Input File | Output File | Notes
```

**Get sheet ID:**
- Copy from URL after /d/

### Step 3: Configure Credentials in n8n (10 min)

**Three credentials needed:**
1. Google Drive OAuth2 API
2. Google Sheets OAuth2 API
3. Google Gemini (PaLM) API

**Steps:**
1. Login to n8n: https://n8n.srv1168256.hstgr.cloud
2. Settings → Credentials
3. Add each credential type
4. Follow OAuth flows / paste API keys
5. Test connections

### Step 4: Import Workflow to n8n (5 min)

1. Login to n8n instance
2. Workflows → Create New Workflow
3. Click ⋮ (three dots) → Import from JSON
4. Paste the workflow JSON
5. Click Import

### Step 5: Update Workflow Configuration (5 min)

**Update these nodes:**

**1. File Created trigger:**
```
Folder to Watch: [Select your Input folder or paste ID]
Poll Time: Every 5 minutes
```

**2. File Updated trigger:**
```
Folder to Watch: [Select your Input folder or paste ID]
Poll Time: Every 5 minutes
```

**3. Workflow Configuration node:**
```javascript
{
  "google_sheet_id": "PASTE_YOUR_SHEET_ID",
  "dest_folder_id": "PASTE_YOUR_OUTPUT_FOLDER_ID",
  "text_prompt": "Transform this product photo into a high-quality, studio-style image. - Background: Remove the original background completely and replace it with a clean, light gray gradient (e.g., #f0f0f0 to #e0e0e0)... [full prompt]"
}
```

**4. All Google nodes (6 total):**
- Download Image → Google Drive credential
- Save image → Google Drive credential
- Create Entry → Google Sheets credential
- Update Entry to Done → Google Sheets credential
- Update Entry to Error → Google Sheets credential

**5. Edit Image node:**
- Google Gemini (PaLM) API credential

### Step 6: Test Workflow (10 min)

**Test process:**
1. Upload 1 test image to Input folder
2. Wait 5 minutes (trigger poll time)
3. Check n8n executions log
4. Verify entry in Google Sheets
5. Check Output folder for enhanced image
6. Review quality

**If successful:**
- Status in Sheets = "Completed"
- Output image exists
- Quality meets expectations

**If error:**
- Check execution log in n8n
- Verify credentials
- Check API quotas
- Review error in Sheets

---

## 📈 EXPECTED RESULTS

### Image Transformation Examples:

**Original Product Photo:**
- Mixed background (wall, table, etc.)
- Shadows and uneven lighting
- Amateur photo quality

**Enhanced Photo:**
- Clean gradient background (#f0f0f0 to #e0e0e0)
- Professional studio lighting
- No shadows, balanced exposure
- Product details preserved 100%
- E-commerce catalog ready

### Processing Metrics:

**Speed:**
- ~30-60 seconds per image (depends on file size)
- Parallel processing: Multiple images processed simultaneously

**Cost:**
- Google Gemini API: ~$0.01-0.05 per image (check current pricing)
- Google Drive: Free (within storage limits)
- Google Sheets: Free

**Accuracy:**
- Background removal: 95%+ accuracy
- Product preservation: 100% (text, details preserved)
- Color accuracy: Natural enhancement, no oversaturation

---

## 🐛 TROUBLESHOOTING

### Issue 1: Workflow Not Triggering

**Problem:** Images uploaded but workflow doesn't run

**Solutions:**
1. Check trigger poll time (default: 5 minutes)
2. Verify folder ID is correct
3. Check Google Drive credentials valid
4. Test trigger manually in n8n

### Issue 2: Image Processing Fails

**Problem:** Error in Edit Image node

**Solutions:**
1. Verify Google Gemini API credential
2. Check API quota not exceeded
3. Verify image format supported (JPG, PNG)
4. Check image size < 20MB

### Issue 3: Google Sheets Not Updating

**Problem:** No entry created or updated

**Solutions:**
1. Verify Google Sheets credential
2. Check sheet name is exactly "Photos"
3. Verify column headers match exactly
4. Check account has Editor access

### Issue 4: Poor Image Quality

**Problem:** Enhanced image doesn't look good

**Solutions:**
1. Adjust text prompt for better results
2. Try different background colors
3. Modify lighting instructions
4. Test with different input image quality

---

## 💡 BEST PRACTICES

### Input Images:

**Recommended:**
- High resolution (min 1500x1500px)
- Clear product visibility
- Minimal background clutter
- Good initial lighting
- Supported formats: JPG, PNG

**Avoid:**
- Very low resolution images
- Blurry or out-of-focus photos
- Extreme angles
- Heavy shadows obscuring product

### Workflow Management:

1. **Batch Processing:**
   - Upload 5-10 images at a time initially
   - Monitor quality before batch uploading all 100
   - Adjust prompt if needed

2. **Folder Organization:**
   - Keep Input folder clean (move processed to archive)
   - Organize Output by product category
   - Maintain naming conventions

3. **Quality Control:**
   - Review first 10 processed images
   - Adjust prompt for consistent results
   - Create quality checklist

4. **Cost Management:**
   - Monitor Google Gemini API usage
   - Set up billing alerts
   - Process in batches to control costs

---

## 📊 ALPHA MEDICAL IMPLEMENTATION PLAN

### Phase 1: Setup (Day 1)
- ✅ Create Google Drive folders
- ✅ Create Google Sheets tracker
- ✅ Configure credentials in n8n
- ✅ Import workflow
- ✅ Update configuration

### Phase 2: Testing (Day 2-3)
- ✅ Process 5 test images
- ✅ Review quality
- ✅ Adjust prompt if needed
- ✅ Validate tracking in Sheets
- ✅ Measure processing time

### Phase 3: Pilot (Week 1)
- ✅ Process 20 high-priority product images
- ✅ Update Shopify with enhanced images
- ✅ Monitor user engagement/conversion
- ✅ Collect feedback

### Phase 4: Full Rollout (Week 2-3)
- ✅ Process remaining 80 products
- ✅ Update all Shopify product images
- ✅ Document process for future use
- ✅ Train team on workflow

---

## 📝 CUSTOMIZATION FOR ALPHA MEDICAL

### Prompt Variations for Different Product Types:

**Massage Chairs:**
```
"Transform this massage chair photo into luxury showroom quality. Replace background with sophisticated gradient (#2c3e50 to #34495e). Professional dramatic lighting highlighting chair features. Preserve all controls and text perfectly. Luxury product catalog style."
```

**Therapeutic Devices:**
```
"Transform into clinical medical catalog style. Pure white background (#FFFFFF). Soft medical-grade lighting showing product details clearly. Preserve all medical labels and text. Professional healthcare product presentation."
```

**Bundles/Kits:**
```
"Transform into professional product bundle presentation. Light gradient background (#f8f9fa to #e9ecef). Balanced lighting showcasing all items. Preserve product arrangement. E-commerce bundle catalog quality."
```

---

## ✅ SUCCESS METRICS

**Track these metrics:**

1. **Processing Success Rate:** Target >95%
2. **Quality Score:** Manual review, target >4/5
3. **Time Saved:** vs manual editing
4. **Cost per Image:** Monitor API costs
5. **Conversion Impact:** A/B test enhanced vs original images

---

## 🔐 SECURITY & PRIVACY

**Data Protection:**
- Images stored in private Google Drive
- Only authorized account has access
- No public sharing enabled
- API credentials secured in n8n

**Compliance:**
- Images processed through Google Gemini API
- Review Google Gemini terms of service
- Ensure product images don't contain sensitive data
- GDPR compliant (no personal data in images)

---

## 📚 RESOURCES

**Documentation:**
- n8n Google Drive Trigger: https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.googledrivetrigger/
- n8n Google Gemini Node: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-langchain.googlegemini/
- Google Gemini API Docs: https://ai.google.dev/gemini-api/docs/image-generation
- Google Drive API: https://developers.google.com/drive
- Google Sheets API: https://developers.google.com/sheets

**Support:**
- n8n Community: https://community.n8n.io/
- Google AI Studio: https://ai.google.dev/

---

## 🎯 NEXT STEPS

1. **Review this document** completely
2. **Gather required information:**
   - Google account credentials
   - Google Gemini API key
   - Folder IDs
   - Sheet ID
3. **Schedule setup time** (1 hour)
4. **Test with 5 sample images**
5. **Adjust and optimize**
6. **Roll out to all 100 products**

---

**Status:** Ready for implementation
**Estimated Setup Time:** 1 hour
**Estimated Processing Time:** ~50-100 minutes for 100 images
**Cost Estimate:** ~$1-5 for 100 images (Google Gemini API)

**Prepared:** 2025-12-01
**For:** Alpha Medical Product Catalog Enhancement
