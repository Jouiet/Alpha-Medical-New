import { NextResponse } from 'next/server';

export async function GET() {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://alphamedicalcare.com';

  // Static pages
  const staticPages = [
    { url: '', changefreq: 'daily', priority: 1.0 },
    { url: '/products', changefreq: 'daily', priority: 0.9 },
    { url: '/about', changefreq: 'monthly', priority: 0.7 },
    { url: '/contact', changefreq: 'monthly', priority: 0.7 },
    { url: '/blog', changefreq: 'weekly', priority: 0.8 },
  ];

  // Product slugs (in a real app, fetch these from Shopify)
  const productSlugs = [
    'medical-neck-traction-device',
    'neck-traction-device-inflatable',
    'posture-corrector-back-brace',
    'back-brace-lower-back-pain',
    'smart-cupping-massage-instrument',
    '5-in-1-smart-cupping-therapy-set',
    'electric-foot-hand-massager',
    'foot-air-pressure-leg-massage',
    'air-pressure-leg-massage-recovery-boots',
    'thermal-knee-massager',
    'heated-rehabilitation-robot-gloves',
    'relax-eye-massage-device',
    'finger-rehabilitation-exerciser-robot-gloves',
    'knee-brace-support-arthritis-pain',
    'achilles-tendon-rehabilitation-boots',
    'adjust-knee-brace-orthopedic-leg-support',
    'knee-ankle-foot-orthosis-hip-fracture',
    'led-facial-mask-neck-treatment',
    'smart-facial-massager-lifting-firming',
    '3-in-1-facial-lifting-device',
  ];

  const productPages = productSlugs.map(slug => ({
    url: `/products/${slug}`,
    changefreq: 'weekly',
    priority: 0.8,
  }));

  const allPages = [...staticPages, ...productPages];

  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages
  .map(
    (page) => `  <url>
    <loc>${baseUrl}${page.url}</loc>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
    <lastmod>${new Date().toISOString()}</lastmod>
  </url>`
  )
  .join('\n')}
</urlset>`;

  return new NextResponse(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600',
    },
  });
}
