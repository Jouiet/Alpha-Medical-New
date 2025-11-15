/**
 * BUNDLE AUTO-CREATION API INTEGRATION
 * Add this code to bundle-builder-combined.js
 *
 * Functions to add:
 * 1. calculateProposalHash() - Calculate unique hash for product combination
 * 2. submitProposalToAPI() - Submit to Vercel API instead of contact form
 * 3. handleAPIResponse() - Show count/status to user
 */

// ============================================================================
// HASH CALCULATION (Add after CONFIG section)
// ============================================================================

/**
 * Calculate unique hash for product combination
 * Same products in different order = same hash
 */
function calculateProposalHash(productIds) {
  // Sort IDs numerically (ensures deterministic hash)
  const sorted = productIds.slice().sort((a, b) => a - b);

  // Join with delimiter
  const string = sorted.join('-');

  // Simple hash function (or use crypto.subtle.digest for SHA-256)
  let hash = 0;
  for (let i = 0; i < string.length; i++) {
    const char = string.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }

  // Return hash with prefix
  return `hash_${Math.abs(hash).toString(16).substring(0, 12)}`;
}

// ============================================================================
// API SUBMISSION (Replace Shopify Contact Form submission)
// ============================================================================

/**
 * Submit proposal to Vercel API
 * REPLACE the form submission with this API call
 */
async function submitProposalToAPI() {
  const emailInput = document.getElementById('customer-email');

  if (!emailInput) {
    console.error('[BundleBuilder] Email input not found');
    return;
  }

  const email = emailInput.value.trim();

  if (!email) {
    alert('Please enter your email address');
    return;
  }

  // Validate email
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    alert('Please enter a valid email address');
    return;
  }

  // Get product IDs
  const productIds = selectedProducts.map(p => p.id);

  if (productIds.length < CONFIG.minProducts || productIds.length > CONFIG.maxProducts) {
    alert(`Please select ${CONFIG.minProducts}-${CONFIG.maxProducts} products`);
    return;
  }

  // Calculate hash
  const proposalHash = calculateProposalHash(productIds);

  console.log('[BundleBuilder] Submitting proposal:', {
    product_ids: productIds,
    email: email,
    hash: proposalHash
  });

  // Show loading state
  const submitBtn = document.getElementById('submit-proposal-btn');
  const originalText = submitBtn ? submitBtn.textContent : '';

  if (submitBtn) {
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';
  }

  try {
    // IMPORTANT: Replace with your actual Vercel API URL
    const API_URL = 'https://YOUR-VERCEL-APP.vercel.app/api/submit';

    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        product_ids: productIds,
        email: email,
        hash: proposalHash
      })
    });

    const data = await response.json();

    if (response.ok && data.success) {
      handleAPISuccess(data);
    } else {
      handleAPIError(data.error || 'Unknown error');
    }

  } catch (error) {
    console.error('[BundleBuilder] API error:', error);
    handleAPIError('Network error. Please try again.');
  } finally {
    if (submitBtn) {
      submitBtn.disabled = false;
      submitBtn.textContent = originalText;
    }
  }
}

/**
 * Handle successful API response
 */
