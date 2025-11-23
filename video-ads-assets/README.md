# VIDEO ADS ASSETS
**Alpha Medical - Organization Centrale Assets Vidéo**

**Created:** 2025-11-23
**Purpose:** Structure standardisée pour création vidéos ads Creatify
**Reference:** VIDEO_ADS_CREATION_PLAYBOOK.md

---

## 📁 STRUCTURE OVERVIEW

```
video-ads-assets/
│
├── products/              # Assets organisés par produit (photos, metadata)
│   ├── tourmaline-knee-pads/
│   ├── lower-back-brace/
│   ├── magnetic-posture-corrector/
│   └── README.md         # Guide organisation produits
│
├── templates/            # Scripts réutilisables par type vidéo
│   ├── ugc-testimonial-template.txt
│   ├── before-after-template.txt
│   ├── product-demo-template.txt
│   ├── comparison-template.txt
│   └── educational-template.txt
│
├── outputs/              # Vidéos finales rendues Creatify
│   ├── production-log.md
│   ├── README.md
│   └── backups/
│
└── scripts/              # Python automation (future use)
    ├── batch_video_creator.py
    └── asset_organizer.py
```

---

## 🚀 QUICK START GUIDE

### First Time Setup (5 minutes)

**1. Read Documentation:**
```bash
# Main playbook (comprehensive guide)
open VIDEO_ADS_CREATION_PLAYBOOK.md

# Product assets guide
open video-ads-assets/products/README.md
```

**2. Verify Structure:**
```bash
cd video-ads-assets/
ls -la  # Should see: products/ templates/ outputs/ scripts/
```

**3. Check Creatify Account:**
- Login: https://app.creatify.ai
- Verify: Creator Plan $39/mois active
- Credits: 50 available

---

### Creating Your First Video (Step-by-Step)

**STEP 1: Prepare Product Assets** (15-30 min)

```bash
# Navigate to products folder
cd products/

# Check TOP 3 priority products
ls -la
# Should see: tourmaline-knee-pads/ lower-back-brace/ magnetic-posture-corrector/

# Start with #1 priority (Tourmaline Knee Pads)
cd tourmaline-knee-pads/

# Check subfolders
ls -la
# Should see: hero-images/ lifestyle-images/ feature-closeups/ metadata/
```

**Gather images:**
1. Open `metadata/shopify-url.txt` → Copy URL
2. Visit Shopify product page
3. Download/save images to appropriate folders:
   - 1+ hero image (white background) → `hero-images/`
   - 1+ lifestyle image (usage context) → `lifestyle-images/`
   - 1+ feature close-up (USP detail) → `feature-closeups/`

**Name images correctly:**
```
tourmaline-knee-pads_hero_front.jpg
tourmaline-knee-pads_lifestyle_senior-outdoor.jpg
tourmaline-knee-pads_feature_magnetic-nodes.jpg
```

**Complete metadata:**
```bash
# Open and fill missing info
open metadata/product-info.txt
# Fill: Actual price, verify certifications, add testimonials
```

---

**STEP 2: Select Script Template** (10 min)

```bash
# Navigate to templates
cd ../../templates/

# Open UGC template (recommended for first video)
open ugc-testimonial-template.txt
```

**Customize script:**
1. Replace `{PAIN_POINT_STATEMENT}` with relatable hook
2. Replace `{PRODUCT_NAME}` with full product name
3. Replace `{USP_1}`, `{USP_2}` with unique selling points
4. Replace `{DISCOUNT_CODE}` with active code

**Example customized:**
```
[0-3s] "My knees used to ache every winter morning..."
[4-7s] "...until I discovered these heated knee pads."
[8-11s] "Self-heating technology. No more pain, even in -10°C."
[12-15s] "Magnetic therapy that works. Link in bio."
Overlay: "alphamedical.shop | -20% CODE: WARMKNEES20"
```

---

**STEP 3: Create in Creatify** (15-20 min)

**Login Creatify:**
```
https://app.creatify.ai
```

**Method A: URL-to-Video** (Faster)
1. Click "URL to Video"
2. Paste: https://alphamedical.shop/products/tourmaline-knee-pads...
3. Wait auto-scrape
4. Edit script if needed

**Method B: Custom Script** (More control)
1. Click "Create from Script"
2. Paste customized script
3. Upload product images manually

**Configure:**
- Format: 9:16 vertical
- Duration: 15 seconds
- Captions: ENABLED ✅
- Music: Upbeat Soft, -18dB

**Select Avatar:**
- Age: 60-65
- Gender: Female
- Setting: Outdoor winter
- Style: Casual warm clothing

**Select Voice:**
- Language: English (US)
- Gender: Female
- Tone: Mature, warm, grateful

---

**STEP 4: Preview & QA** (10-15 min)

**Click "Preview" (FREE, unlimited)**

**Check Quality Checklist:**
- [ ] Hook strong (0-3 sec)
- [ ] Lip-sync natural
- [ ] Captions readable
- [ ] CTA clear + discount visible
- [ ] Duration exact (15 sec)
- [ ] Audio clear (voice + music balance)

**If issues:** Adjust avatar, voice, script → Re-preview
**If perfect:** Proceed to render

---

**STEP 5: Render & Download** (5 min + wait 10-30 min)

**Final check:**
- [ ] Preview watched 2+ times
- [ ] All QA checkboxes ✅
- [ ] Ready to use 1 credit

