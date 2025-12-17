#!/usr/bin/env python3
"""
Alpha Medical Voice AI - Dynamic Knowledge Base Builder
Session 109 - xAI Voice Agent Infrastructure

This module creates a dynamic knowledge base that:
1. Fetches ALL products from Shopify API in real-time
2. Includes business info, FAQ, shipping, return policies
3. Auto-updates on each call (handles future products automatically)
4. Outputs structured JSON for xAI Voice Agent RAG

Usage:
    python3 voice_knowledge_base.py --output knowledge_base.json
    python3 voice_knowledge_base.py --mode refresh  # Force refresh cache
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Load environment
from dotenv import load_dotenv
load_dotenv('.env')
load_dotenv('.env.admin')

# Shopify Configuration
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN', 'azffej-as.myshopify.com')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_API_VERSION = '2025-01'

# Knowledge Base Configuration
CACHE_DIR = Path(__file__).parent / 'cache'
CACHE_FILE = CACHE_DIR / 'knowledge_base_cache.json'
CACHE_MAX_AGE_HOURS = 1  # Refresh cache if older than 1 hour


class KnowledgeBaseBuilder:
    """Builds dynamic knowledge base for Voice AI from Shopify data."""

    def __init__(self):
        self.base_url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{SHOPIFY_API_VERSION}"
        self.headers = {
            'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
            'Content-Type': 'application/json'
        }
        CACHE_DIR.mkdir(exist_ok=True)

    def fetch_all_products(self) -> List[Dict]:
        """Fetch ALL products from Shopify (handles pagination)."""
        products = []
        url = f"{self.base_url}/products.json?limit=250&status=active"

        while url:
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                data = response.json()
                products.extend(data.get('products', []))

                # Handle pagination via Link header
                link_header = response.headers.get('Link', '')
                url = None
                if 'rel="next"' in link_header:
                    for part in link_header.split(','):
                        if 'rel="next"' in part:
                            url = part.split('<')[1].split('>')[0]
                            break
            except Exception as e:
                print(f"❌ Error fetching products: {e}")
                break

        print(f"✅ Fetched {len(products)} products from Shopify")
        return products

    def fetch_collections(self) -> List[Dict]:
        """Fetch all collections for categorization."""
        try:
            response = requests.get(
                f"{self.base_url}/custom_collections.json?limit=250",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            collections = response.json().get('custom_collections', [])

            # Also fetch smart collections
            response2 = requests.get(
                f"{self.base_url}/smart_collections.json?limit=250",
                headers=self.headers,
                timeout=30
            )
            if response2.status_code == 200:
                collections.extend(response2.json().get('smart_collections', []))

            print(f"✅ Fetched {len(collections)} collections")
            return collections
        except Exception as e:
            print(f"⚠️ Error fetching collections: {e}")
            return []

    def format_product_for_voice(self, product: Dict) -> Dict:
        """Format product data for voice agent knowledge base."""
        # Get price range
        variants = product.get('variants', [])
        prices = [float(v.get('price', 0)) for v in variants if v.get('price')]
        min_price = min(prices) if prices else 0
        max_price = max(prices) if prices else 0

        # Get available variants
        available_variants = [
            {
                'title': v.get('title', 'Default'),
                'price': float(v.get('price', 0)),
                'available': v.get('inventory_quantity', 0) > 0
            }
            for v in variants
        ]

        # Clean description (remove HTML)
        import re
        description = product.get('body_html', '') or ''
        description = re.sub(r'<[^>]+>', '', description)
        description = re.sub(r'\s+', ' ', description).strip()

        return {
            'id': product.get('id'),
            'title': product.get('title', ''),
            'handle': product.get('handle', ''),
            'product_type': product.get('product_type', 'Medical Equipment'),
            'vendor': product.get('vendor', 'Alpha Medical'),
            'description': description[:500] + '...' if len(description) > 500 else description,
            'price_range': {
                'min': min_price,
                'max': max_price,
                'formatted': f"${min_price:.2f}" if min_price == max_price else f"${min_price:.2f} - ${max_price:.2f}"
            },
            'variants': available_variants,
            'tags': product.get('tags', '').split(', ') if product.get('tags') else [],
            'in_stock': any(v['available'] for v in available_variants),
            'url': f"https://alphamedical.shop/products/{product.get('handle', '')}"
        }

    def get_business_info(self) -> Dict:
        """Static business information for knowledge base."""
        return {
            'name': 'Alpha Medical Care',
            'domain': 'alphamedical.shop',
            'description': 'B2C retailer specializing in medical-grade orthopedic equipment, pain relief products, and recovery devices.',
            'tagline': 'Making Medical-Grade Recovery Accessible to Everyone',
            'contact': {
                'email': 'support@alphamedical.shop',
                'hours': '24/7 AI Support, Business Hours for Human Support: Mon-Fri 9AM-5PM EST'
            },
            'location': 'United States',
            'currency': 'USD',
            'target_customers': ['Seniors with arthritis/joint pain', 'Office workers with posture issues', 'Athletes for injury prevention/recovery']
        }

    def get_shipping_info(self) -> Dict:
        """Shipping policy information."""
        return {
            'free_shipping_threshold': 150.00,
            'standard_shipping': {
                'name': 'Standard Shipping',
                'time': '7-15 business days',
                'cost': 'Free over $150, otherwise $5.99'
            },
            'expedited_shipping': {
                'name': 'Expedited Shipping',
                'time': '6-8 business days',
                'cost': '$12.99'
            },
            'processing_time': '1-2 business days',
            'tracking': 'Tracking number provided via email once shipped',
            'international': 'Currently shipping to USA only'
        }

    def get_return_policy(self) -> Dict:
        """Return policy information."""
        return {
            'return_window': '30 days from delivery',
            'condition': 'Items must be unused, in original packaging',
            'refund_method': 'Original payment method, processed within 5-7 business days',
            'exchange': 'Free exchanges for different sizes/variants',
            'non_returnable': ['Personalized items', 'Items marked as final sale'],
            'process': 'Contact support@alphamedical.shop to initiate return'
        }

    def get_faq(self) -> List[Dict]:
        """Frequently asked questions."""
        return [
            {
                'question': 'How do I track my order?',
                'answer': 'Once your order ships, you will receive an email with your tracking number. You can also check your order status by logging into your account on our website.'
            },
            {
                'question': 'What payment methods do you accept?',
                'answer': 'We accept all major credit cards including Visa, Mastercard, American Express, and Discover. We also accept Apple Pay and Google Pay. PayPal is not currently accepted.'
            },
            {
                'question': 'How do I choose the right size?',
                'answer': 'Each product page includes a detailed sizing guide. Measure yourself according to the instructions and compare with our size chart. If you are between sizes, we recommend sizing up for comfort.'
            },
            {
                'question': 'Are your products medical grade?',
                'answer': 'Yes! We work exclusively with ISO 13485 certified suppliers. Every product is personally tested for 2 weeks before listing. We only carry top-rated suppliers with 4.5-5 star ratings.'
            },
            {
                'question': 'Can I cancel or modify my order?',
                'answer': 'Orders can be cancelled or modified within 2 hours of placement. After that, the order enters processing and cannot be changed. Contact us immediately at support@alphamedical.shop if you need to make changes.'
            },
            {
                'question': 'Do you offer discounts for bulk orders?',
                'answer': 'Yes, we offer volume discounts for orders of 5 or more items. Contact our support team for a custom quote.'
            },
            {
                'question': 'How long does delivery take?',
                'answer': 'Standard shipping takes 7-15 business days. Expedited shipping takes 6-8 business days. Processing time is 1-2 business days before shipping.'
            },
            {
                'question': 'What is your return policy?',
                'answer': 'We offer a 30-day return policy. Items must be unused and in original packaging. Refunds are processed within 5-7 business days to your original payment method.'
            },
            {
                'question': 'Do you ship internationally?',
                'answer': 'Currently, we only ship within the United States. We are working on expanding to Canada and other countries in 2026.'
            },
            {
                'question': 'How do I contact customer support?',
                'answer': 'You can reach us via email at support@alphamedical.shop, or use this voice assistant 24/7. For urgent matters, our team responds within 24 hours during business days.'
            }
        ]

    def build_knowledge_base(self, force_refresh: bool = False) -> Dict:
        """Build complete knowledge base for voice agent."""

        # Check cache
        if not force_refresh and CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r') as f:
                    cached = json.load(f)
                    cache_time = datetime.fromisoformat(cached.get('generated_at', '2000-01-01'))
                    age_hours = (datetime.now() - cache_time).total_seconds() / 3600
                    if age_hours < CACHE_MAX_AGE_HOURS:
                        print(f"✅ Using cached knowledge base (age: {age_hours:.1f}h)")
                        return cached
            except Exception as e:
                print(f"⚠️ Cache read error: {e}")

        print("🔄 Building fresh knowledge base...")

        # Fetch products and collections
        products = self.fetch_all_products()
        collections = self.fetch_collections()

        # Format products for voice
        formatted_products = [self.format_product_for_voice(p) for p in products]

        # Group by product type
        products_by_type = {}
        for p in formatted_products:
            ptype = p.get('product_type', 'Other')
            if ptype not in products_by_type:
                products_by_type[ptype] = []
            products_by_type[ptype].append(p)

        # Build complete knowledge base
        knowledge_base = {
            'generated_at': datetime.now().isoformat(),
            'version': '1.0',
            'total_products': len(formatted_products),

            # Business Context
            'business': self.get_business_info(),

            # Products (main knowledge)
            'products': formatted_products,
            'products_by_category': products_by_type,
            'product_types': list(products_by_type.keys()),

            # Collections
            'collections': [
                {
                    'title': c.get('title', ''),
                    'handle': c.get('handle', ''),
                    'description': c.get('body_html', '')[:200] if c.get('body_html') else ''
                }
                for c in collections
            ],

            # Policies
            'shipping': self.get_shipping_info(),
            'returns': self.get_return_policy(),

            # FAQ
            'faq': self.get_faq(),

            # Voice Agent Instructions
            'agent_instructions': {
                'greeting': "Hello! Welcome to Alpha Medical Care. I'm your AI assistant. How can I help you today?",
                'fallback': "I'm not sure about that. Would you like me to connect you with our support team at support@alphamedical.shop?",
                'product_recommendation': "Based on what you've described, I'd recommend checking out our {product}. It's priced at {price} and {benefit}.",
                'order_help': "For order-related questions, I'll need your order number or the email address used for the order.",
                'closing': "Thank you for calling Alpha Medical Care! Have a great day and feel better soon!"
            }
        }

        # Save to cache
        try:
            with open(CACHE_FILE, 'w') as f:
                json.dump(knowledge_base, f, indent=2)
            print(f"✅ Knowledge base cached to {CACHE_FILE}")
        except Exception as e:
            print(f"⚠️ Cache write error: {e}")

        return knowledge_base

    def get_product_summary(self) -> str:
        """Get a text summary of products for voice agent context."""
        kb = self.build_knowledge_base()

        summary_lines = [
            f"Alpha Medical currently has {kb['total_products']} products across these categories:",
            ""
        ]

        for ptype, products in kb['products_by_category'].items():
            summary_lines.append(f"- {ptype}: {len(products)} products")
            # List top 3 products in each category
            for p in products[:3]:
                summary_lines.append(f"  • {p['title']} - {p['price_range']['formatted']}")

        return '\n'.join(summary_lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Alpha Medical Voice AI Knowledge Base Builder')
    parser.add_argument('--output', type=str, default=None, help='Output file path')
    parser.add_argument('--mode', type=str, choices=['build', 'refresh', 'summary'], default='build',
                        help='Operation mode')
    args = parser.parse_args()

    print("=" * 60)
    print("ALPHA MEDICAL - VOICE AI KNOWLEDGE BASE BUILDER")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Mode: {args.mode}")
    print(f"Shopify Store: {SHOPIFY_STORE_DOMAIN}")
    print("=" * 60)

    if not SHOPIFY_ADMIN_ACCESS_TOKEN:
        print("❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found in environment")
        print("   Add it to .env.admin file")
        sys.exit(1)

    builder = KnowledgeBaseBuilder()

    if args.mode == 'summary':
        summary = builder.get_product_summary()
        print("\n📊 PRODUCT SUMMARY FOR VOICE AGENT:\n")
        print(summary)
    else:
        force_refresh = args.mode == 'refresh'
        kb = builder.build_knowledge_base(force_refresh=force_refresh)

        print(f"\n📊 KNOWLEDGE BASE SUMMARY:")
        print(f"   Total Products: {kb['total_products']}")
        print(f"   Categories: {len(kb['product_types'])}")
        print(f"   Collections: {len(kb['collections'])}")
        print(f"   FAQ Items: {len(kb['faq'])}")

        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(kb, f, indent=2)
            print(f"\n✅ Knowledge base saved to: {output_path}")

        print("\n✅ Knowledge base ready for Voice Agent")


if __name__ == '__main__':
    main()
