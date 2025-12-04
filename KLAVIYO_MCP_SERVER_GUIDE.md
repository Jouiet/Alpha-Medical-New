# KLAVIYO MCP SERVER - GUIDE ALPHA MEDICAL

> **Status:** ✅ INSTALLED (2025-12-04 Session 76)
> **Purpose:** Direct AI connection to Klaviyo data for analytics, segmentation, and campaign automation

---

## 🎯 QU'EST-CE QUE LE KLAVIYO MCP SERVER?

**Model Context Protocol (MCP)** = Connexion directe entre Claude Code et tes données Klaviyo

**Avant MCP:**
- Aller sur Klaviyo dashboard
- Naviguer dans les menus
- Exporter CSV
- Analyser manuellement
- **Temps:** 15-30 minutes par query

**Avec MCP:**
- Poser la question en langage naturel dans Claude Code
- Réponse instantanée avec données réelles
- **Temps:** 5 secondes

---

## ✅ INSTALLATION (COMPLÈTE)

**Fichier configuré:** `/Users/mac/.config/claude-code/mcp.json`

```json
{
  "mcpServers": {
    "klaviyo": {
      "command": "uvx",
      "args": ["klaviyo-mcp-server@latest"],
      "env": {
        "PRIVATE_API_KEY": "pk_5ea06571b22f82d09dbc157f2c3bd2f0f7",
        "READ_ONLY": "false",
        "ALLOW_USER_GENERATED_CONTENT": "false"
      }
    }
  }
}
```

**⚠️  IMPORTANT:** Redémarrer Claude Code pour activer le MCP server!

---

## 🚀 CAS D'USAGE POUR ALPHA MEDICAL

### 1. ANALYTICS & REPORTING

**Questions que tu peux poser:**

```
"Quel est le revenue total généré par mes flows Klaviyo ce mois?"

"Quel flow a le meilleur open rate?"

"Combien de subscribers actifs j'ai aujourd'hui?"

"Quel email dans le Welcome Series a le meilleur click-through rate?"

"Show me the revenue breakdown by flow for the last 30 days"
```

**Avantage:** Réponses instantanées basées sur données réelles, pas besoin d'aller sur le dashboard.

---

### 2. SEGMENTATION INTELLIGENTE

**Alpha Medical Segments à créer:**

```
"Crée un segment de customers qui ont acheté des knee braces mais pas de posture correctors"

"Trouve les subscribers qui ont ouvert au moins 3 emails mais n'ont jamais acheté"

"Segment: VIP customers (2+ orders, $100+ lifetime value)"

"Créer un segment de cart abandoners avec high-value items ($50+)"
```

**Avantage:** AI recommande les meilleurs critères basés sur tes données comportementales.

---

### 3. OPTIMISATION DES CAMPAIGNS

**Subject Line Optimization:**

```
"Analyse mes 10 derniers emails et dis-moi quels subject lines ont le meilleur open rate"

"Suggère 5 subject lines pour promouvoir les knee braces basés sur mes meilleures performances historiques"

"Quel type de messaging fonctionne le mieux: discounts vs. benefits vs. urgency?"
```

**Send Time Optimization:**

```
"Quel est le meilleur moment pour envoyer mes emails? (basé sur historique)"

"Analyse l'engagement par jour de la semaine pour mes subscribers"
```

---

### 4. CRÉATION DE CAMPAIGNS CONVERSATIONNELLES

**Draft Email Campaigns:**

```
"Crée un email campaign pour promouvoir notre nouveau posture corrector.
Target: Office workers, age 30-50.
Tone: Professional mais empathique.
Include: 15% discount code."

"Draft un win-back email pour les customers inactifs depuis 60 jours"

"Créer une séquence de 3 emails pour le Black Friday (preparation, launch, last chance)"
```

**Avantage:** Draft, review, et launch directement via Claude Code sans aller sur Klaviyo UI.

---

### 5. FLOW PERFORMANCE ANALYSIS

**Questions spécifiques aux 4 flows LIVE:**

```
"Analyse la performance de mon Welcome Series flow:
- Open rates par email
- Click rates par email
- Revenue generated
- Drop-off points"

"Compare les performances: Welcome Series vs. Win-Back flow vs. Cross-Sell flow"

"Où est-ce que je perds le plus de subscribers dans mes flows?"

"Quel email dans mon Abandoned Cart flow a besoin d'optimisation?"
```

---

### 6. REVENUE ATTRIBUTION

**Questions business critiques:**

```
"Combien de revenue Klaviyo a généré ce mois vs. le mois dernier?"

"Quelle est la contribution de Klaviyo au total revenue (Klaviyo vs. autres sources)?"

"ROI de Klaviyo: coût ($30/mo) vs. revenue généré"

"Top 5 products vendus via Klaviyo emails"
```

---

## 📊 EXEMPLES DE REQUÊTES POUR ALPHA MEDICAL

### Startup Routine (chaque matin)

