# ALPHA MEDICAL - TODO MASTER LIST PRE-LAUNCH (23 JOURS)

**Date création:** 2025-11-22
**Date launch:** 2025-12-15
**Jours restants:** 23 jours
**Objectif:** Site e-commerce 100% prêt, lancement réussi, path vers $400K-$1M Year 1

---

## 📋 LÉGENDE PRIORITÉS

- 🔴 **CRITIQUE** = Blocage lancement si non fait
- 🟡 **IMPORTANT** = Impact majeur sur performance
- 🟢 **OPTIMIZATION** = Améliore résultats mais non-bloquant
- 🔵 **PREPARATION** = Anticipe besoins post-launch

---

## 🎯 VUE D'ENSEMBLE - ÉTAT ACTUEL

**Complété:** 80% (fondations techniques)
**Restant:** 20% (finitions critiques + optimizations)

**Temps total estimé restant:** ~8-10 heures sur 23 jours = **TRÈS FAISABLE**

---

## 📅 SEMAINE 1: FINITIONS CRITIQUES (22-29 NOV)

**Objectif:** Compléter TOUS les éléments blocants lancement
**Temps total:** ~2 heures
**Deadline:** 29 novembre 2025 (16 jours avant launch)

---

### JOUR 1 (AUJOURD'HUI - 22 NOV) - ACTIONS IMMÉDIATES

#### 🔴 TÂCHE 1: DÉSACTIVER PAYPAL

**Priorité:** CRITIQUE (blocage launch)
**Temps estimé:** 10 minutes
**Difficulté:** Facile
**Dépendances:** Aucune

**Contexte:**
- Requirement initial: "PAS de PayPal!!"
- Détection actuelle: Script détecte `ShopifyPaypalV4VisibilityTracking = true`
- Status: PROBABLEMENT ACTIF (à vérifier + désactiver)

**Actions détaillées:**
1. [ ] Ouvrir Shopify Admin: https://admin.shopify.com/store/azffej-as/settings/payments
2. [ ] Localiser section "Alternative payment methods" ou "PayPal"
3. [ ] Si PayPal ACTIF:
   - Cliquer bouton "Deactivate" ou "Remove"
   - Confirmer désactivation
   - Cliquer "Save" en haut à droite
4. [ ] Attendre 2-3 minutes (propagation)
5. [ ] Vérifier désactivation:
   ```bash
   cd /Users/mac/Desktop/Alpha-Medical
   python3 verify_paypal_status_forensic.py
   ```
6. [ ] Résultat attendu: "✅ PAYPAL NON DÉTECTÉ" (0 indicators)

**Critères de succès:**
- ✅ PayPal n'apparaît PAS dans Shopify Admin → Payments
- ✅ Script `verify_paypal_status_forensic.py` retourne 0 indicators
- ✅ Test checkout manuel: PayPal button NOT visible

**Fichier output:** Aucun (configuration Shopify)

**En cas de problème:**
- Si PayPal déjà désactivé → ✅ Marquer comme fait
- Si impossibilité technique → Documenter raison + escalade support Shopify
- Guidance: `PAYPAL_DEACTIVATION_GUIDE.md` (existe)

---

#### 🔴 TÂCHE 2: VÉRIFIER GTM VERSION 3 PUBLIÉE

**Priorité:** CRITIQUE (tracking conversions = ROI marketing)
**Temps estimé:** 15 minutes
**Difficulté:** Moyenne
**Dépendances:** Aucune

**Contexte:**
- GTM Version 3 créée: 21/11/2025 23:16
- Tags ajoutés: Google Tag (base) AW-17749024238 + Conversion Linker
- Problème détecté: Script live ne détecte PAS conversion tag sur site

**Actions détaillées:**
1. [ ] Ouvrir Google Tag Manager: https://tagmanager.google.com
2. [ ] Sélectionner container: GTM-WFPH2KZP (Alpha Medical Care)
3. [ ] Vérifier version publiée:
   - Admin → Versions
   - Version active: Doit être "v3.0 - Google Tag + Conversion Linker" ou plus récent
   - Date publication: 21/11/2025 ou après

4. [ ] SI VERSION 3 PAS PUBLIÉE:
   - Workspace → Submit (bouton bleu en haut à droite)
   - Version name: "v3.0 - Google Tag + Conversion Linker"
   - Description: Voir `GTM_ADD_MISSING_TAGS_STEPS.md` ligne 199-213
   - Cliquer "Publish"

5. [ ] Vérifier tags présents (Workspace → Tags):
   - [ ] ✅ "Google Tag - Base (AW-17749024238)" - Trigger: Initialization - All Pages
   - [ ] ✅ "Conversion Linker" - Trigger: All Pages
   - [ ] ✅ "Suivi des conversions Google Ads" - Trigger: Purchase Confirmation Page
     - Conversion ID: AW-17749024238
     - Conversion Label: gm87CKudp8QbEO67so9C

6. [ ] SI TAGS MANQUANTS:
   - Suivre guide complet: `GTM_ADD_MISSING_TAGS_STEPS.md`
   - Sections critiques: Étapes 1-2 (créer Google Tag + Conversion Linker)
   - Temps: +20-30 minutes si création nécessaire

7. [ ] Vérification site live (attendre 5 minutes après publication):
   ```bash
   cd /Users/mac/Desktop/Alpha-Medical
   python3 verify_google_tags_live.py
   ```

8. [ ] Résultat attendu:
   ```
   ✅ GTM DÉTECTÉ: GTM-WFPH2KZP
   ✅ GOOGLE TAG (BASE) DÉTECTÉ: AW-17749024238
   ✅ GT- TAG DÉTECTÉ: GT-NC6L8G55
   ✅ dataLayer DÉTECTÉ
   ✅ CONFIGURATION COMPLÈTE: OK
   ```

**Critères de succès:**
- ✅ GTM Version 3 (ou plus) publiée
- ✅ 3 tags présents dans GTM workspace
- ✅ Script `verify_google_tags_live.py` retourne "CONFIGURATION COMPLÈTE: OK"
- ✅ Preview Mode test: Tags fire sur homepage

**Fichiers à consulter si problème:**
- `GTM_ADD_MISSING_TAGS_STEPS.md` (guide complet 389 lignes)
- `GTM_SETUP_GUIDE.md` (backup guide)
- `GOOGLE_ADS_GTM_PROGRESS.md` (historique setup)

