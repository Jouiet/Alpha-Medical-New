# ÉTAPES MANUELLES À COMPLÉTER - ALPHA MEDICAL
**Date:** 2025-12-04
**Durée Totale:** 6h 55min (sur 11 jours disponibles)
**Stripe Disponible:** 2025-12-15 (dans 11 jours)

---

## 🎯 PRIORITÉ 1: LEGAL COMPLIANCE (1h 55min) - CRITIQUE

### ☐ TÂCHE #6: Terms Age Restriction (30 min)

**URL:** https://admin.shopify.com/store/azffej-as

**ÉTAPES:**
1. Login Shopify Admin
2. Cliquer: **Settings** (bas gauche)
3. Cliquer: **Legal**
4. Cliquer: **Terms of Service**
5. Scroll jusqu'à "Acceptance of Terms"
6. **APRÈS cette section**, ajouter:

```markdown
## Eligibility

You must be at least 18 years of age to use this website and purchase products. By using this site, you represent and warrant that you are at least 18 years old. If you are under 18, you may only use this site with the involvement of a parent or guardian.
```

7. Cliquer: **Save** (haut droite)
8. Attendre: "Changes saved"

**✅ VÉRIFICATION:**
- Ouvrir: https://www.alphamedical.shop/policies/terms-of-service
- Ctrl+F (Cmd+F): Chercher "18 years"
- ✅ Si visible → DONE
- ❌ Si absent → Répéter étapes

**Status:** ☐ TODO

---

### ☐ TÂCHE #1: Footer Policy Links (10 min)

**URL:** https://admin.shopify.com/store/azffej-as

**ÉTAPES:**
1. Login Shopify Admin
2. Cliquer: **Online Store** (menu gauche)
3. Cliquer: **Navigation**
4. Trouver: **"Footer menu"** dans la liste
5. Cliquer sur "Footer menu"

**Ajouter 5 menu items (dans cet ordre):**

**Item 1:**
- Cliquer: "Add menu item"
- Name: `Privacy Policy`
- Link: `/policies/privacy-policy`
- Cliquer: "Add"

**Item 2:**
- Cliquer: "Add menu item"
- Name: `Terms of Service`
- Link: `/policies/terms-of-service`
- Cliquer: "Add"

**Item 3:**
- Cliquer: "Add menu item"
- Name: `Refund Policy`
- Link: `/policies/refund-policy`
- Cliquer: "Add"

**Item 4:**
- Cliquer: "Add menu item"
- Name: `Shipping Policy`
- Link: `/pages/shipping-delivery`
- Cliquer: "Add"

**Item 5:**
- Cliquer: "Add menu item"
- Name: `Accessibility`
- Link: `/pages/accessibility`
- Cliquer: "Add"

6. Cliquer: **"Save menu"** (haut droite)

**✅ VÉRIFICATION:**
- Ouvrir: https://www.alphamedical.shop/
- Scroll vers le bas (footer)
- Vérifier: 5 liens visibles et cliquables
- Tester: Cliquer chaque lien → page s'ouvre

**Status:** ☐ TODO

---

### ☐ TÂCHE #2: Accessibility Statement Page (15 min)

**URL:** https://admin.shopify.com/store/azffej-as

**ÉTAPES:**
1. Login Shopify Admin
2. Cliquer: **Online Store** → **Pages**
3. Cliquer: **"Add page"** (haut droite)

4. **Title:**
```
Accessibility Statement
```

5. **Content:** (copier-coller intégralement)
```markdown
# Accessibility Statement

Alpha Medical Care is committed to ensuring digital accessibility for people with disabilities. We are continually improving the user experience for everyone and applying the relevant accessibility standards.

## Conformance Status
We are committed to WCAG 2.1 Level AA conformance.

## Features
- Keyboard navigation support
- Screen reader compatibility
- Alt text for all images
- Clear heading structure
- Sufficient color contrast

## Feedback
If you experience any difficulty accessing our site, please contact us:
- Email: accessibility@alphamedical.shop
- Phone: 1-888-XXX-XXXX (TBD)

Last updated: December 2025
```

6. **Expand:** "Search engine listing preview" (bas de page)
7. **Vérifier URL handle:** Devrait être `accessibility`
8. **Visibility:** Sélectionner "Visible"
9. Cliquer: **"Save"** (haut droite)

