// ============================================================================
// GOOGLE APPS SCRIPT - BUNDLE AUTO-CREATION SYSTEM
// ============================================================================
//
// Description:
//   Automate bundle creation when 10+ identical proposals are received
//   via Shopify Contact Form → Gmail → Google Sheets
//
// Deployment:
//   1. Create Google Sheet: "Bundle Proposals Auto-Creation"
//   2. Create 2 sheets: PROPOSALS, BUNDLES_CREATED
//   3. Tools → Script editor → Paste this code
//   4. Set SHOPIFY_ADMIN_ACCESS_TOKEN in configuration
//   5. Deploy → New deployment → Web app (Anyone can access)
//   6. Configure Gmail filter to forward "Bundle Proposal" emails
//
// ============================================================================

// ============================================================================
// CONFIGURATION
// ============================================================================

const SHOPIFY_DOMAIN = 'azffej-as.myshopify.com';
const SHOPIFY_ADMIN_ACCESS_TOKEN = 'shpat_xxxxx'; // ⚠️ À CONFIGURER
const SHOPIFY_API_VERSION = '2025-10';
const BUNDLE_COLLECTION_ID = 'gid://shopify/Collection/296239169613';
const THRESHOLD = 10; // Auto-create at 10+ identical proposals

// ============================================================================
// TRIGGER: On Gmail Forward
// ============================================================================

/**
 * Trigger: When Gmail forwards "Bundle Proposal" emails
 * This function is called by Gmail filter → Apps Script webhook
 *
 * Setup Gmail Filter:
 *   1. Gmail Settings → Filters
 *   2. Create filter: subject:"Bundle Proposal"
 *   3. Forward to: Apps Script email endpoint (from deployment)
 */
function processIncomingEmail(e) {
  const message = e.message;
  const body = message.getPlainBody();

  Logger.log('Received email from: ' + message.getFrom());
  Logger.log('Email body: ' + body);

  // Parse JSON from email body
  try {
    const proposalData = JSON.parse(body);

    // Validate data
    if (!proposalData.email || !proposalData.hash || !proposalData.product_ids) {
      Logger.log('❌ Invalid proposal data: ' + body);
      return;
    }

    Logger.log('✅ Valid proposal data parsed');

    // Add to Google Sheet
    addProposalToSheet(proposalData);

  } catch (err) {
    Logger.log('❌ Error parsing email: ' + err.toString());
  }
}

// ============================================================================
// ADD PROPOSAL TO SHEET
// ============================================================================

/**
 * Add new proposal to PROPOSALS sheet
 * Check if threshold reached and trigger auto-creation
 */
function addProposalToSheet(proposalData) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PROPOSALS');

  if (!sheet) {
    Logger.log('❌ Sheet PROPOSALS not found');
    return;
  }

  // Check if email already submitted this hash (prevent duplicates)
  const existingData = sheet.getDataRange().getValues();
  for (let i = 1; i < existingData.length; i++) { // Skip header
    if (existingData[i][1] === proposalData.email && existingData[i][2] === proposalData.hash) {
      Logger.log(`⚠️ Email ${proposalData.email} already submitted hash ${proposalData.hash}`);
      return; // Don't add duplicate
    }
  }

  // Append new row
  sheet.appendRow([
    new Date(), // Column A: Timestamp
    proposalData.email, // Column B: Email
    proposalData.hash, // Column C: Hash
    JSON.stringify(proposalData.product_ids), // Column D: Product_IDs
    JSON.stringify(proposalData.product_handles), // Column E: Product_Handles
    '', // Column F: Count (formula will calculate)
    'FALSE' // Column G: Bundle_Created
  ]);

  Logger.log(`✅ Proposal added to sheet`);

  // Wait for formulas to calculate
  SpreadsheetApp.flush();

  // Count proposals for this hash
  const count = countProposalsForHash(proposalData.hash);

  Logger.log(`📊 Proposal count for hash ${proposalData.hash}: ${count}/${THRESHOLD}`);

  // Check if threshold reached
  if (count >= THRESHOLD) {
    const bundleCreated = isBundleAlreadyCreated(proposalData.hash);

    if (!bundleCreated) {
      Logger.log(`🎉 Threshold reached! Auto-creating bundle...`);
      createBundleAuto(proposalData.hash, proposalData.product_ids, proposalData.product_handles);
    } else {
      Logger.log(`⚠️ Bundle already created for hash: ${proposalData.hash}`);
    }
  } else {
    Logger.log(`⏳ ${THRESHOLD - count} more proposals needed`);
  }
}

