#!/usr/bin/env node
/**
 * Skill Trigger Bridge
 * Triggers GitHub Actions from Local Skills via gh CLI
 */

const { execSync } = require('child_process');

function triggerWorkflow(skillName, context = {}) {
    try {
        const payload = JSON.stringify({ skill: skillName, context });
        console.log(`🚀 Triggering remote workflow for skill: ${skillName}...`);

        // Use gh cli to trigger workflow_dispatch
        // Requires 'gh' to be installed and authenticated
        execSync(`gh workflow run skill-connector.yml -f skill="${skillName}" -f context='${JSON.stringify(context)}'`, { stdio: 'inherit' });

        console.log('✅ Remote trigger successful.');
    } catch (e) {
        console.error('❌ Failed to trigger workflow:', e.message);
        console.error('   Ensure "gh" CLI is installed and authenticated.');
    }
}

// CLI usage
if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length < 1) {
        console.log('Usage: node skill_trigger.js <skill_name> [json_context]');
        process.exit(1);
    }
    const skill = args[0];
    const context = args[1] ? JSON.parse(args[1]) : {};
    triggerWorkflow(skill, context);
}
