# GTM - AJOUTER LES 2 TAGS MANQUANTS (URGENT)

**Date:** 2025-11-21 23:30
**Status:** Configuration incomplète - 2 tags manquants détectés par GTM Diagnostics
**Temps requis:** 10 minutes

---

## 🚨 DIAGNOSTICS GTM - PROBLÈMES DÉTECTÉS

```
URGENT - Incidence sur mesures:

1. ❌ Balise Conversion Linker manquante
   → Nécessaire pour mesurer clics sur annonces

2. ❌ Balises Google manquantes
   → Nécessaire pour mesures exactes (AW-17749024238)
```

**Vérification site live:**
- ✅ GTM-WFPH2KZP: Actif
- ✅ GT-NC6L8G55: Détecté
- ❌ AW-17749024238: NON détecté
- ❌ Conversion tracking code: NON visible dans HTML

**Conclusion:** Version 2 publiée MAIS 2 tags critiques manquants

---

## ÉTAPE 1: Créer Google Tag (Base) - 5 minutes

### A. Dans GTM (https://tagmanager.google.com/)

**Sélectionnez:** Container GTM-WFPH2KZP

### B. Créer le tag

1. **Cliquez:** "Balises" (Tags) → "Nouveau" (bouton rouge)

2. **Nom du tag:**
   ```
   Google Tag - Base (AW-17749024238)
   ```

3. **Configuration du tag:**
   - Cliquez sur l'icône de configuration
   - Dans la recherche, tapez: **"Google Tag"**
   - Sélectionnez: **"Google Tag"** (ou "Balise Google")

   **SI "Google Tag" n'apparaît pas:**
   - Sélectionnez: **"Balise Google Ads"**

4. **Paramètres du tag:**

   **Tag ID / ID de balise:**
   ```
   AW-17749024238
   ```

   **OU si le champ demande le format complet:**
   ```
   GT-NC6L8G55
   ```

   **Note:** Certaines interfaces acceptent AW-XXXXX, d'autres GT-XXXXX. Essayez d'abord AW-17749024238.

5. **Configuration avancée (optionnel):**
   - Laissez tous les paramètres par défaut
   - Ne cochez rien de spécial

6. **Déclencheur:**
   - Cliquez sur "Déclenchement" (en bas)
   - Sélectionnez: **"Initialization - All Pages"**

   **SI "Initialization" n'existe pas:**
   - Sélectionnez: **"All Pages"** (Toutes les pages)

7. **Enregistrer:**
   - Cliquez "Enregistrer" (en haut à droite)

---

## ÉTAPE 2: Créer Conversion Linker - 3 minutes

### A. Créer le tag

1. **Balises → Nouveau**

2. **Nom du tag:**
   ```
   Conversion Linker
   ```

3. **Configuration du tag:**
   - Recherchez: **"Conversion Linker"**
   - Sélectionnez: **"Conversion Linker"**

   **Apparence possible:**
   - "Conversion Linker"
   - "Google Ads - Conversion Linker"
   - "Outil de liaison de conversion"

4. **Paramètres:**
   - **Aucun paramètre requis** - Laissez tout par défaut
   - Ce tag n'a pas de configuration spécifique

5. **Déclencheur:**
   - Sélectionnez: **"All Pages"** (Toutes les pages)

6. **Enregistrer**

---

## ÉTAPE 3: Vérifier la configuration - 2 minutes

### A. Vérifier les 3 tags

**Dans GTM → Balises, vous devriez voir:**

```
✅ Google Tag - Base (AW-17749024238)
   Déclencheur: Initialization - All Pages (ou All Pages)

✅ Conversion Linker
   Déclencheur: All Pages

✅ Suivi des conversions Google Ads (EXISTANT)
   Conversion ID: 17749024238
   Conversion Label: gm87CKudp8QbEO67so9C
   Déclencheur: Purchase Confirmation Page
```

### B. Vérifier l'ordre de déclenchement

**Ordre optimal:**
1. **Google Tag (Base)** - Se charge en premier (Initialization)
2. **Conversion Linker** - Se charge sur toutes les pages
3. **Conversion Tracking** - Se déclenche uniquement sur /thank_you

**Important:** GTM gère l'ordre automatiquement avec les triggers Initialization/All Pages

---

## ÉTAPE 4: Tester en Preview Mode

### A. Activer Preview

1. **Dans GTM:** Cliquez "Aperçu" (Preview) en haut à droite

2. **Connectez le site:**
   ```
   https://www.alphamedical.shop
   ```

### B. Tester sur homepage

1. **Naviguez sur la homepage**

2. **Tag Assistant devrait afficher:**
   ```
   Tags Fired (3 tags):
   ✅ Google Tag - Base (AW-17749024238)
   ✅ Conversion Linker
   ✅ (Autres tags éventuels)
   ```

3. **Vérifiez que le tag Conversion NE SE DÉCLENCHE PAS:**
   ```
   Tags Not Fired:
   - Suivi des conversions Google Ads
   ```

   **Normal:** Ce tag ne doit se déclencher QUE sur /thank_you

### C. Tester le déclenchement Conversion (optionnel - post-launch)

**Après le 15.12.2025, quand vous aurez des commandes:**

1. Créez une commande test
2. Arrivez sur /checkouts/.../thank_you
3. Vérifiez que les 3 tags se déclenchent:
   - Google Tag (Base) ✅
   - Conversion Linker ✅
   - **Conversion Tracking ✅** (doit apparaître ici)

---

## ÉTAPE 5: Publier Version 3

### A. Si tests OK en Preview

1. **Fermez le mode Preview**

2. **Cliquez "Envoyer" (Submit)** en haut à droite

### B. Créer la version

