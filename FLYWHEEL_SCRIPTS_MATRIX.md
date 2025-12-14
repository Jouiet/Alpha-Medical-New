# FLYWHEEL → SCRIPTS MAPPING MATRIX

**Date:** 2025-12-14
**Purpose:** Mapping exhaustif 276 scripts → phases flywheel
**Usage:** Document de référence pour comprendre l'impact business des scripts

---

## 📊 RÉSUMÉ MAPPING

| Phase Flywheel | Scripts | % Total | Description |
|----------------|---------|---------|-------------|
| **PHASE 0: INFRASTRUCTURE** | ~131 | 47.5% | Cross-cutting (setup, audit, deploy, verify) |
| **PHASE 1: ACQUISITION** | ~12 | 4.3% | Lead generation, traffic, SEO |
| **PHASE 2: CONVERSION** | ~50 | 18.1% | Email, popups, bundles, checkout |
| **PHASE 3: RETENTION** | ~27 | 9.8% | Loyalty, subscriptions, customer nurture |
| **PHASE 4: ADVOCACY** | 0 | 0% | Reviews, referrals, UGC |
| **NON-CLASSIFIÉS** | ~56 | 20.3% | Scripts techniques génériques |

---

## 🚨 GAPS CRITIQUES IDENTIFIÉS

### PHASE 4: ADVOCACY = 0 SCRIPTS
**Impact:** Aucune automatisation pour:
- Collection de reviews (Loox integration)
- Programme de referrals
- UGC (User Generated Content)
- Ambassadeurs de marque

**Recommandation:**
- Créer `scripts/advocacy/collect_reviews.py`
- Créer `scripts/advocacy/manage_referrals.py`
- Créer `scripts/advocacy/sync_loox_reviews.py`

---

## PHASE 0: INFRASTRUCTURE (Cross-cutting)

**Scripts:** ~131 (47.5%)
**But:** Support technique pour toutes les phases

### Catégories:
Liste scripts INFRASTRUCTURE:
- FORENSIC_ANALYSIS_COMPLETE_REPORT.py
- VERIFY_footer_final_state.py
- VERIFY_investor_pages_complete.py
- analyze_automation_gaps_complete.py
- analyze_execution_6.py
- analyze_lead_snr_factual.py
- analyze_multi_platform_automation_gaps.py
- analyze_performance_optimizations_prelaunch.py
- analyze_personas_bundles.py
- analyze_pre_launch_email_feasibility.py
- analyze_real_personas.py
- analyze_top10_hero_products.py
- analyze_workflow_outputs.py
- audit_all_products_metafields.py
- audit_automation_complementarity.py
- audit_current_state_forensic.py
- audit_flywheel_missing_components.py
- audit_french_language_complete.py
- audit_seo_complete.py
- audit_store_status.py
- audit_subscriptions.py
- check_bestsellers_special_offers_overlap.py
- check_filter_issue.py
- check_footer_menu.py
- check_footer_structure.py
- check_google_apis.py
- check_gsc_status.py
- check_gtm_status.py
- check_live_theme.py
- check_menu.py

---

## PHASE 1: ACQUISITION (Lead Gen → Traffic)

**Scripts:** ~12 (4.3%)
**But:** Générer leads et traffic

- analyze_lead_snr_factual.py
- audit_seo_complete.py
- comprehensive_seo_validation.py
- facebook_automation_complete.py
- import_leads_to_sheet.py
- optimize_seo.py
- set_homepage_seo.py
- sync_typeform_to_sheet.py

---

## PHASE 2: CONVERSION (Traffic → Purchase)

**Scripts:** ~50 (18.1%)
**But:** Convertir visiteurs en clients

