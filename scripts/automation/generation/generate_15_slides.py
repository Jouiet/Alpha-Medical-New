#!/usr/bin/env python3
"""
Générer templates/index.json avec 15 slides Hero
"""

import json
from pathlib import Path

# Images hero-slide (format shopify://shop_images/)
IMAGE_REFS = [
    "shopify://shop_images/hero-slide-1.png",
    "shopify://shop_images/hero-slide-2.png",
    "shopify://shop_images/hero-slide-3.png",
    "shopify://shop_images/hero-slide-4.png",
    "shopify://shop_images/hero-slide-5.png",
    "shopify://shop_images/hero-slide-6.png",
    "shopify://shop_images/hero-slide-7.png",
    "shopify://shop_images/hero-slide-8.png",
    "shopify://shop_images/hero-slide-9.png",
    "shopify://shop_images/hero-slide-10.png",
    "shopify://shop_images/hero-slide-11.png",
    "shopify://shop_images/hero-slide-12.png",
    "shopify://shop_images/hero-slide-13.png",
    "shopify://shop_images/hero-slide-14.png",
    "shopify://shop_images/hero-slide-15.png"
]

# Content pour les 15 slides (varié et marketing)
SLIDE_CONTENT = [
    {
        "heading": "Professional Medical Support Equipment",
        "subheading": "Quality orthopedic braces, therapy devices & recovery tools",
        "button_label": "Shop Now",
        "link": "shopify://collections/all"
    },
    {
        "heading": "Pain Relief & Recovery Solutions",
        "subheading": "Trusted by thousands for effective pain management",
        "button_label": "Explore Collection",
        "link": "shopify://collections/pain-relief-recovery"
    },
    {
        "heading": "Posture Correction & Support",
        "subheading": "Ergonomic braces for better posture and spine health",
        "button_label": "View Products",
        "link": "shopify://collections/posture-support"
    },
    {
        "heading": "Advanced Therapy & Wellness",
        "subheading": "LED therapy, massage devices & recovery equipment",
        "button_label": "Discover More",
        "link": "shopify://collections/therapy-wellness"
    },
    {
        "heading": "Orthopedic Braces & Supports",
        "subheading": "Professional-grade knee, ankle, wrist & back braces",
        "button_label": "Browse Braces",
        "link": "shopify://collections/all"
    },
    {
        "heading": "LED Light Therapy Devices",
        "subheading": "7-color photon therapy for skin rejuvenation & anti-aging",
        "button_label": "See Devices",
        "link": "shopify://collections/therapy-wellness"
    },
    {
        "heading": "Compression & Recovery Gear",
        "subheading": "Athletic support for sports, gym & injury prevention",
        "button_label": "Shop Sports",
        "link": "shopify://collections/pain-relief-recovery"
    },
    {
        "heading": "Cervical & Neck Support",
        "subheading": "Traction devices, collars & posture correctors",
        "button_label": "View Neck Care",
        "link": "shopify://collections/posture-support"
    },
    {
        "heading": "Massage & Relaxation",
        "subheading": "Electric massagers, cupping therapy & EMS devices",
        "button_label": "Relax Now",
        "link": "shopify://collections/therapy-wellness"
    },
    {
        "heading": "Home Physical Therapy",
        "subheading": "Professional rehab equipment for home use",
        "button_label": "Start Recovery",
        "link": "shopify://collections/pain-relief-recovery"
    },
    {
        "heading": "Beauty & Anti-Aging",
        "subheading": "Face masks, eye massagers & skin care devices",
        "button_label": "Look Younger",
        "link": "shopify://collections/therapy-wellness"
    },
    {
        "heading": "Joint & Muscle Support",
        "subheading": "Targeted relief for knees, shoulders, elbows & more",
        "button_label": "Find Relief",
        "link": "shopify://collections/pain-relief-recovery"
    },
    {
        "heading": "Posture Improvement Tools",
        "subheading": "Correct slouching, reduce back pain, improve alignment",
        "button_label": "Stand Tall",
        "link": "shopify://collections/posture-support"
    },
    {
        "heading": "4.8★ Rated by Thousands",
        "subheading": "Free Shipping Over $50 | 30-Day Returns | Expert Support",
        "button_label": "Shop Bestsellers",
        "link": "shopify://collections/all"
    },
    {
        "heading": "Medical-Grade Quality",
        "subheading": "FDA-approved materials | Professional recommendations",
        "button_label": "Shop All",
        "link": "shopify://collections/all"
    }
]

# Générer les blocks pour le slideshow
blocks = {}
block_order = []

