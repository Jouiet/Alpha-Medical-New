#!/usr/bin/env python3
"""
Bundler App - Frequently Bought Together (FBT) Configuration
10 high-impact product bundles for AOV +15-20% increase

Implementation: Manual via Bundler app UI
"""

print("="*80)
print("BUNDLER APP - FREQUENTLY BOUGHT TOGETHER (FBT) CONFIGURATION")
print("="*80)
print()

print("APP INFO:")
print("  Name: Bundler - Product Bundles")
print("  Status: ✅ INSTALLED")
print("  Purpose: FBT recommendations to increase AOV")
print("  Expected Impact: +15-20% AOV, $800-1,200/month revenue")
print("  Bundle Acceptance Target: 8-12%")
print()

print("="*80)
print("CONFIGURATION OVERVIEW")
print("="*80)
print()
print("BUNDLES TO CREATE: 10 priority configurations")
print("PRODUCTS ANALYZED: 153 across 6 categories")
print("ESTIMATED TIME: 1-2 hours total (10-12 min per bundle)")
print("DISCOUNT STRATEGY: 5-10% bundle discount")
print()

print("="*80)
print("MANUAL CONFIGURATION STEPS (1-2 hours)")
print("="*80)
print()

print("STEP 1: ACCESS BUNDLER APP")
print("-" * 40)
print("1. Shopify Admin → Apps → Bundler - Product Bundles")
print("2. If first time, complete onboarding wizard")
print("3. You'll land on Bundler dashboard")
print("4. Click 'Frequently Bought Together' or 'Create Bundle'")
print()

print("STEP 2: UNDERSTAND BUNDLE CREATION WORKFLOW")
print("-" * 40)
print("For each bundle configuration, you will:")
print("  1. Select main product (trigger product)")
print("  2. Add 1-2 complementary products")
print("  3. Set bundle discount (5-10%)")
print("  4. Configure display settings")
print("  5. Enable on product page")
print("  6. Save and test")
print()

print("="*80)
print("BUNDLE CONFIGURATIONS (PRIORITY ORDER)")
print("="*80)
print()

