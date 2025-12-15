#!/usr/bin/env python3
"""
Verify Shopify Storefront API Scopes Configuration
==================================================
Purpose: Empirical verification of current Storefront API scopes
Method: Query Shopify Admin API for actual configuration
Output: Factual report with security assessment

Author: Claude Code Session 81
Date: 2025-12-06
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
from typing import Dict, List, Tuple

# Load environment variables
load_dotenv('.env.admin')

# Shopify API configuration
SHOPIFY_STORE_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_ADMIN_ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-01'

# Storefront API scopes categories
SCOPES_CATEGORIES = {
    'Checkout': [
        'unauthenticated_read_checkouts',
        'unauthenticated_write_checkouts'
    ],
    'Content': [
        'unauthenticated_read_content'
    ],
    'Customers': [
        'unauthenticated_read_customers',
        'unauthenticated_read_customer_tags',
        'unauthenticated_write_customers'
    ],
    'Metaobjects': [
        'unauthenticated_read_metaobjects'
    ],
    'Products': [
        'unauthenticated_read_product_listings',
        'unauthenticated_read_product_inventory',
        'unauthenticated_read_product_pickup_locations',
        'unauthenticated_read_product_tags'
    ],
    'Selling Plans': [
        'unauthenticated_read_selling_plans'
    ],
    'Bulk Operations': [
        'unauthenticated_read_bulk_operations',
        'unauthenticated_write_bulk_operations'
    ],
    'Bundles': [
        'unauthenticated_read_bundles'
    ],
    'Shop Pay': [
        'unauthenticated_read_shop_pay_installments_pricing'
    ]
}

# Risk levels for scopes
SCOPE_RISK_LEVELS = {
    # Low risk (public data, read-only)
    'unauthenticated_read_product_listings': 'LOW',
    'unauthenticated_read_product_tags': 'LOW',
    'unauthenticated_read_content': 'LOW',
    'unauthenticated_read_selling_plans': 'LOW',
    'unauthenticated_read_bundles': 'LOW',
    'unauthenticated_read_shop_pay_installments_pricing': 'LOW',

    # Medium risk (potentially sensitive data)
    'unauthenticated_read_product_inventory': 'MEDIUM',
    'unauthenticated_read_metaobjects': 'MEDIUM',
    'unauthenticated_read_customer_tags': 'MEDIUM',
    'unauthenticated_read_checkouts': 'MEDIUM',
    'unauthenticated_read_bulk_operations': 'MEDIUM',
    'unauthenticated_read_product_pickup_locations': 'LOW',  # Not applicable for Alpha Medical

    # High risk (privacy concerns)
    'unauthenticated_read_customers': 'HIGH',

    # Critical risk (write operations)
    'unauthenticated_write_checkouts': 'CRITICAL',
    'unauthenticated_write_customers': 'CRITICAL',
    'unauthenticated_write_bulk_operations': 'CRITICAL'
}

# Recommended scopes for Alpha Medical PRE-LAUNCH
RECOMMENDED_ENABLED = {
    'unauthenticated_read_product_listings',
    'unauthenticated_read_product_tags',
    'unauthenticated_read_selling_plans',
    'unauthenticated_read_bundles',
    'unauthenticated_read_shop_pay_installments_pricing'
}

# Critical scopes that should NEVER be enabled
NEVER_ENABLE = {
    'unauthenticated_write_checkouts',
    'unauthenticated_write_customers',
    'unauthenticated_write_bulk_operations'
}

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.END}\n")

def print_section(text: str):
    """Print formatted section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BLUE}{'-'*len(text)}{Colors.END}")

def get_storefront_access_tokens() -> List[Dict]:
    """
    Fetch Storefront Access Tokens from Shopify Admin API
    Returns: List of storefront access token configurations
    """
    url = f"https://{SHOPIFY_STORE_DOMAIN}/admin/api/{API_VERSION}/storefront_access_tokens.json"

    headers = {
        'X-Shopify-Access-Token': SHOPIFY_ADMIN_ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        return data.get('storefront_access_tokens', [])

    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}ERROR: Failed to fetch Storefront Access Tokens{Colors.END}")
        print(f"Error: {e}")
        return []

