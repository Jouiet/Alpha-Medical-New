/**
 * Loyalty Webhooks Handler - Google Apps Script
 * Receives Shopify webhooks and manages loyalty points
 *
 * Webhooks to configure in Shopify Admin:
 * 1. customers/create → handleCustomerCreate()
 * 2. orders/paid → handleOrderPaid()
 *
 * Deploy as Web App: Execute as "Me", Access "Anyone"
 */

// Configuration
const SHOPIFY_STORE = 'azffej-as.myshopify.com';
const ADMIN_TOKEN = 'YOUR_SHOPIFY_ADMIN_TOKEN_HERE'; // Replace with token from .env.admin
const API_VERSION = '2024-10';

// Loyalty configuration
const TIER_THRESHOLDS = {
  bronze: 0,
  silver: 501,
  gold: 1501
};

const SIGNUP_BONUS = 50;

// ============================================================
// HELPER FUNCTIONS
// ============================================================

function calculateTier(points) {
  if (points >= TIER_THRESHOLDS.gold) return 'gold';
  if (points >= TIER_THRESHOLDS.silver) return 'silver';
  return 'bronze';
}

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

function getCustomerMetafields(customerId) {
  const query = `
    query GetCustomerMetafields($id: ID!) {
      customer(id: $id) {
        id
        email
        metafield_points: metafield(namespace: "loyalty", key: "points") { value }
        metafield_tier: metafield(namespace: "loyalty", key: "tier") { value }
        metafield_history: metafield(namespace: "loyalty", key: "history") { value }
        metafield_signup_bonus: metafield(namespace: "loyalty", key: "signup_bonus_claimed") { value }
        metafield_lifetime_earned: metafield(namespace: "loyalty", key: "lifetime_points_earned") { value }
        metafield_lifetime_redeemed: metafield(namespace: "loyalty", key: "lifetime_points_redeemed") { value }
      }
    }
  `;

  const result = shopifyGraphQL(query, { id: customerId });

  if (result.errors) {
    Logger.log('Error getting metafields: ' + JSON.stringify(result.errors));
    return null;
  }

  const customer = result.data.customer;

  return {
    customerId: customerId,
    email: customer.email,
    points: parseInt(customer.metafield_points?.value || 0),
    tier: customer.metafield_tier?.value || 'bronze',
    history: JSON.parse(customer.metafield_history?.value || '[]'),
    signupBonusClaimed: customer.metafield_signup_bonus?.value === 'true',
    lifetimeEarned: parseInt(customer.metafield_lifetime_earned?.value || 0),
    lifetimeRedeemed: parseInt(customer.metafield_lifetime_redeemed?.value || 0)
  };
}

function updateCustomerMetafields(customerId, points, tier, history, signupBonusClaimed, lifetimeEarned, lifetimeRedeemed) {
  const mutation = `
    mutation UpdateCustomerMetafields($input: CustomerInput!) {
      customerUpdate(input: $input) {
        customer { id }
        userErrors { field message }
      }
    }
  `;

  const input = {
    id: customerId,
    metafields: [
      { namespace: 'loyalty', key: 'points', value: String(points), type: 'number_integer' },
      { namespace: 'loyalty', key: 'tier', value: tier, type: 'single_line_text_field' },
      { namespace: 'loyalty', key: 'history', value: JSON.stringify(history), type: 'json' },
      { namespace: 'loyalty', key: 'signup_bonus_claimed', value: String(signupBonusClaimed), type: 'boolean' },
      { namespace: 'loyalty', key: 'lifetime_points_earned', value: String(lifetimeEarned), type: 'number_integer' },
      { namespace: 'loyalty', key: 'lifetime_points_redeemed', value: String(lifetimeRedeemed), type: 'number_integer' }
    ]
  };

  const result = shopifyGraphQL(mutation, { input });

  if (result.errors || result.data.customerUpdate.userErrors.length > 0) {
    Logger.log('Error updating metafields: ' + JSON.stringify(result));
    return false;
  }

  return true;
}

function addPoints(customerId, points, action, metadata = {}) {
  const loyalty = getCustomerMetafields(customerId);
  if (!loyalty) return false;

  const newPoints = loyalty.points + points;
  const newLifetimeEarned = loyalty.lifetimeEarned + points;
  const newTier = calculateTier(newPoints);

  const transaction = {
    date: new Date().toISOString(),
    action: action,
    points: points,
    balance_after: newPoints,
    ...metadata
  };

  const history = loyalty.history;
  history.push(transaction);

  const success = updateCustomerMetafields(
    customerId,
    newPoints,
    newTier,
    history,
    loyalty.signupBonusClaimed,
    newLifetimeEarned,
    loyalty.lifetimeRedeemed
  );

  if (success) {
    Logger.log(`✅ Added ${points} points to customer ${customerId} (${newPoints} total, ${newTier} tier)`);

    // Check tier upgrade
    if (newTier !== loyalty.tier) {
      Logger.log(`🎉 TIER UPGRADE: ${loyalty.tier} → ${newTier}`);
      // TODO: Send tier upgrade email via Klaviyo
    }
  }

  return success;
}

