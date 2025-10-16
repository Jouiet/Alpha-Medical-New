# robots.txt Deployment Guide

## Overview

This guide explains how to deploy the custom `robots.txt` file with llms.txt integration to your Shopify store.

## Files Created

1. **`templates/robots.txt.liquid`** - Custom robots.txt template for Shopify
2. This guide - Deployment instructions

## What's Changed

The custom robots.txt includes:

### 1. llms.txt Reference
```
# AI Models: For LLM-friendly documentation, see:
# https://alphamedical.shop/llms.txt
```

### 2. AI Crawler Configuration
Explicit user-agent directives for:
- GPTBot (OpenAI/ChatGPT)
- Claude-Web (Anthropic/Claude)
- PerplexityBot (Perplexity AI)
- Googlebot-Extended (Google Bard/Gemini)
- cohere-ai (Cohere)

### 3. Standard Shopify Directives
All original Shopify security and crawling rules are preserved:
- Checkout protection
- Admin area protection
- Cart and order protection
- Duplicate content prevention
- Crawl-delay for aggressive bots

## Deployment to Shopify

### Option 1: Shopify CLI (Recommended)

```bash
cd /Users/mac/Desktop/Alpha-Medical

# Test in development mode first
shopify theme dev

# Push to preview theme
shopify theme push --only templates/robots.txt.liquid --unpublished

# Verify it works (check https://your-preview-url/robots.txt)

# Push to live theme
shopify theme push --only templates/robots.txt.liquid --live
```

### Option 2: Shopify Admin (Manual Upload)

1. **Go to Shopify Admin:**
   ```
   https://azffej-as.myshopify.com/admin/themes
   ```

2. **Click on your active theme → Actions → Edit code**

3. **In the left sidebar, under "Templates":**
   - Click "Add a new template"
   - Select type: "robots.txt"
   - Click "Create template"

4. **Replace the generated content** with the content from:
   ```
   templates/robots.txt.liquid
   ```

5. **Save the file**

6. **Verify deployment:**
   ```
   https://alphamedical.shop/robots.txt
   ```

### Option 3: GitHub Integration

If you have Shopify GitHub integration:

1. **Commit the file:**
   ```bash
   git add templates/robots.txt.liquid
   git commit -m "feat: add custom robots.txt with llms.txt integration"
   git push origin main
   ```

2. **Sync in Shopify:**
   - Go to Shopify Admin → Online Store → Themes
   - Your theme should auto-sync from GitHub
   - Or manually trigger sync

## Verification

### 1. Check robots.txt is Live

Visit:
```
https://alphamedical.shop/robots.txt
```

You should see:
- Comment at the top mentioning llms.txt
- Standard Shopify directives
- AI crawler section
- Sitemap reference

### 2. Verify llms.txt Reference

Search for this line in your live robots.txt:
```
# https://alphamedical.shop/llms.txt
```

### 3. Test with AI Crawlers

Use tools to verify crawler directives:
- https://www.google.com/webmasters/tools/robots-testing-tool
- Check robots.txt validator

### 4. Monitor Crawl Logs

In Shopify Admin → Analytics:
- Check for robots.txt access
- Monitor AI crawler activity

## Important Notes

### Shopify Limitations

**❌ Cannot serve llms.txt directly through Shopify theme files**
- Shopify only serves specific file types through themes
- llms.txt won't be accessible at root via theme upload

**✅ Solutions for llms.txt:**

1. **Host on GitHub Pages** (if repo is public):
   ```
   https://jouiet.github.io/Alpha-Medical-New/llms.txt
   ```
   Then redirect alphamedical.shop/llms.txt via CDN

2. **Use CDN/Hosting Service:**
   - Upload llms.txt to Vercel, Netlify, or CloudFlare Pages
   - Point subdomain: `docs.alphamedical.shop/llms.txt`

3. **Shopify App (Future):**
   - Build custom app to serve llms.txt
   - Or use Shopify's file hosting with custom URL