**✅ VÉRIFICATION:**
- Ouvrir: https://www.alphamedical.shop/pages/accessibility
- Vérifier page s'affiche correctement
- ✅ Si page loads → DONE

**Status:** ☐ TODO

---

### ☐ TÂCHE #3: Cookie Consent Banner - CookieYes (1h)

**RECOMMANDÉ:** Option CookieYes (gratuit, 1h vs 4h custom)

#### PARTIE A: Configuration CookieYes (30 min)

**ÉTAPE 1: Créer Compte**
1. Ouvrir: https://www.cookieyes.com/
2. Cliquer: "Get Started Free" ou "Sign Up"
3. Remplir:
   - Email: [votre email]
   - Password: [créer mot de passe]
   - Accepter Terms
4. Cliquer: "Create Account"
5. **Vérifier email:** Ouvrir email confirmation, cliquer lien

**ÉTAPE 2: Ajouter Website**
1. Dans Dashboard, cliquer: "Add Website"
2. Remplir:
   - Website URL: `https://www.alphamedical.shop`
   - Website Name: `Alpha Medical`
   - Language: `English`
   - Region: `United States`
3. Cliquer: "Add Website"

**ÉTAPE 3: Configurer Categories**

**Necessary (vérifier déjà configuré):**
- Shopify session cookies
- Cart cookies
- Security cookies

**Analytics (ajouter):**
- Cliquer: "Analytics" category
- Ajouter:
  - Google Analytics (GA4)
  - Google Tag Manager (GTM)
- Durée: 14-26 months
- Save

**Advertisement (ajouter):**
- Cliquer: "Advertisement" category
- Ajouter:
  - Meta Pixel (Facebook)
  - TikTok Pixel
  - Google Ads
- Durée: up to 24 months
- Save

**ÉTAPE 4: Customize Banner (OPTIONNEL)**
- Position: Bottom
- Colors: #4770db (bleu Alpha Medical)
- Buttons:
  - Accept: "Accept All"
  - Reject: "Reject All"
  - Settings: "Cookie Settings"
- Save Changes

**ÉTAPE 5: Copier Script**
1. Dans Dashboard: "Installation" ou "Get Code"
2. **COPIER ce script complet:**
```html
<script id="cookieyes" type="text/javascript" src="https://cdn-cookieyes.com/client_data/YOUR_UNIQUE_ID/script.js"></script>
```
3. **NOTER L'ID:** YOUR_UNIQUE_ID (exemple: abc123xyz)

#### PARTIE B: Installation Shopify (30 min)

**ÉTAPE 1: Accéder Code**
1. Shopify Admin: https://admin.shopify.com/store/azffej-as
2. **Online Store** → **Themes**
3. Cliquer: **"..."** (trois points) sur thème actif
4. Cliquer: **"Edit code"**

**ÉTAPE 2: Ouvrir theme.liquid**
1. Sidebar gauche: Expand **"Layout"**
2. Cliquer: **`theme.liquid`**
3. Fichier s'ouvre dans éditeur

**ÉTAPE 3: Trouver </head>**
1. Utiliser: Ctrl+F (Cmd+F sur Mac)
2. Chercher: `</head>`
3. Balise trouvée (ligne 100-200 environ)

**ÉTAPE 4: Insérer Script**
1. **JUSTE AVANT** la ligne `</head>`, ajouter:
```liquid
<!-- CookieYes GDPR Banner -->
<script id="cookieyes" type="text/javascript" src="https://cdn-cookieyes.com/client_data/YOUR_UNIQUE_ID/script.js"></script>
```

2. **REMPLACER:** `YOUR_UNIQUE_ID` par l'ID réel copié de CookieYes

**Exemple:**
```liquid
{{ content_for_header }}

<!-- CookieYes GDPR Banner -->
<script id="cookieyes" type="text/javascript" src="https://cdn-cookieyes.com/client_data/abc123xyz/script.js"></script>

</head>
```

3. Cliquer: **"Save"** (haut droite)
4. Attendre: "File saved"

**✅ VÉRIFICATION (5 TESTS OBLIGATOIRES):**

