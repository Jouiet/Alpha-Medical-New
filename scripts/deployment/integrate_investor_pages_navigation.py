#!/usr/bin/env python3
"""
Integrate Investor Pages Navigation
Crée une navigation cohérente entre TOUTES les pages investisseurs.

INTÉGRATION COMPLÈTE:
1. Page principale /investors → Index avec cards vers toutes les sous-pages
2. Navigation menu sur CHAQUE sous-page → Permet de naviguer entre pages
3. Breadcrumb "← Investor Relations" sur chaque sous-page

Session 84 - 2025-12-07 (Navigation Integration)
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.admin')

# Shopify credentials
SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

# BRAND COLORS (OFFICIAL)
BRAND_COLORS = {
    'primary': '#4770db',
    'navy': '#0e1b4d',
    'light_gray': '#eff0f5',
    'white': '#ffffff',
    'sale_red': '#e32402',
}

# SUB-PAGES STRUCTURE
SUB_PAGES = [
    {
        'handle': 'investors-ai-development',
        'title': 'AI Development Partner',
        'description': '10/10 facets AI-assisted with Claude Sonnet 4.5',
        'icon': '🤖',
        'order': 1
    },
    {
        'handle': 'investors-automation-deployed',
        'title': 'Automation Deployed',
        'description': 'Shopify Flow, Klaviyo, GitHub Actions - 70-90% automated',
        'icon': '⚙️',
        'order': 2
    },
    {
        'handle': 'investors-automation-roadmap',
        'title': 'Automation Roadmap',
        'description': 'Gaps → Solutions with clear timelines',
        'icon': '🗺️',
        'order': 3
    },
    {
        'handle': 'investors-analytics',
        'title': 'Analytics & Data',
        'description': 'GTM, GA4, tracking infrastructure + BI roadmap',
        'icon': '📊',
        'order': 4
    },
    {
        'handle': 'investors-flywheel',
        'title': 'Flywheel Strategy',
        'description': 'Acquisition → Conversion → Retention → Advocacy',
        'icon': '🔄',
        'order': 5
    },
    {
        'handle': 'investors-technology-stack',
        'title': 'Technology Stack',
        'description': '278 Python scripts, API-first architecture',
        'icon': '💻',
        'order': 6
    }
]

def get_page_id(handle):
    """Get page ID by handle"""
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    params = {'handle': handle}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        pages = response.json().get('pages', [])
        if pages:
            return pages[0]['id']
    return None

def update_page_html(page_id, new_html):
    """Update page HTML"""
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages/{page_id}.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    update_data = {
        'page': {
            'id': page_id,
            'body_html': new_html
        }
    }

    response = requests.put(url, headers=headers, json=update_data)
    return response.status_code == 200

def create_navigation_component():
    """Create reusable navigation component for sub-pages"""
    nav_html = f"""
<div class="investor-nav-container">
  <div class="investor-breadcrumb">
    <a href="/pages/investors" class="breadcrumb-link">← Investor Relations</a>
  </div>

  <nav class="investor-subnav">
    <a href="/pages/investors-ai-development" class="nav-item">
      <span class="nav-icon">🤖</span>
      <span class="nav-label">AI Development</span>
    </a>
    <a href="/pages/investors-automation-deployed" class="nav-item">
      <span class="nav-icon">⚙️</span>
      <span class="nav-label">Automation Deployed</span>
    </a>
    <a href="/pages/investors-automation-roadmap" class="nav-item">
      <span class="nav-icon">🗺️</span>
      <span class="nav-label">Roadmap</span>
    </a>
    <a href="/pages/investors-analytics" class="nav-item">
      <span class="nav-icon">📊</span>
      <span class="nav-label">Analytics</span>
    </a>
    <a href="/pages/investors-flywheel" class="nav-item">
      <span class="nav-icon">🔄</span>
      <span class="nav-label">Flywheel</span>
    </a>
    <a href="/pages/investors-technology-stack" class="nav-item">
      <span class="nav-icon">💻</span>
      <span class="nav-label">Tech Stack</span>
    </a>
  </nav>
</div>
"""
    return nav_html

def create_navigation_css():
    """Create CSS for navigation components"""
    css = f"""
<style>
/* === INVESTOR NAVIGATION === */
.investor-nav-container {{
  margin: 0 0 40px 0;
  padding: 0;
}}

.investor-breadcrumb {{
  margin-bottom: 20px;
}}

