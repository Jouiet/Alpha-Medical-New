/**
 * Bundle Product Mapping
 * Maps individual products to bundles they belong to
 * Alpha Medical Care - 2025
 */

window.BUNDLE_PRODUCT_MAP = {
  // Mapping format: product_keyword => [bundle_handles]

  // Office Worker bundles
  'posture-corrector': ['office-worker-essential-kit', 'office-worker-advanced-ergonomic', 'ultimate-pain-management-system'],
  'cervical-neck-traction': ['office-worker-essential-kit'],
  'wrist-brace': ['office-worker-essential-kit'],
  'carpal-tunnel': ['office-worker-essential-kit', 'senior-mobility-support'],
  'head-eye-massager': ['office-worker-essential-kit', 'office-worker-premium-workspace'],
  'neck-massage': ['office-worker-essential-kit'],
  'magnetic-posture': ['office-worker-advanced-ergonomic'],
  'led-vibrating-neck': ['office-worker-advanced-ergonomic'],
  'adjustable-cervical-collar': ['office-worker-advanced-ergonomic', 'post-surgery-recovery-complete'],
  'ems-red-light-eye': ['office-worker-advanced-ergonomic'],

  // Senior bundles
  'hinged-knee-brace': ['senior-mobility-support', 'active-athlete-complete-protection'],
  'ankle-support-brace': ['senior-mobility-support'],
  'back-brace-posture': ['senior-mobility-support'],
  'velpeau-neck-traction': ['senior-mobility-support', 'post-surgery-recovery-complete'],
  'velpeau-wrist': ['senior-mobility-support'],
  'bunion-corrector': ['senior-advanced-arthritis'],

  // Chronic Pain bundles
  'tourmaline-magnetic-knee': ['chronic-pain-starter-kit'],
  'lumbar-support-belt': ['chronic-pain-starter-kit', 'chronic-pain-relief-kit', 'ultimate-pain-management-system'],
  'electric-foot-hand-massager': ['chronic-pain-starter-kit'],
  'stomach-massager': ['chronic-pain-starter-kit'],
  'electric-lumbar-massager': ['chronic-pain-relief-kit', 'chronic-pain-whole-body'],
  'electric-ankle-brace': ['chronic-pain-relief-kit'],
  'foreverlily-smart-knee': ['chronic-pain-whole-body'],
  'electric-medical-cupping': ['chronic-pain-whole-body'],

  // Athlete bundles
  'sports-knee-pads': ['active-athlete-knee-specialist'],
  'knee-patellar-tendon': ['active-athlete-knee-specialist'],
  'dynamic-knee-support': ['active-athlete-knee-specialist'],
  'neenca-hinged-knee': ['active-athlete-complete-protection'],
  'drop-foot-brace': ['active-athlete-complete-protection'],
  'basketball-knee-pad': ['active-athlete-complete-protection'],
  'leg-compression-sleeve': ['active-athlete-complete-protection'],
  'elbow-brace': ['active-athlete-complete-protection'],

  // Rehab bundles
  'rehabilitation-robot-gloves': ['rehab-stroke-recovery'],

  // Beauty bundles
  '7-color-led': ['beauty-wellness-led-complete'],
  'v-line-face': ['beauty-wellness-led-complete'],
  'face-lifting-device': ['beauty-wellness-led-complete'],
  'led-facial-mask': ['office-worker-premium-workspace'],
  'neck-led-lift': ['office-worker-premium-workspace'],
  'hello-face-red-light': ['chronic-pain-whole-body']
};

window.BUNDLE_DATA = {
  'office-worker-essential-kit': {
    title: 'Office Worker Essential Kit',
    price: '$218.71',
    regularPrice: '$336.48',
    savings: '$117.77',
    url: '/products/office-worker-essential-kit'
  },
  'senior-mobility-support': {
    title: 'Senior Mobility Support',
    price: '$259.63',
    regularPrice: '$399.43',
    savings: '$139.80',
    url: '/products/senior-mobility-support'
  },
  'chronic-pain-starter-kit': {
    title: 'Chronic Pain Starter Kit',
    price: '$181.11',
    regularPrice: '$278.63',
    savings: '$97.52',
    url: '/products/chronic-pain-starter-kit'
  },
  'active-athlete-knee-specialist': {
    title: 'Active Athlete Knee Specialist',
    price: '$196.66',
    regularPrice: '$302.56',
    savings: '$105.90',
    url: '/products/active-athlete-knee-specialist'
  },
  'active-athlete-complete-protection': {
    title: 'Active Athlete Complete Protection',
    price: '$322.91',
    regularPrice: '$496.79',
    savings: '$173.88',
    url: '/products/active-athlete-complete-protection'
  },
  'chronic-pain-relief-kit': {
    title: 'Chronic Pain Relief Kit',
    price: '$290.36',
    regularPrice: '$446.71',
    savings: '$156.35',
    url: '/products/chronic-pain-relief-kit'
  },
  'office-worker-advanced-ergonomic': {
    title: 'Office Worker Advanced Ergonomic',
    price: '$292.86',
    regularPrice: '$450.56',
    savings: '$157.70',
    url: '/products/office-worker-advanced-ergonomic'
  },
  'rehab-stroke-recovery': {
    title: 'Rehab Stroke Recovery',
    price: '$258.51',
    regularPrice: '$397.71',
    savings: '$139.20',
    url: '/products/rehab-stroke-recovery'
  },
  'beauty-wellness-led-complete': {
    title: 'Beauty & Wellness LED Complete',
    price: '$315.05',
    regularPrice: '$484.70',
    savings: '$169.65',
    url: '/products/beauty-wellness-led-complete'
  },
  'post-surgery-recovery-complete': {
    title: 'Post Surgery Recovery Complete',
    price: '$478.76',
    regularPrice: '$736.48',
    savings: '$257.72',
    url: '/products/post-surgery-recovery-complete'
  },
  'office-worker-premium-workspace': {
    title: 'Office Worker Premium Workspace',
    price: '$414.52',
    regularPrice: '$637.72',
    savings: '$223.20',
    url: '/products/office-worker-premium-workspace'
  },
  'chronic-pain-whole-body': {
    title: 'Chronic Pain Whole Body',
    price: '$448.92',
    regularPrice: '$690.65',
    savings: '$241.73',
    url: '/products/chronic-pain-whole-body'
  },
  'senior-advanced-arthritis': {
    title: 'Senior Advanced Arthritis',
    price: '$457.67',
    regularPrice: '$704.11',
    savings: '$246.44',
    url: '/products/senior-advanced-arthritis'
  },
  'ultimate-pain-management-system': {
    title: 'Ultimate Pain Management System',
    price: '$619.82',
    regularPrice: '$953.57',
    savings: '$333.75',
    url: '/products/ultimate-pain-management-system'
  }
};

/**
 * Find bundles containing a product
 * @param {string} productHandle - Product handle
 * @returns {Array} Array of bundle handles
 */
window.findBundlesForProduct = function(productHandle) {
  const bundles = [];

  for (const [keyword, bundleHandles] of Object.entries(window.BUNDLE_PRODUCT_MAP)) {
    if (productHandle.includes(keyword)) {
      bundles.push(...bundleHandles);
    }
  }

  // Return unique bundles
  return [...new Set(bundles)];
};

/**
 * Get bundle data by handle
 * @param {string} handle - Bundle handle
 * @returns {Object|null} Bundle data or null
 */
window.getBundleData = function(handle) {
  return window.BUNDLE_DATA[handle] || null;
};
