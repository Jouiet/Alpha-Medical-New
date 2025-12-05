#!/usr/bin/env python3
"""
Create Alpha Medical Social Share Image - Using REAL Logo & Assets
Professional version with actual brand logo
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Image dimensions (Facebook/LinkedIn/Twitter optimal)
WIDTH = 1200
HEIGHT = 630

# REAL ALPHA MEDICAL BRANDING COLORS
PRIMARY_BLUE = (0x47, 0x70, 0xDB)    # #4770DB
DARK_NAVY = (0x0E, 0x1B, 0x4D)       # #0E1B4D
WHITE = (255, 255, 255)              # #FFFFFF
LIGHT_BG = (0xEF, 0xF0, 0xF5)        # #EFF0F5

# Create new image with gradient background
img = Image.new('RGB', (WIDTH, HEIGHT), DARK_NAVY)
draw = ImageDraw.Draw(img)

# Create professional gradient background (Dark Navy -> Primary Blue)
for y in range(HEIGHT):
    ratio = y / HEIGHT
    r = int(DARK_NAVY[0] + (PRIMARY_BLUE[0] - DARK_NAVY[0]) * ratio)
    g = int(DARK_NAVY[1] + (PRIMARY_BLUE[1] - DARK_NAVY[1]) * ratio)
    b = int(DARK_NAVY[2] + (PRIMARY_BLUE[2] - DARK_NAVY[2]) * ratio)
    color = (r, g, b)
    draw.line([(0, y), (WIDTH, y)], fill=color)

# Load and resize logo
logo_path = os.path.join(os.path.dirname(__file__), 'Alpha Medical Logo.png')

try:
    logo = Image.open(logo_path)

    # Resize logo to fit nicely (max 400px width, maintain aspect ratio)
    logo_max_width = 400
    aspect_ratio = logo.height / logo.width
    logo_width = logo_max_width
    logo_height = int(logo_width * aspect_ratio)

    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    # Position logo in center-top area
    logo_x = (WIDTH - logo_width) // 2
    logo_y = 100

    # Paste logo (with alpha channel for transparency)
    img.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)

    print(f"✅ Logo loaded and positioned: {logo_width}x{logo_height}px")

except Exception as e:
    print(f"⚠️  Could not load logo: {e}")
    # Continue without logo, will add text fallback

# Try to use system fonts
try:
    font_tagline = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 42)
    font_url = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    font_usps = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
except:
    font_tagline = ImageFont.load_default()
    font_url = ImageFont.load_default()
    font_usps = ImageFont.load_default()

# Text content
text_tagline = "Professional Relief. Proven Results."
text_url = "www.alphamedical.shop"

# USPs (trust badges)
usps = [
    "FDA-Compliant Materials",
    "30-Day Money-Back Guarantee",
    "10,000+ Happy Customers"
]

# Calculate text positions
tagline_bbox = draw.textbbox((0, 0), text_tagline, font=font_tagline)
tagline_width = tagline_bbox[2] - tagline_bbox[0]
tagline_x = (WIDTH - tagline_width) // 2
tagline_y = 420

url_bbox = draw.textbbox((0, 0), text_url, font=font_url)
url_width = url_bbox[2] - url_bbox[0]
url_x = (WIDTH - url_width) // 2
url_y = 530

# Draw tagline with shadow
shadow_offset = 2
draw.text((tagline_x + shadow_offset, tagline_y + shadow_offset), text_tagline,
          font=font_tagline, fill=(0, 0, 0, 80))
draw.text((tagline_x, tagline_y), text_tagline, font=font_tagline, fill=WHITE)

# Draw URL (lighter, no shadow)
draw.text((url_x, url_y), text_url, font=font_url, fill=LIGHT_BG)

# Draw USPs as horizontal badges at bottom
usps_y = 485
usp_spacing = 280
start_x = (WIDTH - (len(usps) * usp_spacing)) // 2 + 60

for i, usp in enumerate(usps):
    usp_x = start_x + (i * usp_spacing)

    # Draw checkmark circle
    circle_radius = 10
    circle_x = usp_x - 25
    circle_y = usps_y + 5

    draw.ellipse(
        [circle_x - circle_radius, circle_y - circle_radius,
         circle_x + circle_radius, circle_y + circle_radius],
        fill=WHITE, outline=None
    )

    # Draw checkmark
    check_points = [
        (circle_x - 4, circle_y),
        (circle_x - 1, circle_y + 4),
        (circle_x + 5, circle_y - 4)
    ]
    draw.line(check_points[:2], fill=PRIMARY_BLUE, width=2)
    draw.line(check_points[1:], fill=PRIMARY_BLUE, width=2)

    # Draw USP text
    draw.text((usp_x, usps_y), usp, font=font_usps, fill=WHITE)

# Save image
output_path = os.path.join(os.path.dirname(__file__), 'alpha_medical_social_share.png')
img.save(output_path, 'PNG', optimize=True, quality=95)

print(f"\n✅ Social share image created with REAL logo!")
print(f"   Path: {output_path}")
print(f"   Dimensions: {WIDTH}x{HEIGHT}px")
print(f"   Branding: #4770DB + #0E1B4D (gradient)")
print(f"   Logo: Alpha Medical (professional icon)")
print(f"   File size: {os.path.getsize(output_path) / 1024:.1f} KB")
print(f"\n📋 NEXT STEP:")
print(f"   Re-upload to: Shopify Admin → Online Store → Preferences → Social sharing image")
print(f"   (Replace current version with this professional logo version)")
