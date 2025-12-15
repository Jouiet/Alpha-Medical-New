# JUDGE.ME IMPORT - INSTRUCTIONS FACTUELLES
**Basé sur l'état vérifié: 0 reviews actuelles, 10 produits actifs**
**Date:** 2025-11-29

---

## ÉTAT ACTUEL (VÉRIFIÉ VIA API)

```
✅ Judge.me installé: True (Handle: judgeme)
✅ Store: Alpha Medical Care
✅ Theme: Alpha-Medical-New/main (ID: 140069830733)
✅ Produits actifs: 10
⚠️ Reviews actuelles: 0
```

---

## FORMULAIRE D'IMPORT (INTERFACE RÉELLE)

Vous avez montré ce formulaire:

```
Import reviews

Shopify product
  Search by product title, handle or ID
  [Please select a product.]

AliExpress product URL
  Paste your AliExpress URL

Translate to (provided by AliExpress)
  English ✓

Number of reviews to import
  15

Email jouiet.hat@gmail.com when import completed
```

---

## PREMIER IMPORT - PRODUIT CONCRET

### Produit sélectionné (vérifié via API):
**Bunion Corrector Toe Separator**
- **Shopify Product ID:** 7616306806861
- **Handle:** bunion-corrector-toe-separator-bunions-haluksy-separators-halux-toe-spreader-finger-straightener-for-toe-hallux-valgus-corrector
- **Prix:** $59.79 USD
- **Type:** Foot Care & Orthotics
- **Inventaire:** 625 unités

**Pourquoi ce produit en premier?**
- Prix accessible ($59.79)
- Inventaire élevé (625 unités)
- Type single product (pas bundle complexe)
- Catégorie populaire (foot care)

---

## STEP 1: TROUVER PRODUIT ALIEXPRESS (MÉTHODE FACTUELLE)

### 1.1 Ouvrir AliExpress
```
URL: https://www.aliexpress.com
```

### 1.2 Recherche exacte
```
Search box: "bunion corrector toe separator hallux valgus"
```

### 1.3 Filtrer résultats (critères factuels)
Cliquer sur filtres:
- **Orders:** Min 1000+ (popularity proof)
- **Star Rating:** 4.5 - 5.0 (quality proof)
- **Shipping from:** China/Overseas (fastest = China)

### 1.4 Sélection produit (critères visuels)
Parcourir les 5-10 premiers résultats, sélectionner produit qui:
- ✅ A photos SIMILAIRES à votre produit Shopify
- ✅ A 100+ reviews with photos
- ✅ A 4.5+ stars
- ✅ A 1000+ orders
- ❌ PAS de mentions "AliExpress" dans review photos
- ❌ PAS de reviews avec mauvaise traduction EN

### 1.5 Copier URL
Cliquer sur le produit → Copier URL de la barre d'adresse

**Format URL attendu:**
```
https://www.aliexpress.com/item/1005XXXXXXXXXXXX.html
OU
https://www.aliexpress.us/item/XXXXXXXXXXXX.html
```

---

## STEP 2: REMPLIR FORMULAIRE JUDGE.ME

### 2.1 Accéder formulaire
```
Judge.me Dashboard → Reviews → Import Reviews
OU
URL directe (si disponible): https://judge.me/reviews/import
```

### 2.2 Champ "Shopify product"
**3 options possibles:**

**Option A - Par Handle (RECOMMANDÉ):**
```
Taper: bunion-corrector-toe-separator
Sélectionner: "Bunion Corrector Toe Separator Bunions Haluksy..."
```

**Option B - Par ID:**
```
Taper: 7616306806861
Sélectionner: Le produit qui apparaît
```

**Option C - Par titre:**
```
Taper: Bunion Corrector
Sélectionner: "Bunion Corrector Toe Separator Bunions Haluksy..."
```

### 2.3 Champ "AliExpress product URL"
```
Coller: [URL copiée de Step 1.5]
Exemple: https://www.aliexpress.com/item/1005003842156789.html
```

### 2.4 Champ "Translate to"
```
Sélectionner: English ✓ (déjà sélectionné)
```

### 2.5 Champ "Number of reviews to import"
```
Entrer: 15
Rationale: 10-15 reviews = optimal first import (pas trop, pas trop peu)
```

### 2.6 Email notification
```
Vérifier: jouiet.hat@gmail.com ✓
```

### 2.7 Click "Import" button
```
Attendre: 5-10 minutes
Check email: Notification de complétion
```

---

## STEP 3: VÉRIFICATION POST-IMPORT (FACTUEL)

### 3.1 Email notification
Vous recevrez (dans 5-10 min):
```
From: Judge.me <noreply@judge.me>
Subject: Review import completed for [Product Name]
Body:
  - Reviews imported: 15
  - Average rating: [X.X] stars
  - Photos imported: [X]
```

