# BASE PROMPT TEMPLATES

> **Purpose:** Universal templates with variables for quick customization
> **Usage:** Copy template, replace {VARIABLES}, generate

---

## 1. UNIVERSAL STRUCTURE

### Master Template Format
```
[SUBJECT]: {PRODUCT_TYPE} for {TARGET_PERSONA}
[STYLE]: {VISUAL_STYLE}, {LIGHTING}, {MOOD}
[CONTEXT]: {SETTING}, {ACTIVITY}
[TECHNICAL]: {DIMENSIONS}, {FORMAT}, {BACKGROUND}
[BRAND]: Alpha Medical, colors #4770db/#0e1b4d/#eff0f5
[NEGATIVE]: {EXCLUDED_ELEMENTS}
```

---

## 2. VARIABLE DEFINITIONS

### Product Variables
| Variable | Options | Example |
|----------|---------|---------|
| `{PRODUCT_TYPE}` | knee brace, posture corrector, compression sleeve, therapy device | knee brace |
| `{PRODUCT_COLOR}` | black, gray, blue, navy | black |
| `{PRODUCT_MATERIAL}` | neoprene, mesh, elastic, fabric | neoprene |
| `{PRODUCT_FEATURE}` | adjustable straps, breathable, compression, support | adjustable straps |

### Persona Variables
| Variable | Options | Example |
|----------|---------|---------|
| `{TARGET_PERSONA}` | senior (65+), office worker (25-55), athlete (18-45) | senior (65+) |
| `{PERSONA_ACTIVITY}` | gardening, working at desk, exercising, walking | gardening |
| `{PERSONA_PAIN_POINT}` | knee pain, back pain, posture issues, recovery | knee pain |

### Visual Variables
| Variable | Options | Example |
|----------|---------|---------|
| `{VISUAL_STYLE}` | professional photography, lifestyle, UGC, infographic | professional photography |
| `{LIGHTING}` | studio, natural, warm, soft | studio lighting |
| `{MOOD}` | empowering, comfortable, active, trustworthy | empowering |
| `{BACKGROUND}` | white, gradient, lifestyle setting, home | white |

### Technical Variables
| Variable | Options | Example |
|----------|---------|---------|
| `{DIMENSIONS}` | 1080×1080, 1200×628, 1080×1920, 1920×1080 | 1080×1080 |
| `{FORMAT}` | square, vertical, horizontal, portrait | square |
| `{PLATFORM}` | Instagram, Facebook, TikTok, Shopify, Email | Instagram |

---

## 3. QUICK TEMPLATES

### Image: Product on White
```
Professional product photography of {PRODUCT_TYPE}.
Clean white background, soft studio lighting.
{PRODUCT_COLOR} {PRODUCT_MATERIAL} material, {PRODUCT_FEATURE} visible.
E-commerce style, high detail, {DIMENSIONS} {FORMAT}.
Medical equipment aesthetic, premium quality appearance.

Negative: blurry, low quality, cluttered background, text overlay
```

### Image: Lifestyle Shot
```
Lifestyle photography of {TARGET_PERSONA} using {PRODUCT_TYPE}.
{SETTING} environment, {LIGHTING} lighting.
{PERSONA_ACTIVITY}, {MOOD} mood, product visible but natural.
{DIMENSIONS} {FORMAT} for {PLATFORM}.
Authentic, relatable, Alpha Medical brand style.

Negative: staged, fake smiles, clinical setting, before/after
```

### Image: Marketing Ad
```
{PLATFORM} advertisement for {PRODUCT_TYPE}.
{VISUAL_STYLE}, {MOOD} tone.
{TARGET_PERSONA} context, addressing {PERSONA_PAIN_POINT}.
Brand colors #4770db accent, text overlay space.
{DIMENSIONS} {FORMAT}, professional advertising quality.

Negative: aggressive sales, medical claims, low quality
```

### Video: Product Demo
```
Product demonstration video for {PRODUCT_TYPE}.
{DURATION} seconds, {FORMAT} format.
Showing {PRODUCT_FEATURE} functionality.
{BACKGROUND}, {LIGHTING} lighting.
Professional quality, e-commerce standard.

Negative: jerky motion, blurry, unrealistic physics
```

### Video: Lifestyle
```
Lifestyle video featuring {TARGET_PERSONA} with {PRODUCT_TYPE}.
{PERSONA_ACTIVITY}, {SETTING} environment.
{DURATION} seconds, {MOOD} energy.
Product integrated naturally, not salesy.
{FORMAT} format for {PLATFORM}.

Negative: fake, staged, clinical, aggressive pitch
```

