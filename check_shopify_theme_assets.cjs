#!/usr/bin/env node
/**
 * CHECK SHOPIFY THEME ASSETS - Verify which widgets are deployed
 */

const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;
const THEME_ID = '140069830733';

const ASSETS_TO_CHECK = [
  'snippets/subscription-widget.liquid',
  'snippets/volume-pricing-widget.liquid',
  'snippets/smart-recommendations-section.liquid',
  'snippets/product-bundle-smart-cta.liquid',
  'sections/bundle-products-showcase.liquid',
  'templates/product.json'
];

if (!ACCESS_TOKEN) {
  console.error('❌ SHOPIFY_ADMIN_ACCESS_TOKEN not set');
  process.exit(1);
}

async function checkAsset(assetKey) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: SHOP,
      path: `/admin/api/2024-10/themes/${THEME_ID}/assets.json?asset[key]=${encodeURIComponent(assetKey)}`,
      method: 'GET',
      headers: {
        'X-Shopify-Access-Token': ACCESS_TOKEN
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const json = JSON.parse(data);
            resolve({
              key: assetKey,
              exists: !!json.asset,
              size: json.asset ? json.asset.size : 0,
              updated_at: json.asset ? json.asset.updated_at : null
            });
          } catch (e) {
            reject(new Error(`Parse error: ${e.message}`));
          }
        } else {
          resolve({ key: assetKey, exists: false, error: `HTTP ${res.statusCode}` });
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function main() {
  console.log('🔍 CHECKING SHOPIFY THEME ASSETS\n');
  console.log(`Theme ID: ${THEME_ID}\n`);

  const results = [];

  for (const assetKey of ASSETS_TO_CHECK) {
    try {
      console.log(`⏳ Checking: ${assetKey}`);
      const result = await checkAsset(assetKey);

      if (result.exists) {
        console.log(`   ✅ EXISTS (${result.size} bytes)`);
        console.log(`   📅 Updated: ${result.updated_at}`);
      } else {
        console.log(`   ❌ NOT FOUND ${result.error ? `(${result.error})` : ''}`);
      }
      console.log('');

      results.push(result);

      await new Promise(r => setTimeout(r, 300)); // Rate limit

    } catch (error) {
      console.error(`   ❌ ERROR: ${error.message}\n`);
      results.push({ key: assetKey, exists: false, error: error.message });
    }
  }

  // Summary
  const existing = results.filter(r => r.exists).length;
  const missing = results.filter(r => !r.exists).length;

  console.log('📊 SUMMARY:\n');
  console.log(`   ✅ Deployed: ${existing}/${ASSETS_TO_CHECK.length}`);
  console.log(`   ❌ Missing: ${missing}/${ASSETS_TO_CHECK.length}\n`);

  if (missing > 0) {
    console.log('❌ MISSING ASSETS:\n');
    results.filter(r => !r.exists).forEach(r => {
      console.log(`   - ${r.key}`);
    });
    console.log('');
  }

  console.log('✅ CHECK COMPLETE\n');
}

main().catch(console.error);
