#!/usr/bin/env python3
"""
Nano Banana (Gemini 2.5 Flash Image) Test Script
Alpha Medical AI Hybrid Production System

Tests image generation and editing capabilities using Google's Gemini API.
Reference: AI_HYBRID_PRODUCTION_SYSTEM_2025.md Section 3.2

Usage:
    python3 test_nano_banana.py --mode generate --prompt "Professional knee brace photo"
    python3 test_nano_banana.py --mode edit --image path/to/image.jpg --prompt "Remove background"
"""

import os
import sys
import argparse
import base64
from pathlib import Path
from datetime import datetime

# Load environment
from dotenv import load_dotenv
load_dotenv('.env.n8n')

GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')

def test_gemini_connection():
    """Test basic Gemini API connection."""
    import requests

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        models = response.json().get('models', [])
        image_models = [m['name'] for m in models if 'image' in m.get('name', '').lower() or 'flash' in m.get('name', '').lower()]
        print(f"✅ Gemini API Connected")
        print(f"   Available image-capable models: {len(image_models)}")
        for model in image_models[:5]:
            print(f"   - {model}")
        return True
    else:
        print(f"❌ Gemini API Error: {response.status_code}")
        print(f"   {response.text[:200]}")
        return False

def generate_image(prompt: str, output_path: str = None):
    """
    Generate image using Gemini 2.5 Flash (Nano Banana).

    Note: Gemini image generation is text-to-description, not text-to-image.
    For actual image generation, use Grok Aurora or Leonardo AI.
    This function tests the API response format.
    """
    import requests

    # Use gemini-2.0-flash-exp for image understanding
    # Note: Gemini generates image DESCRIPTIONS, not actual images
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [{
                "text": f"Describe in detail what an ideal product photo would look like for: {prompt}. Include lighting, background, angles, and style recommendations for e-commerce."
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1024
        }
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        result = response.json()
        text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        print(f"✅ Gemini Response Generated")
        print(f"\n--- IMAGE DESCRIPTION ---\n{text[:500]}...")
        return text
    else:
        print(f"❌ Generation Error: {response.status_code}")
        print(f"   {response.text[:300]}")
        return None

def edit_image_prompt(image_path: str, edit_prompt: str):
    """
    Generate editing instructions for an image using Gemini vision.

    Gemini can ANALYZE images and provide editing recommendations.
    Actual editing should be done via n8n workflow with proper image processing.
    """
    import requests

    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return None

    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Determine mime type
    ext = Path(image_path).suffix.lower()
    mime_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp'}
    mime_type = mime_map.get(ext, 'image/jpeg')

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [
                {"text": f"Analyze this product image and provide specific editing instructions to: {edit_prompt}. Be detailed about what needs to change."},
                {"inline_data": {"mime_type": mime_type, "data": image_data}}
            ]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024
        }
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        result = response.json()
        text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        print(f"✅ Image Analysis Complete")
        print(f"\n--- EDITING INSTRUCTIONS ---\n{text}")
        return text
    else:
        print(f"❌ Analysis Error: {response.status_code}")
        print(f"   {response.text[:300]}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Nano Banana (Gemini) Test Script')
    parser.add_argument('--mode', choices=['test', 'generate', 'edit'], default='test',
                        help='Operation mode: test connection, generate description, or edit image')
    parser.add_argument('--prompt', type=str, default='Medical knee brace on white background',
                        help='Prompt for generation or editing')
    parser.add_argument('--image', type=str, help='Path to image for edit mode')
    parser.add_argument('--output', type=str, help='Output path for results')

    args = parser.parse_args()

    print("=" * 60)
    print("NANO BANANA (GEMINI) TEST - Alpha Medical AI Production")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Mode: {args.mode}")
    print(f"API Key: {'✅ Found' if GEMINI_API_KEY else '❌ Missing'}")
    print("=" * 60)

    if not GEMINI_API_KEY:
        print("\n❌ GOOGLE_GEMINI_API_KEY not found in .env.n8n")
        print("   Please add your API key from https://aistudio.google.com/app/apikey")
        sys.exit(1)

    if args.mode == 'test':
        success = test_gemini_connection()
        sys.exit(0 if success else 1)

    elif args.mode == 'generate':
        result = generate_image(args.prompt, args.output)
        if result and args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"\n✅ Description saved to: {args.output}")

    elif args.mode == 'edit':
        if not args.image:
            print("❌ --image required for edit mode")
            sys.exit(1)
        result = edit_image_prompt(args.image, args.prompt)
        if result and args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"\n✅ Instructions saved to: {args.output}")

if __name__ == '__main__':
    main()
