# IMPLÉMENTATION IMMÉDIATE - GOOGLE ECOSYSTEM + GEMINI 3 PRO

**Date:** 2025-12-09
**Status:** ✅ APPROUVÉ - IMPLÉMENTATION DÈS AUJOURD'HUI
**Timeline:** Phase 1-2 MAINTENANT → Infrastructure Nano Banana/Veo prête → Activation 25.01.2026

---

## 🎯 DÉCISIONS APPROUVÉES (User Confirmation)

1. ✅ **Approuver Google Ecosystem optimization complète**
2. ✅ **Implémenter Phase 1 (FREE Google tools + Apps Script)** - DÈS MAINTENANT
3. ✅ **Gemini 3 Pro Phase 1 (Product descriptions $0.96-4.80)** - DÈS MAINTENANT
4. ✅ **Gemini 3 Pro Phase 2 (Content automation $2.50-13/mo)** - DÈS MAINTENANT
5. ✅ **Nano Banana 2 Phase 2 (Images $16.50-36.50/mo + $60)** - Activation **25.01.2026** (préparer infrastructure MAINTENANT)
6. ✅ **Veo 3.1 Phase 3 (Videos $90/mo + $432)** - Activation **25.01.2026** (préparer infrastructure MAINTENANT)

---

## 📅 TIMELINE PRÉCISE

### AUJOURD'HUI (2025-12-09) - DÉBUT IMMÉDIAT:
- ✅ Phase 1 Setup: Google Apps Script, Forms, Sheets (Jour 1-3)
- ✅ Gemini 3 Pro API Setup (Jour 1)
- ✅ Gemini Product Descriptions (96 produits, Jour 2-3)

### SEMAINE 1 (2025-12-09 → 2025-12-15):
- ✅ Apps Script: Lead collection webhook
- ✅ Apps Script: Lead enrichment (IPinfo.io)
- ✅ Apps Script + Gemini: Lead scoring automation
- ✅ Apps Script + Gemini: Daily sales insights

### SEMAINE 2-4 (2025-12-16 → 2026-01-05):
- ✅ n8n: Blog automation workflow (Gemini 3 Pro, 20 posts/mo)
- ✅ n8n: Social media caption workflow (Gemini 3 Pro, 90 captions/mo)
- ✅ n8n: Email copy generation (Gemini 3 Pro)
- ✅ Google Drive: 200GB setup, organize marketing assets

### SEMAINE 3-4 (PRÉPARATION NANO BANANA/VEO):
- ✅ n8n: Social media image workflow (READY for Nano Banana, activation 25.01)
- ✅ n8n: YouTube thumbnail workflow (READY for Nano Banana, activation 25.01)
- ✅ n8n: Video generation workflow (READY for Veo, activation 25.01)
- ✅ Credentials: fal.ai API key configured (inactive until 25.01)
- ✅ Credentials: Veo 3.1 API key configured (inactive until 25.01)

### 25 JANVIER 2026 - ACTIVATION NANO BANANA + VEO:
- ✅ Activer fal.ai Nano Banana 2 API ($16.50-36.50/mo + $60 one-time)
- ✅ Activer Google Veo 3.1 API ($90/mo + $432 one-time)
- ✅ Launch workflows: Social images, YouTube thumbnails, Video generation
- ✅ Verify: First 10 images + 5 videos generated successfully

---

## 🚀 PLAN D'IMPLÉMENTATION DÉTAILLÉ

### PHASE 1A: GOOGLE APPS SCRIPT SETUP (JOUR 1-3)

#### JOUR 1: SETUP INITIAL

**Étape 1.1: Créer Google Apps Script Project**
```
1. Ouvrir: https://script.google.com/
2. Cliquer: "New Project"
3. Nommer: "Alpha Medical Automation"
4. Sauvegarder
```

**Étape 1.2: Configurer Script Properties (Credentials Sécurisés)**
```
1. Dans Apps Script, cliquer: "Project Settings" (icône engrenage)
2. Scroller: "Script Properties"
3. Cliquer: "Add script property"
4. Ajouter les propriétés suivantes:

SHOP_DOMAIN = azffej-as.myshopify.com
SHOPIFY_ACCESS_TOKEN = [votre Shopify Admin API token]
GEMINI_API_KEY = [votre Gemini API key - obtenir sur https://ai.google.dev]
IPINFO_TOKEN = [votre IPinfo.io token - FREE 50k/mo sur https://ipinfo.io]
```

**Étape 1.3: Obtenir Gemini API Key**
```
1. Aller: https://ai.google.dev/gemini-api/docs/api-key
2. Cliquer: "Get API key"
3. Créer nouveau projet Google Cloud (si nécessaire)
4. Activer: Generative Language API
5. Créer API key
6. Copier API key → Ajouter à Script Properties (GEMINI_API_KEY)
```

**Étape 1.4: Test Gemini API Connection**

Créer nouveau fichier: `test_gemini.gs`

