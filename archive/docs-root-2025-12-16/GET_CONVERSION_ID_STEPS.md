# OBTENIR GOOGLE ADS CONVERSION ID - ÉTAPES EXACTES

**Container GTM installé:** ✅ GTM-WFPH2KZP
**Status:** En attente du Conversion ID pour configuration GTM

---

## ÉTAPE 1: Obtenir Conversion ID + Label (5 minutes)

**J'ai ouvert:** https://ads.google.com/aw/conversions

### Actions à faire:

1. **Sélectionnez le compte:**
   ```
   Alpha Medical Care
   Customer ID: 128-734-6786
   ```

2. **Dans la liste des conversions:**
   ```
   Vous devriez voir une conversion nommée:
   - "Achat" ou
   - "Purchase" ou
   - "Purchase - Alpha Medical"

   Cliquez dessus
   ```

3. **Sur la page de la conversion:**
   ```
   Cherchez un bouton:
   - "Balise" ou
   - "Tag" ou
   - "Installer le tag" ou
   - "Set up tag"

   Cliquez dessus
   ```

4. **Sélectionnez "Installer le tag vous-même":**
   ```
   Options possibles:
   - "Install the tag yourself"
   - "Installer le tag vous-même"
   - "Use Google Tag Manager" (NE PAS choisir encore)

   Choisissez: "Install the tag yourself"
   ```

5. **Copiez les codes:**
   ```
   Vous verrez du code JavaScript avec:

   <!-- Global site tag (gtag.js) - Google Ads: AW-XXXXXXXXXX -->
   <script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXXX"></script>
   <script>
     window.dataLayer = window.dataLayer || [];
     function gtag(){dataLayer.push(arguments);}
     gtag('js', new Date());

     gtag('config', 'AW-XXXXXXXXXX');  ← COPIEZ CE CODE
   </script>

   ET plus bas:

   <!-- Event snippet for Purchase conversion page -->
   <script>
     gtag('event', 'conversion', {
         'send_to': 'AW-XXXXXXXXXX/YYYYYYYYY',  ← COPIEZ AUSSI CE CODE
         'value': 1.0,
         'currency': 'USD',
         'transaction_id': ''
     });
   </script>

   IMPORTANT:
   - AW-XXXXXXXXXX = Conversion ID (10-12 chiffres)
   - YYYYYYYYY = Conversion Label (lettres + chiffres + tirets)

   Exemples réels:
   - AW-1234567890
   - AW-128734678612345

   Exemples de label:
   - AbCdEfGhIj123456
   - xyz_123-ABC
   ```

6. **Collez les codes ici (dans votre terminal ou fichier texte):**
   ```
   Conversion ID: AW-__________________
   Conversion Label: ____________________
   ```

---

## ÉTAPE 2: Configurer Google Ads dans GTM (15 minutes)

### A. Ouvrir GTM

```bash
# Je vais ouvrir GTM pour vous
open "https://tagmanager.google.com/"

# Sélectionnez le container: GTM-WFPH2KZP
```

### B. Créer le tag "Base Pixel"

1. **Dans GTM:**
   ```
   Tags → Nouveau (bouton rouge en haut à droite)
   ```

2. **Nom du tag:**
   ```
   Google Ads - Base Pixel
   ```

3. **Configuration du tag:**
   ```
   Cliquez sur "Configuration du tag"
   → Tapez "Google Ads" dans la recherche
   → Sélectionnez: "Balise Google Ads" (ou "Google Ads Tag")
   ```

4. **ID de conversion:**
   ```
   Entrez: AW-XXXXXXXXXX
   (le Conversion ID que vous avez copié à l'étape 1)
   ```

5. **Déclencheur (Trigger):**
   ```
   Cliquez sur "Déclenchement" (en bas)
   → Sélectionnez: "All Pages" (Toutes les pages)
   ```

6. **Enregistrer:**
   ```
   Cliquez "Enregistrer" (en haut à droite)
   ```

### C. Créer le tag "Purchase Conversion"

1. **Tags → Nouveau:**
   ```
   Nom: Google Ads - Purchase Conversion
   ```

2. **Configuration du tag:**
   ```
   Type: "Suivi des conversions Google Ads"
        (ou "Google Ads Conversion Tracking")
   ```

3. **Paramètres:**
   ```
   ID de conversion: AW-XXXXXXXXXX
   Libellé de conversion: YYYYYYYYY  ← Collez le Conversion Label
   Valeur de conversion: Utilisez les variables suivantes:
     → Sélectionnez: "{{Transaction Revenue}}" (on va créer cette variable après)
   ID de transaction: {{Transaction ID}}
   Code devise: USD (ou votre devise)
   ```

4. **Déclencheur:**
   ```
   On va créer un nouveau trigger:
   Cliquez "Déclenchement" → "+"

   Nom: Purchase Confirmation Page

   Type de déclencheur: "Page View" (Vue de page)

   Ce déclencheur se déclenche sur:
   → Sélectionnez: "Quelques pages vues" (Some Page Views)

   Conditions:
   - Page URL | contient | thank_you
   ```

   **Note:** Si Shopify utilise `/checkouts/` dans l'URL, ajoutez:
   ```
   - Page URL | contient | /checkouts/
   ```

