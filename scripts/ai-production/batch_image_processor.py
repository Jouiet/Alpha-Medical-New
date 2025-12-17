#!/usr/bin/env python3
"""
Batch Image Processor - Alpha Medical AI Hybrid Production System
Reference: AI_HYBRID_PRODUCTION_SYSTEM_2025.md Section 7.2

Processes multiple product images through AI enhancement pipeline.
Supports both Nano Banana (Gemini) for editing and Grok Aurora for generation.

SETUP:
    1. Add GOOGLE_GEMINI_API_KEY to .env.n8n
    2. Add XAI_API_KEY to .env (optional, for Grok generation)
    3. Run: python3 batch_image_processor.py --mode edit --input ./input/ --output ./output/

Usage:
    # Edit existing images (Nano Banana/Gemini)
    python3 batch_image_processor.py --mode edit --input ./input/ --output ./output/

    # Generate new images from prompts file (Grok Aurora)
    python3 batch_image_processor.py --mode generate --prompts prompts.txt --output ./output/

    # Hybrid: Edit some, generate others
    python3 batch_image_processor.py --mode hybrid --input ./input/ --prompts prompts.txt --output ./output/
"""

import os
import sys
import json
import argparse
import base64
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

# Load environment
from dotenv import load_dotenv
load_dotenv('.env')
load_dotenv('.env.n8n')
load_dotenv('.env.admin')

# API Keys
GEMINI_API_KEY = os.getenv('GOOGLE_GEMINI_API_KEY')
XAI_API_KEY = os.getenv('XAI_API_KEY')

# API Endpoints
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
XAI_BASE_URL = "https://api.x.ai/v1"

# Processing Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests

@dataclass
class ProcessingResult:
    """Result of processing a single item."""
    input_path: str
    output_path: Optional[str]
    status: str  # success, error, skipped
    tool_used: str  # gemini, grok, none
    processing_time: float
    error_message: Optional[str] = None
    prompt_used: Optional[str] = None

@dataclass
class BatchReport:
    """Summary report for batch processing."""
    total_items: int
    successful: int
    failed: int
    skipped: int
    total_time: float
    results: List[ProcessingResult]
    timestamp: str

# ============================================================================
# PROMPT TEMPLATES (Reference: prompts/templates/base-templates.md)
# ============================================================================

PRODUCT_ENHANCEMENT_PROMPT = """Transform this product photo into a professional e-commerce image:

REQUIREMENTS:
- Clean white background (#ffffff)
- Soft studio lighting with minimal shadows
- Product centered with proper composition
- High detail preservation on product features
- Remove any imperfections, dust, or blemishes
- Maintain accurate product colors
- E-commerce ready quality

STYLE:
- Professional product photography aesthetic
- Medical equipment premium quality appearance
- Sharp focus on product details
- Consistent with Alpha Medical brand standards

OUTPUT: High-quality product photo suitable for Shopify listing."""

LIFESTYLE_ENHANCEMENT_PROMPT = """Enhance this lifestyle product photo:

REQUIREMENTS:
- Natural, warm lighting
- Authentic lifestyle context
- Product clearly visible but naturally integrated
- Approachable, relatable mood
- Suitable for social media and marketing

STYLE:
- Authentic user-generated content aesthetic
- Empowering, positive mood
- Alpha Medical brand colors (#4770db, #0e1b4d, #eff0f5) where applicable

OUTPUT: Enhanced lifestyle photo for marketing use."""

AD_CREATIVE_PROMPT_TEMPLATE = """Generate a professional product advertisement image:

PRODUCT: {product_name}
TARGET: {target_persona}
PLATFORM: {platform}

REQUIREMENTS:
- {product_description}
- Clean, professional composition
- Space for text overlay ({text_position})
- {dimensions} dimensions
- Marketing-ready quality

STYLE:
- Professional advertising aesthetic
- Trustworthy medical equipment appearance
- Brand colors: Primary Blue #4770db, Navy #0e1b4d

NEGATIVE: blurry, low quality, text in image, watermarks, cluttered background"""

