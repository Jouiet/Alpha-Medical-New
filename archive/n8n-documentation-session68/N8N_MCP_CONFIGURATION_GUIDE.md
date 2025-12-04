# N8N MCP CONFIGURATION GUIDE
## Model Context Protocol Integration with n8n
## Date: 2025-12-01

---

## 🎯 WHAT IS MCP?

**MCP (Model Context Protocol)** is an open protocol developed by Anthropic that standardizes how Large Language Models (LLMs) interact with external tools and data sources.

**Key Concept:** MCP allows AI assistants (like Claude Code, Claude Desktop, Cursor, Windsurf) to:
- Execute n8n workflows as if they were native tools
- Access workflow automation directly from AI conversations
- Trigger complex multi-step processes through natural language

---

## 🔐 YOUR N8N MCP CREDENTIALS

### MCP Server Configuration

```yaml
Server URL: https://n8n.srv1168256.hstgr.cloud/mcp-server/http

MCP Access Token (for MCP Server):
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6IjE5MmUwMDg4LWYyOWItNDA2OS04NmZlLTkzNTg2ZDhlOTdmNSIsImlhdCI6MTc2NDYyNTczMn0.vXYG6FauIcQaJIOwDyCeYBUtCVUwxb1x2mWyJ8enrwE

N8N Public API Key (for REST API):
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NjI1NjI1fQ.YJeonYPrTdnjDewHvVv_BbPAbNnB9UEr2DbtGXIeALo
```

**⚠️ SECURITY NOTES:**
- Ces tokens sont des JWT (JSON Web Tokens) personnels liés à votre compte utilisateur
- Ne jamais les commiter dans Git
- Ne jamais les partager publiquement
- Si compromis, régénérer immédiatement dans n8n Settings > MCP Access

---

## 📋 TWO AUTHENTICATION METHODS

### Method 1: OAuth2 (Recommended for Desktop Apps)
**Usage:** Claude Desktop, Lovable, interactive applications

**Process:**
1. Configure MCP client with server URL
2. Client redirects to n8n for authorization
3. User approves access
4. OAuth token automatically managed

**Pros:**
- More secure (revocable per-client)
- Better for multiple users
- Automatic token refresh

**Cons:**
- Requires user interaction
- More complex setup

### Method 2: Access Token (Recommended for Automation)
**Usage:** Claude Code, scripts, CI/CD, programmatic access

**Process:**
1. Copy MCP Access Token from n8n Settings
2. Configure MCP client with token
3. Immediate access

**Pros:**
- Simple configuration
- Perfect for automation
- No user interaction needed

**Cons:**
- Token visible in config
- Must manually update if regenerated
- Single token for all clients

---

## 🔧 CONFIGURATION FOR CLAUDE CODE

### Step 1: Create MCP Configuration File

**Location:** `~/.config/claude-code/mcp.json` (macOS/Linux)

**Content:**
```json
{
  "mcpServers": {
    "n8n-alpha-medical": {
      "url": "https://n8n.srv1168256.hstgr.cloud/mcp-server/http",
      "transport": {
        "type": "sse",
        "headers": {
          "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6IjE5MmUwMDg4LWYyOWItNDA2OS04NmZlLTkzNTg2ZDhlOTdmNSIsImlhdCI6MTc2NDYyNTczMn0.vXYG6FauIcQaJIOwDyCeYBUtCVUwxb1x2mWyJ8enrwE"
        }
      }
    }
  }
}
```

### Step 2: Enable Workflow Access in n8n

**For each workflow you want to expose to Claude Code:**

1. Open workflow in n8n editor
2. Click "Workflow Settings" (gear icon)
3. Scroll to "MCP Access" section
4. Toggle "Enable workflow access in MCP" to ON
5. Save workflow

**Example workflows to enable:**
- Product sync workflows (Shopify → Sheets)
- Lead generation automations
- Email marketing triggers
- Data processing pipelines

### Step 3: Verify Connection

**Test in Claude Code:**
```
Can you list the available n8n workflows?
```

**Expected response:**
Claude Code should see all workflows you've enabled for MCP access.

---

## 🛠️ N8N MCP ARCHITECTURE

### How it Works

