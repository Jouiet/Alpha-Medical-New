
import json
import os
import re
from datetime import datetime

# Paths
CATALOG_PATH = "alpha_medical_complete_catalog.json"
INVENTORY_PATH = "alpha_medical_product_inventory.json"
REPORT_PATH = "audit_reports/product_audit_report.md"

def load_json(path):
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return None
    with open(path, 'r') as f:
        return json.load(f)

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext.strip()

def run_audit():
    print("🔍 Starting Product Forensic Audit...")
    
    # Load Data
    catalog_data = load_json(CATALOG_PATH)
    inventory = load_json(INVENTORY_PATH)
    
    if not catalog_data or not inventory:
        print("❌ Failed to load data.")
        return

    products = catalog_data.get('products', [])

    # Prepare Inventory Map (Product Name -> Category)
    product_categories = {}
    categories = inventory.get('categories', {})
    
    for cat_name, cat_data in categories.items():
        for prod_name in cat_data.get('products', []):
            product_categories[prod_name] = cat_name

    # Audit Stats
    total_products = len(products)
    issues = {
        "missing_images": [],
        "zero_price": [],
        "missing_description": [],
        "short_description": [], # < 50 chars
        "uncategorized": [],
        "invalid_handle": []
    }

    print(f"📊 Analyzing {total_products} products...")

    for p in products:
        p_id = p.get('id')
        title = p.get('title', 'Unknown')
        handle = p.get('handle', '')
        images = p.get('images', [])
        body_html = p.get('body_html', '') or ''
        clean_desc = clean_html(body_html)
        variants = p.get('variants', [])
        
        # Check Price (Direct key in this file)
        price = p.get('price', "0.00")
        
        # 1. Missing Images (Key missing in this file)
        if 'images' not in p or not p['images']:
            issues["missing_images"].append(f"{title} ({handle})")

        # 2. Zero Price
        try:
            if float(price) == 0.0:
                 issues["zero_price"].append(f"{title} ({handle}) - Price: {price}")
        except:
             issues["zero_price"].append(f"{title} ({handle}) - Invalid Price: {price}")

        # 3. Description Checks (body_html missing in this file)
        clean_desc = ""
        if 'body_html' in p:
             clean_desc = clean_html(p['body_html'] or "")
        
        if not clean_desc:
            issues["missing_description"].append(f"{title} ({handle})")
        elif len(clean_desc) < 50:
            issues["short_description"].append(f"{title} ({handle}) - Len: {len(clean_desc)}")

        # 4. Handle Check
        if not re.match(r'^[a-z0-9-]+$', handle):
             issues["invalid_handle"].append(f"{title} ({handle})")

        # 5. Category Check
        # Try to find title in inventory mapping
        # This is fuzzy because inventory file has names, catalog has names.
        if title not in product_categories:
             issues["uncategorized"].append(f"{title}")

    # Generate Report
    os.makedirs('audit_reports', exist_ok=True)
    
    with open(REPORT_PATH, 'w') as f:
        f.write("# 🕵️ Product Forensic Audit Report\n\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total Products Analyzed:** {total_products}\n\n")
        
        f.write("## 🚨 Executive Summary\n\n")
        f.write("| Metric | Count | Status |\n")
        f.write("| :--- | :---: | :--- |\n")
        f.write(f"| Missing Images | {len(issues['missing_images'])} | {'🔴 Critical' if issues['missing_images'] else '✅ OK'} |\n")
        f.write(f"| Zero Price | {len(issues['zero_price'])} | {'🔴 Critical' if issues['zero_price'] else '✅ OK'} |\n")
        f.write(f"| Missing Descriptions | {len(issues['missing_description'])} | {'🟠 Warning' if issues['missing_description'] else '✅ OK'} |\n")
        f.write(f"| Short Descriptions (<50 chars) | {len(issues['short_description'])} | {'🟡 Info' if issues['short_description'] else '✅ OK'} |\n")
        f.write(f"| Uncategorized (vs Inventory) | {len(issues['uncategorized'])} | {'🟠 Warning' if issues['uncategorized'] else '✅ OK'} |\n")
        f.write("\n")

        f.write("## 📝 Detailed Findings\n\n")
        
        if issues["zero_price"]:
            f.write("### 💸 Zero Price Products (Critical)\n")
            for item in issues["zero_price"]:
                f.write(f"- [ ] {item}\n")
            f.write("\n")

        if issues["missing_images"]:
            f.write("### 🖼️ Products Missing Images\n")
            for item in issues["missing_images"]:
                f.write(f"- [ ] {item}\n")
            f.write("\n")

        if issues["missing_description"]:
            f.write("### 📄 Products with Missing Descriptions\n")
            for item in issues["missing_description"]:
                f.write(f"- [ ] {item}\n")
            f.write("\n")

        if issues["uncategorized"]:
            f.write("### 📂 Uncategorized Products\n")
            f.write("> Note: These products were not found in `alpha_medical_product_inventory.json` by exact name match.\n\n")
            for item in issues["uncategorized"]:
                f.write(f"- {item}\n")
            f.write("\n")

    print(f"✅ Audit Complete. Report generated at: {REPORT_PATH}")
    print(f"   Missing Images: {len(issues['missing_images'])}")
    print(f"   Zero Price: {len(issues['zero_price'])}")
    print(f"   Uncategorized: {len(issues['uncategorized'])}")

if __name__ == "__main__":
    run_audit()
