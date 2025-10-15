/**
 * Recently Viewed Products
 * Stores and displays recently viewed products using localStorage
 * Alpha Medical Care - 2025
 */

class RecentlyViewedProducts {
  constructor(options = {}) {
    this.maxItems = options.maxItems || 4;
    this.storageKey = options.storageKey || 'alpha_recently_viewed';
    this.containerSelector = options.containerSelector || '[data-recently-viewed]';
  }

  /**
   * Add product to recently viewed list
   * @param {Object} productData - Product information
   */
  addProduct(productData) {
    if (!productData || !productData.id) {
      console.warn('[RecentlyViewed] Invalid product data');
      return;
    }

    try {
      let items = this.getProducts();

      // Remove product if already exists (to move it to front)
      items = items.filter(item => item.id !== productData.id);

      // Add product at the beginning
      items.unshift({
        id: productData.id,
        url: productData.url,
        title: productData.title,
        image: productData.image,
        price: productData.price,
        timestamp: Date.now()
      });

      // Keep only max items
      items = items.slice(0, this.maxItems);

      // Save to localStorage
      localStorage.setItem(this.storageKey, JSON.stringify(items));

      console.log('[RecentlyViewed] Product added:', productData.title);
    } catch (error) {
      console.error('[RecentlyViewed] Error adding product:', error);
    }
  }

  /**
   * Get all recently viewed products
   * @returns {Array} Array of product objects
   */
  getProducts() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      return stored ? JSON.parse(stored) : [];
    } catch (error) {
      console.error('[RecentlyViewed] Error reading from localStorage:', error);
      return [];
    }
  }

  /**
   * Render recently viewed products
   */
  render() {
    const container = document.querySelector(this.containerSelector);
    if (!container) {
      return;
    }

    const items = this.getProducts();

    // Don't render if no products or on product page for same product
    if (items.length === 0) {
      container.style.display = 'none';
      return;
    }

    // Build HTML
    const html = `
      <div class="recently-viewed">
        <div class="recently-viewed__header">
          <h2 class="recently-viewed__title">Recently Viewed</h2>
        </div>
        <div class="recently-viewed__grid">
          ${items.map(item => this.renderProductCard(item)).join('')}
        </div>
      </div>
    `;

    container.innerHTML = html;
    container.style.display = 'block';

    console.log('[RecentlyViewed] Rendered', items.length, 'products');
  }

  /**
   * Render single product card
   * @param {Object} item - Product data
   * @returns {string} HTML string
   */
  renderProductCard(item) {
    return `
      <a href="${item.url}" class="recently-viewed__card">
        <div class="recently-viewed__image-wrapper">
          <img
            src="${item.image}"
            alt="${this.escapeHtml(item.title)}"
            class="recently-viewed__image"
            loading="lazy"
          />
        </div>
        <div class="recently-viewed__content">
          <h3 class="recently-viewed__product-title">${this.escapeHtml(item.title)}</h3>
          <span class="recently-viewed__price">${item.price}</span>
        </div>
      </a>
    `;
  }

  /**
   * Escape HTML to prevent XSS
   * @param {string} text - Text to escape
   * @returns {string} Escaped text
   */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  /**
   * Clear all recently viewed products
   */
  clear() {
    try {
      localStorage.removeItem(this.storageKey);
      console.log('[RecentlyViewed] Cleared all products');
    } catch (error) {
      console.error('[RecentlyViewed] Error clearing products:', error);
    }
  }
}

// Initialize global instance
window.RecentlyViewedProducts = RecentlyViewedProducts;

// Auto-initialize if DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.recentlyViewed = new RecentlyViewedProducts();
  });
} else {
  window.recentlyViewed = new RecentlyViewedProducts();
}