**En cas de problème:**
- Tags manquants → Créer manuellement (guide ligne par ligne dans `GTM_ADD_MISSING_TAGS_STEPS.md`)
- Version non publiée → Publier immédiatement
- Conversion tag ne fire pas → Vérifier trigger "Purchase Confirmation Page" URL = `/checkouts/.../thank_you`

---

### JOUR 2 (LUNDI 25 NOV) - EMAIL AUTOMATION

#### 🟡 TÂCHE 3: ACTIVER KLAVIYO WELCOME FLOW

**Priorité:** IMPORTANT (capture premiers subscribers)
**Temps estimé:** 5-10 minutes
**Difficulté:** Facile
**Dépendances:** Klaviyo installé ✅ (app ID: 123074)

**Contexte:**
- Flow documenté: `KLAVIYO_WELCOME_FLOW_IMPLEMENTATION.md` (11,889 bytes)
- Status: CRÉÉ mais NON ACTIVÉ
- Impact: Convertit 5-10% subscribers en premiers acheteurs

**Actions détaillées:**
1. [ ] Ouvrir Klaviyo: https://www.klaviyo.com/login
2. [ ] Navigation: Flows (menu gauche)
3. [ ] Localiser flow: "Welcome Series" ou similaire
   - Si N'EXISTE PAS → Créer en suivant `KLAVIYO_WELCOME_FLOW_IMPLEMENTATION.md`
   - Structure minimale:
     - Email 1: Immediately (Welcome + 10% discount code)
     - Email 2: Day 3 (Best-sellers showcase)
     - Email 3: Day 7 (Educational content + urgency)

4. [ ] Vérifier configuration:
   - Trigger: "Subscribed to List" (newsletter list)
   - Smart Sending: ON (évite spam)
   - From email: support@alphamedical.shop ou noreply@alphamedical.shop
   - From name: "Alpha Medical Team"

5. [ ] Vérifier contenu emails (minimum):
   - Email 1: Subject line engageant + CTA vers produits
   - Discount code: WELCOME10 (10% off) - Vérifier existe dans Shopify Discounts
   - Branding: Logo Alpha Medical + couleurs cohérentes

6. [ ] ACTIVER le flow:
   - Toggle switch en haut à droite: OFF → ON
   - Confirmer activation

7. [ ] Test (optionnel mais recommandé):
   - Aller sur site: https://www.alphamedical.shop
   - S'inscrire newsletter avec email test
   - Vérifier réception email Welcome dans 1-2 minutes

**Critères de succès:**
- ✅ Flow "Welcome Series" existe dans Klaviyo
- ✅ Status: LIVE (toggle ON)
- ✅ Au moins 1 email configuré (idéalement 2-3)
- ✅ Test subscription reçoit email immédiatement

**Fichier référence complet:** `KLAVIYO_WELCOME_FLOW_IMPLEMENTATION.md`

**En cas de problème:**
- Flow n'existe pas → Créer flow basique (1 email suffit pour lancement)
- Emails pas stylisés → Acceptable pour lancement, améliorer post-launch
- Test email non reçu → Vérifier spam folder, vérifier DNS/SPF records Shopify

---

#### 🟡 TÂCHE 4: ACTIVER KLAVIYO ABANDONED CART FLOW

**Priorité:** IMPORTANT (récupère 20-30% carts abandonnés)
**Temps estimé:** 5-10 minutes
**Difficulté:** Facile
**Dépendances:** Klaviyo installé ✅

**Contexte:**
- Flow documenté: `KLAVIYO_ABANDONED_CART_FLOW_IMPLEMENTATION.md` (17,646 bytes)
- Status: CRÉÉ mais NON ACTIVÉ
- Impact: Augmente revenus de 15-25% (industrie standard)

**Actions détaillées:**
1. [ ] Ouvrir Klaviyo: Flows
2. [ ] Localiser flow: "Abandoned Cart" ou "Checkout Started"
   - Si N'EXISTE PAS → Créer en suivant `KLAVIYO_ABANDONED_CART_FLOW_IMPLEMENTATION.md`
   - Structure minimale:
     - Email 1: 1 hour after abandon (reminder)
     - Email 2: 24 hours (urgency + social proof)
     - Email 3: 72 hours (last chance + small discount 5-10%)

3. [ ] Vérifier configuration:
   - Trigger: "Checkout Started" ET "Placed Order" = 0 times (filtre)
   - Time delays: 1h, 24h, 72h (personnalisable)
   - Smart Sending: ON

4. [ ] Vérifier contenu emails:
   - Dynamic cart items: {{ item.product.name }}, {{ item.product.images.0.src }}
   - CTA: "Complete Your Purchase" → Lien vers checkout saved
   - Email 3: Discount code CART10 (10% off) - Créer dans Shopify si n'existe pas

5. [ ] ACTIVER le flow:
   - Toggle: OFF → ON
   - Confirmer

6. [ ] Test (optionnel):
   - Aller sur site
   - Ajouter produit au panier
   - Démarrer checkout (entrer email)
   - ABANDONNER (fermer page)
   - Vérifier email reçu après 1 heure

**Critères de succès:**
- ✅ Flow "Abandoned Cart" existe et LIVE
- ✅ Au moins 2 emails configurés (idéalement 3)
- ✅ Trigger: Checkout Started (pas juste "Added to Cart")
- ✅ Dynamic product data affichée dans emails

**Fichier référence complet:** `KLAVIYO_ABANDONED_CART_FLOW_IMPLEMENTATION.md`

**En cas de problème:**
- Flow complexe → Créer version simplifiée (1-2 emails suffisent pour démarrer)
- Discount code manquant → Créer CART10 dans Shopify → Discounts (5 min)
- Dynamic data ne s'affiche pas → Templates Klaviyo pré-construits existent (drag & drop)

---

### JOUR 3 (MARDI 26 NOV) - LOYALTY PROGRAM

#### 🟡 TÂCHES 5-8: COMPLÉTER SHOPIFY FLOW LOYALTY PROGRAM

**Priorité:** IMPORTANT (retention +15-25%)
**Temps total estimé:** 10-15 minutes
**Difficulté:** Moyenne
**Dépendances:** Shopify Flow installé ✅, Platinum tier déjà configuré ✅

