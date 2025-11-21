# GOOGLE TAG MANAGER (GTM) - GUIDE COMPLET D'INSTALLATION
**Store:** Alpha Medical Care (azffej-as.myshopify.com)
**Date:** 2025-11-21

---

## POURQUOI GTM?

Google Tag Manager (GTM) est un gestionnaire de tags centralisé qui permet de:
- ✅ Installer Google Ads conversion tracking sans modifier le code
- ✅ Gérer tous les pixels marketing (Facebook, TikTok, etc.) depuis une interface
- ✅ Tester les tags avant publication (mode Preview)
- ✅ Historique des versions et rollback facile
- ✅ Pas besoin d'accès développeur pour ajouter/modifier des tags

---

## STATUT ACTUEL

| Élément | Status | Action requise |
|---------|--------|----------------|
| **GTM Container** | ❌ NON CRÉÉ | Créer container + obtenir ID |
| **GTM Code** | ❌ NON INSTALLÉ | Installer dans theme.liquid |
| **Google Ads Tag** | ⏳ EN ATTENTE | Configurer dans GTM |
| **Conversion Tag** | ⏳ EN ATTENTE | Configurer dans GTM |

---

## ÉTAPE 1: CRÉER UN CONTAINER GTM

### A. Accéder à Google Tag Manager

1. **Allez sur:** https://tagmanager.google.com/

2. **Connectez-vous** avec le compte Google associé à:
   - Google Ads: Alpha Medical Care (128-734-6786)
   - Google Analytics: 513383884

### B. Créer un nouveau container

1. **Si aucun container n'existe:**
   ```
   Cliquez "Créer un compte" (Create Account)
   ```

2. **Remplissez le formulaire:**
   ```
   Nom du compte: Alpha Medical
   Pays: [Votre pays]

   Cochez "Partager les données de manière anonyme avec Google..."

   Configuration du container:
   - Nom du container: Alpha Medical Care
   - Type de cible: Web

   Cliquez "Créer"
   ```

3. **Acceptez les conditions:**
   ```
   Lisez les conditions d'utilisation
   → Cochez "J'accepte..."
   → Cliquez "Oui"
   ```

4. **Récupérez le Container ID:**
   ```
   Après création, vous verrez:

   "Installer Google Tag Manager"

   En haut à gauche: GTM-XXXXXXX ← COPIEZ CE CODE

   Exemple: GTM-ABC1234
   ```

---

## ÉTAPE 2: INSTALLER GTM SUR LE SITE

### Prérequis
- Container ID (format: GTM-XXXXXXX)
- Accès au dossier Alpha-Medical/

### Installation automatique

```bash
cd /Users/mac/Desktop/Alpha-Medical

# Remplacez GTM-XXXXXXX par votre vrai Container ID
python3 install_gtm.py GTM-XXXXXXX
```

### Ce que le script fait:

1. ✅ Valide le format du Container ID
2. ✅ Crée un backup: `layout/theme.liquid.backup_gtm`
3. ✅ Installe le code GTM dans `layout/theme.liquid`:
   - Head code (avant `</head>`)
   - Body code (après `<body>`)
4. ✅ Affiche les instructions de configuration

### Vérification manuelle

Après installation, vérifiez que le code GTM est présent:

```bash
# Vérifier head code
grep -A 3 "Google Tag Manager" layout/theme.liquid | head -10

# Vérifier body code (noscript)
grep -A 2 "Google Tag Manager (noscript)" layout/theme.liquid
```

---

## ÉTAPE 3: VÉRIFIER L'INSTALLATION

### A. Test sur le site live

1. **Allez sur:** https://www.alphamedical.shop/

2. **Ouvrez la console développeur:**
   - Chrome: F12 → Console
   - Safari: Option+Cmd+C

3. **Testez GTM:**
   ```javascript
   // Dans la console, tapez:
   dataLayer

   // Vous devriez voir:
   // Array(X) [{gtm.start: ..., event: 'gtm.js'}, ...]

   // Si undefined ou vide = GTM non chargé
   ```

4. **Vérifiez avec Google Tag Assistant:**
   - Extension Chrome: Google Tag Assistant
   - Activez-la sur votre site
   - Devrait détecter: Google Tag Manager (GTM-XXXXXXX)

### B. Mode Aperçu (Preview) dans GTM

1. **Dans GTM:**
   ```
   Allez sur: https://tagmanager.google.com/
   → Sélectionnez: Container GTM-XXXXXXX
   → Cliquez "Aperçu" (Preview) en haut à droite
   ```

2. **Connectez le site:**
   ```
   Entrez: https://www.alphamedical.shop
   → Cliquez "Connect"

   Un nouvel onglet s'ouvre avec le site
   + une fenêtre Tag Assistant en bas
   ```

