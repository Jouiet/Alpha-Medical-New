---
name: seo-optimizer
description: |
  Optimize Shopify content and meta tags for SEO using Alpha Medical's keyword
  strategy and brand guidelines. Use when asked to improve copy for SEO,
  optimize meta descriptions, analyze catalog for SEO gaps, or create
  SEO-friendly content. Integrates keywords naturally while maintaining brand
  voice. Focuses on content optimization, NOT product data modification.
version: 1.0.0
allowed-tools: Read, Grep, Glob
---

# SEO Content Optimizer Skill

## Purpose
Optimize Alpha Medical e-commerce content for search engines while maintaining brand consistency and conversion-focused copy.

## When to Activate This Skill
Claude will automatically use this skill when you ask to:
- Optimize existing descriptions for SEO
- Create new SEO-friendly copy
- Audit meta titles and descriptions
- Analyze catalog for SEO gaps
- Generate keyword-rich content
- Improve search visibility
- Update copy for target keywords

## What This Skill Does

### 1. SEO Strategy Integration
**Loads Strategic Documents:**
- `AI_SEO_MARKETING_STRATEGIC_ANALYSIS_2025-2026.md` (303KB SEO strategy)
- `ALPHA_MEDICAL_BRAND_GUIDELINES.md` (brand voice & messaging)

**Keyword Strategy:**
- Primary keywords (high-volume, high-intent)
- Long-tail keywords (specific pain points)
- LSI keywords (semantic relevance)
- Local keywords (US market focus)

### 2. Content Description Optimization

**Structure Formula:**
```
1. Hook (Primary keyword in first 100 words)
2. Benefits (Evidence-based, keyword-rich)
3. Features (Technical specs, LSI keywords)
4. Trust Signals (ISO 13485, 5-step vetting)
5. Use Cases (Long-tail keyword integration)
6. CTA (Clear, conversion-focused)
```

**SEO Best Practices:**
- Primary keyword density: 1-2% (natural integration)
- Keyword placement: Title, first 100 words, H2 headers, conclusion
- LSI keywords: 3-5 per description (semantic relevance)
- Internal linking: Related items, category pages
- External linking: Evidence-based research (when applicable)

### 3. Meta Tag Optimization

**Meta Title (Max 60 characters):**
- Format: `[Primary Keyword] | [Benefit] | Alpha Medical`
- Example: `Knee Brace for Arthritis | Pain Relief | Alpha Medical`
- Keyword placement: First 3-5 words
- Brand inclusion: End of title

**Meta Description (Max 160 characters):**
- Format: `[Benefit] with [Item]. [Trust Signal]. [CTA]`
- Example: `Evidence-based knee support for arthritis pain. ISO 13485 quality. Free shipping over $150.`
- Keyword integration: Natural, benefit-focused
- Trust signal: ISO 13485, 5-step vetting, free shipping
- CTA: Clear action (Shop now, Learn more, Get relief)

### 4. Heading Structure (H1-H3)

**H1 (Main Title):**
- Primary keyword inclusion (natural)
- Benefit-focused, not just generic name
- Example: `Premium Knee Brace for Arthritis Pain Relief`

**H2 (Section Headers):**
- Secondary keywords integration
- Question-based (user intent matching)
- Examples:
  - "How Does This Knee Brace Relieve Arthritis Pain?"
  - "What Makes Our Posture Corrector Medical-Grade?"
  - "Who Should Use This Therapy Device?"

**H3 (Subsections):**
- LSI keywords, feature-specific
- Examples:
  - "Adjustable Compression Design"
  - "Breathable, Medical-Grade Material"
  - "Clinically-Proven Pain Relief Technology"

### 5. Image Optimization

**Alt Text Formula:**
- Format: `[Item name] - [Primary keyword] - [Key feature]`
- Example: `Alpha Medical Knee Brace - Arthritis Pain Relief - Adjustable Compression`
- Max length: 125 characters
- Keyword integration: Natural, descriptive

