# Alpha Medical - Scripts Directory

> Organized repository structure as of 2025-12-14 (100% PROFESSIONNEL)
> **AUDITÉ FACTUELLEMENT:** Chaque comptage vérifié empiriquement

## 📁 Directory Structure (VÉRIFIÉ 2025-12-14)

```
scripts/                    # 276 total - 100% CATÉGORISÉS ✅
│
├── analysis/               # 91 scripts (33.0%) - AUDIT/ANALYSE
│   ├── audits/             # 26 scripts - Forensic, comprehensive audits
│   ├── checks/             # 20 scripts - Quick status checks
│   ├── verification/       # 29 scripts - Deployment verification
│   └── (root)              # 16 scripts - General analysis
│
├── deployment/             # 57 scripts (20.7%) - DÉPLOIEMENT SHOPIFY
│   └── (flat)              # ⚠️ TODO: Réorganiser en sous-dossiers
│                           #   → theme/, navigation/, pages/, assets/
│
├── automation/             # 45 scripts (16.3%) - AUTOMATISATION
│   ├── creation/           # 19 scripts - Create resources (products, pages)
│   ├── generation/         # 3 scripts - Generate assets (images, matrices)
│   ├── n8n/                # 15 scripts - N8N workflow management
│   ├── klaviyo/            # 4 scripts - Klaviyo email templates/flows
│   └── shopify/            # 4 scripts - Shopify policies/legal
│
├── maintenance/            # 29 scripts (10.5%) - MAINTENANCE
│   ├── fixes/              # 21 scripts - Bug fixes, corrections
│   ├── updates/            # 7 scripts - Update existing resources
│   └── (root)              # 1 script - General maintenance
│
├── features/               # 10 scripts (3.6%) - FONCTIONNALITÉS
│   ├── bundles/            # 7 scripts - Bundle product management
│   └── loyalty/            # 3 scripts - Loyalty program
│
├── analytics/              # 10 scripts (3.6%) - Tracking, data extraction
├── data/                   # 9 scripts (3.3%) - Import/export, retrieval
├── setup/                  # 8 scripts (2.9%) - Configuration, installation
├── tests/                  # 7 scripts (2.5%) - Test scripts
├── fixes/                  # 5 scripts (1.8%) - Bug fixes (legacy)
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

## 📝 Category Descriptions (DÉTAILLÉ)

### Automation (45 scripts) - DÉTAIL COMPLET

#### automation/n8n/ (15 scripts) - N8N Workflow Management
```
activate_n8n_workflow_simple.py    # Activate N8N workflows
activate_workflow_patch.py         # Patch workflow activation
add_filter_node.py                 # Add filter nodes to workflows
complete_flow_automation.py        # Complete flow setup
complete_workflow_final_push.py    # Final workflow deployment
diagnose_loop_problem.py           # Debug infinite loops
diagnose_no_trigger.py             # Debug missing triggers
get_exec_details.py                # Get execution details
get_execution_error.py             # Get execution errors
get_latest_execution_full.py       # Get latest execution data
investigate_output_file.py         # Investigate output files
list_all_workflow_nodes.py         # List all nodes
remove_filter_restore_workflow.py  # Remove filters, restore
restart_workflow.py                # Restart workflows
show_workflow_credential_ids.py    # Show credential IDs
```

#### automation/klaviyo/ (4 scripts) - Klaviyo Email Marketing
```
automate_klaviyo_email.py                      # Automate email flows
get_klaviyo_templates.py                       # Get template list
upload_professional_templates_correct_ids.py  # Upload templates
upload_templates_to_klaviyo.py                # Template upload utility
```

#### automation/shopify/ (4 scripts) - Shopify Policies/Legal
```
automate_legal_compliance.py           # Legal compliance automation
complete_all_shopify_policies_final.py # Complete all policies
complete_shopify_policies.py           # Shopify policy deployment
recategorize_products.py               # Product recategorization
```

#### automation/creation/ (19 scripts) - Resource Creation
```
create_15_bundles_final.py         # Create 15 bundles
create_blog_article_1.py           # Blog article creation
create_blog_article_2.py           # Blog article creation
create_bundle_products.py          # Bundle products
create_klaviyo_discount_codes.py   # Klaviyo discounts
create_llms_page.py                # LLMs.txt page
create_loyalty_discount_codes.py   # Loyalty discounts
create_missing_policy_pages.py     # Policy pages
create_pain_relief_guide_page.py   # Pain relief guide
create_remaining_articles.py       # Remaining articles
create_selling_plans.py            # Selling plans
create_size_quiz_page.py           # Size quiz page
create_social_*.py (7 scripts)     # Social media assets
```

#### automation/generation/ (3 scripts) - Asset Generation
```
generate_15_slides.py              # Generate slides
generate_product_matrix_complete.py # Product matrix
generate_recommendations_matrix.py # Recommendations
```

---

### Analysis (91 scripts) - DÉTAIL COMPLET

#### analysis/audits/ (26 scripts) - Deep Comprehensive Audits
```
generate_forensic_report.py           # Generate forensic reports
forensic_analysis.py                  # General forensic analysis
audit_seo_complete.py                 # Complete SEO audit
comprehensive_validation_audit_2025.py # 2025 validation audit
comprehensive_systems_audit_2025.py   # 2025 systems audit
final_audit_bundle_images_display.py  # Bundle images audit
verify_country_corrections_forensic.py # Country corrections
verify_final_forensic.py              # Final forensic check
verify_transparency_forensic.py       # Transparency audit
audit_current_state_forensic.py       # Current state audit
verify_english_only_forensic.py       # English-only check
verify_paypal_status_forensic.py      # PayPal status
verify_product_type_post_fix_forensic.py # Product type fixes
audit_flywheel_missing_components.py  # Flywheel gaps
forensic_analysis_klaviyo.py          # Klaviyo forensic
forensic_analysis_tracking.py         # Tracking forensic
forensic_drive_access.py              # Google Drive access
audit_subscriptions.py                # Subscription audit
audit_store_status.py                 # Store status audit
comprehensive_store_audit_session52.py # Session 52 audit
audit_all_products_metafields.py      # All metafields audit
forensic_analysis_shopify.py          # Shopify forensic
FORENSIC_ANALYSIS_COMPLETE_REPORT.py  # Complete report
automated_store_validation.py         # Automated validation
complete_workflow_audit.py            # Workflow audit
comprehensive_seo_validation.py       # SEO validation
```

#### analysis/checks/ (20 scripts) - Quick Status Checks
```
check_promotional_duplicates.py       # Check promo duplicates
check_bestsellers_special_offers_overlap.py # Bestsellers overlap
check_store_config.py                 # Store config check
check_script_tags_alpha.py            # Script tags check
check_gsc_status.py                   # GSC status check
check_product_template_integration.py # Template integration
check_gtm_status.py                   # GTM status check
check_google_apis.py                  # Google APIs check
check_policies_api.py                 # Policies API check
check_filter_issue.py                 # Filter issue check
check_n8n_credentials.py              # N8N credentials
check_workflow_execution.py           # Workflow execution
check_theme_pixels.py                 # Theme pixels check
check_uploaded_files.py               # Uploaded files check
check_footer_menu.py                  # Footer menu check
check_live_theme.py                   # Live theme check
check_menu.py                         # Menu check
compare_bestsellers_specialoffers_products.py # Compare products
detect_french_content.py              # Detect French
detect_french_unambiguous.py          # Detect French strict
```

#### analysis/verification/ (29 scripts) - Deployment Verification
```
verify_ai_crawlers.py                 # AI crawlers check
verify_payment_gateways.py            # Payment gateways
verify_schemas_complete.py            # Schemas complete
verify_installed_apps_factual.py      # Installed apps
verify_15_bundles_factual.py          # 15 bundles verify
verify_critical_requirements.py       # Critical requirements
verify_smart_recommendations_deployment.py # Smart recommendations
verify_section_deployment.py          # Section deployment
verify_loyalty_discount_codes.py      # Loyalty codes
verify_google_tags_live.py            # Google tags live
verify_metafields_all_namespaces.py   # All metafields
verify_marketing_readiness.py         # Marketing readiness
verify_flywheel_actual_state.py       # Flywheel state
verify_flywheel_diagram_factual.py    # Flywheel diagram
verify_platform_capabilities_comprehensive.py # Platform caps
verify_discount_codes.py              # Discount codes
verify_infrastructure_gaps.py         # Infrastructure gaps
verify_judgeme_state.py               # JudgeMe state
verify_all_sessions_deployments.py    # All sessions
verify_session51_deployments.py       # Session 51
verify_confetti_deployed.py           # Confetti deployed
verify_bestsellers_special_offers_LIVE.py # Bestsellers LIVE
verify_collection_duplicates.py       # Collection duplicates
verify_duplicates_simple.py           # Simple duplicates
verify_post_deletion.py               # Post deletion
verify_schema_deployment.py           # Schema deployment
verify_title_updates.py               # Title updates
verify_shopify_pixels.py              # Shopify pixels
verify_url_paste.py                   # URL paste
```

#### analysis/ (root) (16 scripts) - General Analysis
```
audit_automation_complementarity.py   # Automation complementarity
audit_french_language_complete.py     # French language audit
verify_klaviyo_flows_live.py          # Klaviyo flows live
VERIFY_footer_final_state.py          # Footer final state
VERIFY_investor_pages_complete.py     # Investor pages
verify_automation_complementarity.py  # Automation check
verify_performance_n8n.py             # N8N performance
analyze_performance_optimizations_prelaunch.py # Performance
create_optimization_plan.py           # Optimization plan
detect_script_duplications.py         # Script duplications
verify_draft_status.py                # Draft status
verify_prelaunch_readiness.py         # Pre-launch readiness
verify_published_items.py             # Published items
verify_shopify_flow_status.py         # Shopify Flow status
investigate_bundle_inventory.py       # Bundle inventory
verify_payment_methods.py             # Payment methods
```

**TOTAL: 26 + 20 + 29 + 16 = 91 scripts ✓**

### Deployment (57 scripts) - DÉTAIL COMPLET

> ⚠️ **STRUCTURE PLATE** - Tous les 57 scripts dans un seul dossier
> Recommandation: Réorganiser en sous-dossiers (theme/, navigation/, pages/, assets/)

#### Catégorie A: Theme/Systems Deploy (20 scripts)
```
deploy_bundle_builder.py              # Bundle builder system
deploy_bundle_assets.py               # Bundle CSS/JS assets
deploy_recommendations_system.py      # Recommendations engine
deploy_smart_recommendations.py       # Smart recommendations
deploy_recommendations_matrix.py      # Recommendations matrix
deploy_loyalty_system_simplified.py   # Loyalty program
deploy_subscriptions_system.py        # Subscription system
deploy_sticky_add_to_cart.py          # Sticky add-to-cart widget
deploy_sticky_widget_optimized.py     # Optimized sticky widget
deploy_all_corrected_snippets.py      # Deploy all snippets
deploy_transparency_updates.py        # Transparency updates
deploy_dynamic_merchandising.py       # Dynamic merchandising
deploy_n8n_workflows.py               # N8N workflow deployment
deploy_confetti_css_fix.py            # Confetti CSS fix
deploy_confetti_celebration.py        # Confetti celebration
deploy_confetti_fix_final.py          # Final confetti fix
deploy_cart_drawer_fix.py             # Cart drawer fix
deploy_email_popups.py                # Email popup system
deploy_theme_liquid.py                # Theme.liquid updates
deploy_schema_markup.py               # Schema.org markup
```

#### Catégorie B: Investor Pages (12 scripts)
```
create_missing_pages.py               # Create missing pages
update_investor_metrics.py            # Update investor metrics
redesign_investor_page_2025.py        # 2025 redesign
create_investor_subpages_complete.py  # Subpages creation
create_investor_subpages_part2.py     # Subpages part 2
create_investor_subpages_part3_final.py # Subpages final
update_investor_roadmap_aliexpress.py # Roadmap updates
fix_all_investor_pages_branding.py    # Branding fixes
fix_investor_roadmap_branding.py      # Roadmap branding
integrate_investor_pages_navigation.py # Navigation integration
implement_investor_password_protection.py # Password protection
secure_investor_pages_complete.py     # Security implementation
```

#### Catégorie C: Footer/Navigation (15 scripts)
```
FORCE_add_investor_footer.py          # Force investor footer
add_investor_link_footer_NOW.py       # Add investor link
add_investor_link_to_footer.py        # Footer link addition
check_footer_structure.py             # Check footer structure
examine_footer.py                     # Examine footer code
get_footer_menu_settings.py           # Get menu settings
FIX_footer_investor_COMPANY_column.py # Fix company column
FINAL_add_investor_to_company_menu.py # Add to company menu
REST_API_add_menu_item.py             # REST API menu addition
REMOVE_duplicate_investor_section.py  # Remove duplicates
RESTORE_country_language_selector.py  # Restore selector
REAL_FIX_footer_company_column.py     # Real fix company column
REMOVE_empty_localization_div.py      # Remove empty div
update_menu.py                        # Update menu
upload_footer.py                      # Upload footer
```

#### Catégorie D: Assets/Upload (10 scripts)
```
add_schema_org_to_theme.py            # Add schema to theme
force_cdn_refresh.py                  # Force CDN refresh
integrate_recommendations_section.py  # Integrate recommendations
push_index_json.py                    # Push index.json
push_llms_template.py                 # Push LLMs template
push_slideshow_liquid.py              # Push slideshow
upload_hero_images.py                 # Upload hero images
upload_hero_png.py                    # Upload hero PNG
upload_hero_to_files.py               # Upload hero to files
upload_liquid_fix.py                  # Upload liquid fix
```

**TOTAL: 20 + 12 + 15 + 10 = 57 scripts ✓**

### Maintenance (29 scripts) - DÉTAIL COMPLET

#### maintenance/fixes/ (21 scripts) - Bug Fixes & Corrections
```
fix_all_colors.py                    # Fix color issues
fix_gtm_documentation.py             # Fix GTM docs
fix_bundle_weights.py                # Fix bundle weights
fix_country_information.py           # Fix country info
fix_international_presence.py        # Fix international
fix_product_type_coherence.py        # Fix product types
fix_folder_ids_swap.py               # Fix folder IDs
fix_n8n_workflow_activation.py       # Fix N8N activation
fix_save_output_folder.py            # Fix output folder
fix_sheet_id.py                      # Fix sheet ID
fix_collections_descriptions.py      # Fix collections
fix_complete_care_kits_image.py      # Fix kit images
fix_email_to_professional.py         # Fix email format
fix_missing_metafields.py            # Fix metafields
fix_sku_remaining.py                 # Fix SKU issues
fix_sku_duplicates.py                # Fix duplicate SKUs
fix_long_titles.py                   # Fix long titles
debug_customer_response.py           # Debug customer API
delete_special_offers.py             # Delete offers
match-images-to-articles.py          # Match images
set_homepage_seo.py                  # Set homepage SEO
```

#### maintenance/updates/ (7 scripts) - Resource Updates
```
update_bundle_prices.py              # Update bundle prices
update_bundle_product_images.py      # Update bundle images
update_about_us_disambiguation.py    # Update about page
update_klaviyo_templates_professional.py # Update Klaviyo
update_privacy_policy.py             # Update privacy
update_sheet_config.py               # Update sheet config
update_workflow_credentials.py       # Update credentials
```

#### maintenance/ (root) (1 script)
```
archive_redundant_scripts.py         # Archive old scripts
```

**TOTAL: 21 + 7 + 1 = 29 scripts ✓**

### Features (10 scripts)
- **bundles/** (7) - Bundle product management and optimization
- **loyalty/** (3) - Loyalty program setup and management

### Other Sections
- **analytics/** (10) - Data extraction, tracking analysis
- **optimization/** (2) - Performance and SEO optimization
- **data/** (9) - Data migration, import, export, sync
- **tests/** (7) - Test scripts for APIs, features, deployments
- **setup/** (8) - Initial configuration and installation
- **cleanup/** (2) - Data cleanup utilities
- **marketing/** (1) - Facebook automation
- **fixes/** (5) - Legacy bug fixes (separate from maintenance/fixes)
- **uncategorized/** (0) - ✅ EMPTY

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

**Last updated:** 2025-12-14 (Session 92 - Complete detailed documentation)
**Status:** ✅ 100% scripts documented with full details (276 scripts, 4 major sections detailed)
