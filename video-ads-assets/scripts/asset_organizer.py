#!/usr/bin/env python3
"""
ASSET ORGANIZER - Alpha Medical Video Ads
Automates folder structure creation and asset organization verification

Usage:
    python asset_organizer.py --create {product-handle}
    python asset_organizer.py --verify {product-handle}
    python asset_organizer.py --verify-all

Examples:
    python asset_organizer.py --create tourmaline-knee-pads
    python asset_organizer.py --verify magnetic-posture-corrector
    python asset_organizer.py --verify-all
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Base paths
SCRIPT_DIR = Path(__file__).parent.resolve()
BASE_DIR = SCRIPT_DIR.parent.parent  # Alpha-Medical/
PRODUCTS_DIR = SCRIPT_DIR.parent / "products"


def create_product_folders(product_handle: str) -> bool:
    """
    Create complete folder structure for a new product

    Creates:
    - products/{handle}/hero-images/
    - products/{handle}/lifestyle-images/
    - products/{handle}/feature-closeups/
    - products/{handle}/metadata/

    Args:
        product_handle: Product handle (e.g., 'tourmaline-knee-pads')

    Returns:
        bool: True if created successfully, False if already exists
    """
    product_path = PRODUCTS_DIR / product_handle

    if product_path.exists():
        print(f"❌ Product folder already exists: {product_handle}")
        print(f"   Location: {product_path}")
        return False

    # Create main product folder
    product_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created product folder: {product_handle}")

    # Create subfolders
    subfolders = [
        "hero-images",
        "lifestyle-images",
        "feature-closeups",
        "metadata"
    ]

    for folder in subfolders:
        folder_path = product_path / folder
        folder_path.mkdir(exist_ok=True)
        print(f"   ✅ Created: {folder}/")

    # Create metadata files
    create_metadata_files(product_path, product_handle)

    print(f"\n🎉 Product structure ready: {product_handle}")
    print(f"📂 Location: {product_path}")
    print(f"\n📝 Next steps:")
    print(f"   1. Update metadata/product-info.txt with product details")
    print(f"   2. Add Shopify URL to metadata/shopify-url.txt")
    print(f"   3. Gather and organize product images into subfolders")

    return True


def create_metadata_files(product_path: Path, product_handle: str):
    """Create metadata template files for a product"""

    metadata_dir = product_path / "metadata"

    # Create shopify-url.txt
    shopify_url_file = metadata_dir / "shopify-url.txt"
    shopify_url_content = f"https://alphamedical.shop/products/{product_handle}\n"
    shopify_url_file.write_text(shopify_url_content)
    print(f"   ✅ Created: metadata/shopify-url.txt")

    # Create product-info.txt template
    product_info_file = metadata_dir / "product-info.txt"
    product_info_template = f"""# PRODUCT METADATA: {product_handle.upper().replace('-', ' ')}

**Created:** {get_current_date()}
**Handle:** {product_handle}
**Shopify URL:** https://alphamedical.shop/products/{product_handle}

---

## BASIC INFO

**Product Name:** [FILL: Full product name]
**Category:** [FILL: Knee Support / Back Support / Posture / etc.]
**Price:** $[FILL]
**Hero Score:** [FILL: Check TOP_10_HERO_PRODUCTS_ANALYSIS.txt]
**Priority Rank:** [FILL: Check TOP_10_HERO_PRODUCTS_MAPPING.md]

---

## TARGET AUDIENCE

**Primary Demographic:**
- Age: [FILL: e.g., 65+, 25-45, etc.]
- Gender: [FILL: Male/Female/Unisex]
- Persona: [FILL: Seniors/Office Workers/Athletes/etc.]

**Pain Points:**
- [FILL: Primary problem this solves]
- [FILL: Secondary problem]
- [FILL: Tertiary problem]

---

## UNIQUE SELLING POINTS (USPs)

**USP 1:** [FILL: e.g., Self-heating technology]
**USP 2:** [FILL: e.g., Magnetic therapy nodes]
**USP 3:** [FILL: e.g., Medical-grade materials]

**Key Features:**
- [FILL: Feature 1]
- [FILL: Feature 2]
- [FILL: Feature 3]

