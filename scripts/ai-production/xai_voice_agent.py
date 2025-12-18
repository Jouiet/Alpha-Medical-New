#!/usr/bin/env python3
"""
Alpha Medical Voice AI Agent - xAI + LiveKit Implementation
Session 109 - Production Voice Agent for Customer Support

This module implements a real-time voice agent using:
- xAI Realtime API (Grok) for conversational AI
- LiveKit for WebRTC voice transport
- Dynamic Knowledge Base for product information

Cost: ~$0.05/minute for voice calls

SETUP REQUIRED:
    1. pip install livekit-agents[xai] python-dotenv requests
    2. Set XAI_API_KEY in .env
    3. Set LIVEKIT_URL and LIVEKIT_API_* (or use local dev mode)
    4. Run: python3 xai_voice_agent.py

Usage:
    # Development mode (local testing)
    python3 xai_voice_agent.py dev

    # Production mode (requires LiveKit Cloud)
    python3 xai_voice_agent.py start

Reference: https://docs.livekit.io/agents/integrations/xai/
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Load environment
from dotenv import load_dotenv
load_dotenv('.env')
load_dotenv('.env.admin')

# Configuration
XAI_API_KEY = os.getenv('XAI_API_KEY')
LIVEKIT_URL = os.getenv('LIVEKIT_URL', '')
LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY', '')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET', '')

# Voice Options: Sal, Rex, Eve, Leo, Ara, Mika, Valentin
VOICE_SELECTION = 'Ara'  # Female, professional, clear

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class AlphaMedicalVoiceAgent:
    """
    Production voice agent for Alpha Medical customer support.

    Features:
    - Real-time voice conversation via xAI Realtime API
    - Dynamic product knowledge from Shopify
    - FAQ, shipping, return policy responses
    - Order status inquiry handling
    """

    def __init__(self):
        self.knowledge_base = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def load_knowledge_base(self) -> Dict:
        """Load knowledge base from builder."""
        try:
            from voice_knowledge_base import KnowledgeBaseBuilder
            builder = KnowledgeBaseBuilder()
            self.knowledge_base = builder.build_knowledge_base()
            logger.info(f"✅ Knowledge base loaded: {self.knowledge_base['total_products']} products")
            return self.knowledge_base
        except Exception as e:
            logger.error(f"❌ Failed to load knowledge base: {e}")
            # Return minimal fallback
            return {
                'business': {'name': 'Alpha Medical Care'},
                'products': [],
                'faq': []
            }

    def get_system_prompt(self) -> str:
        """Generate system prompt - DUAL PURPOSE: AI Shopping Assistant + Customer Support."""
        if not self.knowledge_base:
            self.load_knowledge_base()

        kb = self.knowledge_base
        business = kb.get('business', {})

        # Build detailed product context with prices
        product_details = []
        for ptype, products in kb.get('products_by_category', {}).items():
            product_info = []
            for p in products[:5]:  # Top 5 per category
                price = p.get('price_range', {}).get('formatted', 'Price varies')
                product_info.append(f"  - {p['title']} ({price})")
            product_details.append(f"**{ptype}** ({len(products)} products):\n" + "\n".join(product_info))

        # Build FAQ context
        faq_context = []
        for item in kb.get('faq', [])[:10]:
            faq_context.append(f"Q: {item['question']}\nA: {item['answer']}")

        shipping = kb.get('shipping', {})
        returns = kb.get('returns', {})

        system_prompt = f"""You are an expert AI Assistant for Alpha Medical Care - combining SHOPPING ASSISTANT and CUSTOMER SUPPORT. You help customers find products AND resolve issues.

## BUSINESS CONTEXT
- Company: {business.get('name', 'Alpha Medical Care')}
- Website: {business.get('domain', 'alphamedical.shop')}
- Tagline: "{business.get('tagline', 'Making Medical-Grade Recovery Accessible to Everyone')}"
- Quality: ISO 13485 certified suppliers, every product personally tested for 2 weeks
- Target: Seniors (arthritis), Office workers (posture), Athletes (recovery)

## YOUR DUAL ROLE

### 🛒 ROLE 1: AI SHOPPING ASSISTANT
Help customers find and purchase products:

1. **Needs Discovery** - Ask about their condition:
   - "What type of pain are you experiencing?"
   - "Where is the discomfort located?"
   - "Is this for yourself or someone else?"

2. **Product Matching** - Recommend based on needs:
   - Knee pain/arthritis → Knee braces, compression sleeves
   - Back pain/posture → Posture correctors, back supports
   - Neck pain → Cervical collars, neck traction devices
   - Athletes → Compression wear, joint supports
   - Recovery → Massage chairs, therapy devices

3. **Size Guidance** - Help with sizing:
   - Ask measurements when relevant
   - Recommend sizing up if between sizes

4. **Handle Objections**:
   - Quality: "ISO certified, personally tested 2 weeks"
   - Price: "Free shipping over $150, 30-day risk-free returns"
   - Value: Suggest bundles (save 15-25%)