### 3.2 Vérifier Dashboard Judge.me
```
Judge.me → Reviews → All Reviews
Filter: Product = "Bunion Corrector Toe Separator"
Expected: 15 reviews listées
```

### 3.3 Vérifier Product Page Shopify
```
URL: https://alphamedical.shop/products/bunion-corrector-toe-separator-bunions-haluksy-separators-halux-toe-spreader-finger-straightener-for-toe-hallux-valgus-corrector

Scroll to: Section reviews (bas de page)
Expected: Widget Judge.me avec 15 reviews affichées
```

### 3.4 Quality check
Lire 3-5 reviews importées:
- [ ] Traduction EN correcte (pas de gibberish)
- [ ] Contenu match product features
- [ ] Pas de mentions "AliExpress", "China shipping", "customs"
- [ ] Photos (si importées) sont pertinentes

### 3.5 Actions si problèmes
**Si traduction mauvaise:**
```
Judge.me → Reviews → Edit review → Corriger texte manuellement
```

**Si reviews non pertinentes:**
```
Judge.me → Reviews → Delete review
```

**Si rating trop parfait (all 5-star):**
```
Judge.me → Reviews → Delete quelques 5-star
Goal: Mix 60% 5-star, 30% 4-star, 10% 3-star
```

---

## APRÈS PREMIER IMPORT RÉUSSI

### Re-run verification script
```bash
python3 verify_judgeme_state.py
```

**Expected output (après import):**
```
✅ Judge.me installed: True
✅ Products ready: 10 active products
✅ Current reviews: 1 product with reviews (Bunion Corrector)
📋 Next step: Import next product OR activate Tidio flows #5-6
```

### Décision: Continuer imports OU activer Tidio?

**Option A: Continuer imports (9 produits restants)**
- Suivre même process pour produits #2-10
- Timeline: 1-2 produits/jour = 5 jours

**Option B: Activer Tidio flows #5-6 maintenant**
- 1 produit avec reviews = suffisant pour tester flows
- Flow #5 (Rating Protector) = actif immédiatement
- Flow #6 (Thank Positive Reviews) = actif immédiatement

**Recommandation factuelle:**
Option B - Tester flows avec 1 produit avant d'importer 112 reviews

---

## TROUBLESHOOTING (BASÉ SUR FAITS CONNUS)

### Problème: Produit Shopify non trouvé
**Solution:**
```bash
# Vérifier handle exact
python3 -c "
import os, requests
from dotenv import load_dotenv
load_dotenv('.env.admin')
query = '''{ products(first:1, query:\"id:7616306806861\") { edges { node { title handle } } } }'''
r = requests.post(f'https://{os.getenv(\"SHOPIFY_STORE_DOMAIN\")}/admin/api/2024-01/graphql.json',
  headers={'X-Shopify-Access-Token': os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN'), 'Content-Type': 'application/json'},
  json={'query': query})
print(r.json()['data']['products']['edges'][0]['node']['handle'])
"
```

### Problème: URL AliExpress invalide
**Symptômes:**
- Erreur "Invalid URL" dans Judge.me
- Import ne démarre pas

**Solution:**
- Vérifier format URL: doit contenir `/item/` et finir par `.html`
- Tester URL dans navigateur (doit ouvrir product page)
- Si URL redirect → copier URL finale après redirect

### Problème: Import prend >15 minutes
**Actions:**
- Check email spam folder (notification peut être là)
- Refresh Judge.me dashboard (F5)
- Si >30 min: Contact Judge.me support (support@judge.me)

### Problème: Reviews importées sont en Chinois
**Cause:**
- AliExpress auto-translate OFF
- Reviews source sont en Chinois

**Solution:**
- Judge.me → Reviews → Select all → Bulk actions → Translate to English
- OU Delete + Re-import avec différent produit AliExpress

---

## NEXT STEPS (APRÈS PREMIER IMPORT)

### Immédiat (aujourd'hui):
1. [ ] Importer Produit #1 (Bunion Corrector - 15 reviews)
2. [ ] Vérifier quality (3.1-3.5)
3. [ ] Run verification script
4. [ ] Décider Option A ou B

### Court terme (demain):
- **Si Option A:** Importer Produit #2 (Effective Bunion Corrector Airbag - 12 reviews)
- **Si Option B:** Activer Tidio Flow #5 + #6 (10 minutes)

### Moyen terme (3-7 jours):
- Compléter 10 produits avec reviews (112 total)
- Activer tous Tidio flows (#1-6)
- Monitor conversion rate avec/sans reviews

---

**Document Version:** 1.0 (2025-11-29)
**Basé sur:** État vérifié API (verify_judgeme_state.py)
**Approche:** Bottom-up factuelle (pas de suppositions)
**Status:** Ready for execution
