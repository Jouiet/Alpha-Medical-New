# GOOGLE ADS - GUIDE COMPLET D'INSTALLATION
**Store:** Alpha Medical Care (azffej-as.myshopify.com)
**Google Ads Customer ID:** 128-734-6786
**Date:** 2025-11-21

---

## STATUT ACTUEL

| Élément | Status | Action requise |
|---------|--------|----------------|
| **Compte Google Ads** | ✅ EXISTE | Customer ID: 128-734-6786 |
| **Pixel installé** | ❌ NON | Installation requise |
| **Conversions configurées** | ⚠️ INCONNU | Vérification requise |
| **Liaison GA4** | ⚠️ INCONNU | Configuration requise |

---

## ÉTAPE 1: OBTENIR LE CONVERSION ID (REQUIS)

### Navigation Google Ads

1. **Allez sur:** https://ads.google.com/

2. **Sélectionnez le compte:**
   - Nom: **Alpha Medical Care**
   - Customer ID: **128-734-6786**

3. **Navigation dans l'interface:**
   ```
   Cliquez "Outils et paramètres" (🔧 icône clé en haut à droite)
   └─> Section "Mesure"
       └─> Cliquez "Conversions"
   ```

4. **Deux scénarios possibles:**

#### SCÉNARIO A: Aucune conversion n'existe
```
→ Cliquez "+ Nouvelle action de conversion"
→ Sélectionnez "Site web"
→ Catégorie: "Achat"
→ Nom: "Purchase - Alpha Medical"
→ Valeur: "Utiliser des valeurs de transaction différentes"
→ Cliquez "Créer et continuer"
```

#### SCÉNARIO B: Des conversions existent déjà
```
→ Vous voyez une liste de conversions
→ Cliquez sur la conversion "Purchase" (ou similaire)
→ Cliquez "Modifier les paramètres" ou "Installer le tag"
```

5. **Récupérer le Conversion ID:**
   ```
   Dans la page de configuration du tag:
   → Cliquez "Installer le tag vous-même"
   → Vous verrez un code JavaScript contenant:

   gtag('config', 'AW-XXXXXXXXXX');

   → Copiez le AW-XXXXXXXXXX
   → Exemple: AW-1234567890
   ```

6. **Récupérer AUSSI le Conversion Label:**
   ```
   Dans le même code, cherchez:

   gtag('event', 'conversion', {
     'send_to': 'AW-XXXXXXXXXX/YYYYYYYYY'
   });

   → YYYYYYYYY = Conversion Label (requis pour tracking achat)
   → Exemple: AbCdEfGhIj123456
   ```

---

## ÉTAPE 2: INSTALLATION DU PIXEL

### Prérequis
- Conversion ID (format: AW-XXXXXXXXXX)
- Accès au dossier Alpha-Medical/

### Installation automatique

```bash
cd /Users/mac/Desktop/Alpha-Medical

# Remplacez AW-XXXXXXXXXX par votre vrai Conversion ID
python3 install_google_ads_pixel.py AW-XXXXXXXXXX
```

### Ce que le script fait:

1. ✅ Valide le format du Conversion ID
2. ✅ Crée un backup: `layout/theme.liquid.backup_google_ads`
3. ✅ Installe le pixel gtag.js dans `layout/theme.liquid` (avant `</head>`)
4. ✅ Crée 2 snippets de conversion:
   - `snippets/google-ads-purchase-conversion.liquid` (tracking achat)
   - `snippets/google-ads-add-to-cart.liquid` (tracking panier)

---

## ÉTAPE 3: CONFIGURATION DU TRACKING ACHAT

### A. Éditer le snippet de conversion

1. **Ouvrez le fichier:**
   ```
   snippets/google-ads-purchase-conversion.liquid
   ```

2. **Remplacez `CONVERSION_LABEL`:**
   ```liquid
   <!-- AVANT -->
   'send_to': 'AW-XXXXXXXXXX/CONVERSION_LABEL',

   <!-- APRÈS (avec votre vrai Conversion Label) -->
   'send_to': 'AW-1234567890/AbCdEfGhIj123456',
   ```

3. **Sauvegardez le fichier**

### B. Ajouter le snippet à la page de confirmation

#### Option 1: Shopify Plus (Accès au checkout)
```liquid
Fichier: templates/checkout-confirmation.liquid (ou layout/checkout.liquid)

Ajoutez avant </body>:
{% render 'google-ads-purchase-conversion' %}
```

