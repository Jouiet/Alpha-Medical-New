#!/usr/bin/env python3
"""
Create Alpha Medical Social Share Image - BRANDED VERSION
Using REAL Alpha Medical branding colors and style
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

# Create new image
img = Image.new('RGB', (WIDTH, HEIGHT), DARK_NAVY)
draw = ImageDraw.Draw(img)

# Create gradient background (Dark Navy -> Primary Blue)
for y in range(HEIGHT):
    ratio = y / HEIGHT
    r = int(DARK_NAVY[0] + (PRIMARY_BLUE[0] - DARK_NAVY[0]) * ratio)
    g = int(DARK_NAVY[1] + (PRIMARY_BLUE[1] - DARK_NAVY[1]) * ratio)
    b = int(DARK_NAVY[2] + (PRIMARY_BLUE[2] - DARK_NAVY[2]) * ratio)
    color = (r, g, b)
    draw.line([(0, y), (WIDTH, y)], fill=color)

# Try to use system fonts (fallback to default if not available)
try:
    # Try Helvetica (closest to Archivo for bold headings)
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 110)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    font_url = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
except:
    # Fallback to default
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_url = ImageFont.load_default()

# Text content
text_title = "Alpha Medical Care"
text_subtitle = "Professional Relief. Proven Results."
text_url = "www.alphamedical.shop"

# Calculate text positions (centered)
title_bbox = draw.textbbox((0, 0), text_title, font=font_title)
title_width = title_bbox[2] - title_bbox[0]
title_x = (WIDTH - title_width) // 2
title_y = 160

subtitle_bbox = draw.textbbox((0, 0), text_subtitle, font=font_subtitle)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (WIDTH - subtitle_width) // 2
subtitle_y = 310

url_bbox = draw.textbbox((0, 0), text_url, font=font_url)
url_width = url_bbox[2] - url_bbox[0]
url_x = (WIDTH - url_width) // 2
url_y = 480

# Draw text with shadow for depth (medical professional style)
shadow_offset = 3

# Title shadow + text
draw.text((title_x + shadow_offset, title_y + shadow_offset), text_title,
          font=font_title, fill=(0, 0, 0, 100))
draw.text((title_x, title_y), text_title, font=font_title, fill=WHITE)

# Subtitle shadow + text
draw.text((subtitle_x + shadow_offset, subtitle_y + shadow_offset), text_subtitle,
          font=font_subtitle, fill=(0, 0, 0, 100))
draw.text((subtitle_x, subtitle_y), text_subtitle, font=font_subtitle, fill=WHITE)

# URL (no shadow, lighter style)
draw.text((url_x, url_y), text_url, font=font_url, fill=LIGHT_BG)

# Add decorative medical crosses (subtle brand element)
# Left medical cross
cross_size = 50
cross_x_left = 100
cross_y = HEIGHT // 2
cross_width = 12

# Horizontal bar
draw.rectangle(
    [cross_x_left - cross_size//2, cross_y - cross_width//2,
     cross_x_left + cross_size//2, cross_y + cross_width//2],
    fill=WHITE, outline=None
)
# Vertical bar
draw.rectangle(
    [cross_x_left - cross_width//2, cross_y - cross_size//2,
     cross_x_left + cross_width//2, cross_y + cross_size//2],
    fill=WHITE, outline=None
)

# Right medical cross
cross_x_right = WIDTH - 100
# Horizontal bar
draw.rectangle(
    [cross_x_right - cross_size//2, cross_y - cross_width//2,
     cross_x_right + cross_size//2, cross_y + cross_width//2],
    fill=WHITE, outline=None
)
# Vertical bar
draw.rectangle(
    [cross_x_right - cross_width//2, cross_y - cross_size//2,
     cross_x_right + cross_width//2, cross_y + cross_size//2],
    fill=WHITE, outline=None
)

# Save image
output_path = os.path.join(os.path.dirname(__file__), 'alpha_medical_social_share.png')
img.save(output_path, 'PNG', optimize=True, quality=95)

print(f"✅ Social share image created: {output_path}")
print(f"   Dimensions: {WIDTH}x{HEIGHT}px")
print(f"   Branding: Alpha Medical (#4770DB + #0E1B4D)")
print(f"   File size: {os.path.getsize(output_path) / 1024:.1f} KB")
print(f"\n📋 NEXT STEP:")
print(f"   Upload to: Shopify Admin → Online Store → Preferences → Social sharing image")
