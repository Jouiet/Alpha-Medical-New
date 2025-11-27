# llms.txt Deployment Guide - Alpha Medical

## 🎯 Deployment Options

This guide covers **5 production-ready deployment methods** for serving your llms.txt files to AI models.

**Goal:** Make `llms.txt` accessible at `https://alphamedical.shop/llms.txt` or subdomain

---

## Option 1: GitHub Pages (FREE - Recommended for Testing)

**Pros:** Free, automatic deployment, easy setup
**Cons:** Requires public repository, different domain

### Setup Steps

1. **Make Repository Public** (if not already)
   ```bash
   # Go to GitHub repo settings
   https://github.com/Jouiet/Alpha-Medical-New/settings
   # Scroll to "Danger Zone" → Change visibility → Make public
   ```

2. **Enable GitHub Pages**
   ```
   Repo Settings → Pages
   Source: Deploy from a branch
   Branch: main
   Folder: / (root)
   Save
   ```

3. **Access Your Files**
   ```
   https://jouiet.github.io/Alpha-Medical-New/llms.txt
   https://jouiet.github.io/Alpha-Medical-New/llms-full.txt
   ```

4. **Custom Domain (Optional)**
   ```
   Settings → Pages → Custom domain
   Enter: docs.alphamedical.shop
   ```

   Then add DNS CNAME record:
   ```
   Type: CNAME
   Name: docs
   Value: jouiet.github.io
   ```

**Test:**
```bash
curl https://jouiet.github.io/Alpha-Medical-New/llms.txt
```

---

## Option 2: Vercel (FREE - Best for Custom Domain)

**Pros:** Free, custom domain, automatic HTTPS, blazing fast CDN
**Cons:** Requires Vercel account

### Setup Steps

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Create `vercel.json` in Project Root**
   ```json
   {
     "version": 2,
     "public": true,
     "routes": [
       {
         "src": "/llms.txt",
         "dest": "/llms.txt"
       },
       {
         "src": "/llms-full.txt",
         "dest": "/llms-full.txt"
       }
     ],
     "headers": [
       {
         "source": "/(.*)",
         "headers": [
           {
             "key": "Access-Control-Allow-Origin",
             "value": "*"
           },
           {
             "key": "Content-Type",
             "value": "text/plain; charset=utf-8"
           }
         ]
       }
     ]
   }
   ```

4. **Deploy**
   ```bash
   cd /Users/mac/Desktop/Alpha-Medical
   vercel --prod
   ```

5. **Add Custom Domain**
   ```bash
   vercel domains add docs.alphamedical.shop
   ```

   Then add DNS record:
   ```
   Type: CNAME
   Name: docs
   Value: cname.vercel-dns.com
   ```

**Result:**
```
https://docs.alphamedical.shop/llms.txt
https://docs.alphamedical.shop/llms-full.txt
```

---

## Option 3: Cloudflare Pages (FREE - Best Performance)

**Pros:** Free, unlimited bandwidth, Cloudflare CDN, custom domain
**Cons:** Requires Cloudflare account

### Setup Steps

1. **Go to Cloudflare Pages**
   ```
   https://dash.cloudflare.com/ → Pages → Create a project
   ```

2. **Connect GitHub Repository**
   - Select: `Jouiet/Alpha-Medical-New`
   - Branch: `main`

3. **Build Settings**
   ```
   Framework preset: None
   Build command: (leave empty)
   Build output directory: /
   Root directory: /
   ```

4. **Environment Variables** (none needed)

5. **Deploy**
   - Click "Save and Deploy"
   - Wait ~1 minute

6. **Custom Domain**
   ```
   Project Settings → Custom domains → Add custom domain
   Enter: docs.alphamedical.shop
   ```

   Cloudflare will auto-configure DNS if domain is on Cloudflare.

**Result:**
```
https://alpha-medical-new.pages.dev/llms.txt
https://docs.alphamedical.shop/llms.txt
```

---

## Option 4: AWS S3 + CloudFront (Paid - Enterprise)

**Pros:** Enterprise-grade, full control, can use root domain
**Cons:** Costs money (~$1-5/month), complex setup

### Setup Steps

1. **Create S3 Bucket**
   ```bash
   aws s3 mb s3://alphamedical-llms-txt --region us-east-1
   ```

