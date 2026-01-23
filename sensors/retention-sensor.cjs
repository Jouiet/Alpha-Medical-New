#!/usr/bin/env node
/**
 * Alpha Medical - Retention Sensor
 *
 * Role: Non-agentic data fetcher. Updates GPM pressure based on Churn Risk.
 * Metrics: Customer recency, frequency, churn risk
 *
 * Adapted from 3A Automation for Alpha Medical
 * Version: 1.0.0 | Session 143 | 23/01/2026
 */

const fs = require('fs');
const path = require('path');

// Load environment variables
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

const GPM_PATH = path.join(__dirname, '../data/pressure-matrix.json');

async function fetchShopifyOrders(shop, token) {
    if (!shop || !token) {
        throw new Error('Shopify Shop and Access Token required');
    }
    const url = `https://${shop}/admin/api/2024-01/orders.json?status=any&limit=250&fields=email,created_at,total_price,customer`;
    const response = await fetch(url, {
        headers: {
            'X-Shopify-Access-Token': token,
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) throw new Error(`Shopify API Error: ${response.status}`);
    const data = await response.json();
    return data.orders;
}

function calculateChurnPressure(orders) {
    if (!orders || orders.length === 0) return { pressure: 0, stats: { totalCustomers: 0, highRisk: 0 } };

    const customerMap = {};
    const now = new Date();

    orders.forEach(order => {
        if (!order.email) return;
        if (!customerMap[order.email]) {
            customerMap[order.email] = { orders: [] };
        }
        customerMap[order.email].orders.push(new Date(order.created_at));
    });

    const customers = Object.values(customerMap).map(c => {
        c.orders.sort((a, b) => b - a);
        const lastOrder = c.orders[0];
        const daysSinceLast = Math.floor((now - lastOrder) / (1000 * 60 * 60 * 24));
        return { recency: daysSinceLast, frequency: c.orders.length };
    });

    // High risk = recency > 90 days or only 1 order and recency > 60
    const highRiskCount = customers.filter(c => c.recency > 90 || (c.frequency === 1 && c.recency > 60)).length;
    const churnRate = customers.length > 0 ? highRiskCount / customers.length : 0;

    // Pressure mapping: 0% churn = 0 pressure, 20%+ churn = 95 pressure
    const pressure = Math.min(95, Math.floor(churnRate * 500));

    return {
        pressure,
        stats: {
            totalCustomers: customers.length,
            highRisk: highRiskCount,
            churnRate: (churnRate * 100).toFixed(1) + '%'
        }
    };
}

function updateGPM(pressure, stats) {
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
    gpm.sectors.retention = gpm.sectors.retention || {};
    gpm.sectors.retention.churn = {
        pressure: pressure,
        trend: pressure > (gpm.sectors.retention.churn?.pressure || 0) ? 'UP' : 'DOWN',
        last_check: new Date().toISOString(),
        sensor_data: stats
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

    console.log(`📡 GPM Updated: Retention Pressure is ${pressure}`);
    console.log(`   Customers: ${stats.totalCustomers}, High Risk: ${stats.highRisk}`);
    console.log(`   Churn Rate: ${stats.churnRate}`);
}

async function main() {
    if (process.argv.includes('--health')) {
        console.log('✅ Retention Sensor: OK');
        console.log(`   Store: ${process.env.SHOPIFY_STORE_DOMAIN || 'Not configured'}`);
        process.exit(0);
    }

    const shop = process.env.SHOPIFY_STORE_DOMAIN || process.env.SHOPIFY_STORE;
    const token = process.env.SHOPIFY_ADMIN_ACCESS_TOKEN || process.env.SHOPIFY_ACCESS_TOKEN;

    if (!shop || !token) {
        console.log('⚠️ Shopify credentials missing. Reporting CRITICAL GAP.');
        updateGPM(0, { totalCustomers: 0, highRisk: 0, churnRate: 'N/A' });
        return;
    }

    try {
        console.log('🔄 Analyzing customer retention...');
        const orders = await fetchShopifyOrders(shop, token);
        const { pressure, stats } = calculateChurnPressure(orders);
        updateGPM(pressure, stats);
    } catch (e) {
        console.error(`❌ Retention Sensor Failure: ${e.message}`);
        updateGPM(0, { totalCustomers: 0, highRisk: 0, churnRate: 'Error', error: e.message });
    }
}

main();
