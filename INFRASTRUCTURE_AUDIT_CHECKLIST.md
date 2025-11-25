# INFRASTRUCTURE AUDIT CHECKLIST
## Alpha Medical - Vérification de l'Existant AVANT Planification

**Created:** 2025-11-25 03:30 UTC
**Purpose:** VÉRIFIER factuellement ce qui existe AVANT de planifier/coder
**Approach:** Pas de suppositions - seulement des FAITS vérifiables

---

## 🎯 OBJECTIF

**AVANT de créer quoi que ce soit, répondre à:**
1. Qu'est-ce qui existe DÉJÀ? (workflows, emails, forms, data)
2. Où sont les DONNÉES actuellement? (Shopify, Klaviyo, autres?)
3. Quel est le VOLUME réel? (nombre de leads captés)
4. Qu'est-ce qui MANQUE réellement? (gap analysis)

**Règle:** Zéro assumptions. Seulement des faits vérifiés.

---

## ✅ SECTION 1: SHOPIFY INFRASTRUCTURE

### A. Shopify Admin Access Verification

**Action:** Se connecter à Shopify Admin
- [ ] URL du store Shopify: _________________________
- [ ] Accès admin vérifié: ☐ Oui ☐ Non
- [ ] Date de vérification: _________________________

---

### B. Shopify Flow - Workflows Actifs

**Navigation:** Shopify Admin → Apps → Shopify Flow

**Workflows à vérifier:**

#### 1. Cart Abandonment
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Nom du workflow:** _________________________
- [ ] **Statut:** ☐ Actif ☐ Inactif ☐ Brouillon
- [ ] **Trigger:** _________________________
- [ ] **Actions:** _________________________
- [ ] **Email envoyé?** ☐ Oui ☐ Non
- [ ] **Template email:** _________________________
- [ ] **Données captées:** _________________________
- [ ] **Volume (30 derniers jours):** _________ abandons

#### 2. Account Creation / Welcome
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Nom du workflow:** _________________________
- [ ] **Statut:** ☐ Actif ☐ Inactif ☐ Brouillon
- [ ] **Trigger:** _________________________
- [ ] **Actions:** _________________________
- [ ] **Email envoyé?** ☐ Oui ☐ Non
- [ ] **Template email:** _________________________
- [ ] **Données captées:** _________________________
- [ ] **Volume (30 derniers jours):** _________ créations

#### 3. Newsletter Signup
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Nom du workflow:** _________________________
- [ ] **Statut:** ☐ Actif ☐ Inactif ☐ Brouillon
- [ ] **Trigger:** _________________________
- [ ] **Actions:** _________________________
- [ ] **Email envoyé?** ☐ Oui ☐ Non
- [ ] **Données captées:** _________________________
- [ ] **Volume (30 derniers jours):** _________ signups

#### 4. Contact Form
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Nom du workflow:** _________________________
- [ ] **Statut:** ☐ Actif ☐ Inactif ☐ Brouillon
- [ ] **Trigger:** _________________________
- [ ] **Actions:** _________________________
- [ ] **Où vont les submissions?** _________________________
- [ ] **Volume (30 derniers jours):** _________ soumissions

#### 5. Product Waitlist / Back-in-Stock
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Nom du workflow:** _________________________
- [ ] **Statut:** ☐ Actif ☐ Inactif ☐ Brouillon
- [ ] **Trigger:** _________________________
- [ ] **Actions:** _________________________
- [ ] **Volume (30 derniers jours):** _________ inscriptions

#### 6. Autres Workflows
Liste complète de TOUS les workflows actifs:
```
1. _________________________
2. _________________________
3. _________________________
4. _________________________
5. _________________________
```

---

### C. Shopify Email - Campagnes Actives

**Navigation:** Shopify Admin → Marketing → Automations

**Automations à vérifier:**