#### Option 2: Shopify Standard (Pas d'accès checkout)
```
1. Allez dans: Shopify Admin → Settings → Checkout
2. Section: "Order status page" → "Additional scripts"
3. Collez le code suivant (remplacez AW-XXXXXXXXXX et YYYYYYYYY):

<script>
  gtag('event', 'conversion', {
    'send_to': 'AW-XXXXXXXXXX/YYYYYYYYY',
    'value': {{ order.total_price | money_without_currency }},
    'currency': '{{ order.currency }}',
    'transaction_id': '{{ order.order_number }}'
  });
</script>
```

---

## ÉTAPE 4: GIT COMMIT

```bash
cd /Users/mac/Desktop/Alpha-Medical

# Vérifier les changements
git status

# Ajouter les fichiers modifiés
git add layout/theme.liquid
git add snippets/google-ads-purchase-conversion.liquid
git add snippets/google-ads-add-to-cart.liquid
git add install_google_ads_pixel.py
git add GOOGLE_ADS_SETUP_GUIDE.md

# Commit
git commit -m "feat(google-ads): Install conversion tracking pixel AW-XXXXXXXXXX

GOOGLE ADS CONVERSION TRACKING INSTALLATION:

Pixel installé:
✅ Conversion ID: AW-XXXXXXXXXX (Alpha Medical Care 128-734-6786)
✅ gtag.js installé dans layout/theme.liquid
✅ Purchase conversion snippet créé
✅ Add to cart snippet créé

Files modified:
- layout/theme.liquid: Google Ads gtag.js pixel
- snippets/google-ads-purchase-conversion.liquid: Purchase tracking
- snippets/google-ads-add-to-cart.liquid: Add to cart event

Next steps:
1. Add Conversion Label to purchase snippet
2. Add snippet to checkout confirmation page
3. Test with real order
4. Verify conversions in Google Ads dashboard

Google Ads Account: 128-734-6786
Store: azffej-as.myshopify.com"

# Push vers GitHub
git push origin main
```

---

## ÉTAPE 5: VÉRIFICATION & TEST

### A. Vérifier l'installation du pixel

1. **Allez sur votre site:** https://www.alphamedical.shop/

2. **Ouvrez la console développeur:**
   - Chrome: F12 → Console
   - Safari: Option+Cmd+C

3. **Cherchez le script gtag.js:**
   ```javascript
   // Dans la console, tapez:
   dataLayer

   // Vous devriez voir un array avec des objets
   // Si vide ou undefined = pixel non chargé
   ```

4. **Vérifiez avec Google Tag Assistant:**
   - Extension Chrome: Google Tag Assistant
   - Activez-la sur votre site
   - Devrait détecter: Google Ads Conversion Tracking (AW-XXXXXXXXXX)

### B. Tester une conversion

1. **Créer une commande test:**
   ```
   - Ajoutez un produit au panier
   - Complétez le checkout
   - Utilisez carte de test Shopify: 1 (Bogus Gateway)
   - Confirmez la commande
   ```

2. **Vérifier dans Google Ads:**
   ```
   Allez sur: https://ads.google.com/
   → Compte: Alpha Medical Care (128-734-6786)
   → Mesure → Conversions
   → Onglet "Activité récente"
   → Devrait afficher votre conversion test (délai: 3-24h)
   ```

3. **Si la conversion n'apparaît PAS:**
   - Vérifiez que le Conversion Label est correct
   - Vérifiez la console navigateur pour erreurs JavaScript
   - Vérifiez que le snippet est bien sur la page de confirmation
   - Attendez 24-48h (délai de traitement Google)

---

## ÉTAPE 6: LIAISON GA4 ↔ GOOGLE ADS

### Pourquoi lier?
- Remarketing audiences depuis GA4 vers Google Ads
- Import des conversions GA4 dans Google Ads
- Rapports croisés GA4/Ads

### Navigation

1. **Dans Google Ads:**
   ```
   Outils et paramètres → Configuration → Comptes associés
   → Cherchez "Google Analytics (GA4)"
   → Cliquez "Associer"
   → Sélectionnez: Propriété GA4 "Alpha Medical" (513383884)
   → Confirmez
   ```

