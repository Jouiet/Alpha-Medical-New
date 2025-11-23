# VIDEO ADS SCRIPTS
**Automation Tools for Alpha Medical Video Ads Workflow**

---

## 📜 AVAILABLE SCRIPTS

### 1. asset_organizer.py
**Purpose:** Automate product folder creation and asset verification

**Use Cases:**
- Create complete folder structure for new products
- Verify existing product has all required folders and files
- Check readiness for video creation (are assets complete?)
- Audit all products at once

---

## 🚀 USAGE GUIDE

### Create Folder Structure for New Product

**Command:**
```bash
python3 asset_organizer.py --create {product-handle}
```

**Example:**
```bash
cd /Users/mac/Desktop/Alpha-Medical/video-ads-assets/scripts/

python3 asset_organizer.py --create tourmaline-knee-pads
```

**What it creates:**
```
products/tourmaline-knee-pads/
├── hero-images/
├── lifestyle-images/
├── feature-closeups/
└── metadata/
    ├── shopify-url.txt
    └── product-info.txt (template)
```

**Output:**
```
✅ Created product folder: tourmaline-knee-pads
   ✅ Created: hero-images/
   ✅ Created: lifestyle-images/
   ✅ Created: feature-closeups/
   ✅ Created: metadata/
   ✅ Created: metadata/shopify-url.txt
   ✅ Created: metadata/product-info.txt (template)

🎉 Product structure ready: tourmaline-knee-pads
📂 Location: /Users/mac/Desktop/Alpha-Medical/video-ads-assets/products/tourmaline-knee-pads

📝 Next steps:
   1. Update metadata/product-info.txt with product details
   2. Add Shopify URL to metadata/shopify-url.txt
   3. Gather and organize product images into subfolders
```

---

### Verify Product Readiness

**Command:**
```bash
python3 asset_organizer.py --verify {product-handle}
```

**Example:**
```bash
python3 asset_organizer.py --verify tourmaline-knee-pads
```

**What it checks:**
- ✅ All required folders exist
- ✅ Metadata files present
- ✅ Images counted in each folder
- ✅ Overall readiness for video creation

**Output Example (Ready):**
```
📋 VERIFYING: tourmaline-knee-pads
📂 Location: /Users/mac/Desktop/Alpha-Medical/video-ads-assets/products/tourmaline-knee-pads

✅ hero-images/
✅ lifestyle-images/
✅ feature-closeups/
✅ metadata/

✅ metadata/shopify-url.txt
✅ metadata/product-info.txt

✅ hero-images/: 2 image(s)
      - tourmaline-knee-pads_hero_front.jpg
      - tourmaline-knee-pads_hero_side.jpg
✅ lifestyle-images/: 1 image(s)
      - tourmaline-knee-pads_lifestyle_senior-outdoor.jpg
✅ feature-closeups/: 2 image(s)
      - tourmaline-knee-pads_feature_nodes.jpg
      - tourmaline-knee-pads_feature_heating.jpg

==================================================
READINESS CHECK:
✅ Hero images: Ready
✅ Lifestyle images: Ready
⚠️ Feature close-ups: Ready
✅ Metadata files: Complete

🎉 READY TO CREATE VIDEO!
   Follow: VIDEO_ADS_CREATION_PLAYBOOK.md
   Templates: video-ads-assets/templates/
==================================================
```

**Output Example (Not Ready):**
```
📋 VERIFYING: magnetic-posture-corrector
📂 Location: /Users/mac/Desktop/Alpha-Medical/video-ads-assets/products/magnetic-posture-corrector

✅ hero-images/
✅ lifestyle-images/
✅ feature-closeups/
✅ metadata/

✅ metadata/shopify-url.txt
✅ metadata/product-info.txt

⚠️ hero-images/: 0 image(s)
⚠️ lifestyle-images/: 0 image(s)
⚠️ feature-closeups/: 0 image(s)

==================================================
READINESS CHECK:
❌ Hero images: Need at least 1
❌ Lifestyle images: Need at least 1
❌ Feature close-ups: Recommended (optional)
✅ Metadata files: Complete

⚠️  NOT READY YET
   Next steps:
   1. Add at least 1 hero image to magnetic-posture-corrector/hero-images/
   2. Add at least 1 lifestyle image to magnetic-posture-corrector/lifestyle-images/
   3. Complete metadata files in magnetic-posture-corrector/metadata/
==================================================
```

---

### Verify All Products at Once

**Command:**
```bash
python3 asset_organizer.py --verify-all
```

**Example:**
```bash
cd /Users/mac/Desktop/Alpha-Medical/video-ads-assets/scripts/
python3 asset_organizer.py --verify-all
```

**What it does:**
- Scans all product folders in `products/`
- Runs verification check on each
- Provides summary of which products are ready

