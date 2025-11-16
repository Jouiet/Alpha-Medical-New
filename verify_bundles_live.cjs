const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;

if (!ACCESS_TOKEN) {
  console.error('❌ SHOPIFY_ADMIN_ACCESS_TOKEN not set');
  process.exit(1);
}

const BUNDLE_IDS = [
  7623055966285, // Bundle 1
  7623055999053, // Bundle 2
  7623056097357, // Bundle 3
  7623056162893, // Bundle 4
  7623086604365, // Bundle 5
  7623086637133, // Bundle 6
  7623086669901, // Bundle 7
  7623086702669, // Bundle 8
  7623056031821, // Bundle 9
  7623086735437, // Bundle 10
  7623056064589, // Bundle 11
  7623086768205, // Bundle 12
  7623086800973, // Bundle 13
  7623086833741, // Bundle 14
  7623086866509  // Bundle 15
];

async function verifyBundle(bundleId, index) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: SHOP,
      path: `/admin/api/2024-10/products/${bundleId}.json`,
      method: 'GET',
      headers: {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.product) {
            const html = json.product.body_html || '';
            const matches = html.match(/data-product-id="/g) || [];
            const productCount = matches.length;
            resolve({
              id: bundleId,
              index: index + 1,
              title: json.product.title,
              status: json.product.status,
              productCount: productCount,
              compliant: productCount >= 3 && productCount <= 4
            });
          } else {
            reject(new Error(`Bundle ${bundleId} not found`));
          }
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function main() {
  console.log('🔍 VERIFYING 15 BUNDLES ON LIVE SITE...\n');

  const results = [];
  for (let i = 0; i < BUNDLE_IDS.length; i++) {
    try {
      const result = await verifyBundle(BUNDLE_IDS[i], i);
      results.push(result);
      const emoji = result.compliant ? '✅' : '❌';
      const titleShort = result.title.substring(0, 50);
      console.log(`${emoji} Bundle ${result.index}: ${result.productCount} products - ${titleShort}`);
      await new Promise(r => setTimeout(r, 500)); // Rate limit
    } catch (e) {
      console.error(`❌ Error verifying ${BUNDLE_IDS[i]}:`, e.message);
    }
  }

  console.log('\n📊 SUMMARY:');
  const compliant = results.filter(r => r.compliant).length;
  const total = results.length;
  console.log(`✅ Compliant (3-4 products): ${compliant}/${total} (${(compliant/total*100).toFixed(1)}%)`);
  console.log(`❌ Non-compliant: ${total - compliant}/${total}`);

  if (compliant === total) {
    console.log('\n🎉 SUCCESS: All bundles compliant!');
  } else {
    console.log('\n⚠️  WARNING: Some bundles not compliant');
    results.filter(r => !r.compliant).forEach(r => {
      console.log(`   - Bundle ${r.index}: ${r.productCount} products`);
    });
  }
}

main().catch(console.error);