.breadcrumb-link {{
  display: inline-flex;
  align-items: center;
  font-family: Questrial, -apple-system, sans-serif;
  font-size: 0.9rem;
  color: {BRAND_COLORS['primary']};
  text-decoration: none;
  transition: all 0.2s ease;
}}

.breadcrumb-link:hover {{
  color: {BRAND_COLORS['navy']};
  transform: translateX(-4px);
}}

.investor-subnav {{
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  padding: 20px;
  background: {BRAND_COLORS['light_gray']};
  border-radius: 8px;
  border: 2px solid {BRAND_COLORS['primary']};
}}

.investor-subnav .nav-item {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 16px;
  background: {BRAND_COLORS['white']};
  border: 2px solid transparent;
  border-radius: 8px;
  text-decoration: none;
  transition: all 0.3s ease;
  flex: 1;
  min-width: 120px;
}}

.investor-subnav .nav-item:hover {{
  border-color: {BRAND_COLORS['primary']};
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(71, 112, 219, 0.2);
}}

.investor-subnav .nav-item.active {{
  background: {BRAND_COLORS['primary']};
  border-color: {BRAND_COLORS['primary']};
}}

.investor-subnav .nav-icon {{
  font-size: 1.5rem;
}}

.investor-subnav .nav-item.active .nav-icon {{
  filter: grayscale(100%) brightness(200%);
}}

.investor-subnav .nav-label {{
  font-family: Archivo, -apple-system, sans-serif;
  font-size: 0.85rem;
  font-weight: 600;
  color: {BRAND_COLORS['navy']};
  text-align: center;
  line-height: 1.2;
}}

.investor-subnav .nav-item.active .nav-label {{
  color: {BRAND_COLORS['white']};
}}

/* Mobile responsive */
@media (max-width: 768px) {{
  .investor-subnav {{
    gap: 8px;
    padding: 16px;
  }}

  .investor-subnav .nav-item {{
    min-width: 100px;
    padding: 10px 12px;
  }}

  .investor-subnav .nav-icon {{
    font-size: 1.25rem;
  }}

  .investor-subnav .nav-label {{
    font-size: 0.75rem;
  }}
}}

/* === MAIN PAGE CARDS === */
.investor-pages-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
  margin: 40px 0;
}}

.investor-page-card {{
  background: {BRAND_COLORS['white']};
  border: 2px solid {BRAND_COLORS['light_gray']};
  border-radius: 8px;
  padding: 32px;
  text-decoration: none;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 16px;
}}

.investor-page-card:hover {{
  border-color: {BRAND_COLORS['primary']};
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(71, 112, 219, 0.2);
}}

.page-card-icon {{
  font-size: 3rem;
  line-height: 1;
}}

.page-card-title {{
  font-family: Archivo, -apple-system, sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: {BRAND_COLORS['navy']};
  margin: 0;
}}

.page-card-description {{
  font-family: Questrial, -apple-system, sans-serif;
  font-size: 1rem;
  color: #6b7280;
  line-height: 1.6;
  margin: 0;
}}

.page-card-cta {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: Archivo, -apple-system, sans-serif;
  font-size: 0.9rem;
  font-weight: 600;
  color: {BRAND_COLORS['primary']};
  margin-top: auto;
}}

.investor-page-card:hover .page-card-cta {{
  gap: 12px;
}}
</style>
"""
    return css

def update_main_investor_page():
    """Update main /investors page with sub-pages index"""
    page_id = get_page_id('investors')

    if not page_id:
        print("❌ ERROR: Main investor page not found")
        return False

    # Get current page
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages/{page_id}.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ ERROR: Failed to fetch main page (status {response.status_code})")
        return False

    current_html = response.json()['page']['body_html']

    # Create sub-pages grid section
    pages_grid_html = """
<div class="investor-section">
  <h2 style="font-family: Archivo, sans-serif; font-size: 2rem; font-weight: 700; color: #0e1b4d; margin: 40px 0 20px 0;">Explore Our Investor Relations</h2>
  <p style="font-family: Questrial, sans-serif; font-size: 1.1rem; color: #6b7280; margin-bottom: 32px;">Deep dive into each facet of our AI-driven business model and automation infrastructure.</p>

  <div class="investor-pages-grid">
"""

    # Add cards for each sub-page
    for page in SUB_PAGES:
        card_html = f"""
    <a href="/pages/{page['handle']}" class="investor-page-card">
      <div class="page-card-icon">{page['icon']}</div>
      <h3 class="page-card-title">{page['title']}</h3>
      <p class="page-card-description">{page['description']}</p>
      <div class="page-card-cta">Explore Details →</div>
    </a>
