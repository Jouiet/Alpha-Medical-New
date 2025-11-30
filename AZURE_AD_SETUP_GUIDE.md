# AZURE AD APP REGISTRATION - GUIDE ÉTAPE PAR ÉTAPE
**Projet:** Alpha Medical - Power BI REST API Setup
**Durée estimée:** 10-15 minutes
**Prérequis:** Compte Microsoft/Azure actif (User ID: 100320055EAB028C)

---

## ⚠️ AVANT DE COMMENCER

**Vérifications critiques:**

```bash
# 1. Vérifier compte Microsoft actif
# Aller sur: https://account.microsoft.com
# Vous devez pouvoir vous connecter avec votre email Microsoft

# 2. Vérifier accès Azure Portal
# Aller sur: https://portal.azure.com
# Si vous voyez "Azure services", vous avez accès ✅
# Si erreur "No subscriptions found", c'est NORMAL pour Free tier ✅

# 3. Vérifier Power BI Service access
# Aller sur: https://app.powerbi.com
# Vous devez voir "My Workspace" ✅
```

**IMPORTANT:** Si vous ne pouvez pas accéder à https://portal.azure.com, vous devez d'abord créer un compte Azure (gratuit, pas de carte bancaire requise pour Free tier).

---

## 📋 ÉTAPE 1: OUVRIR AZURE PORTAL

**Action:**
```bash
# Ouvrir dans navigateur (Chrome/Safari recommandé)
open https://portal.azure.com
```

**Ce que vous voyez:**
- Page d'accueil Azure Portal
- Barre de recherche en haut: "Search resources, services, and docs (G+/)"
- Menu hamburger (☰) en haut à gauche
- Icône utilisateur en haut à droite (votre compte)

**Validation:**
✅ Vous êtes connecté avec votre compte Microsoft
✅ Vous voyez "Microsoft Azure" en haut à gauche
✅ Pas de message d'erreur "Access Denied"

---

## 📋 ÉTAPE 2: NAVIGUER VERS AZURE ACTIVE DIRECTORY

**Méthode 1 - Via recherche (RECOMMANDÉ):**

1. **Cliquer barre de recherche** en haut (ou taper `G+/`)
2. **Taper:** `Azure Active Directory`
3. **Cliquer** sur résultat "Azure Active Directory" (icône bleue avec clé)

**Méthode 2 - Via menu:**

1. Cliquer menu hamburger (☰) en haut à gauche
2. Scroller jusqu'à "Azure Active Directory" (section "Azure services")
3. Cliquer "Azure Active Directory"

**Ce que vous voyez maintenant:**
```
Page: Azure Active Directory > Overview
────────────────────────────────────────────────
Sections visibles:
├── Tenant information (nom de votre tenant)
├── Tenant ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  ← COPIER CETTE VALEUR
├── Primary domain: [votre-domaine].onmicrosoft.com
└── Menu gauche: Manage (Users, Groups, App registrations, etc.)
```

**ACTION CRITIQUE #1 - COPIER TENANT ID:**
```bash
# 1. Localiser "Tenant ID" (sous "Tenant information")
# Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# Exemple: 12345678-90ab-cdef-1234-567890abcdef

# 2. Cliquer icône "Copy" à côté du Tenant ID
# OU sélectionner texte et Cmd+C (Mac) / Ctrl+C (Windows)

# 3. Coller dans .env.powerbi
nano .env.powerbi
# Remplacer: AZURE_TENANT_ID=""
# Par:       AZURE_TENANT_ID="12345678-90ab-cdef-1234-567890abcdef"
# Sauver: Ctrl+X → Y → Enter
```

**Validation Étape 2:**
✅ Vous êtes sur page "Azure Active Directory > Overview"
✅ Tenant ID copié et collé dans .env.powerbi
✅ Tenant ID format correct: 8-4-4-4-12 caractères avec tirets

---

## 📋 ÉTAPE 3: CRÉER APP REGISTRATION

**Navigation:**

1. **Dans menu gauche**, section "Manage"
2. **Cliquer:** "App registrations"
3. **Cliquer bouton:** "+ New registration" (en haut)

**Ce que vous voyez:**
```
Page: Register an application
────────────────────────────────────────────────
Formulaire avec 3 sections:
├── Name *
├── Supported account types *
└── Redirect URI (optional)
```

**Remplir le formulaire:**

### 3.1 - NAME (Nom de l'application)

**Valeur exacte à entrer:**
```
Alpha Medical Power BI API
```

**Notes:**
- Nom visible seulement pour vous (pas public)
- Peut être changé plus tard si besoin
- Utilisez exactement ce nom pour cohérence avec documentation

