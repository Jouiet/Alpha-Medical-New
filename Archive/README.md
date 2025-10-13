# 🏥 Alpha Medical Care E-commerce Platform

> Professional headless e-commerce platform for physiotherapy and wellness products

[![Next.js](https://img.shields.io/badge/Next.js-13+-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue)](https://www.typescriptlang.org/)
[![Shopify](https://img.shields.io/badge/Shopify-Storefront_API-green)](https://shopify.dev/)
[![Stripe](https://img.shields.io/badge/Stripe-Payments-purple)](https://stripe.com/)

## ✨ Features

- 🛒 **Full E-commerce**: Product browsing, filtering, cart, and checkout
- 💳 **Stripe Integration**: Secure payment processing
- 🏪 **Shopify Backend**: Headless architecture with Storefront API
- 📱 **Fully Responsive**: Mobile-first design
- 🎨 **Modern UI**: Built with Tailwind CSS and Radix UI
- 🔍 **SEO Optimized**: Schema.org markup, sitemap, meta tags
- ⚡ **Performance**: Server-side rendering with Next.js
- 🔐 **Type Safe**: Full TypeScript implementation

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Add your Shopify and Stripe credentials to .env.local

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the application.

## 📚 Documentation

- **[Setup Guide](./SETUP_GUIDE.md)** - Complete installation and configuration
- **[Environment Variables](./.env.example)** - Required API keys and settings

## 🛠️ Tech Stack

- **Framework**: Next.js 13+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI (shadcn/ui)
- **Backend**: Shopify Storefront API (GraphQL)
- **Payments**: Stripe
- **State Management**: React Context + localStorage
- **Icons**: Lucide React

## 📦 Project Structure

```
Alpha-Medical/
├── app/                    # Next.js 13 app directory
│   ├── page.tsx           # Homepage
│   ├── products/          # Product pages
│   ├── checkout/          # Checkout flow
│   ├── cart/              # Shopping cart
│   └── api/               # API routes
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── SEO/              # SEO components
│   ├── Header.tsx        # Navigation
│   ├── Footer.tsx        # Footer
│   └── StripeCheckout.tsx # Payment component
├── contexts/             # React contexts
│   └── CartContext.tsx   # Cart state management
├── lib/                  # Utility functions
│   ├── shopify.ts        # Shopify API client
│   ├── stripe.ts         # Stripe configuration
│   └── seo-config.ts     # SEO settings
├── public/               # Static assets
└── .env.example          # Environment variables template
```

## 🎯 Key Features

### Product Management
- 20+ professional physiotherapy products
- Advanced filtering (category, price, search)
- High-quality product images
- Detailed product descriptions with specs

### Shopping Experience
- Persistent shopping cart (localStorage)
- Real-time cart updates
- Product quantity management
- Responsive product gallery

### Checkout & Payments
- Two-step checkout process
- Stripe Elements integration
- Secure payment processing
- Order confirmation

### SEO & Performance
- Schema.org structured data
- Dynamic sitemap generation
- Optimized meta tags
- Server-side rendering
- Image optimization

## 🔧 Configuration

### Shopify Setup
1. Create a Shopify store
2. Enable Storefront API
3. Generate access token
4. Add products

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed instructions.

### Stripe Setup
1. Create Stripe account
2. Get API keys (test and live)
3. Configure webhooks
4. Add payment methods

## 🚢 Deployment

### Vercel (Recommended)
```bash
npm i -g vercel
vercel
```

### Other Platforms
- Netlify
- AWS Amplify
- Digital Ocean
- Railway

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for platform-specific instructions.

## 🧪 Testing

```bash
# Type checking
npm run typecheck

# Linting
npm run lint

# Build
npm run build
```

### Testing Stripe Payments
Use test card: `4242 4242 4242 4242`
- Expiry: Any future date
- CVC: Any 3 digits
- ZIP: Any 5 digits

## 📱 Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## 🤝 Contributing

This is a proprietary project. For authorized contributors:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

Proprietary - All rights reserved

## 👨‍💻 Developer

Built for Alpha Medical Care

---

**Need help?** Check the [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed documentation.
