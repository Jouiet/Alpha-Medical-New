# Alpha Medical - Environment Configuration

> Documentation of .env files structure (as of 2025-12-05)

## 📋 Overview

This project uses **5 separate .env files** organized by service for better security and maintainability.

**Total:** 40 environment variables across 5 files

## 🗂️ File Structure

### `.env` - Generic Configuration (5 keys)
**Purpose:** General-purpose keys for multiple services

- `ANTHROPIC_API_KEY` - Claude AI API key
- `KLAVIYO_PRIVATE_API_KEY` - Klaviyo email marketing (private)
- `KLAVIYO_PUBLIC_API_KEY` - Klaviyo email marketing (public)
- `GOOGLE_SHEET_ID` - Lead tracking spreadsheet
- `SHOPIFY_STORE_DOMAIN` - Store domain (⚠️ DUPLICATE - also in .env.admin)

**Used by:** General scripts, lead generation, AI tools

### `.env.admin` - Shopify Admin API (6 keys)
**Purpose:** Shopify store management and Admin API access

- `SHOPIFY_ADMIN_ACCESS_TOKEN` - Admin API access token
- `SHOPIFY_API_KEY` - App API key
- `SHOPIFY_API_SECRET` - App API secret
- `SHOPIFY_STOREFRONT_ACCESS_TOKEN` - Storefront API token
- `SHOPIFY_STORE_DOMAIN` - Store domain (⚠️ DUPLICATE)
- `KLAVIYO_API_KEY` - Klaviyo integration

**Used by:** All Shopify scripts (265+ scripts in repository)

### `.env.n8n` - N8N Workflow Automation (21 keys)
**Purpose:** N8N workflow automation platform

**N8N Platform (6 keys):**
- `N8N_API_KEY` - N8N API authentication
- `N8N_URL` - N8N instance URL
- `N8N_CREDENTIALS_URL` - Credentials management endpoint
- `N8N_GOOGLE_DRIVE_CREDENTIAL_ID` - Google Drive integration
- `N8N_GOOGLE_GEMINI_CREDENTIAL_ID` - Google Gemini AI integration
- `N8N_GOOGLE_SHEETS_CREDENTIAL_ID` - Google Sheets integration

**Workflow Configuration (5 keys):**
- `N8N_WORKFLOW_IMAGE_PROCESSING_ID` - Image processing workflow ID
- `N8N_WORKFLOW_IMAGE_PROCESSING_NAME` - Workflow name
- `N8N_WORKFLOW_IMAGE_PROCESSING_STATUS` - Workflow status
- `N8N_WORKFLOW_IMAGE_PROCESSING_ACTIVATED_DATE` - Activation date
- `N8N_WORKFLOW_IMAGE_URL` - Workflow URL

**Google Cloud Platform (10 keys):**
- `GOOGLE_CLOUD_PROJECT_URL` - GCP project URL
- `GOOGLE_OAUTH_CLIENT_ID` - OAuth client ID
- `GOOGLE_OAUTH_CLIENT_SECRET` - OAuth client secret
- `GOOGLE_GEMINI_API_KEY` - Gemini AI API key
- `GOOGLE_DRIVE_INPUT_FOLDER_ID` - Input folder ID
- `GOOGLE_DRIVE_INPUT_URL` - Input folder URL
- `GOOGLE_DRIVE_OUTPUT_FOLDER_ID` - Output folder ID
- `GOOGLE_DRIVE_OUTPUT_URL` - Output folder URL
- `GOOGLE_SHEETS_TRACKING_ID` - Tracking spreadsheet ID
- `GOOGLE_SHEETS_TRACKING_URL` - Tracking spreadsheet URL

