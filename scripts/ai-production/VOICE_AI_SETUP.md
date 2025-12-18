# Alpha Medical Voice AI Setup Guide

> **Session 109** - xAI Voice Agent Infrastructure
> **Status:** ✅ IMPLEMENTED (Awaiting xAI Credits)
> **Cost:** ~$0.05/minute for voice calls

---

## 🎯 System Overview

Alpha Medical Voice AI is a **DUAL-PURPOSE** AI assistant that combines:

### 🛒 AI Shopping Assistant
- Discovers customer needs (pain type, location, severity)
- Recommends products with prices (85 products, 9 categories)
- Guides size selection
- Handles price objections
- Cross-sells complementary products
- Guides customers to purchase

### 🎧 Customer Support
- Order status inquiries
- Shipping information (7-15 days standard, 6-8 expedited)
- Returns & exchanges (30-day policy)
- Issue resolution
- Escalation to human support

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VOICE AI SYSTEM                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────┐     ┌─────────────┐     ┌──────────────┐ │
│   │   LiveKit   │────▶│   xAI API   │────▶│  Knowledge   │ │
│   │  (WebRTC)   │     │  (Realtime) │     │    Base      │ │
│   └─────────────┘     └─────────────┘     └──────────────┘ │
│         ▲                                        │         │
│         │                                        ▼         │
│   ┌─────────────┐                       ┌──────────────┐  │
│   │  Customer   │                       │   Shopify    │  │
│   │   Phone     │                       │    API       │  │
│   └─────────────┘                       └──────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

### 1. xAI API Access

1. Go to https://console.x.ai
2. Sign in with X (Twitter) account
3. Generate API key
4. **IMPORTANT:** Purchase credits ($10 minimum recommended)
5. Add to `.env`:
   ```
   XAI_API_KEY=xai-your-key-here
   ```

### 2. Python Dependencies

```bash
# Minimum (demo/test mode)
pip install python-dotenv requests

# Full voice support (production)
pip install 'livekit-agents[xai]~=1.3'
```

### 3. LiveKit (Production Only)

For production phone support, you need LiveKit Cloud:
1. Sign up at https://cloud.livekit.io
2. Create a project
3. Get credentials and add to `.env`:
   ```
   LIVEKIT_URL=wss://your-project.livekit.cloud
   LIVEKIT_API_KEY=your-api-key
   LIVEKIT_API_SECRET=your-api-secret
   ```

---

## 🚀 Quick Start

### Test Knowledge Base (No xAI credits needed)

```bash
# View product summary
python3 scripts/ai-production/voice_knowledge_base.py --mode summary

# Build fresh knowledge base
python3 scripts/ai-production/voice_knowledge_base.py --mode refresh

# Export to file
python3 scripts/ai-production/voice_knowledge_base.py --output kb.json
```

### Test Voice Agent (Requires xAI credits)

```bash
# Test knowledge base loading
python3 scripts/ai-production/xai_voice_agent.py test

# Console demo (text mode - simulates voice)
python3 scripts/ai-production/xai_voice_agent.py demo

# Production mode (requires LiveKit)
python3 scripts/ai-production/xai_voice_agent.py start
```

---

## 💰 Cost Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| xAI Realtime API | ~$0.05/min | Voice conversations |
| xAI Chat API | ~$0.001/query | Console demo fallback |
| LiveKit Cloud | Free tier available | 5000 min/month free |
| Shopify API | $0 | Included with store |

### Monthly Cost Estimate

| Usage | Voice Minutes | Cost |
|-------|---------------|------|
| Light | 100 min | ~$5 |
| Medium | 500 min | ~$25 |
| Heavy | 2000 min | ~$100 |

**Comparison:** Tidio AI ($29/mo) does NOT include voice, CHAT only.

---

## 📚 Knowledge Base

The knowledge base auto-syncs with Shopify:

### Product Data
- 85 products across 9 categories
- Prices, descriptions, variants, stock status
- Auto-updates on each call (1-hour cache)

### Business Info
- Company details (Alpha Medical Care)
- Contact info (support@alphamedical.shop)
- Target customers (seniors, office workers, athletes)

### Policies
- Shipping: 7-15 days standard, 6-8 days expedited
- Free shipping over $150
- 30-day returns

### FAQ
- 10 common questions pre-loaded
- Order tracking, payment methods, sizing, etc.

---

## 🔧 Customization

### Change Voice

Edit `xai_voice_agent.py`:
```python
VOICE_SELECTION = 'Ara'  # Options: Sal, Rex, Eve, Leo, Ara, Mika, Valentin
```

### Add FAQ

Edit `voice_knowledge_base.py` `get_faq()` method:
```python
def get_faq(self) -> List[Dict]:
    return [
        {
            'question': 'Your new question?',
            'answer': 'Your answer here.'
        },
        # ... existing FAQ
    ]
```

### Modify System Prompt

Edit `xai_voice_agent.py` `get_system_prompt()` method to change agent behavior.

---

## 🧪 Testing Checklist

- [x] Knowledge base fetches all 85 products
- [x] Knowledge base includes 9 categories
- [x] Knowledge base caches properly (1 hour)
- [ ] xAI API accepts calls (requires credits)
- [ ] Console demo works (text mode)
- [ ] LiveKit integration (production)

---

## 📞 Phone Integration (Future)

To add phone number support:

1. Get a phone number from Twilio or similar
2. Connect to LiveKit via SIP trunk
3. Route calls to voice agent

Or use LiveKit's built-in phone integration:
- https://docs.livekit.io/agents/telephony/

---

## 🚨 Troubleshooting

### "403 - No credits"
- Go to https://console.x.ai
- Purchase credits ($10 minimum)

### "SHOPIFY_ADMIN_ACCESS_TOKEN not found"
- Run from project root: `python3 scripts/ai-production/...`
- Or set full path in script

### "LiveKit not installed"
- Install: `pip install 'livekit-agents[xai]~=1.3'`
- This is optional for demo mode

---

## 📊 Files Created

| File | Purpose |
|------|---------|
| `voice_knowledge_base.py` | Dynamic Shopify product sync |
| `xai_voice_agent.py` | xAI + LiveKit voice agent |
| `requirements_voice.txt` | Python dependencies |
| `cache/knowledge_base_cache.json` | Cached product data |
| `VOICE_AI_SETUP.md` | This documentation |

---

**Created:** Session 109 (2025-12-18)
**Author:** Claude Opus 4.5
**Status:** Ready for xAI credits purchase
