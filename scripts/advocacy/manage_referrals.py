#!/usr/bin/env python3
"""
PHASE 4 ADVOCACY - Referral Program Management
Manages Loox referral program for customer advocacy

Flywheel Stage: ADVOCACY (Customer → Brand Ambassador)
Expected Impact: -40-60% CAC reduction, +15-25% referral CVR

Prerequisites:
1. Loox app installed (DONE - verified)
2. Loox Referrals feature enabled (CHECK IN LOOX ADMIN)
3. Loox API key (REQUIRED - configure in .env)

Referral Program Structure (Recommended):
- Referrer: $10 credit per successful referral
- Referee: 15% discount on first purchase
- VIP bonus: Extra $5 credit for Gold/Platinum loyalty members

Usage:
    python3 scripts/advocacy/manage_referrals.py --mode status
    python3 scripts/advocacy/manage_referrals.py --mode performance
    python3 scripts/advocacy/manage_referrals.py --mode top-referrers
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / '.env')
except ImportError:
    pass

LOOX_API_KEY = os.getenv('LOOX_API_KEY')


def check_api_configured():
    """Check if Loox API is configured"""
    if not LOOX_API_KEY:
        print("=" * 70)
        print("LOOX API NOT CONFIGURED")
        print("=" * 70)
        print("\nTo enable referral management:")
        print("1. Go to Loox Admin → Settings → API")
        print("2. Generate/copy your API key")
        print("3. Add to .env file:")
        print("   LOOX_API_KEY=your_api_key_here")
        print("\nTo enable referral PROGRAM:")
        print("4. Go to Loox Admin → Referrals")
        print("5. Enable referral program")
        print("6. Configure incentives:")
        print("   - Referrer: $10 credit")
        print("   - Referee: 15% discount")
        print("\n" + "=" * 70)
        return False
    return True


def get_referral_status():
    """Get current referral program status"""
    if not check_api_configured():
        return {
            "status": "API_NOT_CONFIGURED",
            "program_setup": {
                "recommended_referrer_reward": "$10 credit",
                "recommended_referee_discount": "15%",
                "vip_bonus": "$5 extra for Gold/Platinum",
                "setup_location": "Loox Admin → Referrals"
            },
            "flywheel_integration": {
                "loyalty_tagging": "Shopify Flow (active)",
                "vip_segments": ["loyalty-gold", "loyalty-platinum"],
                "email_promotion": "Klaviyo post-purchase (Day 30)"
            },
            "expected_impact": {
                "referral_rate": "5-10% of customers",
                "referral_cvr": "15-25%",
                "cac_reduction": "40-60%"
            }
        }

    # TODO: Implement actual API call when configured
    return {"status": "API_CONFIGURED", "message": "Ready to manage referrals"}


def get_referral_performance():
    """Get referral program performance metrics"""
    if not check_api_configured():
        return {
            "status": "API_NOT_CONFIGURED",
            "metrics_available_when_configured": [
                "total_referrals",
                "successful_conversions",
                "total_credits_issued",
                "top_referrers",
                "average_order_value_referred"
            ]
        }

    # TODO: Implement when API configured
    return {"status": "READY"}


def get_top_referrers(limit: int = 10):
    """Get top referrers for VIP recognition"""
    if not check_api_configured():
        return {
            "status": "API_NOT_CONFIGURED",
            "vip_recognition_workflow": {
                "trigger": "Customer refers 3+ successful purchases",
                "action_1": "Add 'brand-advocate' tag (Shopify Flow)",
                "action_2": "Send VIP thank you email (Klaviyo)",
                "action_3": "Upgrade loyalty tier bonus"
            }
        }

    # TODO: Implement when API configured
    return {"status": "READY", "limit": limit}


def generate_referral_report():
    """Generate comprehensive referral report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "program_status": get_referral_status(),
        "flywheel_coverage": {
            "phase": "ADVOCACY",
            "current_scripts": 2,  # sync_loox_reviews.py + manage_referrals.py
            "target_scripts": 3,   # + collect_ugc.py
            "coverage": "67%"
        },
        "integration_map": {
            "loox_referrals": "Primary referral engine",
            "shopify_flow": "Loyalty tier tagging (VIP bonus)",
            "klaviyo": "Email promotion (Day 30 post-purchase)"
        },
        "setup_checklist": [
            {"task": "Enable Loox referrals", "status": "MANUAL - Check Loox Admin"},
            {"task": "Configure incentives", "status": "MANUAL - $10/$15%"},
            {"task": "Add API key to .env", "status": "PENDING"},
            {"task": "Create Klaviyo referral email", "status": "PENDING"},
            {"task": "Add VIP bonus in Shopify Flow", "status": "PENDING"}
        ]
    }
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Referral Program Management - Phase 4 ADVOCACY Automation"
    )
    parser.add_argument(
        '--mode',
        choices=['status', 'performance', 'top-referrers', 'report'],
        default='status',
        help='Operation mode'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Limit for top-referrers mode'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("REFERRAL PROGRAM MANAGEMENT - PHASE 4 ADVOCACY")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)

    if args.mode == 'status':
        result = get_referral_status()
        print("\nReferral Program Status:")
        print(json.dumps(result, indent=2))

    elif args.mode == 'performance':
        result = get_referral_performance()
        print("\nReferral Performance Metrics:")
        print(json.dumps(result, indent=2))

    elif args.mode == 'top-referrers':
        result = get_top_referrers(args.limit)
        print(f"\nTop {args.limit} Referrers:")
        print(json.dumps(result, indent=2))

    elif args.mode == 'report':
        result = generate_referral_report()
        print("\nComprehensive Referral Report:")
        print(json.dumps(result, indent=2))

    print("\n" + "=" * 70)
    print("Flywheel Stage: ADVOCACY (Phase 4)")
    print("Expected Impact: -40-60% CAC, +15-25% referral CVR")
    print("=" * 70)


if __name__ == "__main__":
    main()
