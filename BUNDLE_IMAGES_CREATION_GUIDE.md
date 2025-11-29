# BUNDLE IMAGES CREATION GUIDE
## Create Professional Bundle Images for Complete Care Kits (10 Products)

**Problem:** 10 Complete Care Kit bundles have NO images → Cannot sell = -$50K-80K Year 1
**Solution:** Create composite images showing all 4 products in each bundle
**Time estimate:** 2-3 hours total (10-15min per bundle)

---

## 🎯 REQUIREMENTS

**Image specs:**
- **Size:** 2048 x 2048 px (Shopify recommended)
- **Format:** PNG or JPG
- **Style:** Clean, professional, medical/healthcare aesthetic
- **Content:** All 4 products visible + bundle title + savings badge

---

## 🛠️ METHOD 1: CANVA (RECOMMENDED - FASTEST)

**Step 1: Setup (5min)**

1. Go to: https://www.canva.com
2. Create free account or login
3. Click "Create a design" → "Custom size" → 2048 x 2048 px
4. Search template: "Product Collage" or "Product Bundle"

**Step 2: Create Template (10min first bundle, then duplicate)**

**Base layout:**
```
┌─────────────────────────────────┐
│  BUNDLE TITLE (top)             │
│                                  │
│  [Product 1]    [Product 2]     │  ← 2x2 grid
│                                  │
│  [Product 3]    [Product 4]     │
│                                  │
│  SAVE $XX | 4 ITEMS (bottom)    │
└─────────────────────────────────┘
```

