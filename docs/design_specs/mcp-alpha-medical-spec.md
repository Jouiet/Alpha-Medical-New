# 🏗️ MCP-Alpha-Medical: Custom Server Specification

**Status:** DRAFT
**Version:** 1.0.0
**Date:** 2026-01-23

## 🎯 Objective

Create a custom Model Context Protocol (MCP) server (`mcp-alpha-medical`) to act as the "Neural Backbone" for the Alpha Medical Flywheel. It will expose specialized granular tools to the AI agent to manage the **Acquisition → Conversion → Retention → Advocacy** lifecycle programmatically.

## 🛠️ Tech Stack

- **Language:** TypeScript (Node.js)
- **Transport:** Stdio / SSE
- **Dependencies:** `@modelcontextprotocol/sdk`, `zod`, `axios`, `dotenv`

## 🧩 Core Resources & Tools (The Flywheel)

### 1. Acquisition (Traffic & Ads)

* `get_ad_performance(platform, period)`: Aggregates ROAS/CTR.
- `audit_seo_health(url)`: Checks meta tags/JSON-LD.

### 2. Conversion (Shopify store & CRO)

* **Resources:** `shopify://products/low_stock`
- **Tools:**
  - `get_conversion_metrics()`: Fetches CVR, AOV.
  - `check_price_competitiveness(product_id)`: Comparse prices.

### 3. Retention (Klaviyo & Support)

* `get_flow_performance(flow_id)`: Opens/Clicks.
- `get_pressure_matrix()`: Reads `data/pressure-matrix.json`.

### 4. Advocacy (Social & Reviews)

* `get_review_sentiment()`: Recent reviews analysis.
- `draft_response_to_review(review_id, tone)`: Prepares reply.

## 📂 Directory Structure

```
servers/mcp-alpha-medical/
├── package.json
├── index.ts
└── src/
    ├── flywheels/
    └── lib/
```

## 🚀 Implementation Steps

1. **Scaffold**: Initialize TS project.
2. **Core Setup**: Implement `McpServer`.
3. **Sensor Integration**: Port logic from `.cjs` sensors.
4. **Tool Registration**: Register defined tools.