**Output Example:**
```
============================================================
VERIFYING ALL PRODUCTS (3 found)
============================================================

📋 VERIFYING: tourmaline-knee-pads
[... verification output ...]
🎉 READY TO CREATE VIDEO!

📋 VERIFYING: magnetic-posture-corrector
[... verification output ...]
⚠️  NOT READY YET

📋 VERIFYING: lower-back-brace
[... verification output ...]
🎉 READY TO CREATE VIDEO!

============================================================
SUMMARY: 2/3 products ready for video creation
============================================================

✅ READY FOR VIDEO CREATION:
   - tourmaline-knee-pads
   - lower-back-brace

⚠️  NEED MORE ASSETS:
   - magnetic-posture-corrector
```

---

## 💡 COMMON WORKFLOWS

### Workflow 1: Adding a New Product

```bash
# 1. Create folder structure
python3 asset_organizer.py --create new-product-handle

# 2. Gather images from Shopify
# (Follow ASSET_GATHERING_GUIDE.md)

# 3. Move images to appropriate folders
# hero-images/, lifestyle-images/, feature-closeups/

# 4. Verify readiness
python3 asset_organizer.py --verify new-product-handle

# 5. If ready, create video!
# (Follow VIDEO_ADS_CREATION_PLAYBOOK.md)
```

---

### Workflow 2: Checking What's Ready for Video Creation

```bash
# Quick check all products
python3 asset_organizer.py --verify-all

# Shows which products have complete assets
# Start with products marked "READY"
```

---

### Workflow 3: Troubleshooting Missing Assets

```bash
# Verify specific product
python3 asset_organizer.py --verify tourmaline-knee-pads

# Script will tell you exactly what's missing:
# - "Need at least 1 hero image"
# - "Need at least 1 lifestyle image"
# - etc.

# Gather missing assets, then re-verify
```

---

## 🛠️ TECHNICAL DETAILS

### Requirements
- Python 3.6+
- No external dependencies (uses only standard library)

### File Paths
- **Script location:** `video-ads-assets/scripts/asset_organizer.py`
- **Products folder:** `video-ads-assets/products/`
- **Base directory:** `/Users/mac/Desktop/Alpha-Medical/`

### Folder Structure Created
```
products/{product-handle}/
├── hero-images/          # Product-only, white background
├── lifestyle-images/     # Product in use, realistic context
├── feature-closeups/     # Close-ups of USPs, technology
└── metadata/
    ├── shopify-url.txt   # Auto-filled with URL
    └── product-info.txt  # Template to fill manually
```

---

## 📋 READINESS CRITERIA

**Minimum requirements for "READY TO CREATE VIDEO":**

1. **Hero Images:** At least 1 image ✅
2. **Lifestyle Images:** At least 1 image ✅
3. **Metadata Files:** Both files present ✅
4. **Feature Close-ups:** Recommended but optional ⚠️

**Optimal setup:**
- 2-3 hero images (multiple angles)
- 2-4 lifestyle images (different contexts)
- 2-4 feature close-ups (each USP)
- Metadata fully filled out (no [FILL] placeholders)

---

## 🔄 FUTURE SCRIPTS (Planned)

### batch_video_creator.py (Coming Soon)
**Purpose:** Automate video creation for multiple products using Creatify API

**Planned Features:**
- Batch upload images to Creatify
- Generate videos from templates
- Track rendering status
- Download completed videos
- Update production log

**Status:** Waiting for API implementation (Phase 2)

---

## ❓ TROUBLESHOOTING

### "No such file or directory: products/"

**Solution:**
```bash
# Make sure you're running from scripts/ folder
cd /Users/mac/Desktop/Alpha-Medical/video-ads-assets/scripts/

# Or use absolute paths
python3 /Users/mac/Desktop/Alpha-Medical/video-ads-assets/scripts/asset_organizer.py --verify-all
```

---

### "Permission denied"

**Solution:**
```bash
# Make script executable
chmod +x asset_organizer.py

# Then run
./asset_organizer.py --verify-all
```

---

### "Product folder already exists"

**Solution:**
- This is intentional to prevent overwriting existing work
- If you really want to recreate: manually delete folder first, then run --create
- Or just use --verify to check existing folder

---

## 📞 SUPPORT

**Documentation:**
- Asset gathering process: `ASSET_GATHERING_GUIDE.md`
- Video creation workflow: `VIDEO_ADS_CREATION_PLAYBOOK.md`
- Templates: `video-ads-assets/templates/`

**Script Help:**
```bash
python3 asset_organizer.py --help
```

---

**READY TO USE?** Start with:
```bash
cd /Users/mac/Desktop/Alpha-Medical/video-ads-assets/scripts/
python3 asset_organizer.py --verify-all
```

See which products need assets, gather images, then create videos! 🚀