**Contexte:**
- Status actuel: 60% complété (seul Platinum tier configuré)
- Workflow URL: https://admin.shopify.com/store/azffej-as/apps/flow/editor/019aa2e4-81e1-798b-8beb-91d1e89d7238/01KAHE90EY2HNH84H6P67AM079
- Guide complet: `LOYALTY_AUTOMATION_PROGRESS_REPORT.md` (pages 56-128)
- Discount codes: DÉJÀ ACTIFS ✅ (LOYALTY10/15/25/50)

**Structure finale workflow:**
```
Order paid
│
└─► IF amountSpent >= 2500 (Platinum) ✅ FAIT
    ├─► Add tag: loyalty-platinum ✅
    └─► Remove tags: bronze, silver, gold ⏳ À FAIRE

    └─► ELSE: IF amountSpent >= 1000 (Gold) ⏳ À FAIRE
        ├─► Add tag: loyalty-gold
        └─► Remove tags: bronze, silver, platinum

        └─► ELSE: IF amountSpent >= 500 (Silver) ⏳ À FAIRE
            ├─► Add tag: loyalty-silver
            └─► Remove tags: bronze, gold, platinum

            └─► ELSE (Bronze - default) ⏳ À FAIRE
                ├─► Add tag: loyalty-bronze
                └─► Remove tags: silver, gold, platinum
```

---

#### 🟡 TÂCHE 5: AJOUTER ACTION "REMOVE TAGS" PLATINUM TIER

**Temps estimé:** 2 minutes

**Actions détaillées:**
1. [ ] Ouvrir workflow URL (ci-dessus)
2. [ ] Localiser branche TRUE de condition Platinum (>= $2500)
3. [ ] Action actuelle: "Add customer tags" → "loyalty-platinum" ✅
4. [ ] Cliquer sur "+" SOUS l'action "Add customer tags"
5. [ ] Rechercher: "Remove customer tags"
6. [ ] Sélectionner action "Remove customer tags"
7. [ ] Dans le champ tags à retirer, entrer: `loyalty-bronze, loyalty-silver, loyalty-gold`
   - Méthode: Taper chaque tag + Enter
   - Résultat: 3 tags séparés affichés
8. [ ] Cliquer "Done" ou "Save"

**Critère de succès:**
- ✅ Branche Platinum a 2 actions: "Add loyalty-platinum" + "Remove bronze/silver/gold"

---

#### 🟡 TÂCHE 6: CONFIGURER GOLD TIER ($1000-$2499)

**Temps estimé:** 4 minutes

**Actions détaillées:**
1. [ ] Localiser branche FALSE de condition Platinum
2. [ ] Cliquer sur "+" dans la branche FALSE
3. [ ] Sélectionner "Add condition"
4. [ ] Configurer condition:
   - Variable: `order.purchasingEntity.Customer.amountSpent.amount`
   - Comparison operator: "is greater than or equal to"
   - Value: `1000`
5. [ ] Cliquer "Done"

6. [ ] Dans branche TRUE de cette nouvelle condition (Gold):
   - Cliquer "+"
   - Add action: "Add customer tags"
   - Tag: `loyalty-gold`
   - Cliquer "Done"

7. [ ] Sous action "Add customer tags":
   - Cliquer "+"
   - Add action: "Remove customer tags"
   - Tags: `loyalty-bronze, loyalty-silver, loyalty-platinum`
   - Cliquer "Done"

**Critère de succès:**
- ✅ Condition Gold (>= $1000) créée
- ✅ Branche TRUE a 2 actions: Add gold + Remove bronze/silver/platinum

---

#### 🟡 TÂCHE 7: CONFIGURER SILVER TIER ($500-$999)

**Temps estimé:** 4 minutes

**Actions détaillées:**
1. [ ] Localiser branche FALSE de condition Gold
2. [ ] Cliquer "+"
3. [ ] Add condition:
   - Variable: `order.purchasingEntity.Customer.amountSpent.amount`
   - Operator: "is greater than or equal to"
   - Value: `500`
4. [ ] Done

5. [ ] Branche TRUE (Silver):
   - Add action: "Add customer tags" → `loyalty-silver`
   - Add action: "Remove customer tags" → `loyalty-bronze, loyalty-gold, loyalty-platinum`

**Critère de succès:**
- ✅ Condition Silver (>= $500) créée
- ✅ Actions configurées correctement

---

#### 🟡 TÂCHE 8: CONFIGURER BRONZE TIER (DEFAULT <$500)

**Temps estimé:** 2 minutes

**Actions détaillées:**
1. [ ] Localiser branche FALSE de condition Silver (= tous clients <$500)
2. [ ] Cliquer "+"
3. [ ] Add action: "Add customer tags" → `loyalty-bronze`
4. [ ] Cliquer "+"
5. [ ] Add action: "Remove customer tags" → `loyalty-silver, loyalty-gold, loyalty-platinum`

**Critère de succès:**
- ✅ Branche FALSE Silver (Bronze tier) a 2 actions

---

#### 🟡 TÂCHE 9: ACTIVER WORKFLOW LOYALTY

**Temps estimé:** 1 minute

**Actions détaillées:**
1. [ ] Vérifier structure complète (4 tiers configurés)
2. [ ] En haut à droite du workflow: Toggle "Turn on workflow"
3. [ ] Confirmer activation
4. [ ] Vérifier status: "Active" (badge vert)

**Critère de succès:**
- ✅ Workflow status: ACTIVE
- ✅ Structure complète visible dans éditeur

**Fichier référence:** `LOYALTY_AUTOMATION_PROGRESS_REPORT.md` (étapes détaillées avec screenshots)

---

### JOUR 4 (MERCREDI 27 NOV) - VÉRIFICATIONS

#### 🔴 TÂCHE 10: TEST CHECKOUT COMPLET (DESKTOP)

**Priorité:** CRITIQUE (validation fonctionnement end-to-end)
**Temps estimé:** 15 minutes
**Difficulté:** Facile
**Dépendances:** PayPal désactivé ✅, GTM configuré ✅

**Actions détaillées:**
1. [ ] Ouvrir site en navigation privée: https://www.alphamedical.shop
2. [ ] Sélectionner 1 produit bestseller (ex: Knee brace)
3. [ ] Cliquer "Add to Cart"
4. [ ] Vérifier cart drawer:
   - [ ] Produit affiché correctement (image, nom, prix)
   - [ ] Quantité modifiable
   - [ ] Subtotal correct
   - [ ] Free shipping bar visible (si applicable)

