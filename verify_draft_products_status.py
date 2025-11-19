#!/usr/bin/env python3
"""
FORENSIC AUDIT: Draft Products Security
Verify NO draft products are accessible via /products.json
"""

import requests
import json
from datetime import datetime

print("═══════════════════════════════════════════════════════════════")
print("🔬 FORENSIC AUDIT: DRAFT PRODUCTS SECURITY")
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("═══════════════════════════════════════════════════════════════\n")

# Fetch products
response = requests.get('https://www.alphamedical.shop/products.json', timeout=10)
data = json.loads(response.text)
products = data.get('products', [])

print(f"✅ Fetched {len(products)} products from public feed\n")

# Check if any are drafts (shouldn't be in public feed)
print("🔍 CHECKING PRODUCT STATUS")
print("─" * 60)

draft_count = 0
published_count = 0

for i, product in enumerate(products, 1):
    title = product.get('title', '')[:50]
    status = product.get('status', 'unknown')
    published_at = product.get('published_at')
    
    print(f"[{i}/{len(products)}] {title}")
    
    if status == 'draft' or published_at is None:
        print(f"   ❌ DRAFT/UNPUBLISHED")
        draft_count += 1
    else:
        print(f"   ✅ PUBLISHED")
        published_count += 1

print()
print("═══════════════════════════════════════════════════════════════")
print("📊 SECURITY AUDIT REPORT")
print("═══════════════════════════════════════════════════════════════\n")

print(f"✅ Published products: {published_count}/{len(products)}")
print(f"❌ Draft/unpublished: {draft_count}/{len(products)}")
print()

if draft_count == 0:
    print("🎉 VERDICT: SECURE - No draft products exposed\n")
    exit(0)
else:
    print(f"❌ VERDICT: SECURITY ISSUE - {draft_count} drafts exposed\n")
    exit(1)
