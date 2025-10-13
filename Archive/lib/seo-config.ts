export const siteConfig = {
  name: 'Alpha Medical Care',
  description: 'Professional Physiotherapy & Wellness Equipment - Medical-grade devices for pain relief, rehabilitation, and recovery',
  url: process.env.NEXT_PUBLIC_SITE_URL || 'https://alphamedicalcare.com',
  ogImage: '/og-image.jpg',
  links: {
    facebook: 'https://facebook.com/alphamedicalcare',
    instagram: 'https://instagram.com/alphamedicalcare',
    twitter: 'https://twitter.com/alphamedicalcare',
    linkedin: 'https://linkedin.com/company/alphamedicalcare'
  },
  contact: {
    email: 'support@alphamedicalcare.com',
    phone: '+1 (555) 123-4567'
  }
};

export const defaultMetadata = {
  title: 'Alpha Medical Care - Professional Physiotherapy Equipment',
  description: 'Shop medical-grade physiotherapy and wellness equipment. From pain relief devices to rehabilitation tools, trusted by healthcare professionals worldwide.',
  keywords: 'physiotherapy equipment, medical devices, pain relief, rehabilitation, wellness, massage therapy, posture correction, neck traction, recovery boots'
};

// Page-specific metadata
export const pageMetadata = {
  home: {
    title: 'Alpha Medical Care - Professional Physiotherapy & Wellness Equipment',
    description: 'Discover premium medical-grade physiotherapy equipment for pain relief, rehabilitation, and wellness. Trusted by healthcare professionals. Free shipping on orders over $100.',
    keywords: 'physiotherapy equipment, medical devices, pain relief, wellness products, professional healthcare equipment'
  },
  products: {
    title: 'All Products - Alpha Medical Care',
    description: 'Browse our complete collection of professional physiotherapy and wellness equipment. Medical-grade devices for pain relief, rehabilitation, and recovery.',
    keywords: 'buy physiotherapy equipment, medical devices online, pain relief products, rehabilitation equipment'
  },
  about: {
    title: 'About Us - Alpha Medical Care',
    description: 'Learn about Alpha Medical Care - your trusted source for professional physiotherapy equipment. We provide medical-grade devices backed by expert support.',
    keywords: 'about alpha medical care, medical equipment supplier, professional physiotherapy'
  },
  contact: {
    title: 'Contact Us - Alpha Medical Care',
    description: 'Get in touch with our expert team for personalized advice on physiotherapy equipment. Professional support available 24/7.',
    keywords: 'contact alpha medical care, customer support, physiotherapy advice'
  },
  blog: {
    title: 'Health & Wellness Blog - Alpha Medical Care',
    description: 'Expert articles on pain relief, rehabilitation techniques, and wellness tips. Learn how to use physiotherapy equipment effectively.',
    keywords: 'physiotherapy blog, pain relief tips, rehabilitation exercises, wellness advice'
  }
};
