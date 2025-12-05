# Alpha Medical - Scripts Directory

> Organized repository structure as of 2025-12-05

## 📁 Directory Structure

```
scripts/
├── analysis/
│   ├── audits/          # Comprehensive audits and forensic analysis (30+ scripts)
│   ├── checks/          # Quick status checks (17 scripts)
│   └── verification/    # Verify deployments, configurations, data (44+ scripts)
├── automation/
│   ├── creation/        # Create products, collections, pages (24 scripts)
│   └── generation/      # Generate assets, content, configs (5 scripts)
├── deployment/          # Deploy changes to Shopify (23 scripts)
├── maintenance/
│   ├── fixes/           # Fix bugs, correct data (28 scripts)
│   └── updates/         # Update existing resources (7 scripts)
├── features/
│   ├── bundles/         # Bundle product management (11 scripts)
│   └── loyalty/         # Loyalty program scripts (3 scripts)
├── analytics/           # Tracking, analysis, data extraction (11 scripts)
├── optimization/        # Performance and SEO optimization (2 scripts)
├── data/                # Data migration and import/export (2 scripts)
├── tests/               # Test scripts (5 scripts)
├── setup/               # Configuration and installation (8 scripts)
└── uncategorized/       # Miscellaneous utilities (50 scripts)
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

## 📊 Statistics

- **Total scripts organized:** 265 files
- **Scripts in root (critical):** 15 files
- **Obsolete scripts archived:** 5 files
- **Original root directory:** 284 Python files
- **New root directory:** 15 Python files (95% reduction)

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
- **uncategorized/** - Miscellaneous utilities (to be categorized later)

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