3. **Vérifiez les événements:**
   ```
   Tag Assistant → Onglet "Summary"
   → Devrait afficher: Initialization Event
   → Tags: Aucun tag configuré (normal à cette étape)
   ```

---

## ÉTAPE 4: CONFIGURER GOOGLE ADS TAG

### Prérequis

Vous devez d'abord obtenir de Google Ads:
- ✅ Conversion ID (format: AW-XXXXXXXXXX)
- ✅ Conversion Label (format: YYYYYYYYY)

Si vous ne les avez pas encore:
1. Suivez `GOOGLE_ADS_SETUP_GUIDE.md` ÉTAPE 1
2. Créez la conversion "Purchase" dans Google Ads
3. Récupérez le Conversion ID et le Conversion Label

### A. Créer le tag Google Ads (Base Pixel)

1. **Dans GTM:**
   ```
   Tags → Nouveau
   ```

2. **Configuration du tag:**
   ```
   Nom: Google Ads - Base Pixel

   Type de tag:
   → Cherchez "Google Ads"
   → Sélectionnez "Balise Google Ads"

   Configuration:
   - ID de conversion: AW-XXXXXXXXXX

   Trigger (Déclencheur):
   → All Pages (Toutes les pages)

   Cliquez "Enregistrer"
   ```

### B. Créer le tag de conversion Purchase

1. **Tags → Nouveau:**
   ```
   Nom: Google Ads - Purchase Conversion

   Type de tag:
   → "Suivi des conversions Google Ads"

   Configuration:
   - ID de conversion: AW-XXXXXXXXXX
   - Libellé de conversion: YYYYYYYYY
   - Valeur de conversion: {{Transaction Revenue}}
   - ID de transaction: {{Transaction ID}}
   - Code devise: USD (ou votre devise)

   Trigger (Déclencheur):
   → Créez nouveau: "Purchase" (voir section C)

   Cliquez "Enregistrer"
   ```

### C. Créer le trigger Purchase

1. **Triggers → Nouveau:**
   ```
   Nom: Purchase Confirmation Page

   Type de déclencheur:
   → Page View

   Ce déclencheur se déclenche sur:
   → Quelques pages vues (Some Page Views)

   Condition:
   - Page URL | contient | /checkouts/
   - ET
   - Page URL | contient | /thank_you

   OU (alternative plus fiable):
   - Page Path | correspond à l'expression régulière | /orders/.*

   Cliquez "Enregistrer"
   ```

### D. Créer les variables de transaction

GTM a besoin de récupérer les données de la commande.

#### Option 1: Shopify Plus (Accès checkout)

Éditez `templates/checkout.liquid` ou `layout/checkout.liquid`:

```liquid
{% if first_time_accessed %}
<script>
  window.dataLayer = window.dataLayer || [];
  dataLayer.push({
    'event': 'purchase',
    'transactionId': '{{ order.order_number }}',
    'transactionTotal': {{ order.total_price | money_without_currency }},
    'transactionCurrency': '{{ order.currency }}'
  });
</script>
{% endif %}
```

Puis dans GTM:
```
Variables → Nouvelle variable utilisateur

Variable 1:
- Nom: Transaction Revenue
- Type: Variable de couche de données
- Nom de la variable de couche de données: transactionTotal

Variable 2:
- Nom: Transaction ID
- Type: Variable de couche de données
- Nom de la variable de couche de données: transactionId
```

#### Option 2: Shopify Standard (Additional Scripts)

Dans Shopify Admin:
```
Settings → Checkout → Order status page
→ Additional scripts

Ajoutez:
<script>
  window.dataLayer = window.dataLayer || [];
  dataLayer.push({
    'event': 'purchase',
    'transactionId': '{{ order.order_number }}',
    'transactionTotal': {{ order.total_price | money_without_currency }},
    'transactionCurrency': '{{ order.currency }}'
  });
</script>
```

---

## ÉTAPE 5: TESTER ET PUBLIER

### A. Tester en mode Aperçu

1. **Dans GTM:**
   ```
   Cliquez "Aperçu" (Preview)
   → Connectez: https://www.alphamedical.shop
   ```

2. **Tester le Base Pixel:**
   ```
   Naviguez sur n'importe quelle page
   → Tag Assistant devrait afficher:
     "Google Ads - Base Pixel" | FIRED
   ```

3. **Tester la conversion Purchase:**
   ```
   Créez une commande test:
   - Ajoutez un produit au panier
   - Complétez le checkout
   - Arrivez sur la page de confirmation

   → Tag Assistant devrait afficher:
     "Google Ads - Purchase Conversion" | FIRED
   ```

