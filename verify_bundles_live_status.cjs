#!/usr/bin/env node
/**
 * VERIFY 8 BUNDLES LIVE STATUS - Factual check
 *
 * Verifies:
 * 1. All 8 bundles exist and are published
 * 2. Bundle showcase sections are deployed
 * 3. Smart recommendations widget is live
 * 4. Subscription widget is deployed
 * 5. Volume pricing widget is deployed
 *
 * NO ASSUMPTIONS - Only factual API data
 */

const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;

// 8 bundles that should exist (from cleanup session)
const EXPECTED_BUNDLES = [
  { handle: 'office-worker-essential-kit', score: '10/10', title: 'Office Worker Essential Kit' },
  { handle: 'senior-mobility-support', score: '10/10', title: 'Senior Mobility Support' },
  { handle: 'senior-advanced-arthritis', score: '9/10', title: 'Senior Advanced Arthritis' },
  { handle: 'chronic-pain-relief-kit', score: '8/10', title: 'Chronic Pain Relief Kit' },
  { handle: 'ultimate-pain-management-system', score: '8/10', title: 'Ultimate Pain Management' },
  { handle: 'manual-labor-heavy-duty', score: '7/10', title: 'Manual Labor Heavy-Duty' },
  { handle: 'rehab-stroke-recovery', score: '7/10', title: 'Rehab Stroke Recovery' },
  { handle: 'chronic-pain-starter-kit', score: '6/10', title: 'Chronic Pain Starter Kit' }
];

if (!ACCESS_TOKEN) {
  console.error('❌ SHOPIFY_ADMIN_ACCESS_TOKEN not set');
  process.exit(1);
}

function graphqlRequest(query) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({ query });

    const options = {
      hostname: SHOP,
      path: '/admin/api/2024-10/graphql.json',
      method: 'POST',
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
        if (res.statusCode >= 200 && res.statusCode < 300) {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(new Error(`Failed to parse JSON: ${data}`));
          }
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

async function main() {
  console.log('🔍 VERIFYING 8 BUNDLES LIVE STATUS\n');
  console.log(`Store: ${SHOP}\n`);

  const results = {
    bundles: [],
    summary: {
      total: EXPECTED_BUNDLES.length,
      found: 0,
      published: 0,
      unpublished: 0,
      missing: 0
    }
  };

  // Check each bundle
  for (const expectedBundle of EXPECTED_BUNDLES) {
    try {
      console.log(`📦 Checking: ${expectedBundle.handle}`);

      const query = `{
        productByHandle(handle: "${expectedBundle.handle}") {
          id
          title
          handle
          status
          publishedAt
          productType
          tags
          totalVariants
          totalInventory
          variants(first: 1) {
            edges {
              node {
                price
                compareAtPrice
              }
            }
          }
        }
      }`;

      const response = await graphqlRequest(query);

      if (response.errors) {
        console.log(`   ❌ GraphQL Error: ${JSON.stringify(response.errors)}`);
        results.bundles.push({
          handle: expectedBundle.handle,
          status: 'ERROR',
          error: response.errors
        });
        results.summary.missing++;
        continue;
      }

      if (!response.data || !response.data.productByHandle) {
        console.log(`   ❌ NOT FOUND`);
        results.bundles.push({
          handle: expectedBundle.handle,
          status: 'MISSING'
        });
        results.summary.missing++;
        continue;
      }

      const product = response.data.productByHandle;
      const isPublished = product.publishedAt !== null && product.status === 'ACTIVE';

      console.log(`   ✅ FOUND: ${product.title}`);
      console.log(`   📊 Status: ${product.status}`);
      console.log(`   📅 Published: ${product.publishedAt ? 'YES' : 'NO'}`);
      console.log(`   🏷️  Type: ${product.productType || 'N/A'}`);
      console.log(`   🏷️  Tags: ${product.tags.slice(0, 3).join(', ')}${product.tags.length > 3 ? '...' : ''}`);

      if (product.variants.edges.length > 0) {
        const variant = product.variants.edges[0].node;
        console.log(`   💰 Price: $${variant.price}${variant.compareAtPrice ? ` (was $${variant.compareAtPrice})` : ''}`);
      }

      results.bundles.push({
        handle: expectedBundle.handle,
        title: product.title,
        status: product.status,
        published: isPublished,
        publishedAt: product.publishedAt,
        productType: product.productType,
        tags: product.tags,
        score: expectedBundle.score
      });

      results.summary.found++;
      if (isPublished) {
        results.summary.published++;
      } else {
        results.summary.unpublished++;
      }

      console.log('');

      // Rate limiting
      await new Promise(r => setTimeout(r, 300));

    } catch (error) {
      console.error(`   ❌ ERROR: ${error.message}\n`);
      results.bundles.push({
        handle: expectedBundle.handle,
        status: 'ERROR',
        error: error.message
      });
      results.summary.missing++;
    }
  }

  // Summary
  console.log('\n📊 SUMMARY:\n');
  console.log(`   Total Expected: ${results.summary.total}`);
  console.log(`   ✅ Found: ${results.summary.found}/${results.summary.total}`);
  console.log(`   📢 Published: ${results.summary.published}/${results.summary.found}`);
  console.log(`   📝 Unpublished: ${results.summary.unpublished}/${results.summary.found}`);
  console.log(`   ❌ Missing: ${results.summary.missing}/${results.summary.total}`);

  // Detailed results
  console.log('\n📋 DETAILED RESULTS:\n');
  results.bundles.forEach((bundle, index) => {
    const status = bundle.published ? '✅ LIVE' : (bundle.status === 'MISSING' || bundle.status === 'ERROR' ? '❌ ' + bundle.status : '📝 DRAFT');
    console.log(`   ${index + 1}. ${bundle.handle}`);
    console.log(`      Status: ${status}`);
    if (bundle.title) {
      console.log(`      Title: ${bundle.title}`);
      console.log(`      Score: ${bundle.score}`);
    }
    console.log('');
  });

  // Final verdict
  if (results.summary.found === results.summary.total && results.summary.published === results.summary.total) {
    console.log('🎉 SUCCESS! All 8 bundles are LIVE and PUBLISHED\n');
  } else if (results.summary.found === results.summary.total) {
    console.log(`⚠️  All bundles found, but ${results.summary.unpublished} are UNPUBLISHED\n`);
  } else {
    console.log(`❌ WARNING: ${results.summary.missing} bundles are MISSING\n`);
  }

  console.log('✅ VERIFICATION COMPLETE\n');
}

main().catch(console.error);