bundles = [
    {
        "priority": 1,
        "name": "Neck Pain Relief Bundle",
        "main_product": {
            "name": "Portable Neck Massager | Smart Shoulder Cervical Relief",
            "handle": "portable-neck-massager-smart-shoulder-cervical-relief"
        },
        "fbt_products": [
            {
                "name": "Heat & Music Eye Massager",
                "handle": "heat-music-eye-massager-migraine-eye-fatigue-relief"
            },
            {
                "name": "Shoulder Vibration Massager",
                "handle": "shoulder-vibration-massager-electric-neck-cervical"
            }
        ],
        "rationale": "Neck pain sufferers often have related issues (headaches, shoulder tension)",
        "discount": "10%",
        "aov_increase": "+25-35%",
        "category": "Neck/Cervical"
    },
    {
        "priority": 2,
        "name": "Complete Knee Recovery System",
        "main_product": {
            "name": "Spring Knee Booster | Elderly Climbing Power Support",
            "handle": "spring-knee-booster-elderly-climbing-power-support"
        },
        "fbt_products": [
            {
                "name": "Foreverlily Smart Knee Massager",
                "handle": "foreverlily-smart-knee-massager-vibration-air-pressure"
            },
            {
                "name": "Air Compression Leg Massager",
                "handle": "air-compression-leg-massager-3-modes-heat-therapy"
            }
        ],
        "rationale": "Complete knee + leg recovery system for mobility issues",
        "discount": "10%",
        "aov_increase": "+30-40%",
        "category": "Knee/Joint"
    },
    {
        "priority": 3,
        "name": "Back Support & Therapy Bundle",
        "main_product": {
            "name": "Back Support Brace | Adjustable Posture Corrector",
            "handle": "back-support-brace-adjustable-posture-corrector"
        },
        "fbt_products": [
            {
                "name": "Electric Lumbar Massager",
                "handle": "electric-lumbar-massager-heated-vibration-back-brace"
            },
            {
                "name": "Air Compression Leg Massager",
                "handle": "air-compression-leg-massager-3-modes-heat-therapy"
            }
        ],
        "rationale": "Back pain patients need both support and therapy",
        "discount": "10%",
        "aov_increase": "+25-30%",
        "category": "Back/Posture"
    },
    {
        "priority": 4,
        "name": "Complete Facial Care System",
        "main_product": {
            "name": "2-in-1 LED Face & Body Mask | 7 Colors + Heating",
            "handle": "2-in-1-led-face-body-mask-7-colors-heating"
        },
        "fbt_products": [
            {
                "name": "Anti-Aging LED Eye Mask",
                "handle": "anti-aging-led-eye-mask-photon-therapy-for-dark-circles"
            },
            {
                "name": "Electric Gua Sha Board",
                "handle": "electric-gua-sha-board-vibration-massage-hot-compress"
            }
        ],
        "rationale": "Complete facial care system (light therapy + massage)",
        "discount": "10%",
        "aov_increase": "+35-45%",
        "category": "LED Light Therapy"
    },
    {
        "priority": 5,
        "name": "Full Body Toning System",
        "main_product": {
            "name": "EMS Body Sculptor | Wireless Butt Trainer",
            "handle": "ems-body-sculptor-wireless-butt-trainer-29-levels"
        },
        "fbt_products": [
            {
                "name": "EMS Abdominal Belt",
                "handle": "ems-abdominal-belt-usb-rechargeable-muscle-toner"
            },
            {
                "name": "Smart Hip Trainer",
                "handle": "smart-hip-trainer-ems-vibration-muscle-stimulator"
            }
        ],
        "rationale": "Full body toning system for fitness enthusiasts",
        "discount": "10%",
        "aov_increase": "+30-40%",
        "category": "EMS/Electrical"
    },
    {
        "priority": 6,
        "name": "Body Sculpting & Drainage System",
        "main_product": {
            "name": "Lymphatic Drainage Brush | Electric EMS Body Massage Tool",
            "handle": "lymphatic-drainage-brush-electric-ems-body-massage-tool"
        },
        "fbt_products": [
            {
                "name": "Electric Gua Sha Board",
                "handle": "electric-gua-sha-board-vibration-massage-hot-compress"
            },
            {
                "name": "EMS Body Sculptor",
                "handle": "ems-body-sculptor-wireless-butt-trainer-29-levels"
            }
        ],
        "rationale": "Complete body sculpting and drainage system",
        "discount": "10%",
        "aov_increase": "+25-35%",
        "category": "Massage Therapy"
    },
    {
        "priority": 7,
        "name": "Eye Care + Sleep Quality Bundle",
        "main_product": {
            "name": "Heat & Music Eye Massager",
            "handle": "heat-music-eye-massager-migraine-eye-fatigue-relief"
        },
        "fbt_products": [
            {
                "name": "Anti-Aging LED Eye Mask",
                "handle": "anti-aging-led-eye-mask-photon-therapy-for-dark-circles"
            },
            {
                "name": "Sleep Mask with Bluetooth 5.3",
                "handle": "sleep-mask-with-bluetooth-5-3-headphones-for-sleep"
            }
        ],
        "rationale": "Complete eye care + sleep quality system",
        "discount": "10%",
        "aov_increase": "+20-30%",
        "category": "Massage Therapy"
    },
    {
        "priority": 8,
        "name": "Multi-Modal Neck Therapy",
        "main_product": {
            "name": "8 Mode EMS Neck Massager",
            "handle": "8-mode-ems-neck-massager-remote-control-pain-relief"
        },
        "fbt_products": [
            {
                "name": "LED Face & Neck Mask",
                "handle": "led-face-neck-mask-red-light-infrared-therapy"
            },
            {
                "name": "Electric Gua Sha Board",
                "handle": "electric-gua-sha-board-vibration-massage-hot-compress"
            }
        ],
        "rationale": "Multi-modal neck therapy (EMS + light + massage)",
        "discount": "10%",
        "aov_increase": "+30-40%",
        "category": "Neck/Cervical"
    },
    {
        "priority": 9,
        "name": "Post-Surgery Knee Recovery",
        "main_product": {
            "name": "Hinged Knee Brace | Post-Op ROM Adjustable Recovery",
            "handle": "hinged-knee-brace-post-op-rom-adjustable-recovery"
        },
        "fbt_products": [
            {
                "name": "Foreverlily Smart Knee Massager",
                "handle": "foreverlily-smart-knee-massager-vibration-air-pressure"
            }
        ],
        "rationale": "Post-surgery recovery support + therapy",
        "discount": "10%",
        "aov_increase": "+20-25%",
        "category": "Knee/Joint"
    },
    {
        "priority": 10,
        "name": "Professional Anti-Aging System",
        "main_product": {
            "name": "Red Light Therapy Face Mask",
            "handle": "red-light-therapy-face-mask-3-wavelength-rejuvenation"
        },
        "fbt_products": [
            {
                "name": "V-Line Face Slimming | EMS Lifting",
                "handle": "v-line-face-slimming-ems-lifting-microcurrent-device"
            },
            {
                "name": "Anti-Aging LED Eye Mask",
                "handle": "anti-aging-led-eye-mask-photon-therapy-for-dark-circles"
            }
        ],
        "rationale": "Professional anti-aging system (light + EMS + eye care)",
        "discount": "10%",
        "aov_increase": "+35-45%",
        "category": "LED Light Therapy"
    }
]

