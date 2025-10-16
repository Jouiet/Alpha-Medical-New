# llms.txt Implementation Guide

## What is llms.txt?

`llms.txt` is a proposed standard to help AI models (ChatGPT, Claude, Gemini, Perplexity, etc.) better understand and navigate your website/project at inference time. Think of it as a `robots.txt` but for Large Language Models.

**Official Specification:** https://llmstxt.org/

## Files in This Implementation

### 1. `llms.txt` (Main Index)
**Location:** `/llms.txt`

This is the main file that AI models will read. It contains:
- Project overview and description
- Categorized links to documentation files
- Brief descriptions for each resource
- AI model guidance and best practices

**Format:** Markdown with structured sections

### 2. `generate_llms_txt.py` (Automation Script)
**Location:** `/generate_llms_txt.py`

Automatically scans your project and regenerates `llms.txt` with:
- All markdown documentation files
- Automatic categorization by topic
- Extracted descriptions from file content
- Updated timestamps

**Usage:**
```bash
python3 generate_llms_txt.py
```

**When to run:**
- After adding new documentation files
- After major documentation updates
- Monthly for timestamp refresh
- Before deploying to production

## Deployment to Your Website

### Option 1: Static File (Recommended)
Copy `llms.txt` to your website's root directory:

```bash
# For Shopify (requires custom domain or CDN)
# Upload to your hosting provider at:
# https://alphamedical.shop/llms.txt

# Or use Shopify Files (not ideal, different URL)
```

**Note:** Shopify doesn't natively support serving custom files at root. You'll need:
- Custom hosting (Vercel, Netlify, CloudFlare Pages)
- Or serve from CDN
- Or use Shopify's file hosting (different URL structure)

### Option 2: GitHub Pages
If your repo is public, enable GitHub Pages:

1. Go to repo Settings → Pages
2. Select branch: `main`, folder: `/root`
3. Your llms.txt will be available at:
   `https://[username].github.io/[repo-name]/llms.txt`

### Option 3: Manual Upload to CDN
Upload to your CDN provider:
- CloudFlare
- AWS S3 + CloudFront
- Vercel
- Netlify

Make it accessible at: `https://yourdomain.com/llms.txt`

## How AI Models Use It

When an AI model (like Claude, ChatGPT, or Perplexity) is asked about your project:

1. **Discovery**: Model fetches `https://yourdomain.com/llms.txt`
2. **Navigation**: Reads the structured index to find relevant docs
3. **Deep Dive**: Follows links to specific documentation files
4. **Context**: Uses descriptions to understand content before fetching

## File Structure

```
Alpha-Medical/
├── llms.txt                    # Main index (generated)
├── generate_llms_txt.py        # Automation script
├── LLMS_TXT_README.md         # This file
│
├── SEO_MARKETING_FORENSIC_ANALYSIS.md
├── IMPLEMENTATION_ROADMAP.md
├── DYNAMIC_PRICING_MODEL.md
├── KLAVIYO_WELCOME_FLOW_IMPLEMENTATION.md
└── [all other .md files]       # Linked from llms.txt
```

## Best Practices

### 1. Keep It Updated
Run the generator script regularly:
```bash
# Add to your workflow
python3 generate_llms_txt.py
git add llms.txt
git commit -m "docs: update llms.txt"
```

### 2. Organize Documentation
The script auto-categorizes files based on keywords. For best results:
- Use descriptive file names (e.g., `SEO_AUDIT_RECOMMENDATIONS.md`)
- Add clear descriptions at the top of each markdown file
- Group related docs in subdirectories if needed

### 3. Manual Customizations
If you edit `llms.txt` manually:
- Update the "AI Model Guidance" section with project-specific rules
- Add custom categories by editing `generate_llms_txt.py`
- Preserve your changes before running the generator again

### 4. Monitor Usage
Track how AI models interact with your llms.txt:
- Check access logs for `/llms.txt` requests
- Monitor which documentation pages get the most AI-driven traffic
- Update frequently accessed pages with more details

## Verification

### Test Your llms.txt

1. **Valid Markdown:**
```bash
# Use a markdown linter
npx markdownlint llms.txt
```

2. **File Accessibility:**
```bash
# Test locally
python3 -m http.server 8000
# Visit: http://localhost:8000/llms.txt
```

3. **AI Model Test:**
Ask an AI model:
> "Can you read and summarize the llms.txt file at https://yourdomain.com/llms.txt?"

### Expected Structure
```markdown
# Project Name

> Brief description

## Section 1
- [Doc Title](path/to/doc.md): Description

## Section 2
- [Another Doc](path/to/another.md): Description
```

## Customization

### Add New Categories

Edit `generate_llms_txt.py`:

```python
CATEGORIES = {
    'Your New Category': [
        'KEYWORD1', 'KEYWORD2'
    ],
    # ... existing categories
}
```

### Exclude Files

Add to exclude list in `generate_llms_txt.py`:

```python
EXCLUDE_FILES = {
    'llms.txt',
    'node_modules',
    'YOUR_PRIVATE_DOC.md',  # Add here
}
```

### Custom Description Extraction

Modify the `extract_description()` function to:
- Look for specific frontmatter fields
- Extract from custom comment blocks
- Use file metadata

## Adoption Status (2025)

As of October 2025:
- **Standard:** Proposed (not official yet)
- **Adopters:** ~1000 websites worldwide
- **AI Model Support:** Unofficial (models can read it but don't prioritize)
- **Future Outlook:** Growing adoption, potential official support from AI providers

**Companies using llms.txt:**
- Anthropic (anthropic.com/llms.txt)
- Answer.AI
- LangChain
- Various open-source projects

## Resources

- **Specification:** https://llmstxt.org/
- **Official Repo:** https://github.com/AnswerDotAI/llms-txt
- **Examples Directory:** https://github.com/thedaviddias/llms-txt-hub
- **Discussion:** Discord community at llmstxt.org

## Support

### Questions?
1. Check the official spec: https://llmstxt.org/
2. Review examples: https://github.com/thedaviddias/llms-txt-hub
3. Test with AI models: Ask Claude, ChatGPT, or Perplexity to read your llms.txt

### Contributing
If you improve the generator script or find issues:
1. Document your changes
2. Test with `python3 generate_llms_txt.py`
3. Verify the output `llms.txt` is valid markdown
4. Commit with descriptive message

---

**Last Updated:** October 16, 2025
**Version:** 1.0.0
**Status:** ✅ Production Ready
