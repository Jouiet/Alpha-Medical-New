#!/usr/bin/env python3
"""
CHECK SHOPIFY MARKETS - Alpha Medical
Analyse les marchés configurés sur Shopify pour définir les cibles Apify

Récupère:
- Markets actifs (Shopify Markets)
- Shipping zones configurés
- Currencies acceptées
- Pays cibles pour le lead generation
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env.admin (not .env)
env_admin_path = Path(__file__).parent.parent / ".env.admin"

# Load token from .env.admin
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

if not SHOPIFY_TOKEN:
    print("❌ SHOPIFY_ADMIN_ACCESS_TOKEN not found in .env.admin")
    sys.exit(1)
API_VERSION = "2024-10"

GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"
REST_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}"

headers = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}


def get_markets():
    """Get Shopify Markets configuration"""

    query = """
    {
      markets(first: 10) {
        edges {
          node {
            id
            name
            enabled
            primary
            regions(first: 50) {
              edges {
                node {
                  id
                  name
                  ... on MarketRegionCountry {
                    code
                  }
                }
              }
            }
            currencySettings {
              baseCurrency {
                currencyCode
              }
              localCurrencies
            }
          }
        }
      }
    }
    """

    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get markets: {response.status_code}")
        print(f"   Response: {response.text}")
        return None


def get_shipping_zones():
    """Get shipping zones via REST API"""

    url = f"{REST_URL}/shipping_zones.json"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json().get("shipping_zones", [])
    else:
        print(f"❌ Failed to get shipping zones: {response.status_code}")
        return []


def get_shop_info():
    """Get basic shop info including primary location"""

    query = """
    {
      shop {
        name
        email
        currencyCode
        primaryDomain {
          url
        }
        billingAddress {
          country
          countryCodeV2
        }
      }
    }
    """

    response = requests.post(GRAPHQL_URL, json={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ Failed to get shop info: {response.status_code}")
        return None


def analyze_markets(markets_data):
    """Analyze markets data and return target countries"""

    if not markets_data or 'data' not in markets_data:
        return []

    target_countries = []
    markets = markets_data['data']['markets']['edges']

    print("\n" + "=" * 70)
    print("SHOPIFY MARKETS CONFIGURATION")
    print("=" * 70)

    for market_edge in markets:
        market = market_edge['node']

        print(f"\n📍 Market: {market['name']}")
        print(f"   Status: {'✅ Enabled' if market['enabled'] else '❌ Disabled'}")
        print(f"   Primary: {'Yes' if market['primary'] else 'No'}")

        # Currency
        currency_settings = market.get('currencySettings', {})
        base_currency = currency_settings.get('baseCurrency', {}).get('currencyCode', 'N/A')
        print(f"   Base Currency: {base_currency}")

        # Regions/Countries
        regions = market.get('regions', {}).get('edges', [])
        print(f"   Regions/Countries: {len(regions)}")

        for region_edge in regions:
            region = region_edge['node']
            country_code = region.get('code', 'N/A')
            country_name = region.get('name', 'N/A')

            print(f"      - {country_name} ({country_code})")

            if market['enabled'] and country_code != 'N/A':
                target_countries.append({
                    "country_code": country_code,
                    "country_name": country_name,
                    "market": market['name'],
                    "currency": base_currency
                })

    return target_countries


def analyze_shipping_zones(shipping_zones):
    """Analyze shipping zones to understand coverage"""

    print("\n" + "=" * 70)
    print("SHIPPING ZONES CONFIGURATION")
    print("=" * 70)

    shipping_countries = []

    for zone in shipping_zones:
        print(f"\n🚚 Zone: {zone['name']}")
        print(f"   Countries:")

        for country in zone.get('countries', []):
            code = country.get('code', 'N/A')
            name = country.get('name', 'N/A')

            print(f"      - {name} ({code})")

            if code != 'N/A':
                shipping_countries.append({
                    "country_code": code,
                    "country_name": name,
                    "zone": zone['name']
                })

    return shipping_countries


def generate_apify_target_config(target_countries):
    """
    Generate Apify lead generation target configuration

    Maps countries to:
    - Cities for Google Maps scraping
    - Location tags for Instagram/social media
    """

    # Major cities by country
    CITY_MAPPING = {
        "US": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia",
               "San Francisco", "Miami", "Seattle", "Boston", "Atlanta", "Dallas"],
        "CA": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton"],
        "GB": ["London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Edinburgh"],
        "AU": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"],
        "FR": ["Paris", "Marseille", "Lyon", "Toulouse", "Nice"],
        "DE": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
    }

    apify_config = {
        "target_markets": [],
        "lead_generation_locations": []
    }

    # Get unique countries
    unique_countries = {}
    for country in target_countries:
        code = country['country_code']
        if code not in unique_countries:
            unique_countries[code] = country

    print("\n" + "=" * 70)
    print("APIFY LEAD GENERATION TARGET CONFIGURATION")
    print("=" * 70)

    for code, country in unique_countries.items():
        market_config = {
            "country_code": code,
            "country_name": country['country_name'],
            "cities": CITY_MAPPING.get(code, [country['country_name']]),
            "language": "en" if code in ["US", "CA", "GB", "AU"] else "multi"
        }

        apify_config["target_markets"].append(market_config)

        # Generate lead generation locations
        for city in market_config["cities"]:
            apify_config["lead_generation_locations"].append({
                "location": f"{city}, {country['country_name']}",
                "country_code": code,
                "language": market_config["language"]
            })

        print(f"\n🎯 {country['country_name']} ({code})")
        print(f"   Cities: {', '.join(market_config['cities'][:3])}...")
        print(f"   Language: {market_config['language']}")

    return apify_config


def main():
    print("=" * 70)
    print("SHOPIFY MARKETS ANALYSIS - Alpha Medical")
    print("=" * 70)
    print(f"\nStore: {SHOPIFY_DOMAIN}")

    # Get shop info
    shop_info = get_shop_info()
    if shop_info:
        shop_data = shop_info['data']['shop']
        print(f"Shop Name: {shop_data['name']}")
        print(f"Primary Currency: {shop_data['currencyCode']}")
        print(f"Base Country: {shop_data['billingAddress']['country']}")

    # Get markets
    print("\n" + "=" * 70)
    print("FETCHING MARKETS...")
    print("=" * 70)

    markets_data = get_markets()
    target_countries = analyze_markets(markets_data) if markets_data else []

    # Get shipping zones
    print("\n" + "=" * 70)
    print("FETCHING SHIPPING ZONES...")
    print("=" * 70)

    shipping_zones = get_shipping_zones()
    shipping_countries = analyze_shipping_zones(shipping_zones)

    # Generate Apify configuration
    if target_countries or shipping_countries:
        # Combine both sources
        all_countries = target_countries + shipping_countries

        apify_config = generate_apify_target_config(all_countries)

        # Save configuration
        output_file = Path(__file__).parent / "apify_target_markets.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(apify_config, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 70)
        print("✅ CONFIGURATION SAVED")
        print("=" * 70)
        print(f"\nFile: {output_file}")
        print(f"Total Markets: {len(apify_config['target_markets'])}")
        print(f"Total Locations: {len(apify_config['lead_generation_locations'])}")

        print("\n📋 SUMMARY FOR APIFY LEAD GENERATION:")
        print(f"   • Target Countries: {', '.join([m['country_code'] for m in apify_config['target_markets']])}")
        print(f"   • Lead Gen Locations: {len(apify_config['lead_generation_locations'])} cities")
        print(f"   • Primary Language: English")

        return apify_config

    else:
        print("\n❌ No markets or shipping zones found")
        return None


if __name__ == "__main__":
    main()
