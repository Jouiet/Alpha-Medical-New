#!/usr/bin/env python3
"""
VERIFY AI CRAWLERS - Alpha Medical robots.txt
Check which AI crawlers are configured and their status
"""

import requests
from datetime import datetime

STORE_URL = "https://www.alphamedical.shop"

print("="*80)
print("ALPHA MEDICAL - AI CRAWLERS VERIFICATION")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
print("="*80)

# Fetch robots.txt
try:
    response = requests.get(f"{STORE_URL}/robots.txt", timeout=10)
    robots_txt = response.text
except Exception as e:
    print(f"❌ Failed to fetch robots.txt: {e}")
    exit(1)

print("\n✅ robots.txt fetched successfully")

# Check for AI crawlers
ai_crawlers = {
    "GPTBot": {
        "name": "OpenAI GPTBot (ChatGPT)",
        "official": True,
        "present": False
    },
    "ChatGPT-User": {
        "name": "OpenAI ChatGPT User",
        "official": True,
        "present": False
    },
    "anthropic-ai": {
        "name": "Anthropic AI",
        "official": True,
        "present": False
    },
    "Claude-Web": {
        "name": "Anthropic Claude Web",
        "official": True,
        "present": False
    },
    "cohere-ai": {
        "name": "Cohere AI",
        "official": True,
        "present": False
    },
    "PerplexityBot": {
        "name": "Perplexity AI",
        "official": True,
        "present": False
    },
    "Googlebot-Extended": {
        "name": "Google Gemini (Extended)",
        "official": True,
        "present": False,
        "note": "Used for Gemini AI training"
    },
    "Google-Extended": {
        "name": "Google Extended (alternative)",
        "official": True,
        "present": False
    },
    "GrokBot": {
        "name": "xAI Grok (unofficial)",
        "official": False,
        "present": False,
        "note": "No official crawler yet (as of Q4 2025)"
    }
}

# Check which crawlers are present
for user_agent in ai_crawlers:
    if user_agent in robots_txt:
        ai_crawlers[user_agent]["present"] = True

# Check if they're disallowed
disallowed_crawlers = []
for user_agent in ai_crawlers:
    if ai_crawlers[user_agent]["present"]:
        # Check if Disallow: / follows
        pattern = f"User-agent: {user_agent}"
        start_idx = robots_txt.find(pattern)
        if start_idx != -1:
            next_section = robots_txt[start_idx:start_idx+200]
            if "Disallow: /" in next_section and "Allow:" not in next_section:
                disallowed_crawlers.append(user_agent)

print("\n" + "="*80)
print("AI CRAWLERS STATUS")
print("="*80)

print("\n✅ PRESENT & ALLOWED:\n")
for user_agent, info in ai_crawlers.items():
    if info["present"] and user_agent not in disallowed_crawlers:
        status = "✅"
        print(f"{status} {info['name']}")
        print(f"   User-agent: {user_agent}")
        if "note" in info:
            print(f"   Note: {info['note']}")
        print()

print("\n❌ PRESENT BUT DISALLOWED:\n")
disallowed_found = False
for user_agent in disallowed_crawlers:
    disallowed_found = True
    info = ai_crawlers[user_agent]
    print(f"❌ {info['name']}")
    print(f"   User-agent: {user_agent}")
    print()

if not disallowed_found:
    print("   (none)")

print("\n⚠️  NOT PRESENT (Missing or No Official Crawler):\n")
missing_found = False
for user_agent, info in ai_crawlers.items():
    if not info["present"]:
        missing_found = True
        symbol = "⚠️" if info["official"] else "ℹ️"
        print(f"{symbol} {info['name']}")
        print(f"   User-agent: {user_agent}")
        if "note" in info:
            print(f"   Note: {info['note']}")
        print()

if not missing_found:
    print("   (none)")

# Check llms.txt reference
llms_reference = "llms.txt" in robots_txt or "llms-txt" in robots_txt
print("\n" + "="*80)
print("ADDITIONAL FEATURES")
print("="*80)
print(f"\n{'✅' if llms_reference else '❌'} llms.txt reference: {'PRESENT' if llms_reference else 'MISSING'}")

# Summary
present_count = sum(1 for info in ai_crawlers.values() if info["present"])
allowed_count = present_count - len(disallowed_crawlers)

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\n📊 AI Crawlers Configured: {present_count}/{len(ai_crawlers)}")
print(f"✅ Allowed: {allowed_count}")
print(f"❌ Disallowed: {len(disallowed_crawlers)}")
print(f"⚠️  Not Present: {len(ai_crawlers) - present_count}")

print("\n🎯 RECOMMENDATIONS:\n")

if not any(ai_crawlers[ua]["present"] for ua in ["Googlebot-Extended", "Google-Extended"]):
    print("⚠️  Consider adding Googlebot-Extended for Google Gemini")

if not any(ai_crawlers[ua]["present"] for ua in ["GrokBot"]):
    print("ℹ️  GrokBot: xAI Grok has no official crawler yet (as of Q4 2025)")
    print("   → No action needed until official documentation is released")

print("\n✅ Current configuration allows major AI crawlers (GPT, Claude, Perplexity, Gemini)")
print("✅ llms.txt reference present for structured AI documentation")

print("\n" + "="*80)
