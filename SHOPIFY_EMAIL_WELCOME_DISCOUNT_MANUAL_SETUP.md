# SHOPIFY EMAIL - WELCOME DISCOUNT MANUAL SETUP (3 MIN)

**Status:** Subject + Preview text configured ✅ | Discount link NOT configured ❌

**Raison:** Shopify Email editor = iframe → Chrome DevTools automation bloquée

---

## ✅ DÉJÀ COMPLÉTÉ (via API + Chrome DevTools)

### 1. Discount Code WELCOME10 créé ✅

```yaml
Code: WELCOME10
Value: 10% off entire order
Type: Amount off order
Eligibility: All customers
Once per customer: Yes ✅
Start date: Nov 25, 2025
Price Rule ID: 1312338182221
Status: Active ✅
```

**Vérification:** https://admin.shopify.com/store/azffej-as/discounts/1312338182221

### 2. Email Details configurés ✅

```yaml
To: Customers subscribed to email marketing ✅
Subject: "Welcome to Alpha Medical! Here's 10% OFF" ✅
Preview: "Thanks for joining us! Use code WELCOME10 for 10% off your first order" ✅
From: Alpha Medical Care - contact@alphamedical.shop ✅
```

---

## ⚠️ ÉTAPES MANUELLES REQUISES (3 min)

### Étape 1: Lier le discount code dans l'email (2 min)

**Chemin:**
1. Shopify Admin → Marketing → Automations
2. Cliquer "Welcome new subscribers with a discount email" (Status: Inactive)
3. Cliquer "Email Welcome aboard!"
4. Dans l'email editor:
   - Cliquer sur la section "Discount" (section 4/7)
   - L'alerte rouge dit "Select a discount"
5. **ACTION CRITIQUE:**
   - Cliquer sur le bouton ou dropdown pour sélectionner un discount
   - Chercher et sélectionner: "WELCOME10" ou "Welcome New Subscribers - 10% Off"
6. **Vérifier:** L'alerte "Select a discount" disparaît

**Screenshot avant:** Alerte rouge "Select a discount" visible
**Screenshot après:** Section Discount configurée, pas d'alerte

---

### Étape 2: Vérifier Subject Line (1 min)

**Problème détecté:** L'alerte "Add a subject" persiste même si le champ est rempli

**Solution:**
1. Dans "Email details" → Subject field
2. **SI l'alerte "Add a subject" est encore visible:**
   - Cliquer dans le champ Subject
   - Vérifier que le texte est: "Welcome to Alpha Medical! Here's 10% OFF"
   - **SI le champ semble vide:** Re-taper le subject
   - Cliquer en dehors du champ pour valider
3. **Vérifier:** L'alerte "Add a subject" disparaît

---

### Étape 3: Activer le workflow (30 sec)

**Chemin:**
1. Toujours dans l'email editor
2. En haut à droite: Cliquer "Set to active"
3. **Vérifier:** Status passe de "Draft" → "Active"

---

## ✅ VÉRIFICATION POST-ACTIVATION

### Email Editor devrait montrer:

```yaml
Status: Active ✅
To: Customers subscribed to email marketing ✅
Subject: "Welcome to Alpha Medical! Here's 10% OFF" ✅ (pas d'alerte)
Preview: "Thanks for joining us! Use code WELCOME10 for 10% off your first order" ✅

Sections (7 total):
  1. Header ✅
  2. Divider ✅
  3. Text (Welcome message) ✅
  4. Discount (WELCOME10 linked) ✅ (pas d'alerte)
  5. Text ✅
  6. Product (Bestsellers) ✅
  7. Footer ✅
```

### Automations page devrait montrer:

```
Marketing → Automations:

ACTIVE:
✅ "Welcome new subscribers with a discount email" - ACTIVE (NOUVEAU)
✅ "Convert abandoned product browse" - Active
✅ "Recover abandoned cart" - Active
✅ "Recover abandoned checkout" - Active

INACTIVE:
❌ "Thank customers after they purchase" - Inactive (à activer séparément)
❌ "Welcome new subscribers..." (duplicate #2) - À supprimer
```

---

## 📊 AVANT vs APRÈS

### AVANT (Actuellement):
```yaml
Discount Code: ✅ WELCOME10 créé (API)
Email Subject: ✅ Configuré (Chrome DevTools)
Email Preview: ✅ Configuré (Chrome DevTools)
Discount Linked: ❌ NON lié (alerte persistante)
Workflow Status: ❌ DRAFT

Email capture proactive: ❌ Aucune
```

### APRÈS (3 min manuel):
```yaml
Discount Code: ✅ WELCOME10 actif
Email Subject: ✅ Validé (pas d'alerte)
Email Preview: ✅ Validé
Discount Linked: ✅ Lié dans email
Workflow Status: ✅ ACTIVE

Email capture proactive: ✅ Email subscription popup actif
Expected: 50-125 nouveaux emails/mois (2-5% capture rate)
```

---

## 🎯 IMPACT BUSINESS

**Flow actuel (PRE-ACTIVATION):**
```
Visitor → Add to cart → Abandon → Email capture (réactif seulement)
```

**Flow après activation:**
```
Visitor → Email popup → Opt-in (10% discount) → Welcome email with WELCOME10 → First purchase
```

**Projection:**
- **Email capture rate:** 2-5% des visitors
- **Visitors/mois:** ~2,500 (projection pre-launch)
- **Nouveaux emails:** 50-125/mois
- **Conversion welcome email:** 5-10% (industry benchmark)
- **Nouveaux clients:** 2-12/mois from welcome flow
- **AOV:** $150 (store average)
- **Revenue Month 1:** $300-1,800 from this workflow alone

---

## ⚠️ LIMITATION TECHNIQUE

**Pourquoi manuel?**
- Shopify Email editor = iframe cross-origin
- Chrome DevTools = bloqué par CORS (timeouts sur clics)
- Shopify Email = PAS d'API publique pour configuration email
- **Requiert:** Intervention manuelle via UI Shopify Admin

**Source:** https://shopify.dev/docs/api/admin-rest (Email/Flow API = non disponible)

---

## 🔗 LIENS RAPIDES

- **Automations:** https://admin.shopify.com/store/azffej-as/marketing/automations
- **Workflow Welcome:** https://admin.shopify.com/store/azffej-as/marketing/automations/flows/22968860749
- **Discount WELCOME10:** https://admin.shopify.com/store/azffej-as/discounts/1312338182221
- **Email Editor:** https://admin.shopify.com/store/azffej-as/flow/custom_configuration_page/0199ede9-754e-7c10-8c5e-17b17a29df6c/welcome_email

---

**⏱️ Temps total:** 3 minutes
**🔧 Complexité:** Faible (point-and-click)
**🔒 Prérequis:** Accès Shopify Admin

**📍 Documentation complète:** `/Users/mac/Desktop/Alpha-Medical/SHOPIFY_EMAIL_WELCOME_DISCOUNT_MANUAL_SETUP.md`

**Dernière mise à jour:** 2025-11-26 Session 56
