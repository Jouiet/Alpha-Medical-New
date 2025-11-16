#!/usr/bin/env node
/**
 * VERIFY INSTALLED APPS - Klaviyo connection check
 *
 * Checks:
 * 1. All installed apps
 * 2. Klaviyo connection (MUST be Alpha Medical, NOT Hendersonshop)
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
 * Make GraphQL request to Shopify Admin API
 */
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
  console.log('🔍 VERIFYING INSTALLED APPS - KLAVIYO CHECK\n');
  console.log(`Store: ${SHOP}\n`);

  try {
    // Query to get all installed apps
    const query = `{
      currentAppInstallation {
        id
        app {
          id
          title
          developerName
          handle
        }
      }
      appInstallations(first: 50) {
        edges {
          node {
            id
            app {
              id
              title
              handle
              developerName
              description
            }
            launchUrl
            uninstallUrl
          }
        }
      }
    }`;

    console.log('📊 Fetching installed apps via GraphQL...\n');

    const result = await graphqlRequest(query);

    if (result.errors) {
      console.error('❌ GraphQL Errors:', JSON.stringify(result.errors, null, 2));
      return;
    }

    if (result.data && result.data.appInstallations) {
      const apps = result.data.appInstallations.edges;

      console.log(`✅ FOUND ${apps.length} INSTALLED APP(S)\n`);

      let klaviyoFound = false;

      apps.forEach((edge, index) => {
        const app = edge.node.app;
        const installation = edge.node;

        console.log(`\n📍 App #${index + 1}:`);
        console.log(`   Title: ${app.title}`);
        console.log(`   Developer: ${app.developerName || 'N/A'}`);
        console.log(`   Handle: ${app.handle || 'N/A'}`);
        console.log(`   ID: ${app.id}`);

        if (app.description) {
          console.log(`   Description: ${app.description.substring(0, 100)}...`);
        }

        if (installation.launchUrl) {
          console.log(`   Launch URL: ${installation.launchUrl}`);
        }

        // Check for Klaviyo
        if (app.title.toLowerCase().includes('klaviyo') ||
            (app.handle && app.handle.toLowerCase().includes('klaviyo'))) {
          klaviyoFound = true;
          console.log(`\n   🚨 KLAVIYO DETECTED!`);
          console.log(`   📋 VERIFICATION NEEDED:`);
          console.log(`      - Launch app and verify connected store is "Alpha Medical"`);
          console.log(`      - NOT "Hendersonshop" or any other store`);
          console.log(`      - Launch URL: ${installation.launchUrl || 'N/A'}`);
        }

        // Check for other relevant apps
        if (app.title.toLowerCase().includes('loox')) {
          console.log(`   ✅ LOOX REVIEWS detected`);
        }

        if (app.title.toLowerCase().includes('recon')) {
          console.log(`   ✅ RECONVERT detected`);
        }

        if (app.title.toLowerCase().includes('subscription') ||
            app.title.toLowerCase().includes('recharge')) {
          console.log(`   ✅ SUBSCRIPTION APP detected`);
        }
      });

      console.log('\n\n📊 SUMMARY:');
      console.log(`   Total Apps: ${apps.length}`);
      console.log(`   Klaviyo Found: ${klaviyoFound ? '✅ YES' : '❌ NO'}`);

      if (klaviyoFound) {
        console.log('\n⚠️  MANUAL ACTION REQUIRED:');
        console.log('   1. Open Klaviyo app in Shopify Admin');
        console.log('   2. Go to Account Settings');
        console.log('   3. Verify connected store is "Alpha Medical"');
        console.log('   4. If connected to "Hendersonshop", disconnect and reconnect to Alpha Medical');
      }

    } else {
      console.log('⚠️  No app installations found or unexpected data structure');
      console.log(JSON.stringify(result, null, 2));
    }

  } catch (error) {
    console.error(`\n❌ ERROR: ${error.message}`);
    process.exit(1);
  }

  console.log('\n✅ VERIFICATION COMPLETE\n');
}

main().catch(console.error);