for bundle in bundles:
    print("="*80)
    print(f"BUNDLE #{bundle['priority']}: {bundle['name']}")
    print("="*80)
    print()

    print(f"CATEGORY: {bundle['category']}")
    print(f"EXPECTED AOV INCREASE: {bundle['aov_increase']}")
    print(f"RECOMMENDED DISCOUNT: {bundle['discount']}")
    print()

    print("CONFIGURATION STEPS:")
    print("-" * 40)
    print()

    print("1. CREATE BUNDLE")
    print(f"   - In Bundler app, click 'Create Bundle' or 'Add FBT'")
    print(f"   - Bundle type: Frequently Bought Together")
    print(f"   - Bundle name: '{bundle['name']}'")
    print()

    print("2. SELECT MAIN PRODUCT")
    print(f"   - Search for product handle: {bundle['main_product']['handle']}")
    print(f"   - Or search by name: {bundle['main_product']['name']}")
    print(f"   - Click 'Select' to set as main product")
    print()

    print("3. ADD COMPLEMENTARY PRODUCTS")
    for i, fbt_product in enumerate(bundle['fbt_products'], 1):
        print(f"   FBT Product {i}:")
        print(f"   - Search for handle: {fbt_product['handle']}")
        print(f"   - Or search by name: {fbt_product['name']}")
        print(f"   - Click 'Add to Bundle'")
    print()

    print("4. CONFIGURE BUNDLE SETTINGS")
    print(f"   - Discount type: Percentage")
    print(f"   - Discount value: {bundle['discount']}")
    print(f"   - Apply to: All products in bundle")
    print(f"   - Display on: Product page only")
    print()

    print("5. CUSTOMIZE DISPLAY")
    print(f"   - Widget title: 'Frequently Bought Together'")
    print(f"   - Button text: 'Add All to Cart'")
    print(f"   - Show savings: ✅ Yes")
    print(f"   - Show individual prices: ✅ Yes")
    print(f"   - Widget position: Below product description")
    print()

    print("6. BUNDLE RATIONALE")
    print(f"   {bundle['rationale']}")
    print()

    print("7. SAVE & ENABLE")
    print(f"   - Click 'Save Bundle'")
    print(f"   - Toggle 'Active' to ON")
    print(f"   - Verify status shows: '✅ Active'")
    print()

    print("8. TEST ON FRONTEND")
    print(f"   - Visit product page: https://azffej-as.myshopify.com/products/{bundle['main_product']['handle']}")
    print(f"   - Verify FBT widget appears")
    print(f"   - Check discount calculation is correct")
    print(f"   - Test 'Add All to Cart' button")
    print(f"   - Verify all products added to cart")
    print()