**Colors:**
- Background: White (#FFFFFF) or light medical blue (#F0F8FF)
- Text: Dark blue/navy (#1A365D)
- Accent: Your brand color or medical green (#48BB78)

**Step 3: Get Product Images**

For each bundle, you need images of the 4 component products:

**Option A: Screenshot from your Shopify store**
1. Go to: https://www.alphamedical.shop/products/[product-handle]
2. Right-click product image → "Save image as"
3. Repeat for all 4 products in bundle

**Option B: From Shopify Admin**
1. Shopify Admin → Products
2. Find each product in bundle
3. Download primary image

**Step 4: Build Each Bundle Image (10-15min)**

1. **Add product images** (drag & drop into Canva)
   - Remove backgrounds if needed (Canva has auto background remover)
   - Arrange in 2x2 grid
   - Equal spacing, equal size

2. **Add bundle title** (top)
   - Text: Bundle name (e.g., "Active Athlete Complete Care Kit")
   - Font: Clean, professional (Montserrat, Poppins, or Roboto)
   - Size: 48-60px
   - Color: Navy/dark blue

3. **Add savings badge** (bottom or corner)
   - Circle or rounded rectangle
   - Text: "SAVE $XX" or "4-ITEM KIT" or "BUNDLE & SAVE"
   - Contrasting color (green or your brand color)

4. **Add subtle medical touches** (optional)
   - Small medical cross icon
   - Heartbeat line graphic
   - Wellness symbols

5. **Download:**
   - File type: PNG (transparent background) or JPG
   - Quality: Highest
   - Size: 2048 x 2048 px

**Step 5: Upload to Shopify**

See "UPLOAD METHOD" section below.

---

## 🛠️ METHOD 2: PHOTOSHOP/GIMP (ADVANCED - MORE CONTROL)

**If you're comfortable with photo editing:**

1. Create 2048 x 2048 px canvas
2. Place 4 product images in grid
3. Add text layers (title + savings)
4. Export as PNG/JPG

---

## 🛠️ METHOD 3: QUICK & DIRTY (FASTEST - 5MIN PER BUNDLE)

**Use existing product images + text overlay:**

1. Go to: https://www.remove.bg (remove backgrounds)
2. Upload product images → Download transparent PNGs
3. Go to: https://www.photopea.com (free Photoshop alternative)
4. Create 2048x2048 canvas
5. Drag 4 products → Arrange
6. Add text: Bundle title + "4-Item Kit"
7. Export PNG

---

## 📤 UPLOAD METHOD (AUTOMATED)

**After creating all 10 images**, save them with these exact names:

```
active-athlete-sports-enthusiast.png
active-athlete-knee-support-kit.png
beauty-wellness-premium-facial-therapy-kit.png
beauty-wellness-enthusiast.png
comprehensive-therapy-user.png
elderly-mobility-support.png
foot-care-bunion-relief.png
office-worker-back-neck-relief-kit.png
office-worker-chronic-pain.png
post-injury-post-surgery-recovery.png
```

**Then run the upload script:**

```bash
# Put all images in a folder called "bundle_images"
mkdir bundle_images
# Move your 10 images into bundle_images/

# Run upload script (I'll create this for you)
python3 upload_bundle_images.py
```

---

## 📋 BUNDLE DETAILS (for reference)

| # | Bundle Name | Price | Products | Image Name |
|---|-------------|-------|----------|------------|
| 1 | Active Athlete & Sports Enthusiast | $97.93 | 4 | active-athlete-sports-enthusiast.png |
| 2 | Active Athlete - Knee Support Kit | $112.01 | 4 | active-athlete-knee-support-kit.png |
| 3 | Beauty & Wellness - Premium Facial Therapy Kit | $156.06 | 4 | beauty-wellness-premium-facial-therapy-kit.png |
| 4 | Beauty & Wellness Enthusiast | $80.90 | 4 | beauty-wellness-enthusiast.png |
| 5 | Comprehensive Therapy User | $112.83 | 4 | comprehensive-therapy-user.png |
| 6 | Elderly / Mobility Support | $100.93 | 4 | elderly-mobility-support.png |
| 7 | Foot Care & Bunion Relief | $78.38 | 4 | foot-care-bunion-relief.png |
| 8 | Office Worker - Back & Neck Relief Kit | $83.42 | 4 | office-worker-back-neck-relief-kit.png |
| 9 | Office Worker with Chronic Pain | $104.65 | 4 | office-worker-chronic-pain.png |
| 10 | Post-Injury / Post-Surgery Recovery | $112.39 | 4 | post-injury-post-surgery-recovery.png |

---

## ✅ QUALITY CHECKLIST

Before uploading, check each image:

- [ ] All 4 products clearly visible
- [ ] Bundle title readable
- [ ] Professional appearance (clean, aligned)
- [ ] 2048 x 2048 px (or larger, Shopify will resize)
- [ ] No blurry/pixelated images
- [ ] Consistent style across all 10 bundles
- [ ] Savings/value messaging visible
- [ ] Medical/healthcare aesthetic maintained

---

## 🚀 NEXT STEPS

1. **Create images** (2-3 hours) using Method 1, 2, or 3
2. **Save images** in `bundle_images/` folder with exact names above
3. **Run upload script** (I'll create this when you're ready)
4. **Verify** images appear on storefront
5. **Test checkout** with a bundle product

---

## 💡 PRO TIPS

**Tip 1:** Create the first bundle, then duplicate the Canva design 9 times and just swap products
**Tip 2:** Use Shopify's existing product images (already on brand)
**Tip 3:** Add "BUNDLE & SAVE" badge prominently to increase conversions
**Tip 4:** If short on time, use Method 3 (quick & dirty) - a simple image is 1000x better than NO image
**Tip 5:** Consider hiring on Fiverr ($10-20 for 10 bundle images, delivered in 24h)

---

## 🆘 ALTERNATIVE: HIRE DESIGNER (FASTEST IF YOU VALUE TIME)

**Fiverr/Upwork (24-48h, $15-30 for 10 images):**

Brief:
```
I need 10 product bundle images for my medical equipment store.

Requirements:
- 2048 x 2048 px, PNG format
- Each image shows 4 products arranged in 2x2 grid
- Include bundle title at top
- Include "4-ITEM KIT" or "SAVE $XX" badge
- Clean, professional, medical/healthcare aesthetic
- White or light blue background

I will provide:
- List of 10 bundles (product names + component products)
- Individual product images for all components
- Brand colors/style guide

Delivery: 10 high-quality PNG images (2048x2048px)
Timeline: 24-48 hours
Budget: $15-30
```

Search: "product bundle images" or "product collage design"

---

**Questions? Need help with any step? Let me know!**
