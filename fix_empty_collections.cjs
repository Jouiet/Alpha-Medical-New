#!/usr/bin/env node
/**
 * FIX EMPTY COLLECTIONS - Add SEO descriptions
 *
 * Collections to fix (from SEO_MARKETING_FORENSIC_ANALYSIS.md):
 * 1. bestsellers (13 products) - Empty description
 * 2. new-arrivals (20 products) - Empty description
 * 3. frontpage (0 products) - Empty description
 *
 * NO ASSUMPTIONS - Fetch current state, then update with SEO-optimized descriptions
 */

const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;

if (!ACCESS_TOKEN) {
  console.error('❌ SHOPIFY_ADMIN_ACCESS_TOKEN not set');
  process.exit(1);
}

// SEO-optimized descriptions for each collection
const COLLECTION_DESCRIPTIONS = {
  'bestsellers': {
    title: 'Bestsellers',
    description: `<p><strong>Discover Our Most Popular Medical Equipment</strong></p>

<p>Browse our bestselling medical equipment and ortho supports trusted by thousands of customers. These top-rated products combine professional-grade quality with proven pain relief effectiveness.</p>

<p><strong>Why Our Bestsellers?</strong></p>
<ul>
<li>✅ Highest customer satisfaction ratings (4.5+ stars)</li>
<li>✅ Clinically proven pain relief technology</li>
<li>✅ Professional-grade quality at affordable prices</li>
<li>✅ Fast shipping + 30-day money-back guarantee</li>
</ul>

<p>From knee braces to posture correctors, our bestsellers represent the most effective solutions for common pain points. Shop with confidence knowing you're choosing products verified by real customer results.</p>`,
    seo_title: 'Bestselling Medical Equipment & Ortho Supports | Alpha Medical',
    seo_description: 'Shop our bestselling medical equipment: knee braces, posture correctors, pain relief devices. Top-rated by 1000s of customers. Professional quality, affordable prices. Free shipping on orders $150+.'
  },
  'new-arrivals': {
    title: 'New Arrivals',
    description: `<p><strong>Latest Medical Equipment & Pain Relief Solutions</strong></p>

<p>Explore our newest arrivals in professional medical equipment and ortho supports. We continuously source innovative pain relief technologies to bring you cutting-edge solutions for better health.</p>

<p><strong>What's New:</strong></p>
<ul>
<li>🆕 Latest LED therapy devices for inflammation</li>
<li>🆕 Advanced posture correction technology</li>
<li>🆕 Next-generation compression supports</li>
<li>🆕 Innovative pain relief massagers</li>
</ul>

<p>All new arrivals undergo rigorous quality testing and are backed by our 30-day satisfaction guarantee. Be the first to experience the latest in medical equipment technology.</p>`,
    seo_title: 'New Arrivals: Latest Medical Equipment & Pain Relief Devices',
    seo_description: 'Discover the latest medical equipment and pain relief devices. New LED therapy, posture correctors, compression supports & massagers. Professional quality. Shop new arrivals now.'
  },
  'frontpage': {
    title: 'Home Page',
    description: `<p><strong>Professional Medical Equipment for Pain Relief & Recovery</strong></p>

<p>Alpha Medical provides professional-grade medical equipment and ortho supports for effective pain management and recovery. Trusted by healthcare professionals and patients worldwide.</p>

<p><strong>Featured Categories:</strong></p>
<ul>
<li>🩹 Knee Braces & Supports</li>
<li>🩹 Back & Lumbar Support</li>
<li>🩹 Posture Correctors</li>
<li>🩹 LED Therapy Devices</li>
<li>🩹 Pain Relief Massagers</li>
<li>🩹 Compression Supports</li>
</ul>

<p>Shop with confidence: Free shipping on orders $150+, 30-day money-back guarantee, and dedicated customer support. Your journey to pain-free living starts here.</p>`,
    seo_title: 'Professional Medical Equipment & Ortho Supports | Alpha Medical',
    seo_description: 'Professional medical equipment for pain relief & recovery. Knee braces, posture correctors, LED therapy, compression supports. Free shipping $150+. 30-day guarantee. Shop now.'
  }
};

/**
 * GraphQL mutation to update collection
 */
