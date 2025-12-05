/**
 * ALPHA MEDICAL - DYNAMIC MERCHANDISING SYSTEM
 * Date: 2025-11-19
 * Purpose: Monthly product rotation based on 6-dimension scoring matrix
 *
 * ARCHITECTURE:
 * 1. Load product_matrix_complete.json (injected via Liquid)
 * 2. Detect context (season/month, optional demographics via localStorage)
 * 3. Calculate composite scores for all products
 * 4. Dynamically reorder products in homepage sections
 *
 * SECTIONS AFFECTED:
 * - featured-collection (Featured Products)
 * - bundle-products-showcase (Bundles Showcase)
 * - related-products (Recommended Products)
 *
 * NOT AFFECTED:
 * - slideshow (HERO - owner managed manually)
 */

(function() {
  'use strict';

  // =========================================================================
  // CONFIGURATION
  // =========================================================================

  const CONFIG = {
    // Dimension weights (from segmentation_matrix_alpha_medical.json)
    weights: {
      seasonality: 0.25,
      demographics: 0.20,
      pain_type: 0.20,
      price_tier: 0.15,
      usage_intensity: 0.10,
      medical_condition: 0.10
    },

    // Default demographics if no user preference detected
    defaultDemographic: 'office_workers_25_55', // Largest segment (28.2%)

    // Sections to apply rotation
    targetSections: [
      'featured-collection',
      'bundle-products-showcase',
      'related-products'
    ],

    // Debug mode
    debug: false
  };

  // =========================================================================
  // CONTEXT DETECTION
  // =========================================================================

  function getCurrentContext() {
    const now = new Date();
    const month = now.getMonth(); // 0-11
    const season = getSeasonFromMonth(month);
    const demographic = getUserDemographic();

    return {
      month: month,
      season: season,
      demographic: demographic,
      timestamp: now.toISOString()
    };
  }

  function getSeasonFromMonth(month) {
    // Northern Hemisphere seasons
    if (month === 11 || month === 0 || month === 1) return 'winter'; // Dec, Jan, Feb
    if (month >= 2 && month <= 4) return 'spring'; // Mar, Apr, May
    if (month >= 5 && month <= 7) return 'summer'; // Jun, Jul, Aug
    if (month >= 8 && month <= 10) return 'fall'; // Sep, Oct, Nov
  }

  function getUserDemographic() {
    // Try to get from localStorage (set by user interactions)
    const stored = localStorage.getItem('alphamedical_demographic');
    if (stored) {
      return stored;
    }

    // Try to infer from browsing history (product tags viewed)
    const viewedTags = JSON.parse(localStorage.getItem('alphamedical_viewed_tags') || '[]');
    if (viewedTags.length > 0) {
      const inferred = inferDemographicFromTags(viewedTags);
      return inferred;
    }

    // Default to largest segment
    return CONFIG.defaultDemographic;
  }

  function inferDemographicFromTags(tags) {
    // Count keywords for each demographic
    const counts = {
      office_workers_25_55: 0,
      seniors_65plus: 0,
      beauty_wellness_25_55: 0,
      athletes_18_45: 0,
      gamers_16_35: 0,
      specialized_medical_rehabilitation: 0
    };

    tags.forEach(tag => {
      const tagLower = tag.toLowerCase();

      // Office workers
      if (['posture', 'desk', 'office', 'ergonomic', 'tech neck', 'cervical', 'back', 'lumbar'].some(kw => tagLower.includes(kw))) {
        counts.office_workers_25_55++;
      }

      // Seniors
      if (['arthritis', 'chronic pain', 'magnetic', 'heated', 'tourmaline'].some(kw => tagLower.includes(kw))) {
        counts.seniors_65plus++;
      }

      // Beauty/Wellness
      if (['led', 'face mask', 'anti-aging', 'wrinkle', 'skin', 'rejuvenation'].some(kw => tagLower.includes(kw))) {
        counts.beauty_wellness_25_55++;
      }

      // Athletes
      if (['sports', 'basketball', 'running', 'cycling', 'athletic', 'performance'].some(kw => tagLower.includes(kw))) {
        counts.athletes_18_45++;
      }

      // Gamers
      if (['wrist', 'carpal tunnel', 'gaming', 'hand', 'typing'].some(kw => tagLower.includes(kw))) {
        counts.gamers_16_35++;
      }

      // Specialized medical
      if (['stroke', 'cerebral palsy', 'rehabilitation robot', 'mirror training'].some(kw => tagLower.includes(kw))) {
        counts.specialized_medical_rehabilitation++;
      }
    });

    // Return demographic with highest count
    const topDemo = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
    return topDemo;
  }

  // =========================================================================
  // COMPOSITE SCORE CALCULATION
  // =========================================================================

  function calculateCompositeScore(product, context, productMatrix) {
    const handle = product.handle;
    const matrixData = productMatrix[handle];

    if (!matrixData || !matrixData.scores) {
      CONFIG.debug && console.warn('[DynMerch] No matrix data for product:', handle);
      return 0.5; // Default neutral score
    }

    const scores = matrixData.scores;
    let compositeScore = 0;

    // 1. Seasonality (25%)
    const seasonalityScore = scores.seasonality[context.season] || 0.5;
    compositeScore += seasonalityScore * CONFIG.weights.seasonality;

    // 2. Demographics (20%)
    const demographicScore = scores.demographics[context.demographic] || 0.2;
    compositeScore += demographicScore * CONFIG.weights.demographics;

    // 3. Pain Type (20%) - use max pain type score
    const painTypeScores = Object.values(scores.pain_type || {});
    const maxPainScore = painTypeScores.length > 0 ? Math.max(...painTypeScores) : 0.0;
    compositeScore += maxPainScore * CONFIG.weights.pain_type;

    // 4. Price Tier (15%) - use max price tier score
    const priceTierScores = Object.values(scores.price_tier || {});
    const maxPriceScore = priceTierScores.length > 0 ? Math.max(...priceTierScores) : 0.5;
    compositeScore += maxPriceScore * CONFIG.weights.price_tier;

    // 5. Usage Intensity (10%) - use max usage intensity score
    const usageIntensityScores = Object.values(scores.usage_intensity || {});
    const maxUsageScore = usageIntensityScores.length > 0 ? Math.max(...usageIntensityScores) : 0.3;
    compositeScore += maxUsageScore * CONFIG.weights.usage_intensity;

    // 6. Medical Condition (10%) - use max medical condition score
    const medicalConditionScores = Object.values(scores.medical_condition || {});
    const maxMedicalScore = medicalConditionScores.length > 0 ? Math.max(...medicalConditionScores) : 0.1;
    compositeScore += maxMedicalScore * CONFIG.weights.medical_condition;

    return compositeScore;
  }

  // =========================================================================
  // PRODUCT REORDERING
  // =========================================================================

  function reorderProductsInSection(section, productMatrix, context) {
    // Find all product cards in section
    const productCards = section.querySelectorAll('[data-product-handle], .product-card, .grid__item');

    if (productCards.length === 0) {
      return;
    }

    // Extract products with handles
    const products = Array.from(productCards).map(card => {
      const handle = card.getAttribute('data-product-handle') ||
                     card.querySelector('[data-product-handle]')?.getAttribute('data-product-handle') ||
                     card.querySelector('a[href*="/products/"]')?.getAttribute('href')?.split('/products/')[1]?.split('?')[0];

      if (!handle) {
        CONFIG.debug && console.warn('[DynMerch] Could not extract handle from card:', card);
        return null;
      }

      return {
        handle: handle,
        element: card,
        score: 0
      };
    }).filter(p => p !== null);

    // Calculate composite scores
    products.forEach(product => {
      product.score = calculateCompositeScore(product, context, productMatrix);
    });

    // Sort by composite score (descending)
    products.sort((a, b) => b.score - a.score);

      handle: p.handle,
      score: p.score.toFixed(3)
    })));

    // Reorder DOM elements
    const container = products[0].element.parentElement;
    products.forEach(product => {
      container.appendChild(product.element);
    });
  }

  function applyDynamicMerchandising(productMatrix) {
    const context = getCurrentContext();


    // Apply to each target section
    CONFIG.targetSections.forEach(sectionClass => {
      const sections = document.querySelectorAll(`.${sectionClass}, [data-section-type="${sectionClass}"]`);

      sections.forEach(section => {
        reorderProductsInSection(section, productMatrix, context);
      });
    });

    // Track merchandising application
    if (window.gtag) {
      window.gtag('event', 'dynamic_merchandising_applied', {
        season: context.season,
        demographic: context.demographic,
        month: context.month,
        products_reordered: Object.keys(productMatrix).length
      });
    }

  }

  // =========================================================================
  // PRODUCT INTERACTION TRACKING
  // =========================================================================

  function trackProductView(productHandle, productTags) {
    // Store viewed product tags for demographic inference
    const viewedTags = JSON.parse(localStorage.getItem('alphamedical_viewed_tags') || '[]');

    if (Array.isArray(productTags)) {
      productTags.forEach(tag => {
        if (!viewedTags.includes(tag)) {
          viewedTags.push(tag);
        }
      });
    }

    // Keep only last 50 tags
    const recentTags = viewedTags.slice(-50);
    localStorage.setItem('alphamedical_viewed_tags', JSON.stringify(recentTags));

  }

  // =========================================================================
  // INITIALIZATION
  // =========================================================================

  function init() {

    // Check if product matrix is available (injected via Liquid)
    if (typeof window.AlphaMedicalProductMatrix === 'undefined') {
      console.error('[DynMerch] ❌ Product matrix not loaded! Ensure product-matrix-loader.liquid is included in theme.');
      return;
    }

    const productMatrix = window.AlphaMedicalProductMatrix;

    // Apply dynamic merchandising on DOMContentLoaded
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        applyDynamicMerchandising(productMatrix);
      });
    } else {
      applyDynamicMerchandising(productMatrix);
    }

    // Track product views (for demographic inference)
    // This would be triggered from product pages via theme integration
    window.AlphaMedical = window.AlphaMedical || {};
    window.AlphaMedical.trackProductView = trackProductView;
  }

  // Start initialization
  init();

})();