print("="*80)
print("STYLING & BRANDING")
print("="*80)
print()
print("WIDGET DESIGN SETTINGS:")
print("-" * 40)
print("1. In Bundler → Settings → Design")
print("2. Widget style:")
print("   - Primary color: #4770DB (brand blue)")
print("   - Button style: Solid, rounded corners")
print("   - Font family: Inherit from theme")
print("   - Border radius: 4px")
print()
print("3. Layout:")
print("   - Display type: Horizontal (side-by-side)")
print("   - Image size: Medium")
print("   - Show product variants: ✅ Yes")
print()
print("4. Copy/Messaging:")
print("   - Widget title: 'Frequently Bought Together'")
print("   - Savings text: 'Save [discount]% when you buy together'")
print("   - Button text: 'Add All to Cart'")
print()

print("="*80)
print("GLOBAL SETTINGS")
print("="*80)
print()
print("1. In Bundler → Settings → General")
print("2. Configure:")
print("   - Show on product page: ✅ Enabled")
print("   - Show on collection page: ❌ Disabled")
print("   - Show on cart page: ❌ Disabled")
print("   - Auto-select items: ✅ Yes (pre-check all items)")
print("   - Show total savings: ✅ Yes")
print()
print("3. Performance:")
print("   - Lazy load: ✅ Enabled")
print("   - Cache bundles: ✅ Enabled")
print()

print("="*80)
print("TESTING CHECKLIST")
print("="*80)
print()
print("For each bundle, verify:")
print("  ✓ Widget appears on correct product page")
print("  ✓ All FBT products display with images")
print("  ✓ Discount calculation is accurate")
print("  ✓ 'Add All to Cart' button works")
print("  ✓ Products added to cart at bundle price")
print("  ✓ Cart shows bundle discount applied")
print("  ✓ Mobile responsive (test on phone)")
print("  ✓ Page load speed acceptable (<3s)")
print()

print("TEST SCENARIOS:")
print("-" * 40)
print("1. Visit: https://azffej-as.myshopify.com/products/portable-neck-massager-smart-shoulder-cervical-relief")
print("   Expected: See Eye Massager + Shoulder Massager bundle")
print()
print("2. Click 'Add All to Cart'")
print("   Expected: All 3 products added, 10% discount applied")
print()
print("3. Check cart total")
print("   Expected: Bundle discount shows in cart")
print()
print("4. Complete test purchase")
print("   Expected: Discount carries through to checkout")
print()

print("="*80)
print("MONITORING & OPTIMIZATION")
print("="*80)
print()
print("WEEK 1-2: BASELINE METRICS")
print("-" * 40)
print("1. Bundler Dashboard → Analytics")
print("2. Track for each bundle:")
print("   - Impressions (how many times shown)")
print("   - Click rate ('Add All to Cart' clicks)")
print("   - Conversion rate (actual purchases)")
print("   - Revenue generated")
print()

print("WEEKLY REVIEW:")
print("-" * 40)
print("1. Identify top 3 performing bundles")
print("2. Identify bottom 3 performing bundles")
print("3. For underperformers:")
print("   - Test different discount (5% vs 10%)")
print("   - Try different complementary products")
print("   - Adjust bundle positioning")
print()

print("TARGET METRICS:")
print("-" * 40)
print("  Bundle Acceptance Rate: >8% (industry average)")
print("  AOV Increase: +15-20%")
print("  Revenue from Bundles: $800-1,200/month")
print()
print("CALCULATION:")
print("  - 50 orders/month with bundle opportunity")
print("  - × 10% acceptance rate")
print("  - = 5 bundle orders/month")
print("  - × $160 average bundle value (vs $100 single product)")
print("  - = $800/month additional revenue")
print()

