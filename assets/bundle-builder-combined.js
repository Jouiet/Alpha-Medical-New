/**
 * BUNDLE BUILDER COMBINED - JavaScript
 * Méthodes: Recherche de produits + Input URL
 * Alpha Medical Care - 2025
 */

(function() {
  'use strict';

  // CONFIGURATION
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

  // STATE
  let selectedProducts = [];
  let currentMethod = 'search';
  let searchDebounceTimer = null;
  let urlDebounceTimers = {};

  // DOM ELEMENTS
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
  const bundleMethodInput = document.getElementById('bundle-method');
  const submitButton = document.getElementById('submit-proposal-btn');
  const commitmentCheckbox = document.getElementById('commitment-checkbox');

  const urlInputs = [
    document.getElementById('url-input-1'),
    document.getElementById('url-input-2'),
    document.getElementById('url-input-3'),
    document.getElementById('url-input-4')
  ].filter(Boolean);

  // INITIALIZATION
  function init() {
    console.log('[BundleBuilder] Init:', ALL_PRODUCTS.length, 'products');

    if (searchInput) {
      searchInput.addEventListener('input', handleSearchInput);
      searchInput.addEventListener('focus', handleSearchFocus);
    }

    urlInputs.forEach((input, index) => {
      if (input) {
        input.addEventListener('input', () => handleUrlInput(index + 1));
        input.addEventListener('paste', () => setTimeout(() => handleUrlInput(index + 1), 100));
      }
    });

    if (commitmentCheckbox) commitmentCheckbox.addEventListener('change', validateForm);
    document.addEventListener('click', handleDocumentClick);
  }

  // METHOD SWITCHING
  window.bundleBuilderCombined = {
    switchMethod: function(method) {
      currentMethod = method;
      document.querySelectorAll('.method-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.method === method);
      });
      document.querySelectorAll('.input-method').forEach(panel => {
        panel.classList.toggle('active', panel.dataset.method === method);
      });
      console.log('[BundleBuilder] Method:', method);
    }
  };

  // SEARCH METHOD
  function handleSearchInput(e) {
    clearTimeout(searchDebounceTimer);
    searchDebounceTimer = setTimeout(() => performSearch(e.target.value.trim()), SEARCH_DEBOUNCE_MS);
  }

  function handleSearchFocus() {
    if (searchInput.value.trim() === '') showRecentProducts();
  }

  function performSearch(query) {
    if (!query || query.length < 2) {
      searchResults.innerHTML = '';
      return;
    }

    const queryLower = query.toLowerCase();
    const results = ALL_PRODUCTS.filter(p => 
      p.title.toLowerCase().includes(queryLower) ||
      (p.productType && p.productType.toLowerCase().includes(queryLower)) ||
      (p.vendor && p.vendor.toLowerCase().includes(queryLower))
    ).slice(0, 10);

    displaySearchResults(results, query);
  }

  function showRecentProducts() {
    displaySearchResults(ALL_PRODUCTS.filter(p => p.available).slice(0, 8), '');
  }

  function displaySearchResults(results, query) {
    if (results.length === 0) {
      searchResults.innerHTML = '<div style="padding:20px;text-align:center;color:#6B7280">No products found</div>';
      return;
    }

    searchResults.innerHTML = results.map(product => {
      const isSelected = selectedProducts.some(p => p.id === product.id);
      const isDisabled = isSelected || selectedProducts.length >= CONFIG.maxProducts;

      return `<div class="search-result-item ${isDisabled ? 'disabled' : ''}" onclick="bundleBuilderCombined.selectProduct(${product.id})">
        <img src="${product.image}" alt="${escapeHtml(product.title)}" class="result-image">
        <div class="result-info">
          <h4 class="result-title">${escapeHtml(product.title)}</h4>
          <p class="result-price">$${(product.price / 100).toFixed(2)}</p>
          ${isSelected ? '<span class="result-badge">Selected</span>' : ''}
          ${!product.available ? '<span class="result-badge unavailable">Out of Stock</span>' : ''}
        </div>
        ${!isDisabled && product.available ? '<button class="result-add-btn">+</button>' : ''}
      </div>`;
    }).join('');
  }

  // URL INPUT METHOD
  function handleUrlInput(productNumber) {
    const input = document.getElementById(`url-input-${productNumber}`);
    const statusEl = document.getElementById(`url-status-${productNumber}`);

    if (!input || !statusEl) return;

    const url = input.value.trim();

    clearTimeout(urlDebounceTimers[productNumber]);

    if (!url) {
      input.classList.remove('valid', 'invalid', 'loading');
      statusEl.textContent = '';
      removeProductByUrlInput(productNumber);
      return;
    }

    const urlPattern = /^https?:\/\/(www\.)?alphamedical\.shop\/products\/[a-z0-9\-]+\/?$/i;

    if (!urlPattern.test(url)) {
      input.classList.add('invalid');
      statusEl.textContent = '❌ Invalid URL';
      statusEl.className = 'url-label-status invalid';
      removeProductByUrlInput(productNumber);
      return;
    }

    input.classList.add('loading');
    statusEl.textContent = '⏳ Checking...';
    statusEl.className = 'url-label-status loading';

    urlDebounceTimers[productNumber] = setTimeout(() => fetchProductFromUrl(url, productNumber), 500);
  }

  async function fetchProductFromUrl(url, productNumber) {
    const input = document.getElementById(`url-input-${productNumber}`);
    const statusEl = document.getElementById(`url-status-${productNumber}`);

    try {
      const handle = url.match(/\/products\/([a-z0-9\-]+)/i)?.[1];
      if (!handle) throw new Error('Invalid URL');

      const response = await fetch(`/products/${handle}.js`);
      if (!response.ok) throw new Error('Not found');

      const data = await response.json();

      const product = {
        id: data.id,
        handle: data.handle,
        title: data.title,
        price: data.price,
        image: data.featured_image || data.images?.[0],
        url: `/products/${data.handle}`,
        available: data.available,
        urlInputNumber: productNumber
      };

      if (selectedProducts.some(p => p.id === product.id)) {
        input.classList.add('invalid');
        statusEl.textContent = '⚠️ Already selected';
        statusEl.className = 'url-label-status invalid';
        return;
      }

      if (!product.available) {
        input.classList.add('invalid');
        statusEl.textContent = '❌ Out of stock';
        statusEl.className = 'url-label-status invalid';
        return;
      }

      input.classList.remove('loading', 'invalid');
      input.classList.add('valid');
      statusEl.textContent = '✅ Valid';
      statusEl.className = 'url-label-status valid';

      addProductFromUrl(product, productNumber);
    } catch (error) {
      input.classList.add('invalid');
      statusEl.textContent = '❌ Not found';
      statusEl.className = 'url-label-status invalid';
      removeProductByUrlInput(productNumber);
    }
  }

  function addProductFromUrl(product, urlInputNumber) {
    selectedProducts = selectedProducts.filter(p => p.urlInputNumber !== urlInputNumber);
    selectedProducts.push(product);
    updateSelectedProducts();
    updatePriceSummary();
    validateForm();
    trackEvent('bundle_product_added', { method: 'url', product_id: product.id, bundle_size: selectedProducts.length });
  }

  function removeProductByUrlInput(urlInputNumber) {
    selectedProducts = selectedProducts.filter(p => p.urlInputNumber !== urlInputNumber);
    updateSelectedProducts();
    updatePriceSummary();
    validateForm();
  }

  // PRODUCT SELECTION
  window.bundleBuilderCombined.selectProduct = function(productId) {
    const product = ALL_PRODUCTS.find(p => p.id === productId);
    if (!product || !product.available || selectedProducts.some(p => p.id === productId)) return;
    if (selectedProducts.length >= CONFIG.maxProducts) return;

    selectedProducts.push(product);
    updateSelectedProducts();
    updatePriceSummary();
    validateForm();

    if (searchInput) searchInput.value = '';
    if (searchResults) searchResults.innerHTML = '';

    trackEvent('bundle_product_added', { method: 'search', product_id: product.id, bundle_size: selectedProducts.length });
  };

  window.bundleBuilderCombined.removeProduct = function(productId) {
    const productIndex = selectedProducts.findIndex(p => p.id === productId);
    if (productIndex === -1) return;

    const product = selectedProducts[productIndex];

    if (product.urlInputNumber) {
      const input = document.getElementById(`url-input-${product.urlInputNumber}`);
      const statusEl = document.getElementById(`url-status-${product.urlInputNumber}`);
      if (input) {
        input.value = '';
        input.classList.remove('valid', 'invalid', 'loading');
      }
      if (statusEl) {
        statusEl.textContent = '';
        statusEl.className = 'url-label-status';
      }
    }

    selectedProducts.splice(productIndex, 1);
    updateSelectedProducts();
    updatePriceSummary();
    validateForm();

    trackEvent('bundle_product_removed', { product_id: productId, bundle_size: selectedProducts.length });
  };

  function updateSelectedProducts() {
    if (!selectedCountEl || !selectedContainer) return;

    selectedCountEl.textContent = selectedProducts.length;

    if (selectedProducts.length === 0) {
      selectedContainer.innerHTML = '<div class="empty-state"><p>Select 3-4 products</p></div>';
      return;
    }

    selectedContainer.innerHTML = selectedProducts.map((p, i) => `
      <div class="selected-product">
        <div class="selected-product-number">${i + 1}</div>
        <img src="${p.image}" alt="${escapeHtml(p.title)}" class="selected-product-image">
        <div class="selected-product-info">
          <h3 class="selected-product-title"><a href="${p.url}">${escapeHtml(p.title)}</a></h3>
          <p class="selected-product-price">$${(p.price / 100).toFixed(2)}</p>
        </div>
        <button class="remove-product-btn" onclick="bundleBuilderCombined.removeProduct(${p.id})">×</button>
      </div>
    `).join('');
  }

  // PRICE CALCULATION
  function updatePriceSummary() {
    if (!priceSummaryEl) return;

    if (selectedProducts.length === 0) {
      priceSummaryEl.style.display = 'none';
      if (formContainer) formContainer.style.display = 'none';
      return;
    }

    const regularTotal = selectedProducts.reduce((sum, p) => sum + p.price, 0);
    const bundleTotal = regularTotal * (1 - CONFIG.discountPercent / 100);
    const regularPrice = regularTotal / 100;
    const bundlePrice = bundleTotal / 100;
    const savingsAmount = (regularTotal - bundleTotal) / 100;

    if (regularPriceEl) regularPriceEl.textContent = `$${regularPrice.toFixed(2)}`;
    if (bundlePriceEl) bundlePriceEl.textContent = `$${bundlePrice.toFixed(2)}`;
    if (savingsEl) savingsEl.textContent = `$${savingsAmount.toFixed(2)}`;

    priceSummaryEl.style.display = 'block';

    if (regularPrice > CONFIG.maxValue) {
      if (maxValueWarning) maxValueWarning.style.display = 'flex';
      if (formContainer) formContainer.style.display = 'none';
    } else {
      if (maxValueWarning) maxValueWarning.style.display = 'none';
      if (formContainer && selectedProducts.length >= CONFIG.minProducts) {
        formContainer.style.display = 'block';
      }
    }
  }

  // FORM VALIDATION
  function validateForm() {
    const isValid = selectedProducts.length >= CONFIG.minProducts &&
                    selectedProducts.length <= CONFIG.maxProducts &&
                    (selectedProducts.reduce((s, p) => s + p.price, 0) / 100) <= CONFIG.maxValue &&
                    commitmentCheckbox?.checked;

    if (submitButton) submitButton.disabled = !isValid;
    if (bundleDataInput && selectedProducts.length > 0) bundleDataInput.value = createBundleDataJSON();
    if (bundleMethodInput) bundleMethodInput.value = currentMethod;
  }

  function createBundleDataJSON() {
    const regularTotal = selectedProducts.reduce((s, p) => s + p.price, 0) / 100;
    const bundleTotal = regularTotal * (1 - CONFIG.discountPercent / 100);

    return JSON.stringify({
      timestamp: new Date().toISOString(),
      method: currentMethod,
      products: selectedProducts.map(p => ({ id: p.id, handle: p.handle, title: p.title, price: p.price / 100, url: p.url })),
      pricing: {
        regular_total: regularTotal.toFixed(2),
        bundle_total: bundleTotal.toFixed(2),
        discount_percent: CONFIG.discountPercent,
        savings: (regularTotal - bundleTotal).toFixed(2)
      }
    }, null, 2);
  }

  // UTILITIES
  function escapeHtml(text) {
    return text.replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'})[m]);
  }

  function handleDocumentClick(e) {
    if (searchInput && searchResults && !searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.innerHTML = '';
    }
  }

  function trackEvent(name, params) {
    if (typeof gtag === 'function') gtag('event', name, params);
    else if (typeof dataLayer !== 'undefined') dataLayer.push({ event: name, ...params });
    else console.log('[GA4]', name, params);
  }

  // AUTO-INIT
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
