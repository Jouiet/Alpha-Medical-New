#!/usr/bin/env python3
"""
PHASE 4 ADVOCACY - UGC (User-Generated Content) Collection
Collects and manages customer-generated content for social proof

Flywheel Stage: ADVOCACY (Customer → Brand Ambassador)
Expected Impact: 3-5x higher engagement than brand content

UGC Sources:
1. Loox photo/video reviews (PRIMARY)
2. Instagram hashtag mentions (#AlphaMedicalCare)
3. Customer testimonials (email/chat)
4. Video testimonials (post-purchase request)

Integration:
- Loox: Automatic photo/video review collection
- Klaviyo: Email request for UGC (Day 14 post-delivery)
- Shopify Flow: Tag customers who submit UGC as 'brand-advocate'

Usage:
    python3 scripts/advocacy/collect_ugc.py --mode status
    python3 scripts/advocacy/collect_ugc.py --mode sources
    python3 scripts/advocacy/collect_ugc.py --mode campaign-plan
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

# UGC Campaign Configuration
UGC_CONFIG = {
    "instagram_hashtag": "#AlphaMedicalCare",
    "incentive_photo": "10% discount next purchase",
    "incentive_video": "15% discount next purchase",
    "contest_prize": "$50 gift card monthly",
    "target_monthly_ugc": 20  # pieces of UGC
}


def get_ugc_status():
    """Get current UGC collection status"""
    return {
        "loox_api": "CONFIGURED" if LOOX_API_KEY else "NOT_CONFIGURED",
        "ugc_sources": {
            "loox_reviews": {
                "status": "ACTIVE" if LOOX_API_KEY else "NEEDS_API_KEY",
                "collection_method": "Automatic post-purchase",
                "incentive": UGC_CONFIG["incentive_photo"]
            },
            "instagram": {
                "status": "MANUAL",
                "hashtag": UGC_CONFIG["instagram_hashtag"],
                "collection_method": "Manual search + permission request"
            },
            "email_testimonials": {
                "status": "PASSIVE",
                "collection_method": "Customer support interactions"
            },
            "video_testimonials": {
                "status": "NOT_CONFIGURED",
                "recommended_tool": "Loox video reviews OR VideoAsk"
            }
        },
        "flywheel_impact": {
            "engagement_lift": "3-5x vs brand content",
            "trust_increase": "+79% (Gen Z/Millennials prefer authentic)",
            "ad_performance": "4x CTR, 50% lower CPC"
        }
    }


def get_ugc_sources_detail():
    """Get detailed information about UGC sources"""
    return {
        "primary_source": {
            "name": "Loox Photo/Video Reviews",
            "priority": 1,
            "automation_level": "HIGH",
            "setup_steps": [
                "1. Configure Loox review request timing (Day 14)",
                "2. Enable photo/video uploads",
                "3. Set incentives (10% photo, 15% video)",
                "4. Auto-publish 4-5 star reviews",
                "5. Integrate with Klaviyo for review request emails"
            ],
            "integration": {
                "klaviyo_flow": "Product Review / Cross-Sell - Standard",
                "flow_id": "TxcQgE",
                "trigger": "Fulfilled Order"
            }
        },
        "secondary_source": {
            "name": "Instagram Hashtag Campaign",
            "priority": 2,
            "automation_level": "LOW",
            "setup_steps": [
                "1. Define hashtag: #AlphaMedicalCare",
                "2. Promote hashtag in post-purchase email",
                "3. Run monthly 'Best Post' contest ($50 prize)",
                "4. Manually curate + request permission",
                "5. Feature on website + social"
            ],
            "promotion": {
                "email": "Klaviyo post-purchase (Day 30)",
                "packaging_insert": "Include hashtag on thank you card",
                "website": "Display feed on homepage"
            }
        },
        "tertiary_source": {
            "name": "Video Testimonials",
            "priority": 3,
            "automation_level": "MEDIUM",
            "options": [
                {
                    "tool": "Loox Video Reviews",
                    "cost": "Included in Loox plan",
                    "effort": "LOW (native integration)"
                },
                {
                    "tool": "VideoAsk",
                    "cost": "$24/mo",
                    "effort": "MEDIUM (separate tool)"
                }
            ]
        }
    }


def generate_ugc_campaign_plan():
    """Generate a UGC collection campaign plan"""
    return {
        "campaign_name": "Alpha Medical UGC Collection Campaign",
        "timeline": "Ongoing (monthly refresh)",
        "target": f"{UGC_CONFIG['target_monthly_ugc']} UGC pieces/month",

        "phase_1_foundation": {
            "duration": "Week 1",
            "tasks": [
                {"task": "Configure Loox photo/video reviews", "owner": "USER", "time": "30 min"},
                {"task": "Set review incentives (10%/15%)", "owner": "USER", "time": "10 min"},
                {"task": "Create Klaviyo review request email", "owner": "USER", "time": "20 min"},
                {"task": "Define Instagram hashtag", "owner": "DONE", "result": UGC_CONFIG["instagram_hashtag"]}
            ]
        },

        "phase_2_launch": {
            "duration": "Week 2-4",
            "tasks": [
                {"task": "Announce hashtag in post-purchase email", "owner": "USER", "time": "15 min"},
                {"task": "Launch 'Best Review' monthly contest", "owner": "USER", "time": "30 min"},
                {"task": "Create UGC showcase section on homepage", "owner": "USER", "time": "1-2 hours"}
            ]
        },

        "phase_3_amplification": {
            "duration": "Month 2+",
            "tasks": [
                {"task": "Feature best UGC in ads (permission required)", "owner": "USER", "time": "ongoing"},
                {"task": "Tag UGC contributors as 'brand-advocate'", "owner": "AUTOMATION", "system": "Shopify Flow"},
                {"task": "Send VIP thank you to advocates", "owner": "AUTOMATION", "system": "Klaviyo"}
            ]
        },

        "automation_workflow": {
            "trigger": "Customer submits 5-star photo/video review",
            "actions": [
                "1. Loox: Auto-publish review",
                "2. Shopify Flow: Add 'brand-advocate' tag",
                "3. Klaviyo: Track 'ugc_submitted' event",
                "4. Klaviyo: Send VIP thank you email",
                "5. Optional: Upgrade loyalty tier"
            ]
        },

        "kpis": {
            "monthly_ugc_target": UGC_CONFIG["target_monthly_ugc"],
            "photo_review_rate": "30-50% of reviews",
            "instagram_mentions": "10+/month",
            "ugc_ad_performance": "4x CTR vs branded content"
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description="UGC Collection - Phase 4 ADVOCACY Automation"
    )
    parser.add_argument(
        '--mode',
        choices=['status', 'sources', 'campaign-plan', 'report'],
        default='status',
        help='Operation mode'
    )

    args = parser.parse_args()

    print("=" * 70)
    print("UGC COLLECTION - PHASE 4 ADVOCACY")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)

    if args.mode == 'status':
        result = get_ugc_status()
        print("\nUGC Collection Status:")
        print(json.dumps(result, indent=2))

    elif args.mode == 'sources':
        result = get_ugc_sources_detail()
        print("\nUGC Sources Detail:")
        print(json.dumps(result, indent=2))

    elif args.mode == 'campaign-plan':
        result = generate_ugc_campaign_plan()
        print("\nUGC Campaign Plan:")
        print(json.dumps(result, indent=2))

    elif args.mode == 'report':
        result = {
            "status": get_ugc_status(),
            "sources": get_ugc_sources_detail(),
            "campaign": generate_ugc_campaign_plan()
        }
        print("\nComprehensive UGC Report:")
        print(json.dumps(result, indent=2))

    print("\n" + "=" * 70)
    print("Flywheel Stage: ADVOCACY (Phase 4)")
    print("Expected Impact: 3-5x engagement, 4x ad CTR")
    print("=" * 70)


if __name__ == "__main__":
    main()
