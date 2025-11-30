#!/usr/bin/env python3
"""
Power BI REST API Connection Test - Alpha Medical
Alternative to Power BI MCP Server (macOS compatible)

Requirements:
1. Azure AD App Registration (Power BI Service)
2. Credentials: tenant_id, client_id, username, password

Usage:
    python3 powerbi_connection_test.py
"""

import os
from pbipy import PowerBI
import msal

# ============================================================================
# CONFIGURATION - À remplir avec vos credentials Azure AD
# ============================================================================

# Option 1: Service Principal (recommandé pour automation)
TENANT_ID = os.getenv("AZURE_TENANT_ID", "")  # Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "")  # App registration client ID
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")  # App secret

# Option 2: User credentials (pour tests interactifs)
USERNAME = os.getenv("POWERBI_USERNAME", "")  # Votre email Microsoft/Azure AD
PASSWORD = os.getenv("POWERBI_PASSWORD", "")  # Votre mot de passe

# Power BI API scope
SCOPES = ["https://analysis.windows.net/powerbi/api/.default"]

# User ID fourni (référence seulement)
USER_ID = "100320055EAB028C"

# ============================================================================
# AUTHENTICATION
# ============================================================================

def get_bearer_token_service_principal():
    """Authenticate via Service Principal (app-only)"""
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET]):
        raise ValueError("Missing Service Principal credentials (TENANT_ID, CLIENT_ID, CLIENT_SECRET)")
    
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    
    result = app.acquire_token_for_client(scopes=SCOPES)
    
    if "access_token" in result:
        print("✅ Authentication successful (Service Principal)")
        return result["access_token"]
    else:
        raise Exception(f"Authentication failed: {result.get('error_description')}")


def get_bearer_token_user_password():
    """Authenticate via username/password (delegated permissions)"""
    if not all([TENANT_ID, CLIENT_ID, USERNAME, PASSWORD]):
        raise ValueError("Missing user credentials (TENANT_ID, CLIENT_ID, USERNAME, PASSWORD)")
    
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = msal.PublicClientApplication(CLIENT_ID, authority=authority)
    
    result = app.acquire_token_by_username_password(
        USERNAME, 
        PASSWORD, 
        scopes=SCOPES
    )
    
    if "access_token" in result:
        print("✅ Authentication successful (User credentials)")
        return result["access_token"]
    else:
        raise Exception(f"Authentication failed: {result.get('error_description')}")


# ============================================================================
# POWER BI OPERATIONS
# ============================================================================

def list_workspaces(pbi):
    """List all accessible Power BI workspaces"""
    print("\n📊 Available Workspaces:")
    print("-" * 50)
    
    groups = pbi.groups()
    if not groups:
        print("⚠️  No workspaces found")
        return []
    
    for idx, group in enumerate(groups, 1):
        print(f"{idx}. {group.name} (ID: {group.id})")
    
    return groups


def list_datasets(pbi, workspace_id=None):
    """List datasets in a workspace or user's personal workspace"""
    print("\n📈 Available Datasets:")
    print("-" * 50)
    
    if workspace_id:
        datasets = pbi.datasets(group_id=workspace_id)
    else:
        datasets = pbi.datasets()
    
    if not datasets:
        print("⚠️  No datasets found")
        return []
    
    for idx, dataset in enumerate(datasets, 1):
        print(f"{idx}. {dataset.name} (ID: {dataset.id})")
    
    return datasets


def execute_dax_query(pbi, dataset_id, dax_query):
    """Execute a DAX query against a dataset"""
    print(f"\n🔍 Executing DAX Query:")
    print(f"Dataset ID: {dataset_id}")
    print(f"Query: {dax_query}")
    print("-" * 50)
    
    try:
        dataset = pbi.dataset(dataset_id)
        result = dataset.execute_queries(dax_query)
        
        print("✅ Query executed successfully")
        print(f"Result: {result}")
        return result
    
    except Exception as e:
        print(f"❌ Query failed: {str(e)}")
        return None


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("=" * 70)
    print("POWER BI REST API - CONNECTION TEST (macOS Compatible)")
    print("=" * 70)
    print(f"User ID: {USER_ID}")
    print(f"Python Version: {os.popen('python3 --version').read().strip()}")
    print(f"pbipy Version: 2.13.0")
    
    # Choose authentication method
    try:
        if CLIENT_SECRET:
            print("\n🔐 Using Service Principal authentication...")
            bearer_token = get_bearer_token_service_principal()
        elif USERNAME and PASSWORD:
            print("\n🔐 Using User credentials authentication...")
            bearer_token = get_bearer_token_user_password()
        else:
            raise ValueError(
                "\n❌ No credentials configured!\n"
                "Configure either:\n"
                "  1. Service Principal: AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET\n"
                "  2. User credentials: AZURE_TENANT_ID, AZURE_CLIENT_ID, POWERBI_USERNAME, POWERBI_PASSWORD\n"
                "\nSee setup instructions: https://learn.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal"
            )
        
        # Initialize Power BI client
        pbi = PowerBI(bearer_token)
        print("✅ Power BI client initialized")
        
        # List workspaces
        workspaces = list_workspaces(pbi)
        
        # List datasets (personal workspace)
        datasets = list_datasets(pbi)
        
        # Example DAX query (if datasets exist)
        if datasets:
            print("\n💡 To execute DAX queries:")
            print(f"   dataset_id = '{datasets[0].id}'")
            print(f"   dax = 'EVALUATE TOPN(10, <YourTable>)'")
            print(f"   execute_dax_query(pbi, dataset_id, dax)")
        
        print("\n" + "=" * 70)
        print("✅ CONNECTION TEST SUCCESSFUL")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Create semantic models in Power BI Service")
        print("2. Connect Shopify, GA4, Klaviyo data sources")
        print("3. Execute DAX queries via this script")
        print("4. Integrate with Claude Code workflows")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Verify Azure AD app registration exists")
        print("2. Check Power BI Service admin settings (Enable REST API)")
        print("3. Ensure credentials are correct")
        print("4. User must have Power BI Pro/Premium license (Free tier may be limited)")


if __name__ == "__main__":
    main()
