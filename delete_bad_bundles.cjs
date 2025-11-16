const https = require('https');

const SHOP = 'azffej-as.myshopify.com';
const ACCESS_TOKEN = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN;

if (!ACCESS_TOKEN) {
  console.error('❌ SHOPIFY_ADMIN_ACCESS_TOKEN not set');
  process.exit(1);
}

// Bundles à SUPPRIMER (scores ≤ 5)
const BUNDLES_TO_DELETE = [
  { id: 7623056097357, handle: 'active-athlete-complete-protection', score: '2/10', reason: 'Drop foot neurologique + PostOp incompatibles' },
  { id: 7623086702669, handle: 'office-worker-premium-workspace', score: '3/10', reason: '75% beauty, mal catégorisé' },
  { id: 7623086833741, handle: 'beauty-wellness-led-complete', score: '4/10', reason: '3 LED masks redondants' },
  { id: 7623086604365, handle: 'post-surgery-recovery-complete', score: '4/10', reason: '4 chirurgies simultanées irréaliste' },
  { id: 7623056064589, handle: 'active-athlete-knee-specialist', score: '5/10', reason: '3 knee braces redondants' },
  { id: 7623086735437, handle: 'chronic-pain-whole-body', score: '5/10', reason: 'Face LED = beauty pas pain' },
  { id: 7623086669901, handle: 'office-worker-advanced-ergonomic', score: '5/10', reason: 'Eye massager beauty pas ergonomic' }
];

async function deleteBundle(bundleId) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: SHOP,
      path: `/admin/api/2024-10/products/${bundleId}.json`,
      method: 'DELETE',
      headers: {
        'X-Shopify-Access-Token': ACCESS_TOKEN
      }
    };

    const req = https.request(options, (res) => {
      if (res.statusCode === 200) {
        resolve({ success: true, id: bundleId });
      } else {
        let data = '';
        res.on('data', (chunk) => { data += chunk; });
        res.on('end', () => {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        });
      }
    });

    req.on('error', reject);
    req.end();
  });
}

async function main() {
  console.log('🗑️  SUPPRESSION DES BUNDLES INCOHÉRENTS...\n');
  console.log(`Total à supprimer: ${BUNDLES_TO_DELETE.length}/15 bundles\n`);

  const results = [];
  for (const bundle of BUNDLES_TO_DELETE) {
    try {
      console.log(`⏳ Suppression: ${bundle.handle}`);
      console.log(`   Score: ${bundle.score}`);
      console.log(`   Raison: ${bundle.reason}`);
      await deleteBundle(bundle.id);
      results.push({ ...bundle, deleted: true });
      console.log(`   ✅ SUPPRIMÉ\n`);
      await new Promise(r => setTimeout(r, 500)); // Rate limit
    } catch (e) {
      console.error(`   ❌ ERREUR: ${e.message}\n`);
      results.push({ ...bundle, deleted: false, error: e.message });
    }
  }

  console.log('📊 RÉSUMÉ:');
  const deleted = results.filter(r => r.deleted).length;
  console.log(`✅ Supprimés: ${deleted}/${BUNDLES_TO_DELETE.length}`);
  console.log(`❌ Échecs: ${BUNDLES_TO_DELETE.length - deleted}/${BUNDLES_TO_DELETE.length}`);

  console.log('\n✅ BUNDLES RESTANTS (cohérents):');
  console.log('1. office-worker-essential-kit (10/10) ⭐ PARFAIT');
  console.log('2. senior-mobility-support (10/10) ⭐ PARFAIT');
  console.log('3. senior-advanced-arthritis (9/10) EXCELLENT');
  console.log('4. chronic-pain-relief-kit (8/10) GOOD');
  console.log('5. ultimate-pain-management-system (8/10) GOOD');
  console.log('6. manual-labor-heavy-duty (7/10) OK');
  console.log('7. rehab-stroke-recovery (7/10) OK');
  console.log('8. chronic-pain-starter-kit (6/10) ⚠️ MOYEN');

  if (deleted === BUNDLES_TO_DELETE.length) {
    console.log('\n🎉 SUCCÈS! 7 bundles incohérents supprimés.');
    console.log('Reste 7-8 bundles avec vraies personas cohérentes.');
  }
}

main().catch(console.error);