**Used by:** N8N workflow automation (Workflow #3: Branded image generation)

### `.env.powerbi` - PowerBI Analytics (5 keys)
**Purpose:** PowerBI analytics and reporting (NOT YET IMPLEMENTED)

**Azure AD Authentication:**
- `AZURE_TENANT_ID` - Azure AD tenant
- `AZURE_CLIENT_ID` - Service principal client ID
- `AZURE_CLIENT_SECRET` - Service principal secret

**PowerBI Credentials:**
- `POWERBI_USERNAME` - PowerBI account username
- `POWERBI_PASSWORD` - PowerBI account password

**Status:** ⏳ Configured but not actively used (future analytics dashboard)

**Used by:** PowerBI integration scripts (when implemented)

### `.env.tidio` - Tidio Live Chat (3 keys)
**Purpose:** Customer support chat widget

- `TIDIO_PRIVATE_KEY` - Private API key
- `TIDIO_PUBLIC_KEY` - Public API key
- `TIDIO_CHAT_PAGE_URL` - Chat integration URL

**Status:** ✅ Configured and integrated in theme

**Used by:** Tidio chat widget (embedded in layout/theme.liquid)

## ⚠️ Known Issues

### 1. Duplicate Key
**Key:** `SHOPIFY_STORE_DOMAIN`

**Locations:**
- `.env` (line ~10)
- `.env.admin` (line ~5)

**Impact:** Low - Both contain same value
**Recommendation:** Remove from `.env`, keep only in `.env.admin`

## 🔒 Security

**Git Ignore Status:** ✅ All .env files in .gitignore

```gitignore
# Environment files
.env
.env.*
!.env.example
```

**Never commit:**
- Any file starting with `.env`
- Backup files (`.env.bak`, `.env.backup`)
- Pre-commit hook blocks `.env` files automatically

## 📝 Usage Guidelines

### Loading Environment Variables

**Python (recommended):**
```python
from dotenv import load_dotenv
import os

# Load specific .env file
load_dotenv('.env.admin')

# Access variables
store_domain = os.getenv('SHOPIFY_STORE_DOMAIN')
access_token = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
```

**Python (multiple files):**
```python
# Load multiple .env files (order matters - later overrides earlier)
load_dotenv('.env')  # Load general config first
load_dotenv('.env.admin')  # Override with admin-specific
```

**Bash:**
```bash
# Source single file
source .env.admin

# Source multiple files
set -a  # Automatically export variables
source .env
source .env.admin
set +a
```

### Adding New Variables

**Guidelines:**
1. Choose appropriate file based on service
2. Use UPPERCASE_WITH_UNDERSCORES naming
3. Add descriptive comment
4. Document in this README
5. Never commit the file

**Example:**
```bash
# In .env.admin
# Shopify GraphQL Admin API endpoint
SHOPIFY_GRAPHQL_URL=https://azffej-as.myshopify.com/admin/api/2025-10/graphql.json
```

## 🔄 Migration History

**Date:** 2025-12-05
**Action:** Documented existing structure
**Reason:** P0-DAY3 configuration audit
**Changes:** None (structure already optimal)

**Previous structure:** N/A (no previous documentation)

## 📊 Statistics

- **Total files:** 5
- **Total keys:** 40
- **Duplicates:** 1 (SHOPIFY_STORE_DOMAIN)
- **Categories:** Shopify (6), N8N (21), PowerBI (5), Tidio (3), Other (5)
- **Status:** ✅ Functional, well-organized, no migration needed

## 🎯 Best Practices

1. **One service per file** - Keep Shopify keys in .env.admin, N8N in .env.n8n, etc.
2. **Load only what you need** - Scripts should load specific .env files
3. **Check for duplicates** - Use `analyze_env_files.py` to detect
4. **Document changes** - Update this README when adding/removing keys
5. **Rotate secrets regularly** - Especially API keys and tokens
6. **Use .env.example** - For sharing structure without exposing secrets

## 📚 Related Files

- `analyze_env_files.py` - Script to analyze .env structure
- `.gitignore` - Ensures .env files never committed
- `.claude/hooks/pre-tool-use.sh` - Blocks .env commits

---

**Last updated:** 2025-12-05
**Status:** ✅ Configuration documented and verified
**Next review:** After launch (2026-01-05)
