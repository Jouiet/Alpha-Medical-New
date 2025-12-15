/**
 * Description Truncate - Click to Expand
 * Alpha Medical - Session 98
 * Web Component for truncating long descriptions
 */

if (!customElements.get('description-truncate')) {
  customElements.define(
    'description-truncate',
    class DescriptionTruncate extends HTMLElement {
      constructor() {
        super();
        this.content = this.querySelector('.description-truncate__content');
        this.toggle = this.querySelector('.description-truncate__toggle');
        this.labelMore = this.dataset.labelMore || 'Voir plus';
        this.labelLess = this.dataset.labelLess || 'Voir moins';
        this.maxLines = parseInt(this.dataset.maxLines) || 5;
      }

      connectedCallback() {
        // Check if content needs truncation
        this.checkContentHeight();

        // Add click handler
        if (this.toggle) {
          this.toggle.addEventListener('click', this.handleToggle.bind(this));
        }

        // Recheck on window resize (content may reflow)
        this.resizeObserver = new ResizeObserver(() => {
          if (!this.isExpanded) {
            this.checkContentHeight();
          }
        });
        this.resizeObserver.observe(this.content);
      }

      disconnectedCallback() {
        if (this.resizeObserver) {
          this.resizeObserver.disconnect();
        }
      }

      checkContentHeight() {
        if (!this.content || !this.toggle) return;

        // Temporarily remove collapsed class to measure full height
        const wasCollapsed = this.content.classList.contains('is-collapsed');
        this.content.classList.remove('is-collapsed');
        this.content.style.maxHeight = 'none';

        const fullHeight = this.content.scrollHeight;
        const lineHeight = parseFloat(getComputedStyle(this.content).lineHeight) || 25.6;
        const maxHeight = lineHeight * this.maxLines;

        // Restore collapsed state
        this.content.style.maxHeight = '';

        // Only show toggle if content exceeds max lines
        if (fullHeight > maxHeight + 10) { // 10px tolerance
          this.toggle.classList.remove('is-hidden');
          if (wasCollapsed || !this.isExpanded) {
            this.content.classList.add('is-collapsed');
          }
        } else {
          this.toggle.classList.add('is-hidden');
          this.content.classList.remove('is-collapsed');
        }
      }

      handleToggle() {
        this.isExpanded = !this.isExpanded;

        if (this.isExpanded) {
          this.content.classList.remove('is-collapsed');
          this.content.classList.add('is-expanded');
          this.toggle.classList.add('is-expanded');
          this.toggle.querySelector('.description-truncate__label').textContent = this.labelLess;
          this.toggle.setAttribute('aria-expanded', 'true');
        } else {
          this.content.classList.add('is-collapsed');
          this.content.classList.remove('is-expanded');
          this.toggle.classList.remove('is-expanded');
          this.toggle.querySelector('.description-truncate__label').textContent = this.labelMore;
          this.toggle.setAttribute('aria-expanded', 'false');

          // Scroll back to top of description if needed
          const rect = this.getBoundingClientRect();
          if (rect.top < 0) {
            this.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }
      }
    }
  );
}