#### 1. Abandon de panier
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Statut:** ☐ Actif ☐ Inactif
- [ ] **Nombre d'emails dans séquence:** _________
- [ ] **Délai d'envoi:** _________________________
- [ ] **Taux d'ouverture moyen:** _________%
- [ ] **Taux de conversion:** _________%
- [ ] **Volume envoyé (30 jours):** _________ emails

#### 2. Welcome Series
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Statut:** ☐ Actif ☐ Inactif
- [ ] **Nombre d'emails:** _________
- [ ] **Taux d'ouverture moyen:** _________%
- [ ] **Volume envoyé (30 jours):** _________ emails

#### 3. Browse Abandonment
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Statut:** ☐ Actif ☐ Inactif
- [ ] **Volume envoyé (30 jours):** _________ emails

#### 4. Autres Automations
Liste complète:
```
1. _________________________
2. _________________________
3. _________________________
```

---

### D. Shopify Forms - Forms Actifs

**Navigation:** Shopify Admin → Online Store → Pages / Forms

#### Newsletter Signup Form
- [ ] **Existe sur le site?** ☐ Oui ☐ Non
- [ ] **Emplacement:** ☐ Footer ☐ Popup ☐ Page dédiée ☐ Autre: _________
- [ ] **Champs captés:** _________________________
- [ ] **Action après soumission:** _________________________
- [ ] **Données stockées où?** _________________________

#### Contact Form
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **URL:** _________________________
- [ ] **Champs captés:** _________________________
- [ ] **Où vont les données?** _________________________

#### Product Waitlist Form
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Bouton "Notify me when available"?** ☐ Oui ☐ Non
- [ ] **Champs captés:** _________________________

---

### E. Shopify Customers Database

**Navigation:** Shopify Admin → Customers

**Vérification des données:**
- [ ] **Nombre total de customers:** _________
- [ ] **Customers avec email:** _________
- [ ] **Customers avec phone:** _________
- [ ] **Customers avec tags:** _________
- [ ] **Date du plus ancien customer:** _________________________
- [ ] **Date du plus récent customer:** _________________________

**Tags utilisés (liste complète):**
```
1. _________________________
2. _________________________
3. _________________________
4. _________________________
5. _________________________
```

**Segments créés:**
```
1. _________________________
2. _________________________
3. _________________________
```

---

### F. Shopify Marketing Events

**Navigation:** Shopify Admin → Marketing → Events

- [ ] **Nombre total d'events (30 jours):** _________
- [ ] **Types d'events trackés:** _________________________
- [ ] **Pixels installés:**
  - [ ] Facebook Pixel: ☐ Oui (ID: _________) ☐ Non
  - [ ] TikTok Pixel: ☐ Oui (ID: _________) ☐ Non
  - [ ] Google Analytics: ☐ Oui (ID: _________) ☐ Non
  - [ ] Google Ads: ☐ Oui ☐ Non
  - [ ] Autres: _________________________

---

## ✅ SECTION 2: KLAVIYO INFRASTRUCTURE

### A. Klaviyo Account Access

- [ ] **Compte Klaviyo actif?** ☐ Oui ☐ Non
- [ ] **URL du compte:** _________________________
- [ ] **Accès vérifié:** ☐ Oui ☐ Non
- [ ] **Date de vérification:** _________________________

---

### B. Klaviyo Lists

**Vérification des listes:**

Liste complète de TOUTES les listes:
```
1. Nom: _________________ | Subscribers: _________ | Status: _________
2. Nom: _________________ | Subscribers: _________ | Status: _________
3. Nom: _________________ | Subscribers: _________ | Status: _________
4. Nom: _________________ | Subscribers: _________ | Status: _________
5. Nom: _________________ | Subscribers: _________ | Status: _________
```

---

### C. Klaviyo Flows

**Flows actifs:**

#### 1. Abandon de panier
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Statut:** ☐ Live ☐ Draft ☐ Inactif
- [ ] **Nombre d'emails:** _________
- [ ] **Volume (30 jours):** _________ envois