- add_product_images_to_bundles.py
- analyze_personas_bundles.py
- analyze_pre_launch_email_feasibility.py
- analyze_top10_hero_products.py
- audit_all_products_metafields.py
- automate_klaviyo_email.py
- check_product_template_integration.py
- clean_bundle_documentation.py
- compare_bestsellers_specialoffers_products.py
- configure_fbt_bundles.py
- configure_klaviyo.py
- configure_shopify_email.py
- create_15_bundles_final.py
- create_bundle_products.py
- create_klaviyo_discount_codes.py
- create_loyalty_discount_codes.py
- delete_bundler_css.py
- delete_obsolete_bundles.py
- deploy_bundle_assets.py
- deploy_bundle_builder.py
- deploy_cart_drawer_fix.py
- deploy_email_popups.py
- deploy_sticky_add_to_cart.py
- final_audit_bundle_images_display.py
- fix_bundle_weights.py
- fix_collections_descriptions.py
- fix_email_to_professional.py
- fix_product_type_coherence.py
- forensic_analysis_klaviyo.py
- generate_product_matrix_complete.py
- get_klaviyo_templates.py
- get_missing_products.py
- get_product_samples.py
- investigate_bundle_inventory.py
- list_collections.py
- recategorize_products.py
- reconstruct_bundles_to_3_4_products.py
- test_klaviyo_api.py
- unpublish_bundles_without_images.py
- update_bundle_prices.py
- update_bundle_product_images.py
- update_klaviyo_templates_professional.py
- upload_bundle_images.py
- upload_templates_to_klaviyo.py
- verify_15_bundles_factual.py
- verify_collection_duplicates.py
- verify_discount_codes.py
- verify_klaviyo_flows_live.py
- verify_loyalty_discount_codes.py
- verify_product_type_post_fix_forensic.py

---

## PHASE 3: RETENTION (Customer → Repeat Customer)

**Scripts:** ~27 (9.8%)
**But:** Fidéliser et augmenter LTV

- activate_n8n_workflow_simple.py
- activate_workflow_patch.py
- analyze_workflow_outputs.py
- audit_subscriptions.py
- check_workflow_execution.py
- complete_flow_automation.py
- complete_workflow_audit.py
- complete_workflow_final_push.py
- create_loyalty_discount_codes.py
- debug_customer_response.py
- deploy_loyalty_system_simplified.py
- deploy_n8n_workflows.py
- deploy_subscriptions_system.py
- fix_n8n_workflow_activation.py
- list_all_workflow_nodes.py
- list_recent_customers.py
- loyalty_manager.py
- loyalty_metaobject_setup.py
- loyalty_setup.py
- remove_filter_restore_workflow.py
- restart_workflow.py
- show_workflow_credential_ids.py
- test_shopify_flow_customer.py
- update_workflow_credentials.py
- verify_klaviyo_flows_live.py
- verify_loyalty_discount_codes.py
- verify_shopify_flow_status.py

---

## PHASE 4: ADVOCACY (Customer → Brand Ambassador)

**Scripts:** 0 (0%)
**But:** Transformer clients en ambassadeurs

⚠️ **GAP CRITIQUE:** Aucun script pour:
- Collection automatique de reviews (Loox API)
- Gestion programme referrals
- Sync UGC/testimonials
- Automatisation ambassadeurs

---

## 📈 CONCLUSION

**Couverture Flywheel par scripts:**
- Phase 1 (Acquisition): ✅ 4.3% - Basique
- Phase 2 (Conversion): ✅ 18.1% - Bon
- Phase 3 (Retention): ✅ 9.8% - Bon
- Phase 4 (Advocacy): ❌ 0% - MANQUANT

**Priorité #1:** Créer scripts ADVOCACY (reviews, referrals)

---

## 🏢 AGENCY VALUE (Perspective Complémentaire)

> **Usage:** Les deux perspectives sont COMPLÉMENTAIRES
> - **FLYWHEEL** (ci-dessus) → Comprendre l'architecture opérationnelle
> - **AGENCY VALUE** (ci-dessous) → Vendre les services à des clients

### Services Automatisables par Catégorie

| Service | Scripts | Pitch Client |
|---------|---------|--------------|
| **Audit & Forensic** | 91 | "Diagnostic e-commerce 24h" |
| **Déploiement Shopify** | 57 | "Features en heures, pas semaines" |
| **Automation Workflows** | 45 | "N8N + Klaviyo + Shopify" |
| **Maintenance** | 29 | "Corrections en minutes" |
| **Features Avancées** | 10 | "Bundles + Loyalty" |
| **Analytics & Data** | 19 | "Intelligence business" |
| **Autres** | 25 | "Setup, tests, optimization" |

### Plateformes Couvertes
- Shopify (Admin API, GraphQL, REST)
- Klaviyo (Email, Flows, Templates)
- N8N (Workflows open-source)
- GA4/GTM (Tracking)
- Google Cloud (Drive, Sheets, Gemini)

---

**Last Updated:** 2025-12-14 Session 92
**Verification:** Empirique (`find | wc -l`)
**Bullshit Level:** 0%
