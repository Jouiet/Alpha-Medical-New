# INSTRUCTIONS - AJOUT CTAs BUNDLES À LA HOMEPAGE

**Date**: 2025-11-15
**Action**: Ajouter 2 CTAs bundles à la homepage
**Durée**: 5 minutes
**Snippet**: `bundles-cta-banner.liquid` ✅ DÉJÀ UPLOADÉ

---

## RÉSUMÉ

Ajouter un banner avec 2 CTAs sur la homepage:
1. **CTA 1**: "Shop Bundles" → /pages/bundles (vente 15 bundles, 35% OFF)
2. **CTA 2**: "Build Your Bundle" → /pages/bundle-creator (proposals communautaires)

**Rappel**: Les bundles proposés par clients ne sont créés que si **10+ demandes identiques**

---

## MÉTHODE 1: VIA ADMIN UI (RECOMMANDÉE)

### Étapes:

1. **Connexion Admin Shopify**
   - URL: https://azffej-as.myshopify.com/admin
   - Section: Online Store → Themes → Customize

2. **Naviguer à la Homepage**
   - Cliquer sur "Home page" dans le dropdown en haut

3. **Ajouter Section Custom Liquid**
   - Trouver un emplacement (recommandé: après hero section)
   - Cliquer sur "Add section"
   - Chercher "Custom Liquid"
   - Cliquer sur la section pour l'ajouter

4. **Insérer le Code**
   ```liquid
   {% render 'bundles-cta-banner' %}
   ```

5. **Ajuster Position (Optionnel)**
   - Drag & drop pour déplacer la section
   - Recommandations:
     - **Position 1**: Juste après le hero/bannière principale
     - **Position 2**: Mi-page (entre collections)
     - **Position 3**: Avant footer

6. **Sauvegarder**
   - Cliquer sur "Save" en haut à droite

---

## MÉTHODE 2: VIA CODE (AVANCÉE)

Si vous préférez éditer directement le code du template homepage:

1. **Trouver le template homepage**
   - Admin → Online Store → Themes → Actions → Edit code
   - Chercher: `templates/index.json`

2. **Ajouter section dans le JSON**
   ```json
   {
     "sections": {
       "bundles_cta": {
         "type": "custom-liquid",
         "settings": {
           "custom_liquid": "{% render 'bundles-cta-banner' %}"
         }
       }
     },
     "order": [
       "image_banner",
       "bundles_cta",
       "featured_collection",
       ...
     ]
   }
   ```

3. **Sauvegarder**

---

## APERÇU DU BANNER