#### 2. Welcome Series
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Statut:** ☐ Live ☐ Draft ☐ Inactif
- [ ] **Volume (30 jours):** _________ envois

#### 3. Browse Abandonment
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Statut:** ☐ Live ☐ Draft ☐ Inactif
- [ ] **Volume (30 jours):** _________ envois

#### 4. Post-Purchase
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Volume (30 jours):** _________ envois

Liste COMPLÈTE de tous les flows:
```
1. _________________________
2. _________________________
3. _________________________
4. _________________________
5. _________________________
```

---

### D. Klaviyo Campaigns

**Campagnes envoyées (30 derniers jours):**

| Date | Nom | Recipients | Open Rate | Click Rate | Revenue |
|------|-----|-----------|-----------|------------|---------|
| ____ | ___ | _________ | _________% | _________% | $______ |
| ____ | ___ | _________ | _________% | _________% | $______ |
| ____ | ___ | _________ | _________% | _________% | $______ |

---

### E. Klaviyo Integration avec Shopify

- [ ] **Intégration active?** ☐ Oui ☐ Non
- [ ] **Sync automatique?** ☐ Oui ☐ Non
- [ ] **Données synced:** _________________________
- [ ] **Fréquence de sync:** _________________________
- [ ] **Dernière sync:** _________________________

---

## ✅ SECTION 3: FACEBOOK/META INFRASTRUCTURE

### A. Facebook Business Manager Access

- [ ] **Compte Business Manager?** ☐ Oui ☐ Non
- [ ] **Business Manager ID:** _________________________
- [ ] **Accès vérifié:** ☐ Oui ☐ Non

---

### B. Facebook Ad Account

- [ ] **Ad Account actif?** ☐ Oui ☐ Non
- [ ] **Ad Account ID:** _________________________
- [ ] **Statut:** ☐ Actif ☐ Inactif ☐ Restricted
- [ ] **Spend limit:** $_________________________
- [ ] **Spend (30 derniers jours):** $_________________________

---

### C. Facebook Lead Ads

**Campagnes Lead Ads actives:**

#### Campagne 1:
- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Nom:** _________________________
- [ ] **Statut:** ☐ Active ☐ Paused ☐ Ended
- [ ] **Lead Form ID:** _________________________
- [ ] **Budget:** $_________/day
- [ ] **Leads générés (30 jours):** _________
- [ ] **Cost per lead:** $_________

#### Campagne 2:
- [ ] **Nom:** _________________________
- [ ] **Leads (30 jours):** _________

**Total Lead Ads:**
- **Nombre de campagnes actives:** _________
- **Total leads (30 jours):** _________
- **Total spend (30 jours):** $_________

---

### D. Facebook Pixel

- [ ] **Pixel installé?** ☐ Oui ☐ Non
- [ ] **Pixel ID:** _________________________
- [ ] **Events trackés (30 jours):** _________
- [ ] **Standard events actifs:**
  - [ ] PageView
  - [ ] ViewContent
  - [ ] AddToCart
  - [ ] InitiateCheckout
  - [ ] Purchase
  - [ ] Lead
  - [ ] CompleteRegistration

---

### E. Facebook Custom Audiences

**Audiences créées:**
```
1. Nom: _________________ | Size: _________ | Type: _________
2. Nom: _________________ | Size: _________ | Type: _________
3. Nom: _________________ | Size: _________ | Type: _________
```

**Retargeting campaigns actives:**
- [ ] **Nombre:** _________
- [ ] **Spend (30 jours):** $_________
- [ ] **Results:** _________

---

## ✅ SECTION 4: TIKTOK INFRASTRUCTURE

### A. TikTok Ads Manager

- [ ] **Compte TikTok Ads?** ☐ Oui ☐ Non
- [ ] **Ad Account ID:** _________________________
- [ ] **Statut:** ☐ Actif ☐ Inactif

---

### B. TikTok Pixel

