# Alpha Medical Care E-commerce Setup Guide

## 📋 Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Shopify Configuration](#shopify-configuration)
- [Stripe Configuration](#stripe-configuration)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [SEO Configuration](#seo-configuration)

---

## 🎯 Overview

This is a **headless e-commerce platform** built for physiotherapy and wellness products, featuring:

- **Architecture**: Next.js 13+ (App Router) with TypeScript
- **Backend**: Shopify Storefront API (GraphQL)
- **Payments**: Stripe integration
- **Styling**: Tailwind CSS + Radix UI (shadcn/ui)
- **SEO**: Schema.org markup, sitemap, robots.txt
- **Features**: Cart management, product filtering, customer reviews, mobile-responsive design

---

## ✅ Prerequisites

Before you begin, ensure you have:

- **Node.js** 18+ installed
- A **Shopify** account (any plan)
- A **Stripe** account
- **Git** installed
- A code editor (VS Code recommended)

---

## 📦 Installation

### 1. Clone & Install Dependencies

```bash
# Navigate to project directory
cd Alpha-Medical

# Install dependencies
npm install
```

---

## 🛍️ Shopify Configuration

### Step 1: Create a Shopify Store
1. Go to https://www.shopify.com/
2. Sign up for a Shopify account
3. Complete the store setup

### Step 2: Enable Storefront API
1. In Shopify Admin, go to **Settings** → **Apps and sales channels**
2. Click **Develop apps**
3. Click **Create an app**
4. Name it "Alpha Medical Care Headless"
5. Go to **Configuration** tab
6. Under **Storefront API**, click **Configure**
7. Enable these scopes:
   - `unauthenticated_read_product_listings`
   - `unauthenticated_read_product_inventory`
   - `unauthenticated_read_product_tags`
   - `unauthenticated_read_collection_listings`
   - `unauthenticated_read_customers`
8. Click **Save**
9. Go to **API credentials** tab
10. Copy the **Storefront API access token**

### Step 3: Add Products
1. Go to **Products** → **Add product**
2. Add the 20 products from the list below (or use the provided CSV import)
3. For each product, add:
   - Title
   - Description
   - Price
   - Images (use Pexels or Unsplash for high-quality photos)
   - Inventory quantity

### Product List:
**Pain Relief & Relaxation:**
- Medical Neck Traction Device
- Neck Traction Device Inflatable
- Posture Corrector Back Brace
- Back Brace for Lower Back Pain
- Smart Cupping Massage Instrument
- 5-in-1 Smart Cupping Therapy Set
- Electric Foot and Hand Massager
- Foot Air Pressure Leg Massage
- Air Pressure Leg Massage Recovery Boots
- Thermal Knee Massager
- Relax Eye Massage Device

**Rehabilitation & Mobility:**
- Heated Rehabilitation Robot Gloves
- Finger Rehabilitation Exerciser Robot Gloves
- Knee Brace Support for Arthritis Pain
- Achilles Tendon Rehabilitation Boots
- Adjust Knee Brace Orthopedic Leg Support
- Knee Ankle Foot Orthosis for Hip Fracture

**Wellness & Beauty:**
- LED Facial Mask with Neck Treatment
- Smart Facial Massager Lifting and Firming
- 3 In 1 Facial Lifting Device

---

## 💳 Stripe Configuration

### Step 1: Create Stripe Account
1. Go to https://stripe.com/
2. Sign up for an account
3. Complete account verification

### Step 2: Get API Keys
1. Go to **Developers** → **API keys**
2. Copy your **Publishable key** (starts with `pk_`)
3. Copy your **Secret key** (starts with `sk_`)

⚠️ **Important**: Use **test keys** for development (they start with `pk_test_` and `sk_test_`)

### Step 3: Configure Webhook (Optional for production)
1. Go to **Developers** → **Webhooks**
2. Click **Add endpoint**
3. Enter your webhook URL: `https://yourdomain.com/api/webhooks/stripe`
4. Select events to listen to:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Copy the **Signing secret** (starts with `whsec_`)

---

## 🔐 Environment Variables

### Create `.env.local` file

In the root directory, create a `.env.local` file:

```bash
cp .env.example .env.local
```

### Fill in your credentials:

```env
# Shopify Configuration
NEXT_PUBLIC_SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
NEXT_PUBLIC_SHOPIFY_STOREFRONT_ACCESS_TOKEN=your_storefront_access_token_here

# Stripe Configuration
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Application Configuration
NEXT_PUBLIC_SITE_URL=http://localhost:3000
NEXT_PUBLIC_SITE_NAME=Alpha Medical Care
NEXT_PUBLIC_SITE_DESCRIPTION=Professional Physiotherapy & Wellness Equipment
```

---

## 🚀 Running the Application

### Development Mode

```bash
npm run dev
```

Open http://localhost:3000 in your browser.

### Build for Production

```bash
npm run build
npm start
```

### Type Checking

```bash
npm run typecheck
```

### Linting

```bash
npm run lint
```

---

## 🌐 Deployment

### Deploy to Vercel (Recommended)

1. Push your code to GitHub
2. Go to https://vercel.com/
3. Import your repository
4. Add environment variables from `.env.local`
5. Deploy

```bash
# Or use Vercel CLI
npm i -g vercel
vercel
```

### Deploy to Other Platforms

The app can be deployed to any platform that supports Next.js:
- **Netlify**: Follow their Next.js deployment guide
- **AWS Amplify**: Use their console or CLI
- **Digital Ocean**: Use App Platform
- **Railway**: Connect your GitHub repo

**Important**: Always add your environment variables in the platform's settings!

---

## 🔍 SEO Configuration

### Sitemap
The sitemap is automatically generated at `/sitemap.xml`

### Robots.txt
Located at `/public/robots.txt` - update it with your production domain

### Schema.org Markup
The following schemas are already implemented:
- **ProductSchema**: For individual products
- **OrganizationSchema**: For company info
- **FAQSchema**: For FAQ sections
- **BreadcrumbSchema**: For navigation
- **WebsiteSchema**: For site-wide info

### Google Search Console
1. Go to https://search.google.com/search-console
2. Add your property
3. Verify ownership
4. Submit sitemap: `https://yourdomain.com/sitemap.xml`

### Performance Optimization
- Images are optimized with Next.js Image component
- Lazy loading enabled
- Code splitting automatic
- Static generation for product pages

---

## 📱 Testing Stripe Payments

Use these test card numbers:

| Card Number | Scenario |
|------------|----------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 9995 | Decline |
| 4000 0025 0000 3155 | Requires authentication |

- Use any future expiry date (e.g., 12/25)
- Use any 3-digit CVC
- Use any 5-digit postal code

---

## 🆘 Troubleshooting

### Common Issues

**1. Shopify API returns empty products**
- Check that products are published to the "Online Store" sales channel
- Verify Storefront API token has correct permissions

**2. Stripe payment fails**
- Ensure you're using test keys in development
- Check browser console for errors
- Verify webhook endpoint is correct

**3. Build errors**
- Run `npm install` to ensure all dependencies are installed
- Check TypeScript errors with `npm run typecheck`
- Clear `.next` folder: `rm -rf .next`

**4. Environment variables not working**
- Restart dev server after changing `.env.local`
- Ensure variables start with `NEXT_PUBLIC_` for client-side access
- Check for typos in variable names

---

## 📞 Support

For issues or questions:
- Check documentation at `/docs`
- Review Shopify Storefront API docs: https://shopify.dev/api/storefront
- Review Stripe docs: https://stripe.com/docs
- Open an issue on GitHub

---

## 📄 License

This project is proprietary. All rights reserved.

---

**Built with ❤️ for Alpha Medical Care**
