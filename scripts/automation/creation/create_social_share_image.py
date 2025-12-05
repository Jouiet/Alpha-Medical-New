#!/usr/bin/env python3
"""
Generate Social Share Image (1200x630px) for Alpha Medical
Priority 4 QUICK WIN - Upload to Shopify Theme Settings
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Alpha Medical Brand Colors
GRADIENT_START = "#4A90E2"  # Medical Blue
GRADIENT_END = "#7FCCC9"    # Teal
WHITE = "#FFFFFF"
DARK_GRAY = "#212529"

# Image dimensions (Facebook/LinkedIn optimal)
WIDTH = 1200
HEIGHT = 630

print("=" * 70)
print("CREATING ALPHA MEDICAL SOCIAL SHARE IMAGE")
print("=" * 70)

# Create image with gradient background
image = Image.new('RGB', (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

# Create gradient (blue to teal, left to right)
for x in range(WIDTH):
    # Linear interpolation between colors
    ratio = x / WIDTH
    r = int(0x4A + (0x7F - 0x4A) * ratio)
    g = int(0x90 + (0xCC - 0x90) * ratio)
    b = int(0xE2 + (0xC9 - 0xE2) * ratio)
    color = (r, g, b)
    draw.line([(x, 0), (x, HEIGHT)], fill=color)

# Load fonts (system fonts fallback)
try:
    # Try to load a bold font
    font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
    font_tagline = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    font_url = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
except:
    # Fallback to default
    font_title = ImageFont.load_default()
    font_tagline = ImageFont.load_default()
    font_url = ImageFont.load_default()
    print("⚠️  Using default fonts (system fonts not found)")

# Add text overlay
text_title = "Alpha Medical Care"
text_tagline = "Professional Relief. Proven Results."
text_url = "www.alphamedical.shop"

# Calculate text positions (centered)
bbox_title = draw.textbbox((0, 0), text_title, font=font_title)
title_width = bbox_title[2] - bbox_title[0]
title_x = (WIDTH - title_width) // 2
title_y = 150

bbox_tagline = draw.textbbox((0, 0), text_tagline, font=font_tagline)
tagline_width = bbox_tagline[2] - bbox_tagline[0]
tagline_x = (WIDTH - tagline_width) // 2
tagline_y = 280

bbox_url = draw.textbbox((0, 0), text_url, font=font_url)
url_width = bbox_url[2] - bbox_url[0]
url_x = (WIDTH - url_width) // 2
url_y = 450

# Draw text with shadow for better readability
# Shadow
draw.text((title_x + 3, title_y + 3), text_title, font=font_title, fill=(0, 0, 0, 128))
draw.text((tagline_x + 2, tagline_y + 2), text_tagline, font=font_tagline, fill=(0, 0, 0, 128))
draw.text((url_x + 2, url_y + 2), text_url, font=font_url, fill=(0, 0, 0, 128))

# Main text (white)
draw.text((title_x, title_y), text_title, font=font_title, fill=WHITE)
draw.text((tagline_x, tagline_y), text_tagline, font=font_tagline, fill=WHITE)
draw.text((url_x, url_y), text_url, font=font_url, fill=WHITE)

# Add decorative elements (circles)
draw.ellipse([50, 250, 150, 350], outline=WHITE, width=3)
draw.ellipse([1050, 250, 1150, 350], outline=WHITE, width=3)

# Save image
output_path = "/Users/mac/Desktop/Alpha-Medical/alpha_medical_social_share.png"
image.save(output_path, "PNG", quality=95)

print(f"\n✅ Social share image created successfully!")
print(f"📁 Location: {output_path}")
print(f"📐 Dimensions: {WIDTH}x{HEIGHT}px")
print(f"📊 File size: {os.path.getsize(output_path) / 1024:.1f} KB")

print("\n" + "=" * 70)
print("NEXT STEPS (MANUAL - 5 MINUTES):")
print("=" * 70)
print("1. Go to: Shopify Admin → Online Store → Themes → Customize")
print("2. Click: Theme settings (bottom left)")
print("3. Scroll to: Social media section")
print("4. Upload: alpha_medical_social_share.png to 'Share image' field")
print("5. Click: Save")
print("\nVERIFICATION:")
print("- Test with Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/")
print("- Paste URL: https://www.alphamedical.shop/")
print("- Verify image displays correctly")
print("=" * 70)
