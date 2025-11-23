# PRODUCTS ASSETS FOLDER
**Organisation des Assets par Produit**

## 📁 Structure

Chaque produit a son propre dossier avec 4 sous-dossiers:

```
{product-handle}/
├── hero-images/          # Images fond blanc, studio
├── lifestyle-images/     # Photos en contexte d'usage
├── feature-closeups/     # Close-ups fonctionnalités
└── metadata/            # Info produit + notes
```

---

## 📸 GUIDE: Quelles Images Mettre Où?

### 1. hero-images/ (Images Produit Principales)

**Usage:** Product showcase, CTA final frame, product-in-hand shots

**Caractéristiques:**
- Background: Blanc pur (RGB 255,255,255)
- Lighting: Studio, ombres minimales
- Product: Centré, occupe 70% du frame
- Angles: Front, 45°, side, packaging

**Sources:**
- Shopify product images (download via URL)
- Manufacturer images haute qualité
- Professional product photography

**Nommer comme:**
- `{product-handle}_hero_front.jpg`
- `{product-handle}_hero_angle45.jpg`
- `{product-handle}_hero_packaging.jpg`

**Specs minimum:**
- Format: JPG ou PNG
- Résolution: Min 1080px width
- Aspect ratio: 1:1 preferred, 4:5 acceptable
- File size: <5 MB

---

### 2. lifestyle-images/ (Photos Contexte Usage)

**Usage:** Démonstration, before/after, testimonial scenes, relatability

**Caractéristiques:**
- Background: Natural setting (home, office, outdoor, gym)
- Person: Visible, demographics match persona
- Product: Clairement visible being used
- Emotion: Positive, relief, satisfaction

**Sources:**
- Stock photos (Unsplash, Pexels) + product overlay
- Customer UGC photos (avec permission écrite)
- Professional lifestyle photoshoot

**Nommer comme:**
- `{product-handle}_lifestyle_senior-outdoor.jpg`
- `{product-handle}_lifestyle_office-desk.jpg`
- `{product-handle}_lifestyle_before-after.jpg`

**Specs minimum:**
- Format: JPG
- Résolution: 1080x1920 (9:16 vertical preferred)
- File size: <5 MB
- Person visible: Oui (sauf si product-only demo)

---

### 3. feature-closeups/ (Détails Fonctionnalités)

**Usage:** Highlight USPs, technical demos, differentiators

**Caractéristiques:**
- Focus: Une feature par image
- Lighting: Emphasize texture/details
- Context: Product detail visible
- Annotations: Optional text overlay points

**Exemples requis:**
- Magnetic therapy nodes
- Heated zones technology
- Adjustable straps mechanism
- Steel stays/support structure
- Fabric texture/breathability
- Anti-slip grip bands

**Nommer comme:**
- `{product-handle}_feature_magnetic-nodes.jpg`
- `{product-handle}_feature_heated-zone.jpg`
- `{product-handle}_feature_strap-adjust.jpg`

**Specs minimum:**
- Format: JPG
- Résolution: High-res (allow zoom)
- File size: <3 MB
- Lighting: Clear detail visibility

---

### 4. metadata/ (Information Produit)

**Usage:** Reference data pour scripts, tracking, documentation

**Files requis:**

#### `product-info.txt`
Template complet avec:
- Product name, handle, Shopify URL
- Hero score, rank, demographics
- USPs (3-5 points)
- Pain points addressed
- Proof elements (reviews, certifications)
- Discount codes disponibles

#### `shopify-url.txt`
URL directe Shopify du produit (1 ligne)

#### `production-notes.txt` (optionnel)
Notes spécifiques:
- Best-performing image variations
- A/B test learnings
- Avatar/voice combinations testées
- Performance data links

---

## 🎯 PRIORITY: TOP 3 Produits à Préparer D'ABORD

### 1. tourmaline-knee-pads/
**Rank #2 | Score: 0.923 | Winter Optimal**

**Images requises (min):**
- [ ] 1 hero: Front view fond blanc
- [ ] 1 lifestyle: Senior wearing outdoor winter
- [ ] 1 feature: Magnetic nodes close-up
- [ ] 1 feature: Self-heating zone
- [ ] metadata/product-info.txt complété

---

### 2. lower-back-brace/
**Rank #6 | Score: 0.870 | Office Workers**

**Images requises (min):**
- [ ] 1 hero: Front view fond blanc
- [ ] 1 lifestyle: Office worker at desk wearing
- [ ] 1 lifestyle: Before/after posture
- [ ] 1 feature: 6 steel stays detail
- [ ] metadata/product-info.txt complété

---

### 3. magnetic-posture-corrector/
**Rank #1 | Score: 0.934 | HIGHEST HERO**

**Images requises (min):**
- [ ] 1 hero: Front view fond blanc
- [ ] 1 lifestyle: Professional wearing under shirt
- [ ] 1 lifestyle: Comparison vs generic corrector
- [ ] 1 feature: Magnetic therapy nodes
- [ ] 1 feature: Shoulder straps adjustable
- [ ] metadata/product-info.txt complété

---

## 📥 COMMENT OBTENIR LES IMAGES

### Option 1: Download depuis Shopify (Fastest)

```bash
# URL format Shopify images:
https://cdn.shopify.com/s/files/1/[store-id]/products/{image-name}.jpg

# Ouvrir product page Shopify
# Right-click image → "Copy image address"
# Paste dans browser → Download
# Rename selon convention
```

### Option 2: Stock Photos + Product Overlay

**Sites recommandés (free):**
- Unsplash.com (high-quality, commercial use)
- Pexels.com (lifestyle photos)
- Pixabay.com (diverse options)

**Workflow:**
1. Search: "senior wearing knee brace" or "office worker back pain"
2. Download high-res (1080px+)
3. Overlay product image si nécessaire (Canva, Photoshop)
4. Save with naming convention

### Option 3: Customer UGC (Requires Permission)

**Process:**
1. Email customers avec photos/videos
2. Request permission écrite (email OK)
3. Offer incentive (discount code, feature in ad)
4. Download + rename

**Legal:** Toujours avoir permission écrite avant use commercial

---

## ✅ CHECKLIST: Dossier Produit Complet

Avant de marquer produit "ready for video creation":

- [ ] **hero-images/**: Min 1 image fond blanc (front view)
- [ ] **lifestyle-images/**: Min 1 image contexte usage
- [ ] **feature-closeups/**: Min 1 close-up USP
- [ ] **metadata/product-info.txt**: Complété avec toutes sections
- [ ] **metadata/shopify-url.txt**: URL direct copié
- [ ] **All images**: Named selon convention
- [ ] **All images**: Specs minimum respectées (>1080px)
- [ ] **All images**: File sizes <5 MB

**Quand tous ✅ → Produit READY pour Étape 1 du playbook!**

---

## 🔄 MAINTENANCE

**Ajouter nouveaux produits:**
```bash
cd video-ads-assets/products/
mkdir -p {new-product-handle}/{hero-images,lifestyle-images,feature-closeups,metadata}
```

**Update images:**
- Toujours garder version originale
- Nouvelles versions: append `_v2`, `_v3`
- Document changes dans metadata/production-notes.txt

**Archive old products:**
```bash
mv {product-handle}/ ../archived-products/
```

---

**Questions? Voir:** VIDEO_ADS_CREATION_PLAYBOOK.md
