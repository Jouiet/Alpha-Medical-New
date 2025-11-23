# MARKET ANALYSIS & LEAD GENERATION
**Alpha Medical - Apify Integration**

**Created:** 2025-11-23
**Purpose:** Automate market intelligence, competitor analysis, and influencer lead generation

---

## 📁 STRUCTURE

```
market-analysis/
├── market_analysis_scraper.py       # Sourcing + Competitive Pricing Analysis
├── influencer_lead_generation.py    # Instagram/TikTok Influencer Discovery
├── README.md                         # This file
├── data/                             # Raw scraped data (AliExpress, Google Shopping)
├── reports/                          # Market analysis reports (JSON)
└── leads/                            # Influencer leads (CSV for outreach)
    └── raw_data/                     # Raw Instagram/TikTok data
```

---

## 🎯 USE CASES

### 1. Sourcing + Competitive Pricing Analysis
**Script:** `market_analysis_scraper.py`
**Apify Actors:** AliExpress Scraper + Google Shopping Scraper

**What it does:**
- ✅ Scrapes AliExpress for supplier products (wholesale/sourcing)
- ✅ Scrapes Google Shopping for retail competitors
- ✅ Analyzes pricing positioning (Alpha Medical vs market)
- ✅ Generates comprehensive market analysis reports
- ✅ Tracks price changes over time

**Output:**
- `data/` - Raw JSON datasets
- `reports/` - Market analysis reports with insights

---

### 2. Influencer Lead Generation
**Script:** `influencer_lead_generation.py`
**Apify Actors:** Instagram Hashtag Scraper + Profile Scraper

**What it does:**
- ✅ Discovers micro-influencers via Instagram hashtags
- ✅ Filters by follower count (1K-100K = nano/micro tier)
- ✅ Calculates engagement rate
- ✅ Extracts contact info (email, website from bio)
- ✅ Categorizes by niche (arthritis, senior wellness, posture, health)
- ✅ Exports to CSV for outreach campaigns

**Output:**
- `leads/` - CSV files with qualified influencer leads
- `leads/raw_data/` - Raw Instagram post data

---

## 🚀 QUICK START

### Setup (One-time)

**1. Verify Apify API Token:**
```bash
curl "https://api.apify.com/v2/users/me/limits?token=YOUR_APIFY_API_TOKEN"
```

**2. Check your account:**
- Budget: $39/month
- Current usage: $0.0003 (almost nothing used)
- Status: ✅ Ready

---

## 📊 USE CASE 1: Market Analysis

### Run Full Analysis (All TOP 3 Products)

**Command:**
```bash
cd /Users/mac/Desktop/Alpha-Medical/market-analysis/

python3 market_analysis_scraper.py --full-analysis
```

**What happens:**
1. Scrapes AliExpress for "magnetic knee pads", "magnetic posture corrector", "lower back brace"
2. Scrapes Google Shopping for same keywords
3. Analyzes pricing for each product:
   - Min/Max/Average/Median competitor prices
   - Alpha Medical price vs market positioning
   - Price percentile (are you premium, mid-range, budget?)
4. Identifies top competitors (merchant names, product counts)
5. Generates JSON reports

**Time:** ~15-20 minutes (includes Apify scraping time)

**Output Example:**
```
reports/market_analysis_tourmaline-knee-pads_20251123_143022.json
reports/market_analysis_magnetic-posture-corrector_20251123_143845.json
reports/market_analysis_lower-back-brace_20251123_144512.json
```

---

### Scrape Specific Platform

**AliExpress Only:**
```bash
python3 market_analysis_scraper.py --aliexpress "magnetic knee pads"
```

**Google Shopping Only:**
```bash
python3 market_analysis_scraper.py --google-shopping "tourmaline knee support"
```

---

### Read Analysis Report

