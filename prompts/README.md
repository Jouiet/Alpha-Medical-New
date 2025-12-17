# AI PROMPT LIBRARY - ALPHA MEDICAL

> **Purpose:** Centralized prompt templates for AI Hybrid Production System
> **Last Updated:** 2025-12-17 Session 103
> **Reference:** `AI_HYBRID_PRODUCTION_SYSTEM_2025.md`

---

## Directory Structure

```
prompts/
├── README.md           # This file
├── products/           # Product photography prompts (Nano Banana, Grok)
├── marketing/          # Ad creatives, banners (Grok Aurora)
├── social/             # Social media content (Instagram, TikTok)
├── video/              # Video generation prompts (Kling, Grok Imagine)
└── templates/          # Base templates and variables
```

---

## Tool-Prompt Mapping

| Use Case | Primary Tool | Backup Tool | Prompt Location |
|----------|-------------|-------------|-----------------|
| Product photo editing | Nano Banana | Leonardo | `products/` |
| Product photo generation | Grok Aurora | Leonardo | `products/` |
| Ad creative generation | Grok Aurora | Leonardo | `marketing/` |
| Social media visuals | Grok Aurora | Nano Banana | `social/` |
| Product videos | Grok Imagine | Kling | `video/` |
| Marketing videos | Kling | Grok Imagine | `video/` |

---

## Prompt Engineering Guidelines

### Structure (Universal)
```
[SUBJECT] + [STYLE] + [CONTEXT] + [TECHNICAL SPECS] + [NEGATIVE PROMPTS]
```

### Alpha Medical Brand Constants
- **Colors:** #4770db (primary blue), #0e1b4d (navy), #eff0f5 (light gray)
- **Style:** Professional, clean, medical-grade, trustworthy
- **Background:** White (#ffffff) for product photos, gradient for lifestyle
- **Lighting:** Soft, even, professional studio
- **Mood:** Empowering, relief-focused, accessible

### Quality Checklist
- [ ] Brand colors included (if applicable)
- [ ] White/clean background specified
- [ ] Professional lighting mentioned
- [ ] Medical equipment context clear
- [ ] No unrealistic claims (FDA compliance)

---

## Usage Workflow

1. **Select prompt category** (products, marketing, social, video)
2. **Choose base template** from `templates/`
3. **Customize variables** (product name, colors, etc.)
4. **Select appropriate tool** (Nano Banana for edits, Grok for generation)
5. **Generate and review** output
6. **Log results** in improvement tracker

---

## Free Tier Limits (Daily)

| Tool | Images | Videos | Notes |
|------|--------|--------|-------|
| Nano Banana | ~50 | - | Best for editing |
| Grok Aurora | 4-10 | - | Best for generation |
| Grok Imagine | - | 10 | Short clips |
| Leonardo | ~15 | - | Backup only |
| Kling | - | varies | Marketing videos |

---

## Continuous Improvement

### Weekly Review
- Track successful prompts (save exact wording)
- Note failed prompts (analyze why)
- Update templates with learnings

### Monthly Optimization
- Review conversion rates of generated assets
- A/B test prompt variations
- Update this library with winners

---

**Maintained by:** Claude Code AI System
**Policy:** All prompts must be tested before production use
