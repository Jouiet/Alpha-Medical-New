const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;
const BUNDLE_ID = 7623056031821; // Bundle 9 - Chronic Pain Starter Kit

const options = {
  hostname: SHOP,
  path: `/admin/api/2024-10/products/${BUNDLE_ID}.json`,
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
    const json = JSON.parse(data);
    if (json.product) {
      console.log('📦 BUNDLE:', json.product.title);
      console.log('📋 Status:', json.product.status);
      console.log('\n📝 BODY_HTML (first 500 chars):');
      console.log(json.product.body_html.substring(0, 500));
      console.log('\n...');
      console.log('\n🔍 Searching for product IDs...');
      const productIdMatches = json.product.body_html.match(/data-product-id="[^"]+"/g) || [];
      console.log(`Found ${productIdMatches.length} data-product-id attributes`);
      if (productIdMatches.length > 0) {
        console.log('Examples:', productIdMatches.slice(0, 3));
      }

      // Check for metafields that might store bundle products
      console.log('\n🔍 Checking metafields...');
      if (json.product.metafields && json.product.metafields.length > 0) {
        json.product.metafields.forEach(m => {
          console.log(`  - ${m.namespace}.${m.key}: ${m.value.substring(0, 100)}`);
        });
      } else {
        console.log('  No metafields found');
      }
    }
  });
});

req.on('error', console.error);
req.end();
