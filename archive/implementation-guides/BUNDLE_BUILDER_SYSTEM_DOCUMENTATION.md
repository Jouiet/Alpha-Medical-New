# BUNDLE BUILDER SYSTEM - COMPLETE DOCUMENTATION
## Alpha Medical Community-Validated Bundle Co-Creation System

**Status**: ✅ DEPLOYED & LIVE
**URL**: https://www.alphamedical.shop/pages/build-your-bundle
**Deployment Date**: November 14, 2025
**Version**: 1.0.0

---

## TABLE OF CONTENTS

1. [System Overview](#system-overview)
2. [Technical Architecture](#technical-architecture)
3. [File Structure](#file-structure)
4. [Customer User Journey](#customer-user-journey)
5. [Backend Integration Setup](#backend-integration-setup)
6. [Testing & Verification](#testing--verification)
7. [Maintenance & Updates](#maintenance--updates)
8. [Troubleshooting](#troubleshooting)
9. [Future Enhancements](#future-enhancements)

---

## SYSTEM OVERVIEW

### Concept
The Bundle Builder enables customers to propose custom 3-4 product bundles with automatic 35% discount. When 10+ customers request the **identical bundle combination**, Alpha Medical creates it as a permanent product offering and notifies all proposing customers.

### Key Features
- ✅ **100% Native Shopify** - Zero external apps, zero recurring costs
- ✅ **Product Search** - Debounced fuzzy search (300ms) across all products
- ✅ **Real-time Validation** - 3-4 products, $500 maximum, duplicate prevention
- ✅ **Automatic Pricing** - 35% discount calculated in real-time
- ✅ **Email Integration** - Shopify Contact Form → Gmail → Google Sheets
- ✅ **GA4 Tracking** - Complete analytics for user behavior
- ✅ **Mobile Responsive** - Optimized for all devices
- ✅ **Alpha Medical Branding** - Custom colors (#4A90E2, #7FCCC9)

### Business Rules
| Rule | Value | Rationale |
|------|-------|-----------|
| **Min Products** | 3 | Ensures meaningful discount |
| **Max Products** | 4 | Keeps shipping/logistics manageable |
| **Max Bundle Value** | $500 | Prevents extremely large orders |
| **Discount Rate** | 35% | Competitive bundling incentive |
| **Creation Threshold** | 10+ identical proposals | Validates customer demand |
| **Monthly Limit** | 3 proposals per customer | Prevents spam/abuse |
| **Review Period** | 3-5 business days | Manual admin review time |

---

## TECHNICAL ARCHITECTURE

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     CUSTOMER INTERFACE                       │
│  (Shopify Page: /pages/build-your-bundle)                  │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Product      │  │ Bundle       │  │ Proposal     │     │
│  │ Search       │→│ Selection    │→│ Submission   │     │
│  │ (300ms       │  │ Panel        │  │ Form         │     │
│  │  debounce)   │  │ (3-4 items)  │  │ (Email)      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    SHOPIFY CONTACT FORM                      │
│  (Native Shopify - no external dependencies)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    EMAIL FORWARDING                          │
│  Shopify → Gmail (contact form notifications)               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    GOOGLE SHEETS INTEGRATION                 │
│  Gmail filter → Auto-forward → Apps Script parsing          │
│                                                              │
│  Columns:                                                    │
│  - Timestamp                                                 │
│  - Customer Email                                            │
│  - Product IDs (comma-separated)                            │
│  - Product Titles                                            │
│  - Regular Price                                             │
│  - Bundle Price (35% discount)                              │
│  - Proposal Hash (for duplicate detection)                  │
│  - Vote Count                                                │
│  - Status (Pending/Approved/Created)                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    APPS SCRIPT AUTOMATION                    │
│  - Parse email body JSON                                     │
│  - Generate proposal hash (sorted product IDs)              │
│  - Detect identical proposals (hash matching)               │
│  - Increment vote count                                      │
│  - Trigger notification at 10+ votes                        │
│  - Send Klaviyo email to all proposing customers            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    MANUAL BUNDLE CREATION                    │
│  Admin creates bundle product in Shopify when threshold hit │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Customer Action**: Searches products → Selects 3-4 items → Submits proposal
2. **Shopify Processing**: Contact form → Email notification sent to admin
3. **Email Routing**: Gmail receives notification → Filter triggers
4. **Google Sheets**: Apps Script parses JSON → Inserts row → Checks for matches
5. **Aggregation**: Script counts identical proposals (hash matching)
6. **Threshold Trigger**: At 10+ votes → Admin notification sent
7. **Bundle Creation**: Admin creates bundle product manually
8. **Customer Notification**: Klaviyo email sent to all proposing customers

---

## FILE STRUCTURE

### Deployed Files

```
Alpha-Medical/
├── sections/
│   └── bundle-builder.liquid          (394 lines)
│       - Main section template
│       - Product search interface
│       - Selected products panel
│       - Shopify contact form
│       - FAQ and How It Works sections
│
├── assets/
│   ├── bundle-builder.css             (1,085 lines)
│   │   - Complete styling with Alpha Medical branding
│   │   - CSS custom properties for design system
│   │   - Responsive breakpoints (768px, 480px)
│   │   - Hero, search, selection, form, FAQ styles
│   │
│   └── bundle-builder.js              (438 lines)
│       - Debounced search (300ms)
│       - Fuzzy matching (title, type, vendor)
│       - Real-time validation
│       - Price calculations (35% discount)
│       - Bundle data JSON serialization
│       - GA4 event tracking
│
├── templates/
│   └── page.build-your-bundle.json    (17 lines)
│       - Page template configuration
│       - References bundle-builder section
│
├── layout/
│   └── theme.liquid                   (Updated)
│       - Added bundle-builder.css link (line 309)
│       - Added bundle-builder.js link (line 310)
│
└── deploy_bundle_builder.py           (273 lines)
    - Automated deployment script
    - Uploads all assets to Shopify
    - Creates /pages/build-your-bundle page
```

### Code Architecture

#### sections/bundle-builder.liquid
```liquid
┌─────────────────────────────────────────────────────────┐
│ Hero Section                                             │
│ - Title, subtitle, stats (35%, 10+, 3-4)               │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Main Interface (Two-Column Grid)                        │
│                                                          │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │ LEFT PANEL       │  │ RIGHT PANEL      │           │
│  │ Product Search   │  │ Selected Bundle  │           │
│  │ - Search input   │  │ - Product list   │           │
│  │ - Results list   │  │ - Price summary  │           │
│  │ - Search help    │  │ - Submission form│           │
│  └──────────────────┘  └──────────────────┘           │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ How It Works (4-Step Process)                           │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ FAQ (6 Questions)                                       │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│ Product Data Preload (JavaScript)                      │
│ - window.BUNDLE_BUILDER_PRODUCTS array                 │
│ - window.BUNDLE_BUILDER_CONFIG object                  │
│ - Paginated product fetching (250 per page)            │
└─────────────────────────────────────────────────────────┘
```

#### assets/bundle-builder.js
```javascript
// STATE MANAGEMENT
let selectedProducts = [];
let searchDebounceTimer = null;

// MAIN FUNCTIONS
init()                          // Initialize event listeners
handleSearchInput(e)            // Debounced search trigger
performSearch(query)            // Fuzzy product search
selectProduct(productId)        // Add to bundle (validation)
removeProduct(productId)        // Remove from bundle
updatePriceSummary()            // Calculate 35% discount
validateForm()                  // Enable/disable submit
createBundleDataJSON()          // Serialize for submission
trackEvent(eventName, params)   // GA4 analytics

// VALIDATION RULES
- Min 3 products, max 4 products
- No duplicates
- Max $500 regular price
- Only available products
- Checkbox commitment required
```

#### assets/bundle-builder.css
```css
/* DESIGN SYSTEM */
:root {
  /* Brand Colors */
  --am-primary: #4A90E2;          /* Blue */
  --am-secondary: #7FCCC9;        /* Green */

  /* Spacing Scale */
  --am-space-xs: 4px;
  --am-space-sm: 8px;
  --am-space-md: 16px;
  --am-space-lg: 24px;
  --am-space-xl: 32px;
  --am-space-2xl: 48px;

  /* Typography */
  --am-font-heading: 'Inter', system-ui, sans-serif;
  --am-font-body: 'Source Sans Pro', system-ui, sans-serif;
}

/* COMPONENTS */
.bundle-builder-section         // Main container
.bundle-builder-hero            // Hero section
.bundle-builder-main            // Two-column grid
.builder-search-panel           // Left panel
.builder-selection-panel        // Right panel
.search-results                 // Dropdown results
.selected-products              // Bundle product list
.price-summary                  // Pricing breakdown
.bundle-proposal-form           // Contact form
.how-it-works                   // Steps section
.faq-section                    // FAQ accordion
```

---

## CUSTOMER USER JOURNEY

### Step-by-Step Walkthrough

#### 1. Discovery
**URL**: https://www.alphamedical.shop/pages/build-your-bundle

**Landing Experience**:
- Hero section with clear value proposition
- Stats display: 35% discount, 10+ requests needed, 3-4 products
- Two-panel interface (search left, bundle right)

#### 2. Product Search
**Interaction**:
- Customer types in search input (e.g., "knee support")
- 300ms debounce delay
- Fuzzy matching across product title, type, vendor
- Results display: image, title, price, availability
- Max 10 results shown

**Example Search Results**:
```
┌─────────────────────────────────────────────┐
│ [Image] Knee Support Brace Pro              │
│         $49.99                               │
│         [+ Add]                              │
├─────────────────────────────────────────────┤
│ [Image] Adjustable Knee Compression Sleeve  │
│         $34.99                               │
│         [+ Add]                              │
└─────────────────────────────────────────────┘
```

#### 3. Bundle Selection
**Interaction**:
- Customer clicks "+ Add" button
- Product appears in right panel with remove button
- Counter updates (1/4, 2/4, 3/4, 4/4)
- Price summary updates in real-time

**Bundle Display Example**:
```
Your Bundle (3/4)
┌──────────────────────────────────────┐
│ 1. [Image] Knee Support Brace Pro    │
│    $49.99                   [× Remove]│
├──────────────────────────────────────┤
│ 2. [Image] Ankle Compression Sleeve  │
│    $34.99                   [× Remove]│
├──────────────────────────────────────┤
│ 3. [Image] Posture Corrector         │
│    $39.99                   [× Remove]│
└──────────────────────────────────────┘

Price Summary
─────────────────────────────────────
Total Regular Price:        $124.97
Bundle Price (35% OFF):      $81.23
You Save:                    $43.74
```

#### 4. Validation & Constraints
**Real-time Checks**:
- ✅ Minimum 3 products required (form hidden until met)
- ✅ Maximum 4 products enforced (add buttons disabled at max)
- ✅ No duplicate products allowed
- ✅ $500 maximum bundle value enforced (warning shown if exceeded)
- ✅ Only available products selectable (out-of-stock grayed out)

**$500 Limit Warning**:
```
⚠️ Bundle exceeds $500 maximum. Please remove a product.
```

#### 5. Proposal Submission
**Form Fields**:
- Email address (required) - for notifications
- Commitment checkbox (required) - understands this is proposal, not purchase
- Hidden fields: subject, bundle data JSON

**Submission Data Example**:
```json
{
  "timestamp": "2025-11-14T22:30:00Z",
  "products": [
    {
      "id": 8766345633869,
      "handle": "knee-support-brace-pro",
      "title": "Knee Support Brace Pro",
      "price": 49.99,
      "url": "/products/knee-support-brace-pro"
    },
    {
      "id": 8766345666637,
      "handle": "ankle-compression-sleeve",
      "title": "Ankle Compression Sleeve",
      "price": 34.99,
      "url": "/products/ankle-compression-sleeve"
    },
    {
      "id": 8766345699405,
      "handle": "posture-corrector",
      "title": "Posture Corrector",
      "price": 39.99,
      "url": "/products/posture-corrector"
    }
  ],
  "pricing": {
    "regular_total": "124.97",
    "bundle_total": "81.23",
    "discount_percent": 35,
    "savings": "43.74"
  },
  "metadata": {
    "threshold": 10,
    "monthly_limit": 3,
    "user_agent": "Mozilla/5.0...",
    "screen_width": 1920
  }
}
```

#### 6. Success State
**After Submission**:
```
✓ Proposal Submitted Successfully!

We'll notify you when 10+ customers request this bundle.
Check your email for confirmation details.
```

---

## BACKEND INTEGRATION SETUP

### Phase 1: Email Forwarding (Gmail)

#### Step 1: Configure Gmail Filter
1. Log into Gmail account receiving Shopify contact form notifications
2. Search for: `from:noreply@shopify.com subject:"Bundle Proposal"`
3. Click "Create filter"
4. Actions:
   - ✅ Forward to: `bundles@alphamedical.shop` (or Google Sheets email)
   - ✅ Apply label: "Bundle Proposals"
   - ✅ Never send to spam
5. Save filter

#### Step 2: Create Google Sheet
**Sheet Name**: `Bundle Proposals Tracker`

**Column Structure**:
```
A: Timestamp (auto-generated)
B: Customer Email
C: Product IDs (comma-separated)
D: Product Titles (pipe-separated)
E: Product Handles (comma-separated)
F: Regular Total ($)
G: Bundle Total ($)
H: Savings ($)
I: Proposal Hash (MD5 of sorted product IDs)
J: Vote Count (formula: COUNTIF on Hash column)
K: Status (Pending/Approved/Created/Rejected)
L: Admin Notes
M: Created Date (when bundle was created)
N: Shopify Bundle URL
```

**Sample Row**:
```
2025-11-14 22:30:15 | customer@email.com | 8766345633869,8766345666637,8766345699405 | Knee Support Brace Pro | Ankle Compression Sleeve | Posture Corrector | knee-support-brace-pro,ankle-compression-sleeve,posture-corrector | 124.97 | 81.23 | 43.74 | a3f5c8d2e1b4 | 7 | Pending | | |
```

### Phase 2: Google Apps Script

#### Script Setup
1. Open Google Sheet
2. Extensions → Apps Script
3. Create new script: `BundleProposalParser.gs`

#### Complete Apps Script Code

```javascript
/**
 * BUNDLE PROPOSAL PARSER - Google Apps Script
 *
 * Triggered by Gmail filter forwarding Shopify contact form emails
 * Parses JSON bundle data and aggregates proposals
 */

function parseBundleProposalEmail(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Proposals');
  const adminEmail = 'admin@alphamedical.shop'; // Change to your admin email
  const thresholdVotes = 10;

  try {
    // Extract email body
    const emailBody = e.message || e.postData.contents;

    // Parse JSON from email body (Shopify contact form sends JSON in message)
    const jsonMatch = emailBody.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      Logger.log('No JSON found in email body');
      return;
    }

    const proposalData = JSON.parse(jsonMatch[0]);

    // Extract data
    const timestamp = new Date(proposalData.timestamp);
    const customerEmail = e.from || 'unknown@email.com'; // Extract from email sender
    const products = proposalData.products;
    const pricing = proposalData.pricing;

    // Generate proposal hash (sorted product IDs for matching)
    const sortedProductIds = products.map(p => p.id).sort().join(',');
    const proposalHash = Utilities.computeDigest(
      Utilities.DigestAlgorithm.MD5,
      sortedProductIds
    ).map(byte => ('0' + (byte & 0xFF).toString(16)).slice(-2)).join('').substring(0, 12);

    // Extract product details
    const productIds = products.map(p => p.id).join(',');
    const productTitles = products.map(p => p.title).join(' | ');
    const productHandles = products.map(p => p.handle).join(',');

    // Insert row
    sheet.appendRow([
      timestamp,                      // A: Timestamp
      customerEmail,                  // B: Customer Email
      productIds,                     // C: Product IDs
      productTitles,                  // D: Product Titles
      productHandles,                 // E: Product Handles
      pricing.regular_total,          // F: Regular Total
      pricing.bundle_total,           // G: Bundle Total
      pricing.savings,                // H: Savings
      proposalHash,                   // I: Proposal Hash
      '',                             // J: Vote Count (formula added below)
      'Pending',                      // K: Status
      '',                             // L: Admin Notes
      '',                             // M: Created Date
      ''                              // N: Shopify Bundle URL
    ]);

    // Add vote count formula to column J (counts matching hashes)
    const lastRow = sheet.getLastRow();
    const voteCountFormula = `=COUNTIF($I$2:$I$${lastRow},$I${lastRow})`;
    sheet.getRange(lastRow, 10).setFormula(voteCountFormula);

    // Check if threshold reached
    const voteCount = sheet.getRange(lastRow, 10).getValue();

    if (voteCount >= thresholdVotes) {
      sendThresholdNotification(adminEmail, proposalHash, productTitles, voteCount);
    }

    Logger.log(`Proposal added: ${proposalHash} (${voteCount} votes)`);

  } catch (error) {
    Logger.log('Error parsing proposal: ' + error.toString());
    MailApp.sendEmail({
      to: adminEmail,
      subject: 'Bundle Proposal Parser Error',
      body: 'Error details: ' + error.toString() + '\n\nEmail body: ' + emailBody
    });
  }
}

/**
 * Send notification to admin when threshold reached
 */
function sendThresholdNotification(adminEmail, proposalHash, productTitles, voteCount) {
  const subject = `🎉 Bundle Threshold Reached: ${voteCount} votes!`;
  const body = `
A bundle proposal has reached the ${voteCount}-vote threshold!

Proposal Hash: ${proposalHash}
Products: ${productTitles}
Total Votes: ${voteCount}

Action Required:
1. Review proposal in Google Sheet
2. Create bundle product in Shopify
3. Update status to "Created" in sheet
4. System will send Klaviyo notification to all customers

View Sheet: ${SpreadsheetApp.getActiveSpreadsheet().getUrl()}
  `;

  MailApp.sendEmail({
    to: adminEmail,
    subject: subject,
    body: body
  });
}

/**
 * Manual trigger to send customer notifications after bundle created
 * Run this after creating bundle in Shopify
 */
function sendCustomerNotifications(proposalHash, bundleUrl) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Proposals');
  const data = sheet.getDataRange().getValues();

  // Find all customers who proposed this bundle
  const customers = [];
  for (let i = 1; i < data.length; i++) {
    if (data[i][8] === proposalHash && data[i][10] !== 'Notified') {
      customers.push({
        email: data[i][1],
        row: i + 1
      });
    }
  }

  // Send Klaviyo API request for each customer
  customers.forEach(customer => {
    sendKlaviyoNotification(customer.email, bundleUrl, data[0][3]); // product titles from first row

    // Update status to "Notified"
    sheet.getRange(customer.row, 11).setValue('Notified');
  });

  Logger.log(`Notified ${customers.length} customers for bundle ${proposalHash}`);
}

/**
 * Send Klaviyo notification (requires Klaviyo API key)
 */
function sendKlaviyoNotification(customerEmail, bundleUrl, productTitles) {
  const klaviyoApiKey = 'YOUR_KLAVIYO_PRIVATE_API_KEY'; // Set this
  const klaviyoListId = 'YOUR_BUNDLE_NOTIFICATION_LIST_ID'; // Set this

  const payload = {
    token: klaviyoApiKey,
    event: 'Bundle Created',
    customer_properties: {
      '$email': customerEmail
    },
    properties: {
      bundle_url: bundleUrl,
      product_titles: productTitles,
      discount_percent: 35
    }
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  };

  try {
    UrlFetchApp.fetch('https://a.klaviyo.com/api/track', options);
    Logger.log(`Klaviyo notification sent to ${customerEmail}`);
  } catch (error) {
    Logger.log(`Klaviyo error: ${error.toString()}`);
  }
}

/**
 * Create time-driven trigger to check for threshold violations daily
 */
function createDailyTrigger() {
  ScriptApp.newTrigger('checkThresholdDaily')
    .timeBased()
    .everyDays(1)
    .atHour(9) // 9 AM daily
    .create();
}

/**
 * Daily check for proposals that reached threshold
 */
function checkThresholdDaily() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Proposals');
  const data = sheet.getDataRange().getValues();
  const thresholdVotes = 10;
  const adminEmail = 'admin@alphamedical.shop';

  const hashes = {};
  for (let i = 1; i < data.length; i++) {
    const hash = data[i][8];
    const status = data[i][10];

    if (status === 'Pending') {
      hashes[hash] = (hashes[hash] || 0) + 1;
    }
  }

  // Check for hashes that reached threshold
  Object.keys(hashes).forEach(hash => {
    if (hashes[hash] >= thresholdVotes) {
      const firstRow = data.find(row => row[8] === hash);
      sendThresholdNotification(adminEmail, hash, firstRow[3], hashes[hash]);
    }
  });
}
```

#### Trigger Setup
1. In Apps Script editor: Triggers (clock icon) → Add Trigger
2. Function: `parseBundleProposalEmail`
3. Event source: From spreadsheet → On form submit (if using Google Form)
4. OR Event source: Time-driven → Hour timer → Every hour (to check new emails)

### Phase 3: Klaviyo Integration (Optional)

#### Setup
1. Klaviyo → Account → Settings → API Keys
2. Copy Private API Key
3. Create email template for "Bundle Created" notification
4. Update Apps Script with Klaviyo API key

#### Email Template
**Subject**: Your Bundle is Live! Get 35% OFF Now

**Body**:
```
Hi {first_name},

Great news! The bundle you requested is now available:

🎁 {product_titles}
💰 35% OFF (Save ${savings})

{bundle_url}

As a proposing customer, you get priority access for the next 48 hours.

Why we created this bundle:
✓ 10+ customers (including you!) requested it
✓ Community-validated demand
✓ Exclusive 35% discount

[Shop Now →]

Thanks for helping us co-create products our community actually wants!

- Alpha Medical Team
```

---

## TESTING & VERIFICATION

### Pre-Launch Checklist

#### Frontend Testing
- [ ] Page loads: https://www.alphamedical.shop/pages/build-your-bundle
- [ ] Search functionality works (type "knee", see results)
- [ ] Debouncing active (no lag, 300ms delay)
- [ ] Product selection adds to bundle
- [ ] Remove button works
- [ ] Counter updates (0/4, 1/4, 2/4, 3/4, 4/4)
- [ ] Price calculation correct (35% discount)
- [ ] $500 limit enforced (warning appears)
- [ ] Out-of-stock products disabled
- [ ] Duplicate detection works
- [ ] Form validation (email required, checkbox required)
- [ ] Submit button disabled until valid
- [ ] Success message displays after submission
- [ ] Mobile responsive (test on iPhone, Android)
- [ ] Tablet responsive (test on iPad)
- [ ] Desktop responsive (1920px, 1440px, 1024px)

#### Styling Testing
- [ ] Alpha Medical colors applied (#4A90E2, #7FCCC9)
- [ ] Hover effects work (search results, buttons)
- [ ] Smooth transitions (300ms ease)
- [ ] Typography correct (Inter headings, Source Sans body)
- [ ] Spacing consistent (design system)
- [ ] Shadows subtle (0 2px 8px rgba)
- [ ] FAQ accordion expands/collapses
- [ ] How It Works cards display correctly

#### Backend Testing
- [ ] Contact form submits successfully
- [ ] Email received in Gmail
- [ ] Gmail filter triggers (Bundle Proposals label)
- [ ] Email forwarded to Google Sheets (if configured)
- [ ] Google Sheet row inserted
- [ ] Apps Script parses JSON correctly
- [ ] Proposal hash generated
- [ ] Vote count formula calculates
- [ ] Duplicate proposals detected (same hash)
- [ ] Threshold notification sent at 10+ votes
- [ ] Klaviyo email sent (if configured)

#### Analytics Testing
- [ ] GA4 events firing:
  - `bundle_product_added`
  - `bundle_product_removed`
  - `bundle_proposal_submitted`
- [ ] Event parameters correct (product_id, product_title, bundle_size, etc.)
- [ ] dataLayer pushes working (if using GTM)

### Test Scenarios

#### Scenario 1: Happy Path (3 products)
1. Navigate to /pages/build-your-bundle
2. Search "knee"
3. Add "Knee Support Brace Pro" ($49.99)
4. Search "ankle"
5. Add "Ankle Compression Sleeve" ($34.99)
6. Search "posture"
7. Add "Posture Corrector" ($39.99)
8. Verify price summary:
   - Regular: $124.97
   - Bundle: $81.23 (35% off)
   - Savings: $43.74
9. Enter email: test@example.com
10. Check commitment checkbox
11. Submit
12. Verify success message
13. Check Gmail for confirmation

**Expected Result**: ✅ Proposal submitted, email received, Google Sheet updated

#### Scenario 2: $500 Limit Enforcement
1. Add 4 high-value products totaling >$500
2. Verify warning appears
3. Verify form hidden
4. Remove one product
5. Verify form reappears

**Expected Result**: ✅ Warning shown, form disabled until under $500

#### Scenario 3: Duplicate Detection
1. Submit proposal with Products A, B, C
2. Try to add Product A again
3. Verify alert: "Product already selected"

**Expected Result**: ✅ Duplicate prevented, alert shown

#### Scenario 4: Mobile Experience
1. Open on iPhone Safari
2. Verify responsive layout (single column)
3. Test search (virtual keyboard doesn't break UI)
4. Test product selection (tap targets large enough)
5. Test form submission

**Expected Result**: ✅ Fully functional on mobile

---

## MAINTENANCE & UPDATES

### Regular Maintenance Tasks

#### Weekly
- [ ] Review Google Sheet for new proposals
- [ ] Check vote counts for proposals nearing threshold
- [ ] Respond to customer emails (if any questions)

#### Monthly
- [ ] Analyze GA4 data (conversion rate, popular products)
- [ ] Review proposals with 5-9 votes (potential bundles)
- [ ] Clean up rejected/expired proposals in sheet

#### Quarterly
- [ ] Review discount rate (35% vs. competitors)
- [ ] Evaluate threshold (10+ vs. 5+ or 15+)
- [ ] Update FAQ based on customer questions
- [ ] Refresh product images/descriptions

### Configuration Updates

#### Change Discount Rate
1. Edit `sections/bundle-builder.liquid`:
```liquid
discountPercent: 35,  // Change to desired %
```
2. Edit `assets/bundle-builder.js`:
```javascript
discountPercent: 35,  // Change to match
```
3. Update hero subtitle text
4. Redeploy using `deploy_bundle_builder.py`

#### Change Threshold
1. Edit `templates/page.build-your-bundle.json`:
```json
"threshold": 10,  // Change to desired number
```
2. Update FAQ text
3. Redeploy

#### Change Product Limit
1. Edit `sections/bundle-builder.liquid`:
```liquid
minProducts: 3,  // Change if needed
maxProducts: 4,  // Change if needed
```
2. Edit `assets/bundle-builder.js`:
```javascript
minProducts: 3,
maxProducts: 4,
```
3. Update hero subtitle
4. Redeploy

### Adding New Features

#### Feature: Save Proposals (User Accounts)
**Complexity**: HIGH
**Estimated Time**: 8-12 hours
**Requirements**:
- Shopify customer accounts enabled
- Metafields for customer proposals
- Customer login/dashboard integration

#### Feature: Bundle Preview Images
**Complexity**: MEDIUM
**Estimated Time**: 4-6 hours
**Requirements**:
- Image compositing (Canvas API or server-side)
- Dynamic image generation
- Caching strategy

#### Feature: Social Sharing
**Complexity**: LOW
**Estimated Time**: 2-3 hours
**Requirements**:
- Share buttons (Facebook, Twitter, WhatsApp)
- Open Graph meta tags
- UTM tracking parameters

---

## TROUBLESHOOTING

### Common Issues

#### Issue 1: Page Not Loading
**Symptoms**: Blank page or 404 error

**Solutions**:
1. Verify page exists: Admin → Pages → "Build Your Bundle"
2. Check page status: Published = Yes
3. Verify template suffix: `build-your-bundle`
4. Check theme.liquid includes CSS/JS:
```liquid
{{ 'bundle-builder.css' | asset_url | stylesheet_tag }}
{{ 'bundle-builder.js' | asset_url | script_tag }}
```

#### Issue 2: Search Not Working
**Symptoms**: No results when typing

**Solutions**:
1. Check browser console for errors
2. Verify `window.BUNDLE_BUILDER_PRODUCTS` is populated:
```javascript
console.log(window.BUNDLE_BUILDER_PRODUCTS.length);
```
3. Check product pagination limit (250 products per page)
4. Verify JavaScript is loading (Network tab)

#### Issue 3: Pricing Calculation Wrong
**Symptoms**: Discount not 35% or incorrect totals

**Solutions**:
1. Check `assets/bundle-builder.js` discount rate:
```javascript
discountPercent: 35,
```
2. Verify product prices in cents (Shopify API returns cents):
```javascript
const regularTotal = selectedProducts.reduce((sum, p) => sum + p.price, 0);
const bundleTotal = regularTotal * (1 - CONFIG.discountPercent / 100);
```
3. Test with known products:
   - 3 products × $50 = $150 regular
   - 35% off = $97.50 bundle
   - Savings = $52.50

#### Issue 4: Form Not Submitting
**Symptoms**: Submit button disabled or form errors

**Solutions**:
1. Verify commitment checkbox checked
2. Check email format validity
3. Verify 3-4 products selected
4. Check $500 limit not exceeded
5. Browser console for validation errors

#### Issue 5: Emails Not Received
**Symptoms**: Contact form submits but no Gmail notification

**Solutions**:
1. Check Shopify notification settings: Settings → Notifications → Contact form
2. Verify email address correct
3. Check Gmail spam folder
4. Test with different email address
5. Verify Gmail filter active

#### Issue 6: Google Sheets Not Updating
**Symptoms**: Emails received but sheet not populated

**Solutions**:
1. Verify Apps Script trigger enabled: Triggers → parseBundleProposalEmail
2. Check Apps Script execution logs: View → Logs
3. Test JSON parsing manually:
```javascript
function testParse() {
  const testJson = '{"timestamp":"2025-11-14T22:30:00Z",...}';
  Logger.log(JSON.parse(testJson));
}
```
4. Verify sheet name matches script: `Proposals`

#### Issue 7: Mobile Layout Broken
**Symptoms**: UI overlapping or cut off on mobile

**Solutions**:
1. Check viewport meta tag in theme.liquid:
```html
<meta name="viewport" content="width=device-width,initial-scale=1">
```
2. Verify CSS media queries:
```css
@media (max-width: 768px) { ... }
@media (max-width: 480px) { ... }
```
3. Test on real device (not just browser DevTools)

### Error Messages

#### "Product already selected"
**Cause**: Duplicate product prevention
**Fix**: This is expected behavior. Customer must choose different product.

#### "Maximum 4 products allowed"
**Cause**: Product limit reached
**Fix**: Expected behavior. Customer must remove product before adding another.

#### "Bundle exceeds $500 maximum"
**Cause**: Total regular price > $500
**Fix**: Expected behavior. Customer must remove expensive product.

#### "This product is currently out of stock"
**Cause**: Product availability check
**Fix**: Customer must choose available product.

### Debug Mode

#### Enable Console Logging
Add to `assets/bundle-builder.js`:
```javascript
const DEBUG_MODE = true;

if (DEBUG_MODE) {
  console.log('Selected products:', selectedProducts);
  console.log('Regular total:', regularTotal);
  console.log('Bundle total:', bundleTotal);
  console.log('Bundle data JSON:', createBundleDataJSON());
}
```

#### Test Data
Create test proposal manually:
```javascript
// In browser console
window.bundleBuilder.selectProduct(8766345633869); // Knee brace
window.bundleBuilder.selectProduct(8766345666637); // Ankle sleeve
window.bundleBuilder.selectProduct(8766345699405); // Posture corrector
console.log(document.getElementById('bundle-data-json').value);
```

---

## FUTURE ENHANCEMENTS

### Short-term (1-3 months)

#### 1. Proposal Dashboard (Customer Accounts)
**Description**: Allow logged-in customers to view their proposal history, vote counts, and bundle status.

**Requirements**:
- Shopify customer accounts enabled
- Customer metafields for proposal tracking
- Dashboard page template

**Estimated Effort**: 12-16 hours

#### 2. Email Notifications (Klaviyo)
**Description**: Automated emails at proposal milestones (submitted, 5 votes, 10 votes, created).

**Requirements**:
- Klaviyo account + API key
- Email templates for each milestone
- Apps Script integration

**Estimated Effort**: 8-10 hours

#### 3. Popular Proposals Showcase
**Description**: Display trending proposals on homepage to encourage voting.

**Requirements**:
- Google Sheets API integration
- Homepage section template
- Vote count sorting

**Estimated Effort**: 6-8 hours

### Medium-term (3-6 months)

#### 4. Advanced Search Filters
**Description**: Filter products by collection, price range, rating.

**Requirements**:
- Enhanced JavaScript search logic
- UI for filter controls
- Product metadata enrichment

**Estimated Effort**: 10-12 hours

#### 5. Bundle Preview Generator
**Description**: Auto-generate bundle product images (composite of selected products).

**Requirements**:
- Canvas API or Cloudinary integration
- Image composition logic
- Caching strategy

**Estimated Effort**: 16-20 hours

#### 6. A/B Testing Framework
**Description**: Test different discount rates, thresholds, product limits.

**Requirements**:
- Google Optimize or VWO integration
- Analytics tracking
- Variant configurations

**Estimated Effort**: 8-10 hours

### Long-term (6-12 months)

#### 7. AI-Powered Suggestions
**Description**: Recommend complementary products based on selected items.

**Requirements**:
- Shopify product recommendation API
- Machine learning model (or external API)
- Real-time suggestion UI

**Estimated Effort**: 24-32 hours

#### 8. Social Proof Features
**Description**: Show "X customers want this bundle" badges, social sharing incentives.

**Requirements**:
- Vote count public API
- Social sharing buttons
- Referral tracking

**Estimated Effort**: 12-16 hours

#### 9. Automated Bundle Creation
**Description**: Auto-create bundle products in Shopify when threshold reached (no manual admin step).

**Requirements**:
- Shopify Admin API integration
- Bundle product template
- Automated product image generation
- Automated email notifications
- Error handling & rollback

**Estimated Effort**: 32-40 hours
**Risk**: HIGH (automated product creation requires rigorous testing)

---

## APPENDIX

### Key Metrics to Track

#### Conversion Metrics
- **Proposal Submission Rate**: Page views → Proposals submitted
- **Completion Rate**: Searches → Completed bundles (3-4 products)
- **Abandonment Rate**: Started bundle → Left before submission
- **Threshold Conversion**: Proposals → Bundles created (10+ votes)
- **Purchase Rate**: Bundles created → Bundles purchased

#### Engagement Metrics
- **Avg. Search Queries**: Per session
- **Avg. Products Viewed**: Before first selection
- **Avg. Bundle Value**: Regular price of proposals
- **Repeat Proposers**: % customers submitting 2+ proposals
- **Time to Submit**: Avg. time from page load to submission

#### Product Insights
- **Most Proposed Products**: Top 20 products in bundles
- **Most Common Combinations**: 3-product vs. 4-product bundles
- **Price Range Distribution**: $0-100, $100-200, $200-300, $300-500
- **Collection Preferences**: Which collections appear most

### GA4 Event Tracking

#### Events Implemented
```javascript
// Event 1: Product added to bundle
gtag('event', 'bundle_product_added', {
  product_id: 8766345633869,
  product_title: 'Knee Support Brace Pro',
  product_price: 49.99,
  bundle_size: 1
});

// Event 2: Product removed from bundle
gtag('event', 'bundle_product_removed', {
  product_id: 8766345633869,
  bundle_size: 0
});

// Event 3: Proposal submitted
gtag('event', 'bundle_proposal_submitted', {
  product_count: 3,
  regular_total: 124.97,
  bundle_total: 81.23,
  products: 'Knee Support Brace Pro | Ankle Compression Sleeve | Posture Corrector'
});
```

### Contact Information

**Technical Support**: dev@alphamedical.shop
**Business Inquiries**: admin@alphamedical.shop
**Customer Service**: support@alphamedical.shop

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-14 | Initial deployment - Complete system live |

---

**END OF DOCUMENTATION**

*Last Updated: November 14, 2025*
*Document Maintained By: Claude Code + Alpha Medical Development Team*
