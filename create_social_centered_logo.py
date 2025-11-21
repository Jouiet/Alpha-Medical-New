#!/usr/bin/env python3
"""
Social Share - Logo centré en haut, taille réduite /1.30
"""

from PIL import Image, ImageDraw, ImageFont
import os

WIDTH = 1200
HEIGHT = 630
DARK_NAVY = (0x0E, 0x1B, 0x4D)
WHITE = (255, 255, 255)

# Load base image
base_path = os.path.join(os.path.dirname(__file__), 'Images/Hero-PNG/Design sans titre10.png')
base_img = Image.open(base_path).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

# Create overlay gradient
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

# Load logo PNG (Negatif version)
logo_path = os.path.join(os.path.dirname(__file__), 'Images/Alpha Medical Logo Negatif.png')

try:
    logo = Image.open(logo_path).convert('RGBA')

    # Original size would be 200x200, now divide by 1.30
    logo_size = int(200 / 1.30)  # = 153x153
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Position: CENTRÉ EN HAUT (au milieu horizontalement, en haut)
    logo_x = (WIDTH - logo_size) // 2  # Centré
    logo_y = 25  # En haut

    # Paste logo
    base_img.paste(logo, (logo_x, logo_y), logo)

    print(f"✅ Logo centré en haut: {logo_size}x{logo_size}px at ({logo_x}, {logo_y})")

except Exception as e:
    print(f"❌ Erreur logo: {e}")
    exit(1)

# Fonts
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 62)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 38)
    font_usps = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 26)
except:
    font_title = font_subtitle = font_usps = ImageFont.load_default()

# Text content
text_title = "ALPHA MEDICAL CARE"
text_subtitle = "Professional Relief. Proven Results."
usps_text = "FDA-Compliant  •  30-Day Guarantee  •  10,000+ Customers"

# Text positions (bottom gradient area)
title_y = HEIGHT - 195
subtitle_y = HEIGHT - 125
usps_y = HEIGHT - 65

# Center text horizontally
title_bbox = draw.textbbox((0, 0), text_title, font=font_title)
title_x = (WIDTH - (title_bbox[2] - title_bbox[0])) // 2

subtitle_bbox = draw.textbbox((0, 0), text_subtitle, font=font_subtitle)
subtitle_x = (WIDTH - (subtitle_bbox[2] - subtitle_bbox[0])) // 2

usps_bbox = draw.textbbox((0, 0), usps_text, font=font_usps)
usps_x = (WIDTH - (usps_bbox[2] - usps_bbox[0])) // 2

# Draw text with shadows
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

print(f"\n✅ IMAGE FINALE - LOGO CENTRÉ EN HAUT!")
print(f"   JPEG: {jpg_size:.1f} KB")
print(f"   PNG:  {png_size:.1f} KB")
print(f"   Logo: {logo_size}x{logo_size}px (réduit de 30%)")
print(f"   Position: Centre-haut ({logo_x}, {logo_y})")
print(f"\n🎯 Upload: {output_jpg}")