```
┌─────────────────┐
│  Claude Code    │
│  (MCP Client)   │
└────────┬────────┘
         │ MCP Protocol (HTTPS)
         │ Authorization: Bearer TOKEN
         ▼
┌─────────────────┐
│  n8n Instance   │
│  MCP Server     │
└────────┬────────┘
         │
         │ Executes
         ▼
┌─────────────────┐
│  n8n Workflows  │
│  (Enabled for   │
│   MCP Access)   │
└─────────────────┘
```

### Two Modes

**1. n8n as MCP Server (Your Configuration)**
- Claude Code calls n8n workflows as tools
- Each workflow becomes a callable function
- Use case: "Execute my Shopify product sync workflow"

**2. n8n as MCP Client (Advanced)**
- n8n workflows call external MCP servers
- Requires MCP Client Tool node in workflow
- Use case: n8n workflow calls external AI services

---

## 📊 USE CASES FOR ALPHA MEDICAL

### 1. Automated Product Management
**Scenario:** "Claude, sync all new Shopify products to Google Sheets"

**MCP Workflow:**
- Claude Code → n8n MCP Server
- Triggers: "Shopify Product Sync" workflow
- Workflow: Fetches products → Processes → Updates Sheets
- Response: "Synced 15 new products"

### 2. Marketing Automation
**Scenario:** "Claude, run the lead qualification workflow for new Facebook leads"

**MCP Workflow:**
- Claude Code → n8n MCP Server
- Triggers: "Facebook Lead Qualification" workflow
- Workflow: Fetch leads → Score → Segment → Klaviyo sync
- Response: "Processed 42 leads, 8 qualified"

### 3. Data Analysis
**Scenario:** "Claude, analyze last week's order data and generate report"

**MCP Workflow:**
- Claude Code → n8n MCP Server
- Triggers: "Weekly Analytics" workflow
- Workflow: Shopify API → Data processing → Report generation
- Response: Returns formatted analysis

### 4. Infrastructure Monitoring
**Scenario:** "Claude, check if all workflows are running"

**MCP Workflow:**
- Claude Code → n8n MCP Server
- Triggers: "Health Check" workflow
- Workflow: Check workflow status → Verify connections
- Response: "10/10 workflows operational"

---

## 🔒 SECURITY BEST PRACTICES

### 1. Token Management
```bash
# Store tokens in environment variables
export N8N_MCP_TOKEN="your-mcp-token"
export N8N_API_KEY="your-api-key"

# Reference in config
{
  "transport": {
    "headers": {
      "Authorization": "Bearer ${N8N_MCP_TOKEN}"
    }
  }
}
```

### 2. Workflow Permissions
- **Only enable MCP access for workflows you trust**
- **Avoid exposing sensitive operations** (delete, modify critical data)
- **Use workflow-level authentication** for additional security
- **Review enabled workflows monthly**

### 3. Token Rotation
```yaml
Schedule: Every 90 days
Process:
  1. Generate new MCP token in n8n Settings
  2. Update MCP config with new token
  3. Verify connection works
  4. Old token auto-revoked by n8n
```

### 4. Network Security
- Your n8n instance is publicly accessible (required for cloud MCP clients)
- Use HTTPS only (your instance: ✅ HTTPS)
- Enable n8n IP whitelisting if possible
- Monitor MCP access logs in n8n

---

## 🚀 GETTING STARTED

### Quick Setup (5 minutes)

**Step 1: Verify n8n MCP is Enabled**
```
1. Login to https://n8n.srv1168256.hstgr.cloud
2. Settings > MCP Access
3. Verify "Enable MCP" is ON
4. Copy MCP Server URL (already have it)
```

**Step 2: Configure Claude Code**
```bash
# Create config directory
mkdir -p ~/.config/claude-code

# Create MCP config
cat > ~/.config/claude-code/mcp.json << 'EOF'
{
  "mcpServers": {
    "n8n-alpha-medical": {
      "url": "https://n8n.srv1168256.hstgr.cloud/mcp-server/http",
      "transport": {
        "type": "sse",
        "headers": {
          "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ5MzQ1ZS1kYjk0LTQ1MDYtOTQzNC1lNjUyNWJkMjcxOTAiLCJpc3MiOiJuOG4iLCJhdWQiOiJtY3Atc2VydmVyLWFwaSIsImp0aSI6IjE5MmUwMDg4LWYyOWItNDA2OS04NmZlLTkzNTg2ZDhlOTdmNSIsImlhdCI6MTc2NDYyNTczMn0.vXYG6FauIcQaJIOwDyCeYBUtCVUwxb1x2mWyJ8enrwE"
        }
      }
    }
  }
}
EOF

# Verify file created
cat ~/.config/claude-code/mcp.json
```

