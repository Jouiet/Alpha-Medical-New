# SHOPIFY FLOW - LIMITATION API DOCUMENTÉE
**Date:** 2025-12-05
**Contexte:** Session 80 - Résolution action restante "Shopify Flows API debug"
**Méthodologie:** Web search + documentation officielle Shopify

---

## 🔍 PROBLÈME IDENTIFIÉ

**Erreur rencontrée:**
```
Field 'flows' doesn't exist on type 'QueryRoot'
Code: undefinedField
API: Shopify GraphQL Admin 2025-10
```

**Tentative de requête:**
```graphql
{
  flows(first: 10) {
    edges {
      node {
        id
        name
        enabled
      }
    }
  }
}
```

---

## ✅ RECHERCHE DOCUMENTÉE

**Sources consultées (2025-12-05):**
1. Shopify Changelog: Flow adopts version 2025-10 of GraphQL Admin API
2. Shopify Help Center: Shopify Flow and GraphQL Admin API
3. Shopify Dev Docs: GraphQL Admin API reference
4. Shopify Dev Docs: About Flow actions
5. Web search: Multiple queries sur "Shopify Flow API list workflows"

**Résultat recherche:**

### CE QUI EXISTE ✅

1. **Flow UTILISE GraphQL Admin API 2025-10**
   - Pour évaluer conditions et variables dans les workflows
   - Pour exécuter des actions dans le store
   - Access aux données via API (orders, products, customers, etc.)

2. **flowTriggerReceive mutation** (GraphQL)
   - Permet de déclencher des workflows programmatiquement
   - Workflows qui commencent avec un trigger spécifique
   - Référence: https://shopify.dev/docs/api/admin-graphql/latest/mutations/flowtriggerreceive

3. **Flow Connector APIs**
   - Apps peuvent créer des endpoints API standardisés
   - Custom triggers et actions
   - Webhooks pour notifications

### CE QUI N'EXISTE PAS ❌

**Aucun endpoint API public pour:**
- ❌ Lister tous les workflows d'un store
- ❌ Récupérer les définitions de workflows
- ❌ Query le statut ou la configuration des workflows
- ❌ Gérer programmatiquement les workflows (create, update, delete)

---

## 📊 CONCLUSION FACTUELLE

**LIMITATION TECHNIQUE SHOPIFY CONFIRMÉE:**

> Shopify Flow ne fournit **AUCUNE API publique** (REST ou GraphQL) pour lister, récupérer ou gérer les workflows programmatiquement (en date de décembre 2025).

**Raison technique:**
- Flow est conçu comme une app d'administration uniquement
- Gestion des workflows exclusivement via l'interface Shopify Admin
- Pas de workflow management API dans la roadmap publique

**Impact Alpha Medical:**
- Impossible de vérifier programmatiquement les flows actifs via API
- Vérification manuelle requise via Shopify Admin interface

---

## 🛠️ SOLUTION DE CONTOURNEMENT

### Méthode de Vérification Manuelle

**Étapes:**
1. Se connecter à Shopify Admin: https://azffej-as.myshopify.com/admin
2. Naviguer vers: Apps → Flow
3. Vue "Workflows" affiche tous les flows avec leur statut (On/Off)
4. Cliquer sur chaque flow pour voir détails et exécutions récentes

**Informations disponibles manuellement:**
- ✅ Liste de tous les workflows
- ✅ Statut (On/Off) de chaque workflow
- ✅ Dernière exécution et historique
- ✅ Configuration complète (triggers, conditions, actions)
- ✅ Logs d'exécution et erreurs

**Screenshot recommandé:**
- Prendre screenshot de la liste des workflows
- Sauvegarder avec date pour tracking

---

## 📝 VÉRIFICATION FACTUELLE SESSION 80

**État documenté (sources internes):**
- **INFRASTRUCTURE_AUDIT_CHECKLIST.md:** "Shopify Flow: 5/5 workflows active (100% ✅)"
- **.claude/memory/00-metadata.md:** "Shopify Flow: 5 workflows (5/5 active 100% ✅)"
- **Session 61 verification:** User screenshot verified (Nov 26-27 2025)

**Discordance audit externe:**
- Audit externe mentionne "4 flows" vs documentation interne "5 flows"
- Écart: 1 flow (20% discordance)

**Dernière vérification manuelle:**
- Date: 2025-11-27 (Session 61)
- Méthode: User screenshot
- Résultat: 5/5 workflows actifs confirmés

**Prochaine vérification recommandée:**
- Date: Avant lancement (2025-12-25)
- Méthode: Shopify Admin → Flow → Screenshot
- Objectif: Confirmer 5 flows actifs avant premières commandes

---

## 🎯 DOCUMENTATION MISE À JOUR

**Fichiers à corriger:**

1. **FORENSIC_ANALYSIS_SUMMARY.env**
   - Ligne 78: `SHOPIFY_FLOWS_STATUS`
   - Avant: "INCONNU: L'API GraphQL a retourné une erreur"
   - Après: "NON VÉRIFIABLE API (limitation Shopify 2025): Aucun endpoint public pour lister workflows. Dernière vérification manuelle: 5/5 actifs (Session 61, 2025-11-27, user screenshot)."

2. **INFRASTRUCTURE_AUDIT_CHECKLIST.md**
   - Session 80 actions restantes
   - Avant: "Shopify Flows API debug (medium - GraphQL field inexistant)"
   - Après: "✅ RÉSOLU (limitation technique Shopify documentée)"

3. **check_audit_claims.py**
   - Claim #3 verification
   - Ajouter note: "Limitation API Shopify - vérification manuelle requise"

---

## 📌 RÉFÉRENCES OFFICIELLES

**Shopify Developer Documentation:**
- GraphQL Admin API: https://shopify.dev/docs/api/admin-graphql/latest
- Shopify Flow: https://shopify.dev/docs/apps/build/flow
- Flow Actions: https://shopify.dev/docs/apps/build/flow/actions
- flowTriggerReceive mutation: https://shopify.dev/docs/api/admin-graphql/latest/mutations/flowtriggerreceive

**Changelog:**
- Flow adopts 2025-10 API: https://changelog.shopify.com/posts/flow-adopts-version-2025-10-of-the-graphql-admin-api

**Help Center:**
- Shopify Flow: https://help.shopify.com/en/manual/shopify-flow
- Flow and GraphQL: https://help.shopify.com/en/manual/shopify-flow/concepts/admin-api

---

## ✅ RÉSOLUTION

**STATUS:** RÉSOLU PAR DOCUMENTATION

**Nature:** LIMITATION TECHNIQUE SHOPIFY (pas un bug de notre côté)

**Impact:** Faible
- Flows vérifiés manuellement Session 61 (5/5 actifs)
- Vérification manuelle simple et rapide
- Aucun impact sur fonctionnalité Flow

**Action requise:** Vérification manuelle avant lancement (2025-12-25)

**Documentation:** Complète et factuelle ✅

---

**Analyste:** Claude Code (Session 80)
**Date:** 2025-12-05
**Méthode:** Web search + documentation officielle + zero bullshit
