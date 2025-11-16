#!/usr/bin/env node
/**
 * UPLOAD UPDATED META-TAGS SNIPPET to Shopify
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;
const THEME_ID = '140069830733';

if (!ACCESS_TOKEN) {
  console.error('❌ SHOPIFY_ADMIN_ACCESS_TOKEN not set');
  process.exit(1);
}

async function uploadAsset(filePath, assetKey) {
  return new Promise((resolve, reject) => {
    const fullPath = path.join(__dirname, filePath);

    if (!fs.existsSync(fullPath)) {
      reject(new Error(`File not found: ${fullPath}`));
      return;
    }

    const fileContent = fs.readFileSync(fullPath, 'utf8');

    const payload = JSON.stringify({
      asset: {
        key: assetKey,
        value: fileContent
      }
    });

    const options = {
      hostname: SHOP,
      path: `/admin/api/2024-10/themes/${THEME_ID}/assets.json`,
      method: 'PUT',
      headers: {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode === 200) {
          resolve({ success: true, key: assetKey });
        } else {
          try {
            const json = JSON.parse(data);
            reject(new Error(`HTTP ${res.statusCode}: ${JSON.stringify(json)}`));
          } catch (e) {
            reject(new Error(`HTTP ${res.statusCode}: ${data}`));
          }
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

async function main() {
  console.log('🚀 UPLOADING META-TAGS SNIPPET TO SHOPIFY\n');
  console.log(`Theme: ${THEME_ID}\n`);

  try {
    console.log('⏳ Uploading snippets/meta-tags.liquid...');

    const result = await uploadAsset('snippets/meta-tags.liquid', 'snippets/meta-tags.liquid');

    if (result.success) {
      console.log(`✅ UPLOADED SUCCESSFULLY!`);
      console.log(`   Asset key: ${result.key}\n`);

      console.log('✅ CHANGES APPLIED:');
      console.log('   - Added fallback og:image using alpha-medical-social.png');
      console.log('   - Added fallback twitter:image using alpha-medical-social.png');
      console.log('   - Social sharing images now work even without theme settings\n');

      console.log('🔍 VERIFY:');
      console.log('   1. Visit: https://www.alphamedical.shop');
      console.log('   2. View page source');
      console.log('   3. Search for "og:image" - should show alpha-medical-social.png');
      console.log('   4. Test with Facebook Sharing Debugger:');
      console.log('      https://developers.facebook.com/tools/debug/\n');

      console.log('✅ META-TAGS UPDATE COMPLETE\n');
    }

  } catch (error) {
    console.error(`\n❌ UPLOAD FAILED: ${error.message}`);
    process.exit(1);
  }
}

main().catch(console.error);
