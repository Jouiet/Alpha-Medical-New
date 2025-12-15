# POWER BI LEARNING PATH - ALPHA MEDICAL
**Tier:** Free (0$/mois) - Apprentissage sans pression financière
**Durée estimée:** 3-6 mois (parallèle au lancement store)
**Objectif:** Maîtriser BI avant investissement Pro tier

---

## 🎯 PHASE 1: FONDATIONS (Semaines 1-2)

**Objectif:** Comprendre concepts de base Power BI

### Semaine 1: Interface & Concepts
```yaml
✅ Créer compte Power BI Service (gratuit): https://app.powerbi.com
✅ Explorer "My Workspace" (votre espace personnel)
✅ Comprendre: Datasets vs Reports vs Dashboards
✅ Apprendre navigation interface

Resources:
- Microsoft Learn: "Get started with Power BI" (gratuit)
- YouTube: "Power BI for Beginners" (Guy in a Cube)
- Temps: 2-3h
```

### Semaine 2: Premier dataset (données fictives)
```yaml
✅ Créer Excel avec données e-commerce fictives:
   - Products (10 lignes): name, price, category
   - Orders (20 lignes): date, product_id, quantity, revenue
   - Customers (15 lignes): name, email, signup_date

✅ Importer dans Power BI Desktop (gratuit):
   - Download: https://powerbi.microsoft.com/desktop
   - ⚠️  Requiert Windows VM OU utiliser Power BI Service (upload Excel)

✅ Alternative macOS: Power BI Service web interface
   - Upload Excel directement dans browser
   - Créer visualisations simples (charts, tables)

✅ Créer premier rapport:
   - Chart: Revenue by Product
   - Table: Top 5 Products
   - Card: Total Revenue

Resources:
- Microsoft Learn: "Create your first Power BI report"
- Temps: 3-4h
```

---

## 🔗 PHASE 2: CONNEXIONS SOURCES (Semaines 3-4)

**Objectif:** Connecter Power BI à vos données réelles Alpha Medical

### Semaine 3: Google Sheets (déjà maîtrisé)
```yaml
✅ Connecter Google Sheets lead scraping existant:
   - Power BI Service → Get Data → Google Sheets
   - Sélectionner votre sheet Apify leads
   - Créer visualisations: Leads by Platform, Leads by Date

✅ Apprendre refresh manuel (Free tier limitation)

✅ Test REST API Python:
   python3 powerbi_connection_test.py
   # Lister datasets, exécuter première requête DAX

Resources:
- Vos données: market-analysis/leads Google Sheet
- Temps: 2-3h
```

### Semaine 4: Shopify connector (Power BI Service)
```yaml
✅ Option A - Via Power BI Service web connectors:
   - Get Data → Shopify (si disponible en Free tier)
   - Authentifier avec credentials Shopify
   - Importer: Orders, Products, Customers

✅ Option B - Export CSV manuel (Free tier workaround):
   - Shopify Admin → Export orders.csv
   - Upload CSV dans Power BI Service
   - Refresh manuel quand nouvelles données

✅ Créer rapport Shopify basique:
   - Revenue par jour
   - Top 10 products
   - Orders funnel

Resources:
- Shopify Admin: https://azffej-as.myshopify.com/admin
- Temps: 3-4h
```

---

## 📊 PHASE 3: DAX & MESURES (Semaines 5-8)

**Objectif:** Maîtriser DAX = langage Power BI (équivalent SQL pour analytics)

### Semaines 5-6: DAX Fondations
```yaml
✅ Concepts critiques:
   - Calculated Columns vs Measures (différence cruciale)
   - Context: Row context vs Filter context
   - Functions: SUM, AVERAGE, COUNT, DISTINCTCOUNT

✅ Créer 10 mesures basiques Alpha Medical:
   1. Total Revenue = SUM(Orders[Amount])
   2. Total Orders = COUNTROWS(Orders)
   3. Average Order Value = DIVIDE([Total Revenue], [Total Orders])
   4. Customer Count = DISTINCTCOUNT(Orders[CustomerID])
   5. Revenue per Customer = DIVIDE([Total Revenue], [Customer Count])
   6. Products Sold = SUM(Orders[Quantity])
   7. Conversion Rate = DIVIDE([Total Orders], [Total Visitors])
   8. Cart Abandonment = 1 - [Conversion Rate]
   9. Repeat Customer % = DIVIDE([Repeat Customers], [Customer Count])
   10. Month over Month Growth = ... (time intelligence)

✅ Tester via Python:
   dax = "EVALUATE { [Total Revenue] }"
   execute_dax_query(pbi, dataset_id, dax)

Resources:
- SQLBI.com: "Introducing DAX" (livre gratuit PDF)
- DAX.do: Playground pour tester formules
- Temps: 8-10h
```

