// CONFETTI CELEBRATION SYSTEM - AJAX-COMPATIBLE
(function() {
  'use strict';

  // Global confetti function
  window.triggerFreeShippingConfetti = function() {

    // Check if already celebrated recently
    const lastCelebration = sessionStorage.getItem('free_shipping_confetti_time');
    const now = Date.now();

    if (lastCelebration && (now - parseInt(lastCelebration)) < 5000) {
      return;
    }

    sessionStorage.setItem('free_shipping_confetti_time', now.toString());

    // Create container
    let container = document.getElementById('confetti-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'confetti-container';
      document.body.appendChild(container);
    }

    // Color palette (Alpha Medical brand colors + celebration colors)
    const colors = [
      '#4770DB', // Primary blue
      '#5b84e8', // Light blue
      '#28a745', // Success green
      '#ffc107', // Gold
      '#ff6b6b', // Coral
      '#4ecdc4', // Teal
      '#95e1d3', // Mint
      '#f38181'  // Rose
    ];

    // Shapes
    const shapes = ['square', 'circle', 'triangle'];

    // Generate 50 confetti pieces
    const confettiCount = 50;

    for (let i = 0; i < confettiCount; i++) {
      const confetti = document.createElement('div');
      confetti.className = 'confetti-piece falling';

      // Random shape
      const shape = shapes[Math.floor(Math.random() * shapes.length)];
      confetti.classList.add(shape);

      // Random color
      const color = colors[Math.floor(Math.random() * colors.length)];
      confetti.style.background = color;
      if (shape === 'triangle') {
        confetti.style.borderBottomColor = color;
      }

      // Random horizontal position
      confetti.style.left = Math.random() * 100 + '%';

      // Random animation properties
      const fallDuration = 2 + Math.random() * 1.5; // 2-3.5s
      const drift = (Math.random() - 0.5) * 200; // -100px to +100px drift
      const rotation = Math.random() * 720 - 360; // -360deg to +360deg

      confetti.style.setProperty('--fall-duration', fallDuration + 's');
      confetti.style.setProperty('--drift', drift + 'px');
      confetti.style.setProperty('--rotation', rotation + 'deg');

      // Add delay for staggered effect
      confetti.style.animationDelay = (Math.random() * 0.3) + 's';

      container.appendChild(confetti);
    }


    // Clean up after animations complete
    setTimeout(() => {
      if (container && container.parentNode) {
        container.remove();
      }
    }, 4000);
  };

  // Check for confetti trigger on DOM mutations (for AJAX cart updates)
  function checkConfettiTrigger() {
    const trigger = document.querySelector('[data-confetti-trigger="true"]');
    if (trigger && !trigger.hasAttribute('data-confetti-fired')) {
      trigger.setAttribute('data-confetti-fired', 'true');
      // Small delay to let UI settle
      setTimeout(() => {
        window.triggerFreeShippingConfetti();
      }, 200);
    }
  }

  // Initial check on script load
  checkConfettiTrigger();

  // Watch for DOM changes (AJAX cart updates)
  const observer = new MutationObserver(function(mutations) {
    checkConfettiTrigger();
  });

  // Start observing
  if (document.body) {
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  } else {
    // Body not ready yet, wait for DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function() {
      observer.observe(document.body, {
        childList: true,
        subtree: true
      });
      checkConfettiTrigger();
    });
  }

  // Also listen for cart:updated event as backup
  document.addEventListener('cart:updated', function() {
    setTimeout(checkConfettiTrigger, 500);
  });

})();