5. **Cross-Sell** - Suggest complementary products:
   - "Many customers also get..."
   - Mention bundles for complete solutions

6. **Close the Sale**:
   - Direct to alphamedical.shop
   - Offer to email product links
   - Create urgency: "Free shipping if you order today"

### 🎧 ROLE 2: CUSTOMER SUPPORT
Help with orders and issues:

1. **Order Status** - Ask for order number/email
2. **Shipping** - Standard 7-15 days, Expedited 6-8 days
3. **Returns** - 30 days, unused, original packaging
4. **Issues** - Gather details, offer solutions
5. **Complaints** - Apologize, offer resolution, escalate if needed

## PRODUCT CATALOG ({kb.get('total_products', 0)} products)

{chr(10).join(product_details)}

## BUNDLES (Best Value)
- Chronic Pain Starter Kit - Multi-zone relief
- Office Worker Essential Kit - Posture + ergonomic
- Senior Mobility Support - Joint care package
- Active Athlete Complete Protection - Sports prevention
- Bundles save 15-25% vs buying separately

## POLICIES
**Shipping:**
- FREE over ${shipping.get('free_shipping_threshold', 150)}
- Standard: 7-15 days ($5.99 under $150)
- Expedited: 6-8 days ($12.99)
- USA only

**Returns:**
- 30 days from delivery
- Unused, original packaging
- Free exchanges for sizes
- Refund in 5-7 business days

**Payment:**
- Visa, Mastercard, Amex, Discover
- Apple Pay, Google Pay
- NO PayPal

## FAQ
{chr(10).join(faq_context[:5])}

## CONVERSATION FLOW

**Opening:**
"Hello! Welcome to Alpha Medical Care. I'm your AI assistant. Are you looking for a product recommendation, or do you need help with an existing order?"

**Shopping Flow:**
1. Discover needs (pain type, location, severity)
2. Recommend specific products with prices
3. Handle questions/objections
4. Suggest complementary products
5. Guide to purchase

**Support Flow:**
1. Get order number/email
2. Provide status/resolution
3. Escalate if needed

**Closing (Shopping):**
"I recommend the [Product] at [Price] - it's perfect for [their need]. Visit alphamedical.shop to order. Free shipping over $150!"

**Closing (Support):**
"Is there anything else I can help with? Thank you for choosing Alpha Medical!"

## VOICE STYLE
- Natural, conversational tone
- Concise (2-3 sentences)
- Say prices naturally ("forty-nine ninety-nine")
- Spell product names clearly
- Pause for responses
- Confirm understanding

## ESCALATION
"I want to make sure you get the best help. Our team at support@alphamedical.shop responds within 24 hours. Can I help with anything else?"

## KEY SELLING POINTS
- "ISO 13485 certified suppliers"
- "Every product tested 2 weeks"
- "Only 4.5-5 star rated suppliers"
- "30-day risk-free returns"
- "Free shipping over $150"