---

## CERTIFICATIONS & SOCIAL PROOF

**Certifications:**
- [ ] FDA-Registered
- [ ] CE Certified
- [ ] Medical-Grade
- [ ] Other: [FILL]

**Social Proof:**
- Customer Count: [FILL: e.g., 8,000+]
- Star Rating: [FILL: e.g., 4.8/5]
- Review Count: [FILL: e.g., 3,000+]

---

## DISCOUNT CODES

**Active Codes:**
- Code 1: [FILL: e.g., WARMKNEES20 (-20%)]
- Code 2: [FILL: e.g., SENIOR20 (-20%)]
- Code 3: [FILL: e.g., WINTER30 (-30%)]

---

## VIDEO ADS STRATEGY

**Recommended Video Types (Priority Order):**
1. [ ] UGC Testimonial (15 sec) - Best for: [FILL: Demographic reason]
2. [ ] Before/After (12 sec) - Best for: [FILL: Visual transformation]
3. [ ] Product Demo (20 sec) - Best for: [FILL: Technology/features]
4. [ ] Comparison (25 sec) - Best for: [FILL: Premium positioning]
5. [ ] Educational (30 sec) - Best for: [FILL: Authority building]

**Template Selection:**
- Primary: [FILL: ugc/ba/demo/comp/edu]
- Secondary: [FILL: ugc/ba/demo/comp/edu]

**Platform Priority:**
- Platform 1: [FILL: TikTok/IG Reels/FB Feed]
- Platform 2: [FILL]
- Platform 3: [FILL]

---

## ASSETS INVENTORY

**Hero Images:**
- [ ] [FILL: filename or "Not yet gathered"]

**Lifestyle Images:**
- [ ] [FILL: filename or "Not yet gathered"]

**Feature Close-ups:**
- [ ] [FILL: filename or "Not yet gathered"]

---

## VIDEOS CREATED

**Video 1:**
- Date: [TBD]
- Type: [TBD]
- Filename: [TBD]
- Status: [TBD]

---

