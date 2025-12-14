# Alpha Medical - Scripts Directory

> Organized repository structure as of 2025-12-14 (100% PROFESSIONNEL)

## 📁 Directory Structure

```
scripts/                    # 276 total - 100% CATÉGORISÉS ✅
├── analysis/               # 91 scripts (33.0%)
│   ├── audits/             # 27 scripts - Forensic, validation, comprehensive
│   ├── checks/             # 21 scripts - Quick status checks
│   └── verification/       # 43 scripts - Deployment verification
├── deployment/             # 57 scripts (20.7%) - Theme, assets, schema
├── automation/             # 45 scripts (16.3%)
│   ├── creation/           # 22 scripts - Products, collections, pages
│   ├── generation/         # 5 scripts - Assets, content, configs
│   ├── n8n/                # 15 scripts - N8N workflow management
│   ├── klaviyo/            # 4 scripts - Klaviyo templates, flows
│   └── shopify/            # 4 scripts - Shopify policies, legal
├── maintenance/            # 29 scripts (10.5%)
│   ├── fixes/              # Fix bugs, correct data
│   └── updates/            # Update existing resources
├── features/               # 10 scripts (3.6%)
│   ├── bundles/            # Bundle product management
│   └── loyalty/            # Loyalty program
├── analytics/              # 10 scripts (3.6%) - Tracking, data extraction
├── data/                   # 9 scripts (3.3%) - Import/export, retrieval
├── setup/                  # 8 scripts (2.9%) - Configuration, installation
├── tests/                  # 7 scripts (2.5%) - Test scripts
├── fixes/                  # 5 scripts (1.8%) - Bug fixes
├── optimization/           # 2 scripts (0.7%) - Performance, SEO
├── cleanup/                # 2 scripts (0.7%) - Data cleanup
├── marketing/              # 1 script (0.4%) - Facebook automation
├── uncategorized/          # 0 scripts ✅ ZÉRO
└── racine/                 # 0 scripts ✅ ZÉRO
```

## 🚨 Critical Scripts (Root Directory)

**These scripts MUST remain in root directory** (referenced in GitHub Actions workflows):

### GitHub Actions Workflows:
- `clean_and_segment_leads.py` - Clean and segment lead data
- `sync_facebook_leads_to_sheet.py` - Sync Facebook leads to Google Sheets
- `sync_klaviyo_to_sheet.py` - Sync Klaviyo leads to Google Sheets
- `sync_shopify_forms_to_sheet.py` - Sync Shopify forms to Google Sheets
- `generate_llms_full.py` - Generate complete LLMs.txt file
- `generate_llms_txt.py` - Generate lightweight LLMs.txt
- `validate_llms_txt.py` - Validate LLMs.txt format

### Infrastructure/Audit Tools:
- `audit_forensic_complete_v2.py` - Complete forensic audit
- `audit_infrastructure.py` - Infrastructure health check
- `verify_store_infrastructure.py` - Store infrastructure verification

### Migration Tools (can be archived after session):
- `standardize_api_versions.py` - API version standardization
- `categorize_scripts.py` - Script categorization analysis
- `identify_obsolete_scripts.py` - Identify obsolete scripts
- `migrate_scripts_safe.py` - Safe migration planner
- `execute_migration.py` - Execute migration

## 📊 Statistics (Updated 2025-12-14)

- **Total scripts:** 276 files
- **Scripts categorized:** 276 files (100%) ✅
- **Scripts uncategorized:** 0 files ✅
- **New categories added:** automation/n8n (15), automation/klaviyo (4), automation/shopify (4)

## 🎯 Usage Guidelines

### Running Scripts from New Locations

**From root directory:**
```bash
# Critical workflow scripts (no change)
python3 clean_and_segment_leads.py

# Organized scripts (use full path)
python3 scripts/analysis/audits/audit_forensic_complete_v2.py
python3 scripts/deployment/deploy_bundle_builder.py
python3 scripts/maintenance/fixes/fix_missing_collections.py
```

**Adding scripts to PATH:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$PATH:$HOME/Desktop/Alpha-Medical/scripts"

# Then run from anywhere
audit_forensic_complete_v2.py
```

### Finding Scripts

**By category:**
```bash
ls scripts/analysis/audits/          # All audit scripts
ls scripts/deployment/               # All deployment scripts
ls scripts/maintenance/fixes/        # All fix scripts
```

**By pattern:**
```bash
find scripts/ -name "*bundle*"       # All bundle-related scripts
find scripts/ -name "verify_*"       # All verification scripts
find scripts/ -name "deploy_*"       # All deployment scripts
```

**By content:**
```bash
grep -r "SHOPIFY_API" scripts/       # Scripts using Shopify API
grep -r "klaviyo" scripts/           # Scripts using Klaviyo
```

## 🗄️ Archived Scripts

**Location:** `archive/obsolete-scripts-2025-12-05/`

**Archived scripts (obsolete):**
- `diagnose_confetti.py` - Old debugging script
- `deploy_bundle_ctas_phase1.py` - Old one-time deployment
- `upload_favicon.py` - Old one-time deployment
- `push_theme_fixes_to_shopify.py` - Old deployment script
- `push_size_quiz_to_shopify.py` - Old deployment script

**Restore if needed:**
```bash
cp archive/obsolete-scripts-2025-12-05/script_name.py ./
```

## 📝 Category Descriptions

### Analysis
- **audits/** - Deep comprehensive audits using API + code inspection
- **checks/** - Quick status checks (theme, config, data)
- **verification/** - Verify deployments, changes, data integrity

### Automation
- **creation/** - Create new resources (products, pages, collections)
- **generation/** - Generate assets (images, configs, matrices)
- **n8n/** - N8N workflow management (activate, diagnose, restart)
- **klaviyo/** - Klaviyo templates and flows management
- **shopify/** - Shopify policies and legal compliance

### Deployment
- Deploy theme changes, snippets, sections to Shopify

### Maintenance
- **fixes/** - One-time or recurring bug fixes
- **updates/** - Update existing resources (prices, images, policies)

### Features
- **bundles/** - Bundle product management and optimization
- **loyalty/** - Loyalty program setup and management

### Other
- **analytics/** - Data extraction, tracking analysis
- **optimization/** - Performance and SEO optimization
- **data/** - Data migration, import, export, sync
- **tests/** - Test scripts for APIs, features, deployments
- **setup/** - Initial configuration and installation
- **cleanup/** - Data cleanup utilities
- **marketing/** - Marketing automation (Facebook)
- **uncategorized/** - ✅ EMPTY (0 scripts - fully organized)

## ⚠️ Important Notes

1. **GitHub Actions Dependency:** Never move scripts from root if they're referenced in `.github/workflows/*.yml`
2. **Import Statements:** Scripts are self-contained (no local imports), so moving doesn't break dependencies
3. **Market Analysis:** Scripts in `market-analysis/` directory were not moved (already organized)
4. **API Version:** All scripts now use `API_VERSION = "2025-10"` (latest stable as of 2025-12-05)

## 🔄 Migration History

**Date:** 2025-12-05
**Reason:** P0-DAY3 repository cleanup (Pre-launch task)
**Result:**
- Root directory: 284 → 15 files (95% reduction)
- Organized: 265 files into logical categories
- Archived: 5 obsolete files
- Zero regressions (all GitHub Actions workflows functional)

---

**Last updated:** 2025-12-05
**Status:** ✅ Migration complete and verified