### Semaines 7-8: DAX Avancé (Flywheel KPIs)
```yaml
✅ Time Intelligence (tendances temporelles):
   - Revenue Last Month
   - Revenue Year to Date (YTD)
   - Month over Month % change

✅ Filtres & contexte:
   - Revenue by Traffic Source (GA4 data)
   - LTV by Acquisition Channel
   - Cohort Analysis (customers by signup month)

✅ Créer 15 mesures flywheel:
   
   ACQUISITION:
   - CAC (Customer Acquisition Cost) = Ad Spend / New Customers
   - Lead Cost = Ad Spend / Leads Generated
   - Traffic Sources Breakdown

   CONVERSION:
   - Conversion Rate by Source
   - AOV by Product Category
   - Checkout Abandonment Rate

   RETENTION:
   - Customer LTV = Revenue per Customer / Churn Rate
   - Repeat Purchase Rate
   - Days Between Orders (average)

   ADVOCACY:
   - NPS Score (si reviews importées)
   - Review Volume Trend
   - Referral Rate

Resources:
- SQLBI.com: DAX Patterns (exemples e-commerce)
- Temps: 10-12h
```

---

## 🎨 PHASE 4: DASHBOARDS FLYWHEEL (Semaines 9-12)

**Objectif:** Créer dashboards complets 4 phases flywheel

### Semaine 9-10: Dashboard Acquisition
```yaml
✅ Données sources:
   - Google Sheets (Apify leads)
   - GA4 (via connector OU export CSV)
   - Meta Ads (export CSV)

✅ Visualisations:
   - Line chart: Leads generated over time
   - Pie chart: Leads by platform (Instagram, TikTok, FB)
   - Bar chart: Lead cost by source
   - Card: Total leads, Average cost per lead
   - Table: Top performing hashtags

✅ Filtres interactifs:
   - Date range slicer
   - Platform filter
   - Persona filter (seniors, office-workers, athletes)

Resources:
- Power BI Themes: Alpha Medical brand colors (#4770db, #0e1b4d)
- Temps: 6-8h
```

### Semaine 11: Dashboard Conversion + Retention
```yaml
✅ Dashboard Conversion:
   - Funnel visual: Visitors → Add to Cart → Checkout → Purchase
   - AOV trend line
   - Top converting products
   - Conversion rate by traffic source

✅ Dashboard Retention:
   - Cohort matrix: Retention % by signup month
   - LTV distribution histogram
   - Repeat purchase rate trend
   - Klaviyo email engagement metrics

Resources:
- Shopify data (orders, customers)
- Klaviyo export (email metrics)
- Temps: 6-8h
```

### Semaine 12: Dashboard Advocacy + Master View
```yaml
✅ Dashboard Advocacy:
   - Judge.me reviews volume & rating trend
   - NPS score (si collecté)
   - Referral traffic (GA4)

✅ Master Dashboard (vue unifiée):
   - 4 sections: Acquisition | Conversion | Retention | Advocacy
   - KPI cards: CAC, LTV, AOV, Churn Rate, NPS
   - Flywheel health score (custom measure)
   - Alert tiles (rouge si KPI < threshold)

Resources:
- Power BI mobile app: Tester dashboards sur iPhone
- Temps: 8-10h
```

---

## 🤖 PHASE 5: AUTOMATION PYTHON (Semaines 13-16)

**Objectif:** Intégrer Power BI dans workflows Claude Code

### Semaine 13-14: pbipy mastery
```yaml
✅ Scripts Python automation:

1. powerbi_refresh.py:
   - Trigger manual refresh de tous datasets
   - Log résultats (success/failure)
   - Cron: daily 6am

2. powerbi_export_data.py:
   - Exécuter 20 requêtes DAX
   - Exporter résultats en CSV
   - Upload vers Google Sheets (sync bidirectionnel)

3. powerbi_alerts.py:
   - Checker KPIs critiques via DAX
   - Si AOV < $50 → Send email alert
   - Si Churn > 40% → Slack notification

4. powerbi_claude_integration.py:
   - Claude Code asks: "What was revenue last week?"
   - Script execute DAX query
   - Return formatted answer to Claude

Resources:
- pbipy docs: https://github.com/andrewvillazon/pbipy
- Temps: 10-12h
```