### 3.2 - SUPPORTED ACCOUNT TYPES (Types de comptes supportés)

**Sélectionner:** (CRITIQUE - Ne pas se tromper)

```
○ Accounts in any organizational directory (Any Azure AD directory - Multitenant)
● Accounts in this organizational directory only ([Votre-Nom] only - Single tenant)  ← CETTE OPTION
○ Accounts in any organizational directory and personal Microsoft accounts
○ Personal Microsoft accounts only
```

**Pourquoi "Single tenant":**
- Plus sécurisé (accès limité à votre compte uniquement)
- Suffit pour Power BI personnel
- Free tier ne supporte que single tenant de toute façon

**ATTENTION:** Si vous sélectionnez "Multitenant" par erreur, l'app fonctionnera quand même MAIS moins sécurisé.

### 3.3 - REDIRECT URI (OPTIONNEL)

**Action:** LAISSER VIDE (ne rien sélectionner)

**Pourquoi:**
- Pas nécessaire pour Service Principal authentication
- Sera utilisé seulement si OAuth user login (pas notre cas)
- Peut être ajouté plus tard si besoin

**Formulaire final devrait ressembler à:**
```
Name: Alpha Medical Power BI API
Supported account types: ● Single tenant
Redirect URI: [Vide]
```

### 3.4 - CRÉER L'APPLICATION

**Action:**
1. **Vérifier** formulaire (nom, single tenant, URI vide)
2. **Cliquer bouton bleu:** "Register" (en bas)
3. **Attendre** 3-5 secondes (création app)

**Ce que vous voyez après création:**
```
Page: Alpha Medical Power BI API > Overview
────────────────────────────────────────────────
Informations critiques visibles:
├── Display name: Alpha Medical Power BI API
├── Application (client) ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  ← COPIER
├── Directory (tenant) ID: [Même valeur qu'Étape 2]
├── Object ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
└── Supported account types: My organization only
```

**ACTION CRITIQUE #2 - COPIER CLIENT ID:**
```bash
# 1. Localiser "Application (client) ID"
# Format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# Exemple: abcdef12-3456-7890-abcd-ef1234567890

# 2. Cliquer icône "Copy" à côté
# OU sélectionner et Cmd+C

# 3. Coller dans .env.powerbi
nano .env.powerbi
# Remplacer: AZURE_CLIENT_ID=""
# Par:       AZURE_CLIENT_ID="abcdef12-3456-7890-abcd-ef1234567890"
# Sauver: Ctrl+X → Y → Enter
```

**Validation Étape 3:**
✅ App "Alpha Medical Power BI API" créée
✅ Vous êtes sur page "Overview" de l'app
✅ Application (client) ID copié et collé dans .env.powerbi
✅ Client ID format correct: 8-4-4-4-12 caractères

---

## 📋 ÉTAPE 4: CRÉER CLIENT SECRET (Mot de passe API)

**Navigation:**

1. **Dans menu gauche** de la page app (Alpha Medical Power BI API)
2. Section "Manage"
3. **Cliquer:** "Certificates & secrets"

**Ce que vous voyez:**
```
Page: Certificates & secrets
────────────────────────────────────────────────
2 onglets:
├── Certificates (vide)
└── Client secrets (vide) ← SÉLECTIONNER CET ONGLET
```

**Action:**

1. **Cliquer onglet:** "Client secrets" (si pas déjà sélectionné)
2. **Cliquer bouton:** "+ New client secret"

**Formulaire popup apparaît:**
```
Add a client secret
────────────────────────────────────────────────
Description: [Champ texte vide]
Expires:     [Menu déroulant]
             ○ 3 months
             ○ 6 months
             ● 24 months (recommended)  ← SÉLECTIONNER
             ○ Custom...
────────────────────────────────────────────────
[Cancel]  [Add]
```

### 4.1 - DESCRIPTION

**Valeur à entrer:**
```
Alpha Medical API Key - Production
```