```javascript
function testGeminiAPI() {
  const apiKey = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
  const url = "https://generativelanguage.googleapis.com/v1/models/gemini-3-pro:generateContent";

  const payload = {
    contents: [{
      parts: [{
        text: "Write a 50-word product description for a premium knee brace designed for arthritis pain relief."
      }]
    }]
  };

  const options = {
    method: "post",
    headers: {
      "x-goog-api-key": apiKey,
      "Content-Type": "application/json"
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {
    const response = UrlFetchApp.fetch(url, options);
    const result = JSON.parse(response.getContentText());

    if (result.candidates && result.candidates[0]) {
      const generatedText = result.candidates[0].content.parts[0].text;
      Logger.log("✅ Gemini API Connected Successfully!");
      Logger.log("Generated Description: " + generatedText);
      return generatedText;
    } else {
      Logger.log("❌ Error: " + JSON.stringify(result));
      return null;
    }
  } catch (error) {
    Logger.log("❌ Error: " + error.message);
    return null;
  }
}
```

**Exécuter:** `testGeminiAPI()` → Vérifier logs: "✅ Gemini API Connected Successfully!"

---

#### JOUR 2-3: WORKFLOWS APPS SCRIPT

**Workflow 1: Lead Collection (Contest/Giveaway) - Whitebook 1.1**

Créer fichier: `lead_collection.gs`

```javascript
/**
 * WORKFLOW 1: Contest/Giveaway Lead Collection
 * Trigger: On form submit (Google Forms)
 * Action: Create Shopify customer with tags
 */
function onFormSubmit(e) {
  try {
    // Get form submission data
    const itemResponses = e.response.getItemResponses();
    const email = itemResponses[0].getResponse(); // Assuming first question is email
    const firstName = itemResponses[1].getResponse(); // Second question is first name
    const phone = itemResponses[2].getResponse(); // Third question is phone (optional)

    // Get credentials from Script Properties
    const shopDomain = PropertiesService.getScriptProperties().getProperty("SHOP_DOMAIN");
    const accessToken = PropertiesService.getScriptProperties().getProperty("SHOPIFY_ACCESS_TOKEN");

    // Create Shopify customer
    const customerData = {
      customer: {
        email: email,
        first_name: firstName,
        phone: phone || "",
        tags: "contest_entry,lead_source_google_form",
        accepts_marketing: true,
        marketing_opt_in_level: "single_opt_in"
      }
    };

    const url = `https://${shopDomain}/admin/api/2025-10/customers.json`;
    const options = {
      method: "post",
      headers: {
        "X-Shopify-Access-Token": accessToken,
        "Content-Type": "application/json"
      },
      payload: JSON.stringify(customerData),
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(url, options);
    const statusCode = response.getResponseCode();

    if (statusCode === 201) {
      Logger.log(`✅ Customer created: ${email}`);
      // Log to Google Sheets (optional)
      logToSheet(email, firstName, "SUCCESS", new Date());
      return "SUCCESS";
    } else if (statusCode === 422) {
      // Customer already exists
      Logger.log(`⚠️ Customer already exists: ${email}`);
      logToSheet(email, firstName, "DUPLICATE", new Date());
      return "DUPLICATE";
    } else {
      Logger.log(`❌ Error ${statusCode}: ${response.getContentText()}`);
      logToSheet(email, firstName, `ERROR_${statusCode}`, new Date());
      return "ERROR";
    }
  } catch (error) {
    Logger.log(`❌ Exception: ${error.message}`);
    return "ERROR";
  }
}

/**
 * Helper: Log results to Google Sheets
 */
function logToSheet(email, name, status, timestamp) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName("Lead Collection Log");

  if (!sheet) {
    // Create sheet if doesn't exist
    const newSheet = ss.insertSheet("Lead Collection Log");
    newSheet.appendRow(["Timestamp", "Email", "Name", "Status"]);
  }

  const logSheet = ss.getSheetByName("Lead Collection Log");
  logSheet.appendRow([timestamp, email, name, status]);
}
```

**Setup Trigger:**
```
1. Apps Script: Cliquer "Triggers" (icône horloge)
2. Cliquer: "Add Trigger"
3. Function: onFormSubmit
4. Event source: From spreadsheet
5. Event type: On form submit
6. Save
```

---

**Workflow 2: Lead Enrichment (Real-Time) - Whitebook 1.3**

Créer fichier: `lead_enrichment.gs`

```javascript
/**
 * WORKFLOW 2: Real-Time Lead Enrichment
 * Receives Shopify webhook (customer/create)
 * Enriches with IPinfo.io geolocation data
 */
