# ALPHA MEDICAL - CORE MEMORY

**Project:** B2C e-commerce RETAILER - Medical equipment (alphamedical.shop)
**Status:** PRE-LAUNCH (Launch: 2025-12-25) | Health: 94/100 🟢
**Last Updated:** 2025-12-06 Session 81 (System Optimization 82→100/100)

---

## SYSTEM ARCHITECTURE

Progressive disclosure memory system (3 levels):

**Level 1 (Auto-loaded):**
- @.claude/memory/00-metadata.md - Project essence, business model
- @.claude/memory/01-core-constraints.md - Non-negotiable rules

**Level 2 (Domain-specific - load when needed):**
- @agent_docs/infrastructure-summary.md - Technical context, automation state
- @agent_docs/marketing-context.md - Marketing strategy, campaigns
- @agent_docs/automation-workflows.md - Shopify/Klaviyo/GitHub workflows
- @agent_docs/brand-guidelines.md - Visual identity, messaging framework
- @agent_docs/seo-strategy.md - SEO/content optimization strategy
- @agent_docs/personas.md - Target audience, market research
- @agent_docs/apis-tools.md - Available APIs, MCP tools, credentials

**Level 3 (Deep knowledge - load explicitly):**
- @INFRASTRUCTURE_AUDIT_CHECKLIST.md - Single source of truth (2,184 lines)
- @FLYWHEEL_OPTIMIZATION_BLUEPRINT_2025.md - Complete flywheel strategy

---

## SPECIALIZED AGENTS (70% Context Savings)

Auto-activate via UserPromptSubmit hook (`.claude/hooks/user-prompt-submit.sh`):
- @seo-specialist - SEO optimization, meta descriptions, content
- @automation-specialist - Shopify Flow, GitHub Actions, APIs
- @marketing-specialist - Email flows, ad copy, campaigns

---

## OPERATIONAL BOUNDARIES

**✅ ALWAYS DO:** Update docs, verify facts, test small datasets
**⚠️ ASK FIRST:** Modify Shopify workflows, create campaigns, change themes
**🚫 NEVER DO:** Touch prices/inventory, commit credentials

---

**Hooks:** pre-tool-use.sh (constraint enforcement) + post-tool-use.sh (auto-documentation)
**Single Source of Truth:** @INFRASTRUCTURE_AUDIT_CHECKLIST.md
**Zero Tolerance:** No bullshit, no wishful thinking, only verified facts
