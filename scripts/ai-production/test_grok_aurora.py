#!/usr/bin/env python3
"""
Grok Aurora (xAI) Image Generation Test Script
Alpha Medical AI Hybrid Production System

Tests image generation using xAI's Grok Aurora model.
Reference: AI_HYBRID_PRODUCTION_SYSTEM_2025.md Section 3.3

SETUP REQUIRED:
    1. Get API key from https://x.ai/api or https://console.x.ai
    2. Add to .env: XAI_API_KEY=xai-xxxxxxxxxxxxx
    3. Run: python3 test_grok_aurora.py --mode test

Usage:
    python3 test_grok_aurora.py --mode test
    python3 test_grok_aurora.py --mode generate --prompt "Medical knee brace" --count 4
    python3 test_grok_aurora.py --mode batch --prompts prompts.txt --output ./output/
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Load environment
from dotenv import load_dotenv
load_dotenv('.env')
load_dotenv('.env.admin')

XAI_API_KEY = os.getenv('XAI_API_KEY')
XAI_BASE_URL = "https://api.x.ai/v1"

def test_connection() -> bool:
    """Test xAI API connection."""
    if not XAI_API_KEY:
        print("❌ XAI_API_KEY not found in environment")
        print("\n   SETUP INSTRUCTIONS:")
        print("   1. Go to https://console.x.ai or https://x.ai/api")
        print("   2. Create account / sign in with X (Twitter)")
        print("   3. Generate API key")
        print("   4. Add to .env file: XAI_API_KEY=xai-xxxxxxxxxxxxx")
        return False

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Test with models endpoint
    try:
        response = requests.get(f"{XAI_BASE_URL}/models", headers=headers, timeout=10)
        if response.status_code == 200:
            models = response.json().get('data', [])
            print(f"✅ xAI API Connected")
            print(f"   Available models: {len(models)}")
            for m in models:
                print(f"   - {m.get('id', 'unknown')}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def generate_images(prompt: str, count: int = 1, output_dir: str = None) -> List[str]:
    """
    Generate images using Grok Aurora.

    Args:
        prompt: Text description of desired image
        count: Number of images to generate (1-10)
        output_dir: Directory to save images (optional)

    Returns:
        List of image URLs or file paths
    """
    if not XAI_API_KEY:
        print("❌ XAI_API_KEY required")
        return []

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Grok image generation endpoint
    payload = {
        "model": "grok-2-image",  # Aurora model
        "prompt": prompt,
        "n": min(count, 10),  # Max 10 per request
        "response_format": "url"  # or "b64_json"
    }

    print(f"📸 Generating {count} image(s)...")
    print(f"   Prompt: {prompt[:80]}...")

    try:
        response = requests.post(
            f"{XAI_BASE_URL}/images/generations",
            headers=headers,
            json=payload,
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            images = result.get('data', [])
            urls = [img.get('url') for img in images if img.get('url')]

            print(f"✅ Generated {len(urls)} image(s)")

            # Save images if output_dir specified
            if output_dir and urls:
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)

                saved_paths = []
                for i, url in enumerate(urls):
                    try:
                        img_response = requests.get(url, timeout=30)
                        if img_response.status_code == 200:
                            filename = f"grok_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
                            filepath = output_path / filename
                            with open(filepath, 'wb') as f:
                                f.write(img_response.content)
                            saved_paths.append(str(filepath))
                            print(f"   💾 Saved: {filepath}")
                    except Exception as e:
                        print(f"   ⚠️ Failed to save image {i}: {e}")

                return saved_paths if saved_paths else urls

            return urls

        else:
            print(f"❌ Generation Error: {response.status_code}")
            print(f"   {response.text[:300]}")
            return []

    except Exception as e:
        print(f"❌ Request Error: {e}")
        return []

def batch_generate(prompts_file: str, output_dir: str, images_per_prompt: int = 2) -> dict:
    """
    Batch generate images from a file of prompts.

    Args:
        prompts_file: Path to file with one prompt per line
        output_dir: Directory to save all images
        images_per_prompt: Number of images per prompt

    Returns:
        Dict mapping prompts to generated image paths
    """
    if not os.path.exists(prompts_file):
        print(f"❌ Prompts file not found: {prompts_file}")
        return {}

    with open(prompts_file, 'r') as f:
        prompts = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    print(f"📋 Processing {len(prompts)} prompts")
    print(f"   Images per prompt: {images_per_prompt}")
    print(f"   Total images: {len(prompts) * images_per_prompt}")
    print(f"   Output: {output_dir}")
    print("=" * 60)

    results = {}
    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] {prompt[:50]}...")
        images = generate_images(prompt, images_per_prompt, output_dir)
        results[prompt] = images

        # Respect rate limits (5 requests per second max)
        if i < len(prompts):
            import time
            time.sleep(0.3)

    # Save results manifest
    manifest_path = Path(output_dir) / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Manifest saved: {manifest_path}")

    return results

def main():
    parser = argparse.ArgumentParser(description='Grok Aurora Image Generation Test')
    parser.add_argument('--mode', choices=['test', 'generate', 'batch'], default='test',
                        help='Operation mode')
    parser.add_argument('--prompt', type=str, default='Professional product photo of medical knee brace, white background, studio lighting',
                        help='Prompt for image generation')
    parser.add_argument('--count', type=int, default=1, help='Number of images (1-10)')
    parser.add_argument('--prompts', type=str, help='Path to prompts file for batch mode')
    parser.add_argument('--output', type=str, default='./output/grok', help='Output directory')

    args = parser.parse_args()

    print("=" * 60)
    print("GROK AURORA TEST - Alpha Medical AI Production")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Mode: {args.mode}")
    print(f"API Key: {'✅ Found' if XAI_API_KEY else '❌ Missing (see setup instructions)'}")
    print("=" * 60)

    if args.mode == 'test':
        success = test_connection()
        sys.exit(0 if success else 1)

    elif args.mode == 'generate':
        if not XAI_API_KEY:
            print("\n❌ XAI_API_KEY required for generation")
            print("   Add to .env: XAI_API_KEY=xai-xxxxxxxxxxxxx")
            sys.exit(1)
        results = generate_images(args.prompt, args.count, args.output)
        print(f"\n📊 Results: {len(results)} images")
        for r in results:
            print(f"   - {r}")

    elif args.mode == 'batch':
        if not args.prompts:
            print("❌ --prompts file required for batch mode")
            sys.exit(1)
        results = batch_generate(args.prompts, args.output)
        total = sum(len(v) for v in results.values())
        print(f"\n📊 Batch Complete: {total} images from {len(results)} prompts")

if __name__ == '__main__':
    main()