5. [ ] Cliquer "Checkout"
6. [ ] Page Shopify Checkout:
   - [ ] Entrer informations test:
     - Email: test+desktop@alphamedical.shop
     - Nom: Test Desktop
     - Adresse: Adresse US valide (ex: New York)
     - Phone: (555) 123-4567

7. [ ] Vérifier payment methods affichés:
   - [ ] ✅ Credit Card (Stripe)
   - [ ] ✅ Google Pay (si wallet configuré)
   - [ ] ✅ Apple Pay (si macOS/iOS)
   - [ ] ❌ PayPal (NE DOIT PAS apparaître)

8. [ ] Entrer credit card test (Shopify test mode):
   - Card: 1 (Bogus Gateway success card)
   - OU: 4242 4242 4242 4242 (si Stripe test mode)
   - Expiry: 12/30
   - CVV: 123

9. [ ] Cliquer "Complete Order"
10. [ ] Vérifier redirection vers Thank You page:
    - URL contient: `/checkouts/.../thank_you`
    - Order number affiché
    - Order confirmation visible

**Critères de succès:**
- ✅ Checkout complet sans erreurs
- ✅ PayPal NON visible dans payment methods
- ✅ Redirection Thank You page correcte
- ✅ Email confirmation reçu (vérifier inbox)

**Si erreurs:**
- Payment declined → Vérifier test mode activé dans Shopify Payments
- PayPal apparaît → Retourner Tâche 1 (désactivation incomplète)
- Thank You page 404 → Vérifier theme settings

---

#### 🔴 TÂCHE 11: TEST CHECKOUT MOBILE

**Priorité:** CRITIQUE (60-70% trafic e-commerce = mobile)
**Temps estimé:** 10 minutes
**Difficulté:** Facile

**Actions détaillées:**
1. [ ] Ouvrir site sur smartphone OU responsive mode desktop (F12 → Toggle device toolbar)
2. [ ] Device: iPhone 14 Pro ou Samsung Galaxy S23 (simuler)
3. [ ] Répéter workflow Tâche 10:
   - Add to cart
   - Checkout
   - Complete order (email test: test+mobile@alphamedical.shop)

4. [ ] Vérifications spécifiques mobile:
   - [ ] Sticky Add to Cart bar fonctionne (scroll down = bar apparaît)
   - [ ] Cart drawer swipe fonctionne
   - [ ] Checkout responsive (pas de scroll horizontal)
   - [ ] Payment buttons taille appropriée (touch-friendly)

**Critères de succès:**
- ✅ Checkout mobile fluide (aucun problème UX)
- ✅ Touch targets appropriés (>44px)
- ✅ Order complété sans friction

---

#### 🔴 TÂCHE 12: VÉRIFIER GTM TAGS FIRE SUR TEST ORDER

**Priorité:** CRITIQUE (validation tracking conversions)
**Temps estimé:** 10 minutes
**Difficulté:** Moyenne
**Dépendances:** Test checkout complété (Tâche 10 ou 11)

**Actions détaillées:**
1. [ ] Ouvrir GTM Preview Mode:
   - https://tagmanager.google.com
   - Container: GTM-WFPH2KZP
   - Cliquer "Preview" (en haut à droite)
   - Entrer URL: https://www.alphamedical.shop
   - Cliquer "Connect"

2. [ ] Nouvelle fenêtre s'ouvre avec Tag Assistant connecté
3. [ ] Vérifier homepage:
   - [ ] Tag Assistant affiche "Connected"
   - [ ] Tags Fired section montre:
     - ✅ Google Tag - Base (AW-17749024238)
     - ✅ Conversion Linker
   - [ ] Conversion Tracking: NOT fired (normal, seulement sur /thank_you)

4. [ ] Refaire test checkout (Tâche 10):
   - Add to cart → Checkout → Complete order
   - Email test: test+gtm@alphamedical.shop

5. [ ] Sur Thank You page, vérifier Tag Assistant:
   - [ ] ✅ Google Tag - Base: Fired
   - [ ] ✅ Conversion Linker: Fired
   - [ ] ✅ **Suivi des conversions Google Ads: Fired** ← CRITIQUE

6. [ ] Cliquer sur tag "Suivi des conversions Google Ads":
   - Variables visible: transaction_id, value, currency
   - transaction_id = Order number Shopify
   - value = Order total
   - currency = USD

**Critères de succès:**
- ✅ 3 tags fire sur Thank You page
- ✅ Conversion tag contient dynamic order data
- ✅ Aucune erreur dans Tag Assistant

**Si conversion tag ne fire PAS:**
- Vérifier trigger: URL contains `/thank_you`
- Vérifier GTM Version 3 publiée (Tâche 2)
- Consulter: `GTM_ADD_MISSING_TAGS_STEPS.md`

---

#### 🟡 TÂCHE 13: VÉRIFIER EMAIL FLOWS TRIGGERED

**Priorité:** IMPORTANT (validation automation)
**Temps estimé:** 5 minutes
**Difficulté:** Facile
**Dépendances:** Klaviyo flows activés (Tâches 3-4), Test checkout complété

**Actions détaillées:**
1. [ ] Vérifier inbox des emails test utilisés:
   - test+desktop@alphamedical.shop
   - test+mobile@alphamedical.shop
   - test+gtm@alphamedical.shop

2. [ ] Emails attendus (sous 5 minutes):
   - [ ] ✅ Shopify Order Confirmation (automatique)
   - [ ] ✅ Welcome Email (si email jamais vu avant sur Klaviyo)

3. [ ] Test Abandoned Cart (optionnel):
   - Nouveau checkout avec email: test+abandon@alphamedical.shop
   - Remplir shipping info
   - ABANDONNER (fermer page)
   - Attendre 1 heure
   - Vérifier email "You forgot something..." reçu

**Critères de succès:**
- ✅ Order confirmation reçue pour chaque test order
- ✅ Welcome email reçu (si nouveau subscriber)
- ✅ (Optionnel) Abandoned cart email après 1h

**Si emails non reçus:**
- Vérifier spam folder
- Vérifier Klaviyo → Flows → Status = LIVE
- Vérifier Klaviyo → Analytics → Flow Performance (emails sent?)

---

## 📅 SEMAINE 2: OPTIMIZATIONS (30 NOV - 6 DEC)

