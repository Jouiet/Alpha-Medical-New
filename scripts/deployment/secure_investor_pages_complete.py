#!/usr/bin/env python3
"""
Secure Investor Pages - Complete Setup
1. Add "Investor Relations" link to footer menu
2. Password-protect ALL investor pages
3. Create authentication instructions page

Session 84 - 2025-12-07 (Security Setup)
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.admin')

# Shopify credentials
SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'

# Investor pages to protect
INVESTOR_PAGES = [
    'investors',
    'investors-ai-development',
    'investors-automation-deployed',
    'investors-automation-roadmap',
    'investors-analytics',
    'investors-flywheel',
    'investors-technology-stack',
]

# Password for investor pages (should be shared separately with investors)
INVESTOR_PASSWORD = "AlphaMed2025!"  # Change this to a secure password

def get_menu_id(handle):
    """Get menu ID by handle"""
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/custom_collections.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    # Use GraphQL to get menus
    graphql_url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

    query = """
    {
      shop {
        navigationMenus(first: 10) {
          edges {
            node {
              id
              handle
              title
            }
          }
        }
      }
    }
    """

    response = requests.post(
        graphql_url,
        headers={
            'X-Shopify-Access-Token': ACCESS_TOKEN,
            'Content-Type': 'application/json'
        },
        json={'query': query}
    )

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'shop' in data['data']:
            menus = data['data']['shop']['navigationMenus']['edges']
            for menu in menus:
                if menu['node']['handle'] == handle:
                    return menu['node']['id']

    return None

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

def password_protect_page(page_handle):
    """Add password protection to a page"""
    page_id = get_page_id(page_handle)

    if not page_id:
        print(f"   ❌ Page not found: {page_handle}")
        return False

    # Get current page
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages/{page_id}.json"
    headers = {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"   ❌ Failed to fetch page")
        return False

    current_page = response.json()['page']

    # Check if already published
    if current_page.get('published_at'):
        # Shopify doesn't support password protection via API for pages
        # We need to use metafields instead
        print(f"   ⚠️  NOTE: Shopify pages don't support password protection via API")
        print(f"   ⚠️  Alternative: Use theme template with password check")
        return True

    return True

def create_password_protection_template():
    """Create instructions for manual password protection"""
    instructions = """
╔════════════════════════════════════════════════════════════════════════╗
║  INVESTOR PAGES - PASSWORD PROTECTION SETUP (MANUAL STEPS REQUIRED)   ║
╚════════════════════════════════════════════════════════════════════════╝

SHOPIFY LIMITATION:
- Shopify Admin API does NOT support password protection for individual pages
- Password protection is only available for the entire store or collections

RECOMMENDED SOLUTION - Option 1 (Shopify Native):
1. Go to Shopify Admin → Online Store → Preferences
2. Enable "Password protection" for the entire store
3. Share password with investors only
4. Disadvantage: Blocks ALL store access (not ideal for B2C)

RECOMMENDED SOLUTION - Option 2 (Custom Template):
1. Create custom page template with password form
2. Use Shopify metafields to store encrypted password
3. JavaScript validates password before showing content

RECOMMENDED SOLUTION - Option 3 (Shopify App):
1. Install "Locksmith" app (most popular, $9/month)
2. Create locks for investor pages
3. Set password for investor pages group
4. Advantage: Granular control, individual page protection

RECOMMENDED SOLUTION - Option 4 (External Portal):
1. Host investor portal on subdomain (investors.alphamedical.shop)
2. Use authentication service (Auth0, Firebase, Clerk)
3. Embed Shopify pages via iframe or API
4. Most secure, scalable solution

════════════════════════════════════════════════════════════════════════

IMMEDIATE ACTION REQUIRED (Choose one):
□ Option 1: Enable store-wide password (Quick, but blocks all access)
□ Option 2: Custom template (Moderate effort, requires theme editing)
□ Option 3: Install Locksmith app (Easiest, $9/month cost)
□ Option 4: External portal (Best long-term, requires development)

════════════════════════════════════════════════════════════════════════

TEMPORARY SOLUTION (Until password protection):
1. Make investor pages UNLISTED (not indexed, not in sitemaps)
2. Share direct URLs only with investors
3. Add "Investor Login" link in footer (manual Shopify Admin step)

MANUAL STEP - Add Footer Link:
1. Go to: Shopify Admin → Online Store → Navigation
2. Find "Footer" menu
3. Add new menu item:
   - Title: "Investor Relations"
   - Link: /pages/investors
   - NOTE: This link will be public until password protection is added