**Example report structure:**
```json
{
  "product": "Tourmaline Magnetic Knee Pads",
  "alpha_price": 55,
  "analysis_date": "2025-11-23 14:30:22",

  "aliexpress_analysis": {
    "total_products": 28,
    "min_price": 8.99,
    "max_price": 49.99,
    "avg_price": 23.45,
    "median_price": 21.50,
    "alpha_vs_avg": +31.55,
    "price_percentile": 89
  },

  "google_shopping_analysis": {
    "total_products": 45,
    "avg_price": 42.30,
    "alpha_vs_avg": +12.70,
    "top_merchants": {
      "Amazon": 15,
      "Walmart": 8,
      "eBay": 6
    }
  },

  "summary": {
    "aliexpress_positioning": "Alpha Medical price ($55) is 89th percentile on AliExpress. Average AliExpress price: $23.45",
    "google_shopping_positioning": "Alpha Medical price is $12.70 above average Google Shopping price ($42.30)"
  }
}
```

**Insights:**
- **AliExpress:** You're pricing at 89th percentile (premium vs wholesale)
- **Google Shopping:** You're $12.70 above retail average (premium positioning)
- **Strategy:** Premium product justified by self-heating tech, magnetic therapy

---

## 👥 USE CASE 2: Influencer Lead Generation

### Run Full Discovery (All Niches)

**Command:**
```bash
cd /Users/mac/Desktop/Alpha-Medical/market-analysis/

python3 influencer_lead_generation.py --full-discovery
```

**What happens:**
1. Scrapes Instagram hashtags for 4 niches:
   - **Arthritis Pain Relief:** #arthritisrelief, #kneepainrelief, #chronicpain
   - **Senior Wellness:** #seniorwellness, #seniorhealth, #activesenior
   - **Posture Wellness:** #posturecorrection, #backpainrelief, #deskjob
   - **Health Influencers:** #healthandwellness, #wellnessinfluencer

2. Extracts creator profiles from posts

3. Qualifies leads:
   - Follower count: 1,000 - 100,000 (nano/micro influencers)
   - Engagement rate: >1% (active audience)
   - Location: USA/Canada preferred (from bio)

4. Enriches data:
   - Calculates engagement rate
   - Categorizes tier (Nano $50-$200, Micro $200-$1000)
   - Extracts email/website from bio
   - Estimates cost per post

5. Exports to CSV

**Time:** ~30-45 minutes (4 niches × 7 hashtags each)

**Output Example:**
```
leads/leads_arthritis_pain_relief_20251123.csv    (23 leads)
leads/leads_senior_wellness_20251123.csv          (15 leads)
leads/leads_posture_wellness_20251123.csv         (31 leads)
leads/leads_health_influencers_20251123.csv       (42 leads)
leads/leads_all_niches_20251123.csv               (111 total leads)
```

---

### Discover for Specific Niche

**Arthritis/Pain Relief Only:**
```bash
python3 influencer_lead_generation.py --niche arthritis_pain_relief
```

**Senior Wellness Only:**
```bash
python3 influencer_lead_generation.py --niche senior_wellness
```

**Posture/Office Workers Only:**
```bash
python3 influencer_lead_generation.py --niche posture_wellness
```

**Available niches:**
- `arthritis_pain_relief`
- `senior_wellness`
- `posture_wellness`
- `health_influencers`

---

### Scrape Specific Hashtag

**Custom hashtag:**
```bash
python3 influencer_lead_generation.py --instagram-hashtag "kneepainrelief"
```

---

### Read Lead CSV

**CSV Structure:**
```csv
username,full_name,followers,engagement_rate,tier,estimated_cost_per_post,email,website,is_verified,biography,profile_url,discovered_date

arthritis_warrior_65,Sarah Johnson,8450,3.2,Nano (1K-10K),$50-$200,sarah@example.com,arthritisjourney.com,False,"Living with arthritis for 10 years. Sharing my journey. USA 🇺🇸",https://instagram.com/arthritis_warrior_65,2025-11-23

senior_wellness_coach,Mike Thompson,24300,2.8,Micro (10K-100K),$200-$1000,mike@wellnesscoach.com,seniorwellness.coach,True,"Helping seniors stay active. Certified trainer. Based in Florida",https://instagram.com/senior_wellness_coach,2025-11-23
```