Start by greeting warmly and identifying if they need shopping help or support."""

        return system_prompt

    async def run_with_livekit(self):
        """Run voice agent with LiveKit (production mode)."""
        try:
            from livekit import agents
            from livekit.agents import AgentSession, Agent, RoomInputOptions
            from livekit.plugins import xai
        except ImportError:
            logger.error("❌ LiveKit agents not installed")
            logger.error("   Run: pip install 'livekit-agents[xai]'")
            return

        logger.info("🚀 Starting Alpha Medical Voice Agent with LiveKit...")

        # Load knowledge base
        self.load_knowledge_base()

        # Create agent session
        async def entrypoint(ctx: agents.JobContext):
            # Create the agent session with xAI Realtime
            session = AgentSession(
                llm=xai.realtime.RealtimeModel(
                    voice=VOICE_SELECTION,
                    temperature=0.7,
                    system=self.get_system_prompt(),
                ),
            )

            # Connect to room
            await session.start(
                room=ctx.room,
                participant=ctx.participant,
            )

            # Handle session events
            @session.on("user_speech_started")
            def on_speech_start():
                logger.info("🎤 User speaking...")

            @session.on("agent_speech_started")
            def on_agent_speech():
                logger.info("🔊 Agent responding...")

            logger.info(f"✅ Session started for participant: {ctx.participant.identity}")

        # Start the agent worker
        worker = agents.Worker(
            entrypoint,
            api_key=LIVEKIT_API_KEY,
            api_secret=LIVEKIT_API_SECRET,
            ws_url=LIVEKIT_URL,
        )

        await worker.run()

    async def run_console_demo(self):
        """
        Console demo mode - test the agent without LiveKit.
        Uses text input/output to simulate voice interaction.
        """
        logger.info("🎮 Starting Console Demo Mode (text-based)")
        logger.info("   Type your questions and press Enter")
        logger.info("   Type 'quit' to exit")
        print("-" * 60)

        # Load knowledge base
        self.load_knowledge_base()
        system_prompt = self.get_system_prompt()

        # Check if we can use xAI API directly
        if not XAI_API_KEY:
            logger.error("❌ XAI_API_KEY not set in environment")
            return

        import requests

        # xAI Chat API (non-realtime)
        XAI_CHAT_URL = "https://api.x.ai/v1/chat/completions"

        conversation = [
            {"role": "system", "content": system_prompt}
        ]

        # Opening greeting
        greeting = "Hello! Welcome to Alpha Medical Care. I'm your AI assistant. How can I help you today with our orthopedic and pain relief products?"
        print(f"\n🤖 Agent: {greeting}\n")

        while True:
            try:
                user_input = input("👤 You: ").strip()

                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🤖 Agent: Thank you for calling Alpha Medical Care! Have a great day and feel better soon!")
                    break

                if not user_input:
                    continue

                # Add user message to conversation
                conversation.append({"role": "user", "content": user_input})

                # Call xAI API
                response = requests.post(
                    XAI_CHAT_URL,
                    headers={
                        "Authorization": f"Bearer {XAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "grok-2-latest",
                        "messages": conversation,
                        "temperature": 0.7,
                        "max_tokens": 500
                    },
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    agent_response = result['choices'][0]['message']['content']
                    conversation.append({"role": "assistant", "content": agent_response})
                    print(f"\n🤖 Agent: {agent_response}\n")
                elif response.status_code == 403:
                    logger.error("❌ xAI API: No credits available")
                    logger.error("   Purchase credits at: https://console.x.ai")
                    print("\n🤖 Agent: I'm sorry, I'm having technical difficulties. Please try again later or contact support@alphamedical.shop\n")
                else:
                    logger.error(f"❌ xAI API Error: {response.status_code}")
                    logger.error(f"   {response.text[:200]}")
                    print("\n🤖 Agent: I apologize, but I'm experiencing an issue. Please contact support@alphamedical.shop for assistance.\n")

            except KeyboardInterrupt:
                print("\n\n🤖 Agent: Goodbye! Thank you for calling Alpha Medical Care!")
                break
            except Exception as e:
                logger.error(f"❌ Error: {e}")
                print("\n🤖 Agent: I apologize for the inconvenience. Please contact support@alphamedical.shop\n")


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    missing = []

    try:
        import requests
    except ImportError:
        missing.append('requests')

    try:
        from dotenv import load_dotenv
    except ImportError:
        missing.append('python-dotenv')

    # LiveKit is optional for demo mode
    try:
        from livekit import agents
    except ImportError:
        logger.warning("⚠️ LiveKit not installed (optional for demo mode)")
        logger.warning("   Install with: pip install 'livekit-agents[xai]'")

    if missing:
        logger.error(f"❌ Missing dependencies: {', '.join(missing)}")
        logger.error(f"   Run: pip install {' '.join(missing)}")
        return False

    return True


def main():
    print("=" * 60)
    print("ALPHA MEDICAL - xAI VOICE AGENT")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Voice: {VOICE_SELECTION}")
    print(f"xAI API Key: {'✅ Found' if XAI_API_KEY else '❌ Missing'}")
    print(f"LiveKit: {'✅ Configured' if LIVEKIT_URL else '⚠️ Not configured (demo mode only)'}")
    print("=" * 60)

    if not check_dependencies():
        sys.exit(1)

    if not XAI_API_KEY:
        logger.error("❌ XAI_API_KEY not found in environment")
        logger.error("   1. Get API key from https://console.x.ai")
        logger.error("   2. Add to .env: XAI_API_KEY=xai-xxxxx")
        logger.error("   3. Purchase credits at console.x.ai")
        sys.exit(1)

    agent = AlphaMedicalVoiceAgent()

    # Parse command line arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else 'demo'

    if mode == 'start' or mode == 'production':
        if not LIVEKIT_URL:
            logger.error("❌ LiveKit not configured for production mode")
            logger.error("   Set LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET")
            sys.exit(1)
        asyncio.run(agent.run_with_livekit())

    elif mode == 'demo' or mode == 'dev':
        # Console demo mode
        asyncio.run(agent.run_console_demo())

    elif mode == 'test':
        # Just test knowledge base loading
        kb = agent.load_knowledge_base()
        print("\n📊 Knowledge Base Test:")
        print(f"   Products: {kb.get('total_products', 0)}")
        print(f"   Categories: {len(kb.get('product_types', []))}")
        print(f"   FAQ: {len(kb.get('faq', []))}")
        print("\n✅ Voice Agent ready (knowledge base loaded)")

    else:
        print(f"Unknown mode: {mode}")
        print("Usage:")
        print("  python3 xai_voice_agent.py demo    # Console demo (text mode)")
        print("  python3 xai_voice_agent.py test    # Test knowledge base")
        print("  python3 xai_voice_agent.py start   # Production with LiveKit")


if __name__ == '__main__':
    main()
