# N8N BLOG AUTOMATION - GUIDE SETUP COMPLET
**Date:** 2025-12-03
**Workflow:** AI Blog Generator for Shopify (Google Gemini + Sheets)
**Template Source:** https://n8n.io/workflows/8575
**Target:** Alpha Medical - Wellness Products SEO Content

---

## ÉTAPE 1: PRÉREQUIS (15 min)

### 1.1 Google Gemini API Key ✅ EN COURS

**URL:** https://aistudio.google.com/app/apikey

**Actions:**
1. Cliquez "Create API Key" (ou "Get API key")
2. Sélectionnez project existant OU créez nouveau projet Google Cloud
3. Copiez la clé API (format: `AIza...`)
4. Sauvegardez dans fichier sécurisé

**Cost:** $0 (gratuit jusqu'à 15 requests/minute, 1500/day)

### 1.2 Shopify API Credentials ✅ DÉJÀ CONFIGURÉ

**Vérification:**
```bash
grep -E "SHOPIFY_STORE_URL|SHOPIFY_API_KEY" .env.admin
```

**Attendu:**
- SHOPIFY_STORE_URL=azffej-as.myshopify.com
- SHOPIFY_API_KEY=shpat_xxx (Admin Access Token)

**Status:** ✅ Déjà disponible dans `.env.admin`

### 1.3 Google Sheets Setup ✅ DÉJÀ CONFIGURÉ

**Vérification:**
```bash
# OAuth credentials déjà configurés pour workflow #1 (Gemini image processing)
cat .n8n-credentials.env | grep GOOGLE
```

**Status:** ✅ Credentials Google déjà en place

---

## ÉTAPE 2: IMPORT WORKFLOW N8N (20 min)

### 2.1 Accéder à l'Instance N8N

**URL:** https://n8n.srv1168256.hstgr.cloud

**Login:**
- Email: (votre email n8n)
- Password: (votre password n8n)

### 2.2 Créer Google Sheet pour Blog Tracking

**Actions:**
1. Ouvrir Google Drive
2. Créer nouveau Google Sheet
3. Nom: "Alpha Medical - Blog Automation Tracking"
4. Créer 3 onglets:
   - **Raw Input** (colonnes: product_id, title, description, images, price, url)
   - **Refined Input** (colonnes: product_id, clean_description, plain_text, image_urls)
   - **Blog Post** (colonnes: product_id, blog_title, blog_content, meta_description, blog_status, article_id, published_at)

5. Copier l'ID du Sheet depuis URL:
   ```
   https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit
   ```

**Sauvegardez:** SHEET_ID pour configuration workflow

### 2.3 Télécharger Template JSON

**Option A - Via n8n.io (Recommandé):**
1. Aller sur: https://n8n.io/workflows/8575
2. Cliquer "Use for free"
3. Si demandé de se connecter → utiliser compte n8n existant
4. Copier le JSON du workflow (ou télécharger)

**Option B - Workflow JSON Simplifié (Créé Custom):**

Si le template n8n.io est difficile d'accès, je peux créer un workflow simplifié adapté spécifiquement pour Alpha Medical wellness products.

**Workflow Simplifié Alpha Medical:**
```
Nodes: 10 (vs 15+ template original)
1. Manual Trigger / Cron Trigger
2. Shopify Get Product (random from collection)
3. Google Gemini - Generate Article
4. Code Node - Format HTML
5. Shopify Create Blog Article (DRAFT)
6. Google Sheets - Log Article
7. Email/Slack Notification
```

**Voulez-vous:**
- [ ] Option A: Template complet n8n.io (plus de features)
- [x] Option B: Workflow simplifié custom (plus rapide à setup)

---

## ÉTAPE 3: CONFIGURATION CREDENTIALS (15 min)

### 3.1 Google Gemini Credential

**Dans n8n:**
1. Allez à "Credentials" (menu gauche)
2. Cliquez "+ Add Credential"
3. Recherchez "Google Gemini" ou "Google PaLM"
4. Nom: "Google Gemini - Alpha Medical"
5. API Key: [Coller clé API depuis Étape 1.1]
6. Cliquez "Save"

### 3.2 Shopify Credential

**Dans n8n:**
1. "Credentials" → "+ Add Credential"
2. Type: "Shopify Admin API"
3. Nom: "Shopify Alpha Medical"
4. Shop Subdomain: azffej-as
5. Access Token: [Depuis .env.admin SHOPIFY_API_KEY]
6. Cliquez "Save"

### 3.3 Google Sheets Credential

**Status:** Déjà configuré ✅

Si besoin de reconfigurer:
1. "Credentials" → Rechercher "Google Sheets OAuth2"
2. Vérifier credential existant
3. Si manquant → Créer nouveau avec OAuth flow

---

## ÉTAPE 4: CUSTOMISATION PROMPTS (45 min)

### 4.1 Prompt Template Wellness Products

**Node:** "Google Gemini - Generate Article"

**Prompt Optimisé:**

```
You are an expert wellness content writer for Alpha Medical, a retailer specializing in pain relief and wellness products.

TASK: Write a comprehensive, SEO-optimized blog article about the following product.

PRODUCT INFORMATION:
- Title: {{$json["title"]}}
- Description: {{$json["description"]}}
- Category: {{$json["product_type"]}}
- Price: ${{$json["price"]}}

TARGET AUDIENCE: {{$json["target_persona"] || "Seniors, Office Workers, Athletes"}}

PRIMARY KEYWORD: {{$json["seo_keyword"] || "pain relief for [category]"}}

ARTICLE STRUCTURE (2000-2500 words):

# {{seo_keyword}}: Complete Wellness Guide

## Introduction (150-200 words)
- Hook: Relatable pain point scenario
- Context: Why this wellness support matters
- Preview: What readers will learn

## Understanding [Product Category] (300-350 words)
- What it is and how it works
- Common uses in daily life
- Who benefits most
- Science behind pain relief (general wellness principles)

## Key Benefits and Uses (400-450 words)
- Pain relief and comfort improvement
- Enhanced mobility/posture support
- Prevention of chronic discomfort
- Quality of life improvements
- Specific use cases for target personas

## Choosing the Right [Product Type] (400-450 words)
- Essential features to consider
- Size and fit guidelines
- Material quality factors
- Comfort vs support balance
- When to consult healthcare professional

## Best Practices and Usage Tips (400-450 words)
- How to use correctly and safely
- Duration and frequency recommendations
- Combining with other wellness practices
- Care and maintenance
- Common mistakes to avoid

## Frequently Asked Questions (300-350 words)

Q1: Is this [product] suitable for my specific needs?
A: [General guidance, recommend professional consultation]

Q2: How long until I see results?
A: [Realistic timeline based on typical usage]

Q3: Can I use it during exercise/sleep/work?
A: [Activity-specific guidance]

Q4: What if it feels uncomfortable?
A: [Adjustment tips, when to stop]

Q5: Do I need a prescription?
A: [Clarify wellness vs medical device status]

## Conclusion (150-200 words)
- Recap key wellness benefits
- Encourage proactive self-care
- CTA: "Explore our curated collection of [category]"

---

CRITICAL REQUIREMENTS:

1. **Tone & Voice:**
   - Educational, empathetic, wellness-focused
   - Professional but approachable
   - AVOID: Medical claims, diagnosis language, treatment promises
   - USE: Wellness, comfort, support, relief, improvement

2. **Disclaimers:**
   Add at bottom:
   "DISCLAIMER: This content is for educational and informational purposes only. It is not intended as medical advice, diagnosis, or treatment. Always consult with a qualified healthcare professional before starting any new wellness routine or using pain relief products. Individual results may vary."

3. **SEO Optimization:**
   - Primary keyword in H1, first 100 words, conclusion
   - Secondary keywords natural throughout
   - Meta description (150-160 chars): "[Keyword] guide: Benefits, usage tips, choosing guide. Educational wellness resource for pain relief."
   - URL slug: [primary-keyword-wellness-guide]

4. **Internal Linking:**
   Include 2-3 references to related product categories:
   - "For additional lower back support, explore our [posture correctors]"
   - "Athletes may also benefit from [compression wear]"
   - "Seniors seeking mobility aids can review our [braces collection]"

5. **HTML Format:**
   Return structured HTML:
   - <h2> for main sections
   - <h3> for subsections
   - <ul> for bullet lists
   - <p> for paragraphs
   - <strong> for emphasis
   - NO <h1> (Shopify adds automatically)

6. **Content Quality:**
   - Cite general wellness principles (no medical studies unless verified)
   - Focus on user experience and comfort
   - Evidence-based recommendations (when applicable)
   - Realistic expectations

OUTPUT FORMAT:
Return JSON with these exact fields:
{
  "blog_title": "SEO-optimized title with keyword",
  "meta_description": "150-160 char description",
  "article_body_html": "<h2>Understanding...</h2><p>Content...</p>...",
  "seo_keywords": "primary keyword, secondary 1, secondary 2",
  "url_slug": "primary-keyword-wellness-guide"
}
```

### 4.2 Paramètres Node Gemini

**Model:** gemini-1.5-pro (ou gemini-1.5-flash si plus rapide/cheaper)

**Temperature:** 0.7 (balance créativité/cohérence)

**Max Tokens:** 3000-4000 (pour article 2000-2500 mots)

**Safety Settings:** Moderate (évite contenu médical dangereux)

---

## ÉTAPE 5: TEST PREMIER ARTICLE (30 min)

### 5.1 Préparer Données Test

**Product Suggestion:** Adjustable Knee Brace (best-seller Alpha Medical)

**Données à passer au workflow:**
```json
{
  "title": "Adjustable Knee Brace | Orthopedic Leg Support & Pain Relief",
  "description": "Professional knee support for arthritis, injuries, sports...",
  "product_type": "Knee Braces",
  "price": "167.35",
  "target_persona": "Seniors with arthritis, Athletes recovering from injury",
  "seo_keyword": "knee support for arthritis pain relief"
}
```

### 5.2 Exécuter Workflow Test

**Dans n8n:**
1. Ouvrez workflow créé
2. Cliquez "Execute Workflow" (bouton test)
3. Si Manual Trigger → Cliquez "Execute Node"
4. Observez progression node par node
5. Vérifiez outputs à chaque étape

### 5.3 Vérification Output

**Checks:**
- [ ] Article généré (2000+ mots)
- [ ] Structure HTML correcte
- [ ] Disclaimer présent en bas
- [ ] Meta description 150-160 chars
- [ ] SEO keywords inclus
- [ ] Tone: wellness (NOT medical)
- [ ] Draft créé dans Shopify admin
- [ ] Log dans Google Sheets

**Si erreurs:**
- Note erreurs spécifiques
- Ajuste prompt/paramètres
- Re-test

---

## ÉTAPE 6: OWNER REVIEW PROCESS (30 min)

### 6.1 Review Checklist Template

**Créer dans Google Sheets (onglet "Review Queue"):**

| Article ID | Product | Keywords | Status | Reviewer | Review Date | Publish Date | Notes |
|------------|---------|----------|--------|----------|-------------|--------------|-------|
| DRAFT-001 | Knee Brace | knee support arthritis | PENDING | Owner | | | |

### 6.2 Review Critères

**Vérifier:**
1. **Factual Accuracy:**
   - Product info correct (prix, features, usage)
   - No medical claims ou misinformation
   - Internal links fonctionnels

2. **Tone & Compliance:**
   - Wellness language (not medical treatment)
   - Disclaimer present
   - No overpromising results

3. **SEO Quality:**
   - Keywords natural (not stuffed)
   - Meta description compelling
   - H2-H3 structure logical

4. **Brand Voice:**
   - Professional yet approachable
   - Educational focus
   - Empathetic to pain points

**Decision:**
- ✅ APPROVE → Publish dans Shopify
- ⚠️ MINOR EDITS → Quick fixes puis publish
- ❌ REJECT → Regenerate avec prompt ajustements

---

## ÉTAPE 7: ACTIVATION & SCHEDULING (15 min)

### 7.1 Configure Cron Trigger

**Dans n8n workflow:**
1. Remplacer "Manual Trigger" par "Cron Trigger"
2. Schedule: `0 10 * * 0` (Every Sunday 10:00 AM UTC)
3. OU: `0 10 * * 3,0` (Wednesday + Sunday = 2 articles/week)

### 7.2 Collections Rotation

**Node "Get Random Product":**

Configurer rotation collections:
```javascript
// Code Node - Random Collection Selection
const collections = [
  'Knee Braces',
  'Posture Correctors',
  'Back Support',
  'Ankle Braces',
  'Wrist Support',
  'Compression Wear',
  'Pain Relief Devices'
];

const randomCollection = collections[Math.floor(Math.random() * collections.length)];

return {
  json: {
    collection: randomCollection
  }
};
```

### 7.3 Activate Workflow

**Actions:**
1. Click "Active" toggle → ON
2. Sauvegarde workflow
3. Vérifier dans "Executions" que cron est scheduled

---

## ÉTAPE 8: MONITORING & OPTIMIZATION (Ongoing)

### 8.1 Weekly Monitoring (15 min/week)

**Checks:**
1. **n8n Executions:**
   - Status: Success/Failed?
   - Errors: Note patterns
   - Duration: <5 min normal

2. **Google Sheets Log:**
   - Articles generated this week
   - Status: Draft → Published tracking
   - Duplicates check

3. **Shopify Blog:**
   - Draft review queue
   - Published articles count
   - Reader engagement (views, time on page)

### 8.2 Performance Metrics (Monthly)

**Track in Google Sheets Dashboard:**

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Articles/Month | 4-8 | | |
| Generation Cost | <$0.50/mo | | |
| Owner Review Time | 2h/mo | | |
| Google Indexed | 100% | | |
| Avg Position (3mo) | Page 2-3 | | |
| Organic Traffic | +200/mo (6mo) | | |

### 8.3 Prompt Optimization

**A/B Testing (Month 2-3):**

**Version A:** Current prompt (educational long-form)
**Version B:** Problem-solution focus (shorter, 1500 words)

**Metrics to compare:**
- Google ranking position @ 3 months
- Time on page
- Bounce rate
- Organic traffic generated

**Winner:** Scale the better-performing version

---

## COÛTS ESTIMÉS

### Setup (One-time)
- n8n Instance: $0 (déjà hébergé)
- Google Gemini API: $0 (free tier)
- Google Sheets: $0 (free)
- Setup Time: 6h @ $0

**Total Setup: $0**

### Récurrent (Monthly)
- Google Gemini API: $0.02-0.06 (4 articles @ $0.005-0.015/article)
- n8n hosting: $0 (déjà payé)
- Owner Review: 2h @ $0 (votre temps)
- Google Sheets: $0

**Total Monthly: $0.02-0.06**

### Annual Cost
- API calls: $0.24-0.72
- Infrastructure: $0
- Maintenance: 12h/year

**Total Annual: $0.24-0.72**

**Savings vs Manual:**
- Manual writing: $200/article × 48 = $9,600
- Automation cost: $0.72
- **Savings: $9,599.28 (99.99%)**

---

## TROUBLESHOOTING COMMUN

### Erreur: "Gemini API Key Invalid"
**Solution:** Vérifier clé API copiée complètement, pas d'espaces, projet Google Cloud actif

### Erreur: "Shopify 401 Unauthorized"
**Solution:** Vérifier Access Token dans .env.admin, confirmer permissions Admin API

### Erreur: "Google Sheets Access Denied"
**Solution:** Re-authentifier OAuth credential, partager Sheet avec service account

### Workflow génère contenu trop médical
**Solution:** Ajuster prompt - emphasis "wellness" vs "treatment", add disclaimer reminder

### Articles trop courts (<1500 mots)
**Solution:** Augmenter max_tokens Gemini (3000 → 4000), clarifier word count in prompt

### Duplicates générés
**Solution:** Vérifier Filter Node - check Google Sheets "blog_status" column avant generation

---

## NEXT STEPS

**Immediate (Cette Semaine):**
1. ✅ Get Gemini API Key
2. ✅ Create Google Sheet tracking
3. ✅ Import/Create n8n workflow
4. ✅ Configure credentials
5. ✅ Test 1 article
6. ✅ Owner review test output
7. ✅ Adjust prompt si nécessaire
8. ✅ Activate workflow

**Week 2-4:**
- 3-4 articles automatiques générés
- Owner review 30 min/article
- Publish approved articles
- Monitor Google indexation

**Month 2-3:**
- 12 articles live
- Track rankings (Search Console)
- A/B test prompts
- Optimize based on performance

**Month 4-6:**
- Scale to 2 articles/week (8/month)
- First rankings page 2-3 (long-tail)
- Organic traffic +200-500/month
- ROI validation complete

---

**Setup Guide Version:** 1.0
**Created:** 2025-12-03
**For:** Alpha Medical - Wellness Products Blog Automation
**Total Estimated Setup Time:** 6 hours
**Ongoing Effort:** 2h/month (review only)
**Cost:** $0.24-0.72/year
**ROI:** 13,333× (vs manual writing)
