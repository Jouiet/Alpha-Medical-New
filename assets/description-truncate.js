/**
 * Description Truncate - Click to Expand
 * Alpha Medical - Session 98
 * Modern 2025 Web Component
 */

class DescriptionTruncate extends HTMLElement {
  constructor() {
    super();
    this.isExpanded = false;
  }

  connectedCallback() {
    this.content = this.querySelector('.description-truncate__content');
    this.toggle = this.querySelector('.description-truncate__toggle');
    this.label = this.querySelector('.description-truncate__label');
    this.fade = this.querySelector('.description-truncate__fade');

    this.labelMore = this.getAttribute('data-label-more') || 'Voir plus';
    this.labelLess = this.getAttribute('data-label-less') || 'Voir moins';

    if (!this.content || !this.toggle) return;

    // Check if truncation is needed
    requestAnimationFrame(() => {
      this.checkNeedsTruncation();
    });

    // Listen for toggle clicks
    this.toggle.addEventListener('click', () => this.handleToggle());

    // Recheck on resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
        if (!this.isExpanded) {
          this.checkNeedsTruncation();
        }
      }, 250);
    });
  }

  checkNeedsTruncation() {
    if (!this.content) return;

    // Temporarily expand to measure
    const originalMaxHeight = this.content.style.maxHeight;
    this.content.style.maxHeight = 'none';
    this.content.classList.add('is-expanded');

    const scrollHeight = this.content.scrollHeight;
    const computedStyle = getComputedStyle(this.content);
    const lineHeight = parseFloat(computedStyle.lineHeight) || 22.4;
    const lines = parseInt(getComputedStyle(this).getPropertyValue('--truncate-lines')) || 5;
    const maxHeight = lineHeight * lines;

    // Restore collapsed state
    this.content.style.maxHeight = originalMaxHeight;
    this.content.classList.remove('is-expanded');

    // Show/hide toggle based on content height
    if (scrollHeight > maxHeight + 20) {
      this.toggle.classList.remove('is-hidden');
      if (this.fade) this.fade.style.display = 'block';
    } else {
      this.toggle.classList.add('is-hidden');
      this.content.classList.add('is-expanded');
      if (this.fade) this.fade.style.display = 'none';
    }
  }

  handleToggle() {
    this.isExpanded = !this.isExpanded;

    if (this.isExpanded) {
      this.expand();
    } else {
      this.collapse();
    }
  }

  expand() {
    this.content.classList.add('is-expanded');
    this.toggle.classList.add('is-expanded');
    this.toggle.setAttribute('aria-expanded', 'true');
    if (this.label) this.label.textContent = this.labelLess;
    if (this.fade) this.fade.style.opacity = '0';
    this.classList.add('is-expanded');
  }

  collapse() {
    this.content.classList.remove('is-expanded');
    this.toggle.classList.remove('is-expanded');
    this.toggle.setAttribute('aria-expanded', 'false');
    if (this.label) this.label.textContent = this.labelMore;
    if (this.fade) this.fade.style.opacity = '1';
    this.classList.remove('is-expanded');

    // Scroll back into view if needed
    const rect = this.getBoundingClientRect();
    if (rect.top < 0) {
      this.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }
}

// Register the custom element
if (!customElements.get('description-truncate')) {
  customElements.define('description-truncate', DescriptionTruncate);
}