**Click "Render Video"**
- Credit used: 1/50
- Wait: 10-30 minutes (email notification)

**When ready:**
1. Download MP4
2. Rename: `2025-11-23_tourmaline-knee-pads_ugc_v1.mp4`
3. Move to: `video-ads-assets/outputs/`
4. Copy to: `video-ads-assets/outputs/backups/`

---

**STEP 6: Log Production** (5 min)

```bash
# Open production log
open outputs/production-log.md
```

**Add entry:**
- Date, product, type
- Assets used
- Creatify settings (Avatar ID, Voice ID)
- Script details
- Rendering time
- Quality check results

**Update metadata:**
```bash
# Update product metadata with video filename
open products/tourmaline-knee-pads/metadata/product-info.txt
# Add: Video Created: 2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
```

---

**STEP 7: Upload to Meta Ads** (Next step)

**Video ready!** Now follow Meta Ads campaign setup:
- See: TOP_10_HERO_PRODUCTS_MAPPING.md
- Budget: $60 (7 days)
- Platform: TikTok + IG Reels
- Audience: Seniors 65+

---

## 📚 DOCUMENTATION REFERENCE

**Primary Docs:**
1. **VIDEO_ADS_CREATION_PLAYBOOK.md** - Comprehensive 7-step workflow
2. **products/README.md** - Product assets organization guide
3. **outputs/README.md** - Video naming & tracking guide
4. **TOP_10_HERO_PRODUCTS_MAPPING.md** - Product prioritization & ad strategy

**Templates:**
- `templates/ugc-testimonial-template.txt` - 15 sec UGC format
- `templates/before-after-template.txt` - 12 sec transformation
- `templates/product-demo-template.txt` - 20 sec demo
- `templates/comparison-template.txt` - 25 sec vs competitors
- `templates/educational-template.txt` - 30 sec authority

**Metadata Templates:**
- `products/{handle}/metadata/product-info.txt` - Complete product data
- `outputs/production-log.md` - Video creation tracking

---

## ✅ CHECKLIST: Ready to Create First Video

Before starting, ensure:

**Account & Tools:**
- [ ] Creatify Creator account active ($39/mois)
- [ ] 50 credits available
- [ ] PostNitro account setup (for carousels future)

**Documentation:**
- [ ] VIDEO_ADS_CREATION_PLAYBOOK.md read completely
- [ ] Understand 7-step workflow
- [ ] Templates folder reviewed

**Assets Prepared:**
- [ ] Priority product selected (Tourmaline Knee Pads recommended)
- [ ] Min 1 hero image gathered
- [ ] Min 1 lifestyle image gathered
- [ ] Product metadata completed
- [ ] Script customized from template

**Creatify Knowledge:**
- [ ] Understand URL-to-Video vs Custom Script
- [ ] Know how to select avatar + voice
- [ ] Familiar with preview function (FREE)
- [ ] Understand credit system (1 credit per render)

**When all ✅ → START CRÉATION!**

---

## 🎯 SUCCESS METRICS

**Phase 1 Goals (3 weeks):**
- [ ] 3 videos created (TOP 3 products)
- [ ] 3 carousels created (PostNitro)
- [ ] All assets organized in proper folders
- [ ] Production log maintained
- [ ] 1-2 winning formats identified

**Quality Benchmarks:**
- [ ] Preview-to-render ratio: <3 previews per render (efficiency)
- [ ] QA pass rate: 100% (no failed renders)
- [ ] Production time: <1h per video (including asset prep)
- [ ] Credits used: <10 credits Phase 1 (conservative)

---

## 🔄 MAINTENANCE & UPDATES

**Weekly:**
- Update production-log.md with performance data
- Add new products as needed (follow naming convention)
- Archive old/unused assets

**Monthly:**
- Review template performance (which scripts work best)
- Update metadata with learnings
- Optimize asset library (delete unused)

**Quarterly:**
- Audit entire structure
- Update playbook with new learnings
- Consider API upgrade if >10 videos/month

---

## 🆘 TROUBLESHOOTING

**Common issues:**

**1. "Can't find product images"**
→ Check: products/{handle}/hero-images/
→ Solution: Download from Shopify product page

**2. "Creatify preview not loading"**
→ Check: Internet connection, browser cache
→ Solution: Refresh page, try different browser

**3. "Rendering taking >30 min"**
→ Check: Creatify status page, email
→ Solution: Wait up to 60 min, then contact support

**4. "Video file too large (>100 MB)"**
→ Check: File size in outputs/
→ Solution: Compress with HandBrake or re-render at lower quality

**5. "Don't know which product to start with"**
→ Check: TOP_10_HERO_PRODUCTS_MAPPING.md
→ Solution: Start with Rank #2 (Tourmaline Knee Pads) - winter optimal

**Full troubleshooting:** See VIDEO_ADS_CREATION_PLAYBOOK.md Section "TROUBLESHOOTING"

---

## 📞 SUPPORT

**Internal:**
- Playbook: VIDEO_ADS_CREATION_PLAYBOOK.md
- This README: video-ads-assets/README.md
- Production log: outputs/production-log.md

**External:**
- Creatify Support: [email protected]
- Creatify Dashboard: https://app.creatify.ai
- PostNitro Support: [if needed for carousels]

---

**READY TO CREATE? Follow Quick Start Guide above! 🚀**

**First video target:** 2025-11-23 (TODAY!)
**Status:** ✅ All documentation & structure ready