// ============================================================================
// COUNT PROPOSALS FOR HASH
// ============================================================================

/**
 * Count how many proposals have the same hash
 * (= identical product combinations)
 */
function countProposalsForHash(hash) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PROPOSALS');
  const data = sheet.getDataRange().getValues();

  let count = 0;
  for (let i = 1; i < data.length; i++) { // Skip header row
    if (data[i][2] === hash) { // Column C: Hash
      count++;
    }
  }

  return count;
}

// ============================================================================
// CHECK IF BUNDLE ALREADY CREATED
// ============================================================================

/**
 * Check if bundle was already auto-created for this hash
 * (prevents creating duplicates)
 */
function isBundleAlreadyCreated(hash) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('BUNDLES_CREATED');
  const data = sheet.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) { // Skip header row
    if (data[i][0] === hash) { // Column A: Hash
      return true;
    }
  }

  return false;
}

// ============================================================================
// AUTO-CREATE BUNDLE (SHOPIFY ADMIN API)
// ============================================================================

/**
 * Main function: Auto-create bundle via Shopify Admin API
 *
 * Steps:
 *   1. Fetch product details for pricing
 *   2. Calculate bundle price (35% discount)
 *   3. Generate bundle title and handle
 *   4. Create product via Shopify Admin API
 *   5. Add to collection
 *   6. Record in BUNDLES_CREATED sheet
 *   7. Mark all proposals as created
 *   8. Shopify Flow will auto-send emails (triggered by tag "auto-created")
 */