```bash
"Give me my Klaviyo daily dashboard:
- New subscribers (last 24h)
- Emails sent (last 24h)
- Open rate average (last 7 days)
- Revenue from Klaviyo (last 24h)
- Top performing email today"
```

### Weekly Review (chaque lundi)

```bash
"Weekly Klaviyo report:
- Subscriber growth (week over week)
- Best performing flow
- Worst performing email (needs optimization)
- Revenue by flow
- Segment performance"
```

### Monthly Deep Dive (début du mois)

```bash
"Monthly Klaviyo analytics:
- Total revenue generated
- Flow performance comparison
- Segment growth and engagement
- Best subject lines
- Recommendations for next month"
```

---

## 🎯 ALPHA MEDICAL SPECIFIC USE CASES

### Product Launch Automation

**Scénario:** Tu lances un nouveau produit (ex: Therapy Device)

```
"Crée une campagne email pour lancer notre nouveau therapy device:
- Segment: Customers who bought knee braces or back supports
- Subject line: Basé sur nos meilleures performing emails
- Content: Focus on pain relief benefits
- CTA: Shop now with 20% early bird discount
- Follow-up: 3-day reminder for non-openers"
```

### Customer Retention

**Scénario:** Analyser et améliorer la rétention

```
"Analyse customer retention:
- Combien de customers achètent une 2e fois?
- Délai moyen entre 1er et 2e achat?
- Quel produit génère le plus de repeat purchases?
- Recommande une stratégie de cross-sell basée sur purchase history"
```

### Seasonal Campaigns

**Scénario:** Préparer Black Friday / Cyber Monday

```
"Prépare notre stratégie Black Friday:
- Identifie notre best customer segment (high LTV, engaged)
- Crée 5 emails: teaser (1 semaine avant), early access (2 jours avant),
  launch day, reminder (J+1), last chance (J+2)
- Suggère des discounts basés sur notre AOV historique
- Prédis le revenue potentiel basé sur l'engagement passé"
```

---

## ⚙️ CONFIGURATION

### READ_ONLY Mode

**Actuel:** `"READ_ONLY": "false"` (permet la création de campaigns/segments)

**Si tu veux juste analytics:** Change to `"READ_ONLY": "true"`

### ALLOW_USER_GENERATED_CONTENT

**Actuel:** `"ALLOW_USER_GENERATED_CONTENT": "false"` (sécurité)

**Pour permettre AI de créer du contenu:** Change to `"true"`

---

## 🔒 SÉCURITÉ

**API Key:** Privée (pk_...) - ne JAMAIS commit dans git
**Fichier:** `.env.admin` (déjà dans .gitignore ✅)
**MCP Config:** Local machine seulement (`~/.config/claude-code/`)
**Permissions:** API key a les mêmes permissions que le dashboard Klaviyo

---

## 📈 MÉTRIQUES À TRACKER

**Avant MCP vs. Après MCP:**

| Metric | Avant | Après (Objectif) |
|--------|-------|------------------|
| Temps pour analytics | 15-30 min | 5 sec |
| Création campaign | 45-60 min | 10 min |
| Optimisation subject lines | Manuel, lent | Automatique, data-driven |
| Segmentation | Trial & error | AI recommendations |
| ROI visibility | Mensuel | Real-time |

---

## 🎓 LEARNING CURVE

**Jour 1-3:** Familiarisation avec queries simples (analytics, reporting)
**Semaine 1:** Maîtrise segmentation et campaign creation
**Semaine 2-4:** Advanced use cases (optimization, automation, predictive)
**Mois 2+:** Full automation workflow avec MCP + n8n integration

---

## 🚀 PROCHAINES ÉTAPES

1. **Redémarrer Claude Code** pour activer le MCP server
2. **Première requête test:** "Show me my Klaviyo account overview"
3. **Daily routine:** Morning dashboard query
4. **Weekly optimization:** Subject line analysis
5. **Monthly strategy:** Revenue attribution et growth planning

---

## 📚 RESSOURCES

**Documentation officielle:**
- https://developers.klaviyo.com/en/docs/klaviyo_mcp_server
- https://www.klaviyo.com/blog/introducing-mcp-server

**Alpha Medical Context:**
- Klaviyo Active: ✅ $30/mo plan
- Flows LIVE: 4/4 (Welcome, Abandoned Cart, Win-Back, Cross-Sell)
- Templates: 10/10 professional
- Revenue automation: Active 24/7

---

**🎉 TU AS MAINTENANT ACCÈS À TES DONNÉES KLAVIYO DIRECTEMENT DANS CLAUDE CODE!**

Redémarre Claude Code et commence à poser des questions sur tes flows, segments, et campaigns.

**First query to try:**
```
"Show me the performance of my 4 active Klaviyo flows: Welcome Series, Abandoned Cart, Win-Back, and Cross-Sell"
```

---

**Last Updated:** 2025-12-04 Session 76
**Status:** ✅ Configured (awaiting restart)
**Next:** Test connection après restart