### Semaine 15-16: CI/CD Integration
```yaml
✅ GitHub Actions workflow: .github/workflows/powerbi-sync.yml

name: Power BI Daily Sync
on:
  schedule:
    - cron: '0 6 * * *'  # 6am daily
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: pip install pbipy msal
      - name: Sync Power BI
        env:
          AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
          AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
          AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
        run: python3 powerbi_refresh.py

✅ Ajouter secrets GitHub (déjà maîtrisé Session 56)

Resources:
- Existing: .github/workflows/ (10 workflows déjà actifs)
- Temps: 4-6h
```

---

## 📈 PHASE 6: ANALYSE AVANCÉE (Semaines 17-24)

**Objectif:** Analytics niveau expert (préparer upgrade Pro)

### Semaines 17-20: Attribution multi-touch
```yaml
✅ Problème business:
   Customer journey: Instagram Ad → Google Search → Email → Purchase
   Question: Quel channel créditer pour la conversion?

✅ Solutions Power BI:
   - First-touch attribution (Instagram = 100%)
   - Last-touch attribution (Email = 100%)
   - Linear attribution (tous = 33% chacun)
   - Time-decay attribution (Email = 50%, Google = 30%, Instagram = 20%)

✅ DAX implementation:
   - Créer table Touchpoints (GA4 + Klaviyo + Meta data)
   - Measure: Attribution Score by Channel
   - Visualisation: Sankey diagram (customer journey flow)

Resources:
- DAX Pattern: "Attribution Models"
- Temps: 12-15h
```

### Semaines 21-24: Predictive Analytics (optionnel)
```yaml
✅ Machine Learning integration:
   - Python script: Train model (customer churn prediction)
   - Export predictions → Power BI dataset
   - Dashboard: "Customers at Risk" (churn probability > 70%)

✅ Forecasting:
   - Power BI built-in: Revenue forecast (next 3 months)
   - Confidence intervals (best/worst case scenarios)

Resources:
- Power BI + Python: Integration guide
- Temps: 15-20h (optionnel)
```

---

## ✅ GRADUATION: Quand upgrader vers Pro?

**Triggers upgrade Free → Pro ($10/mois):**

```yaml
✅ Maîtrise technique complète:
   - 50+ mesures DAX créées et comprises
   - 10+ dashboards fonctionnels
   - Python automation opérationnelle
   - 3-6 mois expérience hands-on

✅ Business justification:
   - Revenue > $10K/mois (ROI = 0.1% du revenue)
   - Besoin collaboration (partager avec VA, consultant, partner)
   - Besoin refresh auto (8x/jour vs manuel quotidien)
   - Volume données > 1GB (Free tier limite)

✅ Dépendance workflow:
   - Power BI devient tool quotidien (pas juste exploration)
   - Décisions business basées sur dashboards
   - Automation critique (alertes, rapports auto)
```

---

## 🎓 RESSOURCES D'APPRENTISSAGE (100% GRATUITES)

### Documentation officielle
- **Microsoft Learn:** https://learn.microsoft.com/power-bi
  - Parcours: "Get started with Power BI" (6h)
  - Parcours: "Create and use analytics reports" (8h)
  - Parcours: "Work with Power BI Desktop" (10h)

### Communauté & Forums
- **Power BI Community:** https://community.powerbi.com
  - Forum actif (réponses < 24h)
  - Galerie de templates (télécharger dashboards e-commerce)
- **Reddit:** r/PowerBI (55K membres)

### YouTube (gratuit)
- **Guy in a Cube:** Chaîne officielle Microsoft (500+ videos)
- **SQLBI:** Experts DAX (Alberto Ferrari, Marco Russo)
- **Curbal:** Ruth Pozuelo (DAX tutorials niveau débutant)

### Livres (PDFs gratuits)
- **"The Definitive Guide to DAX"** - SQLBI (1st edition gratuit)
- **"Introducing DAX"** - SQLBI (gratuit)
- Download: https://www.sqlbi.com/books/

### Practice datasets
- **Contoso sample database:** Dataset e-commerce Microsoft officiel
  - Products, Orders, Customers (2009-2024)
  - Parfait pour pratiquer avant vraies données Alpha Medical
  - Download: https://www.microsoft.com/en-us/download/details.aspx?id=18279

---

## 📊 TRACKING PROGRESSION (Self-Assessment)

### Checklist Compétences (cocher au fur et à mesure)

**Fondations:**
- [ ] Comprendre différence Dataset/Report/Dashboard
- [ ] Importer données (Excel, CSV, Google Sheets)
- [ ] Créer visualisations basiques (bar, line, pie charts)
- [ ] Utiliser filtres & slicers