for i, (image_ref, content) in enumerate(zip(IMAGE_REFS, SLIDE_CONTENT), 1):
    block_id = f"slide-{i}"
    block_order.append(block_id)

    blocks[block_id] = {
        "type": "slide",
        "settings": {
            "image": image_ref,
            "image_overlay_opacity": 10,
            "heading": content['heading'],
            "heading_size": "h1",
            "subheading": content['subheading'],
            "button_label": content['button_label'],
            "link": content['link'],
            "button_style_secondary": False,
            "show_text_box": True,
            "box_align": "middle-center",
            "text_alignment": "center",
            "text_alignment_mobile": "center",
            "color_scheme": "scheme-2"
        }
    }

# Créer la structure complète du template
template = {
    "sections": {
        "slideshow": {
            "type": "slideshow",
            "blocks": blocks,
            "block_order": block_order,
            "settings": {
                "layout": "full_bleed",
                "slide_height": "medium",
                "slider_visual": "dots",
                "auto_rotate": True,
                "change_slides_speed": 5,
                "image_behavior": "none",
                "show_text_below": True,
                "accessibility_info": "Alpha Medical Care product showcase"
            }
        },
        "featured-collection-0": {
            "type": "featured-collection",
            "settings": {
                "collection": "all",
                "products_to_show": 4,
                "title": "Featured products",
                "heading_size": "h2",
                "description": "",
                "show_description": False,
                "description_style": "body",
                "columns_desktop": 4,
                "enable_desktop_slider": False,
                "full_width": False,
                "show_view_all": False,
                "view_all_style": "solid",
                "color_scheme": "scheme-1",
                "image_ratio": "portrait",
                "image_shape": "default",
                "show_secondary_image": False,
                "show_vendor": False,
                "show_rating": False,
                "quick_add": "standard",
                "columns_mobile": "2",
                "swipe_on_mobile": False,
                "padding_top": 60,
                "padding_bottom": 60
            }
        },
        "bestsellers-section": {
            "type": "featured-collection",
            "settings": {
                "collection": "all",
                "products_to_show": 8,
                "title": "🔥 Our Bestsellers",
                "heading_size": "h2",
                "description": "<p>Discover our most popular medical support products trusted by thousands</p>",
                "show_description": True,
                "description_style": "body",
                "columns_desktop": 4,
                "enable_desktop_slider": False,
                "full_width": False,
                "show_view_all": True,
                "view_all_style": "solid",
                "color_scheme": "scheme-2",
                "image_ratio": "portrait",
                "image_shape": "default",
                "show_secondary_image": True,
                "show_vendor": False,
                "show_rating": True,
                "quick_add": "standard",
                "columns_mobile": "2",
                "swipe_on_mobile": True,
                "padding_top": 60,
                "padding_bottom": 60
            }
        },
        "black-friday-section": {
            "type": "featured-collection",
            "settings": {
                "title": "Black Friday Special Offers",
                "heading_size": "h2",
                "description": "",
                "show_description": False,
                "description_style": "body",
                "collection": "all",
                "products_to_show": 8,
                "columns_desktop": 4,
                "full_width": False,
                "show_view_all": True,
                "view_all_style": "solid",
                "enable_desktop_slider": False,
                "color_scheme": "scheme-1",
                "image_ratio": "adapt",
                "image_shape": "default",
                "show_secondary_image": False,
                "show_vendor": False,
                "show_rating": False,
                "quick_add": "none",
                "columns_mobile": "2",
                "swipe_on_mobile": False,
                "padding_top": 36,
                "padding_bottom": 36
            }
        },
        "new-arrivals-section": {
            "type": "featured-collection",
            "settings": {
                "title": "New Arrivals",
                "heading_size": "h2",
                "description": "",
                "show_description": False,
                "description_style": "body",
                "collection": "all",
                "products_to_show": 25,
                "columns_desktop": 4,
                "full_width": False,
                "show_view_all": True,
                "view_all_style": "solid",
                "enable_desktop_slider": False,
                "color_scheme": "scheme-1",
                "image_ratio": "adapt",
                "image_shape": "default",
                "show_secondary_image": False,
                "show_vendor": False,
                "show_rating": False,
                "quick_add": "none",
                "columns_mobile": "2",
                "swipe_on_mobile": False,
                "padding_top": 36,
                "padding_bottom": 36
            }
        }
    },
    "order": [
        "slideshow",
        "featured-collection-0",
        "bestsellers-section",
        "black-friday-section",
        "new-arrivals-section"
    ]
}

# Ajouter le header de commentaire
template_with_comment = """/*
 * ------------------------------------------------------------
 * IMPORTANT: The contents of this file are auto-generated.
 *
 * This file may be updated by the Shopify admin theme editor
 * or related systems. Please exercise caution as any changes
 * made to this file may be overwritten.
 * ------------------------------------------------------------
 */
""" + json.dumps(template, indent=2)

# Écrire le fichier
output_path = Path(__file__).parent / "templates" / "index.json"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(template_with_comment)

print("✅ templates/index.json généré avec 15 slides!")
print(f"   Fichier: {output_path}")
print(f"   Slides: {len(blocks)}")
print(f"   Taille: {len(template_with_comment)} caractères")
