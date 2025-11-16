const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;
const BUNDLE_ID = 7623056031821; // Chronic Pain Starter Kit

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
      console.log('\n📝 BODY_HTML:');
      console.log(json.product.body_html);
      console.log('\n🔍 Extracting product list...');

      const lines = json.product.body_html.split('\n');
      const products = [];
      lines.forEach(line => {
        if (line.includes('<li>') && line.includes('✓')) {
          const clean = line.replace(/<[^>]+>/g, '').replace('✓', '').trim();
          if (clean) products.push(clean);
        }
      });

      console.log(`\nProducts listed: ${products.length}`);
      products.forEach((p, i) => {
        console.log(`  ${i + 1}. ${p}`);
      });
    }
  });
});

req.on('error', console.error);
req.end();
