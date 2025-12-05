#!/usr/bin/env python3
"""
CONFETTI DIAGNOSTIC - FORENSIC ANALYSIS
Vérifie FACTUELLEMENT chaque composant du système confetti
"""

import os
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_NAME = os.getenv('SHOPIFY_STORE_DOMAIN')

print("=" * 80)
print("CONFETTI DIAGNOSTIC - FORENSIC VERIFICATION")
print("=" * 80)
print()

# Generate comprehensive JavaScript diagnostic
js_diagnostic = """
console.clear();
console.log('='.repeat(80));
console.log('CONFETTI DIAGNOSTIC - FACTUAL VERIFICATION');
console.log('='.repeat(80));
console.log('');

// TEST 1: Check if free shipping message exists
console.log('TEST 1: Free Shipping Message');
const successMessage = document.querySelector('.free-shipping-message.success');
console.log('  Element exists:', !!successMessage);
if (successMessage) {
  console.log('  ✅ SUCCESS message found');
  console.log('  Text content:', successMessage.textContent.trim().substring(0, 50) + '...');
} else {
  console.log('  ❌ SUCCESS message NOT found');
}
console.log('');

// TEST 2: Check for data-confetti-trigger attribute
console.log('TEST 2: Confetti Trigger Attribute');
const triggerElement = document.querySelector('[data-confetti-trigger="true"]');
console.log('  Element exists:', !!triggerElement);
if (triggerElement) {
  console.log('  ✅ data-confetti-trigger="true" found');
  console.log('  Has data-confetti-fired:', triggerElement.hasAttribute('data-confetti-fired'));
  console.log('  data-confetti-fired value:', triggerElement.getAttribute('data-confetti-fired'));
} else {
  console.log('  ❌ data-confetti-trigger="true" NOT found');
  console.log('  PROBLEM: Liquid template not rendering attribute correctly');
}
console.log('');

// TEST 3: Check cart total vs threshold
console.log('TEST 3: Cart Total vs Threshold');
const wrapper = document.querySelector('.free-shipping-bar-wrapper');
if (wrapper) {
  const cartTotal = parseInt(wrapper.getAttribute('data-cart-total'));
  const threshold = parseInt(wrapper.getAttribute('data-threshold'));
  console.log('  Cart total:', cartTotal, '(' + (cartTotal/100) + ' USD)');
  console.log('  Threshold:', threshold, '(' + (threshold/100) + ' USD)');
  console.log('  Qualified:', cartTotal >= threshold ? '✅ YES' : '❌ NO');
} else {
  console.log('  ❌ Wrapper not found');
}
console.log('');

// TEST 4: Check if confetti function exists
console.log('TEST 4: Confetti Function');
console.log('  typeof window.triggerFreeShippingConfetti:', typeof window.triggerFreeShippingConfetti);
if (typeof window.triggerFreeShippingConfetti === 'function') {
  console.log('  ✅ Function exists');
} else {
  console.log('  ❌ Function NOT defined');
  console.log('  PROBLEM: Script not loaded or IIFE not executing');
}
console.log('');

// TEST 5: Check for confetti container
console.log('TEST 5: Confetti Container');
const container = document.getElementById('confetti-container');
console.log('  Container exists:', !!container);
if (container) {
  console.log('  ✅ Container found');
  console.log('  Children count:', container.children.length);
} else {
  console.log('  ❌ Container not created yet (normal if not triggered)');
}
console.log('');

// TEST 6: Check sessionStorage
console.log('TEST 6: SessionStorage Cooldown');
const lastCelebration = sessionStorage.getItem('free_shipping_confetti_time');
if (lastCelebration) {
  const timeSince = Date.now() - parseInt(lastCelebration);
  console.log('  Last celebration:', timeSince, 'ms ago');
  console.log('  Cooldown active:', timeSince < 5000 ? '⚠️  YES (blocking)' : '✅ NO');
  if (timeSince < 5000) {
    console.log('  CLEAR COOLDOWN: sessionStorage.clear()');
  }
} else {
  console.log('  No previous celebration');
}
console.log('');

// TEST 7: Manual trigger test
console.log('TEST 7: Manual Trigger Test');
console.log('  Run this command to force confetti:');
console.log('  → sessionStorage.clear(); window.triggerFreeShippingConfetti()');
console.log('');

// TEST 8: Check for JavaScript errors
console.log('TEST 8: Script Errors');
console.log('  Check console for red error messages above');
console.log('  If errors exist, script is broken');
console.log('');

// SUMMARY
console.log('='.repeat(80));
console.log('DIAGNOSTIC SUMMARY');
console.log('='.repeat(80));

let issues = [];

if (!successMessage) {
  issues.push('❌ Free shipping message not showing (cart < $150?)');
}

if (!triggerElement) {
  issues.push('❌ CRITICAL: data-confetti-trigger attribute missing in HTML');
}

if (typeof window.triggerFreeShippingConfetti !== 'function') {
  issues.push('❌ CRITICAL: Confetti function not defined (script not loaded)');
}

if (lastCelebration && (Date.now() - parseInt(lastCelebration)) < 5000) {
  issues.push('⚠️  Cooldown active - run: sessionStorage.clear()');
}

if (issues.length === 0) {
  console.log('✅ All checks passed - confetti should work');
  console.log('');
  console.log('MANUAL TEST:');
  console.log('sessionStorage.clear(); window.triggerFreeShippingConfetti()');
} else {
  console.log('ISSUES FOUND:');
  issues.forEach(issue => console.log('  ' + issue));
}

console.log('='.repeat(80));
"""

print("📋 INSTRUCTIONS:")
print()
print("1. Ouvrir https://" + SHOP_NAME)
print("2. Ajouter produits pour cart total >= $150")
print("3. Ouvrir Console Chrome (F12 → Console)")
print("4. Copier-coller ce script JavaScript:")
print()
print("─" * 80)
print(js_diagnostic)
print("─" * 80)
print()
print("5. Appuyez Enter")
print("6. Lire les résultats FACTUELS")
print("7. M'envoyer TOUS les messages de la console")
print()
print("=" * 80)
print("ATTENTE DE VOS RÉSULTATS POUR DIAGNOSTIC FACTUEL")
print("=" * 80)
