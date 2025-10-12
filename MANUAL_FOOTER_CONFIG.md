# MANUAL FOOTER CONFIGURATION REQUIRED

## Store Name Branding

**CRITICAL**: Change store name from "My Store" to "Alpha Medical Care"

### Steps:
1. Go to Shopify Admin → Settings → Store details
2. Change "Store name" from "My Store" to "Alpha Medical Care"
3. Save changes

This will automatically update:
- Footer copyright text
- Header store name
- All references to store name across the site

---

## Footer Menu Structure

**Required**: Create 3 footer menu columns with specific links

### Column 1: SHOP
Navigate to: Shopify Admin → Content → Menus

Create or edit "Footer menu" with these items:
- **Shop All** → /collections/all
- **Bestsellers** → /pages/bestsellers
- **New Arrivals** → /pages/new-arrivals

### Column 2: BRAND
Create new menu "Footer BRAND" with these items:
- **About us** → /pages/a-propos (or /pages/about-us)
- **Shipping & Delivery** → /pages/shipping-delivery
- **Returns & Exchanges** → /pages/returns-exchanges
- **FAQ** → /pages/faq

### Column 3: CONNECT
Create new menu "Footer CONNECT" with these items:
- **Instagram** → https://instagram.com/alphamedicalcare (replace with actual URL)
- **TikTok** → https://tiktok.com/@alphamedicalcare (replace with actual URL)
- **Facebook** → https://facebook.com/alphamedicalcare (replace with actual URL)
- **Contact us** → /pages/contact

---

## Apply Menus to Footer in Theme Customizer

1. Go to: Shopify Admin → Boutique en ligne → Thèmes
2. Click "Personnaliser" on Alpha-Medical-New/main theme
3. Navigate to Footer section at bottom of page
4. For each menu block:
   - Click "Ajouter un bloc" → Select "Menu"
   - Change heading text (e.g., "SHOP", "BRAND", "CONNECT")
   - Click on Menu dropdown → Select the corresponding menu
   - Repeat for all 3 columns

5. **Save** the theme changes

---

## Current Status

**COMPLETED**:
- ✅ About Us page content exists at /pages/a-propos
- ✅ 7 content files created (FAQ, Shipping, Returns, Terms, Bestsellers, Black Friday, New Arrivals)
- ✅ All files pushed to GitHub

**PENDING MANUAL WORK**:
- ⏳ Change store name to "Alpha Medical Care"
- ⏳ Create 3 footer menus (SHOP, BRAND, CONNECT)
- ⏳ Configure footer blocks in theme customizer
- ⏳ Paste content into 7 empty pages in Shopify admin
- ⏳ Set up social media links

---

## Notes

- The store name change will immediately reflect across the entire site
- Menu creation must be done before configuring theme footer blocks
- Each footer column should be a separate menu block in the theme customizer
- Ensure all page URLs match the actual page slugs in Shopify