**How to use:**
1. Open CSV in Excel/Google Sheets
2. Sort by engagement_rate (highest = best ROI)
3. Filter by tier (Nano = cheapest, most authentic)
4. Filter by email presence (easier outreach)
5. Reach out with UGC collaboration offer:
   - Send free product
   - Request authentic testimonial video (15-30 sec)
   - Offer $50-$200 for video rights (depending on tier)
   - Use their content in your video ads

**Sample Outreach:**
> Hi [Name],
>
> I came across your profile and love your content on [niche topic]. We're Alpha Medical, a wellness brand specializing in [product category].
>
> We'd love to send you our [Product Name] to try. If you genuinely love it, we'd offer $[amount] for the rights to use a short testimonial video (15-30 sec) in our ads.
>
> Interested? Let me know!

---

## 🔄 WORKFLOW EXAMPLES

### Workflow 1: Launch New Product - Full Market Research

**Goal:** Understand market before launching "Magnetic Posture Corrector"

**Steps:**
```bash
# 1. Analyze competitor pricing
python3 market_analysis_scraper.py --google-shopping "magnetic posture corrector"

# 2. Find wholesale/sourcing options
python3 market_analysis_scraper.py --aliexpress "magnetic posture corrector"

# 3. Read reports, set competitive price
# (Based on analysis: competitors avg $42, set Alpha at $50 = premium)

# 4. Find influencers for launch
python3 influencer_lead_generation.py --niche posture_wellness

# 5. Reach out to TOP 10 micro-influencers for UGC
# 6. Create video ads using UGC + templates
# 7. Launch campaign
```

---

### Workflow 2: Quarterly Price Monitoring

**Goal:** Track competitor pricing every 3 months

**Steps:**
```bash
# Run full analysis quarterly
python3 market_analysis_scraper.py --full-analysis

# Compare reports over time:
# - reports/market_analysis_tourmaline-knee-pads_20251123.json
# - reports/market_analysis_tourmaline-knee-pads_20260223.json
# - reports/market_analysis_tourmaline-knee-pads_20260523.json

# Identify trends: Are competitors raising/lowering prices?
# Adjust Alpha Medical pricing accordingly
```

---

### Workflow 3: Continuous Influencer Recruitment

**Goal:** Build ongoing UGC creator pipeline

**Steps:**
```bash
# Monthly: Discover new influencers
python3 influencer_lead_generation.py --full-discovery

# Results in:
# - leads/leads_all_niches_20251123.csv (111 leads)
# - leads/leads_all_niches_20251223.csv (94 leads)
# - leads/leads_all_niches_20260123.csv (102 leads)

# Each month:
# 1. Reach out to TOP 20 new leads
# 2. Send products to 5-10 who respond
# 3. Collect 3-5 UGC videos
# 4. Use in video ads (VIDEO_ADS_CREATION_PLAYBOOK.md)
```

---

## 📈 COST ANALYSIS

### Apify Costs

**Your Account:**
- Budget: $39/month
- Current usage: $0.0003

**Actor Costs (Estimates):**
- **AliExpress Scraper:** ~$0.10 per 100 products
- **Google Shopping Scraper:** ~$0.20 per 100 products
- **Instagram Hashtag Scraper:** ~$0.50 per 1000 posts
- **Instagram Profile Scraper:** ~$0.30 per 100 profiles

**Monthly Budget Allocation (Example):**
- Market Analysis (1x per month): ~$2
- Influencer Discovery (1x per month): ~$5
- Reserved for experiments: ~$32

**Total:** Well within $39 budget ✅

---

### Influencer Outreach Costs

