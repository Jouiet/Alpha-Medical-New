# ARCHITECTURE - SYSTÈME AUTO-CRÉATION BUNDLES (GOOGLE SHEETS)

**Date**: 2025-11-15 (Updated)
**Système**: 10+ Propositions Identiques = Auto-Création Automatique
**Storage**: Google Sheets + Apps Script
**Notifications**: Shopify Flow (Native App avec templates existants)

---

## WORKFLOW COMPLET

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLIENT SOUMET PROPOSITION                         │
│   (Sélectionne 3-4 produits via /pages/bundle-creator)              │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│              FRONTEND JAVASCRIPT (bundle-builder-combined.js)        │
│  1. Calcule HASH unique (product_ids triés: "123-456-789")         │
│  2. Soumet via SHOPIFY CONTACT FORM (native):                       │
│     - Email: customer email                                          │
│     - Subject: "Bundle Proposal"                                     │
│     - Body: JSON stringifié {product_ids, hash, email}              │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                 SHOPIFY CONTACT FORM → GMAIL                         │
│  1. Formulaire native Shopify (pas d'API externe)                   │
│  2. Email envoyé à: votre Gmail de support                          │
│  3. Format standardisé pour parsing automatique                     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│              GMAIL → GOOGLE SHEETS (Auto-forwarding)                 │
│  1. Filtre Gmail: "Bundle Proposal"                                 │
│  2. Forward vers: Google Apps Script Email endpoint                 │
│  3. Apps Script parse email → extrait JSON → insère dans Sheet     │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│           GOOGLE SHEETS - STOCKAGE PROPOSITIONS                      │
│  Colonnes:                                                           │
│  | Timestamp | Email | Hash | Product_IDs | Product_Handles | Count |│
│  |-----------|-------|------|-------------|-----------------|-------|│
│  | 2025-11   | a@... | abc1 | [123,456]   | [knee, ankle]  | 5     |│
│  | 2025-11   | b@... | abc1 | [123,456]   | [knee, ankle]  | 5     |│
│  | 2025-11   | c@... | xyz9 | [789,012]   | [back, neck]   | 2     |│
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│         GOOGLE APPS SCRIPT - AGRÉGATION + AUTO-CRÉATION             │
│  Trigger: onFormSubmit (chaque nouvelle ligne)                      │
│                                                                      │
│  1. Lire nouveau row (email, hash, product_ids)                     │
│  2. Compter proposals identiques (COUNTIF hash)                     │
│  3. Si count >= 10 ET bundle pas encore créé:                       │
│     ├─ Fetch product details (Shopify Product JSON API)            │
│     ├─ Calculer prix bundle (35% discount)                          │
│     ├─ Créer bundle (Shopify Admin API REST)                        │
│     ├─ Ajouter à collection 296239169613                            │
│     ├─ Tags: auto-created, proposal-{hash}                          │
│     ├─ Metafields: proposal_hash, customer_emails                   │
│     └─ Marquer dans Sheet: "Bundle Created"                         │
│  4. Retour count au client (via webhook optionnel)                  │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│           SHOPIFY FLOW - NOTIFICATIONS AUTOMATIQUES                  │
│  Trigger: Product created avec tag "auto-created"                   │
│  Condition: Product type = "Bundle"                                  │
│  Action:                                                             │
│    1. Lire metafield: auto_bundle.customer_emails (JSON array)      │
│    2. Loop: Pour chaque email dans array                            │
│    3. Send email (TEMPLATE PRÉDÉFINI DANS FLOW):                    │
│       - Subject: "🎉 Your Custom Bundle is Ready - 35% OFF!"        │
│       - Body: Template avec {{product.title}}, {{product.price}}   │
│       - CTA: Shop Bundle → product URL                              │
│  Note: Templates déjà configurés dans Flow (réutiliser existants)  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. POURQUOI GOOGLE SHEETS + APPS SCRIPT?

### ✅ AVANTAGES:

1. **Zero intégration externe** - Google déjà utilisé
2. **Gratuit** - Google Sheets + Apps Script = 100% gratuit
3. **Simple** - Pas de serveur, pas de Vercel, pas de maintenance
4. **Transparent** - Voir toutes propositions en temps réel dans Sheet
5. **Debugging facile** - Logs Apps Script + Sheet visible
6. **Native Shopify** - Contact Form + Flow (outils natifs)
7. **Scalable** - 5M cells Google Sheets = 50,000+ propositions
8. **Flexible** - Modifier logic Apps Script sans redéploiement

### ❌ Approches REJETÉES:

- **Vercel/Serverless**: Intégration externe NON souhaitée
- **Metafields uniquement**: Limite 100 combinaisons, pas transparent
- **Klaviyo**: Templates déjà dans Flow, pas besoin Klaviyo

---

## 2. GOOGLE SHEETS - STRUCTURE

### Spreadsheet: "Bundle Proposals Auto-Creation"

#### **Sheet 1: PROPOSALS** (données brutes)

| Column A   | Column B            | Column C        | Column D            | Column E                | Column F | Column G         |
|------------|---------------------|-----------------|---------------------|-------------------------|----------|------------------|
| Timestamp  | Email               | Hash            | Product_IDs         | Product_Handles         | Count    | Bundle_Created   |
| 2025-11-15 | customer1@email.com | hash_a1b2c3     | [123,456,789]       | [knee,ankle,back]      | 1        | FALSE            |
| 2025-11-15 | customer2@email.com | hash_a1b2c3     | [123,456,789]       | [knee,ankle,back]      | 2        | FALSE            |
| 2025-11-15 | customer3@email.com | hash_xyz789     | [111,222,333]       | [posture,therapy,led]  | 1        | FALSE            |
| ...        | ...                 | ...             | ...                 | ...                     | ...      | ...              |
| 2025-11-15 | customer10@email.com| hash_a1b2c3     | [123,456,789]       | [knee,ankle,back]      | 10       | TRUE             |

**Formules automatiques**:
- **Column F (Count)**: `=COUNTIF($C$2:$C, C2)` - Compte proposals identiques (même hash)
- **Column G (Bundle_Created)**: Mis à jour par Apps Script après création

#### **Sheet 2: BUNDLES_CREATED** (historique bundles auto-créés)

| Hash        | Bundle_ID     | Bundle_Title           | Created_At | Customer_Count | Customer_Emails              |
|-------------|---------------|------------------------|------------|----------------|------------------------------|
| hash_a1b2c3 | 7623087000001 | Custom Bundle #A1B2C3  | 2025-11-15 | 10             | [email1@..., email2@...]     |
| hash_xyz789 | 7623087000002 | Custom Bundle #XYZ789  | 2025-11-16 | 12             | [email3@..., email4@...]     |

---

## 3. FRONTEND MODIFICATION (Contact Form Submission)

### Modifier `assets/bundle-builder-combined.js`:

```javascript
// ============================================================================
// HASH CALCULATION
// ============================================================================

/**
 * Calculate unique hash for product combination
 * Same products in different order = same hash
 */
function calculateProposalHash(productIds) {
  // Sort IDs numerically (ensures deterministic hash)
  const sorted = productIds.slice().sort((a, b) => a - b);

  // Join with delimiter
  const string = sorted.join('-');

  // Simple hash function
  let hash = 0;
  for (let i = 0; i < string.length; i++) {
    const char = string.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }

  // Return hash with prefix
  return `hash_${Math.abs(hash).toString(16).substring(0, 12)}`;
}

// ============================================================================
// SHOPIFY CONTACT FORM SUBMISSION
// ============================================================================

/**
 * Submit proposal via Shopify Contact Form (native)
 */
async function submitProposal() {
  const emailInput = document.getElementById('customer-email');

  if (!emailInput) {
    console.error('[BundleBuilder] Email input not found');
    return;
  }

  const email = emailInput.value.trim();

  if (!email) {
    alert('Please enter your email address');
    return;
  }

  // Validate email
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    alert('Please enter a valid email address');
    return;
  }

  // Get product IDs and handles
  const productIds = selectedProducts.map(p => p.id);
  const productHandles = selectedProducts.map(p => p.handle);

  if (productIds.length < CONFIG.minProducts || productIds.length > CONFIG.maxProducts) {
    alert(`Please select ${CONFIG.minProducts}-${CONFIG.maxProducts} products`);
    return;
  }

  // Calculate hash
  const proposalHash = calculateProposalHash(productIds);

  // Prepare data for contact form
  const proposalData = {
    product_ids: productIds,
    product_handles: productHandles,
    hash: proposalHash,
    email: email,
    timestamp: new Date().toISOString()
  };

  console.log('[BundleBuilder] Submitting proposal:', proposalData);

  // Show loading state
  const submitBtn = document.getElementById('submit-proposal-btn');
  const originalText = submitBtn ? submitBtn.textContent : '';

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
  }

  try {
    // Submit via Shopify Contact Form (NATIVE)
    const formData = new FormData();
    formData.append('contact[email]', email);
    formData.append('contact[subject]', 'Bundle Proposal');
    formData.append('contact[body]', JSON.stringify(proposalData, null, 2));

    const response = await fetch('/contact', {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      handleSubmissionSuccess(proposalData);
    } else {
      handleSubmissionError('Submission failed. Please try again.');
    }

  } catch (error) {
    console.error('[BundleBuilder] Submission error:', error);
    handleSubmissionError('Network error. Please try again.');
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    }
  }
}

/**
 * Handle successful submission
 */
function handleSubmissionSuccess(proposalData) {
  const formContainer = document.getElementById('submission-form-container');

  // Note: We don't know count yet (Google Sheets will process)
  // Show generic success message
  const successMessage = `
    <div class="proposal-recorded-success">
      <div class="success-icon">✅</div>
      <h2>Proposal Submitted!</h2>
      <p>Your custom bundle proposal has been recorded.</p>
      <div class="proposal-info">
        <strong>Products</strong>: ${proposalData.product_handles.join(', ')}
      </div>
      <p class="notification-text">
        If 10+ customers propose this exact combination, the bundle will be
        <strong>automatically created</strong> and you'll receive an email notification.
      </p>
      <button onclick="location.reload()" class="btn-propose-another">
        Propose Another Bundle
      </button>
    </div>
  `;

  if (formContainer) formContainer.innerHTML = successMessage;

  // Clear selected products
  selectedProducts = [];
  updateSelectedDisplay();

  // Track event (Google Analytics)
  if (typeof gtag !== 'undefined') {
    gtag('event', 'bundle_proposal_submitted', {
      proposal_hash: proposalData.hash,
      product_count: proposalData.product_ids.length
    });
  }
}

/**
 * Handle submission error
 */
function handleSubmissionError(errorMessage) {
  const formContainer = document.getElementById('submission-form-container');

  const errorHTML = `
    <div class="proposal-error">
      <div class="error-icon">❌</div>
      <h2>Submission Error</h2>
      <p>${errorMessage}</p>
      <button onclick="location.reload()" class="btn-try-again">Try Again</button>
    </div>
  `;

  if (formContainer) formContainer.innerHTML = errorHTML;
}
```

---

## 4. GOOGLE APPS SCRIPT - AUTO-CRÉATION

### Script attaché à Google Sheets

**File**: `BundleAutoCreation.gs`

```javascript
// ============================================================================
// CONFIGURATION
// ============================================================================

const SHOPIFY_DOMAIN = 'azffej-as.myshopify.com';
const SHOPIFY_ADMIN_ACCESS_TOKEN = 'shpat_xxxxx'; // À configurer
const SHOPIFY_API_VERSION = '2025-10';
const BUNDLE_COLLECTION_ID = 'gid://shopify/Collection/296239169613';
const THRESHOLD = 10; // Auto-create at 10+ proposals

// ============================================================================
// TRIGGER: On Gmail Forward
// ============================================================================

/**
 * Trigger: When Gmail forwards "Bundle Proposal" emails
 * This function is called by Gmail filter → Apps Script webhook
 */
function processIncomingEmail(e) {
  const message = e.message;
  const body = message.getPlainBody();

  // Parse JSON from email body
  try {
    const proposalData = JSON.parse(body);

    // Validate data
    if (!proposalData.email || !proposalData.hash || !proposalData.product_ids) {
      Logger.log('Invalid proposal data: ' + body);
      return;
    }

    // Add to Google Sheet
    addProposalToSheet(proposalData);

  } catch (err) {
    Logger.log('Error parsing email: ' + err.toString());
  }
}

// ============================================================================
// ADD PROPOSAL TO SHEET
// ============================================================================

function addProposalToSheet(proposalData) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PROPOSALS');

  if (!sheet) {
    Logger.log('Sheet PROPOSALS not found');
    return;
  }

  // Append new row
  sheet.appendRow([
    new Date(), // Timestamp
    proposalData.email,
    proposalData.hash,
    JSON.stringify(proposalData.product_ids),
    JSON.stringify(proposalData.product_handles),
    '', // Count (formula will calculate)
    'FALSE' // Bundle_Created
  ]);

  // Count proposals for this hash
  const count = countProposalsForHash(proposalData.hash);

  Logger.log(`Proposal added. Hash: ${proposalData.hash}, Count: ${count}`);

  // Check if threshold reached
  if (count >= THRESHOLD) {
    const bundleCreated = isBundleAlreadyCreated(proposalData.hash);

    if (!bundleCreated) {
      createBundleAuto(proposalData.hash, proposalData.product_ids, proposalData.product_handles);
    } else {
      Logger.log(`Bundle already created for hash: ${proposalData.hash}`);
    }
  }
}

// ============================================================================
// COUNT PROPOSALS FOR HASH
// ============================================================================

function countProposalsForHash(hash) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PROPOSALS');
  const data = sheet.getDataRange().getValues();

  let count = 0;
  for (let i = 1; i < data.length; i++) { // Skip header
    if (data[i][2] === hash) { // Column C: Hash
      count++;
    }
  }

  return count;
}

// ============================================================================
// CHECK IF BUNDLE ALREADY CREATED
// ============================================================================

function isBundleAlreadyCreated(hash) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('BUNDLES_CREATED');
  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) { // Skip header
    if (data[i][0] === hash) { // Column A: Hash
      return true;
    }
  }

  return false;
}

// ============================================================================
// AUTO-CREATE BUNDLE (SHOPIFY ADMIN API)
// ============================================================================

function createBundleAuto(hash, productIds, productHandles) {
  Logger.log(`Auto-creating bundle for hash: ${hash}`);

  // 1. Fetch product details for pricing
  const products = fetchProductsDetails(productIds);

  if (!products || products.length === 0) {
    Logger.log('Failed to fetch product details');
    return;
  }

  // 2. Calculate pricing
  const totalPrice = products.reduce((sum, p) => sum + parseFloat(p.price), 0);
  const bundlePrice = (totalPrice * 0.65).toFixed(2); // 35% OFF

  Logger.log(`Total price: $${totalPrice}, Bundle price: $${bundlePrice}`);

  // 3. Generate bundle title
  const shortHash = hash.replace('hash_', '').substring(0, 6).toUpperCase();
  const bundleTitle = `Custom Bundle #${shortHash}`;
  const bundleHandle = `custom-bundle-${shortHash.toLowerCase()}`;

  // 4. Get customer emails for this hash
  const customerEmails = getCustomerEmailsForHash(hash);

  // 5. Create bundle via Shopify Admin API (REST)
  const url = `https://${SHOPIFY_DOMAIN}/admin/api/${SHOPIFY_API_VERSION}/products.json`;

  const productPayload = {
    product: {
      title: bundleTitle,
      handle: bundleHandle,
      vendor: 'Alpha Medical',
      product_type: 'Bundle',
      tags: ['bundle', 'auto-created', `proposal-${hash}`],
      status: 'active',
      variants: [{
        price: bundlePrice,
        compare_at_price: totalPrice.toFixed(2),
        inventory_policy: 'continue',
        inventory_management: 'shopify',
        inventory_quantity: 100
      }],
      metafields: [
        {
          namespace: 'auto_bundle',
          key: 'proposal_hash',
          type: 'single_line_text_field',
          value: hash
        },
        {
          namespace: 'auto_bundle',
          key: 'customer_emails',
          type: 'json',
          value: JSON.stringify(customerEmails)
        },
        {
          namespace: 'auto_bundle',
          key: 'product_ids',
          type: 'json',
          value: JSON.stringify(productIds)
        }
      ]
    }
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN
    },
    payload: JSON.stringify(productPayload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(url, options);
  const responseCode = response.getResponseCode();
  const responseBody = response.getContentText();

  Logger.log(`Shopify API Response: ${responseCode}`);
  Logger.log(`Response body: ${responseBody}`);

  if (responseCode === 201) {
    const result = JSON.parse(responseBody);
    const bundleId = result.product.id;

    Logger.log(`✅ Bundle created: ID ${bundleId}, Title: ${bundleTitle}`);

    // 6. Add to collection
    addBundleToCollection(bundleId);

    // 7. Record in BUNDLES_CREATED sheet
    recordBundleCreated(hash, bundleId, bundleTitle, customerEmails);

    // 8. Mark proposals as bundle_created = TRUE
    markProposalsAsCreated(hash);

    // 9. Shopify Flow will auto-send emails (triggered by tag "auto-created")

  } else {
    Logger.log(`❌ Failed to create bundle: ${responseBody}`);
  }
}

// ============================================================================
// FETCH PRODUCT DETAILS (Shopify Product JSON API)
// ============================================================================

function fetchProductsDetails(productIds) {
  const products = [];

  for (let productId of productIds) {
    const url = `https://www.alphamedical.shop/products/${productId}.json`;

    try {
      const response = UrlFetchApp.fetch(url);
      const data = JSON.parse(response.getContentText());

      if (data.product) {
        products.push({
          id: data.product.id,
          title: data.product.title,
          handle: data.product.handle,
          price: data.product.variants[0].price
        });
      }
    } catch (err) {
      Logger.log(`Error fetching product ${productId}: ${err.toString()}`);
    }
  }

  return products;
}

// ============================================================================
// GET CUSTOMER EMAILS FOR HASH
// ============================================================================

function getCustomerEmailsForHash(hash) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PROPOSALS');
  const data = sheet.getDataRange().getValues();

  const emails = [];
  for (let i = 1; i < data.length; i++) { // Skip header
    if (data[i][2] === hash) { // Column C: Hash
      emails.push(data[i][1]); // Column B: Email
    }
  }

  return emails;
}