**NEXT STEPS:**
1. Fill all [FILL] sections with actual product data
2. Gather and organize product images
3. Select template and create first video
4. Update this metadata with video filename when created
"""

    product_info_file.write_text(product_info_template)
    print(f"   ✅ Created: metadata/product-info.txt (template)")


def verify_product_structure(product_handle: str) -> Tuple[bool, Dict]:
    """
    Verify product folder structure and asset completeness

    Args:
        product_handle: Product handle to verify

    Returns:
        Tuple[bool, Dict]: (is_complete, details_dict)
    """
    product_path = PRODUCTS_DIR / product_handle

    if not product_path.exists():
        print(f"❌ Product folder does not exist: {product_handle}")
        print(f"   Run: python asset_organizer.py --create {product_handle}")
        return False, {}

    print(f"\n📋 VERIFYING: {product_handle}")
    print(f"📂 Location: {product_path}\n")

    results = {
        "folders": {},
        "metadata": {},
        "images": {},
        "ready": False
    }

    # Check folders
    required_folders = ["hero-images", "lifestyle-images", "feature-closeups", "metadata"]
    for folder in required_folders:
        folder_path = product_path / folder
        exists = folder_path.exists()
        results["folders"][folder] = exists

        status = "✅" if exists else "❌"
        print(f"{status} {folder}/")

    print()

    # Check metadata files
    metadata_files = ["shopify-url.txt", "product-info.txt"]
    for file in metadata_files:
        file_path = product_path / "metadata" / file
        exists = file_path.exists()
        results["metadata"][file] = exists

        status = "✅" if exists else "❌"
        print(f"{status} metadata/{file}")

    print()

    # Count images in each folder
    image_folders = ["hero-images", "lifestyle-images", "feature-closeups"]
    for folder in image_folders:
        folder_path = product_path / folder
        if folder_path.exists():
            images = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png"))
            count = len(images)
            results["images"][folder] = count

            status = "✅" if count > 0 else "⚠️"
            print(f"{status} {folder}/: {count} image(s)")

            if count > 0:
                for img in images[:3]:  # Show first 3
                    print(f"      - {img.name}")
                if count > 3:
                    print(f"      ... and {count - 3} more")

    print()

    # Overall readiness check
    hero_ready = results["images"].get("hero-images", 0) >= 1
    lifestyle_ready = results["images"].get("lifestyle-images", 0) >= 1
    feature_ready = results["images"].get("feature-closeups", 0) >= 1
    metadata_ready = all(results["metadata"].values())

    results["ready"] = hero_ready and lifestyle_ready and metadata_ready

    print("=" * 50)
    print("READINESS CHECK:")
    print(f"{'✅' if hero_ready else '❌'} Hero images: {'Ready' if hero_ready else 'Need at least 1'}")
    print(f"{'✅' if lifestyle_ready else '❌'} Lifestyle images: {'Ready' if lifestyle_ready else 'Need at least 1'}")
    print(f"{'⚠️' if feature_ready else '❌'} Feature close-ups: {'Ready' if feature_ready else 'Recommended (optional)'}")
    print(f"{'✅' if metadata_ready else '❌'} Metadata files: {'Complete' if metadata_ready else 'Incomplete'}")
    print()

    if results["ready"]:
        print("🎉 READY TO CREATE VIDEO!")
        print(f"   Follow: VIDEO_ADS_CREATION_PLAYBOOK.md")
        print(f"   Templates: video-ads-assets/templates/")
    else:
        print("⚠️  NOT READY YET")
        print("   Next steps:")
        if not hero_ready:
            print(f"   1. Add at least 1 hero image to {product_handle}/hero-images/")
        if not lifestyle_ready:
            print(f"   2. Add at least 1 lifestyle image to {product_handle}/lifestyle-images/")
        if not metadata_ready:
            print(f"   3. Complete metadata files in {product_handle}/metadata/")

    print("=" * 50)

    return results["ready"], results


def verify_all_products() -> Dict:
    """Verify all products in products folder"""

    if not PRODUCTS_DIR.exists():
        print(f"❌ Products directory not found: {PRODUCTS_DIR}")
        return {}

    product_folders = [p for p in PRODUCTS_DIR.iterdir() if p.is_dir() and not p.name.startswith('.')]

    if not product_folders:
        print(f"⚠️  No product folders found in: {PRODUCTS_DIR}")
        return {}

    print(f"\n{'='*60}")
    print(f"VERIFYING ALL PRODUCTS ({len(product_folders)} found)")
    print(f"{'='*60}")

    results = {}
    ready_count = 0

    for product_folder in sorted(product_folders):
        product_handle = product_folder.name
        is_ready, details = verify_product_structure(product_handle)
        results[product_handle] = {"ready": is_ready, "details": details}

        if is_ready:
            ready_count += 1

        print()  # Spacing between products

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: {ready_count}/{len(product_folders)} products ready for video creation")
    print(f"{'='*60}\n")

    ready_products = [handle for handle, data in results.items() if data["ready"]]
    not_ready_products = [handle for handle, data in results.items() if not data["ready"]]

    if ready_products:
        print("✅ READY FOR VIDEO CREATION:")
        for handle in ready_products:
            print(f"   - {handle}")

    if not_ready_products:
        print("\n⚠️  NEED MORE ASSETS:")
        for handle in not_ready_products:
            print(f"   - {handle}")

    return results


def get_current_date() -> str:
    """Get current date in YYYY-MM-DD format"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")


def print_usage():
    """Print usage instructions"""
    print(__doc__)


def main():
    """Main CLI entry point"""

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    if command == "--create":
        if len(sys.argv) < 3:
            print("❌ Error: Product handle required")
            print("Usage: python asset_organizer.py --create {product-handle}")
            sys.exit(1)

        product_handle = sys.argv[2]
        create_product_folders(product_handle)

    elif command == "--verify":
        if len(sys.argv) < 3:
            print("❌ Error: Product handle required")
            print("Usage: python asset_organizer.py --verify {product-handle}")
            sys.exit(1)

        product_handle = sys.argv[2]
        verify_product_structure(product_handle)

    elif command == "--verify-all":
        verify_all_products()

    elif command == "--help" or command == "-h":
        print_usage()

    else:
        print(f"❌ Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
