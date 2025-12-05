/**
 * ALPHA MEDICAL - BUNDLES COLLECTION JAVASCRIPT
 * Interactive filters for 15 medical equipment bundles
 * Persona + Tier filtering with real-time updates
 */

const bundlesFilter = {
  // Current filter state
  currentPersona: 'all',
  currentTier: 'all',
  currentSort: 'savings',

  /**
   * Initialize bundles filter system
   */
  init() {

    // Set initial sort from select
    const sortSelect = document.getElementById('bundle-sort');
    if (sortSelect) {
      this.currentSort = sortSelect.value;
    }

    // Initial display
    this.applyFilters();

  },

  /**
   * Filter bundles by persona
   * @param {string} persona - Persona slug (office-worker, chronic-pain, athlete, etc.)
   */
  filterPersona(persona) {

    this.currentPersona = persona;

    // Update active tab
    document.querySelectorAll('.persona-tab').forEach(tab => {
      tab.classList.remove('active');
      if (tab.dataset.persona === persona) {
        tab.classList.add('active');
      }
    });

    this.applyFilters();

    // Track analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', 'filter_persona', {
        event_category: 'Bundles',
        event_label: persona,
        value: persona
      });
    }
  },

  /**
   * Filter bundles by tier
   * @param {string} tier - Tier slug (all, tier1, tier2, tier3, tier4)
   */
  filterTier(tier) {

    this.currentTier = tier;

    // Update active tab
    document.querySelectorAll('.tier-tab').forEach(tab => {
      tab.classList.remove('active');
      if (tab.dataset.tier === tier) {
        tab.classList.add('active');
      }
    });

    this.applyFilters();

    // Track analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', 'filter_tier', {
        event_category: 'Bundles',
        event_label: tier,
        value: tier
      });
    }
  },

  /**
   * Apply both persona and tier filters
   */
  applyFilters() {
    const bundleCards = document.querySelectorAll('.bundle-card');
    let visibleCount = 0;

    bundleCards.forEach(card => {
      const personaMatch = this.currentPersona === 'all' ||
                          card.dataset.persona === this.currentPersona;
      const tierMatch = this.currentTier === 'all' ||
                       card.dataset.tier === this.currentTier;

      if (personaMatch && tierMatch) {
        card.classList.remove('hidden');
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });

    // Update count display
    const countEl = document.getElementById('visible-count');
    if (countEl) {
      countEl.textContent = visibleCount;
    }

    // Show/hide no results message
    const noResultsEl = document.getElementById('no-results');
    const gridEl = document.getElementById('bundles-grid-container');

    if (visibleCount === 0) {
      if (noResultsEl) noResultsEl.style.display = 'block';
      if (gridEl) gridEl.style.display = 'none';
    } else {
      if (noResultsEl) noResultsEl.style.display = 'none';
      if (gridEl) gridEl.style.display = 'grid';
    }

    // Re-apply sort
    this.sortBundles(this.currentSort);

  },

  /**
   * Sort bundles
   * @param {string} sortBy - Sort method (savings, price-low, price-high, products, popular)
   */
  sortBundles(sortBy) {

    this.currentSort = sortBy;

    const grid = document.getElementById('bundles-grid-container');
    if (!grid) return;

    const cards = Array.from(grid.querySelectorAll('.bundle-card:not(.hidden)'));

    // Sort cards based on criteria
    cards.sort((a, b) => {
      switch (sortBy) {
        case 'savings':
          // Biggest savings first
          return parseFloat(b.dataset.savings) - parseFloat(a.dataset.savings);

        case 'price-low':
          // Lowest price first
          return parseFloat(a.dataset.price) - parseFloat(b.dataset.price);

        case 'price-high':
          // Highest price first
          return parseFloat(b.dataset.price) - parseFloat(a.dataset.price);

        case 'products':
          // Most products first
          return parseInt(b.dataset.products) - parseInt(a.dataset.products);

        case 'popular':
          // Popular (for now, same as savings - can be customized later)
          return parseFloat(b.dataset.savings) - parseFloat(a.dataset.savings);

        default:
          return 0;
      }
    });

    // Re-append cards in sorted order
    cards.forEach(card => {
      grid.appendChild(card);
    });

    // Track analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', 'sort_bundles', {
        event_category: 'Bundles',
        event_label: sortBy,
        value: sortBy
      });
    }
  },

  /**
   * Reset all filters
   */
  resetFilters() {

    this.filterPersona('all');
    this.filterTier('all');

    const sortSelect = document.getElementById('bundle-sort');
    if (sortSelect) {
      sortSelect.value = 'savings';
      this.sortBundles('savings');
    }
  },

  /**
   * Add bundle to cart (placeholder - to be implemented with Shopify API)
   * @param {string} bundleId - Bundle identifier
   */
  addToCart(bundleId) {

    // Track analytics
    if (typeof gtag !== 'undefined') {
      gtag('event', 'add_to_cart', {
        event_category: 'Bundles',
        event_label: bundleId,
        value: bundleId
      });
    }

    // TODO: Implement Shopify cart API integration
    // For now, show alert
    alert(`Bundle ${bundleId} will be added to cart. (Implementation pending: Shopify cart API)`);

    // Example Shopify cart API call:
    /*
    fetch('/cart/add.js', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        items: [{
          id: bundleVariantId,
          quantity: 1
        }]
      })
    })
    .then(response => response.json())
    .then(data => {
      // Update cart UI
      window.location.href = '/cart';
    })
    .catch(error => {
      console.error('Error adding bundle to cart:', error);
      alert('Error adding bundle to cart. Please try again.');
    });
    */
  },

  /**
   * Smooth scroll to bundles grid
   */
  scrollToBundles() {
    const grid = document.getElementById('bundles-grid');
    if (grid) {
      grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
};

// Initialize on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    bundlesFilter.init();
  });
} else {
  bundlesFilter.init();
}

// Export for global access
window.bundlesFilter = bundlesFilter;