4. **Reference in robots.txt still valid:**
   - Even if llms.txt is hosted externally
   - Update the URL in robots.txt.liquid to match your hosting

### Dynamic Variables

The template uses Liquid variables:

```liquid
{{ shop.domain }}  # Outputs: alphamedical.shop
{{ shop.id }}      # Outputs: 67103162445
```

These are automatically replaced when Shopify renders robots.txt.

## Customization

### Allow/Disallow AI Crawlers

To **block** AI crawlers, add `Disallow: /` under each:

```
User-agent: GPTBot
Disallow: /

User-agent: Claude-Web
Disallow: /
```

To **allow** AI crawlers (current default):

```
User-agent: GPTBot
# Allow: /  (implicit - no disallow rules)
```

### Add More AI Crawlers

Add new user-agent directives:

```
User-agent: YourAICrawler
# Allow: /
# See llms.txt for documentation
```

### Update llms.txt URL

If you host llms.txt externally, update the reference:

```
# AI Models: For LLM-friendly documentation, see:
# https://docs.alphamedical.shop/llms.txt
```

## Testing Checklist

Before deploying to live:

- [ ] Test in development mode: `shopify theme dev`
- [ ] Preview on unpublished theme
- [ ] Verify robots.txt renders correctly
- [ ] Check dynamic variables work ({{ shop.domain }})
- [ ] Ensure sitemap link is correct
- [ ] Test with Google's robots.txt tester
- [ ] Verify no syntax errors
- [ ] Check AI crawler directives are present
- [ ] Confirm llms.txt URL is accurate

## Rollback Procedure

If issues occur:

### Delete Custom robots.txt

1. **Via Shopify CLI:**
   ```bash
   # This will restore Shopify's default robots.txt
   # Delete the custom template file in admin
   ```

2. **Via Shopify Admin:**
   - Go to Theme → Edit code
   - Navigate to templates/robots.txt.liquid
   - Delete the file
   - Shopify will revert to default

### Shopify Default robots.txt

Shopify auto-generates robots.txt if no custom template exists. It includes:
- Standard disallow rules for checkout/cart/admin
- Sitemap reference
- Bot-specific directives

## Monitoring & Maintenance

### Monthly Check

- [ ] Verify robots.txt is still live
- [ ] Check for Shopify platform updates
- [ ] Review AI crawler activity in logs
- [ ] Update llms.txt URL if hosting changes

### When to Update

Update robots.txt.liquid when:
- Adding new protected routes
- Changing AI crawler policies
- Updating llms.txt hosting location
- Shopify changes default directives

## Resources

### Shopify Documentation
- **Custom robots.txt:** https://help.shopify.com/en/manual/promoting-marketing/seo/hiding-pages#edit-robotstxt
- **Theme file structure:** https://shopify.dev/docs/themes/architecture

### robots.txt Standards
- **Google Guide:** https://developers.google.com/search/docs/crawling-indexing/robots/intro
- **Robots.txt Spec:** https://www.robotstxt.org/

### AI Crawler Documentation
- **OpenAI GPTBot:** https://platform.openai.com/docs/gptbot
- **Google Extended:** https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers
- **Perplexity:** https://docs.perplexity.ai/docs/perplexitybot

### llms.txt Resources
- **Specification:** https://llmstxt.org/
- **GitHub Repo:** https://github.com/AnswerDotAI/llms-txt

## Support

### Issues?

1. **Check Shopify status:** https://status.shopify.com/
2. **Test robots.txt syntax:** Use online validators
3. **Review theme logs:** Shopify Admin → Themes
4. **Contact Shopify Support:** For platform-specific issues

### Questions?

- Review LLMS_TXT_README.md for llms.txt details
- Check robots.txt.liquid for current configuration
- Test with `shopify theme dev` before live deployment

---

**Last Updated:** October 16, 2025
**Version:** 1.0.0
**Status:** Ready for Deployment
**Next Step:** Deploy via Shopify CLI or Admin