- [ ] **Pixel installé?** ☐ Oui ☐ Non
- [ ] **Pixel ID:** _________________________
- [ ] **Events trackés (30 jours):** _________

---

### C. TikTok Campaigns

**Campagnes actives:**
- [ ] **Nombre de campagnes:** _________
- [ ] **Lead generation campaigns:** _________
- [ ] **Spend (30 jours):** $_________
- [ ] **Leads générés:** _________

---

## ✅ SECTION 5: GOOGLE INFRASTRUCTURE

### A. Google Analytics 4

- [ ] **GA4 installé?** ☐ Oui ☐ Non
- [ ] **Property ID:** _________________________
- [ ] **Events trackés:** _________________________
- [ ] **Conversions configurées:** _________________________

---

### B. Google Ads

- [ ] **Compte Google Ads?** ☐ Oui ☐ Non
- [ ] **Customer ID:** _________________________
- [ ] **Campagnes actives:** _________
- [ ] **Spend (30 jours):** $_________

**Lead Form extensions:**
- [ ] **Utilisées?** ☐ Oui ☐ Non
- [ ] **Leads générés (30 jours):** _________

---

### C. Google Tag Manager

- [ ] **GTM installé?** ☐ Oui ☐ Non
- [ ] **Container ID:** _________________________
- [ ] **Tags actifs:** _________

---

## ✅ SECTION 6: DATA STORAGE & EXPORT

### A. Google Sheet - Lead Database

- [ ] **Existe?** ☐ Oui ☐ Non
- [ ] **Nom exact:** _________________________
- [ ] **URL:** _________________________
- [ ] **Nombre de tabs:** _________
- [ ] **Tab names:** _________________________
- [ ] **Nombre de lignes (total leads):** _________
- [ ] **Dernière mise à jour:** _________________________
- [ ] **Mise à jour manuelle ou automatique?** ☐ Manuelle ☐ Auto
- [ ] **Service account access?** ☐ Oui ☐ Non

**Structure des colonnes (liste exacte):**
```
1. _________________________
2. _________________________
3. _________________________
4. _________________________
5. _________________________
[...]
```

---

### B. Export Existants

**Shopify → Autre système:**
- [ ] **Export automatique?** ☐ Oui ☐ Non
- [ ] **Vers où?** _________________________
- [ ] **Fréquence:** _________________________
- [ ] **Dernière export:** _________________________

**Klaviyo → Autre système:**
- [ ] **Export automatique?** ☐ Oui ☐ Non
- [ ] **Vers où?** _________________________

**Facebook → Autre système:**
- [ ] **Export automatique?** ☐ Oui ☐ Non
- [ ] **Méthode:** _________________________

---

## ✅ SECTION 7: VOLUME METRICS (RÉELS - 30 DERNIERS JOURS)

### A. Shopify Metrics

- **Total visitors:** _________
- **Total sessions:** _________
- **Cart abandonment rate:** _________%
- **Cart abandonments (nombre):** _________
- **Account creations:** _________
- **Newsletter signups (si form existe):** _________
- **Contact form submissions:** _________
- **Orders:** _________
- **Conversion rate:** _________%

---

### B. Email Metrics (Shopify Email + Klaviyo)

- **Total emails envoyés (30 jours):** _________
- **Open rate moyen:** _________%
- **Click rate moyen:** _________%
- **Revenue from email (30 jours):** $_________

---

### C. Paid Ads Metrics

**Facebook Ads:**
- **Impressions:** _________
- **Clicks:** _________
- **Leads:** _________
- **Spend:** $_________
- **CPC:** $_________
- **CPL:** $_________

**TikTok Ads:**
- **Leads:** _________
- **Spend:** $_________

**Google Ads:**
- **Leads:** _________
- **Spend:** $_________

---

## ✅ SECTION 8: GAP ANALYSIS

**À remplir APRÈS avoir complété Sections 1-7:**

### Ce qui EXISTE et FONCTIONNE:
```
1. _________________________
2. _________________________
3. _________________________
4. _________________________
5. _________________________
```

