
import subprocess
import json
import sys
import os

# Path to the Node.js script
NODE_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), '../../automations/lib/resilient-ai-fallback.cjs')

def call_ai_fallback(prompt: str, max_tokens: int = 1000) -> dict:
    """
    Call the Resilient AI Fallback (Node.js) script from Python.
    Returns a dict with 'text', 'provider', 'latency'.
    """
    if not os.path.exists(NODE_SCRIPT_PATH):
        return {"error": f"Fallback script not found at {NODE_SCRIPT_PATH}"}

    # Prepare command: node script.cjs --test "prompt" (but --test prints logs, we need programmatic access)
    # The Node script exposes a CLI but doesn't have a clean "json output" mode for CLI.
    # We will use a temporary bridge script to invoke the library function.
    
    bridge_code = f"""
    // Suppress logs from the library
    const originalLog = console.log;
    const originalWarn = console.warn;
    console.log = function() {{}};
    console.warn = function() {{}};

    const {{ callWithFallback }} = require('{NODE_SCRIPT_PATH}');
    
    async function run() {{
        try {{
            const result = await callWithFallback({json.dumps(prompt)}, {{ maxTokens: {max_tokens} }});
            // Restore log for output
            console.log = originalLog;
            console.log(JSON.stringify(result));
        }} catch (e) {{
            console.log = originalLog;
            console.error(e.message);
            process.exit(1);
        }}
    }}
    run();
    """
    
    try:
        process = subprocess.Popen(
            ['node', '-e', bridge_code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            return {"error": stderr.strip() or "Unknown error in Node script"}
            
        return json.loads(stdout.strip())
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Test CLI
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        prompt = "Hello, are you operational?"
        
    print(f"Testing Fallback with prompt: '{prompt}'")
    result = call_ai_fallback(prompt)
    print(json.dumps(result, indent=2))
