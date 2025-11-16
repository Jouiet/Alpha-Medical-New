#!/usr/bin/env node
/**
 * UPLOAD SOCIAL MEDIA IMAGE to Shopify Theme Assets
 *
 * Uploads alpha-medical-social.png (1200x630px) to theme assets
 * for use as og:image in social media sharing
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;
const THEME_ID = '140069830733'; // Alpha-Medical-New/main theme

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

    // Read file as base64
    const fileContent = fs.readFileSync(fullPath);
    const base64Content = fileContent.toString('base64');

    const payload = JSON.stringify({
      asset: {
        key: assetKey,
        attachment: base64Content
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
  console.log('🚀 UPLOADING SOCIAL MEDIA IMAGE TO SHOPIFY\n');
  console.log(`Theme: ${THEME_ID}`);
  console.log(`File: alpha-medical-social.png\n`);

  try {
    // Check if file exists
    const imagePath = 'alpha-medical-social.png';
    const fullPath = path.join(__dirname, imagePath);

    if (!fs.existsSync(fullPath)) {
      console.error(`❌ Image file not found: ${fullPath}`);
      process.exit(1);
    }

    // Get file stats
    const stats = fs.statSync(fullPath);
    const fileSizeKB = (stats.size / 1024).toFixed(2);

    console.log(`✅ Image file found`);
    console.log(`   Size: ${fileSizeKB} KB`);
    console.log(`   Path: ${fullPath}\n`);

    // Upload to theme assets
    console.log('⏳ Uploading to Shopify theme assets...');

    const result = await uploadAsset(imagePath, 'assets/alpha-medical-social.png');

    if (result.success) {
      console.log(`✅ UPLOADED SUCCESSFULLY!`);
      console.log(`   Asset key: ${result.key}`);
      console.log(`   Theme ID: ${THEME_ID}\n`);

      console.log('📝 NEXT STEPS:');
      console.log('   1. Go to Shopify Admin → Online Store → Themes → Customize');
      console.log('   2. Click Theme Settings (bottom left)');
      console.log('   3. Go to "Social media" section');
      console.log('   4. Upload alpha-medical-social.png as the social sharing image');
      console.log('   5. OR reference it directly in theme code:');
      console.log('      {{ "alpha-medical-social.png" | asset_url }}');

      console.log('\n✅ IMAGE UPLOAD COMPLETE\n');
    }

  } catch (error) {
    console.error(`\n❌ UPLOAD FAILED: ${error.message}`);
    process.exit(1);
  }
}

main().catch(console.error);
