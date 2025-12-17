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
        """Generate system prompt with dynamic product knowledge."""
        if not self.knowledge_base:
            self.load_knowledge_base()

        kb = self.knowledge_base
        business = kb.get('business', {})

        # Build product context
        product_summary = []
        for ptype, products in kb.get('products_by_category', {}).items():
            product_names = [p['title'] for p in products[:5]]  # Top 5 per category
            product_summary.append(f"- {ptype}: {', '.join(product_names)}")

        # Build FAQ context
        faq_context = []
        for item in kb.get('faq', [])[:10]:
            faq_context.append(f"Q: {item['question']}\nA: {item['answer']}")

        shipping = kb.get('shipping', {})
        returns = kb.get('returns', {})

        system_prompt = f"""You are a friendly and helpful voice assistant for Alpha Medical Care, a medical equipment retailer specializing in orthopedic support and pain relief products.

## BUSINESS CONTEXT
- Company: {business.get('name', 'Alpha Medical Care')}
- Website: {business.get('domain', 'alphamedical.shop')}
- Tagline: "{business.get('tagline', 'Making Medical-Grade Recovery Accessible to Everyone')}"
- Target Customers: Seniors with arthritis, office workers with posture issues, athletes needing recovery support

## YOUR ROLE
You are the first point of contact for customers calling Alpha Medical. Your goals:
1. Answer product questions helpfully and accurately
2. Provide shipping and return policy information
3. Help with order inquiries (ask for order number)
4. Recommend products based on customer needs
5. Escalate to human support when needed (support@alphamedical.shop)

## PRODUCT CATALOG ({kb.get('total_products', 0)} products available)
{chr(10).join(product_summary)}

## SHIPPING POLICY
- Standard Shipping: {shipping.get('standard_shipping', {}).get('time', '7-15 days')} - {shipping.get('standard_shipping', {}).get('cost', 'Free over $150')}
- Expedited Shipping: {shipping.get('expedited_shipping', {}).get('time', '6-8 days')} - {shipping.get('expedited_shipping', {}).get('cost', '$12.99')}
- Processing Time: {shipping.get('processing_time', '1-2 business days')}
- Free Shipping: Orders over ${shipping.get('free_shipping_threshold', 150)}

## RETURN POLICY
- Return Window: {returns.get('return_window', '30 days')}
- Condition: {returns.get('condition', 'Unused, original packaging')}
- Refund: {returns.get('refund_method', '5-7 business days to original payment')}

## COMMON FAQ
{chr(10).join(faq_context[:5])}

## VOICE GUIDELINES
- Speak naturally and conversationally
- Keep responses concise (2-3 sentences when possible)
- Use prices in dollars (say "twenty-nine ninety-nine" not "29.99")
- Spell out product names clearly
- Confirm customer understanding before moving on
- If unsure, offer to email information to customer

## ESCALATION
If customer asks something you cannot help with, say:
"I'd be happy to connect you with our support team. They can be reached at support@alphamedical.shop and respond within 24 hours. Is there anything else I can help you with?"

Begin by greeting the customer warmly."""

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