5. **Enregistrer le trigger et le tag**

### D. Créer les variables

**Note:** Pour Shopify, les données de transaction sont déjà disponibles via le dataLayer de Shopify.

1. **Variables → Nouvelle:**
   ```
   Nom: Transaction Revenue

   Type de variable: "Variable de couche de données"
                     (Data Layer Variable)

   Nom de la variable de couche de données: ecommerce.purchase.actionField.revenue
   ```

2. **Variables → Nouvelle:**
   ```
   Nom: Transaction ID

   Type de variable: "Variable de couche de données"

   Nom de la variable de couche de données: ecommerce.purchase.actionField.id
   ```

**Alternative (si les variables ci-dessus ne fonctionnent pas):**

Pour Shopify, vous pouvez aussi utiliser:
- `Shopify.checkout.order_id` pour Transaction ID
- `Shopify.checkout.total_price` pour Transaction Revenue

### E. Tester en mode Aperçu (Preview)

1. **Dans GTM:**
   ```
   Cliquez "Aperçu" (Preview) en haut à droite
   ```

2. **Connectez votre site:**
   ```
   Entrez: https://www.alphamedical.shop
   Cliquez "Connect"
   ```

3. **Un nouvel onglet s'ouvre avec Tag Assistant**

4. **Testez le Base Pixel:**
   ```
   Naviguez sur n'importe quelle page
   → Tag Assistant devrait afficher:
     "Google Ads - Base Pixel" | Tags Fired
   ```

5. **Testez la conversion Purchase:**
   ```
   Créez une commande test:
   - Ajoutez un produit au panier
   - Complétez le checkout (utilisez Bogus Gateway pour test)
   - Arrivez sur la page de confirmation

   → Tag Assistant devrait afficher:
     "Google Ads - Purchase Conversion" | Tags Fired
   ```

6. **Vérifiez les valeurs:**
   ```
   Cliquez sur le tag "Purchase Conversion"
   → Onglet "Variables"
   → Vérifiez que Transaction Revenue et Transaction ID ont des valeurs
   ```

### F. Publier le container

1. **Si les tests sont OK:**
   ```
   Fermez le mode Preview
   Dans GTM, cliquez "Envoyer" (Submit) en haut à droite
   ```

2. **Créez une version:**
   ```
   Nom de la version: v1.0 - Google Ads Conversion Tracking

   Description:
   - Google Ads Base Pixel (AW-XXXXXXXXXX)
   - Purchase Conversion Tracking
   - Conversion Label: YYYYYYYYY

   Cliquez "Publier" (Publish)
   ```

---

## ÉTAPE 3: Vérifier les conversions (24-48h délai)

```
1. Allez sur: https://ads.google.com/aw/conversions
2. Sélectionnez: Alpha Medical Care (128-734-6786)
3. Onglet: "Activité récente" ou "Recent activity"
4. Devrait afficher votre conversion test dans les 24-48 heures
```

---

## COMMANDES RAPIDES

```bash
# Vérifier que GTM est actif sur le site (attendre 2-3 min après push)
python3 check_gtm_status.py

# Devrait afficher:
# ✅ GTM DÉTECTÉ sur le site: GTM-WFPH2KZP
# ✅ dataLayer détecté
```

---

## EN CAS DE PROBLÈME

### Problème: Conversion ID introuvable

**Solution:**
```
1. Allez sur: https://ads.google.com/
2. Outils et paramètres (icône clé) → Mesure → Conversions
3. Cliquez "+ Nouvelle action de conversion"
4. Sélectionnez "Site web"
5. Catégorie: "Achat"
6. Valeur: "Utiliser des valeurs différentes pour chaque conversion"
7. Créez la conversion
8. Puis suivez les étapes ci-dessus pour obtenir les codes
```

### Problème: Variables vides dans GTM

**Solution:**
```
Shopify n'envoie pas toujours les données automatiquement.
Vous devez ajouter du code dans Shopify:

Settings → Checkout → Order status page → Additional scripts

Ajoutez:
<script>
window.dataLayer = window.dataLayer || [];
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'purchase': {
      'actionField': {
        'id': '{{ order.order_number }}',
        'revenue': '{{ order.total_price | money_without_currency }}'
      }
    }
  }
});
</script>

Ensuite, mettez à jour le trigger "Purchase Confirmation Page" dans GTM:
- Événement: purchase (custom event)
- Au lieu de: Page URL contient thank_you
```

---

## RÉSUMÉ

```
✅ GTM installé: GTM-WFPH2KZP
⏳ Conversion ID à obtenir: AW-XXXXXXXXXX + YYYYYYYYY
⏳ Configuration GTM: 15 minutes
⏳ Publication: 2 minutes
⏳ Test: 10 minutes
⏳ Vérification Google Ads: 24-48h

TOTAL: ~30 minutes de travail actif
```

---

**Étape actuelle:** Obtenir Conversion ID depuis Google Ads (fenêtre ouverte)
**Prochaine étape:** Configurer les tags dans GTM
**Status:** 70% complete

---