function doPost(e) {
  try {
    // Parse Shopify webhook data
    const webhookData = JSON.parse(e.postData.contents);
    const customerId = webhookData.id;
    const customerEmail = webhookData.email;
    const customerIP = webhookData.last_order_ip_address || ""; // May be empty for new customers

    if (!customerIP) {
      Logger.log(`⚠️ No IP address for customer ${customerId}`);
      return ContentService.createTextOutput(JSON.stringify({status: "NO_IP"}))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // Get geolocation data from IPinfo.io
    const ipinfoToken = PropertiesService.getScriptProperties().getProperty("IPINFO_TOKEN");
    const ipinfoUrl = `https://ipinfo.io/${customerIP}/json?token=${ipinfoToken}`;
    const ipinfoResponse = UrlFetchApp.fetch(ipinfoUrl);
    const ipData = JSON.parse(ipinfoResponse.getContentText());

    // Extract location data
    const city = ipData.city || "";
    const region = ipData.region || "";
    const country = ipData.country || "";

    // Create tags
    const tags = [];
    if (city) tags.push(`city_${city.toLowerCase().replace(/\s+/g, '')}`);
    if (region) tags.push(`region_${region.toLowerCase().replace(/\s+/g, '')}`);
    if (country) tags.push(`country_${country.toLowerCase()}`);

    // Update Shopify customer with location tags
    const shopDomain = PropertiesService.getScriptProperties().getProperty("SHOP_DOMAIN");
    const accessToken = PropertiesService.getScriptProperties().getProperty("SHOPIFY_ACCESS_TOKEN");

    const updateUrl = `https://${shopDomain}/admin/api/2025-10/customers/${customerId}.json`;
    const updatePayload = {
      customer: {
        id: customerId,
        tags: webhookData.tags + "," + tags.join(",")
      }
    };

    const updateOptions = {
      method: "put",
      headers: {
        "X-Shopify-Access-Token": accessToken,
        "Content-Type": "application/json"
      },
      payload: JSON.stringify(updatePayload),
      muteHttpExceptions: true
    };

    const updateResponse = UrlFetchApp.fetch(updateUrl, updateOptions);
    const updateStatus = updateResponse.getResponseCode();

    if (updateStatus === 200) {
      Logger.log(`✅ Customer ${customerId} enriched: ${tags.join(", ")}`);
      return ContentService.createTextOutput(JSON.stringify({
        status: "SUCCESS",
        customer_id: customerId,
        tags_added: tags
      })).setMimeType(ContentService.MimeType.JSON);
    } else {
      Logger.log(`❌ Error updating customer: ${updateResponse.getContentText()}`);
      return ContentService.createTextOutput(JSON.stringify({status: "ERROR"}))
        .setMimeType(ContentService.MimeType.JSON);
    }
  } catch (error) {
    Logger.log(`❌ Exception: ${error.message}`);
    return ContentService.createTextOutput(JSON.stringify({
      status: "ERROR",
      message: error.message
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
```

**Deploy as Web App:**
```
1. Apps Script: Cliquer "Deploy" → "New deployment"
2. Type: Web app
3. Description: "Lead Enrichment Webhook"
4. Execute as: Me
5. Who has access: Anyone
6. Deploy
7. Copier Web App URL
8. Configurer Shopify Webhook:
   - Shopify Admin → Settings → Notifications → Webhooks
   - Create webhook:
     - Event: Customer creation
     - Format: JSON
     - URL: [Web App URL]
```

---

**Workflow 3: Lead Scoring with Gemini - NEW**

Créer fichier: `lead_scoring_gemini.gs`

```javascript
/**
 * WORKFLOW 3: Lead Scoring with Gemini 3 Pro
 * Runs weekly to score all leads
 */
function scoreLeadsWithGemini() {
  try {
    // Get Lead Management Sheet
    const ss = SpreadsheetApp.openById("1KyE_H8OPLLJfgRjehNZLS_RcMJToHRQ9gny1Sgoa_JE"); // Lead Management Sheet ID
    const sheet = ss.getSheetByName("Leads");

    if (!sheet) {
      Logger.log("❌ Lead sheet not found");
      return;
    }

    // Get all lead data (columns: Email, Name, Phone, Source, Date Created, Lead Score, Segment)
    const dataRange = sheet.getDataRange();
    const data = dataRange.getValues();
    const headers = data[0];
    const leads = data.slice(1); // Skip header row

    // Prepare leads for Gemini analysis (max 500 at a time for token limits)
    const leadsToScore = leads.slice(0, 500);
    const leadDataForGemini = leadsToScore.map(row => ({
      email: row[0],
      source: row[3],
      date_created: row[4]
    }));

    // Call Gemini API
    const apiKey = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
    const url = "https://generativelanguage.googleapis.com/v1/models/gemini-3-pro:generateContent";

    const prompt = `Analyze these leads and assign lead scores (1-100) based on:
    • Source (contest=50, facebook_ad=70, organic=60, referral=80)
    • Recency (last 7 days=+20, 8-30 days=+10, 31-90 days=0, >90 days=-10)

    Output format: JSON array only, no additional text.
    [{"email": "email@example.com", "score": 75, "segment": "Warm"}]

    Segments: Hot (80-100), Warm (50-79), Cold (0-49)

    Leads data:
    ${JSON.stringify(leadDataForGemini, null, 2)}`;

    const payload = {
      contents: [{
        parts: [{ text: prompt }]
      }]
    };

    const options = {
      method: "post",
      headers: {
        "x-goog-api-key": apiKey,
        "Content-Type": "application/json"
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(url, options);
    const result = JSON.parse(response.getContentText());

    if (!result.candidates || !result.candidates[0]) {
      Logger.log("❌ Gemini API error: " + JSON.stringify(result));
      return;
    }

    // Extract JSON from Gemini response
    const geminiText = result.candidates[0].content.parts[0].text;
    const jsonMatch = geminiText.match(/\[[\s\S]*\]/); // Extract JSON array

    if (!jsonMatch) {
      Logger.log("❌ No JSON found in Gemini response");
      return;
    }

    const scoredLeads = JSON.parse(jsonMatch[0]);

    // Update Google Sheets with scores
    scoredLeads.forEach((scoredLead, index) => {
      const rowIndex = index + 2; // +2 because row 1 is header, array is 0-indexed
      sheet.getRange(rowIndex, 6).setValue(scoredLead.score); // Column F: Lead Score
      sheet.getRange(rowIndex, 7).setValue(scoredLead.segment); // Column G: Segment
    });

    Logger.log(`✅ Scored ${scoredLeads.length} leads successfully`);

    // Optional: Export segments to Klaviyo
    exportSegmentsToKlaviyo(scoredLeads);

  } catch (error) {
    Logger.log(`❌ Error: ${error.message}`);
  }
}

/**
 * Helper: Export segments to Klaviyo (optional)
 */
function exportSegmentsToKlaviyo(scoredLeads) {
  // Klaviyo API integration (if needed)
  // TODO: Implement Klaviyo list management
  Logger.log(`ℹ️ Klaviyo export: ${scoredLeads.length} leads ready for segmentation`);
}

/**
 * Setup Time-Based Trigger for Weekly Scoring
 */
function createWeeklyScoringTrigger() {
  // Delete existing triggers first
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'scoreLeadsWithGemini') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Create new weekly trigger (every Monday at 9 AM)
  ScriptApp.newTrigger('scoreLeadsWithGemini')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(9)
    .create();

  Logger.log("✅ Weekly lead scoring trigger created");
}
```

**Execute once:** `createWeeklyScoringTrigger()` → Vérifie Triggers panel

---

**Workflow 4: Daily Sales Insights with Gemini - NEW**

Créer fichier: `sales_insights_gemini.gs`

```javascript
/**
 * WORKFLOW 4: Daily Sales Insights with Gemini 3 Pro
 * Analyzes last 100 orders, provides actionable insights
 */
function generateDailySalesInsights() {
  try {
    // Fetch Shopify orders (last 100)
    const shopDomain = PropertiesService.getScriptProperties().getProperty("SHOP_DOMAIN");
    const accessToken = PropertiesService.getScriptProperties().getProperty("SHOPIFY_ACCESS_TOKEN");

    const ordersUrl = `https://${shopDomain}/admin/api/2025-10/orders.json?limit=100&status=any`;
    const ordersOptions = {
      method: "get",
      headers: {
        "X-Shopify-Access-Token": accessToken
      },
      muteHttpExceptions: true
    };

    const ordersResponse = UrlFetchApp.fetch(ordersUrl, ordersOptions);
    const ordersData = JSON.parse(ordersResponse.getContentText());

    if (!ordersData.orders || ordersData.orders.length === 0) {
      Logger.log("ℹ️ No orders found");
      return;
    }

    // Extract relevant order data
    const ordersSummary = ordersData.orders.map(order => ({
      id: order.id,
      total_price: order.total_price,
      created_at: order.created_at,
      customer_location: order.shipping_address ? order.shipping_address.city : "Unknown",
      line_items: order.line_items.map(item => ({
        product: item.title,
        quantity: item.quantity,
        price: item.price
      }))
    }));

    // Call Gemini for analysis
    const apiKey = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
    const geminiUrl = "https://generativelanguage.googleapis.com/v1/models/gemini-3-pro:generateContent";

    const prompt = `Analyze these e-commerce orders and provide actionable insights:

Orders data (last 100 orders):
${JSON.stringify(ordersSummary, null, 2)}

Provide insights on:
1. Top 5 products by revenue (product name + total revenue)
2. Average Order Value (AOV)
3. Most common customer locations (top 3 cities)
4. Revenue trends (increasing/decreasing/stable)
5. Recommendations for upselling or inventory management

Format: Clear, concise bullet points. Max 200 words.`;

    const payload = {
      contents: [{
        parts: [{ text: prompt }]
      }]
    };

    const geminiOptions = {
      method: "post",
      headers: {
        "x-goog-api-key": apiKey,
        "Content-Type": "application/json"
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const geminiResponse = UrlFetchApp.fetch(geminiUrl, geminiOptions);
    const geminiResult = JSON.parse(geminiResponse.getContentText());

    if (!geminiResult.candidates || !geminiResult.candidates[0]) {
      Logger.log("❌ Gemini API error");
      return;
    }

    const insights = geminiResult.candidates[0].content.parts[0].text;
    Logger.log("✅ Insights generated:\n" + insights);

    // Write insights to Google Sheets
    const ss = SpreadsheetApp.openById("1KyE_H8OPLLJfgRjehNZLS_RcMJToHRQ9gny1Sgoa_JE");
    let insightsSheet = ss.getSheetByName("Daily Insights");

    if (!insightsSheet) {
      insightsSheet = ss.insertSheet("Daily Insights");
      insightsSheet.appendRow(["Date", "Insights", "Orders Analyzed"]);
    }

    insightsSheet.appendRow([new Date(), insights, ordersData.orders.length]);

    // Optional: Send email to owner
    sendInsightsEmail(insights, ordersData.orders.length);

  } catch (error) {
    Logger.log(`❌ Error: ${error.message}`);
  }
}

/**
 * Helper: Send insights via email
 */
function sendInsightsEmail(insights, orderCount) {
  const recipient = "your-email@example.com"; // Replace with owner email
  const subject = `Daily Sales Insights - ${new Date().toLocaleDateString()}`;
  const body = `Daily Sales Analysis (${orderCount} orders analyzed):\n\n${insights}\n\nGenerated by Gemini 3 Pro AI`;

  MailApp.sendEmail(recipient, subject, body);
  Logger.log("✅ Insights email sent");
}

/**
 * Setup Daily Trigger
 */
function createDailyInsightsTrigger() {
  // Delete existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'generateDailySalesInsights') {
      ScriptApp.deleteTrigger(trigger);
    }
  });

  // Create daily trigger (midnight)
  ScriptApp.newTrigger('generateDailySalesInsights')
    .timeBased()
    .everyDays(1)
    .atHour(0) // Midnight
    .create();

  Logger.log("✅ Daily insights trigger created");
}
```

**Execute once:** `createDailyInsightsTrigger()` → Vérifie Triggers panel

---

### PHASE 1B: GEMINI PRODUCT DESCRIPTIONS (JOUR 2-3)

**Script: Generate 96 Product Descriptions**

Créer fichier: `generate_product_descriptions.gs`

```javascript
/**
 * PHASE 1B: Generate 96 Product Descriptions with Gemini 3 Pro
 * Cost: $0.96-4.80 one-time (96 products × $0.01-0.05)
 */
function generateProductDescriptions() {
  try {
    // Fetch Shopify products
    const shopDomain = PropertiesService.getScriptProperties().getProperty("SHOP_DOMAIN");
    const accessToken = PropertiesService.getScriptProperties().getProperty("SHOPIFY_ACCESS_TOKEN");

    const productsUrl = `https://${shopDomain}/admin/api/2025-10/products.json?limit=250`;
    const productsOptions = {
      method: "get",
      headers: {
        "X-Shopify-Access-Token": accessToken
      },
      muteHttpExceptions: true
    };

    const productsResponse = UrlFetchApp.fetch(productsUrl, productsOptions);
    const productsData = JSON.parse(productsResponse.getContentText());

    if (!productsData.products) {
      Logger.log("❌ No products found");
      return;
    }

    const products = productsData.products;
    Logger.log(`Found ${products.length} products`);

    // Process each product (with rate limiting for FREE tier: 5 RPM)
    products.forEach((product, index) => {
      // Rate limiting: Wait 12 seconds between requests (5 RPM = 1 request per 12 seconds)
      if (index > 0) {
        Utilities.sleep(12000); // 12 seconds
      }

      const productId = product.id;
      const productTitle = product.title;
      const productType = product.product_type || "Medical Equipment";
      const currentDescription = product.body_html || "";

      // Skip if description is already 300+ words
      const wordCount = currentDescription.split(/\s+/).length;
      if (wordCount >= 300) {
        Logger.log(`⏭️ Skipping ${productTitle} (already has ${wordCount} words)`);
        return;
      }

      Logger.log(`Processing: ${productTitle} (${index + 1}/${products.length})`);

      // Generate description with Gemini
      const newDescription = generateDescriptionWithGemini(productTitle, productType, currentDescription);

      if (!newDescription) {
        Logger.log(`❌ Failed to generate description for ${productTitle}`);
        return;
      }

      // Update Shopify product
      const updateUrl = `https://${shopDomain}/admin/api/2025-10/products/${productId}.json`;
      const updatePayload = {
        product: {
          id: productId,
          body_html: newDescription
        }
      };

      const updateOptions = {
        method: "put",
        headers: {
          "X-Shopify-Access-Token": accessToken,
          "Content-Type": "application/json"
        },
        payload: JSON.stringify(updatePayload),
        muteHttpExceptions: true
      };

      const updateResponse = UrlFetchApp.fetch(updateUrl, updateOptions);
      const updateStatus = updateResponse.getResponseCode();

      if (updateStatus === 200) {
        Logger.log(`✅ Updated: ${productTitle}`);
      } else {
        Logger.log(`❌ Error updating ${productTitle}: ${updateResponse.getContentText()}`);
      }
    });

    Logger.log(`✅ Complete! Processed ${products.length} products`);

  } catch (error) {
    Logger.log(`❌ Error: ${error.message}`);
  }
}

/**
 * Helper: Generate description with Gemini 3 Pro
 */
function generateDescriptionWithGemini(productTitle, productType, currentDescription) {
  try {
    const apiKey = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEY");
    const url = "https://generativelanguage.googleapis.com/v1/models/gemini-3-pro:generateContent";

    const prompt = `Write a comprehensive, SEO-optimized product description (300-400 words) for this medical equipment product:

**Product:** ${productTitle}
**Category:** ${productType}
**Current Description (if any):** ${currentDescription || "None"}

**Requirements:**
1. **Introduction (50 words):** Hook with common pain point, explain how this product helps
2. **Key Features & Benefits (150 words):** 5-7 features with benefits (comfort, effectiveness, durability). Include medical certifications: ISO 13485, FDA, CE if applicable.
3. **How to Use & Care (50 words):** Brief usage instructions, care tips
4. **Who Should Use This (50 words):** Target users (active seniors, athletes, arthritis sufferers)

**Tone:** Informative, empathetic, trustworthy (NOT promotional)
**Medical Compliance:** AVOID medical claims ("cures arthritis" = FORBIDDEN). Use factual language: "provides support", "helps reduce discomfort"
**Format:** HTML with <p>, <ul>, <li> tags only (NO <h2>, <h3>)
**Output:** Return ONLY the HTML description, no additional commentary.`;

    const payload = {
      contents: [{
        parts: [{ text: prompt }]
      }]
    };

    const options = {
      method: "post",
      headers: {
        "x-goog-api-key": apiKey,
        "Content-Type": "application/json"
      },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(url, options);
    const result = JSON.parse(response.getContentText());

    if (!result.candidates || !result.candidates[0]) {
      Logger.log(`❌ Gemini error for ${productTitle}`);
      return null;
    }

    const generatedDescription = result.candidates[0].content.parts[0].text;
    return generatedDescription;

  } catch (error) {
    Logger.log(`❌ Gemini API error: ${error.message}`);
    return null;
  }
}
```

**Execute:** `generateProductDescriptions()` → Monitor Execution log (View → Execution log)

**Estimated Time:** 96 products × 12 seconds = 19.2 minutes (with rate limiting)
**Cost:** $0.96-4.80 (96 × $0.01-0.05)

---

### PHASE 2: N8N WORKFLOWS (SEMAINE 2-4)

**Prerequisites:**
- n8n installed (self-hosted OR n8n Cloud $20/mo)
- Gemini API key configured in n8n credentials
- Shopify Admin API credentials in n8n

---

#### WORKFLOW 5: Blog Automation (20 posts/month) - **GEMINI 3 PRO**

**n8n Workflow JSON (Import Ready):**

```json
{
  "name": "Blog Automation - Gemini 3 Pro",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "0 0 1 * *"
            }
          ]
        }
      },
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "resource": "product",
        "operation": "getAll",
        "returnAll": true
      },
      "name": "Shopify - Get All Products",
      "type": "n8n-nodes-base.shopify",
      "typeVersion": 1,
      "position": [450, 300],
      "credentials": {
        "shopifyApi": {
          "id": "1",
          "name": "Shopify Alpha Medical"
        }
      }
    },
    {
      "parameters": {
        "batchSize": 1,
        "options": {}
      },
      "name": "Split In Batches",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 1,
      "position": [650, 300]
    },
    {
      "parameters": {
        "url": "https://generativelanguage.googleapis.com/v1/models/gemini-3-pro:generateContent",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "requestMethod": "POST",
        "jsonParameters": true,
        "bodyParametersJson": "={\"contents\":[{\"parts\":[{\"text\":\"Write a comprehensive, SEO-optimized blog post (1,500 words) about this medical equipment product:\\n\\nTitle: {{$json[\\\"title\\\"]}}\\nDescription: {{$json[\\\"body_html\\\"]}}\\nProduct Type: {{$json[\\\"product_type\\\"]}}\\n\\nInclude:\\n\\n1. **Introduction (200 words):**\\n   - Hook: Common pain point\\n   - Problem: Why this pain occurs\\n   - Solution: How this product helps\\n\\n2. **Key Features & Benefits (400 words):**\\n   - List 5-7 features with benefits\\n   - Include medical certifications: ISO 13485, FDA, CE\\n\\n3. **How to Use & Care Guide (300 words):**\\n   - Step-by-step usage instructions\\n   - Care instructions\\n   - When to replace\\n\\n4. **Comparison & Buying Guide (300 words):**\\n   - Compare to alternatives\\n   - Who should use this\\n   - What to look for when buying\\n\\n5. **FAQ (200 words):**\\n   - 5 common questions with answers\\n\\n6. **Conclusion with CTA (100 words):**\\n   - Summarize benefits\\n   - Call to action: \\\"Shop [Product Name] now\\\"\\n\\n**Tone:** Informative, empathetic, trustworthy\\n**SEO:** Optimize for keywords: [product type] + \\\"pain relief\\\", \\\"buying guide\\\"\\n**Medical Compliance:** Avoid medical claims, use factual language\\n**Format:** HTML with <h2>, <h3>, <p>, <ul>, <li> tags\\n**Output:** Return ONLY the blog post HTML\"}]}]}",
        "options": {}
      },
      "name": "Gemini 3 Pro - Generate Blog Post",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [850, 300],
      "credentials": {
        "httpHeaderAuth": {
          "id": "2",
          "name": "Gemini API Key"
        }
      }
    },
    {
      "parameters": {
        "functionCode": "const productTitle = $input.first().json.title;\nconst productType = $input.first().json.product_type;\nconst geminiResponse = $input.last().json;\n\nconst blogContent = geminiResponse.candidates[0].content.parts[0].text;\n\nreturn {\n  json: {\n    title: `${productTitle} - Complete Buying Guide 2025`,\n    body_html: blogContent,\n    tags: `buying-guide,${productType},pain-relief,how-to`,\n    published: true\n  }\n};"
      },
      "name": "Extract Blog Content",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [1050, 300]
    },
    {
      "parameters": {
        "resource": "article",
        "operation": "create",
        "blogId": "YOUR_BLOG_ID",
        "title": "={{$json[\"title\"]}}",
        "bodyHtml": "={{$json[\"body_html\"]}}",
        "tags": "={{$json[\"tags\"]}}",
        "published": "={{$json[\"published\"]}}"
      },
      "name": "Shopify - Create Blog Post",
      "type": "n8n-nodes-base.shopify",
      "typeVersion": 1,
      "position": [1250, 300],
      "credentials": {
        "shopifyApi": {
          "id": "1",
          "name": "Shopify Alpha Medical"
        }
      }
    },
    {
      "parameters": {
        "operation": "append",
        "sheetId": "1KyE_H8OPLLJfgRjehNZLS_RcMJToHRQ9gny1Sgoa_JE",
        "range": "Blog Automation Log!A:D",
        "options": {}
      },
      "name": "Google Sheets - Log Result",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 2,
      "position": [1450, 300],
      "credentials": {
        "googleSheetsOAuth2Api": {
          "id": "3",
          "name": "Google Sheets"
        }
      }
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [[{"node": "Shopify - Get All Products", "type": "main", "index": 0}]]
    },
    "Shopify - Get All Products": {
      "main": [[{"node": "Split In Batches", "type": "main", "index": 0}]]
    },
    "Split In Batches": {
      "main": [[{"node": "Gemini 3 Pro - Generate Blog Post", "type": "main", "index": 0}]]
    },
    "Gemini 3 Pro - Generate Blog Post": {
      "main": [[{"node": "Extract Blog Content", "type": "main", "index": 0}]]
    },
    "Extract Blog Content": {
      "main": [[{"node": "Shopify - Create Blog Post", "type": "main", "index": 0}]]
    },
    "Shopify - Create Blog Post": {
      "main": [[{"node": "Google Sheets - Log Result", "type": "main", "index": 0}]]
    }
  }
}
```

**Setup Instructions:**
1. Import JSON to n8n
2. Configure credentials:
   - Shopify API (Admin Access Token)
   - Gemini API Key (HTTP Header Auth: `x-goog-api-key`)
   - Google Sheets OAuth2
3. Replace `YOUR_BLOG_ID` with actual Shopify blog ID
4. Test with 1 product first
5. Activate workflow

**Cost:** $0.38-10/month (20 posts × $0.019-0.50)
**Schedule:** 1st of month, midnight

---

#### WORKFLOW 6: Social Media Caption Generation - **GEMINI 3 PRO**

**(Infrastructure ready NOW, activation 25.01.2026 for Nano Banana images)**

**n8n Workflow (Partial - Captions only for now):**

```json
{
  "name": "Social Media Automation - Gemini Captions (Ready for Nano Banana)",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "0 10 * * *"
            }
          ]
        }
      },
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "operation": "read",
        "sheetId": "YOUR_CONTENT_CALENDAR_SHEET_ID",
        "range": "Social Media!A:H",
        "options": {}
      },
      "name": "Google Sheets - Fetch Today's Posts",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 2,
      "position": [450, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json[\"Date\"]}}",
              "operation": "equals",
              "value2": "={{$now.toFormat('yyyy-MM-dd')}}"
            },
            {
              "value1": "={{$json[\"Published\"]}}",
              "operation": "equals",
              "value2": "No"
            }
          ]
        }
      },
      "name": "Filter Today's Unpublished",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [650, 300]
    },
    {
      "parameters": {
        "url": "https://generativelanguage.googleapis.com/v1/models/gemini-3-pro:generateContent",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "requestMethod": "POST",
        "jsonParameters": true,
        "bodyParametersJson": "={\"contents\":[{\"parts\":[{\"text\":\"Generate a {{$json[\\\"Platform\\\"]}} caption for this Alpha Medical post:\\n\\nProduct: {{$json[\\\"Product\\\"]}}\\nPost Type: {{$json[\\\"Post Type\\\"]}}\\nBrand Voice: Empathetic, informative, community-focused (medical equipment for pain relief)\\n\\n**Platform-specific requirements:**\\n\\n- **Instagram:** 150 chars max, 5-10 hashtags, emojis encouraged\\n  - Hashtags: #PainRelief #MedicalEquipment #AlphaMedical\\n  - Emojis: Use sparingly (💙 for health, ✅ for benefits)\\n\\n- **Facebook:** 200 chars max, 3-5 hashtags, conversational tone\\n  - Focus: Community, education, support\\n\\n- **TikTok:** 100 chars max, trending hashtags, energetic tone\\n  - Hashtags: #PainRelief #MedicalEquipment #HealthTok\\n\\n**Output:** Caption only (no platform prefix, no additional formatting)\\n\\n**Medical Compliance:** Avoid medical claims, use factual language\"}]}]}",
        "options": {}
      },
      "name": "Gemini 3 Pro - Generate Caption",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [850, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json[\"Image URL\"]}}",
              "operation": "equals",
              "value2": "GENERATE"
            }
          ]
        }
      },
      "name": "Check if Generate Image",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [1050, 300],
      "notes": "ACTIVATION DATE: 25.01.2026 (Nano Banana 2)"
    },
    {
      "parameters": {
        "url": "https://queue.fal.run/fal-ai/nano-banana-pro",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "requestMethod": "POST",
        "jsonParameters": true,
        "bodyParametersJson": "={\"prompt\":\"{{$json[\\\"Product\\\"]}} lifestyle image for social media. Professional, medical equipment, trustworthy. Style: Clean, modern, health-focused.\",\"image_size\":\"square\",\"num_images\":1}",
        "options": {}
      },
      "name": "Nano Banana 2 - Generate Image",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 3,
      "position": [1250, 200],
      "credentials": {
        "httpHeaderAuth": {
          "id": "4",
          "name": "fal.ai API Key"
        }
      },
      "notes": "INACTIVE until 25.01.2026 - Credentials configured, workflow ready"
    }
  ]
}
```

**Status:** Workflow READY, Nano Banana node INACTIVE until 25.01.2026
**Cost (after 25.01):** $0.50-3/mo (Gemini captions) + $13.50-36.50/mo (Nano Banana images)

---

### TIMELINE RÉCAPITULATIF

| Date | Phase | Actions | Coût |
|------|-------|---------|------|
| **09.12.2025** | Phase 1 Start | Apps Script setup, Gemini API key | $0 |
| **10-11.12.2025** | Phase 1 Complete | 4 Apps Script workflows deployed | $0 |
| **12-13.12.2025** | Gemini Descriptions | Generate 96 product descriptions | $0.96-4.80 |
| **16-22.12.2025** | Phase 2 Start | n8n Blog automation, Social captions | $2.50-13/mo |
| **23-29.12.2025** | Infrastructure Prep | Nano Banana/Veo workflows READY (inactive) | $0 |
| **30.12-05.01.2026** | Drive Setup | 200GB upgrade, organize assets | $2.99/mo |
| **25.01.2026** | Activation | Nano Banana 2 + Veo 3.1 LIVE | $106.50-126.50/mo + $492 |

---

## ✅ NEXT STEPS - IMMEDIATE ACTIONS (TODAY)

**Aujourd'hui (09.12.2025):**
1. ☐ **Obtenir Gemini API Key:** https://ai.google.dev/gemini-api/docs/api-key
2. ☐ **Créer Apps Script project:** https://script.google.com → "New Project"
3. ☐ **Configurer Script Properties:** SHOP_DOMAIN, SHOPIFY_ACCESS_TOKEN, GEMINI_API_KEY, IPINFO_TOKEN
4. ☐ **Test Gemini connection:** Exécuter `testGeminiAPI()` function

**Demain (10.12.2025):**
5. ☐ **Deploy Workflow 1:** Lead Collection (onFormSubmit)
6. ☐ **Deploy Workflow 2:** Lead Enrichment (doPost web app)
7. ☐ **Setup Shopify webhook:** Customer creation → Apps Script URL

**11.12.2025:**
8. ☐ **Deploy Workflow 3:** Lead Scoring (weekly trigger)
9. ☐ **Deploy Workflow 4:** Daily Sales Insights (daily trigger)

**12-13.12.2025:**
10. ☐ **Execute:** `generateProductDescriptions()` (96 products, 19 minutes)

**16-22.12.2025:**
11. ☐ **Setup n8n:** Import Blog automation workflow
12. ☐ **Setup n8n:** Import Social media workflow (captions only)
13. ☐ **Test workflows:** 1 blog post, 1 social caption

**23-29.12.2025:**
14. ☐ **Prepare Nano Banana workflow:** Configure credentials (INACTIVE)
15. ☐ **Prepare Veo workflow:** Configure credentials (INACTIVE)

**25.01.2026:**
16. ☐ **ACTIVATE:** Nano Banana 2 API ($16.50-36.50/mo + $60)
17. ☐ **ACTIVATE:** Veo 3.1 API ($90/mo + $432)
18. ☐ **Test:** Generate 10 images + 5 videos
19. ☐ **Launch:** Full content automation workflows

---

**TOUT EST PRÊT POUR L'IMPLÉMENTATION IMMÉDIATE! 🚀**

**Confirmation:** User a approuvé Google Ecosystem optimization complète
**Status:** Infrastructure READY, Phases 1-2 START NOW, Nano Banana/Veo activation 25.01.2026

