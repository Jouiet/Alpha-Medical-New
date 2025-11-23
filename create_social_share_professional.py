#!/usr/bin/env python3
"""
Create Professional Social Share Image - Using REAL Product Photos
High-quality version with actual lifestyle product images
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

# Image dimensions
WIDTH = 1200
HEIGHT = 630

# ALPHA MEDICAL BRANDING COLORS
PRIMARY_BLUE = (0x47, 0x70, 0xDB)
DARK_NAVY = (0x0E, 0x1B, 0x4D)
WHITE = (255, 255, 255)

# Load base image (active lifestyle with knee braces)
base_image_path = os.path.join(os.path.dirname(__file__),
                               'Images/Hero-PNG/Design sans titre10.png')

try:
    # Load and resize base image
    base_img = Image.open(base_image_path)

    # Resize to social share dimensions while maintaining quality
    base_img = base_img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    print(f"✅ Loaded base image: {base_image_path}")

except Exception as e:
    print(f"❌ Error loading base image: {e}")
    exit(1)

# Create overlay for branding
overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw_overlay = ImageDraw.Draw(overlay)

# Add gradient overlay at bottom for text readability
gradient_height = 250
for y in range(gradient_height):
    alpha = int((y / gradient_height) * 180)  # Fade from transparent to semi-opaque
    draw_overlay.rectangle(
        [(0, HEIGHT - gradient_height + y), (WIDTH, HEIGHT - gradient_height + y + 1)],
        fill=(DARK_NAVY[0], DARK_NAVY[1], DARK_NAVY[2], alpha)
    )

# Add slight blue tint overlay on entire image
blue_tint = Image.new('RGBA', (WIDTH, HEIGHT), (*PRIMARY_BLUE, 20))

# Composite overlays
base_img = base_img.convert('RGBA')
base_img = Image.alpha_composite(base_img, blue_tint)
base_img = Image.alpha_composite(base_img, overlay)

# Convert back to RGB for text drawing
base_img = base_img.convert('RGB')
draw = ImageDraw.Draw(base_img)

# Load logo
logo_path = os.path.join(os.path.dirname(__file__), 'Alpha Medical Logo.png')
try:
    logo = Image.open(logo_path).convert('RGBA')
    logo = logo.resize((180, 180), Image.Resampling.LANCZOS)

    # Position logo in top-left
    logo_x = 40
    logo_y = 30

    # Add white background circle for logo visibility
    logo_bg = Image.new('RGBA', (200, 200), (255, 255, 255, 240))
    mask = Image.new('L', (200, 200), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, 200, 200], fill=255)

    base_img.paste(logo_bg, (logo_x - 10, logo_y - 10), mask)
    base_img.paste(logo, (logo_x, logo_y), logo)

    print(f"✅ Logo added: {logo_x}, {logo_y}")

except Exception as e:
    print(f"⚠️  Could not add logo: {e}")

# Load fonts
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 58)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    font_usps = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_usps = ImageFont.load_default()

# Text content
text_title = "ALPHA MEDICAL CARE"
text_subtitle = "Professional Relief. Proven Results."
usps_text = "FDA-Compliant  •  30-Day Guarantee  •  10,000+ Customers"

# Calculate positions (bottom area with gradient)
title_y = HEIGHT - 200
subtitle_y = HEIGHT - 130
usps_y = HEIGHT - 70

# Get text bounding boxes for centering
title_bbox = draw.textbbox((0, 0), text_title, font=font_title)
title_width = title_bbox[2] - title_bbox[0]
title_x = (WIDTH - title_width) // 2

subtitle_bbox = draw.textbbox((0, 0), text_subtitle, font=font_subtitle)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (WIDTH - subtitle_width) // 2

usps_bbox = draw.textbbox((0, 0), usps_text, font=font_usps)
usps_width = usps_bbox[2] - usps_bbox[0]
usps_x = (WIDTH - usps_width) // 2

# Draw text with shadow for depth
shadow_offset = 3

# Title
draw.text((title_x + shadow_offset, title_y + shadow_offset), text_title,
          font=font_title, fill=(0, 0, 0, 180))
draw.text((title_x, title_y), text_title, font=font_title, fill=WHITE)

# Subtitle
draw.text((subtitle_x + shadow_offset, subtitle_y + shadow_offset), text_subtitle,
          font=font_subtitle, fill=(0, 0, 0, 150))
draw.text((subtitle_x, subtitle_y), text_subtitle, font=font_subtitle, fill=WHITE)

# USPs
draw.text((usps_x, usps_y), usps_text, font=font_usps, fill=(255, 255, 255, 230))

# Save final image
output_path = os.path.join(os.path.dirname(__file__), 'alpha_medical_social_share.png')
base_img.save(output_path, 'PNG', optimize=True, quality=95)

file_size = os.path.getsize(output_path) / 1024

print(f"\n✅ PROFESSIONAL SOCIAL SHARE IMAGE CREATED!")
print(f"   Path: {output_path}")
print(f"   Dimensions: {WIDTH}x{HEIGHT}px")
print(f"   Base: Real lifestyle product photos")
print(f"   Branding: Logo + gradient overlay")
print(f"   File size: {file_size:.1f} KB")
print(f"\n📋 FEATURES:")
print(f"   ✅ Real product photography (active lifestyle)")
print(f"   ✅ Alpha Medical logo (top-left)")
print(f"   ✅ Professional gradient overlay")
print(f"   ✅ Clear branding text")
print(f"   ✅ Trust badges (FDA, 30-day, 10,000+)")
print(f"\n🎯 NEXT STEP:")
print(f"   Re-upload to: Shopify → Online Store → Preferences → Social sharing image")
