#!/usr/bin/env python3
import json
import subprocess

# Fetch products
result = subprocess.run(
    ['curl', '-s', 'https://alphamedical.shop/products.json?limit=250'],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
products = data.get('products', [])

# Articles de blog et produits correspondants
blog_articles = {
    'Article #1 - Knee Brace Guide': ['knee', 'brace', 'support', 'patellar', 'ligament'],
    'Article #2 - LED Face Masks': ['led', 'face', 'mask', 'light', 'therapy', 'photon'],
    'Article #3 - Posture Correctors': ['posture', 'corrector', 'back', 'brace', 'spine', 'shoulder'],
    'Article #4 - LED Light Therapy': ['led', 'light', 'therapy', 'photon', 'red'],
    'Article #5 - Posture Correction': ['posture', 'corrector', 'back', 'support'],
    'Article #6 - Knee Pain Relief': ['knee', 'pain', 'brace', 'support'],
    'Article #7 - Cervical Traction': ['cervical', 'neck', 'traction', 'collar'],
    'Article #8 - Chronic Back Pain': ['back', 'lumbar', 'pain', 'support', 'brace'],
    'Article #9 - Knee Surgery Recovery': ['knee', 'immobilizer', 'post', 'surgery', 'recovery'],
    'Article #10 - Office Pain Prevention': ['posture', 'lumbar', 'back', 'neck', 'wrist', 'eye']
}

print('=== FEATURED IMAGE RECOMMENDATIONS PER ARTICLE ===\n')

image_assignments = {}

for article, keywords in blog_articles.items():
    print(f'\n{article}')
    print('=' * 60)

    # Trouver les produits correspondants
    matching_products = []
    for p in products:
        title = p.get('title', '').lower()
        handle = p.get('handle', '').lower()

        # Vérifier si les mots-clés correspondent
        match_score = sum(1 for kw in keywords if kw in title or kw in handle)
        if match_score >= 2:  # Au moins 2 mots-clés correspondent
            images = p.get('images', [])
            if images:
                matching_products.append({
                    'title': p.get('title'),
                    'handle': p.get('handle'),
                    'image': images[0].get('src'),
                    'score': match_score
                })

    # Trier par score et prendre le top 1
    matching_products.sort(key=lambda x: x['score'], reverse=True)

    if matching_products:
        top_product = matching_products[0]
        print(f'RECOMMENDED PRODUCT:')
        print(f'  Title: {top_product["title"]}')
        print(f'  Handle: {top_product["handle"]}')
        print(f'  Image URL: {top_product["image"]}')
        print(f'  Match score: {top_product["score"]}/{len(keywords)}')

        image_assignments[article] = {
            'product_title': top_product['title'],
            'product_handle': top_product['handle'],
            'image_url': top_product['image']
        }
    else:
        print('  ⚠️  No matching products found')

# Save to JSON file
with open('/Users/mac/Desktop/Alpha-Medical/blog-images-assignments.json', 'w') as f:
    json.dump(image_assignments, f, indent=2)

print('\n\n✅ Image assignments saved to: blog-images-assignments.json')