**Per Influencer Tier:**
| Tier | Followers | Engagement | Cost/Post | Authenticity | ROI |
|------|-----------|------------|-----------|--------------|-----|
| Nano | 1K-10K | 3-5% | $50-$200 | ⭐⭐⭐⭐⭐ | Best |
| Micro | 10K-100K | 2-4% | $200-$1000 | ⭐⭐⭐⭐ | Good |
| Mid | 100K-500K | 1-3% | $1000-$5000 | ⭐⭐⭐ | OK |

**Recommended Strategy:**
- Focus on **Nano** and **Micro** influencers
- Send free product ($40-60 COGS) + pay $50-200 for video rights
- Total cost per UGC video: $90-260
- Use video in multiple ad campaigns (amortize cost)

**Budget Example (Per Month):**
- 10 influencers contacted
- 3 accept offer
- 3 × $150 average = $450
- 3 UGC videos collected
- Use each video in 2-3 ad campaigns = 6-9 ads total
- Cost per ad: $450 / 7.5 = $60 per UGC ad (very competitive!)

---

## 🛠️ TECHNICAL DETAILS

### Requirements
- Python 3.6+
- Apify API token (configured in scripts)
- Internet connection

### No External Dependencies
- Uses only Python standard library (json, csv, requests, pathlib, etc.)
- Requests to Apify API (built-in)

### Rate Limiting
- Scripts include automatic rate limiting (5-30 sec delays)
- Prevents Apify account suspension
- Respectful to platform APIs

---

## 📊 DATA RETENTION

**Apify Account:**
- Data retention: 31 days
- After 31 days, raw datasets deleted from Apify servers
- Solution: Scripts auto-download and save locally

**Local Storage:**
- `data/` - Keep raw data indefinitely
- `reports/` - Keep reports for historical analysis
- `leads/` - Keep CSV files for ongoing outreach

**Backup Strategy:**
- Raw data automatically saved to `data/` and `leads/raw_data/`
- Reports saved to `reports/`
- Commit to git periodically (if private repo)

---

## 🔐 SECURITY

**API Token Protection:**
- Token hardcoded in scripts (for convenience)
- ⚠️ NEVER commit to public GitHub repo
- Add to `.gitignore` if using version control

**Best Practice:**
```bash
# Create .env file (add to .gitignore)
echo "APIFY_API_TOKEN=YOUR_APIFY_API_TOKEN" > .env

# Modify scripts to load from .env
# (Not required for personal use, but recommended for team/production)
```

---

## 📞 SUPPORT

**Apify Account Issues:**
- Dashboard: https://console.apify.com
- API Status: https://status.apify.com
- Docs: https://docs.apify.com

**Actor Documentation:**
- AliExpress Scraper: https://apify.com/junglee/aliexpress-scraper
- Google Shopping Scraper: https://apify.com/canadesk/google-shopping-scraper
- Instagram Hashtag Scraper: https://apify.com/shu8hvrXbJbY3Eb9W/instagram-hashtag-scraper

**Script Issues:**
- Check `data/` and `reports/` folders for outputs
- Review console output for error messages
- Verify Apify account limits: `curl "https://api.apify.com/v2/users/me/limits?token=..."`

---

## ✅ QUICK REFERENCE

### Run Market Analysis
```bash
cd /Users/mac/Desktop/Alpha-Medical/market-analysis/
python3 market_analysis_scraper.py --full-analysis
```

### Run Influencer Discovery
```bash
cd /Users/mac/Desktop/Alpha-Medical/market-analysis/
python3 influencer_lead_generation.py --full-discovery
```

### Check Apify Usage
```bash
curl "https://api.apify.com/v2/users/me/usage/monthly?token=YOUR_APIFY_API_TOKEN"
```

---

**READY TO RUN!** Execute scripts above to start gathering market intelligence and influencer leads. 🚀

**Estimated Time:**
- Market Analysis (full): ~20 minutes
- Influencer Discovery (full): ~45 minutes
- **Total first run: ~65 minutes**

**Output:**
- Market reports: JSON (structured data for analysis)
- Influencer leads: CSV (ready for outreach in Excel/Sheets)
