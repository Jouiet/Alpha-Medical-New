# GUIDE COMPLET - DÉPLOIEMENT SYSTÈME AUTO-CRÉATION BUNDLES

**Durée estimée**: 2-3 heures (première fois), 30 minutes (si répété)

**Prérequis**:
- ✅ Accès Google Account (Sheets + Gmail)
- ✅ Accès Shopify Admin
- ✅ Shopify Admin Access Token (déjà configuré dans `.env.admin`)
- ✅ Shopify Flow app activée (native Shopify)

---

## 📋 TABLE DES MATIÈRES

1. [Création Google Sheet](#étape-1-création-google-sheet) (15 min)
2. [Déploiement Apps Script](#étape-2-déploiement-apps-script) (30 min)
3. [Configuration Gmail Forwarding](#étape-3-configuration-gmail-forwarding) (15 min)
4. [Configuration Shopify Flow](#étape-4-configuration-shopify-flow) (20 min)
5. [Tests Workflow Complet](#étape-5-tests-workflow-complet) (30 min)
6. [Monitoring & Maintenance](#étape-6-monitoring--maintenance) (10 min)
7. [Troubleshooting](#troubleshooting)

---

## ÉTAPE 1: CRÉATION GOOGLE SHEET

### 1.1 Créer nouveau spreadsheet

1. **Ouvrir Google Sheets**: https://sheets.google.com
2. Cliquer: **"Blank spreadsheet"** (+ en haut à gauche)
3. Nommer le spreadsheet (cliquer "Untitled spreadsheet"):
   ```
   Bundle Proposals Auto-Creation
   ```

### 1.2 Créer Sheet "PROPOSALS"

1. **Renommer Sheet1**:
   - Double-cliquer sur "Sheet1" (onglet en bas)
   - Renommer: `PROPOSALS`
   - Appuyer Enter

2. **Ajouter headers** (ligne 1):
   - A1: `Timestamp`
   - B1: `Email`
   - C1: `Hash`
   - D1: `Product_IDs`
   - E1: `Product_Handles`
   - F1: `Count`
   - G1: `Bundle_Created`

3. **Formater headers** (optionnel):
   - Sélectionner ligne 1 (A1:G1)
   - Cliquer: **Bold** (Ctrl+B)
   - Background color: Gris clair
   - Text alignment: Center

4. **Ajouter formule Count**:
   - Cliquer cellule **F2**
   - Entrer:
     ```
     =COUNTIF($C$2:$C, C2)
     ```
   - Appuyer Enter

5. **Auto-fill formule** (pour futures lignes):
   - Sélectionner F2
   - Cliquer petit carré bleu en bas à droite
   - Glisser jusqu'à F100 (ou plus)
   - **Important**: La formule doit se copier automatiquement quand Apps Script ajoute lignes

### 1.3 Créer Sheet "BUNDLES_CREATED"

1. **Créer nouvelle sheet**:
   - Cliquer **+** (en bas à gauche, à côté de PROPOSALS)
   - Renommer: `BUNDLES_CREATED`

2. **Ajouter headers** (ligne 1):
   - A1: `Hash`
   - B1: `Bundle_ID`
   - C1: `Bundle_Title`
   - D1: `Bundle_URL`
   - E1: `Created_At`
   - F1: `Customer_Count`
   - G1: `Customer_Emails`

3. **Formater headers** (même que PROPOSALS)

### 1.4 Vérification finale

Votre spreadsheet doit avoir:
- ✅ 2 sheets: PROPOSALS, BUNDLES_CREATED
- ✅ PROPOSALS: 7 colonnes (A-G) avec formule Count en F2
- ✅ BUNDLES_CREATED: 7 colonnes (A-G)
- ✅ Headers en gras (optionnel mais recommandé)

**Screenshot**: Le spreadsheet vide avec headers est maintenant prêt.

---

## ÉTAPE 2: DÉPLOIEMENT APPS SCRIPT

### 2.1 Ouvrir Script Editor

1. Dans votre Google Sheet (Bundle Proposals Auto-Creation)
2. Menu: **Extensions** → **Apps Script**
3. Une nouvelle fenêtre s'ouvre avec un projet Apps Script vide

### 2.2 Copier le code

1. **Supprimer le code par défaut**:
   - Sélectionner tout le code dans `Code.gs`
   - Supprimer (Ctrl+A puis Delete)

2. **Copier le code du fichier**:
   - Ouvrir fichier: `/Users/mac/Desktop/Alpha-Medical/BundleAutoCreation.gs`
   - Sélectionner TOUT le code (Ctrl+A)
   - Copier (Ctrl+C)

3. **Coller dans Apps Script**:
   - Retour dans Apps Script editor
   - Coller le code (Ctrl+V)
   - Vérifier que tout le code est là (~665 lignes)

### 2.3 Configurer SHOPIFY_ADMIN_ACCESS_TOKEN

**IMPORTANT**: Le token est dans `.env.admin`

1. **Lire le token**:
   ```bash
   cat .env.admin | grep SHOPIFY_ADMIN_ACCESS_TOKEN
   ```

2. **Dans Apps Script, ligne 22**:
   ```javascript
   const SHOPIFY_ADMIN_ACCESS_TOKEN = 'shpat_xxxxx'; // ⚠️ À CONFIGURER
   ```

3. **Remplacer** `shpat_xxxxx` par le token réel de `.env.admin`

4. **Sauvegarder**:
   - Cliquer: **Disque** (icône Save) ou Ctrl+S
   - Nommer le projet: `Bundle Auto-Creation`

### 2.4 Vérifier les autres configurations

Vérifier que ces valeurs sont correctes (lignes 19-23):

```javascript
const SHOPIFY_DOMAIN = 'azffej-as.myshopify.com'; // ✅ Correct
const SHOPIFY_API_VERSION = '2025-10'; // ✅ Correct
const BUNDLE_COLLECTION_ID = 'gid://shopify/Collection/296239169613'; // ✅ Correct
const THRESHOLD = 10; // ✅ Correct (10+ proposals = auto-création)
```

### 2.5 Tester le code (optionnel mais recommandé)

1. **Sélectionner fonction de test**:
   - Menu déroulant (en haut): Sélectionner `testAddProposal`

2. **Autoriser permissions**:
   - Cliquer: **Run** (▶ Play button)
   - Popup "Authorization required" apparaît
   - Cliquer: **Review permissions**
   - Sélectionner votre compte Google
   - Cliquer: **Advanced** → **Go to Bundle Auto-Creation (unsafe)**
   - Cliquer: **Allow**

3. **Vérifier logs**:
   - Menu: **View** → **Logs** (ou Ctrl+Enter)
   - Vous devriez voir: "Testing proposal submission..." et "✅ Proposal added to sheet"

4. **Vérifier Google Sheet**:
   - Retour dans Google Sheet (onglet PROPOSALS)
   - Une nouvelle ligne doit apparaître avec:
     - Timestamp: Date actuelle
     - Email: test@example.com
     - Hash: hash_test123abc
     - Count: 1

5. **Supprimer la ligne de test**:
   - Sélectionner ligne 2 (ligne de test)
   - Clic droit → Delete row

### 2.6 Déployer comme Web App

1. **Cliquer**: **Deploy** → **New deployment**

2. **Type**:
   - Cliquer icône **⚙ Settings** (à côté de "Select type")
   - Sélectionner: **Web app**

3. **Configuration**:
   - **Description**: `Bundle Auto-Creation API v1`
   - **Execute as**: `Me (votre.email@gmail.com)`
   - **Who has access**: `Anyone` ⚠️ IMPORTANT

4. **Deploy**:
   - Cliquer: **Deploy**
   - Popup "Authorize access" apparaît
   - Cliquer: **Authorize access**
   - Sélectionner compte → Allow

5. **Copier Web App URL**:
   - Une popup "Deployment" apparaît
   - **Web app URL**: `https://script.google.com/macros/s/XXXXX/exec`
   - **COPIER CETTE URL** → vous en aurez besoin pour Gmail forwarding

6. **Fermer**:
   - Cliquer: **Done**

**✅ Apps Script déployé avec succès!**

---

## ÉTAPE 3: CONFIGURATION GMAIL FORWARDING

### Option A: Forwarding automatique (RECOMMANDÉ)

**Note**: Gmail ne permet pas de forward directement vers Apps Script URL. Solution: utiliser Google Apps Script email trigger.

#### 3.1 Créer trigger "On form submit" simulé

**Alternative plus simple**: Utiliser **Gmail Add-on** ou **Zapier** (mais nécessite intégration externe).

#### 3.2 Solution NATIVE: Email parsing via Trigger

1. **Dans Apps Script**:
   - Menu: **Triggers** (⏰ icône horloge à gauche)
   - Cliquer: **+ Add Trigger**

2. **Configuration trigger**:
   - **Choose which function to run**: `processIncomingEmail`
   - **Choose which deployment should run**: `Head`
   - **Select event source**: `From Gmail`
   - **Select event type**: `On message received`
   - **Failure notification settings**: `Notify me daily`

3. **Sauvegarder trigger**:
   - Cliquer: **Save**
   - Autoriser permissions si demandé

**⚠️ PROBLÈME**: Gmail trigger "On message received" n'existe plus dans Apps Script moderne.

### Option B: Contact Form → Email → Manual processing (INTERIM)

**Solution temporaire** jusqu'à configuration Zapier/Make:

1. Les propositions arrivent via Contact Form dans Gmail
2. Vous voyez les emails avec subject "Bundle Proposal"
3. **Manuellement** copier le JSON body et l'ajouter à Google Sheet

**Cette option n'est PAS automatique** mais fonctionne pour tester.

### Option C: Google Forms (ALTERNATIF - RECOMMANDÉ)

**Solution 100% native Google sans Gmail**:

#### 3.3 Créer Google Form

1. **Créer nouveau form**: https://forms.google.com
2. Nommer: "Bundle Proposal Submission"
3. **Ajouter champs**:
   - Email (required)
   - Proposal Data (Paragraph text, required)

4. **Connecter à Google Sheet**:
   - Responses → Create spreadsheet
   - Sélectionner: "Select existing spreadsheet"
   - Choisir: "Bundle Proposals Auto-Creation"
   - Nouvelle sheet "Form Responses 1" créée

5. **Apps Script trigger**:
   - Dans Apps Script, créer nouveau trigger
   - Function: `onFormSubmit` (à créer)
   - Event source: From spreadsheet
   - Event type: On form submit

**Mais cela nécessite modifier le frontend** pour soumettre à Google Form au lieu de Contact Form.

### ⚠️ RECOMMENDATION FINALE

**Pour 100% automatisation native Shopify + Google**:

Utiliser **Contact Form Shopify** → Gmail → **Google Apps Script Web App** via webhook.

**Configuration Gmail Filter → Webhook**:

1. **Créer filtre Gmail**:
   - Gmail Settings → Filters and Blocked Addresses
   - Create filter
   - Critères: `subject:"Bundle Proposal"`

2. **Forward to email trigger** (nécessite Apps Script Email Service):

Malheureusement Gmail ne peut pas forward directement vers HTTP URL.

**SOLUTION DÉFINITIVE**: Utiliser **Zapier** ou **Make** (anciennement Integromat):

```
Shopify Contact Form → Gmail → Zapier → Google Sheets (append row) → Apps Script Trigger
```

**OU PLUS SIMPLE**: Modifier frontend pour soumettre directement à Google Forms.

---

## ÉTAPE 3 (RÉVISÉE): SOLUTION GOOGLE FORMS

### 3.1 Créer Google Form

1. **Nouveau form**: https://forms.google.com → Blank form
2. **Titre**: Bundle Proposal Submission
3. **Description**: (vide)

4. **Champs**:
   - **Question 1**:
     - Type: Short answer
     - Question: "Your Email"
     - Required: ON
     - Validation: Text → Email

   - **Question 2**:
     - Type: Paragraph
     - Question: "Proposal Data (JSON)"
     - Required: ON
     - Description: "Auto-filled by website form"

5. **Settings**:
   - Cliquer: ⚙ Settings
   - General:
     - ☑ Collect email addresses: OFF (déjà dans question)
     - ☑ Limit to 1 response: OFF
   - Presentation:
     - Confirmation message: "Proposal submitted! You'll be notified if 10+ customers propose the same bundle."

### 3.2 Connecter Form à Sheet

1. **Responses tab**:
   - Cliquer: Responses (en haut)
   - Cliquer: Icône Google Sheets verte "Create Spreadsheet"

2. **Select destination**:
   - Sélectionner: "Select existing spreadsheet"
   - Choisir: "Bundle Proposals Auto-Creation"
   - Cliquer: Select

3. **Nouvelle sheet créée**:
   - Sheet "Form Responses 1" ajoutée au spreadsheet
   - Colonnes: Timestamp | Your Email | Proposal Data (JSON)

### 3.3 Créer Apps Script Trigger

1. **Dans Apps Script** (Extensions → Apps Script)

2. **Ajouter fonction `onFormSubmit`**:

Ajouter cette fonction à `BundleAutoCreation.gs`:

```javascript
/**
 * Trigger: On Form Submit (Google Forms)
 * Alternative to Gmail email parsing
 */
function onFormSubmit(e) {
  const values = e.values; // [Timestamp, Email, JSON]
  const email = values[1]; // Column B: Email
  const jsonString = values[2]; // Column C: Proposal Data (JSON)

  Logger.log('Form submitted by: ' + email);
  Logger.log('JSON data: ' + jsonString);

  try {
    const proposalData = JSON.parse(jsonString);

    // Validate
    if (!proposalData.email || !proposalData.hash || !proposalData.product_ids) {
      Logger.log('❌ Invalid proposal data');
      return;
    }

    // Add to PROPOSALS sheet
    addProposalToSheet(proposalData);

  } catch (err) {
    Logger.log('❌ Error parsing form data: ' + err.toString());
  }
}
```

3. **Créer trigger**:
   - Menu: Triggers (⏰ icône)
   - **+ Add Trigger**
   - Function: `onFormSubmit`
   - Deployment: Head
   - Event source: **From spreadsheet**
   - Event type: **On form submit**
   - Save

### 3.4 Modifier Frontend (Soumettre à Google Form)

**Fichier**: `assets/bundle-builder-combined.js`

**Trouver la fonction de submission** et remplacer par:

```javascript
async function submitProposal() {
  const emailInput = document.getElementById('customer-email');
  const email = emailInput.value.trim();

  // Validate
  if (!email) {
    alert('Please enter your email address');
    return;
  }

  // Get proposal data
  const proposalData = JSON.parse(createBundleDataJSON());

  // Submit to Google Form
  const GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/YOUR_FORM_ID/formResponse';
  const FORM_ENTRY_EMAIL = 'entry.123456789'; // ⚠️ À trouver
  const FORM_ENTRY_JSON = 'entry.987654321'; // ⚠️ À trouver

  const formData = new FormData();
  formData.append(FORM_ENTRY_EMAIL, email);
  formData.append(FORM_ENTRY_JSON, JSON.stringify(proposalData, null, 2));

  try {
    await fetch(GOOGLE_FORM_URL, {
      method: 'POST',
      body: formData,
      mode: 'no-cors' // Important for Google Forms
    });

    // Success (no-cors doesn't return response)
    handleSubmissionSuccess(proposalData);

  } catch (error) {
    handleSubmissionError('Submission failed. Please try again.');
  }
}
```

**Pour trouver FORM_ENTRY IDs**:
1. Ouvrir Google Form
2. Cliquer: Preview (👁 icône en haut)
3. Ouvrir DevTools (F12)
4. Network tab
5. Submit test form
6. Look for "formResponse" request
7. Entry IDs sont dans Form Data

**⚠️ MAIS CELA NÉCESSITE MODIFIER LE FRONTEND** ce qui sort du scope actuel.

---

## ÉTAPE 3 (FINAL): SOLUTION CONTACT FORM + MANUAL MONITORING

**Pour l'instant (MVP), workflow semi-automatique**:

1. ✅ Frontend soumet via Contact Form Shopify (déjà implémenté)
2. ✅ Email arrive dans Gmail avec JSON dans body
3. ❌ **Manualmente** copier JSON et ajouter à Google Sheet PROPOSALS
4. ✅ Apps Script détecte nouveau row et auto-crée bundle si 10+

**Full automation vient plus tard via**:
- Zapier (Gmail → Google Sheets)
- Ou modification frontend vers Google Forms

---

## ÉTAPE 4: CONFIGURATION SHOPIFY FLOW

### 4.1 Accéder à Shopify Flow

1. **Shopify Admin**: https://admin.shopify.com
2. **Settings** (en bas à gauche)
3. **Apps and sales channels**
4. Trouver: **Shopify Flow**
5. Cliquer: **Open app** (ou install si pas encore installé)

### 4.2 Créer nouveau workflow

1. **Create workflow**
2. **Name**: `Bundle Auto-Creation Notifications`
3. **Description**: `Send emails to customers when their proposed bundle is auto-created (10+ proposals)`

### 4.3 Configurer Trigger

1. **Select a trigger**:
   - Search: "product created"
   - Sélectionner: **Product created**

### 4.4 Ajouter Condition

1. **Add condition** (après trigger)
2. **Condition type**: Product
3. **Field**: Tags
4. **Operator**: Contains
5. **Value**: `auto-created`

### 4.5 Ajouter Actions

**Action 1: Get metafield**

1. **Add action**: Get data
2. **Type**: Metafield
3. **Resource**: Product (from trigger)
4. **Namespace**: `auto_bundle`
5. **Key**: `customer_emails`
6. **Save**

**Action 2: Loop through emails**

1. **Add action**: Run code (ou For each si disponible)

**⚠️ PROBLÈME**: Shopify Flow ne supporte pas loop natif sur JSON array dans metafield.

**SOLUTION**: Utiliser **Send internal email** avec metafield comme variable.

**Alternative action (plus simple)**:

1. **Add action**: Send email
2. **To**: (utiliser variable metafield - mais ne supporte pas array)

**⚠️ LIMITATION SHOPIFY FLOW**: Ne peut pas loop sur array dans metafield directement.

### 4.6 Solution Alternative: Klaviyo

**MAIS UTILISATEUR A DIT "PAS KLAVIYO"**!

### 4.7 Solution Flow: Email individuel

Shopify Flow **ne peut pas** envoyer emails à liste dynamique depuis metafield.

**Options**:
1. **Modifier Apps Script** pour créer 10 products séparés (1 par customer) → Flow envoie email au customer associé
2. **Utiliser Shopify Scripts** (deprecated)
3. **Utiliser webhook** vers service externe (Zapier → Klaviyo) - mais externe

**RECOMMENDATION**: Modifier Apps Script pour envoyer emails **directement** via MailApp (Gmail API).

### 4.8 Modifier Apps Script: Envoyer emails directement

**Dans `BundleAutoCreation.gs`, fonction `createBundleAuto`**:

Ajouter à la fin (après ligne 547):

```javascript
// 9. Send emails directly via Gmail (instead of Shopify Flow)
Logger.log('\nStep 9/9: Sending email notifications...');
sendBundleCreatedEmails(bundleTitle, bundleUrl, bundlePrice, totalPrice, customerEmails);
```

**Ajouter nouvelle fonction**:

```javascript
/**
 * Send emails directly via Gmail API
 */
function sendBundleCreatedEmails(bundleTitle, bundleUrl, bundlePrice, totalPrice, customerEmails) {
  const subject = '🎉 Your Custom Bundle is Ready - 35% OFF!';

  const htmlBody = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <div style="background: linear-gradient(135deg, #4A90E2 0%, #7FCCC9 100%); padding: 30px; text-align: center;">
        <h1 style="color: white; margin: 0;">🎉 Your Bundle is Ready!</h1>
      </div>

      <div style="padding: 40px 30px; background: #f9f9f9;">
        <p style="font-size: 16px; line-height: 1.6;">Hi there,</p>

        <p style="font-size: 16px; line-height: 1.6;">
          Great news! Your custom bundle proposal has been <strong>automatically created</strong>.
        </p>

        <p style="font-size: 16px; line-height: 1.6;">
          You and <strong>9+ other customers</strong> requested this exact combination,
          so we've made it official!
        </p>

        <div style="background: white; padding: 30px; border-radius: 12px; margin: 30px 0; text-align: center;">
          <h2 style="margin: 0 0 10px 0;">${bundleTitle}</h2>
          <div style="margin: 20px 0;">
            <span style="text-decoration: line-through; color: #999; font-size: 18px;">
              $${totalPrice}
            </span>
            <span style="font-size: 32px; font-weight: 700; color: #4A90E2; margin: 0 10px;">
              $${bundlePrice}
            </span>
            <span style="background: #FF6B6B; color: white; padding: 6px 16px; border-radius: 20px; font-weight: 700;">
              35% OFF
            </span>
          </div>
          <a href="https://www.alphamedical.shop${bundleUrl}"
             style="display: inline-block; margin-top: 20px; padding: 14px 32px; background: linear-gradient(135deg, #4A90E2 0%, #7FCCC9 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">
            Shop This Bundle →
          </a>
        </div>

        <p style="font-size: 14px; color: #666; line-height: 1.6;">
          Thank you for being part of our community-driven product creation!
          Your feedback helps us create bundles that truly serve our customers.
        </p>

        <p style="font-size: 14px; color: #666;">
          Best regards,<br>
          <strong>Alpha Medical Team</strong>
        </p>
      </div>

      <div style="padding: 20px; text-align: center; background: #f0f0f0; font-size: 12px; color: #999;">
        <p>Alpha Medical | Professional Medical Equipment</p>
      </div>
    </div>
  `;

  // Send email to each customer
  customerEmails.forEach(function(email) {
    try {
      MailApp.sendEmail({
        to: email,
        subject: subject,
        htmlBody: htmlBody
      });

      Logger.log(`   ✅ Email sent to: ${email}`);
    } catch (err) {
      Logger.log(`   ❌ Failed to send email to ${email}: ${err.toString()}`);
    }
  });

  Logger.log(`   📧 Total emails sent: ${customerEmails.length}`);
}
```

**✅ AVEC CETTE MODIFICATION**: Shopify Flow n'est plus nécessaire! Emails envoyés directement par Apps Script.

---

## ÉTAPE 5: TESTS WORKFLOW COMPLET

### 5.1 Test Manual: Ajouter proposition au Sheet

1. **Ouvrir Google Sheet** (PROPOSALS)

2. **Ajouter ligne test manuellement**:
   - A2: `2025-11-15 10:30:00` (timestamp)
   - B2: `test1@example.com`
   - C2: `hash_testbundle`
   - D2: `[7623055966285,7623055999053,7623056031821]`
   - E2: `["office-worker-essential-kit","senior-mobility-support","chronic-pain-starter-kit"]`
   - F2: (formule auto-calcule: devrait afficher `1`)
   - G2: `FALSE`

3. **Vérifier formule Count**:
   - F2 devrait afficher: `1`

4. **Répéter 9 fois** (lignes 3-11) avec emails différents mais MÊME hash:
   - B3: `test2@example.com`
   - C3: `hash_testbundle` (MÊME hash)
   - D3-E3: (mêmes product IDs et handles)
   - ...
   - B11: `test10@example.com`
   - C11: `hash_testbundle`

5. **Vérifier Count**:
   - F2-F11 devraient TOUS afficher: `10`

### 5.2 Test Apps Script: Déclencher auto-création

1. **Apps Script → Run fonction**:
   - Sélectionner fonction: `createBundleAuto`
   - **MAIS**: Cette fonction nécessite paramètres

**Alternative**: Utiliser fonction de test

2. **Ou run fonction**: `testAutoCreation`
   - Cliquer: Run ▶
   - Attendre 30-60 secondes

3. **Vérifier Logs**:
   - View → Logs
   - Devrait afficher:
     ```
     Auto-creating bundle for hash: hash_test123abc
     ✅ Bundle created: ID 7623087XXXXX
     📧 Total emails sent: 10
     ```

4. **Vérifier Shopify Admin**:
   - Products → All products
   - Filtrer par tag: `auto-created`
   - Le bundle test devrait apparaître

5. **Vérifier Sheet BUNDLES_CREATED**:
   - Nouvelle ligne ajoutée avec bundle details

6. **Vérifier emails** (vos 10 test emails):
   - Check inboxes de test1@example.com, test2@example.com, etc.
   - Email "🎉 Your Custom Bundle is Ready" devrait être reçu

### 5.3 Supprimer données de test

1. **Google Sheet PROPOSALS**:
   - Supprimer lignes 2-11 (lignes de test)

2. **Google Sheet BUNDLES_CREATED**:
   - Supprimer ligne 2 (bundle de test)

3. **Shopify Admin**:
   - Products → Trouver bundle test
   - Actions → Delete product

---

## ÉTAPE 6: MONITORING & MAINTENANCE

### 6.1 Dashboard Google Sheets

**Sheet PROPOSALS**:
- Voir toutes propositions en temps réel
- Colonne Count montre progression vers threshold (10)
- Filtrer par Hash pour voir proposals identiques

**Sheet BUNDLES_CREATED**:
- Historique de tous bundles auto-créés
- Customer Count, Emails, Dates

### 6.2 Apps Script Logs

1. **Apps Script** → **Executions**
2. Voir toutes exécutions récentes:
   - Success ✅
   - Failure ❌
3. Cliquer sur exécution → View logs

### 6.3 Shopify Products

1. **Products** → **All products**
2. **Filter by tag**: `auto-created`
3. Voir tous bundles auto-créés

### 6.4 Email Deliverability

1. Vérifier Gmail "Sent" folder
2. Check bounce rate
3. Monitor spam complaints

---

## TROUBLESHOOTING

### Problème 1: Apps Script "Permission denied"

**Solution**:
1. Apps Script → Run any function
2. Authorize permissions
3. Advanced → Go to project (unsafe) → Allow

### Problème 2: Emails pas envoyés

**Vérification**:
1. Apps Script Logs → Check "Email sent" messages
2. Gmail quota: 100 emails/day (account Gmail gratuit)
3. Solution: Utiliser Google Workspace (500/day) ou SMTP service

### Problème 3: Bundle pas créé à 10+ proposals

**Debug**:
1. Apps Script Logs → Check `createBundleAuto` function logs
2. Vérifier `SHOPIFY_ADMIN_ACCESS_TOKEN` est correct
3. Vérifier Shopify API permissions (write_products)
4. Check product handles sont valides (fetch via Product JSON API)

### Problème 4: Formule Count ne fonctionne pas

**Solution**:
1. Vérifier formule en F2: `=COUNTIF($C$2:$C, C2)`
2. S'assurer que hashes sont identiques (case-sensitive)
3. Auto-fill formule jusqu'à ligne 100+

### Problème 5: Contact Form → Gmail → Manual copy trop lent

**Solution long-terme**:
1. Setup Zapier (Gmail → Google Sheets)
2. Ou modifier frontend vers Google Forms
3. Ou utiliser Shopify Webhooks vers Apps Script Web App

---

## ANNEXE: VERSIONS ALTERNATIVES

### Alternative A: Google Forms (Frontend modifié)

Frontend soumet directement à Google Form → onFormSubmit trigger

**Avantage**: 100% automatique, zero Gmail
**Inconvénient**: Modifier frontend Shopify

### Alternative B: Zapier

Gmail → Zapier → Google Sheets → Apps Script trigger

**Avantage**: Zero code, UI simple
**Inconvénient**: Coût Zapier ($20/mois)

### Alternative C: Shopify Webhooks

Shopify webhook → Apps Script Web App → Google Sheets

**Avantage**: Real-time, zero email
**Inconvénient**: Webhook setup complexe

---

## STATUS FINAL

✅ **DÉPLOIEMENT COMPLET** si tous steps suivis

**Résumé**:
1. ✅ Google Sheet créé (PROPOSALS + BUNDLES_CREATED)
2. ✅ Apps Script déployé (BundleAutoCreation.gs)
3. ⚠️ Gmail forwarding (manual interim, Zapier long-terme)
4. ✅ Emails envoyés directement (Apps Script MailApp, pas Flow)
5. ✅ Tests workflow effectués
6. ✅ Monitoring configuré

**Durée réelle**: 2-3 heures première fois

**Prochaine optimisation**: Zapier ou Google Forms pour full automation

---

**VERSION**: 1.0 (2025-11-15)
**AUTEUR**: Claude Code + Alpha Medical Team