**Nom de la version:**
```
v3.0 - Google Tag + Conversion Linker
```

**Description:**
```
- Ajout Google Tag (base): AW-17749024238
- Ajout Conversion Linker pour cross-domain tracking
- Correction diagnostics GTM (2 tags manquants)
- Configuration complète Google Ads conversion tracking

Date: 21/11/2025
Status: Prêt pour launch 15.12.2025
```

3. **Cliquez "Publier" (Publish)**

---

## ÉTAPE 6: Vérifier les diagnostics GTM

### A. Après publication (attendre 2-3 min)

1. **Dans GTM:** Onglet "Admin" → "Diagnostics du Conteneur"

2. **Vérifiez que les 2 alertes ont disparu:**
   ```
   ✅ Balise Conversion Linker: Présente
   ✅ Balises Google: Présente (AW-17749024238)
   ```

3. **Si les alertes persistent:**
   - Attendez 5-10 minutes (délai de propagation)
   - Actualisez la page
   - Vérifiez que Version 3 est bien la version live

---

## COMMANDE DE VÉRIFICATION

```bash
# Vérifier les tags sur le site live (après publication v3)
python3 verify_google_tags_live.py

# Résultat attendu:
# ✅ GTM DÉTECTÉ: GTM-WFPH2KZP
# ✅ GOOGLE TAG (BASE) DÉTECTÉ: AW-17749024238
# ✅ GT- TAG DÉTECTÉ: GT-NC6L8G55
# ✅ dataLayer DÉTECTÉ
# ✅ CONFIGURATION COMPLÈTE: OK
```

---

## ARCHITECTURE FINALE (Après v3)

```
USER VISIT
    ↓
GTM loads (GTM-WFPH2KZP)
    ↓
├── [INITIALIZATION/ALL PAGES]
│   ├── Google Tag (Base) fires
│   │   → Loads gtag.js library
│   │   → ID: AW-17749024238
│   │   → Tracks page views
│   │
│   └── Conversion Linker fires
│       → Enables cross-domain tracking
│       → Links ad clicks to conversions
│
├── [USER BROWSES SITE]
│   → Both tags active on all pages
│   → Collecting analytics data
│
└── [USER COMPLETES PURCHASE]
    → Arrives at /checkouts/.../thank_you
    ↓
    [TRIGGER: Purchase Confirmation Page]
    ↓
    Google Ads Conversion Tracking fires
    → Conversion ID: AW-17749024238
    → Conversion Label: gm87CKudp8QbEO67so9C
    → Value: Order total
    → Transaction ID: Order number
    ↓
    Google Ads records conversion
    ↓
    Visible in dashboard (24-48h delay)
```

---

## DIFFÉRENCE ENTRE LES 3 TAGS

### 1. Google Tag (Base) - AW-17749024238
**Rôle:** Fondation/bibliothèque
- Charge gtag.js sur toutes les pages
- Permet aux autres tags Google de fonctionner
- Collecte données analytics basiques

### 2. Conversion Linker
**Rôle:** Attribution cross-domain
- Lie les clics sur annonces aux conversions
- Nécessaire pour mesure précise ROI
- Gère les cookies de tracking

### 3. Conversion Tracking (EXISTANT)
**Rôle:** Événement spécifique
- Se déclenche UNIQUEMENT sur /thank_you
- Envoie données de conversion à Google Ads
- Utilise la fondation des 2 premiers tags

**Analogie:**
- Google Tag = Fondation d'une maison
- Conversion Linker = Système électrique
- Conversion Tracking = Ampoule qui s'allume (événement)

---

## DÉPANNAGE

### Problème: "Google Tag" n'apparaît pas dans les types de balises

**Solution:**
1. Utilisez "Balise Google Ads" à la place
2. Configurez avec: AW-17749024238
3. Trigger: Initialization - All Pages

### Problème: Diagnostics GTM ne se mettent pas à jour

**Solution:**
1. Attendez 10 minutes après publication
2. Videz le cache navigateur (Cmd+Shift+R)
3. Vérifiez que v3 est la version live (Admin → Versions)

### Problème: Tags détectés en Preview mais pas sur live site

**Solution:**
1. Attendez 2-3 minutes (cache Shopify)
2. Testez en navigation privée
3. Vérifiez avec: `python3 verify_google_tags_live.py`

---

## CHECKLIST FINALE

**Avant publication v3:**
- [ ] Google Tag créé avec AW-17749024238
- [ ] Conversion Linker créé
- [ ] Les 3 tags visibles dans GTM
- [ ] Preview mode testé (3 tags sur homepage)
- [ ] Conversion tag NE SE DÉCLENCHE PAS sur homepage (normal)

**Après publication v3:**
- [ ] Version 3 publiée
- [ ] Diagnostics GTM: 0 alertes
- [ ] Script verify_google_tags_live.py: Configuration complète
- [ ] Documentation mise à jour

**Post-launch (15.12.2025):**
- [ ] Première commande test
- [ ] Vérifier déclenchement des 3 tags
- [ ] Conversion visible dans Google Ads (24-48h)

---

## VALEURS DE RÉFÉRENCE

```
GTM Container: GTM-WFPH2KZP
Google Ads Account: 128-734-6786
Conversion ID: AW-17749024238
Conversion Label: gm87CKudp8QbEO67so9C
Google Tag: GT-NC6L8G55 (détecté sur site)

Store: alphamedical.shop
Launch date: 15.12.2025
Business model: Dropshipping (pre-launch)
```

---

**ÉTAPE ACTUELLE:** Créer les 2 tags manquants dans GTM
**TEMPS ESTIMÉ:** 10 minutes
**STATUS:** Configuration à 85% → 100% après v3
**BLOCAGE:** None - Action immédiate possible

---