2. **Configure Bucket for Static Hosting**
   ```bash
   aws s3 website s3://alphamedical-llms-txt \
     --index-document llms.txt \
     --error-document llms.txt
   ```

3. **Upload Files**
   ```bash
   aws s3 cp llms.txt s3://alphamedical-llms-txt/llms.txt \
     --content-type "text/plain; charset=utf-8" \
     --metadata-directive REPLACE

   aws s3 cp llms-full.txt s3://alphamedical-llms-txt/llms-full.txt \
     --content-type "text/plain; charset=utf-8" \
     --metadata-directive REPLACE
   ```

4. **Make Public**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Sid": "PublicReadGetObject",
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::alphamedical-llms-txt/*"
       }
     ]
   }
   ```

5. **Create CloudFront Distribution**
   - Origin: S3 bucket endpoint
   - Viewer Protocol Policy: Redirect HTTP to HTTPS
   - Allowed HTTP Methods: GET, HEAD, OPTIONS
   - Cache Policy: CachingOptimized

6. **Add Custom Domain**
   - Alternate Domain Names (CNAMEs): `docs.alphamedical.shop`
   - SSL Certificate: Request ACM certificate

**Result:**
```
https://docs.alphamedical.shop/llms.txt
```

---

## Option 5: Netlify (FREE - Alternative to Vercel)

**Pros:** Free, custom domain, drag-and-drop deploy
**Cons:** Requires Netlify account

### Setup Steps

1. **Go to Netlify**
   ```
   https://app.netlify.com/
   ```

2. **Connect GitHub**
   - Sites → Add new site → Import an existing project
   - GitHub → Select `Jouiet/Alpha-Medical-New`

3. **Build Settings**
   ```
   Branch: main
   Build command: (leave empty)
   Publish directory: /
   ```

4. **Deploy**

5. **Custom Domain**
   ```
   Site settings → Domain management → Add custom domain
   Enter: docs.alphamedical.shop
   ```

   Add DNS CNAME:
   ```
   Type: CNAME
   Name: docs
   Value: [your-site].netlify.app
   ```

**Result:**
```
https://alpha-medical.netlify.app/llms.txt
https://docs.alphamedical.shop/llms.txt
```

---

## 🚀 Quick Start - Recommended Path

### For Immediate Testing (5 minutes)
**Use GitHub Pages** - Option 1

### For Production (15 minutes)
**Use Vercel or Cloudflare Pages** - Options 2 or 3

### Setup Now

1. **Choose a platform** from above
2. **Follow the setup steps**
3. **Verify deployment**:
   ```bash
   curl https://your-domain.com/llms.txt
   ```
4. **Test with AI model**:
   > "Can you read https://your-domain.com/llms.txt and summarize it?"

---

## 📋 Post-Deployment Checklist

After deploying to any platform:

```bash
# 1. Verify llms.txt is accessible
curl -I https://your-domain.com/llms.txt

# Should return:
# HTTP/2 200
# Content-Type: text/plain; charset=utf-8

# 2. Verify content is correct
curl https://your-domain.com/llms.txt | head -20

# Should show:
# # Alpha Medical Care
# > Professional medical support...

# 3. Test with AI model
# Ask ChatGPT/Claude/Gemini:
# "Read https://your-domain.com/llms.txt and tell me about Alpha Medical"

# 4. Validate format
python3 validate_llms_txt.py

# 5. Monitor access logs
# Check your platform's analytics for /llms.txt requests
```

---

## 🔄 Continuous Deployment

### GitHub Actions (Already Configured)

The `.github/workflows/update-llms-txt.yml` workflow will:
- ✅ Trigger on any `.md` file change
- ✅ Regenerate llms.txt and llms-full.txt
- ✅ Validate both files
- ✅ Auto-commit if changed

**This works automatically with:**
- GitHub Pages
- Vercel (with GitHub integration)
- Cloudflare Pages (with GitHub integration)
- Netlify (with GitHub integration)

**Manual deployments** (S3/CloudFront):
```bash
# Add to GitHub Actions workflow
- name: Deploy to S3
  run: |
    aws s3 cp llms.txt s3://your-bucket/llms.txt
    aws s3 cp llms-full.txt s3://your-bucket/llms-full.txt
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

---

## 🌐 DNS Configuration

### For Custom Domain (docs.alphamedical.shop)

**If using Shopify DNS:**
1. Shopify Admin → Settings → Domains
2. Can't add CNAME to subdomain directly
3. **Solution:** Use Cloudflare DNS instead

**If using Cloudflare DNS:**
```
Type: CNAME
Name: docs
Target: [your-deployment-url]
Proxy: Enabled (orange cloud)
TTL: Auto
```

**If using Other DNS Provider:**
```
Type: CNAME
Name: docs
Value: [your-deployment-url]
TTL: 300
```

### Verification
```bash
dig docs.alphamedical.shop

# Should show:
# docs.alphamedical.shop. 300 IN CNAME [deployment-url]
```

---

## 📊 Monitoring & Analytics

### Track Usage

**Vercel Analytics:**
```bash
# Add to vercel.json
{
  "analytics": true
}
```

**Cloudflare Analytics:**
- Built-in Web Analytics in Pages dashboard

**Google Analytics:**
```html
<!-- Not needed for llms.txt - it's a plain text file -->
```

**Custom Tracking:**
```javascript
// If using JavaScript redirect page
fetch('/api/track', {
  method: 'POST',
  body: JSON.stringify({
    path: '/llms.txt',
    referrer: document.referrer
  })
});
```

### Monitor AI Bot Traffic

Check access logs for:
- `ChatGPT-User` (OpenAI)
- `Claude-Web` (Anthropic)
- `Google-Extended` (Google AI)
- `Perplexity` (Perplexity AI)

---

## 🔒 Security Considerations

### CORS Headers
```json
{
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
  "Access-Control-Max-Age": "86400"
}
```

### Rate Limiting (Optional)
```
Not needed for llms.txt - AI bots are well-behaved
CDN caching handles traffic spikes automatically
```

### HTTPS Required
All deployment options provide automatic HTTPS.
**Never serve llms.txt over HTTP.**

---

## 🎯 Recommended: Vercel Deployment

**Best balance of ease, performance, and features.**

```bash
# One-time setup (5 minutes)
npm install -g vercel
cd /Users/mac/Desktop/Alpha-Medical
vercel login
vercel --prod

# Add custom domain
vercel domains add docs.alphamedical.shop

# Done! Your files are at:
# https://docs.alphamedical.shop/llms.txt
# https://docs.alphamedical.shop/llms-full.txt
```

**Auto-updates:**
- Every git push to main triggers GitHub Actions
- llms.txt regenerates automatically
- Vercel deploys automatically
- Zero manual intervention

---

## ✅ Final Verification

```bash
# 1. URL is live
curl -I https://docs.alphamedical.shop/llms.txt
# → 200 OK

# 2. Content is correct
curl https://docs.alphamedical.shop/llms.txt | head -5
# → # Alpha Medical Care

# 3. File size is reasonable
curl -s https://docs.alphamedical.shop/llms.txt | wc -c
# → ~10,000 bytes (10 KB)

# 4. HTTPS is enforced
curl -I http://docs.alphamedical.shop/llms.txt
# → 301 Moved Permanently (redirects to HTTPS)

# 5. AI models can read it
# Test with ChatGPT:
# "Can you read https://docs.alphamedical.shop/llms.txt?"
# → Should summarize your project
```

---

## 🚨 Troubleshooting

### Issue: 404 Not Found
**Check:**
- File exists in repository root
- Deployment includes root directory
- No `.gitignore` excluding `*.txt`

### Issue: CORS Error
**Fix:**
```json
{
  "headers": {
    "Access-Control-Allow-Origin": "*"
  }
}
```

### Issue: Wrong Content-Type
**Fix:**
```
Content-Type: text/plain; charset=utf-8
```
Not `text/html` or `application/octet-stream`

### Issue: File Not Updating
**Check:**
- GitHub Actions ran successfully
- Cache cleared (may need to wait 5 minutes)
- Using correct URL (not cached version)

---

## 📞 Support

**Vercel:** https://vercel.com/support
**Cloudflare:** https://community.cloudflare.com/
**Netlify:** https://answers.netlify.com/
**GitHub Pages:** https://docs.github.com/pages

**llms.txt Spec:** https://llmstxt.org/
**Community:** Discord at llmstxt.org

---

**Last Updated:** October 16, 2025
**Status:** ✅ Production Ready - Choose deployment option and deploy