**Step 3: Enable Workflows in n8n**
```
1. Open your first workflow (e.g., Shopify product sync)
2. Workflow Settings > MCP Access
3. Enable "Enable workflow access in MCP"
4. Save
5. Repeat for all workflows you want to expose
```

**Step 4: Test Connection**
```
# In Claude Code:
"Can you list the available n8n workflows?"

# Expected output:
Claude Code should list all workflows you enabled
```

---

## 📖 ADDITIONAL RESOURCES

### Official Documentation
- n8n MCP Docs: https://docs.n8n.io/advanced-ai/accessing-n8n-mcp-server/
- MCP Server Trigger Node: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-langchain.mcptrigger/
- Anthropic MCP Spec: https://modelcontextprotocol.io/

### Community Resources
- n8n MCP GitHub: https://github.com/czlonkowski/n8n-mcp
- n8n Community Forum: https://community.n8n.io/t/provide-and-use-model-context-protocol/63799
- Step-by-Step Guide: https://generect.com/blog/n8n-mcp/

### Tutorials
- Hostinger MCP Guide: https://www.hostinger.com/tutorials/how-to-use-n8n-with-mcp
- Medium Integration Guide: https://medium.com/@tam.tamanna18/integrating-n8n-workflow-automation-with-model-context-protocol-mcp-servers-0e7ef54729c1

---

## 🐛 TROUBLESHOOTING

### Issue 1: "Connection Refused"
**Problem:** Claude Code cannot connect to n8n MCP server

**Solutions:**
1. Verify n8n instance is accessible: `curl https://n8n.srv1168256.hstgr.cloud`
2. Check MCP is enabled in n8n Settings
3. Verify token is correct (copy fresh from n8n)
4. Check firewall/network restrictions

### Issue 2: "No Workflows Available"
**Problem:** Claude Code connects but sees no workflows

**Solutions:**
1. Enable MCP access in workflow settings
2. Save workflow after enabling
3. Restart n8n instance (if self-hosted)
4. Verify user has permission to access workflows

### Issue 3: "Authentication Failed"
**Problem:** Token rejected by n8n

**Solutions:**
1. Regenerate token in n8n Settings > MCP Access
2. Update mcp.json with new token
3. Verify token format (should be JWT)
4. Check token expiration (shouldn't expire, but verify)

### Issue 4: "Workflow Execution Failed"
**Problem:** Workflow called but fails to execute

**Solutions:**
1. Test workflow manually in n8n editor
2. Check workflow error logs
3. Verify workflow credentials are valid
4. Ensure workflow is activated (not paused)

---

## 📝 NOTES & BEST PRACTICES

### Token Security
- ⚠️ **CRITICAL:** Never commit tokens to Git repositories
- Store tokens in `.env` files (add to `.gitignore`)
- Use environment variables in production
- Rotate tokens every 90 days

### Workflow Design for MCP
- **Clear naming:** Use descriptive workflow names (Claude sees these)
- **Add descriptions:** Workflow description helps Claude understand purpose
- **Handle errors:** Include error handling in workflows
- **Return useful data:** Design workflows to return actionable results

### Performance
- **Async execution:** Long workflows should run asynchronously
- **Timeout handling:** Set appropriate workflow timeouts
- **Rate limiting:** Be aware of n8n execution limits
- **Caching:** Use caching for frequently accessed data

### Monitoring
- **Check logs:** Regularly review n8n execution logs
- **Track usage:** Monitor which workflows are called via MCP
- **Performance:** Track workflow execution times
- **Errors:** Set up alerts for failed executions

---

## ✅ NEXT STEPS

1. **Setup MCP config** in Claude Code (5 min)
2. **Enable 3-5 key workflows** for MCP access (10 min)
3. **Test connection** with simple workflow (5 min)
4. **Create automation workflows** specific to Alpha Medical needs (ongoing)
5. **Document workflows** for team usage (ongoing)

---

**Last Updated:** 2025-12-01
**Configuration Status:** Credentials Saved ✅
**Ready to Use:** YES

**Key Credentials Location:** This document (N8N_MCP_CONFIGURATION_GUIDE.md)