**TEST 1: Banner Appears**
- Mode Incognito: Ctrl+Shift+N (Chrome)
- Ouvrir: https://www.alphamedical.shop/
- ✅ Banner cookie visible avec boutons

**TEST 2: Accept Works**
- Cliquer: "Accept All"
- ✅ Banner disparaît
- ✅ Page normale

**TEST 3: Reject Works**
- Clear cookies: DevTools → Application → Cookies → Clear
- Reload page
- Cliquer: "Reject All"
- ✅ Banner disparaît

**TEST 4: Settings Works**
- Clear cookies, reload
- Cliquer: "Cookie Settings"
- ✅ Modal s'ouvre avec toggles
- ✅ On/off fonctionne

**TEST 5: Mobile Responsive**
- DevTools → Toggle device (Ctrl+Shift+M)
- iPhone mode
- ✅ Banner responsive

**Status:** ☐ TODO

---

## 🎯 PRIORITÉ 2: ANALYTICS VALIDATION (2h) - HIGH

### ☐ TÂCHE #17: Data Layer Validation (1h)

**Prérequis:** Chrome Browser + DevTools

#### TEST 1: Homepage (10 min)

**ÉTAPES:**
1. Ouvrir: https://www.alphamedical.shop/
2. **F12** (ou Cmd+Option+I sur Mac) → DevTools
3. Aller: **Console** tab
4. Taper: `dataLayer`
5. Press: **Enter**

**✅ VÉRIFICATION:**
```javascript
// ATTENDU: Array avec événements
▼ Array(19) [...]
  0: {gtm.start: ..., event: "gtm.js"}
  1: {event: "gtm.dom"}
  2: {event: "page_view", ...}
```

**Checklist:**
- ☐ dataLayer existe (pas "undefined")
- ☐ dataLayer est un Array
- ☐ dataLayer.length > 0
- ☐ Event "page_view" présent

6. **Screenshot:** DevTools Console → dataLayer
7. Sauvegarder: `homepage_datalayer.png`

**Status:** ☐ TODO

---

#### TEST 2: Product Page (15 min)

**ÉTAPES:**
1. Naviguer: Product page (ex: /products/knee-brace-support)
2. DevTools → Console
3. Taper: `dataLayer.filter(item => item.event === 'view_item')`
4. Press: Enter

**✅ VÉRIFICATION:**
```javascript
{
  event: "view_item",
  ecommerce: {
    currency: "USD",
    value: 29.99,  // Prix produit
    items: [{
      item_id: "...",
      item_name: "...",
      price: 29.99
    }]
  }
}
```

**Checklist:**
- ☐ Event "view_item" présent
- ☐ ecommerce object existe
- ☐ currency: "USD"
- ☐ value = prix produit
- ☐ items array présent

5. **Screenshot:** view_item event
6. Sauvegarder: `product_view_item.png`

**Status:** ☐ TODO

---

#### TEST 3: Add to Cart (15 min)

**ÉTAPES:**
1. Sur product page (rester sur même page)
2. DevTools → Console ouvert
3. **Cliquer:** "Add to Cart" button
4. Observer Console (nouveau event)

5. Taper: `dataLayer.filter(item => item.event === 'add_to_cart')`
6. Press: Enter

**✅ VÉRIFICATION:**
```javascript
{
  event: "add_to_cart",
  ecommerce: {
    currency: "USD",
    value: 29.99,
    items: [...]
  }
}
```

**Checklist:**
- ☐ Event "add_to_cart" présent
- ☐ Fired APRÈS click
- ☐ ecommerce.value correct
- ☐ items présent

7. **Screenshot:** add_to_cart event
8. Sauvegarder: `add_to_cart_event.png`

**Status:** ☐ TODO

---

#### TEST 4: Cart Page (10 min)

**ÉTAPES:**
1. Naviguer: /cart
2. DevTools → Console
3. Taper: `dataLayer`

**✅ VÉRIFICATION:**
- ☐ dataLayer existe
- ☐ page_view event pour /cart
- ☐ Pas d'erreurs JavaScript

**Status:** ☐ TODO

---

#### TEST 5: Collection Page (10 min)

**ÉTAPES:**
1. Naviguer: Collection (ex: /collections/pain-relief)
2. DevTools → Console
3. Taper: `dataLayer`