"""
        pages_grid_html += card_html

    pages_grid_html += """
  </div>
</div>
"""

    # Insert before closing </div> or at the end before <style>
    insertion_point = current_html.find('<style>')
    if insertion_point == -1:
        insertion_point = current_html.rfind('</div>')

    if insertion_point != -1:
        new_html = current_html[:insertion_point] + '\n\n' + pages_grid_html + '\n\n' + current_html[insertion_point:]
    else:
        new_html = current_html + '\n\n' + pages_grid_html

    # Add CSS if not already present
    if '.investor-pages-grid' not in new_html:
        nav_css = create_navigation_css()
        style_close = new_html.rfind('</style>')
        if style_close != -1:
            new_html = new_html[:style_close] + '\n' + nav_css + '\n' + new_html[style_close:]
        else:
            new_html += '\n\n' + nav_css

    # Update page
    if update_page_html(page_id, new_html):
        print("✅ Main investor page updated with sub-pages index")
        return True
    else:
        print("❌ ERROR: Failed to update main page")
        return False

def add_navigation_to_subpage(page_handle):
    """Add navigation component to a sub-page"""
    page_id = get_page_id(page_handle)

    if not page_id:
        print(f"   ⏭️  SKIP: Page not found ({page_handle})")
        return False

    # Get current page
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages/{page_id}.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"   ❌ ERROR: Failed to fetch page (status {response.status_code})")
        return False

    current_html = response.json()['page']['body_html']

    # Check if navigation already exists
    if 'investor-nav-container' in current_html:
        print(f"   ✅ SKIP: Navigation already exists")
        return True

    # Add navigation at the top (after first opening tag)
    nav_component = create_navigation_component()

    # Find first <div> or <section> and insert navigation after it starts
    first_div = current_html.find('<div')
    if first_div != -1:
        # Find end of opening tag
        opening_close = current_html.find('>', first_div)
        if opening_close != -1:
            new_html = current_html[:opening_close+1] + '\n\n' + nav_component + '\n\n' + current_html[opening_close+1:]
        else:
            new_html = nav_component + '\n\n' + current_html
    else:
        new_html = nav_component + '\n\n' + current_html

    # Add CSS if not present
    if '.investor-nav-container' not in new_html:
        nav_css = create_navigation_css()
        style_close = new_html.rfind('</style>')
        if style_close != -1:
            new_html = new_html[:style_close] + '\n' + nav_css + '\n' + new_html[style_close:]
        else:
            new_html += '\n\n' + nav_css

    # Add active class to current page
    current_page_link = f'href="/pages/{page_handle}"'
    new_html = new_html.replace(
        f'<a {current_page_link} class="nav-item">',
        f'<a {current_page_link} class="nav-item active">'
    )

    # Update page
    if update_page_html(page_id, new_html):
        print(f"   ✅ Navigation added")
        return True
    else:
        print(f"   ❌ ERROR: Failed to update")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("INTEGRATE INVESTOR PAGES NAVIGATION")
    print("=" * 70)
    print()

    if not SHOP_DOMAIN or not ACCESS_TOKEN:
        print("❌ ERROR: Missing Shopify credentials")
        sys.exit(1)

    # Step 1: Update main investor page
    print("STEP 1: Update main /investors page with sub-pages index")
    print("=" * 70)
    if not update_main_investor_page():
        print("\n❌ FAILED: Could not update main page")
        sys.exit(1)

    print()

    # Step 2: Add navigation to all sub-pages
    print("STEP 2: Add navigation to all sub-pages")
    print("=" * 70)

    success_count = 0
    for page in SUB_PAGES:
        print(f"\n📄 {page['handle']}")
        if add_navigation_to_subpage(page['handle']):
            success_count += 1

    print()
    print("=" * 70)
    print("INTEGRATION COMPLETE")
    print("=" * 70)
    print(f"✅ Main page updated: /pages/investors (with sub-pages index)")
    print(f"✅ Navigation added to: {success_count}/{len(SUB_PAGES)} sub-pages")
    print()
    print("NAVIGATION FEATURES:")
    print("   • Breadcrumb '← Investor Relations' on each sub-page")
    print("   • Horizontal navigation menu with 6 sub-pages")
    print("   • Active page highlighting")
    print("   • Main page with clickable cards to all sub-pages")
    print("   • 100% brand-compliant colors and typography")