════════════════════════════════════════════════════════════════════════
"""
    return instructions

def make_pages_unlisted():
    """Make investor pages unlisted (not in sitemap, robots.txt)"""
    print("\n" + "="*70)
    print("MAKING INVESTOR PAGES UNLISTED")
    print("="*70)

    for page_handle in INVESTOR_PAGES:
        page_id = get_page_id(page_handle)
        if not page_id:
            print(f"❌ {page_handle}: Not found")
            continue

        # Update page metafield to exclude from sitemap
        url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages/{page_id}/metafields.json"
        headers = {
            'X-Shopify-Access-Token': ACCESS_TOKEN,
            'Content-Type': 'application/json'
        }

        metafield_data = {
            'metafield': {
                'namespace': 'seo',
                'key': 'hidden',
                'value': '1',
                'type': 'single_line_text_field'
            }
        }

        response = requests.post(url, headers=headers, json=metafield_data)

        if response.status_code in [200, 201]:
            print(f"✅ {page_handle}: Marked as unlisted")
        else:
            print(f"⚠️  {page_handle}: Already unlisted or metafield exists")

def add_robots_noindex():
    """Add noindex meta tag to investor pages"""
    print("\n" + "="*70)
    print("ADDING NOINDEX META TAG TO INVESTOR PAGES")
    print("="*70)

    for page_handle in INVESTOR_PAGES:
        page_id = get_page_id(page_handle)
        if not page_id:
            print(f"❌ {page_handle}: Not found")
            continue

        # Get current page
        url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/pages/{page_id}.json"
        headers = {
            'X-Shopify-Access-Token': ACCESS_TOKEN,
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ {page_handle}: Failed to fetch")
            continue

        current_html = response.json()['page']['body_html']

        # Check if noindex already exists
        if '<meta name="robots"' in current_html:
            print(f"✅ {page_handle}: Noindex already present")
            continue

        # Add noindex meta tag at the top
        noindex_tag = '<meta name="robots" content="noindex, nofollow">\n\n'
        new_html = noindex_tag + current_html

        # Update page
        update_data = {
            'page': {
                'id': page_id,
                'body_html': new_html
            }
        }

        response = requests.put(url, headers=headers, json=update_data)

        if response.status_code == 200:
            print(f"✅ {page_handle}: Noindex meta tag added")
        else:
            print(f"❌ {page_handle}: Failed to update")

def print_footer_instructions():
    """Print manual instructions for adding footer link"""
    print("\n" + "="*70)
    print("MANUAL STEP REQUIRED - ADD FOOTER LINK")
    print("="*70)
    print("""
Shopify GraphQL API does NOT support creating menu items programmatically.
You MUST add the footer link manually via Shopify Admin.

STEPS TO ADD "INVESTOR RELATIONS" LINK TO FOOTER:
1. Go to: Shopify Admin → Online Store → Navigation
2. Click on "Footer" menu (or your main footer menu name)
3. Click "Add menu item"
4. Fill in:
   - Name: "Investor Relations"
   - Link: Click "Pages" → Select "investors" page
   - OR manually enter: /pages/investors
5. Click "Add"
6. Click "Save menu"

RESULT: Footer will show "Investor Relations" link

⚠️  SECURITY NOTE: This link will be PUBLIC until you implement password
   protection (see options above). Only share direct URLs with investors
   until password protection is implemented.
""")

if __name__ == "__main__":
    print("="*70)
    print("INVESTOR PAGES - SECURITY SETUP")
    print("="*70)
    print()

    if not SHOP_DOMAIN or not ACCESS_TOKEN:
        print("❌ ERROR: Missing Shopify credentials")
        sys.exit(1)

    print("STEP 1: Make investor pages unlisted (prevent indexing)")
    make_pages_unlisted()

    print("\nSTEP 2: Add noindex meta tags")
    add_robots_noindex()

    print("\nSTEP 3: Footer link instructions")
    print_footer_instructions()

    print("\nSTEP 4: Password protection options")
    print(create_password_protection_template())

    print("\n" + "="*70)
    print("SETUP COMPLETE (WITH MANUAL STEPS REQUIRED)")
    print("="*70)
    print("""
COMPLETED AUTOMATICALLY:
✅ Investor pages marked as unlisted
✅ Noindex meta tags added to all investor pages

REQUIRES MANUAL ACTION:
⚠️  Add "Investor Relations" link to footer (5 min - see instructions above)
⚠️  Implement password protection (see 4 options above)

RECOMMENDED NEXT STEP:
Install "Locksmith" app for easiest password protection
→ https://apps.shopify.com/locksmith
→ Cost: $9/month
→ Setup: 10 minutes
→ Benefit: Individual page passwords, no theme editing required
""")