**✅ VÉRIFICATION:**
- ☐ dataLayer existe
- ☐ page_view pour collection
- ☐ dataLayer.length augmenté

**Status:** ☐ TODO

---

### ☐ GA4 Real-Time Verification (30 min)

**URL:** https://analytics.google.com/

**ÉTAPES:**

**TEST 1: Accès GA4**
1. Login Google Analytics
2. Sélectionner: Propriété "Alpha Medical" (GT-NC6L8G55)
3. Menu gauche: **Reports** → **Real-time**

**TEST 2: Page View**
1. Autre tab: Ouvrir https://www.alphamedical.shop/
2. Attendre: 5-10 secondes
3. GA4 Real-Time:
   - ✅ "Users in last 30 minutes" >= 1
   - ✅ Event "page_view" visible

**TEST 3: View Item**
1. Naviguer: Product page
2. Attendre: 10-15 secondes
3. GA4 Real-Time:
   - ✅ Event "view_item" visible

**TEST 4: Add to Cart**
1. Cliquer: "Add to Cart"
2. Attendre: 10-15 secondes
3. GA4 Real-Time:
   - ✅ Event "add_to_cart" visible

**TEST 5: Screenshot**
- GA4 Real-Time overview avec events
- Sauvegarder: `ga4_realtime_events.png`

**Status:** ☐ TODO

---

### ☐ Meta Pixel Verification (30 min)

**URL:** https://business.facebook.com/events_manager2/

**OPTION A: Events Manager (si accès)**

**ÉTAPES:**
1. Login Facebook Business
2. Events Manager
3. Sélectionner: Pixel "Alpha Medical"
4. Onglet: **"Test Events"**

**Tests:**
- Visit homepage → ✅ PageView visible
- Visit product → ✅ ViewContent visible
- Add to cart → ✅ AddToCart visible

**Screenshot:** Events Manager
**Sauvegarder:** `meta_pixel_events.png`

---

**OPTION B: DevTools Method (si pas accès Events Manager)**

**ÉTAPES:**
1. Homepage: https://www.alphamedical.shop/
2. **F12** → DevTools
3. Onglet: **Network**
4. Filter: Taper `tr?` dans search box

**Tests:**
- Reload homepage
- Visit product
- Add to cart

**✅ VÉRIFICATION:**
- ☐ Requêtes `facebook.com/tr?` présentes
- ☐ Paramètres: ev=PageView
- ☐ Paramètres: ev=ViewContent
- ☐ Paramètres: ev=AddToCart

**Screenshot:** DevTools Network
**Sauvegarder:** `meta_pixel_devtools.png`

**Status:** ☐ TODO

---

## 🎯 PRIORITÉ 3: EMAIL OPTIMIZATION (2h) - MEDIUM

### ☐ TÂCHE #8: Klaviyo A/B Test Config (1h)

**URL:** https://www.klaviyo.com/

**ÉTAPES:**
1. Login Klaviyo
2. Menu: **Flows**
3. Trouver: "Welcome Series - Final Email Discount"
4. Cliquer sur flow

5. **Sélectionner:** Email #1 (premier email du flow)
6. Cliquer: **"Create A/B Test"**

7. **Configure:**
   - **Variant A (Control):** Sujet actuel (laisser tel quel)
   - **Variant B:** Nouveau sujet:
     ```
     Your [Pain Point] Solution Awaits - 10% Off Inside
     ```
   - **Metric:** Open rate
   - **Split:** 50/50
   - **Duration:** 30 days
   - **Winner Selection:** Automatic

8. Cliquer: **"Save"** (NE PAS activer encore)

**✅ VÉRIFICATION:**
- ☐ Flow montre badge "A/B Test Configured"
- ☐ Test est SAVED mais pas ACTIVE
- ☐ Activation prévue POST-LAUNCH (besoin traffic)

**Note:** Activer après 500+ subscribers

**Status:** ☐ TODO

---

### ☐ TÂCHE #11: Klaviyo Segmentation (1h)

**URL:** https://www.klaviyo.com/

**Créer 4 segments:**

#### SEGMENT 1: VIP Customers

