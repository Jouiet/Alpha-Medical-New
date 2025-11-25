#!/usr/bin/env python3
"""
Session 51 Deployment Verification
Verify all automated deployments from Session 50 & 51
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.admin')

SHOPIFY_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
SHOPIFY_THEME_ID = os.getenv('SHOPIFY_THEME_ID', '140069830733')
API_VERSION = '2024-10'
BASE_URL = f'https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}'

HEADERS = {
    'Content-Type': 'application/json',
    'X-Shopify-Access-Token': SHOPIFY_TOKEN
}

def check_theme_asset(asset_key):
    """Check if asset exists in theme"""
    url = f'{BASE_URL}/themes/{SHOPIFY_THEME_ID}/assets.json'
    params = {'asset[key]': asset_key}

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        response.raise_for_status()

        result = response.json()
        asset_info = result.get('asset', {})

        if asset_info:
            return {
                'exists': True,
                'size': asset_info.get('size', 0),
                'updated': asset_info.get('updated_at', 'N/A')
            }
        else:
            return {'exists': False}

    except Exception as e:
        return {'exists': False, 'error': str(e)}

def check_local_file(file_path):
    """Check if local file exists"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        return {'exists': True, 'size': size}
    else:
        return {'exists': False}

def main():
    print("=" * 80)
    print("SESSION 51 DEPLOYMENT VERIFICATION")
    print("=" * 80)
    print(f"Store: {SHOPIFY_DOMAIN}")
    print(f"Theme ID: {SHOPIFY_THEME_ID}")
    print("=" * 80)

    verifications = []

    # 1. AI Recommendations Matrix (Session 50 generated, Session 51 deployed)
    print("\n1. AI RECOMMENDATIONS MATRIX:")
    print("   " + "-" * 76)

    # Check local file
    local_path = '/Users/mac/Desktop/Alpha-Medical/assets/product-recommendations-matrix.js'
    local_check = check_local_file(local_path)

    if local_check['exists']:
        print(f"   ✅ Local file exists: {local_check['size']:,} bytes")
    else:
        print(f"   ❌ Local file missing: {local_path}")

    # Check deployed asset
    asset_check = check_theme_asset('assets/product-recommendations-matrix.js')

    if asset_check['exists']:
        print(f"   ✅ Deployed to theme: {asset_check['size']:,} bytes")
        print(f"   📅 Last updated: {asset_check['updated']}")
        verifications.append(('AI Recommendations Matrix', 'DEPLOYED'))
    else:
        print(f"   ❌ NOT deployed to theme")
        if 'error' in asset_check:
            print(f"   Error: {asset_check['error']}")
        verifications.append(('AI Recommendations Matrix', 'FAILED'))

    # 2. Social Share Image (Session 51 generated)
    print("\n2. SOCIAL SHARE IMAGE:")
    print("   " + "-" * 76)

    social_image_path = '/Users/mac/Desktop/Alpha-Medical/alpha_medical_social_share.png'
    social_check = check_local_file(social_image_path)

    if social_check['exists']:
        print(f"   ✅ Generated: {social_check['size']:,} bytes ({social_check['size']/1024:.1f} KB)")
        print(f"   📁 Location: {social_image_path}")
        print(f"   ⏳ Manual upload required: Shopify Admin → Theme Settings → Social media")
        verifications.append(('Social Share Image', 'GENERATED (Manual upload pending)'))
    else:
        print(f"   ❌ NOT generated")
        verifications.append(('Social Share Image', 'FAILED'))

    # 3. Generate Recommendations Matrix Script
    print("\n3. GENERATE RECOMMENDATIONS SCRIPT:")
    print("   " + "-" * 76)

    script_path = '/Users/mac/Desktop/Alpha-Medical/generate_recommendations_matrix.py'
    script_check = check_local_file(script_path)

    if script_check['exists']:
        print(f"   ✅ Script exists: {script_check['size']:,} bytes")
        print(f"   📄 Can regenerate matrix anytime: python3 generate_recommendations_matrix.py")
        verifications.append(('Generate Recommendations Script', 'READY'))
    else:
        print(f"   ❌ Script missing")
        verifications.append(('Generate Recommendations Script', 'MISSING'))

    # 4. Deploy Script
    print("\n4. DEPLOY SCRIPT:")
    print("   " + "-" * 76)

    deploy_path = '/Users/mac/Desktop/Alpha-Medical/deploy_recommendations_matrix.py'
    deploy_check = check_local_file(deploy_path)

    if deploy_check['exists']:
        print(f"   ✅ Script exists: {deploy_check['size']:,} bytes")
        print(f"   📄 Can redeploy anytime: python3 deploy_recommendations_matrix.py")
        verifications.append(('Deploy Script', 'READY'))
    else:
        print(f"   ❌ Script missing")
        verifications.append(('Deploy Script', 'MISSING'))

    # 5. GitHub Secrets Guide (Session 50)
    print("\n5. GITHUB SECRETS SETUP GUIDE:")
    print("   " + "-" * 76)

    guide_path = '/Users/mac/Desktop/Alpha-Medical/market-analysis/SETUP_GITHUB_SECRETS_GUIDE.md'
    guide_check = check_local_file(guide_path)

    if guide_check['exists']:
        print(f"   ✅ Guide created: {guide_check['size']:,} bytes")
        print(f"   ⚠️  Gitignored (matches *_SECRET* pattern)")
        print(f"   ⏳ Manual setup required (5 min): Follow guide to configure 4 secrets")
        verifications.append(('GitHub Secrets Guide', 'CREATED (Gitignored)'))
    else:
        print(f"   ❌ Guide missing")
        verifications.append(('GitHub Secrets Guide', 'MISSING'))

    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)

    for item, status in verifications:
        status_icon = "✅" if "DEPLOYED" in status or "READY" in status or "GENERATED" in status or "CREATED" in status else "❌"
        print(f"{status_icon} {item:40s} | {status}")

    print("\n" + "=" * 80)
    print("SESSION 51 STATUS")
    print("=" * 80)

    automated_complete = sum(1 for _, s in verifications if "DEPLOYED" in s or "READY" in s or "GENERATED" in s)
    manual_pending = sum(1 for _, s in verifications if "Manual" in s or "pending" in s)

    print(f"Automated Deployments: {automated_complete}/{len(verifications)}")
    print(f"Manual Actions Pending: {manual_pending}")

    print("\nNEXT MANUAL ACTIONS:")
    print("1. Upload social share image to Shopify Theme Settings (5 min)")
    print("2. Configure GitHub Secrets (5 min) - Unblocks 9 workflows")
    print("3. Create smart-recommendations.liquid snippet (15 hours)")
    print("4. Shopify Flow configurations (60 min)")

    print("=" * 80)

if __name__ == '__main__':
    main()