function updateCollection(collectionId, input) {
  return new Promise((resolve, reject) => {
    const mutation = `
      mutation collectionUpdate($input: CollectionInput!) {
        collectionUpdate(input: $input) {
          collection {
            id
            title
            handle
            description
            descriptionHtml
            seo {
              title
              description
            }
          }
          userErrors {
            field
            message
          }
        }
      }
    `;

    const variables = {
      input: {
        id: collectionId,
        ...input
      }
    };

    const payload = JSON.stringify({ query: mutation, variables });

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

/**
 * Get collection by handle
 */
function getCollectionByHandle(handle) {
  return new Promise((resolve, reject) => {
    const query = `{
      collectionByHandle(handle: "${handle}") {
        id
        title
        handle
        description
        descriptionHtml
        productsCount {
          count
        }
        seo {
          title
          description
        }
      }
    }`;

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
  console.log('🔧 FIXING EMPTY COLLECTIONS - SEO DESCRIPTIONS\n');
  console.log(`Store: ${SHOP}\n`);

  const collectionsToFix = ['bestsellers', 'new-arrivals', 'frontpage'];
  const results = [];

  for (const handle of collectionsToFix) {
    try {
      console.log(`\n📍 Processing: ${handle}`);
      console.log('   ⏳ Fetching current state...');

      const response = await getCollectionByHandle(handle);

      if (response.errors) {
        console.error(`   ❌ GraphQL Error: ${JSON.stringify(response.errors)}`);
        results.push({ handle, success: false, error: 'GraphQL error' });
        continue;
      }

      if (!response.data || !response.data.collectionByHandle) {
        console.log(`   ⚠️  Collection "${handle}" not found - may not exist`);
        results.push({ handle, success: false, error: 'Not found' });
        continue;
      }

      const collection = response.data.collectionByHandle;

      console.log(`   ✅ Found: ${collection.title}`);
      console.log(`   📊 Products: ${collection.productsCount?.count || 0}`);
      console.log(`   📝 Current description: ${collection.description ? collection.description.substring(0, 50) + '...' : 'EMPTY'}`);
      console.log(`   🔍 Current SEO title: ${collection.seo?.title || 'EMPTY'}`);
      console.log(`   🔍 Current SEO description: ${collection.seo?.description || 'EMPTY'}`);

      // Update collection with new description
      const updateData = COLLECTION_DESCRIPTIONS[handle];

      if (!updateData) {
        console.log(`   ⚠️  No description data found for "${handle}"`);
        results.push({ handle, success: false, error: 'No description data' });
        continue;
      }

      console.log(`\n   ⏳ Updating collection...`);

      const updateInput = {
        descriptionHtml: updateData.description,
        seo: {
          title: updateData.seo_title,
          description: updateData.seo_description
        }
      };

      const updateResponse = await updateCollection(collection.id, updateInput);

      if (updateResponse.errors || (updateResponse.data && updateResponse.data.collectionUpdate && updateResponse.data.collectionUpdate.userErrors.length > 0)) {
        console.error(`   ❌ Update failed:`, updateResponse.errors || updateResponse.data.collectionUpdate.userErrors);
        results.push({ handle, success: false, error: 'Update failed' });
        continue;
      }

      console.log(`   ✅ UPDATED successfully`);
      console.log(`   📝 New description: ${updateData.description.substring(0, 80)}...`);
      console.log(`   🔍 New SEO title: ${updateData.seo_title}`);
      console.log(`   🔍 New SEO description: ${updateData.seo_description.substring(0, 80)}...`);

      results.push({ handle, success: true });

      // Rate limiting
      await new Promise(r => setTimeout(r, 500));

    } catch (error) {
      console.error(`   ❌ ERROR: ${error.message}`);
      results.push({ handle, success: false, error: error.message });
    }
  }

  console.log('\n\n📊 SUMMARY:');
  const successful = results.filter(r => r.success).length;
  console.log(`   ✅ Successful: ${successful}/${collectionsToFix.length}`);
  console.log(`   ❌ Failed: ${collectionsToFix.length - successful}/${collectionsToFix.length}`);

  results.forEach(r => {
    if (r.success) {
      console.log(`   ✅ ${r.handle}`);
    } else {
      console.log(`   ❌ ${r.handle} - ${r.error}`);
    }
  });

  if (successful === collectionsToFix.length) {
    console.log('\n🎉 ALL COLLECTIONS UPDATED SUCCESSFULLY!');
  } else {
    console.log('\n⚠️  Some collections failed - check errors above');
    process.exit(1);
  }

  console.log('\n✅ COMPLETE\n');
}

main().catch(console.error);