// ============================================================================
// ADD BUNDLE TO COLLECTION
// ============================================================================

function addBundleToCollection(productId) {
  // Extract numeric ID from GID format
  const numericCollectionId = BUNDLE_COLLECTION_ID.split('/').pop();

  const url = `https://${SHOPIFY_DOMAIN}/admin/api/${SHOPIFY_API_VERSION}/collects.json`;

  const payload = {
    collect: {
      product_id: productId,
      collection_id: numericCollectionId
    }
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(url, options);
  Logger.log(`Add to collection response: ${response.getResponseCode()}`);
}

// ============================================================================
// RECORD BUNDLE CREATED
// ============================================================================

function recordBundleCreated(hash, bundleId, bundleTitle, customerEmails) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('BUNDLES_CREATED');

  sheet.appendRow([
    hash,
    bundleId,
    bundleTitle,
    new Date(),
    customerEmails.length,
    JSON.stringify(customerEmails)
  ]);
}

// ============================================================================
// MARK PROPOSALS AS CREATED
// ============================================================================

function markProposalsAsCreated(hash) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PROPOSALS');
  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) { // Skip header
    if (data[i][2] === hash) { // Column C: Hash
      sheet.getRange(i + 1, 7).setValue('TRUE'); // Column G: Bundle_Created
    }
  }
}
```

---

## 5. GMAIL → GOOGLE SHEETS FORWARDING

### Configuration Gmail:

1. **Créer filtre Gmail**:
   - Critère: `subject:"Bundle Proposal"`
   - Action: Forward to → Apps Script email endpoint

2. **Apps Script Webhook** (alternative):
   - Publish Apps Script as Web App
   - Gmail Filter → Forward to webhook URL
   - Apps Script parses POST request

**OU (plus simple)**:

3. **Google Forms Alternative**:
   - Frontend soumet directement à Google Form (au lieu de Contact Form)
   - Apps Script trigger: `onFormSubmit`
   - Plus direct, pas de Gmail intermediaire

**RECOMMANDATION**: Contact Form → Gmail → Apps Script (utilise outils Shopify natifs)

---

## 6. SHOPIFY FLOW - NOTIFICATIONS

### Configuration (Admin → Settings → Apps → Shopify Flow):

**Workflow**: Bundle Auto-Creation Notifications

**Trigger**: Product created
**Condition**: Product tags contains "auto-created"

**Action**:
1. Get data source: Product metafield
   - Namespace: `auto_bundle`
   - Key: `customer_emails`
   - Type: JSON

2. Loop through emails: For each email in customer_emails array

3. Send email:
   - **To**: {{email}} (from loop)
   - **From**: noreply@alphamedical.shop
   - **Subject**: 🎉 Your Custom Bundle is Ready - 35% OFF!

   **Body** (UTILISER TEMPLATE DÉJÀ EXISTANT DANS FLOW):
   ```html
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
         <h2 style="margin: 0 0 10px 0;">{{product.title}}</h2>
         <div style="margin: 20px 0;">
           <span style="text-decoration: line-through; color: #999; font-size: 18px;">
             ${{product.compare_at_price}}
           </span>
           <span style="font-size: 32px; font-weight: 700; color: #4A90E2; margin: 0 10px;">
             ${{product.price}}
           </span>
           <span style="background: #FF6B6B; color: white; padding: 6px 16px; border-radius: 20px; font-weight: 700;">
             35% OFF
           </span>
         </div>
         <a href="https://www.alphamedical.shop/products/{{product.handle}}"
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
   ```

**Note**: Réutiliser templates email déjà configurés dans Flow pour cohérence.

---

## 7. DÉPLOIEMENT

### Étape 1: Créer Google Sheet

```
1. Créer nouveau Google Sheet: "Bundle Proposals Auto-Creation"
2. Créer 2 sheets:
   - PROPOSALS (colonnes A-G)
   - BUNDLES_CREATED (colonnes A-F)
