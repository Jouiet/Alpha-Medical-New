#!/bin/bash

###############################################################################
# Alpha Medical - robots.txt Deployment Script
# Safely deploys custom robots.txt with llms.txt integration to Shopify
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Alpha Medical - robots.txt Deployment                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "templates/robots.txt.liquid" ]; then
    echo -e "${RED}❌ Error: templates/robots.txt.liquid not found${NC}"
    echo "   Make sure you're in the Alpha-Medical directory"
    exit 1
fi

# Check if Shopify CLI is installed
if ! command -v shopify &> /dev/null; then
    echo -e "${RED}❌ Error: Shopify CLI not found${NC}"
    echo "   Install it with: npm install -g @shopify/cli"
    exit 1
fi

echo -e "${YELLOW}📋 Pre-deployment Checklist:${NC}"
echo "   ✓ robots.txt.liquid file exists"
echo "   ✓ Shopify CLI installed"
echo ""

# Ask for deployment target
echo -e "${YELLOW}🎯 Select deployment target:${NC}"
echo "   1) Development mode (test locally)"
echo "   2) Preview theme (safe testing)"
echo "   3) Live theme (production)"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo -e "${BLUE}🚀 Starting development mode...${NC}"
        echo ""
        shopify theme dev
        ;;
    2)
        echo -e "${BLUE}🚀 Deploying to preview theme...${NC}"
        echo ""

        # Show current theme status
        echo -e "${YELLOW}📊 Current themes:${NC}"
        shopify theme list
        echo ""

        # Deploy to unpublished
        shopify theme push --only templates/robots.txt.liquid --unpublished

        echo ""
        echo -e "${GREEN}✅ Deployed to preview theme!${NC}"
        echo ""
        echo -e "${YELLOW}📝 Next steps:${NC}"
        echo "   1. Get preview URL from theme list"
        echo "   2. Visit: [preview-url]/robots.txt"
        echo "   3. Verify llms.txt reference is present"
        echo "   4. If OK, run this script again and select option 3"
        ;;
    3)
        echo -e "${RED}⚠️  WARNING: This will deploy to LIVE production theme!${NC}"
        echo ""
        read -p "Are you sure? Type 'YES' to confirm: " confirm

        if [ "$confirm" = "YES" ]; then
            echo ""
            echo -e "${BLUE}🚀 Deploying to LIVE theme...${NC}"
            echo ""

            # Backup check
            echo -e "${YELLOW}💾 Creating backup...${NC}"
            git add templates/robots.txt.liquid
            git commit -m "feat: deploy custom robots.txt with llms.txt integration" || echo "Already committed"

            # Deploy to live
            shopify theme push --only templates/robots.txt.liquid --live

            echo ""
            echo -e "${GREEN}✅ Deployed to LIVE theme!${NC}"
            echo ""
            echo -e "${YELLOW}🔍 Verification steps:${NC}"
            echo "   1. Visit: https://alphamedical.shop/robots.txt"
            echo "   2. Check for llms.txt reference at top"
            echo "   3. Verify AI crawler section exists"
            echo "   4. Confirm sitemap link works"
            echo ""
            echo -e "${BLUE}📊 Opening robots.txt in browser...${NC}"

            # Try to open in browser (macOS)
            if [[ "$OSTYPE" == "darwin"* ]]; then
                open "https://alphamedical.shop/robots.txt"
            fi
        else
            echo -e "${YELLOW}❌ Deployment cancelled${NC}"
            exit 0
        fi
        ;;
    *)
        echo -e "${RED}❌ Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✨ Done!${NC}"
echo ""
echo -e "${BLUE}📚 Additional Resources:${NC}"
echo "   - Deployment guide: ROBOTS_TXT_DEPLOYMENT.md"
echo "   - llms.txt guide: LLMS_TXT_README.md"
echo "   - View live: https://alphamedical.shop/robots.txt"
echo ""