function handleAPISuccess(data) {
  const formContainer = document.getElementById('submission-form-container');

  if (data.bundle_created) {
    // BUNDLE WAS AUTO-CREATED!
    const successMessage = `
      <div class="bundle-auto-created-success">
        <div class="success-icon">🎉</div>
        <h2>Bundle Auto-Created!</h2>
        <p>Your proposed bundle has been created based on <strong>${data.count} identical proposals</strong>.</p>
        <h3>${data.bundle_title}</h3>
        <p class="bundle-price">
          <span class="original">was $${data.compare_at_price || 'XXX'}</span>
          <span class="sale">$${data.price || 'XXX'}</span>
          <span class="discount">35% OFF</span>
        </p>
        <a href="${data.bundle_url}" class="btn-shop-bundle">Shop This Bundle →</a>
        <p class="notification-note">You and ${data.count - 1} other customers will receive an email notification.</p>
      </div>
    `;

    if (formContainer) formContainer.innerHTML = successMessage;

    // Clear selected products
    selectedProducts = [];
    updateSelectedDisplay();

    // Track event (Google Analytics)
    if (typeof gtag !== 'undefined') {
      gtag('event', 'bundle_auto_created', {
        bundle_id: data.bundle_id,
        bundle_title: data.bundle_title,
        proposals_count: data.count
      });
    }

  } else {
    // PROPOSAL RECORDED (not yet 10+)
    const countMessage = `
      <div class="proposal-recorded-success">
        <div class="success-icon">✅</div>
        <h2>Proposal Recorded!</h2>
        <p>Your bundle proposal has been submitted.</p>
        <div class="proposal-count">
          <strong>${data.count} / ${CONFIG.threshold}</strong>
          <span>proposals received</span>
        </div>
        <p class="remaining-note"><strong>${data.remaining} more identical proposals</strong> needed for auto-creation.</p>
        <p class="notification-text">We'll notify you by email when this bundle is created.</p>
        <button onclick="location.reload()" class="btn-propose-another">Propose Another Bundle</button>
      </div>
    `;

    if (formContainer) formContainer.innerHTML = countMessage;

    // Track event (Google Analytics)
    if (typeof gtag !== 'undefined') {
      gtag('event', 'bundle_proposal_submitted', {
        proposal_count: data.count,
        remaining: data.remaining
      });
    }
  }
}

/**
 * Handle API error
 */
function handleAPIError(errorMessage) {
  const formContainer = document.getElementById('submission-form-container');

  const errorHTML = `
    <div class="proposal-error">
      <div class="error-icon">❌</div>
      <h2>Submission Error</h2>
      <p>${errorMessage}</p>
      <button onclick="location.reload()" class="btn-try-again">Try Again</button>
    </div>
  `;

  if (formContainer) formContainer.innerHTML = errorHTML;

  // Track error (Google Analytics)
  if (typeof gtag !== 'undefined') {
    gtag('event', 'bundle_proposal_error', {
      error_message: errorMessage
    });
  }
}

// ============================================================================
// INTEGRATION INSTRUCTIONS
// ============================================================================

/*

STEP 1: Add this code to assets/bundle-builder-combined.js

STEP 2: Replace the form submission handler

FIND this code in bundle-builder-combined.js:
```
// Somewhere near the bottom where form submission is handled
```

REPLACE with:
```
// Add button click handler
if (submitButton) {
  submitButton.addEventListener('click', (e) => {
    e.preventDefault();
    submitProposalToAPI(); // Call API instead of submitting form
  });
}
```

STEP 3: Update API_URL in submitProposalToAPI()

Replace:
```
const API_URL = 'https://YOUR-VERCEL-APP.vercel.app/api/submit';
```

With your actual Vercel deployment URL after deploying backend.

STEP 4: Add CSS for success/error messages

Add to assets/bundle-builder-combined.css:
```css
.bundle-auto-created-success,
.proposal-recorded-success,
.proposal-error {
  text-align: center;
  padding: 40px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.success-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.error-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.proposal-count {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px 0;
  padding: 30px;
  background: linear-gradient(135deg, #4A90E2 0%, #7FCCC9 100%);
  color: white;
  border-radius: 12px;
}

.proposal-count strong {
  font-size: 48px;
  font-weight: 700;
}

.btn-shop-bundle,
.btn-propose-another,
.btn-try-again {
  display: inline-block;
  margin-top: 20px;
  padding: 14px 32px;
  background: linear-gradient(135deg, #4A90E2 0%, #7FCCC9 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-shop-bundle:hover,
.btn-propose-another:hover,
.btn-try-again:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(74, 144, 226, 0.4);
}
```

*/
