# SHOPIFY EMAIL - MANUEL D'ACTIVATION (5 MIN)

**Raison:** Shopify Flow n'a PAS d'API publique - activation MANUELLE requise via UI

---

## 🚨 ACTIONS CRITIQUES (5 min total)

### 1. Activer "Thank you!" workflow (2 min) - CRITIQUE

**Chemin:**
1. Shopify Admin → Apps → Email → Tab "Automations"
2. Chercher: "Thank you!" (Status: Draft)
3. Cliquer sur "Thank you!"
4. Cliquer "Turn on automation"
5. **Vérifier:** Status passe de "Draft" à "Active"

**Impact:**
- ❌ ACTUELLEMENT: Aucun email après achat
- ✅ APRÈS ACTIVATION: Email automatique post-purchase (brand building, upsell)

---

### 2. Résoudre Duplicate "Welcome with discount" (3 min)

**Chemin:**
1. Shopify Admin → Apps → Email → Tab "Automations"
2. Identifier les 2 duplicates (même nom, même trigger)

**DUPLICATE #1** (Garder):
- Nom: "Welcome with discount"
- Status: Draft
- Trigger: Customer subscribed to email marketing
- **ACTION:** Activer celui-ci (cliquer → "Turn on automation")

**DUPLICATE #2** (Supprimer):
- Nom: "Welcome with discount"
- Status: Draft
- Trigger: Customer subscribed to email marketing
- **ACTION:** Supprimer (cliquer → More actions → Delete)

**Impact:**
- ❌ RISQUE: Duplicate emails si les 2 actifs
- ✅ APRÈS FIX: Un seul email welcome envoyé

---

## ✅ VERIFICATION POST-ACTIVATION

### Shopify Email - Automations Tab
**Devrait montrer:**
```
ACTIVE (5 total):
✅ "We're happy to see you again" - Browse abandonment
✅ "Did something catch your eye?" - Browse abandonment
✅ "You left items in your cart" - Cart abandonment
✅ "You left items at checkout" - Checkout abandonment
✅ "Thank you!" - Post-purchase (NOUVEAU)
✅ "Welcome with discount" - Email subscription (NOUVEAU)

DRAFT (0):
(Aucun - tous actifs ou supprimés)
```

---

## 📊 AVANT vs APRÈS

### AVANT (Session 56):
```
Active: 4/7 workflows (57%)
- Browse/Cart/Checkout abandonment ✅
- Post-purchase ❌ INACTIF
- Welcome discount ❌ INACTIF (2 duplicates)

Email capture sources actives:
- Cart abandonment (capture email au checkout)
- Account creation
- 0 proactive capture (pas de popup)
```

### APRÈS (5 min manuel):
```
Active: 6/7 workflows (86%)
- Browse/Cart/Checkout abandonment ✅
- Post-purchase ✅ ACTIF
- Welcome discount ✅ ACTIF (1 seul, duplicate supprimé)

Email capture sources actives:
- Cart abandonment ✅
- Account creation ✅
- Email subscription popup ✅ (NOW ACTIVE)
```

---

## 🎯 IMPACT BUSINESS

**Actuellement (PRE-ACTIVATION):**
- Visitors → Add to cart → Abandon → Email capture
- **Problème:** Aucune capture proactive avant abandon

**Après activation:**
- Visitors → Email popup → Opt-in → 10% discount → Purchase
- **Flow:** Welcome email → Nurture → Conversion
- **Expected:** 2-5% email capture rate = 50-125 emails/month (sur 2,500 visitors/month)

---

## ⚠️ LIMITATION TECHNIQUE

**Pourquoi manuel?**
- Shopify Flow n'a PAS d'API publique
- Shopify Email workflows = gérés via Shopify Flow
- Impossible d'automatiser via scripts/API
- **Requiert:** Intervention manuelle via UI Shopify Admin

**Source:** https://shopify.dev/docs/api/admin-rest (Flow API = non disponible)

---

**Temps total:** 5 minutes
**Complexité:** Faible (point-and-click)
**Prérequis:** Accès Shopify Admin

**Dernière mise à jour:** 2025-11-26 Session 56