function createBundleAuto(hash, productIds, productHandles) {
  Logger.log(`\n${'='.repeat(80)}`);
  Logger.log(`AUTO-CREATING BUNDLE FOR HASH: ${hash}`);
  Logger.log(`${'='.repeat(80)}\n`);

  // 1. Fetch product details for pricing
  Logger.log('Step 1/8: Fetching product details...');
  const products = fetchProductsDetails(productHandles);

  if (!products || products.length === 0) {
    Logger.log('❌ Failed to fetch product details');
    return;
  }

  Logger.log(`✅ Fetched ${products.length} products`);

  // 2. Calculate pricing
  Logger.log('\nStep 2/8: Calculating pricing...');
  const totalPrice = products.reduce((sum, p) => sum + parseFloat(p.price), 0);
  const bundlePrice = (totalPrice * 0.65).toFixed(2); // 35% OFF

  Logger.log(`   Total regular price: $${totalPrice.toFixed(2)}`);
  Logger.log(`   Bundle price (35% OFF): $${bundlePrice}`);
  Logger.log(`   Savings: $${(totalPrice - bundlePrice).toFixed(2)}`);

  // 3. Generate bundle title and handle
  Logger.log('\nStep 3/8: Generating bundle metadata...');
  const shortHash = hash.replace('hash_', '').substring(0, 6).toUpperCase();
  const bundleTitle = `Custom Bundle #${shortHash}`;
  const bundleHandle = `custom-bundle-${shortHash.toLowerCase()}`;

  Logger.log(`   Title: ${bundleTitle}`);
  Logger.log(`   Handle: ${bundleHandle}`);

  // 4. Get customer emails for this hash
  Logger.log('\nStep 4/8: Getting customer emails...');
  const customerEmails = getCustomerEmailsForHash(hash);
  Logger.log(`   Customers to notify: ${customerEmails.length}`);

  // 5. Create bundle via Shopify Admin API (REST)
  Logger.log('\nStep 5/8: Creating bundle via Shopify Admin API...');

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
        },
        {
          namespace: 'auto_bundle',
          key: 'product_handles',
          type: 'json',
          value: JSON.stringify(productHandles)
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

  Logger.log(`   API Response Code: ${responseCode}`);

  if (responseCode === 201) {
    const result = JSON.parse(responseBody);
    const bundleId = result.product.id;
    const bundleUrl = `https://www.alphamedical.shop/products/${bundleHandle}`;

    Logger.log(`   ✅ Bundle created successfully!`);
    Logger.log(`   Bundle ID: ${bundleId}`);
    Logger.log(`   Bundle URL: ${bundleUrl}`);

    // 6. Add to collection
    Logger.log('\nStep 6/8: Adding bundle to collection...');
    addBundleToCollection(bundleId);

    // 7. Record in BUNDLES_CREATED sheet
    Logger.log('\nStep 7/8: Recording in BUNDLES_CREATED sheet...');
    recordBundleCreated(hash, bundleId, bundleTitle, bundleUrl, customerEmails);

    // 8. Mark proposals as bundle_created = TRUE
    Logger.log('\nStep 8/9: Marking proposals as created...');
    markProposalsAsCreated(hash);

    // 9. Send emails directly via Gmail (Apps Script MailApp)
    Logger.log('\nStep 9/9: Sending email notifications...');
    sendBundleCreatedEmails(bundleTitle, bundleUrl, bundlePrice, totalPrice.toFixed(2), customerEmails);

    Logger.log(`\n${'='.repeat(80)}`);
    Logger.log(`🎉 BUNDLE AUTO-CREATION COMPLETE`);
    Logger.log(`${'='.repeat(80)}`);
    Logger.log(`📦 Bundle: ${bundleTitle}`);
    Logger.log(`💰 Price: $${bundlePrice} (was $${totalPrice.toFixed(2)})`);
    Logger.log(`📧 Notifications: ${customerEmails.length} customers`);
    Logger.log(`🔗 URL: ${bundleUrl}`);
    Logger.log(`\n✅ Emails sent directly via Apps Script MailApp.`);
    Logger.log(`${'='.repeat(80)}\n`);

  } else {
    Logger.log(`   ❌ Failed to create bundle`);
    Logger.log(`   Response: ${responseBody}`);
  }
}

// ============================================================================
// FETCH PRODUCT DETAILS (Shopify Product JSON API)
// ============================================================================

/**
 * Fetch product details via public Product JSON API
 * Note: Using handles instead of IDs (public API accessible)
 */
function fetchProductsDetails(productHandles) {
  const products = [];

  for (let handle of productHandles) {
    const url = `https://www.alphamedical.shop/products/${handle}.json`;

    try {
      const response = UrlFetchApp.fetch(url, {muteHttpExceptions: true});

      if (response.getResponseCode() !== 200) {
        Logger.log(`⚠️ Failed to fetch product ${handle}: HTTP ${response.getResponseCode()}`);
        continue;
      }

      const data = JSON.parse(response.getContentText());

      if (data.product) {
        products.push({
          id: data.product.id,
          title: data.product.title,
          handle: data.product.handle,
          price: data.product.variants[0].price
        });

        Logger.log(`   ✓ ${data.product.title}: $${data.product.variants[0].price}`);
      }
    } catch (err) {
      Logger.log(`❌ Error fetching product ${handle}: ${err.toString()}`);
    }
  }

  return products;
}

// ============================================================================
// GET CUSTOMER EMAILS FOR HASH
// ============================================================================

/**
 * Get all customer emails who proposed this bundle (same hash)
 */
function getCustomerEmailsForHash(hash) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PROPOSALS');
  const data = sheet.getDataRange().getValues();

  const emails = [];
  for (let i = 1; i < data.length; i++) { // Skip header row
    if (data[i][2] === hash) { // Column C: Hash
      emails.push(data[i][1]); // Column B: Email
    }
  }

  return emails;
}

