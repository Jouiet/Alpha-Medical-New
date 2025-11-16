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

const FILES_TO_UPLOAD = [
  {
    path: 'sections/bundle-products-showcase.liquid',
    key: 'sections/bundle-products-showcase.liquid'
  },
  {
    path: 'sections/bundle-products-included.liquid',
    key: 'sections/bundle-products-included.liquid'
  },
  {
    path: 'templates/product.json',
    key: 'templates/product.json'
  }
];

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
  console.log('🚀 UPLOADING BUNDLE SECTIONS TO SHOPIFY...\n');
  console.log(`Theme: ${THEME_ID}`);
  console.log(`Files: ${FILES_TO_UPLOAD.length}\n`);

  const results = [];
  for (const file of FILES_TO_UPLOAD) {
    try {
      console.log(`⏳ Uploading ${file.key}...`);
      const result = await uploadAsset(file.path, file.key);
      results.push(result);
      console.log(`✅ ${file.key} uploaded successfully`);
      await new Promise(r => setTimeout(r, 500)); // Rate limit
    } catch (e) {
      console.error(`❌ Failed to upload ${file.key}:`, e.message);
      results.push({ success: false, key: file.key, error: e.message });
    }
  }

  console.log('\n📊 SUMMARY:');
  const successful = results.filter(r => r.success).length;
  console.log(`✅ Successful: ${successful}/${FILES_TO_UPLOAD.length}`);
  console.log(`❌ Failed: ${FILES_TO_UPLOAD.length - successful}/${FILES_TO_UPLOAD.length}`);

  if (successful === FILES_TO_UPLOAD.length) {
    console.log('\n🎉 ALL FILES UPLOADED SUCCESSFULLY!');
    console.log('\n✅ Bundle sections are now live on product pages.');
    console.log('🔍 Visit any bundle product to see the showcase section:');
    console.log('   https://www.alphamedical.shop/products/chronic-pain-starter-kit');
  } else {
    console.log('\n⚠️  Some files failed to upload. Check errors above.');
    process.exit(1);
  }
}

main().catch(console.error);