**ÉTAPES:**
1. Klaviyo → **Segments**
2. Cliquer: **"Create Segment"**
3. Name: `VIP Customers - 3+ Orders`
4. **Conditions:**
   - What someone has done: Placed Order
   - at least 3 times
   - in the last 365 days
5. Cliquer: **"Create Segment"**

**✅ VÉRIFICATION:**
- ☐ Segment créé
- ☐ Count: 0 members (normal PRE-LAUNCH)

---

#### SEGMENT 2: High-Value Customers

**ÉTAPES:**
1. Create Segment
2. Name: `High-Value - LTV $200+`
3. **Conditions:**
   - Metric: Historic CLV (Customer Lifetime Value)
   - is greater than: $200
4. Create Segment

---

#### SEGMENT 3: Inactive 60+ Days

**ÉTAPES:**
1. Create Segment
2. Name: `Inactive 60+ Days`
3. **Conditions:**
   - What someone has NOT done: Placed Order
   - in the last 60 days
   - AND
   - What someone HAS done: Placed Order
   - at least 1 time
   - all time
4. Create Segment

---

#### SEGMENT 4: Pain Point - Knee Pain

**ÉTAPES:**
1. Create Segment
2. Name: `Interest - Knee Pain Relief`
3. **Conditions:**
   - What someone has done: Viewed Product
   - where Product Name contains: "knee" OR "brace"
   - in the last 90 days
4. Create Segment

**✅ VÉRIFICATION FINALE:**
- ☐ 4 segments créés
- ☐ Tous montrent 0 members (normal PRE-LAUNCH)
- ☐ Rules valides

**Status:** ☐ TODO

---

## 🎯 PRIORITÉ 4: SHOPIFY FLOW FIX (10 min) - MEDIUM

### ☐ TÂCHE #14: Loyalty Tier Tag Removal (MANUEL)

**URL:** https://admin.shopify.com/store/azffej-as

**PROBLÈME:** Customers accumulent tags (bronze + silver + gold) au lieu de remplacer

**SOLUTION:** Ajouter "Remove tag" actions AVANT "Add tag"

**ÉTAPES:**

1. Shopify Admin → **Apps** → **Flow**
2. Trouver workflow: **"New Loyalty Tier Tagging (Automatic)"**
3. Cliquer pour ouvrir

4. **Pour chaque tier (Bronze, Silver, Gold):**

**Action existante:** "Add customer tag: bronze"
**Modifier pour:**
```
1. Remove customer tag: bronze
2. Remove customer tag: silver
3. Remove customer tag: gold
4. PUIS Add customer tag: bronze
```

**Instructions détaillées:**

**BRONZE TIER:**
1. Cliquer sur "+" AVANT action "Add tag: bronze"
2. Ajouter: "Remove customer tag"
3. Tag: `silver`
4. Ajouter encore: "Remove customer tag"
5. Tag: `gold`
6. Garder: "Add customer tag: bronze"

**SILVER TIER:**
1. Avant "Add tag: silver"
2. Remove: `bronze`
3. Remove: `gold`
4. Puis Add: `silver`

**GOLD TIER:**
1. Avant "Add tag: gold"
2. Remove: `bronze`
3. Remove: `silver`
4. Puis Add: `gold`

5. Cliquer: **"Save"**
6. Workflow reste ACTIVE

**✅ VÉRIFICATION:**
- ☐ 3 tiers modifiés (Bronze, Silver, Gold)
- ☐ Chaque tier: Remove old tags AVANT Add new tag
- ☐ Workflow status: ACTIVE

**TEST (si client test disponible):**
- Upgrade customer: Bronze → Silver
- ✅ Tag "bronze" removed
- ✅ Tag "silver" added
- ✅ Only 1 tag present

**Status:** ☐ TODO

**Note:** Guide complet disponible: `SHOPIFY_FLOW_LOYALTY_TIER_TAGGING_MANUAL_MODIFICATION.md`

---

## 📊 RÉCAPITULATIF DES TÂCHES

### PRIORITÉ 1: LEGAL (1h 55min) - CRITIQUE ⚠️

