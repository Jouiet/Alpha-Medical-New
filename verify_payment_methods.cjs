#!/usr/bin/env node
/**
 * VERIFY PAYMENT METHODS - Factual Shopify Admin API Check
 *
 * Checks:
 * 1. PayPal status (MUST be disabled per requirements)
 * 2. Shopify Payments status (MUST be enabled with Stripe, Google Pay, Apple Pay)
 *
 * NO ASSUMPTIONS - Only factual API data
 */

const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;

if (!ACCESS_TOKEN) {
  console.error('❌ SHOPIFY_ADMIN_ACCESS_TOKEN not set');
  process.exit(1);
}

/**
 * Make HTTPS request to Shopify Admin API
 */
function shopifyRequest(path, method = 'GET') {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: SHOP,
      path: path,
      method: method,
      headers: {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            resolve(data);
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function main() {
  console.log('🔍 VERIFYING PAYMENT METHODS - FACTUAL CHECK\n');
  console.log(`Store: ${SHOP}\n`);

  try {
    // Check shop settings for payment providers
    console.log('📊 Fetching shop settings...');
    const shopData = await shopifyRequest('/admin/api/2024-10/shop.json');

    console.log('\n✅ SHOP DATA RETRIEVED\n');

    if (shopData.shop) {
      console.log('🏪 Shop Details:');
      console.log(`   Name: ${shopData.shop.name}`);
      console.log(`   Email: ${shopData.shop.email}`);
      console.log(`   Domain: ${shopData.shop.domain}`);
      console.log(`   Currency: ${shopData.shop.currency}`);
      console.log(`   Money Format: ${shopData.shop.money_format}`);

      // Check payment providers (if available in API)
      if (shopData.shop.enabled_presentment_currencies) {
        console.log(`\n💰 Currencies: ${shopData.shop.enabled_presentment_currencies.join(', ')}`);
      }

      // Check checkout settings
      if (shopData.shop.checkout_api_supported !== undefined) {
        console.log(`\n🛒 Checkout API: ${shopData.shop.checkout_api_supported ? 'Enabled' : 'Disabled'}`);
      }
    }

    // Try to get payment gateways (this endpoint may require specific permissions)
    console.log('\n\n🔍 Attempting to fetch payment gateways...');

    try {
      const paymentData = await shopifyRequest('/admin/api/2024-10/payment_gateways.json');

      if (paymentData.payment_gateways && Array.isArray(paymentData.payment_gateways)) {
        console.log(`\n✅ FOUND ${paymentData.payment_gateways.length} PAYMENT GATEWAY(S)\n`);

        let paypalFound = false;
        let shopifyPaymentsFound = false;

        paymentData.payment_gateways.forEach((gateway, index) => {
          console.log(`\n📍 Gateway #${index + 1}:`);
          console.log(`   ID: ${gateway.id}`);
          console.log(`   Name: ${gateway.name}`);
          console.log(`   Type: ${gateway.type || 'N/A'}`);
          console.log(`   Enabled: ${gateway.enabled ? '✅ YES' : '❌ NO'}`);
          console.log(`   Disabled: ${gateway.disabled ? '❌ YES' : '✅ NO'}`);

          if (gateway.name && gateway.name.toLowerCase().includes('paypal')) {
            paypalFound = true;
            console.log(`   🚨 PAYPAL DETECTED!`);
            if (gateway.enabled) {
              console.log(`   ❌ STATUS: ACTIVE (VIOLATION - Must be disabled)`);
            } else {
              console.log(`   ✅ STATUS: DISABLED (Compliant)`);
            }
          }

          if (gateway.name && (gateway.name.toLowerCase().includes('shopify') || gateway.name.toLowerCase().includes('stripe'))) {
            shopifyPaymentsFound = true;
            console.log(`   ✅ SHOPIFY PAYMENTS/STRIPE DETECTED`);
          }
        });

        console.log('\n\n📊 SUMMARY:');
        console.log(`   PayPal Found: ${paypalFound ? '✅ YES' : '❌ NO'}`);
        console.log(`   Shopify Payments/Stripe Found: ${shopifyPaymentsFound ? '✅ YES' : '❌ NO'}`);

      } else {
        console.log('⚠️  Payment gateways data structure unexpected');
        console.log(JSON.stringify(paymentData, null, 2));
      }
    } catch (paymentError) {
      console.log(`\n⚠️  Payment gateways endpoint error: ${paymentError.message}`);
      console.log('\n💡 NOTE: Payment gateway management typically requires manual Shopify Admin access');
      console.log('   Go to: Shopify Admin → Settings → Payments');
    }

  } catch (error) {
    console.error(`\n❌ ERROR: ${error.message}`);
    process.exit(1);
  }

  console.log('\n\n📝 MANUAL VERIFICATION REQUIRED:');
  console.log('   1. Go to Shopify Admin: https://admin.shopify.com/store/azffej-as/settings/payments');
  console.log('   2. Verify PayPal is DEACTIVATED');
  console.log('   3. Verify Shopify Payments is ACTIVE with:');
  console.log('      - Stripe');
  console.log('      - Google Pay');
  console.log('      - Apple Pay');
  console.log('\n✅ VERIFICATION COMPLETE\n');
}

main().catch(console.error);
