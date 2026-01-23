#!/usr/bin/env node
/**
 * Alpha Medical - GA4 Situational Receptor (Sensor)
 *
 * Role: Non-agentic data fetcher. Updates GPM pressure based on marketing ROI.
 * Purpose: Decouples "Observation" from "Reasoning" to save tokens.
 *
 * Transferred from 3A via Technology Shelf (Étagère Technologique)
 * Original: 3A automations/agency/core/ga4-sensor.cjs
 * Version: 1.0.0 | Session 144 | 23/01/2026
 */

const fs = require('fs');
const path = require('path');

// Load environment variables from Alpha Medical .env files
const envPaths = [
    path.join(__dirname, '../.env'),
    path.join(__dirname, '../.env.admin'),
    path.join(process.cwd(), '.env')
];

for (const envPath of envPaths) {
    if (fs.existsSync(envPath)) {
        require('dotenv').config({ path: envPath });
    }
}

// Alpha Medical pressure matrix path
const GPM_PATH = path.join(__dirname, '../data/pressure-matrix.json');
const STORE_ID = 'alpha-medical';

// Check for Google Analytics Data API
let BetaAnalyticsDataClient;
try {
    BetaAnalyticsDataClient = require('@google-analytics/data').BetaAnalyticsDataClient;
} catch (e) {
    BetaAnalyticsDataClient = null;
}

async function fetchGA4Data(propertyId) {
    if (!BetaAnalyticsDataClient) {
        throw new Error('GA4 SDK not installed. Run: npm install @google-analytics/data');
    }

    if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
        throw new Error('GOOGLE_APPLICATION_CREDENTIALS not set');
    }

    const analyticsDataClient = new BetaAnalyticsDataClient();
    const [response] = await analyticsDataClient.runReport({
        property: `properties/${propertyId}`,
        dateRanges: [{ startDate: '7daysAgo', endDate: 'yesterday' }],
        dimensions: [{ name: 'sessionSource' }],
        metrics: [
            { name: 'sessions' },
            { name: 'conversions' },
            { name: 'totalRevenue' },
            { name: 'advertiserAdCost' }
        ],
    });

    return response.rows ? response.rows.map(row => ({
        source: row.dimensionValues[0].value,
        sessions: parseInt(row.metricValues[0].value),
        conversions: parseInt(row.metricValues[1].value),
        revenue: parseFloat(row.metricValues[2].value),
        cost: parseFloat(row.metricValues[3] ? row.metricValues[3].value : 0)
    })) : [];
}

function calculatePressure(data) {
    // Find Google Ads data
    const googleAds = data.find(s => s.source.toLowerCase().includes('google'));

    if (!googleAds || googleAds.cost === 0) {
        // No ad spend = passive mode
        return { pressure: 50, roas: 0, note: 'No Google Ads spend detected' };
    }

    const roas = googleAds.revenue / googleAds.cost;
    let pressure;

    // Pressure scale: higher = more opportunity
    if (roas > 5) pressure = 95;      // Critical opportunity - scale up!
    else if (roas > 4) pressure = 75; // High opportunity
    else if (roas > 3) pressure = 60; // Good performance
    else if (roas > 2) pressure = 50; // Neutral
    else if (roas > 1) pressure = 30; // Below target
    else pressure = 10;                // Negative ROAS - pause ads

    return { pressure, roas, googleAds };
}

function updateGPM(pressure, metrics, data) {
    // Ensure data directory exists
    const dataDir = path.dirname(GPM_PATH);
    if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
    }

    let gpm = {
        store: 'Alpha Medical',
        version: '1.0.0',
        created: new Date().toISOString(),
        sectors: { operations: {}, marketing: {}, retention: {}, acquisition: {} }
    };

    if (fs.existsSync(GPM_PATH)) {
        gpm = JSON.parse(fs.readFileSync(GPM_PATH, 'utf8'));
    }

    gpm.store = 'Alpha Medical';
    gpm.sectors = gpm.sectors || {};
    gpm.sectors.marketing = gpm.sectors.marketing || {};
    gpm.sectors.marketing.ga4 = {
        pressure: pressure,
        trend: pressure > (gpm.sectors.marketing.ga4?.pressure || 0) ? 'UP' : 'DOWN',
        last_check: new Date().toISOString(),
        sensor_data: {
            roas: metrics.roas.toFixed(2),
            revenue_7d: data.reduce((acc, s) => acc + s.revenue, 0).toFixed(2),
            cost_7d: data.reduce((acc, s) => acc + s.cost, 0).toFixed(2),
            sessions_7d: data.reduce((acc, s) => acc + s.sessions, 0),
            conversions_7d: data.reduce((acc, s) => acc + s.conversions, 0)
        }
    };

    // Update global metrics
    gpm.metrics = gpm.metrics || {};
    gpm.metrics.global_roas = metrics.roas.toFixed(2);
    gpm.metrics.total_revenue_7d = data.reduce((acc, s) => acc + s.revenue, 0).toFixed(2);

    // Recalculate overall pressure
    const allPressures = [];
    for (const sector of Object.values(gpm.sectors || {})) {
        for (const value of Object.values(sector)) {
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

    console.log(`📡 GPM Updated: GA4 Marketing Pressure is ${pressure}`);
    console.log(`   ROAS: ${metrics.roas.toFixed(2)}, Revenue 7d: €${data.reduce((acc, s) => acc + s.revenue, 0).toFixed(2)}`);
    console.log(`   Sessions: ${data.reduce((acc, s) => acc + s.sessions, 0)}, Conversions: ${data.reduce((acc, s) => acc + s.conversions, 0)}`);
}

async function main() {
    // Health check mode
    if (process.argv.includes('--health')) {
        console.log('✅ GA4 Sensor: OK');
        console.log(`   Property ID: ${process.env.GA4_PROPERTY_ID || 'Not configured'}`);
        console.log(`   Credentials: ${process.env.GOOGLE_APPLICATION_CREDENTIALS ? 'Set' : 'Missing'}`);
        console.log(`   SDK: ${BetaAnalyticsDataClient ? 'Installed' : 'Not installed'}`);
        process.exit(0);
    }

    // Get property ID from environment
    const propertyId = process.env.GA4_PROPERTY_ID;

    if (!propertyId) {
        console.log('⚠️ GA4_PROPERTY_ID not set. Reporting PASSIVE state.');
        updateGPM(50, { roas: 0 }, []);
        return;
    }

    try {
        console.log(`📊 Fetching GA4 data for property ${propertyId}...`);
        const data = await fetchGA4Data(propertyId);
        const metrics = calculatePressure(data);
        updateGPM(metrics.pressure, metrics, data);
    } catch (e) {
        console.error(`❌ GA4 Sensor Failure: ${e.message}`);
        updateGPM(50, { roas: 0 }, []);
    }
}

main();