**Objectif:** Ajouter éléments qui améliorent performance (non-bloquants)
**Temps total:** ~4-5 heures
**Deadline:** 6 décembre 2025 (9 jours avant launch)

---

### 🟢 TÂCHE 14: INSTALLER FACEBOOK PIXEL

**Priorité:** OPTIMIZATION (requis pour Facebook Ads future)
**Temps estimé:** 15-20 minutes
**Difficulté:** Moyenne
**Deadline:** Avant lancement Facebook Ads (Week 2-3 post-launch)

**Actions détaillées:**

**MÉTHODE 1: Via GTM (Recommandé)**

1. [ ] Créer Facebook Pixel:
   - Aller sur https://business.facebook.com/events_manager
   - Data Sources → Add → Web → Facebook Pixel
   - Nom: "Alpha Medical Pixel"
   - Copier Pixel ID (format: 123456789012345)

2. [ ] Installer dans GTM:
   - GTM → Tags → New
   - Tag type: "Custom HTML"
   - Nom: "Facebook Pixel - Base Code"
   - HTML: Coller code Facebook Pixel (fourni par Facebook)
   - Trigger: "All Pages"
   - Save

3. [ ] Ajouter événements:
   - Tag "Facebook Pixel - Purchase":
     - Custom HTML: Événement Purchase
     - Trigger: "Purchase Confirmation Page" (same as Google Ads)
   - Tag "Facebook Pixel - Add to Cart":
     - Custom HTML: Événement AddToCart
     - Trigger: "Add to Cart" (à créer)

4. [ ] Publier GTM Version 4:
   - Submit → Version name: "v4.0 - Facebook Pixel"
   - Publish

**MÉTHODE 2: Via Shopify App (Plus facile, moins flexible)**

1. [ ] Shopify Admin → Apps → Search "Facebook & Instagram"
2. [ ] Installer app officielle Facebook & Instagram
3. [ ] Connecter compte Facebook Business
4. [ ] Accepter permissions
5. [ ] Pixel installé automatiquement

**Vérification:**
1. [ ] Facebook Events Manager → Test Events
2. [ ] Aller sur site: https://www.alphamedical.shop
3. [ ] Vérifier événement "PageView" apparaît en temps réel
4. [ ] Test checkout → Vérifier événement "Purchase" apparaît

**Critères de succès:**
- ✅ Pixel ID configuré
- ✅ PageView events détectés
- ✅ Purchase event fire sur Thank You page

**Fichiers à créer si problème:**
- Documentation personnalisée pour setup si blocage

---

### 🟢 TÂCHE 15: CRÉER 3-5 BUNDLES PRIORITAIRES

**Priorité:** OPTIMIZATION (AOV +20-35%)
**Temps estimé:** 45-60 minutes
**Difficulté:** Moyenne
**Deadline:** Semaine 1 post-launch acceptable

**Contexte:**
- Bundles documentés: `ALPHA_MEDICAL_8_BUNDLES_FINAL.md` (83,704 bytes)
- 8 bundles détaillés avec produits, pricing, descriptions
- App requise: Bundler (déjà installé ✅)

**Actions détaillées:**

1. [ ] Ouvrir Bundler app: Shopify Admin → Apps → Bundler
2. [ ] Sélectionner 3-5 bundles prioritaires (référence document):