**Image File Naming:**
- Format: `item-name-primary-keyword.jpg`
- Example: `knee-brace-arthritis-pain-relief.jpg`
- SEO-friendly: Hyphens, lowercase, descriptive

### 6. Schema Markup (Structured Data)

**Schema.org Implementation:**
```json
{
  "@type": "Product",
  "name": "[Name with Primary Keyword]",
  "description": "[SEO-optimized description]",
  "brand": "Alpha Medical",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[if available]",
    "reviewCount": "[if available]"
  },
  "offers": {
    "@type": "Offer",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock"
  }
}
```

### 7. Internal Linking Strategy

**Related Items:**
- Link to complementary items (e.g., knee brace → knee sleeves)
- Anchor text: Keyword-rich, natural
- Example: "Pair with our [medical-grade knee sleeves] for enhanced support"

**Category Pages:**
- Link to relevant collections (e.g., Arthritis Relief, Knee Support)
- Breadcrumb navigation optimization
- Example: Home > Pain Relief > Knee Support > [Item]

## How to Use This Skill

### Example 1: Optimize Existing Description
**User Request:** "Optimize the description for the knee brace"

**Skill Actions:**
1. Read current description
2. Load SEO strategy (keyword research)
3. Load brand guidelines (voice, tone)
4. Analyze keyword gaps
5. Rewrite description with:
   - Primary keyword in first 100 words
   - 3-5 LSI keywords naturally integrated
   - Trust signals (ISO 13485, 5-step vetting)
   - Clear H2/H3 structure
   - Internal links to related items
6. Generate optimized meta title (≤60 chars)
7. Generate optimized meta description (≤160 chars)
8. Provide before/after comparison

**Output:** SEO-optimized description + meta tags + analysis

### Example 2: Create New SEO Copy
**User Request:** "Write SEO-friendly copy for new posture corrector"

**Skill Actions:**
1. Load SEO strategy (identify target keywords)
2. Load brand guidelines (apply voice)
3. Research competitor positioning (if needed)
4. Create structured content:
   - H1: Title with primary keyword
   - H2: Benefits section (keywords integrated)
   - H2: Features section (LSI keywords)
   - H2: Trust & quality (ISO 13485, testing)
   - H2: Use cases (long-tail keywords)
5. Generate meta tags (title, description)
6. Suggest image alt text
7. Recommend internal links

**Output:** Complete SEO + brand optimized copy

### Example 3: SEO Catalog Audit
**User Request:** "Analyze all items for SEO optimization gaps"

**Skill Actions:**
1. Read all descriptions (Glob + Read)
2. Analyze each for:
   - Primary keyword presence (first 100 words)
   - Meta title length (≤60 chars)
   - Meta description length (≤160 chars)
   - Keyword density (1-2% target)
   - LSI keyword integration
   - Trust signal presence
   - Internal linking opportunities
3. Prioritize by:
   - Missing meta tags (critical)
   - Low keyword density (high priority)
   - No trust signals (medium priority)
   - Missing internal links (low priority)
4. Generate action plan with:
   - List sorted by priority
   - Specific fixes needed per item
   - Estimated time per fix

**Output:** SEO audit report + prioritized action plan

### Example 4: Keyword Integration Analysis
**User Request:** "Check if our knee items target the right keywords"

**Skill Actions:**
1. Load SEO strategy (keyword research data)
2. Read all knee-related descriptions
3. Extract keywords used (current state)
4. Compare with target keywords (strategy)
5. Identify gaps:
   - High-volume keywords missing
   - Keyword cannibalization (multiple items same keyword)
   - Opportunity keywords (low competition, high intent)
6. Recommend keyword redistribution
7. Suggest content updates

**Output:** Keyword gap analysis + recommendations

## SEO Best Practices Checklist

### On-Page SEO
- [ ] Primary keyword in first 100 words
- [ ] Meta title ≤60 characters (keyword-rich)
- [ ] Meta description ≤160 characters (benefit + CTA)
- [ ] H1 includes primary keyword (natural)
- [ ] H2/H3 include secondary/LSI keywords
- [ ] Keyword density 1-2% (natural integration)
- [ ] 3-5 LSI keywords included
- [ ] Alt text optimized for all images
- [ ] Internal links to related items/categories
- [ ] Schema markup implemented (if applicable)

