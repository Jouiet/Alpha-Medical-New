#!/usr/bin/env python3
"""
CHECK INSTALLED SHOPIFY APPS - Alpha Medical
Liste toutes les apps déjà installées pour identifier les intégrations possibles

Recherche:
- Apps CRM
- Apps Email Marketing
- Apps Automation
- Apps Analytics
"""

import os
import sys
import json
import requests
from pathlib import Path

# Load .env.admin
env_admin_path = Path(__file__).parent.parent / ".env.admin"

SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
SHOPIFY_TOKEN = None

try:
    with open(env_admin_path, 'r') as f:
        for line in f:
            if line.startswith('SHOPIFY_ADMIN_ACCESS_TOKEN='):
                SHOPIFY_TOKEN = line.split('=', 1)[1].strip()
                break
except Exception as e:
    print(f"❌ Failed to load .env.admin: {e}")
    sys.exit(1)

API_VERSION = "2024-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}


def get_installed_apps():
    """Get list of installed apps via GraphQL"""

    query = """
    {
      currentAppInstallation {
        app {
          title
          handle
          description
          features
        }
      }
      appInstallations(first: 50) {
        edges {
          node {
            app {
              title
              handle
              description
              apiKey
              features
            }
            launchUrl
            uninstallUrl
          }
        }
      }
    }
    """

    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get apps: {response.status_code}")
        print(f"   Response: {response.text}")
        return None


def categorize_apps(apps_data):
    """Categorize apps by function"""

    if not apps_data or 'data' not in apps_data:
        return {}

    categories = {
        "email_marketing": [],
        "crm": [],
        "automation": [],
        "analytics": [],
        "inventory": [],
        "shipping": [],
        "other": []
    }

    apps = apps_data['data']['appInstallations']['edges']

    print("\n" + "=" * 70)
    print("INSTALLED SHOPIFY APPS")
    print("=" * 70)

    for app_edge in apps:
        app = app_edge['node']['app']

        title = app.get('title', 'N/A')
        handle = app.get('handle', 'N/A')
        description = app.get('description') or ''

        print(f"\n📱 {title}")
        print(f"   Handle: {handle}")

        if description:
            print(f"   Description: {description[:100]}...")

        # Categorize based on keywords
        title_lower = (title or '').lower()
        desc_lower = (description or '').lower()

        if any(kw in title_lower or kw in desc_lower for kw in ['email', 'mail', 'newsletter', 'campaign']):
            categories['email_marketing'].append(app)
        elif any(kw in title_lower or kw in desc_lower for kw in ['crm', 'customer relationship', 'contact']):
            categories['crm'].append(app)
        elif any(kw in title_lower or kw in desc_lower for kw in ['automat', 'workflow', 'flow']):
            categories['automation'].append(app)
        elif any(kw in title_lower or kw in desc_lower for kw in ['analytic', 'report', 'dashboard', 'tracking']):
            categories['analytics'].append(app)
        elif any(kw in title_lower or kw in desc_lower for kw in ['inventory', 'stock', 'product']):
            categories['inventory'].append(app)
        elif any(kw in title_lower or kw in desc_lower for kw in ['shipping', 'fulfillment', 'delivery']):
            categories['shipping'].append(app)
        else:
            categories['other'].append(app)

    return categories


def print_categories(categories):
    """Print apps by category"""

    print("\n" + "=" * 70)
    print("APPS BY CATEGORY")
    print("=" * 70)

    for category, apps in categories.items():
        if apps:
            print(f"\n{'='*70}")
            print(f"📂 {category.upper().replace('_', ' ')} ({len(apps)} apps)")
            print(f"{'='*70}")

            for app in apps:
                print(f"\n   • {app.get('title', 'N/A')}")
                print(f"     Handle: {app.get('handle', 'N/A')}")


def suggest_automation_workflows(categories):
    """Suggest automation workflows based on installed apps"""

    print("\n" + "=" * 70)
    print("🤖 AUTOMATION WORKFLOWS POSSIBLES (APIFY + APPS INSTALLÉES)")
    print("=" * 70)

    suggestions = []

    # Email Marketing automation
    if categories['email_marketing']:
        print(f"\n📧 EMAIL MARKETING AUTOMATION:")
        print(f"   Apps installées: {', '.join([a.get('title', 'N/A') for a in categories['email_marketing']])}")
        suggestions.append({
            "workflow": "Lead Gen → Email Nurturing",
            "steps": [
                "1. Apify scrape Instagram/Google Maps → Leads",
                "2. Google Sheets → Store & qualify leads",
                "3. Email Marketing App → Automated campaigns",
                "4. Shopify Flow → Trigger based on customer behavior"
            ]
        })

    # CRM automation
    if categories['crm']:
        print(f"\n👥 CRM AUTOMATION:")
        print(f"   Apps installées: {', '.join([a.get('title', 'N/A') for a in categories['crm']])}")
        suggestions.append({
            "workflow": "Lead Gen → CRM → Sales Closing",
            "steps": [
                "1. Apify scrape B2B leads (Google Maps)",
                "2. Enrich with contact info",
                "3. CRM App → Add to pipeline",
                "4. Shopify → Track conversions"
            ]
        })

    # Analytics automation
    if categories['analytics']:
        print(f"\n📊 ANALYTICS & REPORTING:")
        print(f"   Apps installées: {', '.join([a.get('title', 'N/A') for a in categories['analytics']])}")
        suggestions.append({
            "workflow": "Competitive Intelligence → Reporting",
            "steps": [
                "1. Apify scrape competitor prices",
                "2. Google Sheets → Store historical data",
                "3. Analytics App → Visualize trends",
                "4. Shopify → Adjust pricing strategy"
            ]
        })

    # Inventory automation
    if categories['inventory']:
        print(f"\n📦 INVENTORY & FULFILLMENT:")
        print(f"   Apps installées: {', '.join([a.get('title', 'N/A') for a in categories['inventory']])}")
        suggestions.append({
            "workflow": "Order Automation → Fulfillment",
            "steps": [
                "1. Shopify → New order trigger",
                "2. Inventory App → Check stock",
                "3. Shopify Flow → Notify fulfillment",
                "4. Email App → Customer updates"
            ]
        })

    print("\n" + "=" * 70)
    print("💡 WORKFLOW RECOMMENDATIONS")
    print("=" * 70)

    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion['workflow']}")
        for step in suggestion['steps']:
            print(f"   {step}")

    return suggestions


def main():
    print("=" * 70)
    print("SHOPIFY APPS ANALYSIS - Alpha Medical")
    print("=" * 70)
    print(f"\nStore: {SHOPIFY_DOMAIN}")

    # Get installed apps
    apps_data = get_installed_apps()

    if not apps_data:
        print("\n❌ No apps data retrieved")
        return

    # Categorize apps
    categories = categorize_apps(apps_data)

    # Print by category
    print_categories(categories)

    # Suggest automation workflows
    suggestions = suggest_automation_workflows(categories)

    # Save to JSON
    output = {
        "store": SHOPIFY_DOMAIN,
        "timestamp": "2025-11-22",
        "categories": {k: [{"title": a.get("title"), "handle": a.get("handle")} for a in v]
                      for k, v in categories.items()},
        "automation_suggestions": suggestions
    }

    output_file = Path(__file__).parent / "shopify_apps_analysis.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Analysis saved: {output_file}")


if __name__ == "__main__":
    main()