// ============================================================================
// ADD BUNDLE TO COLLECTION
// ============================================================================

/**
 * Add bundle to "Medical Equipment Bundles" collection
 */
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
  const responseCode = response.getResponseCode();

  if (responseCode === 201) {
    Logger.log(`   ✅ Added to collection ${BUNDLE_COLLECTION_ID}`);
  } else {
    Logger.log(`   ⚠️ Failed to add to collection: HTTP ${responseCode}`);
    Logger.log(`   Response: ${response.getContentText()}`);
  }
}

// ============================================================================
// RECORD BUNDLE CREATED
// ============================================================================

/**
 * Record bundle creation in BUNDLES_CREATED sheet
 */
function recordBundleCreated(hash, bundleId, bundleTitle, bundleUrl, customerEmails) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('BUNDLES_CREATED');

  if (!sheet) {
    Logger.log('⚠️ Sheet BUNDLES_CREATED not found');
    return;
  }

  sheet.appendRow([
    hash, // Column A: Hash
    bundleId, // Column B: Bundle_ID
    bundleTitle, // Column C: Bundle_Title
    bundleUrl, // Column D: Bundle_URL
    new Date(), // Column E: Created_At
    customerEmails.length, // Column F: Customer_Count
    JSON.stringify(customerEmails) // Column G: Customer_Emails
  ]);

  Logger.log(`   ✅ Recorded in BUNDLES_CREATED sheet`);
}

// ============================================================================
// MARK PROPOSALS AS CREATED
// ============================================================================

/**
 * Mark all proposals with this hash as bundle_created = TRUE
 */
function markProposalsAsCreated(hash) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('PROPOSALS');
  const data = sheet.getDataRange().getValues();

  let updated = 0;

  for (let i = 1; i < data.length; i++) { // Skip header row
    if (data[i][2] === hash) { // Column C: Hash
      sheet.getRange(i + 1, 7).setValue('TRUE'); // Column G: Bundle_Created
      updated++;
    }
  }

  Logger.log(`   ✅ Marked ${updated} proposals as created`);
}

// ============================================================================
// SEND EMAIL NOTIFICATIONS (Apps Script MailApp)
// ============================================================================

/**
 * Send bundle creation emails directly via Gmail
 *
 * Note: Apps Script MailApp quotas:
 * - Gmail free: 100 emails/day
 * - Google Workspace: 1,500 emails/day
 *
 * If you need to send more emails, consider using external email service
 * (SendGrid, Mailgun, etc.) via UrlFetchApp
 */
