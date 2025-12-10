// Updated: 1765392121
/**
 * Bundle Builder - Complete Interactive Functionality
 * Handles product search, selection, price calculation, and form submission
 * 
 * Dependencies: window.BUNDLE_BUILDER_PRODUCTS, window.BUNDLE_BUILDER_CONFIG
 */

(function () {
    'use strict';

    // State management
    const state = {
        selectedProducts: [],
        searchResults: [],
        config: window.BUNDLE_BUILDER_CONFIG || {
            minProducts: 3,
            maxProducts: 4,
            maxValue: 500,
            discountPercent: 35,
            threshold: 10,
            monthlyLimit: 3
        }
    };

    // DOM elements (cached)
    const elements = {
        searchInput: null,
        searchResults: null,
        selectedProducts: null,
        selectedCount: null,
        priceSummary: null,
        regularPrice: null,
        bundlePrice: null,
        savings: null,
        maxValueWarning: null,
        submissionForm: null,
        submitButton: null,
        bundleDataInput: null,
        commitmentCheckbox: null,
        emailInput: null
    };

    /**
     * Initialize the bundle builder
     */
    function init() {
        // Cache DOM elements
        cacheElements();

        // Check if all required elements exist
        if (!validateElements()) {
            console.error('[Bundle Builder] Required elements not found');
            return;
        }

        // Attach event listeners
        attachEventListeners();

        // Initial render
        renderSelectedProducts();

        console.log('[Bundle Builder] Initialized successfully');
    }

    /**
     * Cache all DOM elements
     */
    function cacheElements() {
        elements.searchInput = document.getElementById('product-search-input');
        elements.searchResults = document.getElementById('search-results');
        elements.selectedProducts = document.getElementById('selected-products');
        elements.selectedCount = document.getElementById('selected-count');
        elements.priceSummary = document.getElementById('price-summary');
        elements.regularPrice = document.getElementById('regular-price');
        elements.bundlePrice = document.getElementById('bundle-price');
        elements.savings = document.getElementById('savings');
        elements.maxValueWarning = document.getElementById('max-value-warning');
        elements.submissionForm = document.getElementById('submission-form-container');
        elements.submitButton = document.getElementById('submit-proposal-btn');
        elements.bundleDataInput = document.getElementById('bundle-data-json');
        elements.commitmentCheckbox = document.getElementById('commitment-checkbox');
        elements.emailInput = document.getElementById('contact-email');
    }

    /**
     * Validate that all required elements exist
     */
    function validateElements() {
        const required = ['searchInput', 'searchResults', 'selectedProducts', 'selectedCount'];
        return required.every(key => elements[key] !== null);
    }

    /**
     * Attach all event listeners
     */
    function attachEventListeners() {
        // Search input (debounced)
        let searchTimeout;
        elements.searchInput.addEventListener('input', function (e) {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => handleSearch(e.target.value), 300);
        });

        // Event delegation for search results (add product)
        elements.searchResults.addEventListener('click', function (e) {
            const addBtn = e.target.closest('.add-product-btn');
            if (addBtn) {
                const productId = parseInt(addBtn.dataset.productId, 10);
                handleAddProduct(productId);
            }
        });

        // Event delegation for selected products (remove product)
        elements.selectedProducts.addEventListener('click', function (e) {
            const removeBtn = e.target.closest('.remove-product-btn');
            if (removeBtn) {
                const productId = parseInt(removeBtn.dataset.productId, 10);
                handleRemoveProduct(productId);
            }
        });

        // Commitment checkbox
        if (elements.commitmentCheckbox) {
            elements.commitmentCheckbox.addEventListener('change', updateSubmitButton);
        }

        // Email input validation
        if (elements.emailInput) {
            elements.emailInput.addEventListener('input', updateSubmitButton);
        }

        // Form submission
        const form = document.querySelector('.bundle-proposal-form');
        if (form) {
            form.addEventListener('submit', handleFormSubmit);
        }
    }

    /**
     * Handle product search
     */
    function handleSearch(query) {
        const trimmedQuery = query.trim().toLowerCase();

        if (trimmedQuery.length < 2) {
            elements.searchResults.innerHTML = '';
            return;
        }

        // Filter products
        const allProducts = window.BUNDLE_BUILDER_PRODUCTS || [];
        const results = allProducts.filter(product => {
            if (!product.available) return false;

            const searchableText = [
                product.title,
                product.productType,
                product.vendor
            ].join(' ').toLowerCase();

            return searchableText.includes(trimmedQuery);
        }).slice(0, 8); // Limit to 8 results

        state.searchResults = results;
        renderSearchResults(results);
    }

    /**
     * Render search results
     */
    function renderSearchResults(results) {
        if (results.length === 0) {
            elements.searchResults.innerHTML = `
        <div class="search-empty">
          <p>No products found. Try a different search term.</p>
        </div>
      `;
            return;
        }

        const html = results.map(product => {
            const isSelected = state.selectedProducts.some(p => p.id === product.id);
            const isDisabled = isSelected || state.selectedProducts.length >= state.config.maxProducts;

            return `
        <div class="search-result-item">
          <img src="${product.image}" alt="${escapeHtml(product.title)}" class="result-image" loading="lazy">
          <div class="result-info">
            <h4 class="result-title">${escapeHtml(product.title)}</h4>
            <p class="result-price">${formatPrice(product.price)}</p>
          </div>
          <button
            type="button"
            class="add-product-btn ${isSelected ? 'added' : ''}"
            data-product-id="${product.id}"
            ${isDisabled ? 'disabled' : ''}
          >
            ${isSelected ? '✓ Added' : '+ Add'}
          </button>
        </div>
      `;
        }).join('');

        elements.searchResults.innerHTML = html;
    }

    /**
     * Handle adding a product to selection
     */
    function handleAddProduct(productId) {
        // Check if already selected
        if (state.selectedProducts.some(p => p.id === productId)) {
            return;
        }

        // Check max products constraint
        if (state.selectedProducts.length >= state.config.maxProducts) {
            alert(`You can only select up to ${state.config.maxProducts} products.`);
            return;
        }

        // Find product in all products
        const product = (window.BUNDLE_BUILDER_PRODUCTS || []).find(p => p.id === productId);
        if (!product) return;

        // Add to selected products
        state.selectedProducts.push(product);

        // Re-render
        renderSelectedProducts();
        renderSearchResults(state.searchResults); // Update add buttons
        updatePriceDisplay();
        updateFormVisibility();

        // Track event (GTM)
        trackEvent('bundle_product_added', { product_id: productId, product_title: product.title });
    }

    /**
     * Handle removing a product from selection
     */
    function handleRemoveProduct(productId) {
        state.selectedProducts = state.selectedProducts.filter(p => p.id !== productId);

        // Re-render
        renderSelectedProducts();
        renderSearchResults(state.searchResults); // Update add buttons
        updatePriceDisplay();
        updateFormVisibility();

        // Track event (GTM)
        trackEvent('bundle_product_removed', { product_id: productId });
    }

    /**
     * Render selected products
     */
    function renderSelectedProducts() {
        const count = state.selectedProducts.length;
        elements.selectedCount.textContent = count;

        if (count === 0) {
            elements.selectedProducts.innerHTML = `
        <div class="empty-state">
          <svg class="empty-icon" width="48" height="48" viewBox="0 0 48 48" fill="none">
            <path d="M8 12L20 4L32 12M8 12L8 36L20 44M8 12L20 20M20 44L32 36L32 12M20 44L20 20M32 12L20 20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <p>Search and select 3-4 products to build your bundle</p>
        </div>
      `;
            return;
        }

        const html = state.selectedProducts.map((product, index) => `
      <div class="selected-product-item" style="animation: fadeIn 0.3s ease ${index * 0.1}s both">
        <img src="${product.image}" alt="${escapeHtml(product.title)}" class="selected-image">
        <div class="selected-info">
          <h4 class="selected-title">${escapeHtml(product.title)}</h4>
          <p class="selected-price">${formatPrice(product.price)}</p>
        </div>
        <button
          type="button"
          class="remove-product-btn"
          data-product-id="${product.id}"
          aria-label="Remove ${escapeHtml(product.title)}"
        >
          ✕
        </button>
      </div>
    `).join('');

        elements.selectedProducts.innerHTML = html;
    }

    /**
     * Update price display
     */
    function updatePriceDisplay() {
        const count = state.selectedProducts.length;

        if (count === 0) {
            if (elements.priceSummary) {
                elements.priceSummary.style.display = 'none';
            }
            if (elements.maxValueWarning) {
                elements.maxValueWarning.style.display = 'none';
            }
            return;
        }

        // Calculate prices
        const regularTotal = state.selectedProducts.reduce((sum, p) => sum + p.price, 0);
        const discountAmount = regularTotal * (state.config.discountPercent / 100);
        const bundleTotal = regularTotal - discountAmount;

        // Update DOM
        if (elements.regularPrice) {
            elements.regularPrice.textContent = formatPrice(regularTotal);
        }
        if (elements.bundlePrice) {
            elements.bundlePrice.textContent = formatPrice(bundleTotal);
        }
        if (elements.savings) {
            elements.savings.textContent = formatPrice(discountAmount);
        }

        // Show price summary
        if (elements.priceSummary) {
            elements.priceSummary.style.display = 'block';
        }

        // Check max value
        const exceedsMax = regularTotal > state.config.maxValue * 100; // Price is in cents
        if (elements.maxValueWarning) {
            elements.maxValueWarning.style.display = exceedsMax ? 'flex' : 'none';
        }

        // Disable submit if exceeds max
        if (exceedsMax && elements.submitButton) {
            elements.submitButton.disabled = true;
        }
    }

    /**
     * Update form visibility and validation
     */
    function updateFormVisibility() {
        const count = state.selectedProducts.length;
        const meetsMinimum = count >= state.config.minProducts;
        const regularTotal = state.selectedProducts.reduce((sum, p) => sum + p.price, 0);
        const withinMaxValue = regularTotal <= state.config.maxValue * 100;

        if (elements.submissionForm) {
            elements.submissionForm.style.display = (meetsMinimum && withinMaxValue) ? 'block' : 'none';
        }

        updateSubmitButton();
    }

    /**
     * Update submit button state
     */
    function updateSubmitButton() {
        if (!elements.submitButton) return;

        const hasEmail = elements.emailInput && elements.emailInput.value.trim().length > 0;
        const emailValid = elements.emailInput && elements.emailInput.validity.valid;
        const commitmentChecked = elements.commitmentCheckbox && elements.commitmentCheckbox.checked;
        const hasProducts = state.selectedProducts.length >= state.config.minProducts;
        const regularTotal = state.selectedProducts.reduce((sum, p) => sum + p.price, 0);
        const withinMaxValue = regularTotal <= state.config.maxValue * 100;

        elements.submitButton.disabled = !(hasEmail && emailValid && commitmentChecked && hasProducts && withinMaxValue);
    }

    /**
     * Handle form submission
     */
    function handleFormSubmit(e) {
        // Don't prevent default - let Shopify handle the form submission
        // But prepare the bundle data JSON
        const bundleData = {
            products: state.selectedProducts.map(p => ({
                id: p.id,
                handle: p.handle,
                title: p.title,
                price: p.price
            })),
            regularPrice: state.selectedProducts.reduce((sum, p) => sum + p.price, 0),
            discountPercent: state.config.discountPercent,
            timestamp: new Date().toISOString()
        };

        // Set the JSON data in the hidden field
        if (elements.bundleDataInput) {
            elements.bundleDataInput.value = JSON.stringify(bundleData, null, 2);
        }

        // Track event (GTM)
        trackEvent('bundle_proposal_submitted', {
            product_count: state.selectedProducts.length,
            bundle_value: bundleData.regularPrice / 100
        });

        console.log('[Bundle Builder] Form submitted', bundleData);
    }

    /**
     * Utility: Format price (cents to dollars)
     */
    function formatPrice(cents) {
        const dollars = cents / 100;
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(dollars);
    }

    /**
     * Utility: Escape HTML
     */
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Utility: Track GTM event
     */
    function trackEvent(eventName, eventData) {
        if (window.dataLayer) {
            window.dataLayer.push({
                event: eventName,
                ...eventData
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Add fadeIn animation CSS if not present
    if (!document.getElementById('bundle-builder-animation-styles')) {
        const style = document.createElement('style');
        style.id = 'bundle-builder-animation-styles';
        style.textContent = `
      @keyframes fadeIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
    `;
        document.head.appendChild(style);
    }

})();
