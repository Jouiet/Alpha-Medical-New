# ASSET GATHERING GUIDE
**Alpha Medical - Video Ads Image Collection**

**Created:** 2025-11-23
**Purpose:** Step-by-step guide to gather and organize product images for Creatify video creation
**Priority:** TOP 3 products first (Tourmaline Knee Pads, Magnetic Posture Corrector, Lower Back Brace)

---

## 🎯 PRIORITY PRODUCTS (Start Here)

### 1. Tourmaline Magnetic Knee Pads (FIRST - HIGHEST PRIORITY)
- **Score:** 0.923 (Rank #2)
- **Why First:** Perfect winter product, seniors demographic, self-heating tech demo-friendly
- **Shopify URL:** https://alphamedical.shop/products/tourmaline-magnetic-knee-pads-self-heating-support
- **Folder:** `video-ads-assets/products/tourmaline-knee-pads/`
- **First Video Type:** UGC Testimonial (15 sec)

### 2. Magnetic Posture Corrector (SECOND)
- **Score:** 0.934 (Rank #1 - HIGHEST HERO SCORE)
- **Why Second:** Office workers demographic, invisible design feature-rich
- **Shopify URL:** [Need to locate in Shopify]
- **Folder:** `video-ads-assets/products/magnetic-posture-corrector/`
- **Video Type:** Product Demo OR Before/After (posture transformation)

### 3. Lower Back Brace (THIRD)
- **Score:** 0.870 (Rank #6)
- **Why Third:** Medical-grade features, broad demographic appeal
- **Shopify URL:** [Need to locate in Shopify]
- **Folder:** `video-ads-assets/products/lower-back-brace/`
- **Video Type:** Before/After (pain relief, mobility)

---

## 📸 IMAGE TYPES NEEDED (Per Product)

### HERO IMAGES (Product Only)
**Purpose:** Main product shots for Creatify, clean professional look

**Requirements:**
- ✅ White or neutral background
- ✅ High resolution (min 1000x1000px)
- ✅ Well-lit, no shadows
- ✅ Product centered, clear details visible
- ✅ Multiple angles if available (front, side, back)

**Naming Convention:**
```
{product-handle}_hero_{angle}.jpg

Examples:
tourmaline-knee-pads_hero_front.jpg
tourmaline-knee-pads_hero_side.jpg
tourmaline-knee-pads_hero_pair.jpg
```

**Folder:** `video-ads-assets/products/{handle}/hero-images/`

**How Many:** Minimum 1, ideal 2-3

---

### LIFESTYLE IMAGES (Product in Use)
**Purpose:** Show product in realistic context, builds trust and relatability

**Requirements:**
- ✅ Person wearing/using product
- ✅ Realistic setting (home, office, outdoor, gym)
- ✅ Natural lighting preferred
- ✅ Demographically relevant model (age, gender match target)
- ✅ Activity context (walking, sitting, working, exercising)

**Naming Convention:**
```
{product-handle}_lifestyle_{context}.jpg

Examples:
tourmaline-knee-pads_lifestyle_senior-outdoor.jpg
tourmaline-knee-pads_lifestyle_home-sitting.jpg
magnetic-posture-corrector_lifestyle_office-desk.jpg
```

**Folder:** `video-ads-assets/products/{handle}/lifestyle-images/`

**How Many:** Minimum 1, ideal 2-4

**Context Ideas by Product:**
- **Tourmaline Knee Pads:** Senior outdoor winter, home sitting, walking stairs
- **Posture Corrector:** Office desk worker, under-clothes demonstration, laptop work
- **Lower Back Brace:** Person lifting, gardening, standing at counter, relieved expression

---

### FEATURE CLOSE-UPS (USP Details)
**Purpose:** Highlight unique selling points, technology, materials for Demo videos

**Requirements:**
- ✅ Macro/close-up shot of specific feature
- ✅ Clear detail (nodes, stays, fabric texture, adjustability)
- ✅ Good lighting to show texture/material
- ✅ Focused on ONE feature per image

**Naming Convention:**
```
{product-handle}_feature_{feature-name}.jpg

Examples:
tourmaline-knee-pads_feature_magnetic-nodes.jpg
tourmaline-knee-pads_feature_heating-zone.jpg
magnetic-posture-corrector_feature_invisible-thin.jpg
lower-back-brace_feature_steel-stays.jpg
```

**Folder:** `video-ads-assets/products/{handle}/feature-closeups/`

**How Many:** Minimum 1-2, ideal 3-4

**Feature Ideas by Product:**
- **Tourmaline Knee Pads:** Tourmaline mineral nodes, magnetic points, fabric breathability, velcro adjustability
- **Posture Corrector:** Magnetic nodes along spine, thin mesh fabric, adjustable straps, under-shirt demonstration
- **Lower Back Brace:** 6 steel stays, dual-layer compression, lumbar support zone, adjustable velcro

---

## 🗂️ STEP-BY-STEP: Gathering Images

### STEP 1: Access Shopify Product Page

**For Tourmaline Knee Pads (FIRST):**
1. Open: https://alphamedical.shop/products/tourmaline-magnetic-knee-pads-self-heating-support
2. Right-click on each product image → "Save Image As..."
3. Save to Desktop temporarily (we'll organize after)

**For Other Products:**
1. Go to: https://alphamedical.shop/collections/all
2. Search for product name (e.g., "Magnetic Posture Corrector")
3. Open product page
4. Save all images visible in gallery

**Download ALL images available** - we'll categorize them next.

---

### STEP 2: Categorize Downloaded Images

Open each image and decide category:

**Ask yourself:**
- **Is it product-only on white/neutral background?** → Hero image
- **Is it showing person using product in context?** → Lifestyle image
- **Is it close-up of specific feature/detail?** → Feature close-up

**Create temporary folders on Desktop:**
```
Desktop/
└── alpha-medical-assets-temp/
    ├── tourmaline-knee-pads-hero/
    ├── tourmaline-knee-pads-lifestyle/
    ├── tourmaline-knee-pads-features/
    ├── posture-corrector-hero/
    ├── posture-corrector-lifestyle/
    └── etc...
```

**Sort images into appropriate folders.**

---

### STEP 3: Rename Images with Convention

**Use consistent naming:**

```bash
# Example for Tourmaline Knee Pads
tourmaline-knee-pads_hero_front.jpg
tourmaline-knee-pads_hero_side.jpg
tourmaline-knee-pads_lifestyle_senior-outdoor.jpg
tourmaline-knee-pads_feature_magnetic-nodes.jpg
```

**Naming Tips:**
- All lowercase
- Use hyphens `-` not underscores in product handle
- Use underscores `_` to separate sections (handle_type_description)
- Keep description concise (2-3 words max)
- Use `.jpg` extension (consistent)

**Batch Rename (Mac):**
1. Select images in Finder
2. Right-click → Rename X items
3. Use "Replace Text" or "Format" with custom name

---

### STEP 4: Move to Final Folder Structure

**Navigate to:**
```
/Users/mac/Desktop/Alpha-Medical/video-ads-assets/products/
```

**For each product, move images to appropriate subfolders:**

**Example for Tourmaline Knee Pads:**
```bash
# Move hero images
mv ~/Desktop/alpha-medical-assets-temp/tourmaline-knee-pads-hero/* \
   ~/Desktop/Alpha-Medical/video-ads-assets/products/tourmaline-knee-pads/hero-images/

# Move lifestyle images
mv ~/Desktop/alpha-medical-assets-temp/tourmaline-knee-pads-lifestyle/* \
   ~/Desktop/Alpha-Medical/video-ads-assets/products/tourmaline-knee-pads/lifestyle-images/

# Move feature close-ups
mv ~/Desktop/alpha-medical-assets-temp/tourmaline-knee-pads-features/* \
   ~/Desktop/Alpha-Medical/video-ads-assets/products/tourmaline-knee-pads/feature-closeups/
```

**OR use Finder:**
1. Open two Finder windows side-by-side
2. Left: Temp folder with categorized images
3. Right: Final destination folder
4. Drag and drop images

---

### STEP 5: Verify Organization

**Check each product folder:**

```bash
cd ~/Desktop/Alpha-Medical/video-ads-assets/products/tourmaline-knee-pads/

# List all images
ls -la hero-images/
ls -la lifestyle-images/
ls -la feature-closeups/
```

**Expected result:**
```
hero-images/
  tourmaline-knee-pads_hero_front.jpg
  tourmaline-knee-pads_hero_side.jpg

lifestyle-images/
  tourmaline-knee-pads_lifestyle_senior-outdoor.jpg
  tourmaline-knee-pads_lifestyle_home-sitting.jpg

feature-closeups/
  tourmaline-knee-pads_feature_magnetic-nodes.jpg
  tourmaline-knee-pads_feature_heating-zone.jpg
```

**Minimum Requirements Met?**
- [ ] At least 1 hero image
- [ ] At least 1 lifestyle image
- [ ] At least 1 feature close-up
- [ ] All images properly named
- [ ] All images in correct folders

✅ **If all checked → Ready to create first video!**

---

## 📋 QUICK CHECKLIST: Tourmaline Knee Pads (FIRST VIDEO)

Use this checklist to ensure you have everything for the FIRST video creation:

### ✅ Assets Gathered
- [ ] Downloaded all images from Shopify product page
- [ ] At least 1 hero image (white background, product-only)
- [ ] At least 1 lifestyle image (senior wearing, outdoor/home)
- [ ] At least 1 feature close-up (magnetic nodes or heating zone)

### ✅ Images Renamed
- [ ] Consistent naming convention applied
- [ ] Format: `tourmaline-knee-pads_{type}_{description}.jpg`
- [ ] All lowercase, hyphens for handle, underscores for sections

### ✅ Images Organized
- [ ] Hero images in `video-ads-assets/products/tourmaline-knee-pads/hero-images/`
- [ ] Lifestyle images in `video-ads-assets/products/tourmaline-knee-pads/lifestyle-images/`
- [ ] Feature close-ups in `video-ads-assets/products/tourmaline-knee-pads/feature-closeups/`

### ✅ Ready for Creatify
- [ ] Selected 1 hero image to upload
- [ ] Selected 1 lifestyle image to upload
- [ ] Script customized from UGC template (~150 words)
- [ ] Creatify Creator account logged in (50 credits available)

**When all ✅ → Proceed to VIDEO_ADS_CREATION_PLAYBOOK.md Step 3!**

---

## 🔧 TOOLS & SHORTCUTS

### Image Viewing (Mac)
```bash
# Preview all images in folder
open hero-images/

# Quick Look (select file, press Space)
# Useful for quick category decisions
```

### Batch Operations (Mac Terminal)
```bash
# Count images in folder
ls hero-images/ | wc -l

# Find images by name pattern
find . -name "*hero*" -type f

# Copy (not move) images
cp source/* destination/
```

### Image Quality Check
**Before uploading to Creatify, verify:**
- Resolution: Right-click image → Get Info → Dimensions (should be min 1000x1000)
- File size: <10 MB (Creatify upload limit, though 1-3 MB is typical)
- Format: JPG or PNG (JPG preferred for Creatify)

**Quick resize if needed (Mac):**
1. Open image in Preview
2. Tools → Adjust Size
3. Set width to 1920px (maintain aspect ratio)
4. Save

---

## ❓ TROUBLESHOOTING

### "Shopify product page has very few images (2-3 only)"

**Solution:**
1. Use what's available (quality > quantity)
2. If no lifestyle images exist, use hero images only for first video
3. Consider creating lifestyle photos later (phone camera + natural lighting)
4. Start with Product Demo format instead of UGC (requires fewer lifestyle shots)

### "Images are low resolution or blurry"

**Solution:**
1. Look for higher resolution on Shopify (click image to expand, right-click expanded version)
2. Check if Shopify has "View full-size image" option
3. If Shopify images insufficient, check:
   - Supplier images (if dropshipping)
   - Product manufacturer website
   - AliExpress/Amazon listings (similar products for lifestyle inspiration)

### "Can't find specific product on Shopify"

**Solution:**
1. Check `product_matrix_complete.json` for exact product handle
2. Use handle in URL: `https://alphamedical.shop/products/{exact-handle}`
3. Search Shopify admin (if you have access)
4. Check collections: /collections/all or specific collections

### "Images from Shopify have watermarks or text overlays"

**Solution:**
1. Use them anyway if minor (Creatify can add new overlays)
2. If major watermark, crop it out (Preview → Tools → Rectangular Selection → Crop)
3. Or use clean hero images only, skip watermarked lifestyle shots

---

## 🎬 NEXT STEPS AFTER ASSET GATHERING

### Once Assets Ready for TOP 3 Products:

**IMMEDIATE (TODAY - 2025-11-23):**
1. Create Video #1: Tourmaline Knee Pads UGC (15 sec)
   - Use: `ugc-testimonial-template.txt`
   - Assets: 1 hero + 1 lifestyle + 1 feature
   - Upload to Creatify, render (1 credit)

**THIS WEEK (Week of Nov 25):**
2. Create Video #2: Magnetic Posture Corrector Demo (20 sec)
   - Use: `product-demo-template.txt`
   - Assets: 1 hero + 1 lifestyle + 2 features (invisible design + magnetic nodes)

3. Create Video #3: Lower Back Brace Before/After (12 sec)
   - Use: `before-after-template.txt`
   - Assets: 1 hero + 1 lifestyle (before/after context)

**PHASE 1 GOAL (By Dec 15):**
- ✅ 3 videos created
- ✅ 3 carousels created (PostNitro)
- ✅ All assets organized
- ✅ Production log updated

---

## 📞 SUPPORT REFERENCE

**If stuck, refer to:**
- **This guide:** Asset gathering process
- **VIDEO_ADS_CREATION_PLAYBOOK.md:** Complete video creation workflow (7 steps)
- **video-ads-assets/README.md:** Quick start guide and folder overview
- **Templates:** Specific script and configuration guides

**External Resources:**
- Shopify product pages: Source of images
- Creatify dashboard: https://app.creatify.ai
- Canva (if creating custom graphics): https://canva.com

---

**READY TO START?** Begin with Tourmaline Knee Pads - gather 3 images (hero + lifestyle + feature) and you're ready to create your first video! 🚀

**Estimated Time:**
- Asset gathering (3 products): 45-60 minutes
- First product only: 15-20 minutes

**Start NOW:** Open https://alphamedical.shop/products/tourmaline-magnetic-knee-pads-self-heating-support
