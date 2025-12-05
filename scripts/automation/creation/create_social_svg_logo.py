#!/usr/bin/env python3
"""
Final Social Share - SVG Logo (Higher Quality)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import subprocess

WIDTH = 1200
HEIGHT = 630
DARK_NAVY = (0x0E, 0x1B, 0x4D)
WHITE = (255, 255, 255)

# Convert SVG to PNG first (high resolution)
svg_path = os.path.join(os.path.dirname(__file__), 'Images/Alpha Medical Logo Negatif.svg')
logo_png_temp = '/tmp/logo_negatif_temp.png'

# Try multiple conversion methods
converted = False

# Method 1: qlmanage (macOS built-in)
try:
    subprocess.run([
        'qlmanage', '-t', '-s', '600', '-o', '/tmp/', svg_path
    ], check=True, capture_output=True, timeout=5)

    # qlmanage creates filename.svg.png
    qlmanage_output = svg_path.split('/')[-1] + '.png'
    qlmanage_path = f'/tmp/{qlmanage_output}'

    if os.path.exists(qlmanage_path):
        os.rename(qlmanage_path, logo_png_temp)
        converted = True
        print(f"✅ SVG converted via qlmanage")
except:
    pass

# Method 2: Use rsvg-convert if available
if not converted:
    try:
        subprocess.run([
            'rsvg-convert', '-h', '600', svg_path, '-o', logo_png_temp
        ], check=True, timeout=5)
        converted = True
        print(f"✅ SVG converted via rsvg-convert")
    except:
        pass

# Method 3: Use ImageMagick convert
if not converted:
    try:
        subprocess.run([
            'convert', '-density', '300', '-background', 'none',
            svg_path, '-resize', '600x600', logo_png_temp
        ], check=True, timeout=5)
        converted = True
        print(f"✅ SVG converted via ImageMagick")
    except:
        pass

if not converted:
    print(f"❌ Could not convert SVG. Using PNG fallback.")
    logo_png_temp = os.path.join(os.path.dirname(__file__), 'Images/Alpha Medical Logo Negatif.png')

# Load base image
base_path = os.path.join(os.path.dirname(__file__), 'Images/Hero-PNG/Design sans titre10.png')
base_img = Image.open(base_path).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

# Overlay
overlay = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw_overlay = ImageDraw.Draw(overlay)

gradient_height = 250
for y in range(gradient_height):
    alpha = int((y / gradient_height) * 180)
    draw_overlay.rectangle(
        [(0, HEIGHT - gradient_height + y), (WIDTH, HEIGHT - gradient_height + y + 1)],
        fill=(DARK_NAVY[0], DARK_NAVY[1], DARK_NAVY[2], alpha)
    )

base_img = base_img.convert('RGBA')
base_img = Image.alpha_composite(base_img, overlay)
base_img = base_img.convert('RGB')
draw = ImageDraw.Draw(base_img)

# Load logo (now high-res from SVG)
try:
    logo = Image.open(logo_png_temp).convert('RGBA')
    logo = logo.resize((200, 200), Image.Resampling.LANCZOS)
    base_img.paste(logo, (30, 25), logo)
    print(f"✅ High-res logo added from SVG")
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

shadow = 3

# Title
draw.text((title_x + shadow, title_y + shadow), text_title, font=font_title, fill=(0, 0, 0))
draw.text((title_x, title_y), text_title, font=font_title, fill=WHITE)

# Subtitle
draw.text((subtitle_x + shadow, subtitle_y + shadow), text_subtitle, font=font_subtitle, fill=(0, 0, 0))
draw.text((subtitle_x, subtitle_y), text_subtitle, font=font_subtitle, fill=WHITE)

# USPs
draw.text((usps_x, usps_y), usps_text, font=font_usps, fill=WHITE)

# Save
output_jpg = os.path.join(os.path.dirname(__file__), 'alpha_medical_social_share.jpg')
output_png = os.path.join(os.path.dirname(__file__), 'alpha_medical_social_share.png')

base_img.save(output_jpg, 'JPEG', quality=85, optimize=True)
base_img.save(output_png, 'PNG', optimize=True)

jpg_size = os.path.getsize(output_jpg) / 1024
png_size = os.path.getsize(output_png) / 1024

print(f"\n✅ FINAL VERSION WITH SVG LOGO!")
print(f"   JPEG: {jpg_size:.1f} KB")
print(f"   PNG:  {png_size:.1f} KB")
print(f"   Logo: SVG → High-resolution PNG")
print(f"\n🎯 Upload: {output_jpg}")