2. **Dans Google Analytics 4:**
   ```
   Admin → Propriété: Alpha Medical
   → Liens vers les produits Google Ads
   → Cliquez "Associer"
   → Sélectionnez: Customer ID 128-734-6786
   → Activez "Import de conversions" et "Personnalisation"
   → Enregistrer
   ```

3. **Vérification:**
   ```
   Dans Google Ads:
   → Outils → Comptes associés
   → Google Analytics devrait afficher "Associé" avec une coche verte
   ```

---

## ÉTAPE 7: CONFIGURATION AVANCÉE (OPTIONNELLE)

### A. Dynamic Remarketing (Produits vus)

Ajouter à `layout/theme.liquid` après le pixel principal:

```liquid
<!-- Google Ads Dynamic Remarketing -->
<script>
  {% if template contains 'product' %}
  gtag('event', 'view_item', {
    'send_to': 'AW-XXXXXXXXXX',
    'value': {{ product.price | money_without_currency }},
    'items': [{
      'id': '{{ product.id }}',
      'google_business_vertical': 'retail'
    }]
  });
  {% endif %}
</script>
```

### B. Enhanced Conversions (Email + Phone hashing)

```liquid
<!-- Enhanced Conversions (GDPR compliant) -->
<script>
  {% if customer %}
  gtag('set', 'user_data', {
    'email': '{{ customer.email | sha256 }}',
    'phone_number': '{{ customer.phone | sha256 }}'
  });
  {% endif %}
</script>
```

---

## DÉPANNAGE

### Problème: Pixel ne charge pas

**Symptômes:**
- `dataLayer` est undefined dans console
- Google Tag Assistant ne détecte rien

**Solutions:**
1. Vérifiez que `layout/theme.liquid` contient le script gtag.js
2. Videz le cache: Shopify Admin → Online Store → Themes → Actions → Edit code → Ctrl+S
3. Testez en navigation privée
4. Vérifiez bloqueurs de publicité (désactivez pour test)

### Problème: Conversions ne trackent pas

**Symptômes:**
- Aucune conversion dans Google Ads après 24-48h
- Console affiche erreur gtag

**Solutions:**
1. Vérifiez le Conversion Label (doit être exact)
2. Vérifiez que le snippet est sur la BONNE page (order confirmation)
3. Testez avec Google Tag Assistant en temps réel
4. Vérifiez les paramètres de conversion (valeur, devise, transaction_id)

### Problème: Erreur "AW-XXXXXXXXXX not found"

**Cause:** Conversion ID invalide ou compte Google Ads désactivé

**Solutions:**
1. Re-vérifiez le Conversion ID dans Google Ads
2. Vérifiez que le compte 128-734-6786 est actif
3. Attendez 15 minutes après création de conversion (propagation)

---

## RESSOURCES

**Documentation officielle:**
- Google Ads Conversion Tracking: https://support.google.com/google-ads/answer/6095821
- gtag.js Reference: https://developers.google.com/gtagjs/reference/api
- Shopify Order Confirmation: https://help.shopify.com/en/manual/orders/order-status

**Outils de diagnostic:**
- Google Tag Assistant: https://chrome.google.com/webstore (extension Chrome)
- Google Ads Conversion Tracking Status: Google Ads → Tools → Conversions → Tracking status

---

## CHECKLIST FINALE

Avant de considérer l'installation complète:

- [ ] Conversion ID (AW-XXXXXXXXXX) obtenu depuis Google Ads
- [ ] Conversion Label obtenu (YYYYYYYYY)
- [ ] Script `install_google_ads_pixel.py` exécuté avec succès
- [ ] Pixel gtag.js installé dans `layout/theme.liquid`
- [ ] Conversion Label ajouté dans `snippets/google-ads-purchase-conversion.liquid`
- [ ] Snippet de conversion ajouté à la page de confirmation d'achat
- [ ] Git commit + push effectué
- [ ] Pixel vérifié avec Google Tag Assistant
- [ ] Commande test créée
- [ ] Conversion test apparaît dans Google Ads (24-48h délai)
- [ ] GA4 ↔ Google Ads liaison établie
- [ ] Documentation mise à jour

---

**Installation Date:** 2025-11-21
**Account:** Alpha Medical Care (128-734-6786)
**Store:** azffej-as.myshopify.com
**Status:** ⏳ EN ATTENTE DU CONVERSION ID

---