def analyze_scopes(scopes: List[str]) -> Dict:
    """
    Analyze scopes configuration and generate security assessment

    Args:
        scopes: List of enabled scope strings

    Returns:
        Dictionary with analysis results
    """
    scopes_set = set(scopes)

    # Calculate statistics
    enabled_recommended = scopes_set & RECOMMENDED_ENABLED
    missing_recommended = RECOMMENDED_ENABLED - scopes_set
    critical_enabled = scopes_set & NEVER_ENABLE

    # Categorize enabled scopes by risk
    risk_distribution = {
        'LOW': [],
        'MEDIUM': [],
        'HIGH': [],
        'CRITICAL': []
    }

    for scope in scopes:
        risk = SCOPE_RISK_LEVELS.get(scope, 'UNKNOWN')
        risk_distribution[risk].append(scope)

    # Security score (0-100)
    score = 100

    # Deduct points for critical risks
    score -= len(critical_enabled) * 40  # -40 points per CRITICAL scope
    score -= len(risk_distribution['HIGH']) * 20  # -20 points per HIGH risk
    score -= len(risk_distribution['MEDIUM']) * 5  # -5 points per MEDIUM risk

    # Add points for recommended scopes
    score += len(enabled_recommended) * 2  # +2 points per recommended

    # Ensure score stays within 0-100
    score = max(0, min(100, score))

    return {
        'total_scopes': len(scopes),
        'enabled_recommended': enabled_recommended,
        'missing_recommended': missing_recommended,
        'critical_enabled': critical_enabled,
        'risk_distribution': risk_distribution,
        'security_score': score
    }

def print_token_info(token: Dict):
    """Print information about a Storefront Access Token"""
    print(f"Token ID: {token.get('id', 'N/A')}")
    print(f"Title: {token.get('title', 'N/A')}")
    print(f"Access Token: {token.get('access_token', 'N/A')[:20]}...{token.get('access_token', '')[-10:]}")
    print(f"Created At: {token.get('created_at', 'N/A')}")

def print_scopes_by_category(scopes: List[str]):
    """Print scopes organized by category"""
    print_section("Enabled Scopes by Category")

    scopes_set = set(scopes)

    for category, category_scopes in SCOPES_CATEGORIES.items():
        enabled_in_category = [s for s in category_scopes if s in scopes_set]

        if enabled_in_category:
            print(f"\n{Colors.BOLD}{category}:{Colors.END}")
            for scope in enabled_in_category:
                risk = SCOPE_RISK_LEVELS.get(scope, 'UNKNOWN')
                risk_color = {
                    'LOW': Colors.GREEN,
                    'MEDIUM': Colors.YELLOW,
                    'HIGH': Colors.RED,
                    'CRITICAL': Colors.RED + Colors.BOLD
                }.get(risk, '')

                # Check if recommended or critical
                status = ""
                if scope in RECOMMENDED_ENABLED:
                    status = f" {Colors.GREEN}[RECOMMENDED]{Colors.END}"
                elif scope in NEVER_ENABLE:
                    status = f" {Colors.RED}{Colors.BOLD}[🚨 CRITICAL RISK]{Colors.END}"

                print(f"  ✓ {scope} {risk_color}[{risk}]{Colors.END}{status}")

