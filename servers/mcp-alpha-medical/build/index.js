"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const mcp_js_1 = require("@modelcontextprotocol/sdk/server/mcp.js");
const stdio_js_1 = require("@modelcontextprotocol/sdk/server/stdio.js");
const zod_1 = require("zod");
const dotenv = __importStar(require("dotenv"));
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
// Load environment variables from project root
dotenv.config({ path: path.join(__dirname, "../../../.env.admin") });
dotenv.config({ path: path.join(__dirname, "../../../.env") });
const server = new mcp_js_1.McpServer({
    name: "mcp-alpha-medical",
    version: "1.0.0"
});
// Helper: Read Pressure Matrix (Retention/Conversion Resource)
const GPM_PATH = path.join(__dirname, "../../../data/pressure-matrix.json");
function getGPM() {
    try {
        if (!fs.existsSync(GPM_PATH))
            return { error: "GPM File not found" };
        const data = fs.readFileSync(GPM_PATH, 'utf8');
        return JSON.parse(data);
    }
    catch (e) {
        return { error: e.message };
    }
}
// --- Acquisition Tools ---
server.tool("get_ad_performance", "Get ROAS and CTR from ad platforms", {
    platform: zod_1.z.enum(["meta", "google", "tiktok"]),
    period: zod_1.z.enum(["today", "yesterday", "last_7d", "last_30d"]).default("last_7d")
}, async ({ platform, period }) => {
    // Mock data for now as we don't have live Ad APIs yet
    // In reality this would fetch from Meta Graph API etc.
    const mockData = {
        meta: { roas: 3.2, ctr: 1.4, spend: 1200 },
        google: { roas: 4.5, ctr: 2.1, spend: 850 },
        tiktok: { roas: 2.1, ctr: 0.9, spend: 400 }
    };
    const data = mockData[platform] || {};
    return {
        content: [{ type: "text", text: JSON.stringify({ platform, period, ...data }, null, 2) }]
    };
});
// --- Conversion Tools ---
server.tool("get_conversion_metrics", "Get Store Conversion Rate and AOV from GPM", {}, async () => {
    const gpm = getGPM();
    // Fallback to reading specific sensors if GPM is empty
    // For Alpha Medical, we often store this in pressure-matrix.json
    const metrics = {
        cvr: "2.1%", // Placeholder / Mock until real sensor wire-up
        aov: "$65.00",
        pressure_score: gpm.global_score || "Unknown"
    };
    return {
        content: [{ type: "text", text: JSON.stringify(metrics, null, 2) }]
    };
});
server.tool("check_price_competitiveness", "Compare product price vs benchmarks", { product_id: zod_1.z.string() }, async ({ product_id }) => {
    // Read local catalog
    const CATALOG_PATH = path.join(__dirname, "../../../alpha_medical_complete_catalog.json");
    try {
        const catalog = JSON.parse(fs.readFileSync(CATALOG_PATH, 'utf8'));
        const product = catalog.products?.find((p) => p.id == product_id || p.handle == product_id);
        if (!product)
            return { content: [{ type: "text", text: "Product not found" }] };
        const price = parseFloat(product.price);
        const benchmark = price * 1.1; // Simulated competitor price
        const diff = ((price - benchmark) / benchmark * 100).toFixed(1);
        return {
            content: [{
                    type: "text", text: JSON.stringify({
                        product: product.title,
                        your_price: price,
                        market_avg: benchmark.toFixed(2),
                        competitiveness: `${diff}% vs Market`
                    }, null, 2)
                }]
        };
    }
    catch (e) {
        return { content: [{ type: "text", text: `Error: ${e.message}` }] };
    }
});
// --- Retention Tools ---
server.tool("get_pressure_matrix", "Get the current Global Pressure Matrix (GPM)", {}, async () => {
    const gpm = getGPM();
    return {
        content: [{ type: "text", text: JSON.stringify(gpm, null, 2) }]
    };
});
// --- Start Server ---
async function main() {
    const transport = new stdio_js_1.StdioServerTransport();
    await server.connect(transport);
    console.error("Alpha Medical MCP Server running on stdio");
}
main().catch((error) => {
    console.error("Server error:", error);
    process.exit(1);
});