function sendBundleCreatedEmails(bundleTitle, bundleUrl, bundlePrice, compareAtPrice, customerEmails) {
  const subject = '🎉 Your Custom Bundle is Ready - 35% OFF!';

  // HTML email template
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
              $${compareAtPrice}
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
        <p>
          <a href="https://www.alphamedical.shop" style="color: #4A90E2; text-decoration: none;">Visit our store</a>
        </p>
      </div>
    </div>
  `;

  // Send email to each customer
  let sentCount = 0;
  let failedCount = 0;

  customerEmails.forEach(function(email) {
    try {
      MailApp.sendEmail({
        to: email,
        subject: subject,
        htmlBody: htmlBody,
        name: 'Alpha Medical' // Sender name
      });

      Logger.log(`   ✅ Email sent to: ${email}`);
      sentCount++;

    } catch (err) {
      Logger.log(`   ❌ Failed to send email to ${email}: ${err.toString()}`);
      failedCount++;
    }
  });

  Logger.log(`\n   📧 Email summary:`);
  Logger.log(`      Sent: ${sentCount}`);
  Logger.log(`      Failed: ${failedCount}`);
  Logger.log(`      Total: ${customerEmails.length}`);
}

// ============================================================================
// MANUAL TESTING FUNCTIONS
// ============================================================================

/**
 * Test function: Simulate receiving a proposal
 * Usage: Run this function from Apps Script editor to test
 */
function testAddProposal() {
  const testProposal = {
    email: 'test@example.com',
    hash: 'hash_test123abc',
    product_ids: [7623055966285, 7623055999053, 7623056031821],
    product_handles: ['office-worker-essential-kit', 'senior-mobility-support', 'chronic-pain-starter-kit'],
    timestamp: new Date().toISOString()
  };

  Logger.log('Testing proposal submission...');
  addProposalToSheet(testProposal);
}

/**
 * Test function: Simulate auto-creation (10+ proposals)
 * Usage: Run this 10 times with different emails to trigger auto-creation
 */
function testAutoCreation() {
  const testHash = 'hash_test123abc';
  const testHandles = ['office-worker-essential-kit', 'senior-mobility-support', 'chronic-pain-starter-kit'];
  const testIds = [7623055966285, 7623055999053, 7623056031821];

  // Simulate 10 proposals
  for (let i = 1; i <= 10; i++) {
    const testProposal = {
      email: `customer${i}@example.com`,
      hash: testHash,
      product_ids: testIds,
      product_handles: testHandles,
      timestamp: new Date().toISOString()
    };

    Logger.log(`Adding test proposal ${i}/10...`);
    addProposalToSheet(testProposal);
  }
}

/**
 * Test function: Check bundle creation status
 */
function checkBundleStatus(hash) {
  const created = isBundleAlreadyCreated(hash);
  const count = countProposalsForHash(hash);

  Logger.log(`Bundle Status for hash: ${hash}`);
  Logger.log(`  Proposals count: ${count}`);
  Logger.log(`  Bundle created: ${created}`);
  Logger.log(`  Status: ${count >= THRESHOLD ? '✅ Ready for creation' : `⏳ ${THRESHOLD - count} more needed`}`);
}

// ============================================================================
// DEPLOYMENT INSTRUCTIONS
// ============================================================================

/**
 * DEPLOYMENT STEPS:
 *
 * 1. CREATE GOOGLE SHEET:
 *    - Name: "Bundle Proposals Auto-Creation"
 *    - Sheet 1: PROPOSALS
 *      Columns: Timestamp | Email | Hash | Product_IDs | Product_Handles | Count | Bundle_Created
 *      Formula in F2: =COUNTIF($C$2:$C, C2)
 *    - Sheet 2: BUNDLES_CREATED
 *      Columns: Hash | Bundle_ID | Bundle_Title | Bundle_URL | Created_At | Customer_Count | Customer_Emails
 *
 * 2. APPS SCRIPT SETUP:
 *    - Tools → Script editor
 *    - Paste this code
 *    - Update SHOPIFY_ADMIN_ACCESS_TOKEN (line 22)
 *    - Save project
 *
 * 3. DEPLOY AS WEB APP:
 *    - Deploy → New deployment
 *    - Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 *    - Deploy
 *    - Copy Web App URL
 *
 * 4. GMAIL FILTER SETUP:
 *    - Gmail Settings → Filters and Blocked Addresses
 *    - Create filter: subject:"Bundle Proposal"
 *    - Action: Forward to → Apps Script email endpoint
 *    - Save filter
 *
 * 5. EMAIL NOTIFICATIONS:
 *    - Emails sent directly via Apps Script MailApp (Gmail)
 *    - No Shopify Flow configuration needed
 *    - Quotas: Gmail free (100/day), Google Workspace (1,500/day)
 *    - Template included in sendBundleCreatedEmails() function
 *
 * 6. TESTING:
 *    - Run testAddProposal() function
 *    - Check PROPOSALS sheet for new row
 *    - Run testAutoCreation() to simulate 10 proposals
 *    - Check BUNDLES_CREATED sheet
 *    - Verify bundle in Shopify Admin
 *    - Verify emails sent via Flow
 *
 * STATUS: ✅ READY FOR DEPLOYMENT
 */
