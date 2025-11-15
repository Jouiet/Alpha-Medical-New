/**
 * Loyalty Redemption API - Google Apps Script
 * Handles point redemption and discount code generation
 *
 * Deploy as Web App:
 * - Execute as: Me
 * - Access: Anyone
 *
 * Endpoint: /apps/loyalty/redeem
 */

// Configuration
const SHOPIFY_STORE = 'azffej-as.myshopify.com';
const ADMIN_TOKEN = 'YOUR_SHOPIFY_ADMIN_TOKEN_HERE'; // Replace with token from .env.admin
const API_VERSION = '2024-10';

// Redemption tiers
const REDEMPTION_TIERS = {
  100: 5,    // 100 points = $5 OFF
  200: 12,   // 200 points = $12 OFF (bonus $2)
  500: 35,   // 500 points = $35 OFF (bonus $10)
  1000: 80   // 1000 points = $80 OFF (bonus $20)
};

// ============================================================
// SHOPIFY API HELPERS
// ============================================================

function shopifyGraphQL(query, variables = {}) {
  const url = `https://${SHOPIFY_STORE}/admin/api/${API_VERSION}/graphql.json`;

  const options = {
    method: 'post',
    headers: {
      'X-Shopify-Access-Token': ADMIN_TOKEN,
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify({ query, variables })
  };

  const response = UrlFetchApp.fetch(url, options);
  return JSON.parse(response.getContentText());
}

function shopifyREST(endpoint, method = 'GET', data = null) {
  const url = `https://${SHOPIFY_STORE}/admin/api/${API_VERSION}${endpoint}`;

  const options = {
    method: method,
    headers: {
      'X-Shopify-Access-Token': ADMIN_TOKEN,
      'Content-Type': 'application/json'
    }
  };

  if (data) {
    options.payload = JSON.stringify(data);
  }

  const response = UrlFetchApp.fetch(url, options);
  return JSON.parse(response.getContentText());
}

// ============================================================
// CUSTOMER LOYALTY FUNCTIONS
// ============================================================

function getCustomerByEmail(email) {
  const query = `
    query GetCustomer($query: String!) {
      customers(first: 1, query: $query) {
        edges {
          node {
            id
            email
            metafield_points: metafield(namespace: "loyalty", key: "points") { value }
            metafield_tier: metafield(namespace: "loyalty", key: "tier") { value }
            metafield_history: metafield(namespace: "loyalty", key: "history") { value }
            metafield_lifetime_redeemed: metafield(namespace: "loyalty", key: "lifetime_points_redeemed") { value }
          }
        }
      }
    }
  `;

  const result = shopifyGraphQL(query, { query: `email:${email}` });

  if (result.errors || !result.data.customers.edges.length) {
    return null;
  }

  const customer = result.data.customers.edges[0].node;

  return {
    id: customer.id,
    email: customer.email,
    points: parseInt(customer.metafield_points?.value || 0),
    tier: customer.metafield_tier?.value || 'bronze',
    history: JSON.parse(customer.metafield_history?.value || '[]'),
    lifetimeRedeemed: parseInt(customer.metafield_lifetime_redeemed?.value || 0)
  };
}

function updateCustomerPoints(customerId, newPoints, history, lifetimeRedeemed) {
  const mutation = `
    mutation UpdateCustomerMetafields($input: CustomerInput!) {
      customerUpdate(input: $input) {
        customer { id }
        userErrors { field message }
      }
    }
  `;

  const newTier = calculateTier(newPoints);

  const input = {
    id: customerId,
    metafields: [
      { namespace: 'loyalty', key: 'points', value: String(newPoints), type: 'number_integer' },
      { namespace: 'loyalty', key: 'tier', value: newTier, type: 'single_line_text_field' },
      { namespace: 'loyalty', key: 'history', value: JSON.stringify(history), type: 'json' },
      { namespace: 'loyalty', key: 'lifetime_points_redeemed', value: String(lifetimeRedeemed), type: 'number_integer' }
    ]
  };

  const result = shopifyGraphQL(mutation, { input });

  return !result.errors && !result.data.customerUpdate.userErrors.length;
}

function calculateTier(points) {
  if (points >= 1501) return 'gold';
  if (points >= 501) return 'silver';
  return 'bronze';
}

// ============================================================
// DISCOUNT CODE CREATION
// ============================================================

function createDiscountCode(customerId, customerEmail, pointsValue, discountAmount) {
  // Extract customer ID number from GID
  const customerIdNum = customerId.split('/').pop();

  // Generate unique code
  const timestamp = Date.now().toString(36);
  const code = `LOYALTY${pointsValue}-${timestamp}`.toUpperCase();

  // Create price rule
  const priceRuleData = {
    price_rule: {
      title: `Loyalty ${pointsValue}pts - ${customerEmail}`,
      target_type: 'line_item',
      target_selection: 'all',
      allocation_method: 'across',
      value_type: 'fixed_amount',
      value: `-${discountAmount}.00`,
      customer_selection: 'prerequisite',
      prerequisite_customer_ids: [parseInt(customerIdNum)],
      usage_limit: 1,
      once_per_customer: true,
      starts_at: new Date().toISOString()
    }
  };

  const priceRule = shopifyREST('/price_rules.json', 'POST', priceRuleData);

  if (!priceRule.price_rule) {
    throw new Error('Failed to create price rule');
  }

  // Create discount code
  const discountCodeData = {
    discount_code: {
      code: code
    }
  };

  const discountCode = shopifyREST(
    `/price_rules/${priceRule.price_rule.id}/discount_codes.json`,
    'POST',
    discountCodeData
  );

  if (!discountCode.discount_code) {
    throw new Error('Failed to create discount code');
  }

  return code;
}

// ============================================================
// REDEMPTION HANDLER
// ============================================================

function handleRedemption(customerEmail, points) {
  Logger.log(`Redemption request: ${customerEmail}, ${points} points`);

  // Validate points value
  if (!REDEMPTION_TIERS[points]) {
    return {
      success: false,
      error: `Invalid points value. Must be one of: ${Object.keys(REDEMPTION_TIERS).join(', ')}`
    };
  }

  // Get customer
  const customer = getCustomerByEmail(customerEmail);

  if (!customer) {
    return {
      success: false,
      error: 'Customer not found'
    };
  }

  // Check sufficient balance
  if (customer.points < points) {
    return {
      success: false,
      error: `Insufficient points. You have ${customer.points}, need ${points}`
    };
  }

  const discountAmount = REDEMPTION_TIERS[points];

  try {
    // Create discount code
    const code = createDiscountCode(customer.id, customerEmail, points, discountAmount);

    // Deduct points
    const newPoints = customer.points - points;
    const newLifetimeRedeemed = customer.lifetimeRedeemed + points;

    // Add transaction to history
    const transaction = {
      date: new Date().toISOString(),
      action: 'redemption',
      points: -points,
      balance_after: newPoints,
      discount_code: code,
      discount_value: discountAmount
    };

    const history = customer.history;
    history.push(transaction);

    // Update customer metafields
    const success = updateCustomerPoints(customer.id, newPoints, history, newLifetimeRedeemed);

    if (!success) {
      Logger.log('Failed to update customer metafields');
      return {
        success: false,
        error: 'Failed to update points balance'
      };
    }

    Logger.log(`✅ Redemption successful: ${code}`);

    return {
      success: true,
      code: code,
      points: points,
      discount_value: discountAmount,
      new_balance: newPoints
    };

  } catch (error) {
    Logger.log(`❌ Redemption error: ${error.toString()}`);

    return {
      success: false,
      error: error.toString()
    };
  }
}

// ============================================================
// WEB APP ENTRY POINT
// ============================================================

function doPost(e) {
  try {
    const requestData = JSON.parse(e.postData.contents);
    const customerEmail = requestData.customer_email;
    const points = parseInt(requestData.points);

    if (!customerEmail || !points) {
      return ContentService.createTextOutput(JSON.stringify({
        success: false,
        error: 'Missing customer_email or points'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    const result = handleRedemption(customerEmail, points);

    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    Logger.log('❌ API error: ' + error.toString());

    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: 'Loyalty Redemption API',
    version: '1.0',
    endpoints: {
      'POST /redeem': {
        description: 'Redeem points for discount code',
        parameters: {
          customer_email: 'string (required)',
          points: 'integer (100, 200, 500, or 1000)'
        }
      }
    }
  })).setMimeType(ContentService.MimeType.JSON);
}

// ============================================================
// TESTING FUNCTION
// ============================================================

function testRedemption() {
  const testEmail = 'loyalty.test@alphamedical.shop';
  const testPoints = 100;

  const result = handleRedemption(testEmail, testPoints);

  Logger.log('Test redemption result:');
  Logger.log(JSON.stringify(result, null, 2));
}
