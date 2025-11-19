#!/usr/bin/env node
/**
 * CHECK SELLING PLANS STATUS - Verify subscription configuration
 *
 * Checks:
 * 1. Which selling plan groups exist
 * 2. Which products/bundles are assigned to selling plans
 * 3. Configuration of each selling plan
 *
 * NO ASSUMPTIONS - Only factual API data
 */

const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;

const BUNDLE_HANDLES = [
  'office-worker-essential-kit',
  'senior-mobility-support',
  'senior-advanced-arthritis',
  'chronic-pain-relief-kit',
  'ultimate-pain-management-system',
  'manual-labor-heavy-duty',
  'rehab-stroke-recovery',
  'chronic-pain-starter-kit'
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
            reject(new Error(`Parse error: ${data}`));
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
  console.log('🔍 CHECKING SELLING PLANS STATUS\n');
  console.log(`Store: ${SHOP}\n`);

  try {
    // Step 1: Get all selling plan groups
    console.log('📊 Step 1: Fetching selling plan groups...\n');

    const sellingPlansQuery = `{
      sellingPlanGroups(first: 10) {
        edges {
          node {
            id
            name
            description
            merchantCode
            productCount
            sellingPlans(first: 10) {
              edges {
                node {
                  id
                  name
                  description
                  billingPolicy {
                    ... on SellingPlanRecurringBillingPolicy {
                      interval
                      intervalCount
                    }
                  }
                  deliveryPolicy {
                    ... on SellingPlanRecurringDeliveryPolicy {
                      interval
                      intervalCount
                    }
                  }
                  pricingPolicies {
                    ... on SellingPlanFixedPricingPolicy {
                      adjustmentType
                      adjustmentValue {
                        ... on SellingPlanPricingPolicyPercentageValue {
                          percentage
                        }
                      }
                    }
                    ... on SellingPlanRecurringPricingPolicy {
                      adjustmentType
                      adjustmentValue {
                        ... on SellingPlanPricingPolicyPercentageValue {
                          percentage
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }`;

    const sellingPlansResult = await graphqlRequest(sellingPlansQuery);

    if (sellingPlansResult.errors) {
      console.error('❌ GraphQL Errors:', JSON.stringify(sellingPlansResult.errors, null, 2));
      return;
    }

    const sellingPlanGroups = sellingPlansResult.data?.sellingPlanGroups?.edges || [];

    console.log(`✅ Found ${sellingPlanGroups.length} selling plan group(s)\n`);

    if (sellingPlanGroups.length === 0) {
      console.log('⚠️  NO SELLING PLAN GROUPS FOUND');
      console.log('   Selling plans must be created in Shopify Admin:');
      console.log('   → Shopify Admin → Products → Subscriptions\n');
    } else {
      sellingPlanGroups.forEach((edge, index) => {
        const group = edge.node;
        console.log(`📦 Selling Plan Group #${index + 1}:`);
        console.log(`   ID: ${group.id}`);
        console.log(`   Name: ${group.name}`);
        console.log(`   Description: ${group.description || 'N/A'}`);
        console.log(`   Products Assigned: ${group.productCount}`);
        console.log(`   Selling Plans: ${group.sellingPlans.edges.length}`);

        if (group.sellingPlans.edges.length > 0) {
          group.sellingPlans.edges.forEach((planEdge, planIndex) => {
            const plan = planEdge.node;
            console.log(`\n   📋 Plan ${planIndex + 1}: ${plan.name}`);
            console.log(`      ID: ${plan.id}`);

            if (plan.deliveryPolicy) {
              console.log(`      Delivery: Every ${plan.deliveryPolicy.intervalCount} ${plan.deliveryPolicy.interval}(s)`);
            }

            if (plan.pricingPolicies && plan.pricingPolicies.length > 0) {
              plan.pricingPolicies.forEach(policy => {
                if (policy.adjustmentValue && policy.adjustmentValue.percentage) {
                  console.log(`      Discount: ${policy.adjustmentValue.percentage}% off`);
                }
              });
            }
          });
        }

        console.log('');
      });
    }

    // Step 2: Check if bundles have selling plans assigned
    console.log('\n📦 Step 2: Checking if bundles have selling plans...\n');

    const results = {
      withPlans: [],
      withoutPlans: []
    };

    for (const handle of BUNDLE_HANDLES) {
      try {
        const productQuery = `{
          productByHandle(handle: "${handle}") {
            id
            title
            handle
            requiresSellingPlan
            sellingPlanGroups(first: 5) {
              edges {
                node {
                  id
                  name
                }
              }
            }
          }
        }`;

        const productResult = await graphqlRequest(productQuery);

        if (productResult.data && productResult.data.productByHandle) {
          const product = productResult.data.productByHandle;
          const hasPlans = product.sellingPlanGroups.edges.length > 0;

          console.log(`${hasPlans ? '✅' : '❌'} ${handle}`);

          if (hasPlans) {
            console.log(`   Plans: ${product.sellingPlanGroups.edges.map(e => e.node.name).join(', ')}`);
            results.withPlans.push(handle);
          } else {
            console.log(`   ⚠️  No selling plans assigned`);
            results.withoutPlans.push(handle);
          }
        } else {
          console.log(`❌ ${handle} - Not found`);
        }

        await new Promise(r => setTimeout(r, 300)); // Rate limit

      } catch (error) {
        console.error(`❌ ${handle} - Error: ${error.message}`);
      }
    }

    // Summary
    console.log('\n📊 SUMMARY:\n');
    console.log(`   Selling Plan Groups: ${sellingPlanGroups.length}`);
    console.log(`   Bundles with plans: ${results.withPlans.length}/8`);
    console.log(`   Bundles without plans: ${results.withoutPlans.length}/8\n`);

    if (results.withoutPlans.length > 0) {
      console.log('⚠️  ACTION REQUIRED:');
      console.log('   Assign bundles to selling plan groups in Shopify Admin:');
      console.log('   1. Go to: Shopify Admin → Products → Subscriptions');
      console.log('   2. Click on selling plan group');
      console.log('   3. Click "Manage products"');
      console.log('   4. Add bundles:\n');
      results.withoutPlans.forEach(handle => {
        console.log(`      - ${handle}`);
      });
      console.log('');
    }

    if (sellingPlanGroups.length === 0) {
      console.log('🚨 CRITICAL:');
      console.log('   NO selling plan groups exist!');
      console.log('   Subscription widget will NOT appear until selling plans are created.\n');
      console.log('   NEXT STEPS:');
      console.log('   1. Create selling plan group in Shopify Admin');
      console.log('   2. Configure delivery frequency + discount');
      console.log('   3. Assign products/bundles to the group\n');
    }

    console.log('✅ CHECK COMPLETE\n');

  } catch (error) {
    console.error(`\n❌ ERROR: ${error.message}`);
    process.exit(1);
  }
}

main().catch(console.error);