3. Ajouter formule Count: =COUNTIF($C$2:$C, C2) dans colonne F
```

### Étape 2: Apps Script

```
1. Tools → Script editor
2. Copier code BundleAutoCreation.gs
3. Configurer: SHOPIFY_ADMIN_ACCESS_TOKEN
4. Deploy → New deployment → Web app
5. Execute as: Me
6. Who has access: Anyone
7. Copy Web App URL
```

### Étape 3: Gmail Forwarding

```
1. Settings → Filters
2. Create filter: subject:"Bundle Proposal"
3. Forward to: Apps Script email ou webhook
```

### Étape 4: Frontend Update

```
1. Modifier assets/bundle-builder-combined.js
2. Remplacer submission logic par Contact Form
3. Upload vers Shopify (via deploy script)
```

### Étape 5: Shopify Flow

```
1. Admin → Settings → Apps → Shopify Flow
2. Create workflow (voir section 6)
3. Tester avec bundle test
```

---

## 8. TESTING

### Test 1: Submission

1. Aller sur /pages/bundle-creator
2. Sélectionner 3 produits
3. Entrer email
4. Submit
5. Vérifier: Email reçu dans Gmail
6. Vérifier: Nouvelle ligne dans Google Sheet

### Test 2: Auto-création (10+ proposals)

1. Soumettre 10 propositions identiques (différents emails)
2. Vérifier: Apps Script logs
3. Vérifier: Bundle créé dans Shopify Admin
4. Vérifier: Bundle dans collection "Medical Equipment Bundles"
5. Vérifier: Emails envoyés via Shopify Flow

### Test 3: Flow Notifications

1. Créer produit test avec tag "auto-created"
2. Ajouter metafield: customer_emails = ["test@example.com"]
3. Vérifier: Email envoyé automatiquement

---

## 9. MONITORING

### Google Sheet Dashboard:

- **PROPOSALS**: Voir toutes propositions en temps réel
- **Count column**: Voir progressions vers threshold
- **BUNDLES_CREATED**: Historique bundles créés

### Apps Script Logs:

- Executions → View logs
- Vérifier: Proposals received, Auto-creations triggered

### Shopify:

- Products → Filter tag "auto-created"
- Flow → Workflows → View runs
- Check email delivery status

---

## 10. AVANTAGES ARCHITECTURE GOOGLE SHEETS

✅ **Zero intégration externe** (pas de Vercel, pas de serveurs)
✅ **100% gratuit** (Google + Shopify natifs)
✅ **Transparent** (voir toutes données en temps réel)
✅ **Simple debugging** (logs visibles, Sheet éditable)
✅ **Shopify Flow** (utilise templates déjà existants)
✅ **Contact Form** (outil natif Shopify, pas d'API custom)
✅ **Scalable** (5M cells = 50,000+ propositions)
✅ **Maintenance zero** (pas de serveur à gérer)

---

## STATUT: ✅ ARCHITECTURE DÉFINIE - PRÊT POUR IMPLÉMENTATION

**NEXT STEPS**:
1. Créer Google Sheet avec structure définie
2. Créer Apps Script (BundleAutoCreation.gs)
3. Modifier frontend (Contact Form submission)
4. Configurer Gmail forwarding
5. Configurer Shopify Flow
6. Tester workflow complet (10+ proposals)

**DURÉE ESTIMÉE**: 2-3 heures (setup + test + deploy)
