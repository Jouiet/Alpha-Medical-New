# ADVANCED RETRIEVAL PATTERNS - ALPHA MEDICAL

> **Purpose:** Practical patterns for optimal context loading
> **Efficiency:** 85-90% token savings using these patterns
> **Status:** ✅ Production-Ready
> **Date:** 2025-11-26

---

## 🎯 CORE PRINCIPLE

**Don't load what you don't need. Load only what's relevant.**

Traditional approach: Load entire files → 50,000-100,000 tokens
Advanced approach: Load specific chunks → 5,000-15,000 tokens
**Savings:** 70-90%

---

## 📋 PATTERN CATALOG

### Pattern 1: Progressive Loading

**Use When:** You're not sure which context you need yet

**Strategy:**
1. Load Level 1 (core memory) - ~1,000 tokens
2. Assess task type
3. Load Level 2 (domain-specific) - ~1,200 tokens
4. If needed, load specific Level 3 chunks - ~5,000-10,000 tokens

**Example:**
```
User: "Help me improve SEO for the blog"

Step 1: Level 1 loaded automatically (metadata + constraints)
Step 2: Assess → SEO task → Load 03-marketing-context.md
Step 3: Need details → Load AI_SEO_MARKETING... chunk seo-03-onpage
Total: ~9,000 tokens instead of 65,000 (86% savings)
```

---

### Pattern 2: Chunk-Specific Loading

**Use When:** You know exactly what topic you need

**Strategy:**
1. Reference `.claude/SEMANTIC_CHUNKS_MANIFEST.json`
2. Identify relevant chunk ID
3. Load only that chunk (specific lines)

**Example:**
```bash
# Task: Debug GitHub Actions workflow

# Instead of:
Read(file_path: "market-analysis/AUTOMATION_COMPLETE_WORKFLOWS.md")
# → Loads 5,962 lines (~45,000 tokens)

# Do this:
# 1. Check manifest → chunk "auto-03-github-actions" = lines 1501-2500
# 2. Load only that chunk:
Read(file_path: "market-analysis/AUTOMATION_COMPLETE_WORKFLOWS.md", offset: 1501, limit: 1000)
# → Loads 1,000 lines (~9,000 tokens)

# Savings: 80%
```

---

### Pattern 3: Agent-Mediated Loading

**Use When:** Complex domain-specific task

**Strategy:**
1. Invoke specialized agent (seo-specialist, automation-specialist, marketing-specialist)
2. Agent auto-loads only relevant context
3. Saves 70% tokens vs manual loading

**Example:**
```bash
# Task: Create email welcome flow

# Instead of:
@03-marketing-context.md  # ~1,200 tokens
@KLAVIYO_WELCOME_FLOW_IMPLEMENTATION.md  # ~8,000 tokens
@market-analysis/AUTOMATION_COMPLETE_WORKFLOWS.md (chunk auto-06-klaviyo)  # ~9,000 tokens
# Total: ~18,000 tokens

# Do this:
Task(subagent_type: "marketing-specialist", prompt: "Create Klaviyo welcome flow")
# Agent loads only necessary sections
# Total: ~5,000-7,000 tokens

# Savings: 60-70%
```

---

### Pattern 4: Hybrid Search (Future with MCP)

**Use When:** Semantic search needed (MCP server implemented)

**Strategy:**
1. Semantic search for relevant chunks
2. Load only top 2-3 results
3. Combine with keyword filtering

**Example:**
```bash
# Task: "How to fix abandoned cart recovery?"

# MCP search returns:
# 1. KLAVIYO_ABANDONED_CART_FLOW... (relevance: 0.95)
# 2. AUTOMATION_COMPLETE_WORKFLOWS.md chunk auto-06-klaviyo (relevance: 0.88)

# Load only those 2 → ~12,000 tokens instead of 45,000+
# Savings: 73%
```

---

### Pattern 5: Context Caching

**Use When:** Multi-turn conversation on same topic

**Strategy:**
1. Load relevant context once
2. Reference it in subsequent turns (Claude remembers within session)
3. Don't reload unnecessarily

**Example:**
```
Turn 1:
User: "Optimize homepage meta description"
Assistant: [Loads SEO chunk seo-03-onpage]
Response: "Here's the optimized meta..."

Turn 2:
User: "Now do the same for product pages"
Assistant: [Context already loaded, no reload needed]
Response: "Based on the same SEO principles..."

# Savings: 50% on turn 2+ (no reload)
```

---

### Pattern 6: Lazy Loading

**Use When:** Exploratory tasks where exact need is unclear

**Strategy:**
1. Start with minimal context (Level 1 only)
2. Load additional context only when explicitly needed
3. Ask user before loading large chunks

**Example:**
```
User: "Help with email automation"```
User: "Help with email automation"