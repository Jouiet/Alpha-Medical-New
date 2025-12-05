#!/usr/bin/env python3
"""
Final Professional Social Share Image - With Negative Logo
"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 1200
HEIGHT = 630

# BRANDING
DARK_NAVY = (0x0E, 0x1B, 0x4D)
WHITE = (255, 255, 255)

# Load base lifestyle image
base_path = os.path.join(os.path.dirname(__file__), 'Images/Hero-PNG/Design sans titre10.png')
base_img = Image.open(base_path).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

# Create overlay
overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw_overlay = ImageDraw.Draw(overlay)

# Gradient overlay at bottom (for text readability)
gradient_height = 250
for y in range(gradient_height):
    alpha = int((y / gradient_height) * 180)
    draw_overlay.rectangle(
        [(0, HEIGHT - gradient_height + y), (WIDTH, HEIGHT - gradient_height + y + 1)],
        fill=(DARK_NAVY[0], DARK_NAVY[1], DARK_NAVY[2], alpha)
    )

# Composite
base_img = base_img.convert('RGBA')
base_img = Image.alpha_composite(base_img, overlay)
base_img = base_img.convert('RGB')
draw = ImageDraw.Draw(base_img)

# Load NEGATIVE logo
logo_path = os.path.join(os.path.dirname(__file__), 'Images/Alpha Medical Logo Negatif.png')
try:
    logo = Image.open(logo_path).convert('RGBA')
    logo = logo.resize((200, 200), Image.Resampling.LANCZOS)

    # Position in top-left without background circle (logo has its own style)
    base_img.paste(logo, (30, 25), logo)
    print(f"✅ Negative logo added")
except Exception as e:
    print(f"⚠️  Logo error: {e}")

# Fonts
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 62)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 38)
    font_usps = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
except:
    font_title = font_subtitle = font_usps = ImageFont.load_default()

# Text
text_title = "ALPHA MEDICAL CARE"
text_subtitle = "Professional Relief. Proven Results."
usps_text = "FDA-Compliant  •  30-Day Guarantee  •  10,000+ Customers"

# Positions
title_y = HEIGHT - 195
subtitle_y = HEIGHT - 125
usps_y = HEIGHT - 65

# Center text
title_bbox = draw.textbbox((0, 0), text_title, font=font_title)
title_x = (WIDTH - (title_bbox[2] - title_bbox[0])) // 2

subtitle_bbox = draw.textbbox((0, 0), text_subtitle, font=font_subtitle)
subtitle_x = (WIDTH - (subtitle_bbox[2] - subtitle_bbox[0])) // 2

usps_bbox = draw.textbbox((0, 0), usps_text, font=font_usps)
usps_x = (WIDTH - (usps_bbox[2] - usps_bbox[0])) // 2

# Draw with shadows
shadow = 3

# Title
draw.text((title_x + shadow, title_y + shadow), text_title, font=font_title, fill=(0, 0, 0))
draw.text((title_x, title_y), text_title, font=font_title, fill=WHITE)

# Subtitle
draw.text((subtitle_x + shadow, subtitle_y + shadow), text_subtitle, font=font_subtitle, fill=(0, 0, 0))
draw.text((subtitle_x, subtitle_y), text_subtitle, font=font_subtitle, fill=WHITE)

# USPs
draw.text((usps_x, usps_y), usps_text, font=font_usps, fill=WHITE)

# Save as JPEG (optimized for photos)
output_jpg = os.path.join(os.path.dirname(__file__), 'alpha_medical_social_share.jpg')
base_img.save(output_jpg, 'JPEG', quality=85, optimize=True)

# Also save PNG (if Shopify prefers)
output_png = os.path.join(os.path.dirname(__file__), 'alpha_medical_social_share.png')
base_img.save(output_png, 'PNG', optimize=True)

jpg_size = os.path.getsize(output_jpg) / 1024
png_size = os.path.getsize(output_png) / 1024

print(f"\n✅ FINAL PROFESSIONAL SOCIAL SHARE IMAGE!")
print(f"   JPEG: {jpg_size:.1f} KB (recommended)")
print(f"   PNG:  {png_size:.1f} KB")
print(f"\n📋 FEATURES:")
print(f"   ✅ Real lifestyle product photos")
print(f"   ✅ Negative logo (cyan - professional)")
print(f"   ✅ Gradient overlay for text readability")
print(f"   ✅ Trust badges (FDA, 30-day, 10,000+)")
print(f"\n🎯 Upload: {output_jpg if jpg_size < 150 else output_png}")