**DAX Niveau 1:**
- [ ] Créer measures simples (SUM, AVERAGE, COUNT)
- [ ] Comprendre différence Calculated Column vs Measure
- [ ] Utiliser CALCULATE() pour filtrer contexte
- [ ] Time Intelligence (YTD, MTD, Last Month)

**DAX Niveau 2:**
- [ ] Iterator functions (SUMX, AVERAGEX)
- [ ] Créer mesures complexes (LTV, CAC, Churn)
- [ ] Variables (VAR) pour optimisation
- [ ] Context transition (row → filter)

**Dashboards:**
- [ ] Créer dashboard multi-pages (Acquisition, Conversion, etc.)
- [ ] Thème custom (Alpha Medical brand colors)
- [ ] Drillthrough & tooltips interactifs
- [ ] Performance optimization (< 3 sec load time)

**Automation:**
- [ ] Utiliser pbipy pour lister datasets
- [ ] Exécuter DAX queries via Python
- [ ] Automatiser refresh avec scripts
- [ ] Intégrer dans GitHub Actions workflow

**Total:** 20 compétences → Si 15+ cochées = Prêt pour Pro tier

---

## 💰 COÛT TOTAL APPRENTISSAGE

```yaml
Free tier (Mois 0-6):
- Power BI Free license: $0/mois × 6 = $0
- Microsoft Learn courses: $0
- YouTube tutorials: $0
- SQLBI books (gratuits): $0
- Temps investi: 100-150h sur 6 mois = 16-25h/mois
- Temps opportunity cost: $0 (parallèle au lancement, pas exclusif)

Total: $0 💰

Bénéfices:
- Maîtrise tool $10/mois (value = $120/an)
- Éviter consultants BI ($100-200/h) = $5,000-10,000 économisés
- Meilleure prise décision = $5,000-15,000 revenue incrémental/an
- ROI compétence: INFINI (coût $0, bénéfices $10K-25K/an)
```

---

## 🎯 PLAN DE DÉPLOIEMENT TIMELINE

**Approche réaliste (parallèle au lancement store):**

```
┌─────────────────────────────────────────────────────────┐
│ Mois 0-1 (PRE-LAUNCH): Fondations + Apprentissage      │
│ ├── Créer compte Power BI Free                         │
│ ├── Tutorials Microsoft Learn (5-10h)                   │
│ ├── Premier dataset (données fictives)                  │
│ └── Objectif: Comprendre interface & concepts           │
├─────────────────────────────────────────────────────────┤
│ Mois 1-3 (LAUNCH): Connexions + DAX Basique            │
│ ├── Connecter Google Sheets (leads scraping)           │
│ ├── Connecter Shopify (quand premiers orders)          │
│ ├── Apprendre DAX fondations (20-30h)                   │
│ ├── Créer 10 mesures basiques (Revenue, AOV, etc.)     │
│ └── Objectif: Analytics opérationnelles                 │
├─────────────────────────────────────────────────────────┤
│ Mois 3-6 (POST-LAUNCH): Dashboards + Automation        │
│ ├── Créer dashboards flywheel (4 phases)               │
│ ├── DAX avancé (LTV, CAC, cohorts)                      │
│ ├── Python automation (pbipy scripts)                   │
│ ├── GitHub Actions integration                          │
│ └── Objectif: BI infrastructure complète                │
├─────────────────────────────────────────────────────────┤
│ Mois 6-12 (GROWTH): Analyse Avancée + Upgrade Pro      │
│ ├── Attribution multi-touch                             │
│ ├── Predictive analytics (optionnel)                    │
│ ├── Partage dashboards avec équipe                      │
│ ├── Upgrade Pro si revenue > $10K/mois                  │
│ └── Objectif: Analytics-driven decision making          │
└─────────────────────────────────────────────────────────┘
```

**Temps hebdomadaire recommandé:** 4-6h/semaine (réaliste, pas overwhelming)

---

**PROCHAINE ACTION IMMÉDIATE:**

```bash
# 1. Créer compte Power BI Service (5 min)
open https://app.powerbi.com/home

# 2. Configuration Azure AD (déjà créé template .env.powerbi)
# Suivre instructions section "ÉTAPE 1" message précédent

# 3. Premier test connexion
python3 powerbi_connection_test.py

# 4. Commencer Microsoft Learn (2-3h)
open https://learn.microsoft.com/training/paths/get-started-power-bi/
```

**Status:** Learning path documenté ✅, Prêt à démarrer apprentissage Phase 1