4. **Vérifier les valeurs:**
   ```
   Cliquez sur le tag "Purchase Conversion"
   → Onglet "Variables"
   → Vérifiez:
     - Transaction Revenue = montant correct
     - Transaction ID = order number
   ```

### B. Publier le container

1. **Si tous les tests passent:**
   ```
   Dans GTM, cliquez "Envoyer" (Submit)
   ```

2. **Créez une version:**
   ```
   Nom de la version: v1.0 - Google Ads Conversion Tracking

   Description:
   - Google Ads Base Pixel (AW-XXXXXXXXXX)
   - Purchase Conversion Tracking
   - Transaction revenue and ID variables

   Cliquez "Publier"
   ```

3. **Confirmation:**
   ```
   Vous devriez voir:
   "Version 1 publiée" avec date et heure
   ```

---

## ÉTAPE 6: VÉRIFIER LES CONVERSIONS

### A. Dans GTM (Temps réel)

```
Vue d'ensemble → Section "Débogage"
→ Devrait afficher les récents événements de page vues
```

### B. Dans Google Ads (24-48h délai)

```
Allez sur: https://ads.google.com/
→ Compte: Alpha Medical Care (128-734-6786)
→ Outils et paramètres → Mesure → Conversions
→ Onglet "Activité récente"

Devrait afficher:
- Source: Website (gtag)
- Conversion name: Purchase
- Date/heure de la conversion test
```

---

## ÉTAPE 7: GIT COMMIT

```bash
cd /Users/mac/Desktop/Alpha-Medical

# Vérifier les changements
git status

# Ajouter les fichiers modifiés
git add layout/theme.liquid
git add install_gtm.py
git add GTM_SETUP_GUIDE.md

# Commit
git commit -m "feat(gtm): Install Google Tag Manager GTM-XXXXXXX

GOOGLE TAG MANAGER INSTALLATION:

GTM Container installed:
✅ Container ID: GTM-XXXXXXX (Alpha Medical Care)
✅ Head code installé dans layout/theme.liquid
✅ Body code (noscript) installé après <body>
✅ Backup créé: layout/theme.liquid.backup_gtm

Tags configured in GTM:
✅ Google Ads Base Pixel (AW-XXXXXXXXXX)
✅ Purchase Conversion (AW-XXXXXXXXXX/YYYYYYYYY)
✅ Variables: Transaction Revenue, Transaction ID
✅ Trigger: Purchase Confirmation Page

Files modified:
- layout/theme.liquid: GTM container code
- install_gtm.py (NEW): Automated GTM installation script
- GTM_SETUP_GUIDE.md (NEW): Complete setup guide

Testing:
- Mode Preview: All tags firing correctly
- Test order: Conversion tracked successfully
- Google Tag Assistant: GTM detected

Next steps:
1. Monitor conversions in Google Ads (24-48h)
2. Add additional tags (Facebook Pixel, etc.) in GTM
3. Setup GA4 e-commerce tracking via GTM

Store: azffej-as.myshopify.com
GTM Container: GTM-XXXXXXX
Google Ads: 128-734-6786"

# Push vers GitHub
git push origin main
```

---

## ÉTAPE 8: CONFIGURATION AVANCÉE (OPTIONNELLE)

### A. Enhanced Conversions (Données utilisateur hachées)

Dans GTM:
```
Tags → Google Ads - Purchase Conversion → Modifier
→ Section "Données utilisateur"
→ Activez "Inclure les données utilisateur depuis les variables"

Variables à créer:
- email: Variable de couche de données | email (haché côté serveur)
- phone: Variable de couche de données | phone (haché côté serveur)
```

### B. Dynamic Remarketing (Produits vus)

```
Tags → Nouveau
Nom: Google Ads - Product View

Type: Balise Google Ads - Remarketing

Configuration:
- ID de conversion: AW-XXXXXXXXXX
- Données de remarketing personnalisées:
  * ecomm_prodid: {{Product ID}}
  * ecomm_pagetype: product
  * ecomm_totalvalue: {{Product Price}}

Trigger: Product Page View (créez un trigger pour template.product)
```

### C. Add to Cart Event

```
Tags → Nouveau
Nom: Google Ads - Add to Cart

Type: Balise Google Ads

Configuration:
- ID de conversion: AW-XXXXXXXXXX
- Événement: add_to_cart

Trigger: Add to Cart Button Click (créez un trigger sur bouton)
```

---

## DÉPANNAGE

### Problème: GTM ne charge pas

**Symptômes:**
- `dataLayer` est undefined dans console
- Google Tag Assistant ne détecte rien

**Solutions:**
1. Vérifiez que `layout/theme.liquid` contient le code GTM (head + body)
2. Videz le cache Shopify: Admin → Themes → Actions → Edit code → Ctrl+S
3. Testez en navigation privée
4. Vérifiez bloqueurs de publicité (désactivez pour test)
5. Vérifiez que le Container ID est correct (GTM-XXXXXXX)