---

## 4. PERSONA-SPECIFIC PRESETS

### Preset: Senior (65+)
```
PERSONA_DEFAULTS:
- Activity: gardening, walking, playing with grandchildren
- Setting: home, backyard, park
- Mood: empowering, independent, joyful
- Lighting: warm, natural
- Pain Point: arthritis, joint pain, mobility
- Products: knee brace, compression sleeve
```

### Preset: Office Worker (25-55)
```
PERSONA_DEFAULTS:
- Activity: working at desk, commuting, meetings
- Setting: modern office, home office
- Mood: productive, comfortable, professional
- Lighting: natural window light, office lighting
- Pain Point: back pain, posture issues, desk strain
- Products: posture corrector, lumbar support
```

### Preset: Athlete (18-45)
```
PERSONA_DEFAULTS:
- Activity: running, gym workout, sports, recovery
- Setting: gym, outdoor sports, home recovery
- Mood: dynamic, performance, recovery
- Lighting: natural, gym lighting
- Pain Point: injury prevention, recovery, performance
- Products: compression gear, therapy devices
```

---

## 5. TOOL-SPECIFIC ADJUSTMENTS

### For Nano Banana (Editing)
```
Prefix: "Edit this image to..."
Focus: Background removal, cleanup, enhancement
Style: Keep original product, modify surroundings
Output: Maintains original product fidelity
```

### For Grok Aurora (Generation)
```
Prefix: "Generate/Create..."
Focus: New images from description
Style: Detailed description of desired output
Output: New image based on prompt
Batch: Up to 10 images per request
```

### For Grok Imagine (Video)
```
Prefix: "Create video of..."
Focus: Motion, sequence, narrative
Duration: 5-15 seconds typical
Output: Video clip
Daily limit: ~10 videos
```

### For Kling AI (Video)
```
Prefix: "Generate video showing..."
Focus: High quality, longer duration
Duration: 5-30 seconds
Output: Marketing quality video
Best for: Polished marketing content
```

---

## 6. BRAND CONSTANTS

### Always Include (When Applicable)
```
BRAND ELEMENTS:
- Primary Blue: #4770db
- Navy (text): #0e1b4d
- Light Gray (bg): #eff0f5
- Sale Red: #e32402
- Style: Professional, trustworthy, accessible
- Tone: Medical-grade quality, consumer-friendly
```

### Always Exclude
```
UNIVERSAL NEGATIVES:
- Medical cure claims
- Before/after medical comparison
- Unrealistic promises
- Aggressive sales tactics
- Low quality output
- Competitor references
- Watermarks
- FDA non-compliant imagery
```

---

## 7. QUICK COPY-PASTE BLOCKS

### Product Photo Block
```
Professional product photography, clean white background,
soft studio lighting, e-commerce style, high detail,
medical equipment aesthetic, premium quality.
```

### Lifestyle Block
```
Authentic lifestyle context, natural lighting,
relatable and approachable, product integrated naturally,
empowering mood, genuine expressions.
```

### Marketing Block
```
Professional advertising quality, brand colors #4770db,
clear messaging space, conversion-focused composition,
trustworthy aesthetic, platform-optimized.
```

### Technical Block
```
High resolution, sharp focus, proper exposure,
color accurate, ready for production use,
meets platform specifications.
```

---

## 8. ITERATION WORKFLOW

### First Generation
```
1. Use base template with variables filled
2. Generate 2-4 variations
3. Review outputs
4. Note what works/doesn't work
```

### Refinement
```
1. Keep successful elements
2. Adjust problematic elements in prompt
3. Add specificity where needed
4. Remove vague language
5. Re-generate with refined prompt
```

### Documentation
```
1. Save successful prompts exactly
2. Note tool, settings, date
3. Track performance metrics
4. Update template library
```

---

## 9. PROMPT QUALITY CHECKLIST

Before generating, verify:

- [ ] Subject clearly defined (product type)
- [ ] Style specified (photography, UGC, etc.)
- [ ] Context included (setting, activity)
- [ ] Technical specs stated (dimensions, format)
- [ ] Brand elements mentioned (if applicable)
- [ ] Negative prompts included
- [ ] Tool-appropriate phrasing used
- [ ] No medical claims in prompt
- [ ] Variables replaced with specifics

---

## TEMPLATE VERSIONING

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-17 | Initial creation |
| | | |

*Update this log when templates are modified*