// ============================================================
// WEBHOOK HANDLERS
// ============================================================

function handleCustomerCreate(webhookData) {
  Logger.log('Processing customer/create webhook');

  const customerId = webhookData.admin_graphql_api_id;
  const email = webhookData.email;

  Logger.log(`Customer created: ${email} (${customerId})`);

  // Check if signup bonus already claimed
  const loyalty = getCustomerMetafields(customerId);

  if (!loyalty) {
    Logger.log('⚠️  Failed to get customer loyalty data');
    return;
  }

  if (loyalty.signupBonusClaimed) {
    Logger.log('ℹ️  Signup bonus already claimed');
    return;
  }

  // Award signup bonus
  const success = addPoints(customerId, SIGNUP_BONUS, 'signup_bonus');

  if (success) {
    // Mark signup bonus as claimed
    updateCustomerMetafields(
      customerId,
      SIGNUP_BONUS,
      'bronze',
      loyalty.history,
      true,  // signupBonusClaimed
      SIGNUP_BONUS,
      0
    );

    Logger.log(`✅ Awarded ${SIGNUP_BONUS} signup bonus to ${email}`);

    // TODO: Send welcome email with points info via Klaviyo
  }
}

function handleOrderPaid(webhookData) {
  Logger.log('Processing orders/paid webhook');

  const customerId = webhookData.customer?.admin_graphql_api_id;
  const orderTotal = parseFloat(webhookData.total_price);
  const orderId = webhookData.id;
  const orderName = webhookData.name;

  if (!customerId) {
    Logger.log('⚠️  No customer associated with order');
    return;
  }

  // Calculate points (1 point per $1)
  const points = Math.floor(orderTotal);

  if (points === 0) {
    Logger.log('ℹ️  Order total too low for points');
    return;
  }

  Logger.log(`Order ${orderName}: $${orderTotal} = ${points} points`);

  // Award purchase points
  const success = addPoints(customerId, points, 'purchase', {
    order_id: orderName,
    order_total: orderTotal
  });

  if (success) {
    Logger.log(`✅ Awarded ${points} points for order ${orderName}`);
  }
}

// ============================================================
// WEB APP ENTRY POINT
// ============================================================

function doPost(e) {
  try {
    const webhookTopic = e.parameter.topic || e.postData?.headers?.['X-Shopify-Topic'];
    const webhookData = JSON.parse(e.postData.contents);

    Logger.log(`Received webhook: ${webhookTopic}`);

    switch (webhookTopic) {
      case 'customers/create':
        handleCustomerCreate(webhookData);
        break;

      case 'orders/paid':
        handleOrderPaid(webhookData);
        break;

      default:
        Logger.log(`Unknown webhook topic: ${webhookTopic}`);
    }

    return ContentService.createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    Logger.log('❌ Webhook error: ' + error.toString());

    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// ============================================================
// TESTING FUNCTIONS
// ============================================================

function testSignupBonus() {
  // Test with a real customer ID
  const testCustomerId = 'gid://shopify/Customer/8042770759757';

  const loyalty = getCustomerMetafields(testCustomerId);
  Logger.log('Current loyalty data: ' + JSON.stringify(loyalty));

  if (!loyalty.signupBonusClaimed) {
    const success = addPoints(testCustomerId, SIGNUP_BONUS, 'signup_bonus');
    Logger.log('Signup bonus awarded: ' + success);
  } else {
    Logger.log('Signup bonus already claimed');
  }
}

function testPurchasePoints() {
  // Test with a real customer ID
  const testCustomerId = 'gid://shopify/Customer/8042770759757';
  const orderTotal = 150.00;
  const points = Math.floor(orderTotal);

  const success = addPoints(testCustomerId, points, 'purchase', {
    order_id: '#TEST001',
    order_total: orderTotal
  });

  Logger.log('Purchase points awarded: ' + success);

  // Check new balance
  const loyalty = getCustomerMetafields(testCustomerId);
  Logger.log('New balance: ' + JSON.stringify(loyalty));
}