def print_security_assessment(analysis: Dict):
    """Print security assessment report"""
    print_section("Security Assessment")

    # Security score
    score = analysis['security_score']
    score_color = Colors.GREEN if score >= 80 else Colors.YELLOW if score >= 60 else Colors.RED
    print(f"\n{Colors.BOLD}Security Score: {score_color}{score}/100{Colors.END}")

    # Risk distribution
    print(f"\n{Colors.BOLD}Risk Distribution:{Colors.END}")
    print(f"  {Colors.RED}CRITICAL:{Colors.END} {len(analysis['risk_distribution']['CRITICAL'])} scopes")
    print(f"  {Colors.RED}HIGH:{Colors.END} {len(analysis['risk_distribution']['HIGH'])} scopes")
    print(f"  {Colors.YELLOW}MEDIUM:{Colors.END} {len(analysis['risk_distribution']['MEDIUM'])} scopes")
    print(f"  {Colors.GREEN}LOW:{Colors.END} {len(analysis['risk_distribution']['LOW'])} scopes")

    # Critical scopes alert
    if analysis['critical_enabled']:
        print(f"\n{Colors.RED}{Colors.BOLD}🚨 CRITICAL SECURITY ALERT 🚨{Colors.END}")
        print(f"{Colors.RED}The following CRITICAL RISK scopes are enabled:{Colors.END}")
        for scope in analysis['critical_enabled']:
            print(f"  • {scope} {Colors.RED}[DISABLE IMMEDIATELY]{Colors.END}")

    # Recommended scopes status
    print(f"\n{Colors.BOLD}Recommended Configuration:{Colors.END}")
    print(f"  Enabled: {len(analysis['enabled_recommended'])}/{len(RECOMMENDED_ENABLED)} recommended scopes")

    if analysis['enabled_recommended']:
        print(f"\n  {Colors.GREEN}✓ Enabled (Recommended):{Colors.END}")
        for scope in analysis['enabled_recommended']:
            print(f"    • {scope}")

    if analysis['missing_recommended']:
        print(f"\n  {Colors.YELLOW}✗ Missing (Recommended):{Colors.END}")
        for scope in analysis['missing_recommended']:
            print(f"    • {scope} {Colors.YELLOW}[CONSIDER ENABLING]{Colors.END}")

def print_recommendations(analysis: Dict, current_scopes: List[str]):
    """Print actionable recommendations"""
    print_section("Recommendations")

    actions_needed = False

    # Critical: Disable high-risk scopes
    if analysis['critical_enabled'] or analysis['risk_distribution']['HIGH']:
        actions_needed = True
        print(f"\n{Colors.RED}{Colors.BOLD}1. IMMEDIATE ACTION REQUIRED - Disable High-Risk Scopes:{Colors.END}")

        if analysis['critical_enabled']:
            print(f"\n   {Colors.RED}CRITICAL RISK (DISABLE NOW):{Colors.END}")
            for scope in analysis['critical_enabled']:
                print(f"   ❌ {scope}")

        if analysis['risk_distribution']['HIGH']:
            print(f"\n   {Colors.RED}HIGH RISK (SHOULD DISABLE):{Colors.END}")
            for scope in analysis['risk_distribution']['HIGH']:
                print(f"   ⚠️ {scope}")

    # Enable recommended scopes
    if analysis['missing_recommended']:
        actions_needed = True
        print(f"\n{Colors.YELLOW}{Colors.BOLD}2. Consider Enabling Recommended Scopes:{Colors.END}")
        for scope in analysis['missing_recommended']:
            print(f"   ✓ {scope} {Colors.GREEN}[LOW RISK, HIGH VALUE]{Colors.END}")

    # Review medium-risk scopes
    medium_enabled = analysis['risk_distribution']['MEDIUM']
    if medium_enabled:
        actions_needed = True
        print(f"\n{Colors.YELLOW}{Colors.BOLD}3. Review Medium-Risk Scopes:{Colors.END}")
        for scope in medium_enabled:
            # Check if scope is applicable to Alpha Medical
            if scope == 'unauthenticated_read_product_pickup_locations':
                print(f"   ⚠️ {scope} {Colors.YELLOW}[NOT NEEDED - No physical stores]{Colors.END}")
            elif scope == 'unauthenticated_read_product_inventory':
                print(f"   ℹ️ {scope} {Colors.YELLOW}[OPTIONAL - Enable if showing stock levels]{Colors.END}")
            else:
                print(f"   ℹ️ {scope} {Colors.YELLOW}[REVIEW - Enable if needed]{Colors.END}")

    if not actions_needed and analysis['security_score'] >= 80:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Configuration looks good!{Colors.END}")
        print(f"{Colors.GREEN}No immediate actions required.{Colors.END}")
        print(f"\n{Colors.CYAN}Next Steps:{Colors.END}")
        print("  1. Review quarterly (next review: 2026-03-01)")
        print("  2. Audit actual Storefront API usage vs enabled scopes")
        print("  3. Check Shopify security recommendations")
    else:
        print(f"\n{Colors.CYAN}How to Apply Changes:{Colors.END}")
        print("  1. Go to: Shopify Admin → Settings → Apps and sales channels")
        print("  2. Click: Develop apps (or your custom app)")
        print("  3. Navigate to: Configuration → Storefront API access scopes")
        print("  4. Enable/Disable scopes as recommended above")
        print("  5. Save configuration")
        print("  6. Run this script again to verify")