print("="*80)
print("OPTIMIZATION STRATEGIES")
print("="*80)
print()

print("STRATEGY 1: A/B TEST DISCOUNTS")
print("-" * 40)
print("Week 1-2: Run all bundles at 10% discount")
print("Week 3-4: Test top 5 bundles at 5% discount")
print("Week 5+: Use winning discount level")
print("Hypothesis: Lower discount may maintain AOV while still driving bundle sales")
print()

print("STRATEGY 2: ADJUST PRODUCT PAIRINGS")
print("-" * 40)
print("If bundle #4 (Facial Care) underperforms:")
print("  - Remove Electric Gua Sha")
print("  - Add V-Line Face Slimming instead")
print("  - Monitor for 1 week")
print("  - Compare performance")
print()

print("STRATEGY 3: SEASONAL BUNDLES")
print("-" * 40)
print("Winter (Nov-Feb): Focus on pain relief bundles (#1, #2, #3)")
print("Summer (Jun-Aug): Focus on beauty/wellness (#4, #6, #10)")
print("Year-round: Maintain top 5 performers")
print()

print("STRATEGY 4: TIERED BUNDLING")
print("-" * 40)
print("If budget allows, create:")
print("  - TIER 1: Main + 1 product (5% off)")
print("  - TIER 2: Main + 2 products (10% off)")
print("  - TIER 3: Main + 3 products (15% off)")
print("Goal: Maximize AOV by encouraging larger bundles")
print()

print("="*80)
print("TROUBLESHOOTING")
print("="*80)
print()

print("ISSUE 1: Widget not showing on product page")
print("-" * 40)
print("✓ Check bundle is set to 'Active'")
print("✓ Verify main product handle is correct")
print("✓ Check Bundler app permissions in Shopify")
print("✓ Clear browser cache and reload")
print("✓ Test in incognito mode")
print()

print("ISSUE 2: Discount not calculating correctly")
print("-" * 40)
print("✓ Verify discount type (percentage vs fixed)")
print("✓ Check discount applies to 'all products in bundle'")
print("✓ Ensure no conflicting discount codes active")
print("✓ Test with products that have no variants")
print()

print("ISSUE 3: 'Add All to Cart' button not working")
print("-" * 40)
print("✓ Check JavaScript not blocked by theme")
print("✓ Disable other cart apps temporarily")
print("✓ Test with default theme (Dawn)")
print("✓ Contact Bundler support if persists")
print()

print("ISSUE 4: Bundle acceptance rate <5%")
print("-" * 40)
print("✓ Increase discount to 15%")
print("✓ Improve product pairings (more relevant)")
print("✓ Add urgency text ('Limited time offer')")
print("✓ Test different widget positioning")
print()

print("="*80)
print("EXPECTED RESULTS")
print("="*80)
print()
print("BASELINE (No FBT bundles):")
print("  - AOV: ~$100")
print("  - Bundle acceptance: 0%")
print("  - Revenue opportunity: Missed $800-1,200/month")
print()
print("AFTER FBT IMPLEMENTATION (10 bundles):")
print("  - AOV: $115-120 (+15-20%)")
print("  - Bundle acceptance: 8-12%")
print("  - Additional revenue: $800-1,200/month")
print()
print("TOP PERFORMING BUNDLES (Expected):")
print("  #1: Neck Pain Relief Bundle → 12-15% acceptance")
print("  #2: Complete Knee Recovery → 10-12% acceptance")
print("  #4: Complete Facial Care → 8-10% acceptance")
print()