**BUNDLE 1: "Complete Knee Recovery Kit" (Priorité #1)**
- Produits (référence `ALPHA_MEDICAL_8_BUNDLES_FINAL.md` lignes 45-65):
  - Adjustable Hinged Knee Brace Support ($89.67)
  - Compression Leg Massager ($145.56)
  - Hot & Cold Therapy Wrap ($42.18)
- Prix bundle: $277.41 (prix normal) → **$249.67** (10% discount)
- Savings: $27.74

**BUNDLE 2: "Back Pain Relief Essentials"**
- (Voir document lignes 120-140 pour produits exacts)

**BUNDLE 3: "Athletic Recovery Pro Pack"**
- (Voir document lignes 200-220)

3. [ ] Pour CHAQUE bundle:
   - [ ] Bundler → Create Bundle
   - [ ] Nom: [Nom du bundle]
   - [ ] Type: "Fixed Bundle" (produits fixes, non customizable)
   - [ ] Ajouter produits (search par nom)
   - [ ] Prix: Calculé automatiquement OU override avec prix discount
   - [ ] Description: Copier depuis document markdown
   - [ ] Image: Upload image bundle (si existe) OU utiliser image premier produit
   - [ ] Collections: Assigner à "Bundle Deals"
   - [ ] Save

4. [ ] Publier bundles:
   - [ ] Status: Active
   - [ ] Online Store: Visible

**Critères de succès:**
- ✅ 3-5 bundles créés dans Bundler app
- ✅ Bundles visibles sur collection: https://www.alphamedical.shop/collections/bundle-deals
- ✅ Prix discount appliqué (5-15% savings)
- ✅ Add to cart fonctionne

**Si complexité trop élevée:**
- Créer 1-2 bundles simples pour lancement
- Ajouter bundles restants post-launch (semaines 2-4)

**Fichier référence:** `ALPHA_MEDICAL_8_BUNDLES_FINAL.md` (détails complets 8 bundles)

---

### 🔵 TÂCHE 16: CRÉER GOOGLE ADS CAMPAIGN (DRAFT)

**Priorité:** PREPARATION (prêt pour launch day)
**Temps estimé:** 45-60 minutes
**Difficulté:** Moyenne
**Deadline:** 13 décembre 2025 (2 jours avant launch)

**Contexte:**
- Google Ads account: 128-734-6786
- Conversion tracking: Configuré ✅ (Tâche 2)
- Budget initial: $30/jour ($900/mois)

**Actions détaillées:**

1. [ ] Ouvrir Google Ads: https://ads.google.com
2. [ ] Account: 128-734-6786
3. [ ] Campaigns → New Campaign

**CAMPAIGN 1: Search - Brand Protection**

4. [ ] Campaign type: "Search"
5. [ ] Goal: "Sales" → "Website sales"
6. [ ] Campaign name: "Search - Brand - Alpha Medical"
7. [ ] Bidding: "Maximize conversions" (début) OU "Target CPA" ($35)
8. [ ] Budget: $10/jour
9. [ ] Networks: Search only (décocher Display Network)
10. [ ] Locations: United States (ou cibler états spécifiques)
11. [ ] Languages: English

12. [ ] Ad Group 1: "Brand Keywords"
    - Keywords:
      - [alpha medical]
      - [alpha medical care]
      - [alphamedical.shop]
      - "alpha medical" (phrase match)
    - Match types: Exact + Phrase

13. [ ] Ads (3 variations):
    - **Ad 1:**
      - Headline 1: "Alpha Medical - Official Site"
      - Headline 2: "Medical-Grade Recovery Equipment"
      - Headline 3: "Free Shipping on Orders $50+"
      - Description 1: "Shop knee braces, back supports & therapy devices. Medical-grade quality at affordable prices."
      - Description 2: "30-day money-back guarantee. Fast US shipping."
      - Final URL: https://www.alphamedical.shop

    - **Ad 2-3:** Variations avec USPs différentes

14. [ ] Sitelink Extensions:
    - Pain Relief Products → /collections/pain-relief-recovery
    - Back Supports → /collections/posture-support
    - Free Shipping → /pages/shipping
    - Contact Us → /pages/contact

15. [ ] **NE PAS ACTIVER** - Sauvegarder en DRAFT

**CAMPAIGN 2: Search - Product Categories**

16. [ ] Nouvelle campaign: "Search - Products - Knee Braces"
17. [ ] Budget: $20/jour
18. [ ] Ad Group: "Knee Braces"
    - Keywords (5-10):
      - knee brace
      - knee support
      - hinged knee brace
      - knee brace for pain
      - best knee brace
      - knee brace for running
      - adjustable knee brace
    - Match types: Phrase + Broad match modifier

19. [ ] Ads (focus bénéfices):
    - Headline: "Adjustable Knee Brace - $XX"
    - Description: Pain relief + support + free shipping
    - Final URL: /collections/joint-support (ou produit spécifique)

20. [ ] **NE PAS ACTIVER** - DRAFT

**Critères de succès:**
- ✅ 2 campaigns créées en DRAFT
- ✅ Keywords recherchés et validés (search volume >100/mois)
- ✅ Ads rédigées avec USPs claires
- ✅ Conversion tracking linked
- ✅ DRAFT (NOT LIVE) - Activation Jour Launch

**Fichiers référence:**
- `GOOGLE_ADS_SETUP_GUIDE.md`
- `GOOGLE_ADS_NEXT_STEPS.md`

---

### 🔵 TÂCHE 17: PRÉPARER CONTENU SOCIAL MEDIA

**Priorité:** PREPARATION (annonce lancement)
**Temps estimé:** 60-90 minutes
**Difficulté:** Facile
**Deadline:** 14 décembre 2025 (1 jour avant launch)

**Actions détaillées:**

1. [ ] Créer 5 posts pour lancement (Instagram + Facebook):

**POST 1: Annonce Lancement (Jour J - 15 Dec)**
- Visual: Image hero produit (knee brace ou bestseller)
- Copy:
  ```
  🚀 WE'RE LIVE! Alpha Medical is officially open.

  Your trusted source for medical-grade recovery equipment at prices that make sense.

  ✅ Free shipping on orders $50+
  ✅ 30-day money-back guarantee
  ✅ Fast US delivery

  Shop now: alphamedical.shop

  #AlphaMedical #PainRelief #RecoveryEquipment #Launch
  ```

**POST 2: Problem-Solution (Jour J+1)**
- Visual: Before/After ou infographic
- Copy: Highlight pain point (knee pain, back pain) → Solution (product)

**POST 3: Product Showcase (Jour J+3)**
- Visual: Carousel 3-5 bestsellers
- Copy: "Our top 5 bestsellers" + prices + benefits

**POST 4: Educational (Jour J+5)**
- Visual: Tips récupération ou exercices
- Copy: "5 ways to speed up recovery" + CTA vers blog

**POST 5: Social Proof (Jour J+7)**
- Visual: Testimonial (si existe) OU stock photo client
- Copy: Trust-building message

2. [ ] Créer visuels (si pas de designer):
   - Canva templates: "Product Launch" / "E-commerce"
   - Utiliser images produits Shopify (download high-res)
   - Dimensions: 1080x1080 (Instagram square) + 1080x1350 (portrait)

3. [ ] Scheduler posts (optionnel):
   - Meta Business Suite: https://business.facebook.com
   - Scheduler les 5 posts sur 7 jours

**Critères de succès:**
- ✅ 5 posts créés (copy + visuals)
- ✅ Saved en draft (pas publiés avant launch)
- ✅ Hashtags recherchés (#PainRelief, #KneeBrace, etc.)

---

## 📅 SEMAINE 3: FINAL PREP (7-13 DEC)

**Objectif:** Validation finale, backup, GO/NO-GO decision
**Temps total:** ~3 heures
**Deadline:** 13 décembre 2025 (2 jours avant launch)

---

### 🔵 TÂCHE 18: VÉRIFIER STOCK DSERS TOP 20 PRODUITS

**Priorité:** PREPARATION (éviter stock-outs Day 1)
**Temps estimé:** 30 minutes
**Difficulté:** Facile
**Deadline:** 9 décembre 2025

**Actions détaillées:**

1. [ ] Ouvrir DSers app: Shopify Admin → Apps → DSers
2. [ ] Identifier top 20 produits (référence: Bestsellers collection)
3. [ ] Pour CHAQUE produit:
   - [ ] Vérifier supplier stock: >50 units disponibles
   - [ ] Vérifier shipping time: 7-15 jours acceptable
   - [ ] Vérifier supplier rating: >95% positive
   - [ ] Vérifier supplier orders: >1000 orders (reliable)

4. [ ] SI stock <20 units:
   - [ ] Identifier backup supplier (AliExpress search)
   - [ ] Ajouter backup supplier dans DSers
   - [ ] Documenter: Fichier "BACKUP_SUPPLIERS.md"

5. [ ] Test order 1-2 produits (optionnel mais recommandé):
   - Commander échantillon pour QC personnel
   - Vérifier qualité produit
   - Mesurer shipping time réel
   - Documenter: Photos + notes

**Critères de succès:**
- ✅ Top 20 produits: Stock >50 units
- ✅ Backup suppliers identifiés pour produits critiques
- ✅ (Optionnel) 1-2 échantillons commandés

---

### 🔵 TÂCHE 19: BACKUP COMPLET STORE

**Priorité:** PREPARATION (sécurité)
**Temps estimé:** 20 minutes
**Difficulté:** Facile
**Deadline:** 10 décembre 2025

**Actions détaillées:**

1. [ ] Backup Theme:
   - Shopify Admin → Online Store → Themes
   - Theme actuel → Actions → Download theme file
   - Sauvegarder: `alpha-medical-theme-backup-2025-12-10.zip`

2. [ ] Export Products:
   - Shopify Admin → Products
   - Export → CSV file
   - Sauvegarder: `alpha-medical-products-2025-12-10.csv`

3. [ ] Export Customers (si applicable):
   - Customers → Export
   - Sauvegarder: `alpha-medical-customers-2025-12-10.csv`

4. [ ] Screenshot Configs:
   - GTM container: Screenshot tags list
   - Klaviyo flows: Screenshot flow structures
   - Shopify Payments: Screenshot active methods
   - Shopify Flow: Screenshot loyalty workflow
   - Apps installed: Screenshot apps list

5. [ ] Sauvegarder scripts Python:
   - Copier dossier `/Users/mac/Desktop/Alpha-Medical/`
   - Vers backup externe ou cloud (Google Drive, Dropbox)

**Critères de succès:**
- ✅ Theme backup downloaded
- ✅ Products CSV exported
- ✅ Screenshots configs sauvegardés
- ✅ Scripts Python backed up

---

### 🔴 TÂCHE 20: GO/NO-GO DECISION FINALE

**Priorité:** CRITIQUE (décision lancement)
**Temps estimé:** 60 minutes (review complet)
**Difficulté:** Facile
**Deadline:** 13 décembre 2025 (2 jours avant launch)

**Checklist GO/NO-GO:**

**BLOCKERS (1 seul = NO-GO):**

- [ ] ✅ PayPal DÉSACTIVÉ (Tâche 1)
  - Vérification: `python3 verify_paypal_status_forensic.py` = 0 indicators
  - Vérification: Test checkout = PayPal button NOT visible

- [ ] ✅ GTM Conversion Tracking ACTIF (Tâche 2)
  - Vérification: GTM Version 3+ publiée
  - Vérification: Test order = Conversion tag fires sur Thank You page

- [ ] ✅ Checkout fonctionne (Desktop + Mobile) (Tâches 10-11)
  - Vérification: 2+ test orders complétés sans erreurs
  - Vérification: Payment methods corrects affichés

- [ ] ✅ Email flows ACTIVÉS (Tâches 3-4)
  - Vérification: Klaviyo flows status = LIVE
  - Vérification: Test emails reçus

**IMPORTANT (Acceptable de lancer sans, mais à corriger rapidement):**

- [ ] ⚠️ Loyalty Program complet et activé (Tâches 5-9)
  - Si non: Acceptable de lancer, compléter Week 1 post-launch

- [ ] ⚠️ Bundles créés (Tâche 15)
  - Si non: Acceptable de lancer, ajouter Week 1-2 post-launch

- [ ] ⚠️ Facebook Pixel installé (Tâche 14)
  - Si non: Acceptable si pas de Facebook Ads immédiat

- [ ] ⚠️ Google Ads campaign prête (Tâche 16)
  - Si non: Peut créer Jour Launch (3-4h travail)

**DECISION:**

- [ ] **GO**: Tous blockers ✅ → **LAUNCH 15.12.2025 CONFIRMÉ**
- [ ] **NO-GO**: 1+ blocker ❌ → **DELAY 1 semaine (22.12.2025)**
  - Documenter raisons delay
  - Créer plan correction (timeline + responsable)

**Output fichier:**
- Créer: `GO_NO_GO_DECISION_2025-12-13.md`
- Contenu: Checklist ci-dessus + décision + justification

---

## 🚀 JOUR LANCEMENT (15 DEC 2025)

**Timeline heure par heure:**

---

### 🔴 TÂCHE 21: VÉRIFICATION FINALE PRÉ-LAUNCH (09:00)

**Priorité:** CRITIQUE
**Temps estimé:** 30 minutes

**Actions:**
1. [ ] Site accessible: https://www.alphamedical.shop (200 status)
2. [ ] Test checkout rapide (1 produit) → Success
3. [ ] Tous liens homepage fonctionnent (navigation, footer)
4. [ ] GTM Preview Mode: Tags fire correctement
5. [ ] Email test: Klaviyo flows trigger correctly

**Critères de succès:**
- ✅ Aucune erreur 404
- ✅ Checkout fonctionne
- ✅ Tracking actif

---

### 🚀 TÂCHE 22: ACTIVER GOOGLE ADS CAMPAIGN (10:00)

**Priorité:** CRITIQUE (début acquisition trafic)
**Temps estimé:** 10 minutes

**Actions:**
1. [ ] Google Ads → Campaigns
2. [ ] Localiser campaigns DRAFT (Tâche 16):
   - "Search - Brand - Alpha Medical"
   - "Search - Products - Knee Braces"
3. [ ] Pour CHAQUE campaign:
   - Status: DRAFT → **ENABLED**
   - Vérifier budget: $10/jour (Brand) + $20/jour (Products)
   - Vérifier conversion tracking linked
4. [ ] Activer campaigns → Confirmer

**Monitoring initial:**
- [ ] 11:00 (1h après): Vérifier impressions started
- [ ] 13:00 (3h après): Vérifier premiers clics
- [ ] 18:00 (8h après): Review metrics (CTR, CPC, impressions)

**Critères de succès:**
- ✅ Campaigns LIVE (status: Enabled)
- ✅ Impressions >100 première journée
- ✅ CTR >1% (brand), >0.5% (product keywords)
- ✅ CPC <$2 (brand), <$5 (product)

---

### 📣 TÂCHE 23: ANNONCER LANCEMENT (12:00)

**Priorité:** IMPORTANT (générer awareness)
**Temps estimé:** 30 minutes

**Actions:**

1. [ ] **Email blast** (si email list existe):
   - Subject: "🚀 We're Live! Alpha Medical is Now Open"
   - Body: Annonce + 10% launch discount code LAUNCH10
   - CTA: "Shop Now"
   - Send

2. [ ] **Instagram post** (Tâche 17 - Post 1):
   - Publier post annonce lancement
   - Story: Screenshot homepage + swipe up (si >10K followers)

3. [ ] **Facebook post**:
   - Même contenu Instagram
   - Publier sur page Facebook

4. [ ] **LinkedIn post** (si applicable):
   - Annonce professionnelle
   - Focus: Mission, innovation, problem solved

5. [ ] **Réseau personnel**:
   - Message WhatsApp/SMS à entourage
   - Demander partage social media

**Critères de succès:**
- ✅ Au moins 2 canaux activés (email + social)
- ✅ Posts schedulés pour journée complète

---

### 📊 TÂCHE 24: MONITORING PREMIÈRE JOURNÉE (18:00)

**Priorité:** CRITIQUE (détection problèmes rapide)
**Temps estimé:** 30-60 minutes

**Métriques à vérifier:**

1. [ ] **Traffic (Google Analytics / Shopify Analytics)**:
   - Sessions: Target >100 (Day 1)
   - Users: Target >80
   - Bounce rate: <70% acceptable
   - Pages/session: >2 idéal

2. [ ] **Google Ads**:
   - Impressions: >500
   - Clicks: >20
   - CTR: >1%
   - Cost: ~$30 spent
   - Conversions: 0-2 (normal Day 1)

3. [ ] **Conversions**:
   - Orders: Target 1-3 (Day 1 realistic)
   - Conversion rate: >0.5%
   - AOV: ~$85 projected

4. [ ] **Issues détectés**:
   - Errors 404: Check server logs
   - Checkout abandons: Vérifier friction points
   - Customer support: Emails/messages reçus?

**Actions si problèmes:**
- Conversion rate <0.3% → Analyser heatmaps (Clarity), checkout friction
- CPC >$10 → Pause ads, review keywords negative
- Erreurs techniques → Fix immédiatement (priorité #1)

**Output:**
- Créer: `LAUNCH_DAY_REPORT_2025-12-15.md`
- Contenu: Métriques + observations + actions correctives

---

## 📊 POST-LAUNCH: SEMAINES 1-4

**Roadmap résumée (détails complets dans `PRE_LAUNCH_CHECKLIST_23_DAYS.md`):**

---

### SEMAINE 1-2 (15-29 DEC): VALIDATION

**Objectif:** 20-50 premières ventes
**Budget ads:** $30/jour Google Ads
**Focus:** Monitoring tracking + customer support <24h

**Actions clés:**
- [ ] Monitor GTM tags daily
- [ ] Répondre emails <24h
- [ ] Ajuster ads based on performance
- [ ] Compléter bundles (si pas fait)
- [ ] Demander premières reviews (emails automatiques)

**Success metrics:**
- 20-50 orders ✅
- CAC <$50
- Conversion rate >0.8%
- No major technical issues

---

### SEMAINE 3-4 (30 DEC - 12 JAN): OPTIMISATION

**Objectif:** 50-100 orders total
**Budget ads:** Scale $50/jour si CAC <$40
**Focus:** Lancer Facebook Ads + optimiser email flows

**Actions clés:**
- [ ] Lancer Facebook Ads ($20/jour)
- [ ] Analyser email flow metrics (open rate, click rate)
- [ ] A/B test: Product pages, checkout
- [ ] Publier 2 nouveaux articles blog (SEO)

**Success metrics:**
- 80-120 orders cumul
- CAC <$40
- Email attribution: 15-20% revenue
- 5-10 reviews collectées

---

### MOIS 2-3 (JAN-FEB): CROISSANCE

**Objectif:** $10K-$15K MRR
**Budget ads:** $100-150/jour combined (Google + Facebook)
**Focus:** Partnerships + SEO + retargeting

**Actions clés:**
- [ ] Contacter 5-10 physios/coachs (affiliation 15%)
- [ ] Publier 4-6 articles blog/mois
- [ ] Lancer Facebook retargeting campaigns
- [ ] Considérer: VA customer service (si >100 orders/mois)

**Success metrics:**
- Revenue: $10K-$15K MRR
- CAC: <$35
- ROAS: >2.5:1
- Repeat purchase rate: >10%

---

## 📋 RÉCAPITULATIF - PRIORISATION ABSOLUE

### 🔴 BLOCKERS LANCEMENT (7 tâches - 2h total)

**CETTE SEMAINE (22-27 NOV):**

1. ⚠️ PayPal désactivation (10 min)
2. ⚠️ GTM conversion tracking vérification (15 min)
3. ⚠️ Klaviyo Welcome Flow activation (10 min)
4. ⚠️ Klaviyo Abandoned Cart activation (10 min)
5. ⚠️ Loyalty program completion (15 min)
6. ⚠️ Test checkout Desktop + Mobile (25 min)
7. ⚠️ Vérifier GTM tags + email flows (15 min)

**= 100 MINUTES TOTAL = TOUT CRITIQUE TERMINÉ** ✅

---

### 🟡 IMPORTANT (Non-bloquant mais impact majeur)

**SEMAINE 2 (30 NOV - 6 DEC):**

8. Facebook Pixel installation (20 min)
9. Bundles création 3-5 (60 min)
10. Google Ads campaign draft (60 min)
11. Social media content prep (90 min)

**= 3-4 HEURES**

---

### 🟢 OPTIMIZATIONS (Nice-to-have)

**SEMAINE 3 (7-13 DEC):**

12. Stock DSers vérification (30 min)
13. Backup complet (20 min)
14. GO/NO-GO decision (60 min)

**= 2 HEURES**

---

## ✅ TOTAL TEMPS REQUIS PRÉ-LAUNCH

**Critique:** 2 heures
**Important:** 4 heures
**Optimizations:** 2 heures
**TOTAL:** **8 heures sur 23 jours**

**= 20 MINUTES PAR JOUR EN MOYENNE** ✅

---

## 🎯 OBJECTIF FINAL

**15 DÉCEMBRE 2025:**
- ✅ Site 100% fonctionnel
- ✅ Tracking conversions actif (GTM + Facebook)
- ✅ Email automation live (Klaviyo)
- ✅ Loyalty program operational
- ✅ Google Ads campaigns live ($30/jour)
- ✅ Premiers clients acquis (1-3 orders Day 1)

**PATH TO $400K-$1M YEAR 1:**
- Month 1: 100 orders → $9K revenue
- Croissance: 20% MoM
- Month 12: 744 orders → $67K MRR
- Year 1 total: **$356K** (+ holiday boost = **$400K+**) ✅

---

**PRÊT POUR LE LANCEMENT** 🚀

**FOCUS IMMÉDIAT: COMPLÉTER LES 7 TÂCHES CRITIQUES CETTE SEMAINE (2 HEURES)**