| # | Tâche | Durée | Status |
|---|-------|-------|--------|
| 6 | Terms Age Restriction | 30 min | ☐ TODO |
| 1 | Footer Policy Links | 10 min | ☐ TODO |
| 2 | Accessibility Statement | 15 min | ☐ TODO |
| 3 | Cookie Consent Banner | 1h | ☐ TODO |

**Output:** Legal compliance 100%, GDPR compliant

---

### PRIORITÉ 2: ANALYTICS (2h) - HIGH 📊

| # | Tâche | Durée | Status |
|---|-------|-------|--------|
| 17 | Data Layer Validation (5 tests) | 1h | ☐ TODO |
| - | GA4 Real-Time Verification | 30 min | ☐ TODO |
| - | Meta Pixel Verification | 30 min | ☐ TODO |

**Output:** Analytics foundation verified (83% - 17% pending Stripe)

---

### PRIORITÉ 3: EMAIL (2h) - MEDIUM 📧

| # | Tâche | Durée | Status |
|---|-------|-------|--------|
| 8 | Klaviyo A/B Test Config | 1h | ☐ TODO |
| 11 | Klaviyo Segmentation (4 segments) | 1h | ☐ TODO |

**Output:** Email optimization ready POST-LAUNCH

---

### PRIORITÉ 4: FLOW FIX (10 min) - MEDIUM ⚙️

| # | Tâche | Durée | Status |
|---|-------|-------|--------|
| 14 | Loyalty Tier Tag Removal | 10 min | ☐ TODO |

**Output:** Segmentation quality improved

---

## 🎯 PLANNING SUGGÉRÉ

### OPTION A: MINIMUM VIABLE (4h 55min)

**Exécuter:** Priorité 1 + 2 uniquement
- Legal compliance (1h 55min)
- Analytics validation (2h)
- GA4 + Meta Pixel (1h)

**Result:** Site légalement conforme + analytics opérationnel

---

### OPTION B: RECOMMANDÉ (6h 55min)

**Exécuter:** Priorité 1 + 2 + 3 (sans Priorité 4)
- Legal (1h 55min)
- Analytics (2h)
- Email optimization (2h)
- Flow fix (10 min)

**Result:** 88.6% workflows testable, prêt pour launch

---

### OPTION C: MAXIMUM (6h 55min)

**Exécuter:** TOUTES les priorités
- Legal (1h 55min)
- Analytics (2h)
- Email (2h)
- Flow (10 min)

**Result:** Optimization complète PRE-STRIPE

---

## 📈 SUCCESS METRICS

**Après Priorité 1 (Legal):**
- ✅ Terms: 18+ restriction
- ✅ Footer: 5 policy links
- ✅ Accessibility: Page published
- ✅ Cookie Consent: GDPR banner

**Après Priorité 2 (Analytics):**
- ✅ dataLayer: 5/6 pages verified
- ✅ GA4: 3/5 events (page_view, view_item, add_to_cart)
- ✅ Meta Pixel: 3/5 events

**Après Priorité 3 (Email):**
- ✅ A/B test: Configured
- ✅ Segments: 4 created

**Après Priorité 4 (Flow):**
- ✅ Loyalty tags: Fixed

---

## ⏳ TÂCHES POST-STRIPE (2025-12-15+)

**CANNOT COMPLETE NOW - Require payment gateway:**

1. ⏳ Enhanced Ecommerce full test (2h)
   - Test purchase avec carte 4242 4242 4242 4242
   - Verify: begin_checkout + purchase events

2. ⏳ Post-Purchase Email Testing (1h)
   - Thank You email
   - Review Request email
   - Cross-Sell email

3. ⏳ Checkout Flow (30 min)
   - End-to-end cart → payment → confirmation

**Testable après:** 2025-12-15 (11 jours)

---

## 📁 DOCUMENTATION DE RÉFÉRENCE

**Guide complet:** `/tmp/EXECUTION_MANUAL_JOURS_1-3.md` (888 lignes)

**Contient:**
- Instructions détaillées étape par étape
- Screenshots à capturer
- Vérifications obligatoires
- Troubleshooting
- Tests de validation

---

**PRÊT POUR EXÉCUTION**
**Durée:** 4h 55min (minimum) à 6h 55min (recommandé)
**Période:** 11 jours disponibles (2025-12-04 → 2025-12-15)
**Charge:** 25-38 min/jour moyenne