print("="*80)
print("IMPLEMENTATION TIMELINE")
print("="*80)
print()
print("HOUR 1 (Bundles #1-5):")
print("  - Bundle #1: Neck Pain Relief (12 min)")
print("  - Bundle #2: Knee Recovery (12 min)")
print("  - Bundle #3: Back Support (12 min)")
print("  - Bundle #4: Facial Care (12 min)")
print("  - Bundle #5: Body Toning (12 min)")
print("  - Total: ~60 minutes")
print()
print("HOUR 2 (Bundles #6-10 + Testing):")
print("  - Bundle #6: Body Sculpting (10 min)")
print("  - Bundle #7: Eye Care (10 min)")
print("  - Bundle #8: Neck Therapy (10 min)")
print("  - Bundle #9: Knee Surgery Recovery (10 min)")
print("  - Bundle #10: Anti-Aging (10 min)")
print("  - Testing all bundles (10 min)")
print("  - Total: ~60 minutes")
print()
print("TOTAL TIME: 1.5-2 hours")
print()

print("="*80)
print("CATEGORY BREAKDOWN")
print("="*80)
print()
print("Neck/Cervical (27 products) → 2 bundles (#1, #8)")
print("Knee/Joint (37 products) → 2 bundles (#2, #9)")
print("Back/Posture (17 products) → 1 bundle (#3)")
print("LED Light Therapy (12 products) → 2 bundles (#4, #10)")
print("EMS/Electrical (11 products) → 1 bundle (#5)")
print("Massage Therapy (31 products) → 2 bundles (#6, #7)")
print()
print("Total: 10 bundles covering 135 products")
print()

print("="*80)
print("IMPORTANT NOTES")
print("="*80)
print()
print("⚠️  Bundler app requires MANUAL UI configuration")
print("⚠️  Estimated time: 1.5-2 hours for all 10 bundles")
print("⚠️  Test each bundle on frontend before moving to next")
print("⚠️  Monitor performance weekly - optimize underperformers")
print("⚠️  Product handles must match exactly (case-sensitive)")
print("⚠️  Start with top 5 bundles if time-constrained")
print("⚠️  Mobile testing critical (60%+ traffic from mobile)")
print()

print("PRIORITY ORDER IF TIME-LIMITED:")
print("  1. Bundle #1 (Neck Pain) - Highest expected acceptance")
print("  2. Bundle #2 (Knee Recovery) - High AOV increase")
print("  3. Bundle #4 (Facial Care) - Highest AOV increase")
print("  4. Bundle #5 (Body Toning) - Strong product fit")
print("  5. Bundle #8 (Neck Therapy) - Multi-modal appeal")
print()

print("="*80)
print("SUCCESS CRITERIA")
print("="*80)
print()
print("WEEK 1:")
print("  ✅ All 10 bundles configured and active")
print("  ✅ All bundles tested on frontend")
print("  ✅ No JavaScript errors in console")
print("  ✅ Mobile responsive verified")
print()
print("WEEK 2:")
print("  ✅ Bundle acceptance rate >5%")
print("  ✅ At least 3 bundle purchases")
print("  ✅ No customer support issues")
print("  ✅ AOV increase visible in analytics")
print()
print("MONTH 1:")
print("  ✅ Bundle acceptance rate >8%")
print("  ✅ AOV increase +10-15%")
print("  ✅ Additional revenue $500-800")
print("  ✅ Top 3 performers identified")
print()
print("MONTH 3:")
print("  ✅ Bundle acceptance rate >10%")
print("  ✅ AOV increase +15-20%")
print("  ✅ Additional revenue $800-1,200")
print("  ✅ All bundles optimized based on data")
print()

print("="*80)
print("CONFIGURATION GUIDE COMPLETE!")
print("="*80)
print()
print("NEXT STEPS:")
print("  1. Open Bundler app in Shopify admin")
print("  2. Follow bundle configurations above (priority #1-10)")
print("  3. Test each bundle after creation")
print("  4. Monitor performance in Bundler analytics")
print("  5. Optimize based on weekly data")
print()
print("EXPECTED OUTCOME: $800-1,200/month additional revenue")
print()
