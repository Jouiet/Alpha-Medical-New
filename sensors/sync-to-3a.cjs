#!/usr/bin/env node
/**
 * Alpha Medical - GPM Sync to 3A Central
 *
 * Role: Pushes local pressure-matrix.json to 3A centralized GPM
 * Architecture: Twin Sovereignty - Alpha Medical feeds data to 3A orchestrator
 *
 * Version: 1.0.0 | Session 143 | 23/01/2026
 */

const fs = require('fs');
const path = require('path');

const LOCAL_GPM_PATH = path.join(__dirname, '../data/pressure-matrix.json');
const CENTRAL_GPM_PATH = process.env.CENTRAL_GPM_PATH || '/Users/mac/Desktop/JO-AAA/landing-page-hostinger/data/pressure-matrix.json';
const STORE_ID = 'alpha-medical';

function loadLocalGPM() {
    if (!fs.existsSync(LOCAL_GPM_PATH)) {
        console.error('❌ Local GPM not found:', LOCAL_GPM_PATH);
        return null;
    }
    return JSON.parse(fs.readFileSync(LOCAL_GPM_PATH, 'utf8'));
}

function loadCentralGPM() {
    if (!fs.existsSync(CENTRAL_GPM_PATH)) {
        console.error('❌ Central GPM not found:', CENTRAL_GPM_PATH);
        return null;
    }
    return JSON.parse(fs.readFileSync(CENTRAL_GPM_PATH, 'utf8'));
}

function syncTocentral() {
    const localGPM = loadLocalGPM();
    const centralGPM = loadCentralGPM();

    if (!localGPM || !centralGPM) {
        console.error('❌ Cannot sync - GPM files missing');
        process.exit(1);
    }

    // Add/Update Alpha Medical data in central GPM
    centralGPM.subsidiaries = centralGPM.subsidiaries || {};
    centralGPM.subsidiaries[STORE_ID] = {
        name: localGPM.store || 'Alpha Medical',
        overall_pressure: localGPM.overall_pressure,
        sectors: localGPM.sectors,
        last_sync: new Date().toISOString(),
        source: 'sensors/sync-to-3a.cjs'
    };

    // Recalculate global pressure including subsidiaries
    const allPressures = [];

    // Main 3A sectors
    if (centralGPM.sectors) {
        for (const sector of Object.values(centralGPM.sectors)) {
            for (const metric of Object.values(sector)) {
                if (metric && typeof metric.pressure === 'number') {
                    allPressures.push(metric.pressure);
                }
            }
        }
    }

    // Subsidiaries
    if (centralGPM.subsidiaries) {
        for (const sub of Object.values(centralGPM.subsidiaries)) {
            if (sub && typeof sub.overall_pressure === 'number') {
                allPressures.push(sub.overall_pressure);
            }
        }
    }

    // Update timestamp
    centralGPM.last_updated = new Date().toISOString();

    // Save
    fs.writeFileSync(CENTRAL_GPM_PATH, JSON.stringify(centralGPM, null, 2));

    console.log(`✅ Synced ${STORE_ID} to central GPM`);
    console.log(`   Local pressure: ${localGPM.overall_pressure}`);
    console.log(`   Sectors synced: ${Object.keys(localGPM.sectors || {}).length}`);
    console.log(`   Central GPM updated: ${CENTRAL_GPM_PATH}`);
}

// CLI
if (process.argv.includes('--health')) {
    console.log('✅ Sync-to-3A: OK');
    console.log(`   Local GPM: ${fs.existsSync(LOCAL_GPM_PATH) ? 'Found' : 'Missing'}`);
    console.log(`   Central GPM: ${fs.existsSync(CENTRAL_GPM_PATH) ? 'Found' : 'Missing'}`);
    process.exit(0);
}

syncTocentral();
