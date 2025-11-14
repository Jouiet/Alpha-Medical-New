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
   * Validate if product URL exists
   * @param {string} url - Product URL
   * @returns {Promise<boolean>} True if product exists
   */
  async validateProduct(url) {
    try {
      const response = await fetch(url, { method: 'HEAD' });
      return response.ok;
    } catch (error) {
      console.warn('[RecentlyViewed] Error validating product:', url, error);
      return false;
    }
  }

  /**
   * Render recently viewed products (without validation - direct display)
   */
  async render() {
    const container = document.querySelector(this.containerSelector);
    if (!container) {
      return;
    }

    let items = this.getProducts();

    // Don't render if no products
    if (items.length === 0) {
      container.style.display = 'none';
      console.log('[RecentlyViewed] No products to display');
      return;
    }

    // Filter out items with missing data
    items = items.filter(item => item.url && item.image && item.title && item.price);

    if (items.length === 0) {
      container.style.display = 'none';
      console.log('[RecentlyViewed] No valid product data');
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

    console.log('[RecentlyViewed] Rendered', items.length, 'product(s)');
  }

  /**
   * Render single product card
   * @param {Object} item - Product data
   * @returns {string} HTML string
   */
  renderProductCard(item) {
    // Clean image URL - ensure it's properly formatted
    const imageUrl = item.image || '';
    const escapedUrl = imageUrl.replace(/"/g, '&quot;');

    return `
      <a href="${item.url}" class="recently-viewed__card">
        <div class="recently-viewed__image-wrapper">
          <img
            src="${escapedUrl}"
            alt="${this.escapeHtml(item.title)}"
            class="recently-viewed__image"
            loading="lazy"
            onerror="this.onerror=null; this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22400%22 height=%22400%22%3E%3Crect fill=%22%23f3f4f6%22 width=%22400%22 height=%22400%22/%3E%3Ctext fill=%22%239ca3af%22 font-family=%22sans-serif%22 font-size=%2218%22 dy=%2210.5%22 font-weight=%22bold%22 x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22%3EImage unavailable%3C/text%3E%3C/svg%3E';"
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