### Design:
- **Fond**: Gradient animé (bleu #4A90E2 → cyan #7FCCC9)
- **Layout**: 2 cartes côte à côte (responsive)
- **Animations**: Float icons, hover effects, pulse gradient
- **Stats**: 15 bundles | 35% savings | 8 personas | Free shipping

### CTA 1 (Shop Bundles):
- **Icône**: 🎁 (gift)
- **Badge**: "35% OFF ALL BUNDLES" (rouge/orange)
- **Description**: "Browse 15 expertly curated bundles..."
- **Bouton**: "Shop Now" → /pages/bundles

### CTA 2 (Build Your Bundle):
- **Icône**: 🛠️ (tools)
- **Badge**: "10+ VOTES = WE CREATE IT" (bleu/cyan)
- **Description**: "Can't find the perfect bundle? Create your own!..."
- **Bouton**: "Build Now" → /pages/bundle-creator

### Stats Footer:
- ✅ 15 Pre-Made Bundles
- 💰 35% Savings
- 🎯 8 Patient Personas
- 🚚 Free Shipping

---

## EMPLACEMENTS RECOMMANDÉS

### Option A: Après Hero Section (RECOMMANDÉ)
```
┌─────────────────────────┐
│   HERO BANNER           │ ← Section principale
├─────────────────────────┤
│   BUNDLES CTA BANNER    │ ← AJOUTER ICI ⭐
├─────────────────────────┤
│   Featured Collection   │
│   Product Grid          │
└─────────────────────────┘
```

**Avantages**:
- Haute visibilité (above the fold ou juste en dessous)
- Capture l'attention immédiatement
- Promotion agressive des bundles

### Option B: Mi-Page
```
┌─────────────────────────┐
│   Hero Section          │
│   Featured Collection   │
├─────────────────────────┤
│   BUNDLES CTA BANNER    │ ← AJOUTER ICI
├─────────────────────────┤
│   More Collections      │
│   Footer                │
└─────────────────────────┘
```

**Avantages**:
- Break visuel entre sections
- Engage les visiteurs qui scrollent
- Moins agressif que Option A

---

## VÉRIFICATION

Après ajout, vérifier:

1. **Homepage**:
   - Visiter: https://www.alphamedical.shop
   - Banner visible? ✅
   - Design responsive (mobile + desktop)? ✅

2. **CTA 1 - Shop Bundles**:
   - Cliquer "Shop Now"
   - Redirige vers: /pages/bundles ✅
   - Page affiche 15 bundles avec filtres ✅

3. **CTA 2 - Build Your Bundle**:
   - Cliquer "Build Now"
   - Redirige vers: /pages/bundle-creator ✅
   - Page affiche formulaire avec 2 méthodes (search + URL) ✅

4. **Responsive**:
   - Desktop: 2 cartes côte à côte ✅
   - Mobile: 2 cartes empilées ✅

5. **Animations**:
   - Icons flottent (float animation) ✅
   - Hover sur cartes: translateY + shadow ✅
   - Gradient pulse en arrière-plan ✅

---

## ANALYTICS (Recommandé)

Ajouter tracking GA4 pour mesurer performance:

**Événements à tracker**:
1. `bundles_cta_shop_click` → Click "Shop Now"
2. `bundles_cta_build_click` → Click "Build Now"
3. `bundles_cta_impression` → Banner viewed

**Méthode**: Ajouter data-attributes ou GTM events dans le snippet

---

## PERSONNALISATION (Optionnel)

Si vous voulez modifier le texte/design:

1. **Éditer le snippet**:
   - Admin → Online Store → Themes → Actions → Edit code
   - Chercher: `snippets/bundles-cta-banner.liquid`

2. **Textes modifiables**:
   - Titre principal: `<h2>Complete Care Bundles</h2>`
   - Sous-titre: `<p>Save more with curated...</p>`
   - CTA 1 titre: `<h3>Shop Bundles</h3>`
   - CTA 2 titre: `<h3>Build Your Bundle</h3>`
   - Badges: `35% OFF ALL BUNDLES` et `10+ VOTES = WE CREATE IT`

3. **Couleurs modifiables** (dans `<style>`):
   - Gradient background: `#4A90E2` → `#7FCCC9`
   - Badge discount: `#FF6B6B` → `#FF8E53`
   - Badge threshold: `#4A90E2` → `#7FCCC9`

---

## TROUBLESHOOTING

### Banner n'apparaît pas?
1. Vérifier que le snippet est uploadé: `snippets/bundles-cta-banner.liquid`
2. Vérifier le code Liquid: `{% render 'bundles-cta-banner' %}`
3. Clear cache navigateur + hard refresh (Cmd+Shift+R)
4. Vérifier theme customizer: section visible et activée?

### CTAs ne redirigent pas?
1. Vérifier URLs dans snippet:
   - `/pages/bundles` (sans https://domain.com)
   - `/pages/bundle-creator` (sans https://domain.com)
2. Vérifier que pages existent (voir verification script)

### Design cassé sur mobile?
1. Vérifier CSS responsive: `@media (min-width: 768px)`
2. Tester sur device réel ou Chrome DevTools mobile emulator

---

## SUPPORT

**Snippet uploadé**: ✅ `snippets/bundles-cta-banner.liquid`
**Status**: Prêt à être ajouté à la homepage
**Compatibilité**: Tous thèmes Shopify (custom liquid section)

---

**RAPPEL IMPORTANT**:

Les bundles proposés par clients via `/pages/bundle-creator` ne sont créés par l'équipe Alpha Medical que si **10+ demandes identiques** sont reçues.

Workflow:
1. Client soumet bundle proposal (3-4 produits)
2. Système agrège proposals identiques
3. Si 10+ demandes → Notification admin
4. Admin crée bundle manuellement dans Shopify
5. Tous les 10+ clients sont notifiés (email Klaviyo)
6. Bundle ajouté à la collection "Medical Equipment Bundles"

---

**FIN DES INSTRUCTIONS**