### Content Quality
- [ ] Evidence-based claims (cite research if possible)
- [ ] Trust signals present (ISO 13485, 5-step vetting)
- [ ] Brand voice consistent (professional + accessible)
- [ ] User intent matched (pain points addressed)
- [ ] Clear value proposition (why choose this)
- [ ] CTA included (clear next step)
- [ ] Mobile-friendly formatting (short paragraphs, bullets)
- [ ] Scannable content (headers, bold, lists)

### Technical SEO
- [ ] URL structure: /products/[keyword-rich-slug]
- [ ] Image file names: keyword-rich, hyphens
- [ ] Page load speed optimized (images compressed)
- [ ] Mobile responsiveness verified
- [ ] Breadcrumb navigation implemented
- [ ] Canonical tags set correctly
- [ ] Robots.txt allows pages
- [ ] Sitemap.xml includes all pages

## Keyword Strategy Guidelines

### Primary Keywords (1 per item)
- High search volume (1,000+ monthly searches)
- High commercial intent (buying keywords)
- Relevant to category
- Examples:
  - "knee brace for arthritis"
  - "posture corrector for back pain"
  - "compression knee sleeve"

### Long-Tail Keywords (2-3 per item)
- Lower search volume (100-1,000 monthly)
- Very specific user intent
- Higher conversion rate
- Examples:
  - "best knee brace for arthritis pain relief"
  - "medical grade posture corrector for office workers"
  - "compression sleeve for knee swelling after surgery"

### LSI Keywords (3-5 per item)
- Semantically related to primary keyword
- Natural language variations
- Context and relevance
- Examples (for "knee brace"):
  - knee support
  - knee stabilizer
  - knee compression
  - joint pain relief
  - arthritis support

### Local Keywords (when applicable)
- US market focus
- Examples:
  - "knee brace USA"
  - "medical equipment America"
  - "pain relief products US"

## Output Format

### Before/After Comparison
```
**BEFORE:**
[Original description]
- Meta Title: [original]
- Meta Description: [original]
- Primary Keyword Presence: [Yes/No]
- Keyword Density: [X%]

**AFTER:**
[Optimized description]
- Meta Title: [optimized, ≤60 chars]
- Meta Description: [optimized, ≤160 chars]
- Primary Keyword Presence: ✅ (first 100 words)
- Keyword Density: [1-2%]
- LSI Keywords: [list]
- Trust Signals: [list]
- Internal Links: [list]

**IMPROVEMENTS:**
1. Added primary keyword in first sentence
2. Integrated 4 LSI keywords naturally
3. Included ISO 13485 trust signal
4. Optimized meta tags (char limits)
5. Added internal links to [related items]
6. Improved H2 structure for SEO
```

## Reference Documents

### Primary Sources (Auto-Loaded)
- `AI_SEO_MARKETING_STRATEGIC_ANALYSIS_2025-2026.md` - Keyword strategy
- `ALPHA_MEDICAL_BRAND_GUIDELINES.md` - Brand voice compliance

### Complementary References (Load as Needed)
- Current content files (descriptions)
- Competitor analysis (if available)
- Google Search Console data (if available)

## Success Metrics

**SEO Optimization Score:**
- Meta tags optimized: ✅/❌
- Primary keyword integrated: ✅/❌
- LSI keywords present (3-5): ✅/❌
- Trust signals included: ✅/❌
- Internal links added: ✅/❌
- Brand voice maintained: ✅/❌

**Target:** 100% content with all criteria met
**Validation:** Audit report with checklist scores

---

**Skill Status:** ACTIVE
**Last Updated:** 2025-12-06 Session 81
**Validation:** Factual (references verified SEO strategy + brand guidelines)
**Confidence:** 100% (based on documented strategy)
**Impact:** HIGH (immediate value for 100 items)
**Note:** READ-ONLY skill - analyzes and recommends, does NOT modify data
