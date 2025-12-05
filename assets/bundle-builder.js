/**
 * BUNDLE BUILDER - Frontend Logic
 *
 * Features:
 * - Debounced search (300ms)
 * - Fuzzy matching (title, product_type, vendor)
 * - Duplicate prevention
 * - Real-time validation
 * - $500 maximum check
 * - Product URLs (clickable, internal only)
 * - Bundle data JSON serialization
 * - GA4 event tracking
 *
 * Zero external dependencies - vanilla JavaScript
 */

(function() {
  'use strict';

  // =========================================================================
  // CONFIGURATION
  // =========================================================================

  const CONFIG = window.BUNDLE_BUILDER_CONFIG || {
    minProducts: 3,
    maxProducts: 4,
    maxValue: 500,
    discountPercent: 35,
    threshold: 10,
    monthlyLimit: 3
  };

  const SEARCH_DEBOUNCE_MS = 300;
  const ALL_PRODUCTS = window.BUNDLE_BUILDER_PRODUCTS || [];

  // =========================================================================
  // STATE MANAGEMENT
  // =========================================================================

  let selectedProducts = [];
  let searchDebounceTimer = null;

  // =========================================================================
  // DOM ELEMENTS
  // =========================================================================

  const searchInput = document.getElementById('product-search-input');
  const searchResults = document.getElementById('search-results');
  const selectedContainer = document.getElementById('selected-products');
  const selectedCountEl = document.getElementById('selected-count');
  const priceSummaryEl = document.getElementById('price-summary');
  const regularPriceEl = document.getElementById('regular-price');
  const bundlePriceEl = document.getElementById('bundle-price');
  const savingsEl = document.getElementById('savings');
  const maxValueWarning = document.getElementById('max-value-warning');
  const formContainer = document.getElementById('submission-form-container');
  const bundleDataInput = document.getElementById('bundle-data-json');
  const submitButton = document.getElementById('submit-proposal-btn');
  const commitmentCheckbox = document.getElementById('commitment-checkbox');

  // =========================================================================
  // INITIALIZATION
  // =========================================================================

  function init() {
    if (!searchInput || ALL_PRODUCTS.length === 0) {
      console.warn('Bundle Builder: Missing elements or products data');
      return;
    }

    // Event listeners
    searchInput.addEventListener('input', handleSearchInput);
    searchInput.addEventListener('focus', handleSearchFocus);
    document.addEventListener('click', handleDocumentClick);

    if (commitmentCheckbox) {
      commitmentCheckbox.addEventListener('change', validateForm);
    }

  }

  // =========================================================================
  // SEARCH FUNCTIONALITY
  // =========================================================================

  /**
   * Handle search input with debouncing
   */
  function handleSearchInput(e) {
    const query = e.target.value.trim();

    // Clear previous timer
    clearTimeout(searchDebounceTimer);

    // Debounce search
    searchDebounceTimer = setTimeout(() => {
      performSearch(query);
    }, SEARCH_DEBOUNCE_MS);
  }

  /**
   * Handle search input focus - show recent results if empty
   */
  function handleSearchFocus() {
    if (searchInput.value.trim() === '') {
      showRecentProducts();
    }
  }

  /**
   * Perform fuzzy search across products
   */
  function performSearch(query) {
    if (!query || query.length < 2) {
      searchResults.innerHTML = '';
      return;
    }

    const queryLower = query.toLowerCase();
    const results = ALL_PRODUCTS.filter(product => {
      // Fuzzy matching: title, product_type, vendor
      return (
        product.title.toLowerCase().includes(queryLower) ||
        (product.productType && product.productType.toLowerCase().includes(queryLower)) ||
        (product.vendor && product.vendor.toLowerCase().includes(queryLower))
      );
    }).slice(0, 10); // Limit to 10 results

    displaySearchResults(results, query);
  }

  /**
   * Show recent/popular products when no search query
   */
  function showRecentProducts() {
    const recent = ALL_PRODUCTS.filter(p => p.available).slice(0, 8);
    displaySearchResults(recent, '');
  }

  /**
   * Display search results
   */
  function displaySearchResults(results, query) {
    if (results.length === 0) {
      searchResults.innerHTML = `
        <div class="search-empty">
          <p>No products found for "${query}"</p>
        </div>
      `;
      return;
    }

    searchResults.innerHTML = results.map(product => {
      const isSelected = selectedProducts.some(p => p.id === product.id);
      const isDisabled = isSelected || selectedProducts.length >= CONFIG.maxProducts;

      return `
        <div class="search-result-item ${isDisabled ? 'disabled' : ''}"
             data-product-id="${product.id}"
             onclick="bundleBuilder.selectProduct(${product.id})">
          <img src="${product.image}" alt="${escapeHtml(product.title)}" class="result-image">
          <div class="result-info">
            <h4 class="result-title">${highlightQuery(product.title, query)}</h4>
            <p class="result-price">$${(product.price / 100).toFixed(2)}</p>
            ${isSelected ? '<span class="result-badge">Selected</span>' : ''}
            ${!product.available ? '<span class="result-badge unavailable">Out of Stock</span>' : ''}
          </div>
          ${!isDisabled && product.available ? `
            <button class="result-add-btn" aria-label="Add ${escapeHtml(product.title)}">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 5V15M5 10H15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          ` : ''}
        </div>
      `;
    }).join('');
  }

  /**
   * Highlight search query in text
   */
  function highlightQuery(text, query) {
    if (!query) return escapeHtml(text);

    const escaped = escapeHtml(text);
    const regex = new RegExp(`(${escapeRegex(query)})`, 'gi');
    return escaped.replace(regex, '<mark>$1</mark>');
  }

  // =========================================================================
  // PRODUCT SELECTION
  // =========================================================================

  /**
   * Select a product and add to bundle
   */
  window.bundleBuilder = window.bundleBuilder || {};
  window.bundleBuilder.selectProduct = function(productId) {
    // Find product
    const product = ALL_PRODUCTS.find(p => p.id === productId);
    if (!product) return;

    // Validation
    if (!product.available) {
      alert('This product is currently out of stock');
      return;
    }

    if (selectedProducts.some(p => p.id === productId)) {
      alert('Product already selected');
      return;
    }

    if (selectedProducts.length >= CONFIG.maxProducts) {
      alert(`Maximum ${CONFIG.maxProducts} products allowed`);
      return;
    }

    // Add to selection
    selectedProducts.push(product);
    updateSelectedProducts();
    updatePriceSummary();
    validateForm();

    // Clear search
    searchInput.value = '';
    searchResults.innerHTML = '';

    // Track event
    trackEvent('bundle_product_added', {
      product_id: product.id,
      product_title: product.title,
      product_price: product.price / 100,
      bundle_size: selectedProducts.length
    });
  };

  /**
   * Remove a product from bundle
   */
  window.bundleBuilder.removeProduct = function(productId) {
    selectedProducts = selectedProducts.filter(p => p.id !== productId);
    updateSelectedProducts();
    updatePriceSummary();
    validateForm();

    // Track event
    trackEvent('bundle_product_removed', {
      product_id: productId,
      bundle_size: selectedProducts.length
    });
  };

  /**
   * Update selected products display
   */
  function updateSelectedProducts() {
    selectedCountEl.textContent = selectedProducts.length;

    if (selectedProducts.length === 0) {
      selectedContainer.innerHTML = `
        <div class="empty-state">
          <svg class="empty-icon" width="48" height="48" viewBox="0 0 48 48" fill="none">
            <path d="M8 12L20 4L32 12M8 12L8 36L20 44M8 12L20 20M20 44L32 36L32 12M20 44L20 20M32 12L20 20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>Search and select ${CONFIG.minProducts}-${CONFIG.maxProducts} products to build your bundle</p>
        </div>
      `;
      return;
    }

    selectedContainer.innerHTML = selectedProducts.map((product, index) => `
      <div class="selected-product" data-product-id="${product.id}">
        <div class="selected-product-number">${index + 1}</div>
        <img src="${product.image}" alt="${escapeHtml(product.title)}" class="selected-product-image">
        <div class="selected-product-info">
          <h4 class="selected-product-title">
            <a href="${product.url}" target="_blank" rel="noopener">${escapeHtml(product.title)}</a>
          </h4>
          <p class="selected-product-price">$${(product.price / 100).toFixed(2)}</p>
        </div>
        <button
          class="remove-product-btn"
          onclick="bundleBuilder.removeProduct(${product.id})"
          aria-label="Remove ${escapeHtml(product.title)}"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </button>
      </div>
    `).join('');
  }

  // =========================================================================
  // PRICE CALCULATION
  // =========================================================================

  /**
   * Update price summary
   */
  function updatePriceSummary() {
    if (selectedProducts.length === 0) {
      priceSummaryEl.style.display = 'none';
      formContainer.style.display = 'none';
      return;
    }

    // Calculate prices
    const regularTotal = selectedProducts.reduce((sum, p) => sum + p.price, 0);
    const bundleTotal = regularTotal * (1 - CONFIG.discountPercent / 100);
    const savings = regularTotal - bundleTotal;

    // Convert cents to dollars
    const regularPrice = regularTotal / 100;
    const bundlePrice = bundleTotal / 100;
    const savingsAmount = savings / 100;

    // Update DOM
    regularPriceEl.textContent = `$${regularPrice.toFixed(2)}`;
    bundlePriceEl.textContent = `$${bundlePrice.toFixed(2)}`;
    savingsEl.textContent = `$${savingsAmount.toFixed(2)}`;

    priceSummaryEl.style.display = 'block';

    // Check maximum value
    if (regularPrice > CONFIG.maxValue) {
      maxValueWarning.style.display = 'flex';
      formContainer.style.display = 'none';
    } else {
      maxValueWarning.style.display = 'none';

      // Show form only if minimum products met
      if (selectedProducts.length >= CONFIG.minProducts) {
        formContainer.style.display = 'block';
      } else {
        formContainer.style.display = 'none';
      }
    }
  }

  // =========================================================================
  // FORM VALIDATION & SUBMISSION
  // =========================================================================

  /**
   * Validate form and enable/disable submit button
   */
  function validateForm() {
    const isValid = (
      selectedProducts.length >= CONFIG.minProducts &&
      selectedProducts.length <= CONFIG.maxProducts &&
      (selectedProducts.reduce((sum, p) => sum + p.price, 0) / 100) <= CONFIG.maxValue &&
      commitmentCheckbox &&
      commitmentCheckbox.checked
    );

    if (submitButton) {
      submitButton.disabled = !isValid;
    }

    // Update bundle data JSON (for form submission)
    if (bundleDataInput && selectedProducts.length > 0) {
      const bundleData = createBundleDataJSON();
      bundleDataInput.value = bundleData;
    }
  }

  /**
   * Create JSON data for bundle proposal
   */
  function createBundleDataJSON() {
    const regularTotal = selectedProducts.reduce((sum, p) => sum + p.price, 0) / 100;
    const bundleTotal = regularTotal * (1 - CONFIG.discountPercent / 100);

    const data = {
      timestamp: new Date().toISOString(),
      products: selectedProducts.map(p => ({
        id: p.id,
        handle: p.handle,
        title: p.title,
        price: p.price / 100,
        url: p.url
      })),
      pricing: {
        regular_total: regularTotal.toFixed(2),
        bundle_total: bundleTotal.toFixed(2),
        discount_percent: CONFIG.discountPercent,
        savings: (regularTotal - bundleTotal).toFixed(2)
      },
      metadata: {
        threshold: CONFIG.threshold,
        monthly_limit: CONFIG.monthlyLimit,
        user_agent: navigator.userAgent,
        screen_width: window.innerWidth
      }
    };

    return JSON.stringify(data, null, 2);
  }

  /**
   * Track form submission (called by form onsubmit)
   */
  window.bundleBuilder.trackSubmission = function() {
    trackEvent('bundle_proposal_submitted', {
      product_count: selectedProducts.length,
      regular_total: selectedProducts.reduce((sum, p) => sum + p.price, 0) / 100,
      bundle_total: selectedProducts.reduce((sum, p) => sum + p.price, 0) / 100 * (1 - CONFIG.discountPercent / 100),
      products: selectedProducts.map(p => p.title).join(' | ')
    });
  };

  // =========================================================================
  // UTILITIES
  // =========================================================================

  /**
   * Escape HTML to prevent XSS
   */
  function escapeHtml(text) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
  }

  /**
   * Escape regex special characters
   */
  function escapeRegex(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * Close search results when clicking outside
   */
  function handleDocumentClick(e) {
    if (searchInput && searchResults) {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.innerHTML = '';
      }
    }
  }

  /**
   * Track Google Analytics 4 event
   */
  function trackEvent(eventName, params) {
    if (typeof gtag === 'function') {
      gtag('event', eventName, params);
    } else if (typeof dataLayer !== 'undefined') {
      dataLayer.push({
        event: eventName,
        ...params
      });
    } else {
    }
  }

  // =========================================================================
  // AUTO-INITIALIZATION
  // =========================================================================

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