# ============================================================================
# NANO BANANA (GEMINI) FUNCTIONS
# ============================================================================

def enhance_image_gemini(image_path: str, prompt: str = None, output_path: str = None) -> Tuple[bool, str, str]:
    """
    Enhance an image using Gemini 2.5 Flash.

    Args:
        image_path: Path to input image
        prompt: Custom prompt (uses default if None)
        output_path: Path to save result (auto-generated if None)

    Returns:
        Tuple of (success, output_path_or_error, prompt_used)
    """
    if not GEMINI_API_KEY:
        return False, "GOOGLE_GEMINI_API_KEY not configured", ""

    if not os.path.exists(image_path):
        return False, f"Image not found: {image_path}", ""

    # Use default prompt if none provided
    if prompt is None:
        prompt = PRODUCT_ENHANCEMENT_PROMPT

    # Read and encode image
    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    # Determine mime type
    ext = Path(image_path).suffix.lower()
    mime_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp'}
    mime_type = mime_map.get(ext, 'image/jpeg')

    # Use Gemini 2.0 Flash with image generation capability
    url = f"{GEMINI_BASE_URL}/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [
                {"text": f"Edit this image according to these instructions: {prompt}"},
                {"inline_data": {"mime_type": mime_type, "data": image_data}}
            ]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": 2048
        }
    }

    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(url, json=payload, timeout=120)

            if response.status_code == 200:
                result = response.json()

                # Check for generated image in response
                candidates = result.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    for part in parts:
                        if 'inlineData' in part:
                            # Save generated image
                            if output_path is None:
                                stem = Path(image_path).stem
                                output_path = str(Path(image_path).parent / f"{stem}_enhanced.png")

                            img_data = base64.b64decode(part['inlineData']['data'])
                            with open(output_path, 'wb') as f:
                                f.write(img_data)
                            return True, output_path, prompt

                        elif 'text' in part:
                            # Gemini returned text (description) instead of image
                            # This is expected for non-generation models
                            text_response = part['text']

                            # For editing, we need Imagen or specific edit models
                            # Return the analysis for now
                            return False, f"Model returned text analysis (editing requires different approach): {text_response[:200]}...", prompt

                return False, "No output generated", prompt

            elif response.status_code == 429:
                # Rate limited, wait and retry
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            else:
                return False, f"API Error {response.status_code}: {response.text[:200]}", prompt

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return False, f"Request failed: {str(e)}", prompt

    return False, "Max retries exceeded", prompt

