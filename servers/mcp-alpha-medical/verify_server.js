
const { spawn } = require('child_process');
const path = require('path');

const serverPath = path.join(__dirname, 'build/index.js');
const server = spawn('node', [serverPath], {
    stdio: ['pipe', 'pipe', 'pipe']
});

console.log('🚀 Starting MCP Server for verification...');

// JSON-RPC 2.0 Request to list tools
const request = {
    jsonrpc: "2.0",
    id: 1,
    method: "tools/list",
    params: {}
};

server.stdout.on('data', (data) => {
    console.log(`📩 Received: ${data.toString()}`);
    try {
        const response = JSON.parse(data.toString());
        if (response.result && response.result.tools) {
            console.log('✅ Verification Successful! Tools found:');
            response.result.tools.forEach(tool => {
                console.log(`   - ${tool.name}: ${tool.description}`);
            });
            server.kill();
            process.exit(0);
        }
    } catch (e) {
        // Ignore partial chunks or stderr logs
    }
});

server.stderr.on('data', (data) => {
    console.error(`⚠️ Server Log: ${data.toString()}`);
});

// Send request
server.stdin.write(JSON.stringify(request) + '\n');

// Timeout
setTimeout(() => {
    console.error('❌ Verification Timeout');
    server.kill();
    process.exit(1);
}, 5000);
