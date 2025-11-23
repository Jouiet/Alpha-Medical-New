# VIDEO ADS CREATION PLAYBOOK
**Alpha Medical - Pattern Standard pour Toutes Vidéos Ads**

**Version:** 1.0
**Date:** 22 Novembre 2025
**Auteur:** Alpha Medical Marketing Team
**Objectif:** Pattern réutilisable, documenté, actionnable pour création vidéos ads Creatify

---

## TABLE DES MATIÈRES

1. [STRUCTURE DOSSIERS & ASSETS](#structure-dossiers--assets)
2. [WORKFLOW STANDARD 7 ÉTAPES](#workflow-standard-7-étapes)
3. [TEMPLATES PAR TYPE DE VIDÉO](#templates-par-type-de-vidéo)
4. [NAMING CONVENTIONS](#naming-conventions)
5. [QUALITY CHECKLIST](#quality-checklist)
6. [TROUBLESHOOTING](#troubleshooting)

---

## STRUCTURE DOSSIERS & ASSETS

### 📁 Arborescence Complète

```
/video-ads-assets/
├── products/                          # Assets organisés par produit
│   ├── tourmaline-knee-pads/
│   │   ├── hero-images/              # Images principales produit (fond blanc)
│   │   │   ├── front-view.jpg
│   │   │   ├── side-view.jpg
│   │   │   └── packaging.jpg
│   │   ├── lifestyle-images/         # Photos en contexte d'usage
│   │   │   ├── senior-wearing.jpg
│   │   │   ├── outdoor-winter.jpg
│   │   │   └── before-after.jpg
│   │   ├── feature-closeups/         # Close-ups fonctionnalités
│   │   │   ├── magnetic-nodes.jpg
│   │   │   ├── heated-zone.jpg
│   │   │   └── strap-detail.jpg
│   │   └── metadata/                 # Info produit
│   │       ├── product-info.txt
│   │       └── shopify-url.txt
│   │
│   ├── lower-back-brace/
│   │   ├── hero-images/
│   │   ├── lifestyle-images/
│   │   ├── feature-closeups/
│   │   └── metadata/
│   │
│   └── magnetic-posture-corrector/
│       ├── hero-images/
│       ├── lifestyle-images/
│       ├── feature-closeups/
│       └── metadata/
│
├── templates/                         # Templates scripts réutilisables
│   ├── ugc-testimonial-template.txt
│   ├── before-after-template.txt
│   ├── product-demo-template.txt
│   ├── comparison-template.txt
│   └── educational-template.txt
│
├── outputs/                           # Vidéos finales rendues
│   ├── 2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
│   ├── 2025-11-24_lower-back-brace_ba_v1.mp4
│   └── production-log.md
│
└── scripts/                           # Scripts Python automation (future)
    ├── batch_video_creator.py
    └── asset_organizer.py
```

---

### 📸 GUIDE: Sélection Images Produit pour Vidéo Ads

#### **Type 1: Hero Images** (fond blanc, studio lighting)

**Usage:** Product showcase, CTA final frame
**Specs:**
- Format: 1:1 square ou 9:16 vertical
- Résolution: Min 1080px largeur
- Background: Blanc pur (RGB 255,255,255)
- Lighting: Studio, ombres minimales
- Product: Centré, 70% frame

**Où obtenir:**
- Shopify product images (URLs directes)
- Photos studio produit
- Manufacturer images (si haute qualité)

**Naming convention:**
- `{product-handle}_hero_front.jpg`
- `{product-handle}_hero_angle45.jpg`
- `{product-handle}_hero_packaging.jpg`

---

#### **Type 2: Lifestyle Images** (en contexte, personne utilisant)

**Usage:** Démonstration usage, before/after, testimonial scenes
**Specs:**
- Format: 9:16 vertical preferred
- Résolution: Min 1080x1920px
- Background: Natural setting (home, office, outdoor)
- Person: Visible, relatable demographics match
- Product: Clairement visible en usage

**Exemples requis:**
- Senior wearing knee brace outdoor winter ❄️
- Office worker with posture corrector at desk 💻
- Before (bad posture) vs After (corrected) 📐

**Sources:**
- Stock photos (Unsplash, Pexels) avec product overlay
- UGC customer photos (avec permission)
- Professional photoshoot (recommandé long-terme)

**Naming convention:**
- `{product-handle}_lifestyle_senior-outdoor.jpg`
- `{product-handle}_lifestyle_office-desk.jpg`
- `{product-handle}_lifestyle_before-after.jpg`

---

#### **Type 3: Feature Close-ups** (détails fonctionnalités)

**Usage:** Highlight unique selling points, technical demo
**Specs:**
- Format: Any (recadré dans vidéo)
- Résolution: High-res (permettre zoom)
- Focus: Une feature par image
- Lighting: Emphasize texture/materials

**Exemples requis:**
- Magnetic therapy nodes close-up 🧲
- Heated zone technology ♨️
- Adjustable strap mechanism ⚙️
- 6 steel stays detail 🔩

**Naming convention:**
- `{product-handle}_feature_magnetic-nodes.jpg`
- `{product-handle}_feature_heated-zone.jpg`
- `{product-handle}_feature_strap-adjust.jpg`

---

### 📋 Template: product-info.txt (Metadata)

**Créer ce fichier pour chaque produit:**

```
# PRODUCT METADATA
# Generated: 2025-11-23

Product Name: Tourmaline Magnetic Knee Pads | Self-Heating Support
Product Handle: tourmaline-magnetic-knee-pads-self-heating-support
Shopify URL: https://alphamedical.shop/products/tourmaline-magnetic-knee-pads-self-heating-support

## Hero Score
Rank: #2
Score: 0.923
Winter Score: 1.00
Primary Demo: Seniors 65+

## Unique Selling Points (USPs)
1. Self-heating technology (no batteries)
2. Magnetic therapy nodes (tourmaline)
3. Winter pain relief specialist
4. Medical-grade compression

## Target Demographics
- Seniors 65+ (primary)
- Active adults 50-70 with arthritis
- Winter climate regions

## Pain Points Addressed
- Winter morning knee stiffness
- Arthritis flare-ups cold weather
- Chronic knee pain daily activities
- Reduced mobility winter months

## Proof Elements
- 4.8/5 stars
- 500+ reviews
- FDA registered
- Used by 2000+ seniors

## Discount Codes
- WARMKNEES20 (20% off)
- SENIOR20 (20% seniors)
- WINTER30 (bundle 30%)

## Ad Format Recommendations
1. UGC Testimonial (9:16) - Priority HIGH
2. Before/After (1:1) - Priority MEDIUM
3. Educational Demo (9:16) - Priority LOW
```

**Sauvegardez:** `video-ads-assets/products/{product-handle}/metadata/product-info.txt`

---

## WORKFLOW STANDARD 7 ÉTAPES

**Suivre cette séquence exacte pour chaque vidéo:**

### ⚙️ ÉTAPE 1: PRÉPARATION ASSETS (15-30 min)

**1.1 Sélectionner le produit**
- Consulter: `TOP_10_HERO_PRODUCTS_MAPPING.md`
- Choisir produit selon priorité (rank, seasonality, budget)

**1.2 Créer dossier produit**
```bash
mkdir -p video-ads-assets/products/{product-handle}/{hero-images,lifestyle-images,feature-closeups,metadata}
```

**1.3 Rassembler images**
- [ ] Min 1 hero image (fond blanc)
- [ ] Min 1 lifestyle image (contexte usage)
- [ ] Min 1 feature close-up (USP visuel)
- [ ] Créer `product-info.txt` (metadata)

**1.4 Vérifier qualité images**
- [ ] Résolution >1080px
- [ ] Format compatible (JPG, PNG)
- [ ] Lighting correct (pas trop sombre)
- [ ] Product clairement visible

**Outputs Étape 1:**
- ✅ Dossier produit avec 3-5 images
- ✅ Metadata file complété
- ✅ Shopify URL copied

---

### 📝 ÉTAPE 2: SÉLECTION TEMPLATE SCRIPT (10 min)

**2.1 Identifier type de vidéo optimal**

Consulter `product-info.txt` → "Ad Format Recommendations"

**5 Types de vidéos disponibles:**

| Type | Usage | Demographics | Durée | Format |
|------|-------|--------------|-------|--------|
| **UGC Testimonial** | Authenticité, social proof | Tous | 15 sec | 9:16 |
| **Before/After** | Transformation visuelle | Seniors, Office | 12 sec | 1:1 |
| **Product Demo** | Features techniques | Office, Athletes | 20 sec | 9:16 |
| **Comparison** | Vs competitors | Athletes, Tech-savvy | 25 sec | 9:16 |
| **Educational** | Authority building | Medical-aware | 30 sec | 9:16 |

**2.2 Sélectionner template**

Ouvrir: `video-ads-assets/templates/{type}-template.txt`

**2.3 Customiser script**

Remplacer variables:
- `{PRODUCT_NAME}` → Nom produit
- `{USP_1}`, `{USP_2}`, `{USP_3}` → Unique selling points
- `{PAIN_POINT}` → Pain point principal
- `{DEMOGRAPHICS}` → Persona cible
- `{DISCOUNT_CODE}` → Code promo

**Outputs Étape 2:**
- ✅ Script customisé 15-30 secondes
- ✅ Hook validé (3 premières secondes)
- ✅ CTA clair avec discount code

---

### 🎬 ÉTAPE 3: CONFIGURATION CREATIFY (15 min)

**3.1 Login Creatify Creator**
- Dashboard: https://app.creatify.ai
- Vérifier crédits disponibles (min 1)

**3.2 Choisir méthode création**

**Option A: URL-to-Video** (Recommandé si images Shopify bonnes)
```
Input: https://alphamedical.shop/products/{product-handle}
Avantage: Auto-scrape images + description
Temps: 5 min setup
```

**Option B: Custom Script** (Recommandé si contrôle total voulu)
```
Input: Script customisé Étape 2
Avantage: 100% contrôle créatif
Temps: 15 min setup
```

**3.3 Configuration vidéo**

**Settings obligatoires:**
```
Format: 9:16 vertical (ou 1:1 selon template)
Duration: {template_duration} secondes
Resolution: 1080x1920 (auto)
Captions: ENABLED ✅
Music: Enabled, -18dB volume
Language: English (ou French)
```

**Outputs Étape 3:**
- ✅ Creatify project créé
- ✅ Product URL ou script loaded
- ✅ Settings configurés

---

### 👤 ÉTAPE 4: SÉLECTION AVATAR & VOICE (10 min)

**4.1 Déterminer persona target**

Consulter `product-info.txt` → "Primary Demo"

**Persona → Avatar mapping:**

| Persona | Avatar Search Terms | Age | Gender | Style |
|---------|-------------------|-----|--------|-------|
| **Seniors 65+** | "mature woman outdoor", "senior active" | 60-70 | F/M | Casual warm |
| **Office 25-55** | "professional woman desk", "businessman casual" | 35-50 | F/M | Business casual |
| **Athletes 18-45** | "athletic woman gym", "runner outdoor" | 25-40 | F/M | Activewear |

**4.2 Filtrer avatars Creatify**

```
Filters:
- Age range: [according to persona]
- Gender: [according to demographics data]
- Setting: [indoor/outdoor according to script]
- Ethnicity: Diverse (or match primary audience)
```

**4.3 Tester 2-3 avatars en preview** (gratuit)
- Avatar 1: Premier choix
- Avatar 2: Backup si lip-sync pas naturel
- Avatar 3: Alternative style

**4.4 Sélection voice**

**Voice characteristics par persona:**

| Persona | Voice Type | Tone | Emotion |
|---------|-----------|------|---------|
| **Seniors** | Mature Female/Male | Warm, reassuring | Relief, grateful |
| **Office** | Natural conversational | Professional, friendly | Confident, relatable |
| **Athletes** | Energetic young | Dynamic, motivational | Excited, competitive |

**Settings voice:**
```
Language: English (US) ou French (Canadian)
Speed: Normal (1.0x)
Pitch: Normal
Emotion: [selon template]
```

**4.5 Preview combinaison Avatar + Voice**
- Écouter 5-10 secondes
- Vérifier lip-sync naturel
- Ajuster si robotique

**Outputs Étape 4:**
- ✅ Avatar sélectionné (ID saved for future)
- ✅ Voice sélectionnée (ID saved)
- ✅ Preview validé (pas robotique)

---

### 🎨 ÉTAPE 5: CUSTOMIZATION & BRANDING (10 min)

**5.1 Captions (Sous-titres) - MANDATORY**

```
Settings:
✅ Enable Captions: YES
Style: White text, black box background
Font: Sans-serif, bold weight
Size: Medium (readable mobile)
Position: Bottom-center (pas top, pas trop bas)
```

**5.2 Background Music**

```
Settings:
✅ Add Music: YES
Genre: [selon mood template]
  - UGC: Upbeat soft, friendly
  - Before/After: Inspirational calm
  - Demo: Corporate minimal
  - Comparison: Energetic modern
Volume: -18dB to -20dB (subtle, ne couvre PAS voix)
```

**5.3 Text Overlays**

**Overlay 1: USP Highlight** (mid-video 8-11 sec)
```
Text: "Self-Heating Technology ❄️→🔥"
Position: Top-center
Duration: 3 seconds
Font: Bold, large
Animation: Fade in/out
```

**Overlay 2: CTA Final** (12-15 sec)
```
Text: "alphamedical.shop | -20% CODE: {DISCOUNT_CODE}"
Position: Bottom (above captions)
Duration: 3 seconds
Font: Bold, high contrast
```

**5.4 Product Image Insertion** (si option disponible)

```
Timing: 4-7 sec (après hook, durant solution)
Image: video-ads-assets/products/{handle}/hero-images/front-view.jpg
Position: Center ou product-in-hand avatar
Duration: 3 seconds
```

**5.5 Brand Elements**

```
Logo: Alpha Medical logo PNG (if option available)
Position: Top-right corner (petit, discret)
Duration: Toute vidéo (watermark)
Colors: Brand colors si customizable
  - Primary: #[your-blue]
  - Accent: #[your-green]
```

**Outputs Étape 5:**
- ✅ Captions enabled + styled
- ✅ Music added, volume adjusted
- ✅ Text overlays créés (USP + CTA)
- ✅ Product image inserted (si applicable)
- ✅ Branding applied

---

### 👁️ ÉTAPE 6: PREVIEW & QA (15 min)

**6.1 Preview complet** (GRATUIT - illimité)

Cliquez "Preview" et regardez 2-3 fois la vidéo complète.

**6.2 Quality Checklist Étape par Étape**

**[0-3 sec] HOOK:**
- [ ] Accroche attention immédiatement
- [ ] Relatable pain point ou curiosity
- [ ] Avatar expression engageante
- [ ] Captions lisibles dès début

**[4-7 sec] PROBLEM → SOLUTION:**
- [ ] Transition naturelle
- [ ] Product introduction claire
- [ ] Product image visible (si inséré)
- [ ] USP mentionné

**[8-11 sec] DÉMONSTRATION:**
- [ ] Benefit clairement démontré
- [ ] Text overlay USP apparaît si applicable
- [ ] Avatar crédible (pas over-acting)
- [ ] Captions sync avec audio

**[12-15 sec] CTA:**
- [ ] Call-to-action clair ("Link in bio", "Try now")
- [ ] Discount code visible et lisible
- [ ] URL alphamedical.shop visible
- [ ] Ending pas abrupt (fade-out si option)

**6.3 Technical QA**

- [ ] **Durée exacte:** {template_duration} sec (±1 sec acceptable)
- [ ] **Format:** 9:16 ou 1:1 selon specs
- [ ] **Resolution:** 1080x1920 minimum
- [ ] **Lip-sync:** Naturel (pas décalage >0.5 sec)
- [ ] **Audio:** Voice claire, music pas trop forte
- [ ] **Captions:** 100% sync, pas fautes
- [ ] **Visual quality:** Pas pixelated, pas artifacts

**6.4 Brand QA**

- [ ] Tone of voice match brand (professional yet accessible)
- [ ] Medical claims compliant (pas "cure", "treat disease")
- [ ] Product name correct spelling
- [ ] Discount code correct
- [ ] No competitor mention

**6.5 Platform QA (Mobile)**

**Simuler viewing sur mobile:**
- [ ] Regarder preview sur téléphone (si possible)
- [ ] Captions lisibles petit écran
- [ ] Text overlays pas trop petits
- [ ] Hook impactful même sans son
- [ ] CTA visible même avec UI mobile

**6.6 Décision: Render ou Ajuster**

**SI tous ✅ → Passez Étape 7 (Render)**

**SI problèmes détectés:**

| Problème | Solution |
|----------|----------|
| Lip-sync décalé | Changer voice, re-preview |
| Avatar pas naturel | Changer avatar, re-preview |
| Hook pas fort | Modifier script 0-3 sec |
| Music trop forte | Réduire volume à -20dB |
| Captions fautes | Corriger script, re-preview |
| Durée trop longue | Couper script, re-preview |

**Re-preview après chaque ajustement** (gratuit)

**Outputs Étape 6:**
- ✅ Preview validé (tous checkboxes cochés)
- ✅ Aucun problème technique détecté
- ✅ Ready to render

---

### 🚀 ÉTAPE 7: RENDER & DELIVERY (5 min + wait 10-30 min)

**7.1 Final Check avant rendering**

**ATTENTION:** Rendering = 1 crédit consommé, pas de retour arrière!

**Dernière vérification:**
- [ ] Preview regardé minimum 2 fois
- [ ] Tous QA checkboxes ✅
- [ ] Crédits disponibles (min 1)
- [ ] Prêt à attendre 10-30 min rendering

**7.2 Lancer rendering**

```
Action: Click "Render Video" ou "Generate"
Crédit consommé: 1/50
Temps estimated: 10-30 minutes (selon queue)
Notification: Email quand prêt
```

**7.3 Pendant rendering (productive)**

**Option A: Préparer assets vidéo suivante**
- Étape 1 pour Video #2 (gather images)

**Option B: Commencer carousel ads**
- Setup PostNitro
- Design Carousel #1

**Option C: Setup Meta Ads Manager**
- Créer campaign structure
- Définir audiences
- Préparer ad copy

**7.4 Download & Quality Check Final**

**Quand email reçu "Video Ready":**

1. **Download MP4**
   - Résolution: 1080x1920 (ou 1080x1080 si 1:1)
   - Format: MP4 (H.264)
   - Size: Typiquement 5-20 MB

2. **Naming convention**
   ```
   Format: YYYY-MM-DD_{product-handle}_{type}_v{version}.mp4

   Exemples:
   2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
   2025-11-24_lower-back-brace_ba_v1.mp4
   2025-11-25_magnetic-posture_demo_v1.mp4
   ```

3. **Save to outputs folder**
   ```bash
   mv ~/Downloads/video.mp4 video-ads-assets/outputs/2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
   ```

4. **Final QA vidéo rendue**
   - [ ] Regarder complète 1 fois
   - [ ] Vérifier qualité (pas compression artifacts)
   - [ ] Tester sur mobile (transférer et regarder)
   - [ ] Vérifier captions sync final
   - [ ] File size <100 MB (Meta ads limit)

**7.5 Documentation & Logging**

**Créer production log entry:**

Fichier: `video-ads-assets/outputs/production-log.md`

```markdown
## Video Production Log

### 2025-11-23 | Tourmaline Knee Pads UGC v1

**Product:** Tourmaline Magnetic Knee Pads
**Type:** UGC Testimonial
**Duration:** 15 sec
**Format:** 9:16 vertical
**Target:** Seniors 65+, FB Reels + IG Reels

**Assets Used:**
- Hero image: tourmaline-knee-pads_hero_front.jpg
- Lifestyle: tourmaline-knee-pads_lifestyle_senior-outdoor.jpg

**Creatify Settings:**
- Avatar: ID #12345 (Mature woman outdoor)
- Voice: ID #67890 (Mature Female Warm EN-US)
- Music: Upbeat Soft, -18dB
- Captions: Enabled, white/black

**Script:** [UGC Testimonial Template]
Hook: "My knees used to ache every winter morning..."
CTA: "alphamedical.shop | -20% CODE: WARMKNEES20"

**Rendering:**
- Started: 2025-11-23 14:30
- Completed: 2025-11-23 14:45
- Render time: 15 minutes
- Credit used: 1/50

**Quality Check:**
✅ All QA passed
✅ Mobile tested
✅ Ready for Meta upload

**Next Steps:**
- [ ] Upload to Meta Ads Manager
- [ ] Create Ad Set (Budget $60, 7 days)
- [ ] Launch or wait for batch (Videos #2 + #3)

**Performance Tracking:**
- Campaign ID: [to be added]
- Ad Set ID: [to be added]
- Metrics tracking sheet: [link]
```

**7.6 Backup & Version Control**

```bash
# Backup vidéo finale
cp video-ads-assets/outputs/2025-11-23_tourmaline-knee-pads_ugc_v1.mp4 \
   video-ads-assets/outputs/backups/

# Si variations futures (v2, v3)
# Sauvegarder toujours v1 comme référence
```

**Outputs Étape 7:**
- ✅ Vidéo MP4 downloadée
- ✅ Nommée selon convention
- ✅ Sauvée dans `/outputs/`
- ✅ Production log complété
- ✅ QA final validé
- ✅ Ready for Meta Ads upload

---

## TEMPLATES PAR TYPE DE VIDÉO

### 📄 TEMPLATE 1: UGC Testimonial (15 sec)

**File:** `video-ads-assets/templates/ugc-testimonial-template.txt`

```
# UGC TESTIMONIAL TEMPLATE
# Duration: 15 seconds
# Format: 9:16 vertical
# Best for: All demographics, authenticity, social proof

[0-3 sec] HOOK - Personal struggle
{PAIN_POINT_STATEMENT}

Example:
"I couldn't run for 6 months because of knee pain..."
"My back used to hurt after 2 hours at my desk..."
"Arthritis made simple tasks impossible..."

[4-7 sec] PROBLEM → SOLUTION - Discovery moment
"...until I discovered {PRODUCT_NAME}."

Visual: Show product (avatar holding or close-up image)

[8-11 sec] DEMONSTRATION - Results/Benefits
"{BENEFIT_STATEMENT}. {USP_1}. {USP_2}."

Examples:
"Now I'm back to 5K runs. Zero pain."
"Self-heating technology. Works even in -10°C."
"All-day comfort. I barely notice I'm wearing it."

[12-15 sec] CTA - Call to action + offer
"Link in bio. You won't regret it."

Text overlay: "alphamedical.shop | -{DISCOUNT}% CODE: {CODE}"

---

CUSTOMIZATION VARIABLES:
- {PAIN_POINT_STATEMENT}: Relatable struggle opening
- {PRODUCT_NAME}: Full product name
- {BENEFIT_STATEMENT}: Primary benefit achieved
- {USP_1}, {USP_2}: Top 2 unique selling points
- {DISCOUNT}: Percentage (20, 25, 30)
- {CODE}: Discount code (WARMKNEES20, OFFICE25, etc.)

AVATAR SETTINGS:
- Age: Match target demographic
- Style: Casual, authentic (not too polished)
- Setting: Relevant to usage (outdoor, home, office)
- Expression: Relief, gratitude, authentic excitement

VOICE SETTINGS:
- Tone: Natural, conversational, genuine
- Emotion: Grateful, relieved, enthusiastic (not salesy)
- Speed: Normal (not rushed)

BEST FOR:
✅ Cold audiences (prospecting)
✅ Mobile-first platforms (TikTok, IG Reels)
✅ Lower-priced products ($30-80)
✅ Relatable pain points
```

**Sauvegardez ce template et créez les 4 autres types dans le même format:**
- `before-after-template.txt`
- `product-demo-template.txt`
- `comparison-template.txt`
- `educational-template.txt`

---

## NAMING CONVENTIONS

### 📛 Standard de Nommage Strict

**Pourquoi important:**
- Organisation scalable (100+ vidéos futures)
- Tracking performance facile
- Éviter confusions/overwrites
- Professionnalisme

---

### Files & Folders Naming

**Format général:**
```
{category}_{descriptor}_{variant}.{extension}
```

**Exemples:**

**Product Folders:**
```
✅ CORRECT: tourmaline-knee-pads/
✅ CORRECT: magnetic-posture-corrector/
❌ WRONG: Tourmaline Knee Pads/  (spaces, capitals)
❌ WRONG: knee_pads_tourmaline/  (inconsistent order)
```

**Image Files:**
```
✅ CORRECT: tourmaline-knee-pads_hero_front.jpg
✅ CORRECT: lower-back-brace_lifestyle_office-desk.jpg
✅ CORRECT: magnetic-posture_feature_magnetic-nodes.jpg

❌ WRONG: IMG_1234.jpg  (non-descriptive)
❌ WRONG: Knee Pad Front.jpg  (spaces, capitals)
```

**Video Output Files:**
```
Format: YYYY-MM-DD_{product-handle}_{type}_v{version}.mp4

✅ CORRECT: 2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
✅ CORRECT: 2025-11-24_lower-back-brace_ba_v2.mp4
✅ CORRECT: 2025-12-01_magnetic-posture_demo_v1.mp4

❌ WRONG: video1.mp4
❌ WRONG: Tourmaline_Knee_UGC.mp4  (no date, capitals)
❌ WRONG: 23-11-2025_knee.mp4  (date format wrong)
```

**Type Abbreviations:**
- `ugc` = UGC Testimonial
- `ba` = Before/After
- `demo` = Product Demo
- `comp` = Comparison
- `edu` = Educational

**Version Numbers:**
- `v1` = First version
- `v2` = Second iteration (different hook, avatar, etc.)
- `v3` = Third iteration
- `_final` = Approved final version for ads

---

### Metadata Files Naming

```
✅ product-info.txt  (standardized)
✅ shopify-url.txt
✅ production-notes.txt

❌ info.txt  (too generic)
❌ Product Information.txt  (spaces, capitals)
```

---

## QUALITY CHECKLIST

### ✅ Pre-Render Checklist (Étape 6)

**Copy-paste ce checklist pour chaque vidéo:**

```markdown
## Video QA Checklist: {Product Name} - {Type} - v{Version}

### Technical Specs
- [ ] Format: 9:16 vertical (ou 1:1 if before/after)
- [ ] Duration: {target} seconds (±1 sec OK)
- [ ] Resolution: 1080x1920 minimum
- [ ] File format: MP4
- [ ] Captions: Enabled + readable
- [ ] Audio: Voice clear, music -18dB

### Content Quality
- [ ] Hook (0-3s): Stops scroll immediately
- [ ] Problem (4-7s): Relatable pain point
- [ ] Solution (8-11s): Product benefit clear
- [ ] CTA (12-15s): Actionable + discount visible
- [ ] Script: No typos, natural flow
- [ ] Transitions: Smooth (not abrupt)

### Avatar & Voice
- [ ] Avatar: Matches target demographic
- [ ] Lip-sync: Natural (no delay >0.5s)
- [ ] Expression: Authentic (not over-acting)
- [ ] Voice: Tone appropriate for persona
- [ ] Emotion: Matches script mood

### Branding & Compliance
- [ ] Product name: Correct spelling
- [ ] Discount code: Correct + visible
- [ ] URL: alphamedical.shop visible
- [ ] No medical claims (cure, treat)
- [ ] Tone: Professional yet accessible
- [ ] Logo: Present if option available

### Mobile Optimization
- [ ] Captions readable on small screen
- [ ] Text overlays not too small
- [ ] Hook works WITHOUT sound
- [ ] CTA visible with mobile UI
- [ ] Vertical format optimized

### Platform-Specific
**Facebook/Instagram:**
- [ ] Square (1:1) if Feed, Vertical (9:16) if Reels
- [ ] First 3 sec hook extra strong (auto-play muted)
- [ ] Captions MANDATORY

**TikTok:**
- [ ] 9:16 vertical only
- [ ] Native UGC feel (not too polished)
- [ ] Trending music style (optional)

### Final Approval
- [ ] Preview watched 2+ times
- [ ] Tested on mobile if possible
- [ ] All checkboxes above ✅
- [ ] Ready to render (1 credit)

**Approved by:** [Your Name]
**Date:** [YYYY-MM-DD]
**Time:** [HH:MM]
```

---

## TROUBLESHOOTING

### 🔧 Problèmes Fréquents & Solutions

#### **Problème 1: Lip-sync décalé (voice pas sync avec bouche)**

**Symptômes:**
- Bouche bouge avant/après audio
- Délai >0.5 secondes visible

**Solutions:**
1. **Changer voice:**
   - Tester voice différente (même langue)
   - Voices "Natural" ou "Conversational" = meilleur sync
   - Éviter voices trop rapides ou lentes

2. **Ajuster script:**
   - Phrases plus courtes
   - Pauses naturelles (virgules, points)
   - Éviter tongue-twisters

3. **Changer avatar:**
   - Certains avatars = meilleur lip-sync tech
   - Tester 2-3 avatars différents

**Prevention:**
- Toujours preview 2-3 fois avant render
- Tester voice + avatar combo dès début

---

#### **Problème 2: Avatar looks "robotic" ou "uncanny valley"**

**Symptômes:**
- Mouvements pas naturels
- Expression faciale weird
- Yeux dead/lifeless

**Solutions:**
1. **Utiliser avatars "realistic" tier:**
   - Filter par "Most Realistic"
   - Éviter avatars "stylized" ou "cartoon"

2. **Changer background:**
   - Natural settings = plus believable
   - Studio blanc = peut accentuer uncanny

3. **Shorter duration:**
   - 15 sec max = moins temps pour notice
   - Couper parties où avatar idle (sans parler)

**Alternative:**
- Si critical: Utiliser B-roll footage à la place
- Product demos sans avatar (voiceover only)

---

#### **Problème 3: Music trop forte (couvre voix)**

**Symptômes:**
- Difficile entendre voix
- Captions nécessaires pour comprendre
- Music distracting

**Solutions:**
1. **Réduire volume music:**
   - From -18dB → -20dB ou -22dB
   - Test incremental 2dB à la fois

2. **Changer genre music:**
   - "Soft", "Ambient", "Minimal"
   - Éviter "Energetic" si voix importante

3. **Disable music option:**
   - Certaines vidéos = better sans music
   - Especially educational/demo formats

---

#### **Problème 4: Captions fautes d'orthographe**

**Symptômes:**
- Typos dans captions auto-générées
- Product name incorrect
- Discount code wrong

**Solutions:**
1. **Edit script before rendering:**
   - Copier script dans Word/Docs
   - Spell-check complet
   - Paste back into Creatify

2. **Manual caption edit:**
   - Si option disponible dans Creatify
   - Corriger directement captions

3. **Post-production edit:**
   - Dernière option: Edit vidéo avec tool externe
   - CapCut, InShot (mobile) pour fix captions

**Prevention:**
- Always spell-check script AVANT upload Creatify
- Vérifier product name spelling (Shopify exact)

---

#### **Problème 5: Rendering bloqué >30 min**

**Symptômes:**
- Status "Processing..." >30 minutes
- Pas d'email completion
- Dashboard stuck

**Solutions:**
1. **Wait patience:**
   - Peak hours = slower (weekdays 9am-5pm)
   - Off-peak = faster (nights, weekends)
   - Max wait: 60 minutes before action

2. **Check status:**
   - Refresh dashboard
   - Check email (spam folder)
   - Look for error messages

3. **Contact support:**
   - Email: [email protected]
   - Live chat si disponible
   - Provide: Job ID, timestamp, product URL

4. **Re-render si stuck >60 min:**
   - Cancel job (if option)
   - Start new render (additional credit)

**Prevention:**
- Render during off-peak hours
- Avoid complex videos (>30 sec) at first

---

#### **Problème 6: Downloaded video quality bad (pixelated)**

**Symptômes:**
- Vidéo floue/pixelated
- Compression artifacts visible
- Quality worse than preview

**Solutions:**
1. **Check download settings:**
   - Ensure "High Quality" ou "Original" selected
   - Not "Preview Quality"

2. **Re-download:**
   - Sometimes first download corrupted
   - Try again from dashboard

3. **Check source images:**
   - If product images low-res → output low-res
   - Use min 1080px images

4. **Contact support:**
   - Report quality issue
   - Request re-render at higher quality

**Prevention:**
- Always use high-res product images (>1080px)
- Download "Original Quality" option

---

#### **Problème 7: Video duration wrong (trop long/court)**

**Symptômes:**
- Vidéo 18 sec instead of 15 sec
- Vidéo 11 sec instead of 12 sec
- Script cut-off abruptly

**Solutions:**
1. **Adjust script length:**
   - Count words: ~3 words per second
   - 15 sec = ~45 words max
   - Remove filler words

2. **Voice speed adjustment:**
   - If too slow → speed 1.1x
   - If too fast → speed 0.9x

3. **Trim in post:**
   - Use CapCut to trim 1-2 sec
   - Keep hook + CTA intact

**Prevention:**
- Use templates (pre-timed scripts)
- Count script words before upload
- Preview shows exact duration

---

### 📞 Support Resources

**Creatify Support:**
- Email: [email protected]
- Response time: 24-48h
- Priority support: API plans

**Community:**
- Discord: [if available]
- Facebook Group: Creatify Users

**Internal Alpha Medical:**
- Marketing lead: [contact]
- This playbook: VIDEO_ADS_CREATION_PLAYBOOK.md
- Asset library: video-ads-assets/

---

## APPENDIX: Quick Reference Cards

### 🎴 Card 1: 15-Second UGC Script Formula

```
[0-3s] Pain Point Hook
[4-7s] "...until {PRODUCT}"
[8-11s] Benefit + USP
[12-15s] CTA + Discount
```

---

### 🎴 Card 2: Avatar Selection Cheat Sheet

| Demo | Age | Gender | Setting | Vibe |
|------|-----|--------|---------|------|
| Seniors | 60-70 | F/M | Home/Outdoor | Warm, grateful |
| Office | 35-50 | F/M | Desk/Indoor | Professional, relatable |
| Athletes | 25-40 | F/M | Gym/Outdoor | Energetic, confident |

---

### 🎴 Card 3: Pre-Render Checklist (Mini)

```
✅ Preview 2x
✅ Captions ON
✅ Music -18dB
✅ Duration exact
✅ Hook strong
✅ CTA visible
✅ Mobile-tested
```

---

### 🎴 Card 4: File Naming Formula

```
YYYY-MM-DD_{product-handle}_{type}_v{#}.mp4

Example:
2025-11-23_tourmaline-knee-pads_ugc_v1.mp4
```

---

## CHANGELOG

**v1.0 - 2025-11-23**
- Initial playbook creation
- 7-step workflow documented
- 5 video templates created
- Quality checklist finalized
- Troubleshooting guide added

**Future updates:**
- v1.1: Add A/B testing variations guide
- v1.2: Add Meta Ads upload integration
- v1.3: Add performance tracking templates

---

**END OF PLAYBOOK**

**Next Steps:**
1. ✅ Read entire playbook once
2. ✅ Setup video-ads-assets/ folder structure
3. ✅ Create first video following 7-step workflow
4. ✅ Document learnings in production log
5. ✅ Iterate and improve process

**Questions? Updates needed?**
This is a living document - update as you learn!

**Version:** 1.0
**Last Updated:** 2025-11-23
**Owner:** Alpha Medical Marketing Team