### Ce qui EXISTE mais NE FONCTIONNE PAS:
```
1. _________________________
2. _________________________
3. _________________________
```

### Ce qui MANQUE complètement:
```
1. _________________________
2. _________________________
3. _________________________
4. _________________________
5. _________________________
```

### DONNÉES non exportées vers Google Sheet:
```
1. Source: _________ | Volume: _________ | Pourquoi pas exporté: _________
2. Source: _________ | Volume: _________ | Pourquoi pas exporté: _________
3. Source: _________ | Volume: _________ | Pourquoi pas exporté: _________
```

---

## 🎯 CONCLUSIONS DE L'AUDIT

**À remplir APRÈS audit complet:**

### 1. Infrastructure Existante (Score /10)

| Catégorie | Score | Notes |
|-----------|-------|-------|
| Shopify workflows | __/10 | ___________________________ |
| Email automation | __/10 | ___________________________ |
| Forms & capture | __/10 | ___________________________ |
| Data storage | __/10 | ___________________________ |
| Paid ads setup | __/10 | ___________________________ |
| Export/sync | __/10 | ___________________________ |
| **TOTAL** | **__/60** | |

---

### 2. Priorités Réelles (Basées sur FAITS)

**Top 3 quick wins (déjà presque prêt):**
```
1. _________________________
2. _________________________
3. _________________________
```

**Top 3 gaps critiques (manque le plus):**
```
1. _________________________
2. _________________________
3. _________________________
```

**Top 3 améliorations (existe mais peut être mieux):**
```
1. _________________________
2. _________________________
3. _________________________
```

---

### 3. Volume Réel vs Potentiel

| Source | Volume Actuel | Volume Potentiel | Gap | Action Requise |
|--------|---------------|------------------|-----|----------------|
| Cart Abandonment | _________ | _________ | ___% | _______________ |
| Account Creation | _________ | _________ | ___% | _______________ |
| Newsletter | _________ | _________ | ___% | _______________ |
| Contact Form | _________ | _________ | ___% | _______________ |
| FB Lead Ads | _________ | _________ | ___% | _______________ |
| **TOTAL** | **_________** | **_________** | **___%** | |

---

### 4. Plan d'Action Réel (Post-Audit)

**Phase 1: Quick Wins (0-2 semaines)**
```
1. _________________________
2. _________________________
3. _________________________
```

**Phase 2: Gaps Critiques (2-4 semaines)**
```
1. _________________________
2. _________________________
3. _________________________
```

**Phase 3: Optimisations (4-8 semaines)**
```
1. _________________________
2. _________________________
3. _________________________
```

---

## 📋 INSTRUCTIONS POUR COMPLÉTER CET AUDIT

**Option A: Audit Manuel (Recommandé pour précision)**
1. Se connecter à chaque plateforme (Shopify, Klaviyo, FB, etc.)
2. Remplir chaque section avec les DONNÉES RÉELLES
3. Screenshots des dashboards importants
4. Noter TOUT ce qui existe (même si non utilisé)

**Option B: Audit Assisté (Plus rapide)**
1. Fournir accès temporaire aux plateformes
2. Scripts d'audit automatiques (Shopify API, Klaviyo API, etc.)
3. Génération automatique des métriques
4. Vérification manuelle des résultats

---

**Temps estimé pour audit complet:** 4-6 heures
**Deadline:** Avant tout coding/planning supplémentaire
**Responsable:** _________________________
**Date de complétion:** _________________________

---

**UNE FOIS CET AUDIT COMPLÉTÉ, nous aurons les FAITS pour:**
- Savoir exactement ce qui existe
- Identifier les VRAIS gaps
- Planifier SEULEMENT ce qui manque
- Éviter de dupliquer l'existant
- Construire sur ce qui fonctionne déjà

**PAS de coding avant que cet audit soit complété avec des FAITS vérifiables.**