### Problème: Tags ne se déclenchent pas

**Symptômes:**
- Tag Assistant affiche le tag comme "Not Fired"
- Aucun événement dans GTM Debug

**Solutions:**
1. Vérifiez les triggers en mode Preview
2. Vérifiez les conditions des triggers (URL, événements)
3. Testez les variables (Variables → Debug)
4. Vérifiez l'ordre de déclenchement (Tags → Order)

### Problème: Conversions ne trackent pas dans Google Ads

**Symptômes:**
- Aucune conversion dans Google Ads après 24-48h
- Tag se déclenche dans GTM mais pas dans Ads

**Solutions:**
1. Vérifiez le Conversion ID (doit être exact: AW-XXXXXXXXXX)
2. Vérifiez le Conversion Label (doit être exact: YYYYYYYYY)
3. Vérifiez les variables Transaction Revenue et Transaction ID
4. Vérifiez que la conversion existe dans Google Ads
5. Attendez 24-48h (délai de traitement)

### Problème: Variables vides (Transaction Revenue = 0)

**Cause:** dataLayer ne contient pas les données de transaction

**Solutions:**
1. Vérifiez que le code dataLayer.push() est sur la page de confirmation
2. Dans console, tapez: `dataLayer` → vérifiez les valeurs
3. Vérifiez les noms des variables (case-sensitive)
4. Ajoutez console.log() pour déboguer:
   ```javascript
   console.log('Transaction Total:', '{{ order.total_price | money_without_currency }}');
   ```

---

## RESSOURCES

**Documentation officielle:**
- Google Tag Manager: https://support.google.com/tagmanager
- GTM for e-commerce: https://developers.google.com/tag-platform/gtagjs/reference/events
- Shopify + GTM: https://help.shopify.com/en/manual/promoting-marketing/analyze-marketing/google-tag-manager

**Outils de diagnostic:**
- Google Tag Assistant: https://chrome.google.com/webstore (extension Chrome)
- GTM Preview Mode: Intégré dans GTM
- Conversion Tracking Status: Google Ads → Tools → Conversions → Tracking status

**Templates GTM populaires:**
- Facebook Pixel via GTM
- TikTok Pixel via GTM
- GA4 E-commerce via GTM
- Hotjar via GTM

---

## CHECKLIST FINALE

Avant de considérer l'installation complète:

**GTM Installation:**
- [ ] Container GTM créé (GTM-XXXXXXX obtenu)
- [ ] Script `install_gtm.py` exécuté avec succès
- [ ] Code GTM installé dans `layout/theme.liquid` (head + body)
- [ ] dataLayer fonctionne (test console navigateur)
- [ ] Google Tag Assistant détecte GTM
- [ ] Mode Preview fonctionne

**Google Ads Configuration:**
- [ ] Conversion ID (AW-XXXXXXXXXX) obtenu depuis Google Ads
- [ ] Conversion Label (YYYYYYYYY) obtenu
- [ ] Tag "Base Pixel" créé dans GTM
- [ ] Tag "Purchase Conversion" créé dans GTM
- [ ] Variables Transaction Revenue et Transaction ID créées
- [ ] Trigger "Purchase Confirmation Page" créé

**Testing:**
- [ ] Mode Preview testé (tous tags se déclenchent)
- [ ] Commande test créée
- [ ] Tag "Purchase Conversion" déclenché sur page confirmation
- [ ] Variables contiennent les bonnes valeurs (montant, ID commande)
- [ ] Container publié (Version 1)

**Vérification:**
- [ ] Conversion test apparaît dans Google Ads (24-48h délai)
- [ ] Git commit + push effectué
- [ ] Documentation mise à jour

---

**Installation Date:** 2025-11-21
**Store:** Alpha Medical Care (azffej-as.myshopify.com)
**Google Ads:** 128-734-6786
**Status:** ⏳ EN ATTENTE DU GTM CONTAINER ID

---

## TEMPS ESTIMÉ

| Étape | Temps | Complexité |
|-------|-------|------------|
| Créer container GTM | 3 min | Facile |
| Installer GTM (script) | 1 min | Automatique |
| Vérifier installation | 2 min | Facile |
| Configurer tags Google Ads | 10 min | Moyen |
| Créer variables + triggers | 5 min | Moyen |
| Tester en Preview | 5 min | Facile |
| Commande test + vérification | 10 min | Facile |
| Publier + commit | 2 min | Facile |
| **TOTAL** | **38 min** | **Moyen** |

**Prérequis:** Conversion ID Google Ads (AW-XXXXXXXXXX) obtenu avant de commencer.

---