**Notes:**
- Description pour vous (rappel de l'usage)
- Peut mettre ce que vous voulez
- Utile si vous créez plusieurs secrets plus tard

### 4.2 - EXPIRES (Expiration)

**Sélectionner:** `24 months (recommended)`

**Pourquoi 24 mois:**
- Équilibre sécurité/praticité
- Évite renouvellement trop fréquent
- Vous recevrez email reminder avant expiration
- Peut être renouvelé plus tard facilement

**ATTENTION:** Si vous sélectionnez "Custom" et mettez date > 24 mois, Azure peut refuser (limite Free tier).

### 4.3 - CRÉER LE SECRET

**Action:**
1. **Vérifier** Description + Expires (24 months)
2. **Cliquer bouton:** "Add"
3. **ATTENDRE** affichage du secret (3-5 secondes)

**CE QUI APPARAÎT (CRITIQUE - LIRE ATTENTIVEMENT):**

```
Client secrets
────────────────────────────────────────────────
Description              Value                    Expires
Alpha Medical API...     [••••••••••••••••]       [Date dans 24 mois]
                         ↑ MASQUÉ

[Icône Copy]  ← CLIQUER ICI IMMÉDIATEMENT
```

**APRÈS AVOIR CLIQUÉ "Copy":**

Le secret est maintenant visible temporairement:
```
Value: AbCdEf123456~GhIjKl789012-MnOpQr345678  ← C'EST VOTRE SECRET
```

**⚠️ AVERTISSEMENT CRITIQUE:**

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚠️  CETTE VALEUR NE SERA PLUS JAMAIS AFFICHÉE !                │
│                                                                  │
│  Si vous quittez cette page sans copier le secret:              │
│  ❌ Impossible de le récupérer                                   │
│  ❌ Vous devrez créer un NOUVEAU secret                          │
│  ❌ L'ancien secret restera actif (risque sécurité)             │
│                                                                  │
│  ACTION REQUISE: Copier MAINTENANT dans .env.powerbi            │
└─────────────────────────────────────────────────────────────────┘
```

**ACTION CRITIQUE #3 - COPIER CLIENT SECRET (IMMÉDIATEMENT):**

```bash
# 1. Le secret est déjà dans votre clipboard (vous avez cliqué Copy)
# Si pas copié: Sélectionner tout le texte du secret et Cmd+C

# 2. IMMÉDIATEMENT ouvrir .env.powerbi
nano .env.powerbi

# 3. Remplacer:
AZURE_CLIENT_SECRET=""

# 4. Par (coller votre secret):
AZURE_CLIENT_SECRET="AbCdEf123456~GhIjKl789012-MnOpQr345678"

# 5. VÉRIFIER que vous avez bien collé (secret visible dans nano)

# 6. Sauver: Ctrl+X → Y → Enter

# 7. VÉRIFIER que le secret est sauvé
cat .env.powerbi | grep AZURE_CLIENT_SECRET
# Output devrait montrer: AZURE_CLIENT_SECRET="[votre-secret]"
```

**Format secret (validation visuelle):**
```
Caractéristiques du secret:
├── Longueur: 40-50 caractères environ
├── Caractères: Lettres (a-z, A-Z), chiffres (0-9), tirets (-), tildes (~)
├── Exemple format: AbC123~DeF-456GhI
└── PAS d'espaces, PAS de guillemets DANS le secret
```

**Si vous avez manqué de copier le secret:**

```bash
# Option 1: Créer un nouveau secret (RECOMMANDÉ)
# 1. Retourner sur page "Certificates & secrets"
# 2. Cliquer "+ New client secret"
# 3. Description: "Alpha Medical API Key - Production v2"
# 4. Expires: 24 months
# 5. Add → COPIER IMMÉDIATEMENT cette fois

# Option 2: Supprimer l'ancien et créer nouveau (PLUS SÛR)
# 1. Sur page "Certificates & secrets"
# 2. Cliquer icône poubelle à côté du secret non copié
# 3. Confirmer suppression
# 4. Créer nouveau secret (Option 1)
```

**Validation Étape 4:**
✅ Client secret créé (visible dans liste "Client secrets")
✅ Secret copié dans .env.powerbi (AZURE_CLIENT_SECRET rempli)
✅ Secret sauvegardé (cat .env.powerbi montre la valeur)
✅ Secret format correct (40-50 chars, lettres/chiffres/tirets/tildes)

---

## 📋 ÉTAPE 5: CONFIGURER API PERMISSIONS

**Navigation:**

1. **Dans menu gauche** de la page app (Alpha Medical Power BI API)
2. Section "Manage"
3. **Cliquer:** "API permissions"

**Ce que vous voyez:**
```
Page: API permissions
────────────────────────────────────────────────
Configured permissions:
├── Microsoft Graph (1)
│   └── User.Read (Delegated) - Granted for [Tenant]
└── [Vide - Pas de Power BI permissions encore]

Boutons en haut:
[+ Add a permission]  [Grant admin consent]  [...]
```

**Action - Ajouter Power BI permissions:**

### 5.1 - CLIQUER "+ Add a permission"

**Popup apparaît:**
```
Request API permissions
────────────────────────────────────────────────
Onglets:
├── Microsoft APIs (SÉLECTIONNÉ)
├── APIs my organization uses
└── My APIs

Liste APIs Microsoft:
├── Microsoft Graph
├── Azure Service Management
├── Power BI Service  ← CHERCHER CELLE-CI
├── ...
```

**Si vous ne voyez PAS "Power BI Service" immédiatement:**

```bash
# 1. Scroller dans la liste (20-30 APIs affichées)
# OU
# 2. Utiliser barre de recherche en haut du popup:
#    Taper: "Power BI"
# 3. Cliquer sur "Power BI Service" (icône orange/rouge)
```

### 5.2 - SÉLECTIONNER "Power BI Service"

**Page suivante:**
```
Request API permissions > Power BI Service
────────────────────────────────────────────────
What type of permissions does your application require?

○ Delegated permissions (SÉLECTIONNER CELUI-CI)
  Access the Power BI Service as the signed-in user

○ Application permissions
  Access the Power BI Service as the application itself
```

**Sélectionner:** `Delegated permissions`

**Pourquoi Delegated:**
- Service Principal utilisera credentials user (votre compte)
- Plus sécurisé pour usage personnel
- Application permissions = pour apps qui tournent sans user (pas notre cas)

### 5.3 - SÉLECTIONNER PERMISSIONS SPÉCIFIQUES

**Liste permissions s'affiche:**
```
Select permissions (Delegated)
────────────────────────────────────────────────
Search: [Barre recherche]

☐ Dataset.Read.All
   Read all datasets
   
☐ Dataset.ReadWrite.All  ← COCHER CELLE-CI
   Read and write all datasets
   
☐ Report.Read.All
   Read all reports
   
☐ Dashboard.Read.All
   Read all dashboards
   
... [Plus de permissions]
```

**Permissions à cocher (MINIMUM REQUIS):**

```
✅ Dataset.Read.All
   - Permet lire structure datasets
   - Permet exécuter DAX queries (read-only)
   
✅ Dataset.ReadWrite.All  ← CRITIQUE
   - Permet créer/modifier datasets
   - Permet refresh datasets
   - Inclut automatiquement Dataset.Read.All
```

**Permissions OPTIONNELLES (recommandées pour plus tard):**

```
☐ Report.Read.All
   - Si vous voulez lire rapports via API
   - Pas nécessaire pour learning initial
   
☐ Dashboard.Read.All
   - Si vous voulez lire dashboards via API
   - Pas nécessaire pour learning initial
```

**RECOMMANDATION:** Cocher UNIQUEMENT `Dataset.ReadWrite.All` pour commencer (principe least privilege).

### 5.4 - AJOUTER LES PERMISSIONS

**Action:**
1. **Vérifier:** ✅ Dataset.ReadWrite.All coché
2. **Cliquer bouton bleu:** "Add permissions" (en bas du popup)
3. **Attendre** fermeture popup (2-3 secondes)

**Ce que vous voyez maintenant:**
```
Page: API permissions
────────────────────────────────────────────────
Configured permissions:
├── Microsoft Graph (1)
│   └── User.Read (Delegated) - ✅ Granted
└── Power BI Service (1)  ← NOUVEAU
    └── Dataset.ReadWrite.All (Delegated) - ⚠️ Not granted
                                              ↑ NORMAL - Voir étape suivante
```

**⚠️ "Not granted" est NORMAL à ce stade** - Vous devez faire "Grant admin consent" (Étape 5.5)

### 5.5 - GRANT ADMIN CONSENT (Accorder consentement)

**Ce que c'est:**
- Autorise l'app à utiliser les permissions demandées
- Requis pour Service Principal authentication
- Vous êtes l'admin de votre tenant (Free tier), donc vous pouvez le faire

**Action:**

1. **Cliquer bouton:** "Grant admin consent for [Votre Tenant]" (en haut)

**Popup de confirmation apparaît:**
```
┌─────────────────────────────────────────────────────────────────┐
│  Grant admin consent                                             │
│                                                                  │
│  Granting admin consent will allow this app to act on behalf    │
│  of all users in your organization. Permissions being granted:  │
│                                                                  │
│  • Read and write all datasets (Power BI Service)               │
│                                                                  │
│  This cannot be undone from this screen.                        │
│                                                                  │
│  [Cancel]  [Yes]  ← CLIQUER "Yes"                               │
└─────────────────────────────────────────────────────────────────┘
```

2. **Cliquer:** "Yes"
3. **Attendre** notification (3-5 secondes)

**Confirmation success:**
```
✅ Successfully granted admin consent for the requested permissions
```

**Page se rafraîchit:**
```
Configured permissions:
├── Microsoft Graph (1)
│   └── User.Read (Delegated) - ✅ Granted for [Tenant]
└── Power BI Service (1)
    └── Dataset.ReadWrite.All (Delegated) - ✅ Granted for [Tenant]
                                              ↑ MAINTENANT "Granted" ✅
```

**Validation Étape 5:**
✅ Power BI Service permissions ajoutées
✅ Dataset.ReadWrite.All cochée
✅ Admin consent accordé (status "Granted" visible)
✅ Pas de message d'erreur

---

## 📋 ÉTAPE 6: ACTIVER POWER BI REST API (Admin Portal)

**Navigation:**

```bash
# 1. Ouvrir Power BI Service dans nouvel onglet
open https://app.powerbi.com

# 2. Vous connecter si nécessaire (même compte Microsoft)
```

**Dans Power BI Service:**

1. **Cliquer icône ⚙️ (Settings)** en haut à droite
2. **Dans menu déroulant, cliquer:** "Admin portal"

**⚠️ SI VOUS NE VOYEZ PAS "Admin portal":**

```
Raisons possibles:
├── Vous n'êtes pas admin de votre tenant
│   → Solution: Utiliser compte qui a créé tenant Azure AD
│   
├── Power BI Free tier limitations
│   → Solution: Certaines settings requièrent Pro ($10/mois)
│   → MAIS: "Dataset Execute Queries REST API" devrait être disponible Free
│
└── Compte récent (< 24h)
    → Solution: Attendre 24-48h que permissions propagent
    → Workaround: Tester quand même les scripts (peut fonctionner même sans admin access)
```

**Si "Admin portal" accessible:**

**Page Admin portal s'ouvre:**
```
Power BI Admin Portal
────────────────────────────────────────────────
Menu gauche:
├── Usage metrics
├── Users
├── Audit logs
├── Tenant settings  ← CLIQUER ICI
├── ...
```

### 6.1 - NAVIGUER VERS TENANT SETTINGS

1. **Cliquer:** "Tenant settings" (menu gauche)
2. **Attendre** chargement settings (5-10 secondes - beaucoup de settings)

**Page Tenant settings:**
```
Tenant settings
────────────────────────────────────────────────
Sections (scrollables):
├── Help and support settings
├── Workspace settings
├── Information protection
├── Export and sharing settings
├── Content pack and app settings
├── Integration settings
├── Power Platform
├── Developer settings  ← CHERCHER CETTE SECTION
├── ...
```

### 6.2 - SCROLLER VERS "Developer settings"

```bash
# Option 1: Scroller manuellement (beaucoup de sections, 2-3 min)
# Option 2: Utiliser Cmd+F / Ctrl+F
#   Rechercher: "Developer settings"
#   Appuyer Enter pour sauter à la section
```

**Section "Developer settings":**
```
Developer settings
────────────────────────────────────────────────
☐ Embed content in apps
   Allow users to embed Power BI content...
   
☐ Service principals can use Power BI APIs
   Allow service principals to use Power BI APIs...
   
☐ Dataset Execute Queries REST API  ← CHERCHER CELUI-CI
   Allows applications to execute queries...
```

### 6.3 - ACTIVER "Dataset Execute Queries REST API"

**Action:**

1. **Cliquer sur "Dataset Execute Queries REST API"** pour expand
2. **Section s'ouvre:**

```
Dataset Execute Queries REST API
────────────────────────────────────────────────
○ Disabled (désactivé)
● Enabled   ← SÉLECTIONNER CELUI-CI

Apply to:
● The entire organization  ← LAISSER CELUI-CI
○ Specific security groups (Not recommended)
   [+ Add security groups]

[Apply]  [Cancel]
```

**Sélections:**
- Status: ✅ `Enabled`
- Apply to: ✅ `The entire organization`

3. **Cliquer bouton:** "Apply" (en bas de la section)

**Confirmation popup:**
```
┌─────────────────────────────────────────────────────────────────┐
│  Apply tenant setting                                            │
│                                                                  │
│  This change might take up to 15 minutes to take effect.        │
│                                                                  │
│  [Cancel]  [Apply]  ← CLIQUER "Apply"                           │
└─────────────────────────────────────────────────────────────────┘
```

4. **Cliquer:** "Apply"
5. **Attendre notification:** "Successfully updated tenant settings"

**⚠️ IMPORTANT - DÉLAI D'ACTIVATION:**

```
La setting prend 15 minutes pour se propager dans Azure AD.

Timeline:
├── T+0 min:  Setting activée dans Power BI portal ✅
├── T+5 min:  Propagation dans Azure backend (en cours)
├── T+15 min: Activée partout ✅ (API calls fonctionneront)
└── T+30 min: Garanti activé (si 15 min pas assez)

Recommandation: Attendre 15-20 min avant de tester powerbi_connection_test.py
```

**Validation Étape 6:**
✅ Accès Admin portal confirmé
✅ "Developer settings" section trouvée
✅ "Dataset Execute Queries REST API" = Enabled
✅ Apply to = "Entire organization"
✅ Setting appliquée (notification success)

---

## 📋 ÉTAPE 7: VALIDATION FINALE CREDENTIALS

**Vérifier que .env.powerbi est complet:**

```bash
# 1. Afficher contenu .env.powerbi (sans commentaires)
grep -v '^#' .env.powerbi | grep -v '^$'

# Output attendu (vos valeurs exactes):
AZURE_TENANT_ID="12345678-90ab-cdef-1234-567890abcdef"
AZURE_CLIENT_ID="abcdef12-3456-7890-abcd-ef1234567890"
AZURE_CLIENT_SECRET="AbCdEf123456~GhIjKl789012-MnOpQr345678"
POWERBI_USERNAME=""  # Optionnel (pas utilisé pour Service Principal)
POWERBI_PASSWORD=""  # Optionnel (pas utilisé pour Service Principal)
```

**Checklist credentials:**

```yaml
✅ AZURE_TENANT_ID:
   - Format: 8-4-4-4-12 caractères (36 chars total avec tirets)
   - Guillemets présents: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   - Source: Azure AD > Overview > Tenant ID

✅ AZURE_CLIENT_ID:
   - Format: 8-4-4-4-12 caractères (36 chars total avec tirets)
   - Guillemets présents: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   - Source: App Registration > Overview > Application (client) ID

✅ AZURE_CLIENT_SECRET:
   - Format: 40-50 caractères environ (lettres, chiffres, tirets, tildes)
   - Guillemets présents: "AbC123~DeF-456..."
   - PAS de guillemets À L'INTÉRIEUR du secret
   - Source: App Registration > Certificates & secrets > Value (copié immédiatement)
```

**Si une valeur manque ou incorrecte:**

```bash
# TENANT_ID manquant:
# Retourner Étape 2, copier Tenant ID

# CLIENT_ID manquant:
# Retourner Étape 3, page Overview app, copier Application (client) ID

# CLIENT_SECRET manquant:
# Retourner Étape 4:
# 1. Page "Certificates & secrets"
# 2. Créer NOUVEAU secret (l'ancien ne peut plus être récupéré)
# 3. Copier IMMÉDIATEMENT la valeur
```

**Test format (optionnel mais recommandé):**

```bash
# Vérifier que les credentials sont bien formattés
python3 << 'PYEOF'
import os
import re

# Charger .env.powerbi
with open('.env.powerbi') as f:
    for line in f:
        line = line.strip()
        if line.startswith('AZURE_TENANT_ID='):
            tenant = line.split('=', 1)[1].strip('"')
            if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', tenant, re.I):
                print("✅ AZURE_TENANT_ID format correct")
            else:
                print("❌ AZURE_TENANT_ID format incorrect")
        
        elif line.startswith('AZURE_CLIENT_ID='):
            client = line.split('=', 1)[1].strip('"')
            if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', client, re.I):
                print("✅ AZURE_CLIENT_ID format correct")
            else:
                print("❌ AZURE_CLIENT_ID format incorrect")
        
        elif line.startswith('AZURE_CLIENT_SECRET='):
            secret = line.split('=', 1)[1].strip('"')
            if len(secret) >= 30 and not '"' in secret:
                print(f"✅ AZURE_CLIENT_SECRET format correct ({len(secret)} chars)")
            else:
                print(f"❌ AZURE_CLIENT_SECRET format incorrect ou trop court ({len(secret)} chars)")
PYEOF
```

**Output attendu:**
```
✅ AZURE_TENANT_ID format correct
✅ AZURE_CLIENT_ID format correct
✅ AZURE_CLIENT_SECRET format correct (44 chars)
```

---

## 📋 ÉTAPE 8: TEST CONNEXION POWER BI

**Attendre délai activation (CRITIQUE):**

```bash
# ⏰ ATTENDRE 15-20 MINUTES après Étape 6 (activation REST API)

# Pendant l'attente, vous pouvez:
# - Vérifier credentials (Étape 7)
# - Lire POWER_BI_LEARNING_PATH.md
# - Préparer un café ☕

# Vérifier temps écoulé:
date  # Noter l'heure
# Attendre jusqu'à 15 min après activation REST API
```

**Lancer test connexion:**

```bash
# 1. S'assurer d'être dans répertoire projet
cd /Users/mac/Desktop/Alpha-Medical

# 2. Vérifier que credentials sont exportés
export $(grep -v '^#' .env.powerbi | grep -v '^$' | xargs)

# 3. Vérifier que variables sont chargées
echo "Tenant: $AZURE_TENANT_ID"
echo "Client: $AZURE_CLIENT_ID"
echo "Secret: ${AZURE_CLIENT_SECRET:0:10}..."  # Affiche premiers 10 chars seulement

# 4. Lancer script test
python3 powerbi_connection_test.py
```

**Output attendu (SUCCESS):**

```
======================================================================
POWER BI REST API - CONNECTION TEST (macOS Compatible)
======================================================================
User ID: 100320055EAB028C
Python Version: Python 3.13.2

🔐 Using Service Principal authentication...
✅ Authentication successful (Service Principal)
✅ Power BI client initialized

📊 Available Workspaces:
--------------------------------------------------
1. My Workspace (ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

📈 Available Datasets:
--------------------------------------------------
⚠️  No datasets found

💡 To execute DAX queries:
   First create a dataset in Power BI Service
   Then use: execute_dax_query(pbi, dataset_id, dax)

======================================================================
✅ CONNECTION TEST SUCCESSFUL
======================================================================

Next steps:
1. Create semantic models in Power BI Service
2. Connect Shopify, GA4, Klaviyo data sources
3. Execute DAX queries via this script
4. Integrate with Claude Code workflows
```

**Interprétation SUCCESS:**
- ✅ Authentication successful = Credentials corrects
- ✅ Power BI client initialized = API activé
- ✅ Workspaces listés = Accès Power BI Service confirmé
- ⚠️ No datasets = NORMAL (vous n'avez pas encore créé datasets)

---

## 🚨 TROUBLESHOOTING - ERREURS COMMUNES

### Erreur #1: "Missing Service Principal credentials"

**Output:**
```
❌ ERROR: Missing Service Principal credentials (TENANT_ID, CLIENT_ID, CLIENT_SECRET)
```

**Cause:** Variables .env.powerbi pas chargées

**Solution:**
```bash
# Exporter variables explicitement
export $(grep -v '^#' .env.powerbi | grep -v '^$' | xargs)

# Vérifier
echo $AZURE_TENANT_ID
echo $AZURE_CLIENT_ID

# Re-lancer test
python3 powerbi_connection_test.py
```

---

### Erreur #2: "Authentication failed: AADSTS7000215"

**Output:**
```
❌ ERROR: Authentication failed: AADSTS7000215: Invalid client secret provided
```

**Cause:** Client secret incorrect ou expiré

**Solution:**
```bash
# 1. Vérifier secret dans .env.powerbi
cat .env.powerbi | grep CLIENT_SECRET

# 2. Si vide ou suspect, créer nouveau secret:
# - Retourner Étape 4
# - Certificates & secrets → + New client secret
# - Copier IMMÉDIATEMENT
# - Mettre à jour .env.powerbi

# 3. Re-exporter variables
export $(grep -v '^#' .env.powerbi | grep -v '^$' | xargs)

# 4. Re-tester
python3 powerbi_connection_test.py
```

---

### Erreur #3: "AADSTS700016: Application not found"

**Output:**
```
❌ ERROR: AADSTS700016: Application with identifier 'xxx' was not found in the directory
```

**Cause:** CLIENT_ID incorrect

**Solution:**
```bash
# 1. Vérifier CLIENT_ID
cat .env.powerbi | grep CLIENT_ID

# 2. Retourner Azure Portal:
# https://portal.azure.com
# → Azure Active Directory
# → App registrations
# → Alpha Medical Power BI API
# → Overview
# → Copier "Application (client) ID"

# 3. Mettre à jour .env.powerbi avec valeur correcte

# 4. Re-tester
```

---

### Erreur #4: "Dataset Execute Queries REST API is not enabled"

**Output:**
```
❌ ERROR: 403 Forbidden - Dataset Execute Queries REST API is not enabled
```

**Cause:** REST API pas encore activé OU délai 15 min pas écoulé

**Solution:**
```bash
# 1. Vérifier activation (Étape 6):
# https://app.powerbi.com/admin-portal/tenantSettings
# → Developer settings
# → Dataset Execute Queries REST API = Enabled?

# 2. Si Enabled, attendre 15-20 min depuis activation

# 3. Si > 20 min et erreur persiste:
# - Désactiver setting (Disabled)
# - Sauver (Apply)
# - Attendre 2 min
# - Réactiver (Enabled)
# - Sauver (Apply)
# - Attendre 15 min
# - Re-tester
```

---

### Erreur #5: "No admin portal access"

**Symptôme:** "Admin portal" pas visible dans Power BI Service settings

**Cause:** Compte pas admin OU Free tier limitations

**Solution:**
```bash
# Test 1: Vérifier script fonctionne QUAND MÊME
python3 powerbi_connection_test.py

# Si authentication success:
# ✅ REST API fonctionne malgré pas d'accès admin portal
# → Continuer normalement

# Si authentication fail:
# Option 1: Attendre 24-48h (nouveau compte)
# Option 2: Upgrade Power BI Pro ($10/mois) pour accès admin complet
# Option 3: Créer nouveau tenant Azure AD (gratuit)
```

---

## ✅ VALIDATION FINALE - CHECKLIST COMPLÈTE

**Azure AD App Registration:**
```yaml
✅ App créée: "Alpha Medical Power BI API"
✅ App type: Single tenant (My organization only)
✅ Tenant ID copié dans .env.powerbi
✅ Client ID copié dans .env.powerbi
✅ Client secret créé et copié dans .env.powerbi
✅ Secret expires: 24 months (date notée)
✅ API permissions: Power BI Service > Dataset.ReadWrite.All
✅ Admin consent: Granted
```

**Power BI Service Configuration:**
```yaml
✅ Accès Power BI Service: https://app.powerbi.com
✅ My Workspace visible
✅ Admin portal accessible (ou test script fonctionne quand même)
✅ Developer settings > Dataset Execute Queries REST API = Enabled
✅ Délai 15 min activation respecté
```

**Credentials Validation:**
```yaml
✅ .env.powerbi existe
✅ AZURE_TENANT_ID rempli (format UUID correct)
✅ AZURE_CLIENT_ID rempli (format UUID correct)
✅ AZURE_CLIENT_SECRET rempli (40-50 chars, pas de guillemets internes)
✅ Variables exportées (export $(grep ...))
✅ Test format Python passed
```

**Connection Test:**
```yaml
✅ python3 powerbi_connection_test.py exécuté
✅ "Authentication successful" affiché
✅ "Power BI client initialized" affiché
✅ Workspaces listés (minimum "My Workspace")
✅ Pas d'erreurs AADSTS*
✅ Pas d'erreurs 403 Forbidden
```

---

## 🎯 PROCHAINES ÉTAPES (POST-SETUP)

**Immédiat (aujourd'hui):**

```bash
# 1. Utiliser quick start helper
./powerbi_quick_start.sh

# 2. Explorer Power BI Service
open https://app.powerbi.com
# - Cliquer "My Workspace"
# - Se familiariser avec interface
```

**Cette semaine (Semaines 1-2 - Phase 1 Learning Path):**

```bash
# 1. Lire learning guide
cat POWER_BI_LEARNING_PATH.md | less

# 2. Commencer Microsoft Learn tutorial
open https://learn.microsoft.com/training/paths/get-started-power-bi/

# 3. Créer premier dataset (données fictives)
# Suivre POWER_BI_LEARNING_PATH.md > Phase 1 > Semaine 2

# 4. Temps investi recommandé: 2-3h cette semaine
```

**Mois 1-3 (Phase 2-3):**
- Connecter Shopify, GA4, Google Sheets
- Apprendre DAX (mesures basiques)
- Créer premiers rapports

**Mois 3-6 (Phase 4-5):**
- Dashboards flywheel complets
- Automation Python (pbipy scripts)
- Décision upgrade Pro tier (si revenue > $10K/mois)

---

## 📝 NOTES DE SÉCURITÉ

**Credentials Protection:**

```bash
# 1. .env.powerbi est dans .gitignore ✅
# Vérifier:
git status  # .env.powerbi NE DOIT PAS apparaître

# 2. Ne JAMAIS commiter .env.powerbi
# Si committé par erreur:
git rm --cached .env.powerbi
git commit -m "Remove credentials"
git push --force  # ⚠️ Utiliser avec précaution

# 3. Rotation secret (tous les 24 mois):
# - Créer nouveau secret
# - Tester avec nouveau secret
# - Supprimer ancien secret
# - Mettre à jour .env.powerbi
```

**Client Secret Expiration:**

```bash
# Date expiration: [Noter la date de création + 24 mois]
# Exemple: Créé 2025-11-30 → Expire 2027-11-30

# Azure enverra email reminder 30 jours avant expiration

# Renouvellement:
# 1. Étape 4 (créer nouveau secret)
# 2. Tester nouveau secret
# 3. Supprimer ancien secret (après confirmation nouveau fonctionne)
```

---

**GUIDE COMPLET - DURÉE TOTALE:** 10-20 minutes (si tout va bien)  
**CRÉÉ:** 2025-11-30  
**VERSION:** 1.0  
**POUR:** Alpha Medical - Power BI Free Tier Learning