def print_summary(tokens_count: int, analysis: Dict):
    """Print executive summary"""
    print_header("EXECUTIVE SUMMARY")

    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print(f"Storefront Access Tokens: {tokens_count}")
    print(f"Total Scopes Enabled: {analysis['total_scopes']}")
    print(f"Security Score: {analysis['security_score']}/100")

    if analysis['security_score'] >= 80:
        status = f"{Colors.GREEN}GOOD{Colors.END}"
    elif analysis['security_score'] >= 60:
        status = f"{Colors.YELLOW}NEEDS REVIEW{Colors.END}"
    else:
        status = f"{Colors.RED}CRITICAL - ACTION REQUIRED{Colors.END}"

    print(f"Status: {status}")

    if analysis['critical_enabled']:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️ CRITICAL: {len(analysis['critical_enabled'])} high-risk WRITE scopes enabled{Colors.END}")

    print(f"\n{Colors.CYAN}Analysis Complete: 2025-12-06 Session 81{Colors.END}")
    print(f"{Colors.CYAN}Method: Empirical verification via Shopify Admin API{Colors.END}")

def main():
    """Main execution function"""
    print_header("SHOPIFY STOREFRONT API SCOPES VERIFICATION")

    # Verify environment variables
    if not SHOPIFY_STORE_DOMAIN or not SHOPIFY_ADMIN_ACCESS_TOKEN:
        print(f"{Colors.RED}ERROR: Missing environment variables{Colors.END}")
        print("Required: SHOPIFY_STORE_DOMAIN, SHOPIFY_ADMIN_ACCESS_TOKEN")
        print("Check .env.admin file")
        sys.exit(1)

    print(f"Store: {SHOPIFY_STORE_DOMAIN}")
    print(f"API Version: {API_VERSION}")

    # Fetch Storefront Access Tokens
    print_section("Fetching Storefront Access Tokens...")
    tokens = get_storefront_access_tokens()

    if not tokens:
        print(f"{Colors.YELLOW}No Storefront Access Tokens found or API error{Colors.END}")
        print("\nPossible reasons:")
        print("  1. No custom apps with Storefront API access configured")
        print("  2. Admin API token lacks read_storefront_access_tokens scope")
        print("  3. API error or connection issue")
        sys.exit(1)

    print(f"Found {len(tokens)} Storefront Access Token(s)")

    # Analyze each token
    for i, token in enumerate(tokens, 1):
        print_header(f"TOKEN #{i} ANALYSIS")

        # Print token info
        print_section("Token Information")
        print_token_info(token)

        # Get scopes
        scopes = token.get('access_scopes', [])
        scope_handles = [scope['handle'] for scope in scopes]

        if not scope_handles:
            print(f"\n{Colors.YELLOW}No scopes enabled for this token{Colors.END}")
            continue

        # Print scopes by category
        print_scopes_by_category(scope_handles)

        # Analyze scopes
        analysis = analyze_scopes(scope_handles)

        # Print security assessment
        print_security_assessment(analysis)

        # Print recommendations
        print_recommendations(analysis, scope_handles)

    # Print summary
    if tokens:
        # Use first token for summary (typically only one token exists)
        scopes = tokens[0].get('access_scopes', [])
        scope_handles = [scope['handle'] for scope in scopes]
        analysis = analyze_scopes(scope_handles)
        print_summary(len(tokens), analysis)

    print(f"\n{Colors.GREEN}Verification complete!{Colors.END}\n")

if __name__ == "__main__":
    main()
