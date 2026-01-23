#!/usr/bin/env node
/**
 * Alpha Medical - Klaviyo Email Performance Sensor
 *
 * Role: Non-agentic data fetcher. Monitors email marketing health.
 * Metrics: List growth, Campaign performance, Flow activity
 *
 * Adapted from 3A Automation for Alpha Medical
 * Version: 1.0.0 | Session 143 | 23/01/2026
 */

const fs = require('fs');
const path = require('path');

// Load environment variables from Alpha Medical .env files
const envPaths = [
    path.join(__dirname, '../.env.admin'),
    path.join(__dirname, '../.env'),
    path.join(process.cwd(), '.env.admin'),
    path.join(process.cwd(), '.env')
];

for (const envPath of envPaths) {
    if (fs.existsSync(envPath)) {
        require('dotenv').config({ path: envPath });
    }
}

// Alpha Medical pressure matrix path
const GPM_PATH = path.join(__dirname, '../data/pressure-matrix.json');

async function klaviyoRequest(endpoint, apiKey) {
    const response = await fetch(`https://a.klaviyo.com/api/${endpoint}`, {
        headers: {
            'Authorization': `Klaviyo-API-Key ${apiKey}`,
            'revision': '2024-02-15',
            'Accept': 'application/json'
        }
    });
    if (!response.ok) throw new Error(`Klaviyo API Error: ${response.status}`);
    return response.json();
}

async function getEmailMetrics(apiKey) {
    const metrics = {
        lists: { total: 0, totalProfiles: 0 },
        flows: { total: 0, active: 0 },
        campaigns: { recent: 0 }
    };

    try {
        // Get lists
        const listsData = await klaviyoRequest('lists/', apiKey);
        metrics.lists.total = listsData.data?.length || 0;

        // Get flows
        const flowsData = await klaviyoRequest('flows/', apiKey);
        metrics.flows.total = flowsData.data?.length || 0;
        metrics.flows.active = flowsData.data?.filter(f => f.attributes?.status === 'live').length || 0;

        // Get recent campaigns (last 30 days)
        const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
        const campaignsData = await klaviyoRequest(`campaigns/?filter=greater-or-equal(created_at,${thirtyDaysAgo})`, apiKey);
        metrics.campaigns.recent = campaignsData.data?.length || 0;

    } catch (e) {
        console.error(`Klaviyo API Error: ${e.message}`);
    }

    return metrics;
}

function calculatePressure(metrics) {
    let pressure = 0;

    // No active flows = high pressure
    if (metrics.flows.active === 0) pressure += 40;
    else if (metrics.flows.active < 3) pressure += 20;

    // No recent campaigns = medium pressure
    if (metrics.campaigns.recent === 0) pressure += 25;
    else if (metrics.campaigns.recent < 2) pressure += 10;

    // Few lists = setup incomplete
    if (metrics.lists.total < 2) pressure += 15;

    return Math.min(pressure, 100);
}

function updateGPM(pressure, metrics) {
    // Ensure data directory exists
    const dataDir = path.dirname(GPM_PATH);
    if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
    }

    let gpm = {};
    if (fs.existsSync(GPM_PATH)) {
        gpm = JSON.parse(fs.readFileSync(GPM_PATH, 'utf8'));
    }

    gpm.store = 'Alpha Medical';
    gpm.sectors = gpm.sectors || {};
    gpm.sectors.marketing = gpm.sectors.marketing || {};
    gpm.sectors.marketing.klaviyo = {
        pressure: pressure,
        trend: pressure > (gpm.sectors.marketing.klaviyo?.pressure || 0) ? 'UP' : 'DOWN',
        last_check: new Date().toISOString(),
        sensor_data: {
            lists_total: metrics.lists.total,
            flows_total: metrics.flows.total,
            flows_active: metrics.flows.active,
            campaigns_last_30d: metrics.campaigns.recent
        }
    };

    // Calculate overall pressure
    const sectors = Object.values(gpm.sectors || {});
    const allPressures = [];
    for (const sector of sectors) {
        for (const [key, value] of Object.entries(sector)) {
            if (value && typeof value.pressure === 'number') {
                allPressures.push(value.pressure);
            }
        }
    }
    gpm.overall_pressure = allPressures.length > 0
        ? Math.round(allPressures.reduce((a, b) => a + b, 0) / allPressures.length)
        : pressure;

    gpm.last_updated = new Date().toISOString();
    fs.writeFileSync(GPM_PATH, JSON.stringify(gpm, null, 2));

    console.log(`📡 GPM Updated: Klaviyo Pressure is ${pressure}`);
    console.log(`   Lists: ${metrics.lists.total}, Flows: ${metrics.flows.active}/${metrics.flows.total} active`);
    console.log(`   Campaigns (30d): ${metrics.campaigns.recent}`);
}

async function main() {
    // Health check mode
    if (process.argv.includes('--health')) {
        console.log('✅ Klaviyo Sensor: OK');
        console.log(`   API Key: ${process.env.KLAVIYO_PRIVATE_API_KEY ? 'Set' : 'Missing'}`);
        process.exit(0);
    }

    const apiKey = process.env.KLAVIYO_PRIVATE_API_KEY || process.env.KLAVIYO_API_KEY;

    if (!apiKey) {
        console.log('⚠️ Klaviyo API key missing. Reporting CRITICAL GAP.');
        updateGPM(95, { lists: { total: 0 }, flows: { total: 0, active: 0 }, campaigns: { recent: 0 } });
        return;
    }

    try {
        console.log('📧 Fetching Klaviyo email metrics...');
        const metrics = await getEmailMetrics(apiKey);
        const pressure = calculatePressure(metrics);
        updateGPM(pressure, metrics);
    } catch (e) {
        console.error(`❌ Klaviyo Sensor Failure: ${e.message}`);
        updateGPM(80, { lists: { total: 0 }, flows: { total: 0, active: 0 }, campaigns: { recent: 0 } });
    }
}

main();
