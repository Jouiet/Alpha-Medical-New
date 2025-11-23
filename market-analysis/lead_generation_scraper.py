#!/usr/bin/env python3
"""
LEAD GENERATION SCRAPER - Alpha Medical
Scrapes high-quality leads from Instagram, Facebook, TikTok, Google Maps using Apify

OBJECTIFS:
- Lead generation géolocalisé (Instagram, FB, TikTok, Google)
- Intelligence économique (tendances, prix, produits)
- Profiling par persona (Office Workers, Seniors, Athletes, Beauty/Wellness)
- PAS d'influenceurs - LEADS QUALIFIÉS uniquement

Features:
- Instagram: Scrape profiles, posts, hashtags by location/demographic
- Facebook: Scrape pages, groups, marketplace by interest
- TikTok: Scrape creators, hashtags, trending content
- Google Maps: Scrape local businesses (clinics, physio centers, gyms)
- Trending Products: Monitor trending health/wellness products

Usage:
    # Lead generation par platform
    python3 lead_generation_scraper.py --instagram --location "New York" --demographic "seniors"
    python3 lead_generation_scraper.py --facebook --interest "back pain relief"
    python3 lead_generation_scraper.py --tiktok --hashtag "kneepainarth
    python3 lead_generation_scraper.py --google-maps --location "Los Angeles" --category "physical therapy"

    # Full lead generation workflow
    python3 lead_generation_scraper.py --full-lead-gen --persona "seniors"
    python3 lead_generation_scraper.py --trending-products --category "knee-support"

Environment:
    APIFY_API_TOKEN=<your_apify_token_here>
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from collections import defaultdict


# Configuration
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "")
if not APIFY_API_TOKEN:
    raise ValueError("APIFY_API_TOKEN environment variable not set. Add it to .env file")
APIFY_API_BASE = "https://api.apify.com/v2"

# Apify Actor IDs for Lead Generation (CORRECTED - verified Nov 2025)
LEAD_ACTORS = {
    # Social Media Scrapers
    "instagram_scraper": "apify/instagram-scraper",  # General Instagram scraper
    "instagram_profile": "apify/instagram-profile-scraper",  # Profile scraper
    "instagram_hashtag": "apify/instagram-hashtag-scraper",  # Hashtag posts
    "instagram_post": "apify/instagram-post-scraper",  # Post details + comments

    # Google Maps
    "google_maps": "compass/crawler-google-places",  # Google Maps businesses (CORRECTED)

    # Note: TikTok/Facebook actors may require different IDs - verify before use
    "tiktok_profile": "apify/tiktok-scraper",  # TikTok scraper
    "facebook_pages": "apify/facebook-pages-scraper",  # Pages scraper
}

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
LEADS_DIR = SCRIPT_DIR / "leads"
TRENDS_DIR = SCRIPT_DIR / "trends"
REPORTS_DIR = SCRIPT_DIR / "reports"

# Alpha Medical Personas (from market_analysis_scraper.py)
PERSONAS = {
    "office-workers": {
        "age_range": "25-55",
        "demographics": ["office workers", "desk workers", "remote workers"],
        "pain_points": ["back pain", "neck pain", "posture", "shoulder pain"],
        "interests": ["ergonomics", "posture correction", "office wellness"],
        "categories": ["posture-support", "pain-relief-recovery"],
        "locations": ["New York", "San Francisco", "Los Angeles", "Chicago", "Seattle", "Austin"],
        "instagram_hashtags": [
            "#deskjobpain", "#officeposture", "#backpainrelief",
            "#neckpainrelief", "#workfromhomepain", "#ergonomics"
        ],
        "facebook_interests": [
            "back pain relief", "posture correction", "office wellness",
            "ergonomic solutions", "desk job health"
        ],
        "tiktok_hashtags": [
            "#deskjobpain", "#posturecheck", "#backpain", "#officelife"
        ]
    },

    "seniors": {
        "age_range": "65+",
        "demographics": ["seniors", "elderly", "retired", "grandparents"],
        "pain_points": ["arthritis", "knee pain", "mobility", "chronic pain", "joint pain"],
        "interests": ["arthritis relief", "mobility aids", "senior health", "pain management"],
        "categories": ["pain-relief-recovery", "therapy-wellness"],
        "locations": ["Florida", "Arizona", "California", "Texas", "North Carolina"],
        "instagram_hashtags": [
            "#arthritisrelief", "#seniorhealth", "#kneepainrelief",
            "#arthritispain", "#jointpainrelief", "#seniorwellness"
        ],
        "facebook_interests": [
            "arthritis relief", "knee pain", "senior health",
            "mobility solutions", "chronic pain management"
        ],
        "tiktok_hashtags": [
            "#seniorhealth", "#arthritisrelief", "#kneepain", "#elderlywellness"
        ]
    },

    "athletes": {
        "age_range": "18-45",
        "demographics": ["athletes", "runners", "gym-goers", "sports enthusiasts"],
        "pain_points": ["sports injury", "recovery", "knee injury", "muscle pain"],
        "interests": ["sports recovery", "injury prevention", "athletic performance"],
        "categories": ["pain-relief-recovery", "therapy-wellness"],
        "locations": ["Los Angeles", "Miami", "Denver", "San Diego", "Portland"],
        "instagram_hashtags": [
            "#sportsrecovery", "#injuryprevention", "#athleterecovery",
            "#kneeinjury", "#runnerknee", "#sportsinjury"
        ],
        "facebook_interests": [
            "sports recovery", "injury prevention", "athletic training",
            "sports medicine", "recovery equipment"
        ],
        "tiktok_hashtags": [
            "#sportsrecovery", "#injuryprevention", "#athletictraining", "#recoverytools"
        ]
    },

    "beauty-wellness": {
        "age_range": "25-55",
        "demographics": ["beauty enthusiasts", "wellness seekers", "skincare lovers"],
        "pain_points": ["aging", "skin health", "facial care", "anti-aging"],
        "interests": ["LED therapy", "red light therapy", "anti-aging", "facial care"],
        "categories": ["therapy-wellness"],
        "locations": ["Los Angeles", "New York", "Miami", "Las Vegas", "San Francisco"],
        "instagram_hashtags": [
            "#ledtherapy", "#redlighttherapy", "#antiaging",
            "#ledmask", "#skincaredevice", "#beautytechnology"
        ],
        "facebook_interests": [
            "LED therapy", "red light therapy", "anti-aging skincare",
            "beauty devices", "facial care technology"
        ],
        "tiktok_hashtags": [
            "#ledmask", "#redlighttherapy", "#antiaging", "#beautygadgets"
        ]
    },

    "post-surgery": {
        "age_range": "35-75",
        "demographics": ["post-surgery patients", "rehabilitation", "injury recovery"],
        "pain_points": ["post-op recovery", "rehabilitation", "mobility restoration"],
        "interests": ["rehabilitation", "physical therapy", "recovery equipment"],
        "categories": ["pain-relief-recovery", "posture-support"],
        "locations": ["All major cities with hospitals"],
        "instagram_hashtags": [
            "#postoprecovery", "#rehabilitation", "#physicaltherapy",
            "#surgeryrecovery", "#recoveryjourney"
        ],
        "facebook_interests": [
            "post-surgery recovery", "rehabilitation equipment",
            "physical therapy", "mobility restoration"
        ],
        "tiktok_hashtags": [
            "#recoveryjourney", "#postsurgery", "#rehabilitation", "#physicaltherapy"
        ]
    }
}


class ApifyLeadScraper:
    """Scrape leads from social media and local sources using Apify"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        })

    def scrape_instagram_hashtag(
        self,
        hashtags: List[str],
        max_posts: int = 50
    ) -> List[Dict]:
        """
        Scrape Instagram posts by hashtags

        Args:
            hashtags: List of hashtags (e.g., ["kneepainarth", "backpainrelief"])
            max_posts: Maximum posts per hashtag

        Returns:
            List of post dictionaries with engagement data
        """

        actor_id = LEAD_ACTORS["instagram_hashtag"].replace('/', '~')  # Fix format
        run_url = f"{APIFY_API_BASE}/acts/{actor_id}/runs?token={self.api_token}"

        # Build hashtag URLs
        hashtag_urls = [f"https://www.instagram.com/explore/tags/{tag.replace('#', '')}/"
                       for tag in hashtags]

        actor_input = {
            "hashtags": hashtags,  # Use hashtag names directly
            "resultsLimit": max_posts,
            "addParentData": False
        }

        print(f"\n📸 Scraping Instagram Hashtags: {', '.join(hashtags)}")
        print(f"   Max posts per hashtag: {max_posts}")

        response = self.session.post(run_url, json=actor_input)

        if response.status_code != 201:
            print(f"❌ Failed to start actor: {response.status_code}")
            return []

        run_data = response.json()['data']
        run_id = run_data['id']

        print(f"   Run ID: {run_id}")

        # Wait for completion
        completed_run = self._wait_for_run(run_id)
        if not completed_run:
            return []

        # Get dataset
        dataset_id = completed_run['defaultDatasetId']
        posts = self._get_dataset_items(dataset_id)

        print(f"✅ Scraped {len(posts)} Instagram posts")

        return posts

    def scrape_instagram_profile(
        self,
        usernames: List[str],
        max_posts: int = 30
    ) -> List[Dict]:
        """
        Scrape Instagram profiles and their posts

        Args:
            usernames: List of Instagram usernames
            max_posts: Maximum posts per profile

        Returns:
            List of profile + posts data
        """

        actor_id = LEAD_ACTORS["instagram_profile"]
        run_url = f"{APIFY_API_BASE}/acts/{actor_id}/runs"

        # Build profile URLs
        profile_urls = [f"https://www.instagram.com/{username}/" for username in usernames]

        actor_input = {
            "directUrls": profile_urls,
            "resultsLimit": max_posts,
            "proxyConfiguration": {"useApifyProxy": True}
        }

        print(f"\n📸 Scraping Instagram Profiles: {', '.join(usernames)}")
        print(f"   Max posts per profile: {max_posts}")

        response = self.session.post(run_url, json=actor_input)

        if response.status_code != 201:
            print(f"❌ Failed to start actor: {response.status_code}")
            return []

        run_data = response.json()['data']
        run_id = run_data['id']

        # Wait for completion
        completed_run = self._wait_for_run(run_id)
        if not completed_run:
            return []

        # Get dataset
        dataset_id = completed_run['defaultDatasetId']
        profiles = self._get_dataset_items(dataset_id)

        print(f"✅ Scraped {len(profiles)} Instagram profiles")

        return profiles

    def scrape_facebook_pages(
        self,
        page_urls: List[str],
        max_posts: int = 50
    ) -> List[Dict]:
        """
        Scrape Facebook pages and posts

        Args:
            page_urls: List of Facebook page URLs
            max_posts: Maximum posts per page

        Returns:
            List of page + posts data
        """

        actor_id = LEAD_ACTORS["facebook_pages"]
        run_url = f"{APIFY_API_BASE}/acts/{actor_id}/runs"

        actor_input = {
            "startUrls": [{"url": url} for url in page_urls],
            "maxPosts": max_posts,
            "proxyConfiguration": {"useApifyProxy": True}
        }

        print(f"\n👥 Scraping Facebook Pages: {len(page_urls)} pages")
        print(f"   Max posts per page: {max_posts}")

        response = self.session.post(run_url, json=actor_input)

        if response.status_code != 201:
            print(f"❌ Failed to start actor: {response.status_code}")
            return []

        run_data = response.json()['data']
        run_id = run_data['id']

        # Wait for completion
        completed_run = self._wait_for_run(run_id)
        if not completed_run:
            return []

        # Get dataset
        dataset_id = completed_run['defaultDatasetId']
        pages = self._get_dataset_items(dataset_id)

        print(f"✅ Scraped {len(pages)} Facebook pages")

        return pages

    def scrape_tiktok_hashtag(
        self,
        hashtags: List[str],
        max_videos: int = 50
    ) -> List[Dict]:
        """
        Scrape TikTok videos by hashtags

        Args:
            hashtags: List of hashtags
            max_videos: Maximum videos per hashtag

        Returns:
            List of video dictionaries
        """

        actor_id = LEAD_ACTORS["tiktok_hashtag"]
        run_url = f"{APIFY_API_BASE}/acts/{actor_id}/runs"

        # Build hashtag URLs
        hashtag_urls = [f"https://www.tiktok.com/tag/{tag.replace('#', '')}"
                       for tag in hashtags]

        actor_input = {
            "hashtags": hashtag_urls,
            "resultsPerPage": max_videos,
            "proxyConfiguration": {"useApifyProxy": True}
        }

        print(f"\n🎵 Scraping TikTok Hashtags: {', '.join(hashtags)}")
        print(f"   Max videos per hashtag: {max_videos}")

        response = self.session.post(run_url, json=actor_input)

        if response.status_code != 201:
            print(f"❌ Failed to start actor: {response.status_code}")
            return []

        run_data = response.json()['data']
        run_id = run_data['id']

        # Wait for completion
        completed_run = self._wait_for_run(run_id)
        if not completed_run:
            return []

        # Get dataset
        dataset_id = completed_run['defaultDatasetId']
        videos = self._get_dataset_items(dataset_id)

        print(f"✅ Scraped {len(videos)} TikTok videos")

        return videos

    def scrape_google_maps(
        self,
        search_query: str,
        location: str,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Scrape Google Maps for local businesses

        Args:
            search_query: Search query (e.g., "physical therapy clinic")
            location: Location (e.g., "New York, NY")
            max_results: Maximum results

        Returns:
            List of business dictionaries with contact info
        """

        actor_id = LEAD_ACTORS["google_maps"].replace('/', '~')  # Fix format
        run_url = f"{APIFY_API_BASE}/acts/{actor_id}/runs?token={self.api_token}"

        actor_input = {
            "searchStringsArray": [f"{search_query} in {location}"],
            "maxCrawledPlaces": max_results,
            "language": "en"
        }

        print(f"\n🗺️  Scraping Google Maps: '{search_query}' in '{location}'")
        print(f"   Max results: {max_results}")

        response = self.session.post(run_url, json=actor_input)

        if response.status_code != 201:
            print(f"❌ Failed to start actor: {response.status_code}")
            return []

        run_data = response.json()['data']
        run_id = run_data['id']

        # Wait for completion
        completed_run = self._wait_for_run(run_id)
        if not completed_run:
            return []

        # Get dataset
        dataset_id = completed_run['defaultDatasetId']
        businesses = self._get_dataset_items(dataset_id)

        print(f"✅ Scraped {len(businesses)} Google Maps businesses")

        return businesses

    def _wait_for_run(self, run_id: str, timeout: int = 600) -> Optional[Dict]:
        """Wait for Apify actor run to complete"""

        status_url = f"{APIFY_API_BASE}/actor-runs/{run_id}"
        start_time = time.time()

        print(f"   ⏳ Waiting for completion...", end='')

        while True:
            if time.time() - start_time > timeout:
                print(f" ❌ Timeout after {timeout}s")
                return None

            response = self.session.get(status_url)
            if response.status_code != 200:
                print(f" ❌ Status check failed: {response.status_code}")
                return None

            run_data = response.json()['data']
            status = run_data['status']

            if status == 'SUCCEEDED':
                duration = run_data.get('stats', {}).get('durationMillis', 0) / 1000
                print(f" ✅ ({duration:.1f}s)")
                return run_data

            elif status == 'FAILED':
                print(f" ❌ Run failed")
                return None

            elif status in ['RUNNING', 'READY']:
                elapsed = int(time.time() - start_time)
                print(f"\r   ⏳ Waiting for completion... {elapsed}s", end='')
                time.sleep(5)

            else:
                time.sleep(5)

    def _get_dataset_items(self, dataset_id: str) -> List[Dict]:
        """Retrieve items from Apify dataset"""

        dataset_url = f"{APIFY_API_BASE}/datasets/{dataset_id}/items"
        response = self.session.get(dataset_url)

        if response.status_code != 200:
            return []

        return response.json()


class LeadAnalyzer:
    """Analyze and qualify leads from scraped data"""

    def __init__(self, leads_dir: Path):
        self.leads_dir = leads_dir
        self.leads_dir.mkdir(parents=True, exist_ok=True)

    def qualify_instagram_leads(
        self,
        posts: List[Dict],
        min_engagement: int = 100
    ) -> List[Dict]:
        """
        Qualify Instagram posts as potential lead sources

        Filters:
        - Minimum engagement (likes + comments)
        - Relevant content
        - Active accounts

        Returns:
            List of qualified lead dictionaries
        """

        qualified_leads = []

        for post in posts:
            engagement = post.get('likesCount', 0) + post.get('commentsCount', 0)

            if engagement >= min_engagement:
                lead = {
                    "platform": "instagram",
                    "type": "post",
                    "url": post.get('url', ''),
                    "username": post.get('ownerUsername', ''),
                    "caption": post.get('caption', ''),
                    "engagement": engagement,
                    "likes": post.get('likesCount', 0),
                    "comments": post.get('commentsCount', 0),
                    "timestamp": post.get('timestamp', ''),
                    "quality_score": self._calculate_quality_score(post)
                }

                qualified_leads.append(lead)

        # Sort by quality score
        qualified_leads.sort(key=lambda x: x['quality_score'], reverse=True)

        return qualified_leads

    def qualify_google_maps_leads(
        self,
        businesses: List[Dict],
        min_rating: float = 4.0
    ) -> List[Dict]:
        """
        Qualify Google Maps businesses as B2B leads

        Filters:
        - Minimum rating
        - Has contact info
        - Active business

        Returns:
            List of qualified B2B lead dictionaries
        """

        qualified_leads = []

        for business in businesses:
            rating = business.get('totalScore') or 0  # Handle None

            # Must have rating above threshold and contact info
            if rating >= min_rating and (business.get('phone') or business.get('website')):
                lead = {
                    "platform": "google_maps",
                    "type": "b2b",
                    "name": business.get('title', ''),
                    "address": business.get('address', ''),
                    "phone": business.get('phone', ''),
                    "website": business.get('website', ''),
                    "email": business.get('email', ''),
                    "rating": rating,
                    "review_count": business.get('reviewsCount', 0),
                    "category": business.get('categoryName', ''),
                    "quality_score": rating * (1 + business.get('reviewsCount', 0) / 100)
                }

                qualified_leads.append(lead)

        # Sort by quality score
        qualified_leads.sort(key=lambda x: x['quality_score'], reverse=True)

        return qualified_leads

    def _calculate_quality_score(self, post: Dict) -> float:
        """
        Calculate quality score for Instagram post

        Factors:
        - Engagement rate
        - Recency
        - Authenticity (comments/likes ratio)
        """

        likes = post.get('likesCount', 0)
        comments = post.get('commentsCount', 0)

        # Engagement score
        engagement = likes + (comments * 10)  # Comments weighted higher

        # Authenticity score (comments should be ~5-10% of likes)
        if likes > 0:
            comment_ratio = comments / likes
            authenticity = 1.0 if 0.05 <= comment_ratio <= 0.15 else 0.5
        else:
            authenticity = 0.5

        # Recency score (placeholder - would need timestamp parsing)
        recency = 1.0

        quality_score = (engagement * authenticity * recency) / 100

        return quality_score

    def save_leads(
        self,
        leads: List[Dict],
        persona: str,
        platform: str
    ) -> Path:
        """Save qualified leads to JSON file"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"leads_{persona}_{platform}_{timestamp}.json"
        filepath = self.leads_dir / persona / filename

        filepath.parent.mkdir(parents=True, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(leads, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Saved {len(leads)} leads to: {filepath}")

        return filepath

    def generate_lead_report(
        self,
        persona: str,
        instagram_leads: List[Dict] = None,
        facebook_leads: List[Dict] = None,
        tiktok_leads: List[Dict] = None,
        maps_leads: List[Dict] = None
    ) -> Dict:
        """Generate comprehensive lead generation report"""

        report = {
            "persona": persona,
            "analysis_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_leads": 0,
            "by_platform": {},
            "top_leads": [],
            "summary": {}
        }

        all_leads = []

        if instagram_leads:
            report["by_platform"]["instagram"] = len(instagram_leads)
            all_leads.extend(instagram_leads)

        if facebook_leads:
            report["by_platform"]["facebook"] = len(facebook_leads)
            all_leads.extend(facebook_leads)

        if tiktok_leads:
            report["by_platform"]["tiktok"] = len(tiktok_leads)
            all_leads.extend(tiktok_leads)

        if maps_leads:
            report["by_platform"]["google_maps"] = len(maps_leads)
            all_leads.extend(maps_leads)

        report["total_leads"] = len(all_leads)

        # Top 10 leads by quality score
        all_leads.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        report["top_leads"] = all_leads[:10]

        # Summary insights
        report["summary"]["avg_quality_score"] = (
            sum(lead.get('quality_score', 0) for lead in all_leads) / len(all_leads)
            if all_leads else 0
        )

        return report

    def print_lead_summary(self, report: Dict):
        """Print lead generation summary to console"""

        print("\n" + "=" * 70)
        print(f"LEAD GENERATION REPORT: {report['persona'].upper()}")
        print("=" * 70)

        print(f"\n📊 Total Leads Generated: {report['total_leads']}")

        print(f"\n📱 By Platform:")
        for platform, count in report['by_platform'].items():
            print(f"   • {platform.capitalize()}: {count} leads")

        print(f"\n💡 Insights:")
        print(f"   • Average Quality Score: {report['summary']['avg_quality_score']:.2f}")

        print(f"\n🏆 TOP 5 LEADS:")
        for i, lead in enumerate(report['top_leads'][:5], 1):
            platform = lead.get('platform', 'unknown')

            if platform == 'instagram':
                print(f"   {i}. @{lead.get('username', 'N/A')} | "
                      f"Engagement: {lead.get('engagement', 0):,} | "
                      f"Score: {lead.get('quality_score', 0):.2f}")

            elif platform == 'google_maps':
                print(f"   {i}. {lead.get('name', 'N/A')} | "
                      f"Rating: {lead.get('rating', 0):.1f} | "
                      f"Score: {lead.get('quality_score', 0):.2f}")

        print("\n" + "=" * 70)


def full_lead_generation_workflow(
    scraper: ApifyLeadScraper,
    analyzer: LeadAnalyzer,
    persona: str
) -> Dict:
    """
    Full lead generation workflow for a specific persona

    Workflow:
    1. Scrape Instagram hashtags relevant to persona
    2. Scrape TikTok hashtags relevant to persona
    3. Scrape Google Maps for B2B leads (clinics, gyms, etc.)
    4. Qualify and analyze all leads
    5. Generate comprehensive report

    Args:
        scraper: ApifyLeadScraper instance
        analyzer: LeadAnalyzer instance
        persona: Persona key (e.g., "seniors", "office-workers")

    Returns:
        Lead generation report dictionary
    """

    if persona not in PERSONAS:
        print(f"❌ Unknown persona: {persona}")
        print(f"   Available personas: {', '.join(PERSONAS.keys())}")
        return None

    persona_data = PERSONAS[persona]

    print("=" * 70)
    print(f"FULL LEAD GENERATION WORKFLOW: {persona.upper()}")
    print("=" * 70)
    print(f"\nTarget Demographics: {', '.join(persona_data['demographics'])}")
    print(f"Age Range: {persona_data['age_range']}")
    print(f"Pain Points: {', '.join(persona_data['pain_points'])}")
    print("=" * 70)

    # 1. Instagram Lead Generation
    print(f"\n{'='*70}")
    print("PHASE 1: INSTAGRAM LEAD GENERATION")
    print(f"{'='*70}")

    instagram_posts = scraper.scrape_instagram_hashtag(
        hashtags=persona_data['instagram_hashtags'][:3],  # Top 3 hashtags
        max_posts=30
    )

    instagram_leads = analyzer.qualify_instagram_leads(instagram_posts, min_engagement=50)

    if instagram_leads:
        analyzer.save_leads(instagram_leads, persona, "instagram")

    # 2. TikTok Lead Generation
    print(f"\n{'='*70}")
    print("PHASE 2: TIKTOK LEAD GENERATION")
    print(f"{'='*70}")

    tiktok_videos = scraper.scrape_tiktok_hashtag(
        hashtags=persona_data['tiktok_hashtags'][:3],  # Top 3 hashtags
        max_videos=30
    )

    # TikTok leads (simplified - similar to Instagram)
    tiktok_leads = []  # Would need similar qualification logic

    # 3. Google Maps B2B Lead Generation (for personas with B2B potential)
    print(f"\n{'='*70}")
    print("PHASE 3: GOOGLE MAPS B2B LEAD GENERATION")
    print(f"{'='*70}")

    maps_leads = []

    # B2B targets vary by persona
    if persona == "seniors":
        # Target senior centers, retirement communities, physical therapy clinics
        for location in persona_data['locations'][:2]:  # Top 2 locations
            businesses = scraper.scrape_google_maps(
                search_query="senior center",
                location=location,
                max_results=20
            )
            maps_leads.extend(analyzer.qualify_google_maps_leads(businesses, min_rating=4.0))

    elif persona == "athletes":
        # Target gyms, sports clinics, athletic training centers
        for location in persona_data['locations'][:2]:
            businesses = scraper.scrape_google_maps(
                search_query="sports medicine clinic",
                location=location,
                max_results=20
            )
            maps_leads.extend(analyzer.qualify_google_maps_leads(businesses, min_rating=4.0))

    elif persona == "office-workers":
        # Target corporate wellness centers, ergonomic consultants
        for location in persona_data['locations'][:2]:
            businesses = scraper.scrape_google_maps(
                search_query="chiropractic office",
                location=location,
                max_results=20
            )
            maps_leads.extend(analyzer.qualify_google_maps_leads(businesses, min_rating=4.0))

    if maps_leads:
        analyzer.save_leads(maps_leads, persona, "google_maps")

    # 4. Generate Comprehensive Report
    print(f"\n{'='*70}")
    print("GENERATING COMPREHENSIVE REPORT")
    print(f"{'='*70}")

    report = analyzer.generate_lead_report(
        persona=persona,
        instagram_leads=instagram_leads,
        tiktok_leads=tiktok_leads,
        maps_leads=maps_leads
    )

    # Save report
    report_file = REPORTS_DIR / f"lead_report_{persona}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Report saved: {report_file}")

    # Print summary
    analyzer.print_lead_summary(report)

    return report


def main():
    """CLI entry point"""

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable commands:")
        print("\n  LEAD GENERATION:")
        print("    --full-lead-gen --persona <persona>    Full lead gen workflow for persona")
        print("    --instagram --hashtag <hashtag>        Scrape Instagram hashtag")
        print("    --tiktok --hashtag <hashtag>           Scrape TikTok hashtag")
        print("    --google-maps --query <query> --location <location>")
        print("\n  PERSONAS:")
        print("    " + ", ".join(PERSONAS.keys()))
        sys.exit(1)

    command = sys.argv[1]

    scraper = ApifyLeadScraper(APIFY_API_TOKEN)
    analyzer = LeadAnalyzer(LEADS_DIR)

    if command == "--full-lead-gen":
        if "--persona" not in sys.argv:
            print("❌ Error: --persona required")
            print(f"   Available personas: {', '.join(PERSONAS.keys())}")
            sys.exit(1)

        persona_idx = sys.argv.index("--persona") + 1
        persona = sys.argv[persona_idx]

        full_lead_generation_workflow(scraper, analyzer, persona)

    elif command == "--instagram":
        if "--hashtag" not in sys.argv:
            print("❌ Error: --hashtag required")
            sys.exit(1)

        hashtag_idx = sys.argv.index("--hashtag") + 1
        hashtag = sys.argv[hashtag_idx]

        posts = scraper.scrape_instagram_hashtag([hashtag], max_posts=50)
        leads = analyzer.qualify_instagram_leads(posts)

        print(f"\n✅ Generated {len(leads)} qualified leads from Instagram")

        # Save leads
        analyzer.save_leads(leads, "general", "instagram")

    elif command == "--tiktok":
        if "--hashtag" not in sys.argv:
            print("❌ Error: --hashtag required")
            sys.exit(1)

        hashtag_idx = sys.argv.index("--hashtag") + 1
        hashtag = sys.argv[hashtag_idx]

        videos = scraper.scrape_tiktok_hashtag([hashtag], max_videos=50)

        print(f"\n✅ Scraped {len(videos)} TikTok videos")

    elif command == "--google-maps":
        if "--query" not in sys.argv or "--location" not in sys.argv:
            print("❌ Error: --query and --location required")
            sys.exit(1)

        query_idx = sys.argv.index("--query") + 1
        location_idx = sys.argv.index("--location") + 1

        query = sys.argv[query_idx]
        location = sys.argv[location_idx]

        businesses = scraper.scrape_google_maps(query, location, max_results=100)
        leads = analyzer.qualify_google_maps_leads(businesses)

        print(f"\n✅ Generated {len(leads)} qualified B2B leads from Google Maps")

        # Save leads
        analyzer.save_leads(leads, "general", "google_maps")

    else:
        print(f"❌ Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