def analyze_image_gemini(image_path: str) -> Tuple[bool, str]:
    """
    Analyze an image using Gemini for quality assessment.

    Args:
        image_path: Path to image

    Returns:
        Tuple of (success, analysis_or_error)
    """
    if not GEMINI_API_KEY:
        return False, "GOOGLE_GEMINI_API_KEY not configured"

    if not os.path.exists(image_path):
        return False, f"Image not found: {image_path}"

    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    ext = Path(image_path).suffix.lower()
    mime_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp'}
    mime_type = mime_map.get(ext, 'image/jpeg')

    url = f"{GEMINI_BASE_URL}/models/gemini-2.0-flash-exp:generateContent?key={GEMINI_API_KEY}"

    payload = {
        "contents": [{
            "parts": [
                {"text": """Analyze this product photo for e-commerce readiness:

1. QUALITY ASSESSMENT (1-10):
   - Lighting quality
   - Background cleanliness
   - Product visibility
   - Color accuracy
   - Overall professional appearance

2. ISSUES IDENTIFIED:
   - List specific problems to fix

3. ENHANCEMENT RECOMMENDATIONS:
   - Prioritized list of improvements

4. E-COMMERCE READINESS: YES/NO with reason"""},
                {"inline_data": {"mime_type": mime_type, "data": image_data}}
            ]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            result = response.json()
            text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            return True, text
        else:
            return False, f"API Error {response.status_code}: {response.text[:200]}"
    except Exception as e:
        return False, f"Request failed: {str(e)}"

# ============================================================================
# GROK AURORA FUNCTIONS
# ============================================================================

def generate_image_grok(prompt: str, output_path: str = None, count: int = 1) -> Tuple[bool, List[str], str]:
    """
    Generate images using Grok Aurora.

    Args:
        prompt: Text description for image generation
        output_path: Directory to save results
        count: Number of images to generate (1-10)

    Returns:
        Tuple of (success, list_of_paths_or_errors, prompt_used)
    """
    if not XAI_API_KEY:
        return False, ["XAI_API_KEY not configured. Add to .env: XAI_API_KEY=xai-xxxxxxxxxxxxx"], prompt

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-image",
        "prompt": prompt,
        "n": min(count, 10),
        "response_format": "url"
    }

    for attempt in range(MAX_RETRIES):
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

                if not urls:
                    return False, ["No images generated"], prompt

                # Download and save images
                saved_paths = []
                if output_path:
                    output_dir = Path(output_path)
                    output_dir.mkdir(parents=True, exist_ok=True)

                    for i, url in enumerate(urls):
                        try:
                            img_response = requests.get(url, timeout=30)
                            if img_response.status_code == 200:
                                filename = f"grok_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i}.png"
                                filepath = output_dir / filename
                                with open(filepath, 'wb') as f:
                                    f.write(img_response.content)
                                saved_paths.append(str(filepath))
                        except Exception as e:
                            saved_paths.append(f"Error saving: {e}")

                    return True, saved_paths if saved_paths else urls, prompt

                return True, urls, prompt

            elif response.status_code == 429:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            else:
                return False, [f"API Error {response.status_code}: {response.text[:200]}"], prompt

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            return False, [f"Request failed: {str(e)}"], prompt

    return False, ["Max retries exceeded"], prompt

# ============================================================================
# BATCH PROCESSING FUNCTIONS
# ============================================================================

def process_batch_edit(input_dir: str, output_dir: str, prompt: str = None) -> BatchReport:
    """
    Batch process images for editing using Gemini.

    Args:
        input_dir: Directory containing source images
        output_dir: Directory to save enhanced images
        prompt: Custom prompt for all images (uses default if None)

    Returns:
        BatchReport with processing results
    """
    start_time = time.time()
    results = []

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Find all image files
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    images = [f for f in input_path.iterdir() if f.suffix.lower() in image_extensions]

    print(f"📁 Found {len(images)} images in {input_dir}")
    print(f"📤 Output directory: {output_dir}")
    print("=" * 60)

    for i, img_file in enumerate(images, 1):
        print(f"\n[{i}/{len(images)}] Processing: {img_file.name}")
        item_start = time.time()

        output_file = output_path / f"{img_file.stem}_enhanced{img_file.suffix}"

        success, result, prompt_used = enhance_image_gemini(
            str(img_file),
            prompt,
            str(output_file)
        )

        processing_time = time.time() - item_start

        if success:
            print(f"   ✅ Success: {output_file.name} ({processing_time:.1f}s)")
            results.append(ProcessingResult(
                input_path=str(img_file),
                output_path=str(output_file),
                status="success",
                tool_used="gemini",
                processing_time=processing_time,
                prompt_used=prompt_used[:100] + "..." if len(prompt_used) > 100 else prompt_used
            ))
        else:
            print(f"   ❌ Error: {result[:100]}...")
            results.append(ProcessingResult(
                input_path=str(img_file),
                output_path=None,
                status="error",
                tool_used="gemini",
                processing_time=processing_time,
                error_message=result,
                prompt_used=prompt_used[:100] + "..." if prompt_used and len(prompt_used) > 100 else prompt_used
            ))

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

    total_time = time.time() - start_time
    successful = len([r for r in results if r.status == "success"])
    failed = len([r for r in results if r.status == "error"])
    skipped = len([r for r in results if r.status == "skipped"])

    report = BatchReport(
        total_items=len(images),
        successful=successful,
        failed=failed,
        skipped=skipped,
        total_time=total_time,
        results=results,
        timestamp=datetime.now().isoformat()
    )

    return report

def process_batch_generate(prompts_file: str, output_dir: str, images_per_prompt: int = 2) -> BatchReport:
    """
    Batch generate images from a prompts file using Grok Aurora.

    Args:
        prompts_file: Path to file with one prompt per line
        output_dir: Directory to save generated images
        images_per_prompt: Number of images per prompt

    Returns:
        BatchReport with processing results
    """
    start_time = time.time()
    results = []

    if not os.path.exists(prompts_file):
        return BatchReport(
            total_items=0,
            successful=0,
            failed=1,
            skipped=0,
            total_time=0,
            results=[ProcessingResult(
                input_path=prompts_file,
                output_path=None,
                status="error",
                tool_used="none",
                processing_time=0,
                error_message=f"Prompts file not found: {prompts_file}"
            )],
            timestamp=datetime.now().isoformat()
        )

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Read prompts
    with open(prompts_file, 'r') as f:
        prompts = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    print(f"📋 Found {len(prompts)} prompts in {prompts_file}")
    print(f"📤 Output directory: {output_dir}")
    print(f"🖼️ Images per prompt: {images_per_prompt}")
    print("=" * 60)

    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/{len(prompts)}] {prompt[:50]}...")
        item_start = time.time()

        success, paths_or_errors, prompt_used = generate_image_grok(
            prompt,
            str(output_path),
            images_per_prompt
        )

        processing_time = time.time() - item_start

        if success:
            print(f"   ✅ Generated {len(paths_or_errors)} images ({processing_time:.1f}s)")
            for path in paths_or_errors:
                results.append(ProcessingResult(
                    input_path=prompt[:100],
                    output_path=path,
                    status="success",
                    tool_used="grok",
                    processing_time=processing_time / len(paths_or_errors),
                    prompt_used=prompt_used[:100] + "..." if len(prompt_used) > 100 else prompt_used
                ))
        else:
            print(f"   ❌ Error: {paths_or_errors[0][:100]}...")
            results.append(ProcessingResult(
                input_path=prompt[:100],
                output_path=None,
                status="error",
                tool_used="grok",
                processing_time=processing_time,
                error_message=paths_or_errors[0],
                prompt_used=prompt_used[:100] + "..." if len(prompt_used) > 100 else prompt_used
            ))

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

    total_time = time.time() - start_time
    successful = len([r for r in results if r.status == "success"])
    failed = len([r for r in results if r.status == "error"])

    report = BatchReport(
        total_items=len(prompts),
        successful=successful,
        failed=failed,
        skipped=0,
        total_time=total_time,
        results=results,
        timestamp=datetime.now().isoformat()
    )

    return report

def save_report(report: BatchReport, output_path: str):
    """Save batch processing report to JSON file."""
    report_file = Path(output_path) / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Convert to dict for JSON serialization
    report_dict = {
        "summary": {
            "total_items": report.total_items,
            "successful": report.successful,
            "failed": report.failed,
            "skipped": report.skipped,
            "total_time_seconds": round(report.total_time, 2),
            "timestamp": report.timestamp
        },
        "results": [asdict(r) for r in report.results]
    }

    with open(report_file, 'w') as f:
        json.dump(report_dict, f, indent=2)

    print(f"\n📊 Report saved: {report_file}")
    return report_file

def print_summary(report: BatchReport):
    """Print formatted summary of batch processing."""
    print("\n" + "=" * 60)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total Items:     {report.total_items}")
    print(f"Successful:      {report.successful} ✅")
    print(f"Failed:          {report.failed} ❌")
    print(f"Skipped:         {report.skipped} ⏭️")
    print(f"Total Time:      {report.total_time:.1f}s")
    print(f"Avg Time/Item:   {report.total_time/max(report.total_items, 1):.1f}s")
    print(f"Success Rate:    {100*report.successful/max(report.total_items, 1):.1f}%")
    print("=" * 60)

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Batch Image Processor - Alpha Medical AI Hybrid Production',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Edit existing images with Gemini
    python3 batch_image_processor.py --mode edit --input ./input/ --output ./output/

    # Generate new images with Grok
    python3 batch_image_processor.py --mode generate --prompts prompts.txt --output ./output/

    # Analyze images without editing
    python3 batch_image_processor.py --mode analyze --input ./input/
        """
    )

    parser.add_argument('--mode', choices=['edit', 'generate', 'analyze', 'hybrid'],
                        required=True, help='Processing mode')
    parser.add_argument('--input', type=str, help='Input directory for edit/analyze modes')
    parser.add_argument('--prompts', type=str, help='Prompts file for generate mode')
    parser.add_argument('--output', type=str, default='./output/ai-production',
                        help='Output directory')
    parser.add_argument('--prompt', type=str, help='Custom prompt for edit mode')
    parser.add_argument('--count', type=int, default=2,
                        help='Images per prompt for generate mode')
    parser.add_argument('--no-report', action='store_true',
                        help='Skip saving JSON report')

    args = parser.parse_args()

    print("=" * 60)
    print("BATCH IMAGE PROCESSOR - Alpha Medical AI Hybrid Production")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Mode: {args.mode}")
    print(f"Gemini API: {'✅ Found' if GEMINI_API_KEY else '❌ Missing'}")
    print(f"Grok API: {'✅ Found' if XAI_API_KEY else '❌ Missing (add XAI_API_KEY to .env)'}")
    print("=" * 60)

    if args.mode == 'edit':
        if not args.input:
            print("❌ --input required for edit mode")
            sys.exit(1)
        if not GEMINI_API_KEY:
            print("❌ GOOGLE_GEMINI_API_KEY required for edit mode")
            sys.exit(1)

        report = process_batch_edit(args.input, args.output, args.prompt)
        print_summary(report)
        if not args.no_report:
            save_report(report, args.output)

    elif args.mode == 'generate':
        if not args.prompts:
            print("❌ --prompts required for generate mode")
            sys.exit(1)
        if not XAI_API_KEY:
            print("❌ XAI_API_KEY required for generate mode")
            print("   Add to .env: XAI_API_KEY=xai-xxxxxxxxxxxxx")
            print("   Get key from: https://console.x.ai")
            sys.exit(1)

        report = process_batch_generate(args.prompts, args.output, args.count)
        print_summary(report)
        if not args.no_report:
            save_report(report, args.output)

    elif args.mode == 'analyze':
        if not args.input:
            print("❌ --input required for analyze mode")
            sys.exit(1)
        if not GEMINI_API_KEY:
            print("❌ GOOGLE_GEMINI_API_KEY required for analyze mode")
            sys.exit(1)

        input_path = Path(args.input)
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        images = [f for f in input_path.iterdir() if f.suffix.lower() in image_extensions]

        print(f"📁 Analyzing {len(images)} images...")

        for i, img_file in enumerate(images, 1):
            print(f"\n[{i}/{len(images)}] {img_file.name}")
            print("-" * 40)
            success, analysis = analyze_image_gemini(str(img_file))
            if success:
                print(analysis)
            else:
                print(f"❌ Error: {analysis}")
            time.sleep(RATE_LIMIT_DELAY)

    elif args.mode == 'hybrid':
        if not args.input and not args.prompts:
            print("❌ --input and/or --prompts required for hybrid mode")
            sys.exit(1)

        # Process edits if input provided
        if args.input:
            print("\n📝 PHASE 1: Image Editing (Gemini)")
            edit_report = process_batch_edit(args.input, args.output, args.prompt)
            print_summary(edit_report)

        # Process generations if prompts provided
        if args.prompts:
            print("\n🎨 PHASE 2: Image Generation (Grok)")
            gen_report = process_batch_generate(args.prompts, args.output, args.count)
            print_summary(gen_report)

if __name__ == '__main__':
    main()
