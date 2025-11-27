# Configuration Manuelle - 40% Restant du Workflow Loyalty Tier Tagging

**Date:** 2025-11-20
**Statut Actuel:** 60% automatisé | 40% à compléter manuellement
**Temps estimé:** 10 minutes

---

## RÉSUMÉ DE CE QUI EST DÉJÀ FAIT

### ✅ Complété Automatiquement (60%)

1. **4 Codes de réduction - 100% ACTIFS**
   - LOYALTY10 (Bronze - 10%)
   - LOYALTY15 (Silver - 15%)
   - LOYALTY25 (Gold - 25%)
   - LOYALTY50 (Platinum - 50%)

2. **Workflow Shopify Flow - Structure de base**
   - Trigger: "Order paid" ✅
   - Condition Platinum ($2500+) ✅
   - Actions Platinum:
     * Add tag: loyalty-platinum ✅
     * Remove tags: loyalty-bronze, loyalty-silver, loyalty-gold ✅
   - Branche FALSE créée avec nouvelle condition vide ✅

### ⏳ À Compléter Manuellement (40%)

Le workflow est ouvert à cette URL:
https://admin.shopify.com/store/azffej-as/apps/flow/editor/019aa2e4-81e1-798b-8beb-91d1e89d7238/01KAHE90EY2HNH84H6P67AM079

---

## INSTRUCTIONS DÉTAILLÉES

### Étape 1: Configurer la Condition Gold ($1000+)

Vous devriez voir une condition avec "Select condition" qui est déjà créée dans la branche FALSE.

1. **Ajouter la variable:**
   - Dans le panneau latéral "Add a variable", cliquez sur **"order"**
   - Naviguez: `order` → `purchasingEntity` → `Customer` → `amountSpent` → `amount`
   - Cliquez pour sélectionner `amount`

2. **Configurer la comparaison:**
   - Dans "Comparison", sélectionnez: **"Greater than or equal to"**
   - Dans "Amount", entrez: **1000**

3. **Sauvegarder:**
   - Le workflow devrait sauvegarder automatiquement

---

### Étape 2: Ajouter Actions Gold (Branche TRUE)

1. **Cliquez sur le "+" de la branche TRUE de la condition Gold**

2. **Action 1: Add customer tags**
   - Cherchez: "Add customer tags"
   - Dans "Tags", tapez: **loyalty-gold**
   - Cliquez "Close"

3. **Cliquez sur le "+" sous l'action "Add customer tags"**

4. **Action 2: Remove customer tags**
   - Cherchez: "Remove customer tags"
   - Dans "Tags", tapez: **loyalty-bronze, loyalty-silver, loyalty-platinum**
   - Cliquez "Close"

---

### Étape 3: Créer Condition Silver ($500+)

1. **Dans la branche FALSE de la condition Gold:**
   - Cliquez sur le bouton "Expand menu" (les 3 points)
   - Sélectionnez "Create condition"

2. **Configurer la condition:**
   - Variable: `order.purchasingEntity.Customer.amountSpent.amount`
   - Comparison: "Greater than or equal to"
   - Amount: **500**

---

### Étape 4: Ajouter Actions Silver (Branche TRUE)

1. **Action 1: Add customer tags**
   - Tags: **loyalty-silver**

2. **Action 2: Remove customer tags**
   - Tags: **loyalty-bronze, loyalty-gold, loyalty-platinum**

---

### Étape 5: Ajouter Actions Bronze (Branche FALSE)

Dans la branche FALSE de la condition Silver (dernier niveau):

1. **Action 1: Add customer tags**
   - Tags: **loyalty-bronze**

2. **Action 2: Remove customer tags**
   - Tags: **loyalty-silver, loyalty-gold, loyalty-platinum**

---

### Étape 6: Activer le Workflow

1. **Cliquez sur "Turn on workflow"** en haut à droite
2. **Confirmez** l'activation

---

## STRUCTURE FINALE ATTENDUE

```
Order paid
│
└─► IF amount >= 2500 (Platinum) ✅ FAIT
    ├─► TRUE:
    │   ├─► Add tag: loyalty-platinum ✅
    │   └─► Remove tags: bronze, silver, gold ✅
    │
    └─► FALSE: IF amount >= 1000 (Gold) ⏳ À FAIRE
        ├─► TRUE:
        │   ├─► Add tag: loyalty-gold
        │   └─► Remove tags: bronze, silver, platinum
        │
        └─► FALSE: IF amount >= 500 (Silver) ⏳ À FAIRE
            ├─► TRUE:
            │   ├─► Add tag: loyalty-silver
            │   └─► Remove tags: bronze, gold, platinum
            │
            └─► FALSE (Bronze) ⏳ À FAIRE
                ├─► Add tag: loyalty-bronze
                └─► Remove tags: silver, gold, platinum
```

---

## VÉRIFICATION FINALE

### Test 1: Vérifier que le workflow est actif
- Le workflow devrait afficher "Active" en haut

### Test 2: Créer une commande test
1. Créez une commande de test pour $100
2. Marquez-la comme payée
3. Vérifiez que le client reçoit le tag `loyalty-bronze`

### Test 3: Vérifier les codes de réduction
```bash
python3 verify_loyalty_discount_codes.py
```

Devrait afficher:
```
✅ LOYALTY10 - Bronze Tier (10% off) - ACTIVE
✅ LOYALTY15 - Silver Tier (15% off) - ACTIVE
✅ LOYALTY25 - Gold Tier (25% off) - ACTIVE
✅ LOYALTY50 - Platinum Tier (50% off) - ACTIVE
```

---

## IMPACT ATTENDU

Une fois le workflow activé:

- **Tagging automatique:** Chaque commande payée déclenche l'attribution du tier approprié
- **Mise à jour automatique:** Les clients qui franchissent un seuil sont automatiquement upgradés
- **Codes de réduction prêts:** Les 4 codes sont actifs et fonctionnels
- **Badge de fidélité:** Visible sur `/account` pour chaque client

---

## SUPPORT

**Fichiers de référence:**
- `verify_loyalty_discount_codes.py` - Vérification des codes
- `LOYALTY_AUTOMATION_PROGRESS_REPORT.md` - Rapport de progression
- `complete_flow_automation.py` - Guide automatisé

**En cas de problème:**
1. Vérifiez que tous les tags sont exactement: `loyalty-bronze`, `loyalty-silver`, `loyalty-gold`, `loyalty-platinum`
2. Vérifiez que les montants sont: 500, 1000, 2500
3. Vérifiez que la comparaison est "Greater than or equal to" pour toutes les conditions

---

**Temps estimé de complétion:** 10 minutes
**Difficulté:** Faible (copier-coller les valeurs ci-dessus)

🎯 Le tier Platinum est déjà 100% configuré et sert de modèle pour les 3 tiers restants!
