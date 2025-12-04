# CONFIGURATION N8N - ALPHA MEDICAL
## Google Gemini Product Photo Enhancement
## Date: 2025-12-01

---

## ✅ ÉTAT ACTUEL

### Workflow existant dans n8n ✅
- **Nom:** "Enhance Product Photos with Google Gemini AI for E-commerce Catalog"
- **Status:** Importé mais à configurer
- **JSON sauvegardé:** `n8n-google-gemini-image-workflow.json`

### Credentials déjà configurés ✅
- **Google Drive OAuth2:** htidcOV6hR8kh9tB ("Google Drive account")
- **Google Sheets OAuth2:** HTAGRgrsWTF0cfU2 ("Google Sheets account")
- **Google Gemini API:** 7tlny7NnnrQIfupF ("Google Gemini(PaLM) Api account")

### MCP Configuration ✅
- **MCP Access Token:** Configuré dans Claude Code
- **N8N Instance:** https://n8n.srv1168256.hstgr.cloud
- **Status:** Ready to activate

---

## 🎯 CONFIGURATION REQUISE (3 VALEURS À AJOUTER)

Le workflow est 90% prêt. Il manque seulement **3 IDs** à configurer:

### 1. Input Folder ID (Google Drive)
**À configurer dans:** `File Created` + `File Updated` nodes

### 2. Output Folder ID (Google Drive)
**À configurer dans:** `Workflow Configuration` node

### 3. Google Sheet ID
**À configurer dans:** `Workflow Configuration` node

---

## 📋 PROCÉDURE COMPLÈTE (15 minutes)

### ÉTAPE 1: Créer Google Drive Folders (3 min)

**Actions:**

1. **Ouvrir Google Drive:** https://drive.google.com

2. **Créer dossier Input:**
   ```
   Nom: Alpha Medical - Product Photos Input
   ```
   - Créer le dossier
   - Ouvrir le dossier
   - Copier l'URL: `https://drive.google.com/drive/folders/XXXXX`
   - **Noter le Folder ID:** `_________________`

3. **Créer dossier Output:**
   ```
   Nom: Alpha Medical - Product Photos Output
   ```
   - Créer le dossier
   - Ouvrir le dossier
   - Copier l'URL: `https://drive.google.com/drive/folders/XXXXX`
   - **Noter le Folder ID:** `_________________`

---

### ÉTAPE 2: Créer Google Sheet (3 min)

**Actions:**

1. **Ouvrir Google Sheets:** https://sheets.google.com

2. **Créer nouveau spreadsheet:**
   ```
   Nom: Alpha Medical - Product Image Processing
   ```

3. **Renommer Sheet1 en "Photos"** (nom exact requis)

4. **Ajouter les headers (ligne 1):**
   ```
   A1: File name
   B1: Status
   C1: Start Time
   D1: End Time
   E1: Input File
   F1: Output File
   G1: Notes
   ```

5. **Copier Sheet ID:**
   - URL format: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
   - **Noter le Sheet ID:** `_________________`

---

### ÉTAPE 3: Configurer le Workflow dans n8n (7 min)

**Actions:**

1. **Login n8n:** https://n8n.srv1168256.hstgr.cloud

2. **Ouvrir le workflow:**
   - Aller dans "Workflows"
   - Chercher: "Enhance Product Photos with Google Gemini AI for E-commerce Catalog"
   - Cliquer pour ouvrir

3. **Configurer "File Created" node:**
   - Cliquer sur le node "File Created"
   - Dans "Folder to Watch":
     - Mode: "By ID"
     - Value: **[Coller Input Folder ID]**
   - Vérifier Poll Time = 5 minutes ✅
   - Credential déjà configuré ✅

4. **Configurer "File Updated" node:**
   - Cliquer sur le node "File Updated"
   - Dans "Folder to Watch":
     - Mode: "By ID"
     - Value: **[Coller Input Folder ID]**
   - Vérifier Poll Time = 5 minutes ✅
   - Credential déjà configuré ✅

5. **Configurer "Workflow Configuration" node:**
   - Cliquer sur le node "Workflow Configuration"
   - Dans "Assignments":
     - `google_sheet_id`: **[Coller Sheet ID]**
     - `dest_folder_id`: **[Coller Output Folder ID]**
     - `text_prompt`: Déjà configuré ✅
   - Sauvegarder

6. **Vérifier les credentials (6 nodes):**
   - ✅ "Download Image" → Credential "Google Drive account"
   - ✅ "Save image" → Credential "Google Drive account"
   - ✅ "Create Entry" → Credential "Google Sheets account"
   - ✅ "Update Entry to Done" → Credential "Google Sheets account"
   - ✅ "Update Entry to Error" → Credential "Google Sheets account"
   - ✅ "Edit Image" → Credential "Google Gemini(PaLM) Api account"

---

### ÉTAPE 4: Activer MCP Access (2 min)

**Actions:**

1. **Dans le workflow n8n ouvert:**
   - Cliquer sur ⚙️ "Workflow Settings" (en haut à droite)

2. **Scroller vers "MCP Access":**
   - Toggle "Enable workflow access in MCP" → **ON** ✅

3. **Activer le workflow:**
   - Toggle "Active" en haut → **ON** ✅

4. **Sauvegarder:**
   - Cliquer "Save"

---

### ÉTAPE 5: Vérifier depuis Claude Code (1 min)

**Actions:**

1. **Tester la connexion MCP:**
   - Dans Claude Code, demander: "Can you list the available n8n workflows?"
   - Je devrais voir: "Enhance Product Photos with Google Gemini AI for E-commerce Catalog"

---

### ÉTAPE 6: Test avec 1 Image (10 min)

**Préparation:**

1. **Sélectionner 1 image produit Alpha Medical:**
   - Massage chair, therapeutic device, ou bundle
   - Format: JPG ou PNG
   - Taille: < 20MB
   - Qualité: Peu importe (le workflow l'améliorera)

2. **Upload dans Input folder:**
   - Ouvrir "Alpha Medical - Product Photos Input"
   - Drag & drop l'image
   - Attendre 5 minutes (trigger poll time)

**Vérification:**

3. **Après 5 minutes, vérifier n8n:**
   - Aller dans "Executions" tab
   - Vérifier dernière execution
   - Status devrait être "Success" (vert) ✅

4. **Vérifier Google Sheets:**
   - Ouvrir le sheet "Photos"
   - Nouvelle ligne devrait apparaître:
     - File name: [nom de votre image]
     - Status: "Completed"
     - Start Time: [timestamp]
     - End Time: [timestamp]
     - Input File: [lien Google Drive]
     - Output File: [lien Google Drive]

5. **Vérifier Output folder:**
   - Ouvrir "Alpha Medical - Product Photos Output"
   - Image enhanced devrait être présente
   - Format nom: `{nom_original}_clean.{extension}`

6. **Vérifier qualité:**
   - Télécharger l'image enhanced
   - Comparer avec l'original
   - Vérifier:
     - ✅ Background removed/replaced
     - ✅ Professional lighting
     - ✅ Product details préservés
     - ✅ Texte lisible

---

## ✅ CRITÈRES DE SUCCÈS

### Test réussi = 100% si:
- [ ] Workflow visible dans Claude Code via MCP
- [ ] 1 image uploadée dans Input folder
- [ ] Workflow exécuté après 5 min
- [ ] Execution Status = Success dans n8n
- [ ] Nouvelle ligne dans Google Sheets avec Status "Completed"
- [ ] Image enhanced dans Output folder
- [ ] Qualité image = Professional (background clean, lighting pro)

---

## 🚀 APRÈS TEST RÉUSSI

### Batch Processing des 100 Produits Alpha Medical:

**Option 1: Processing par lots progressifs (recommandé)**
1. Upload 5 images → Vérifier qualité
2. Upload 10 images → Vérifier consistance
3. Upload 20 images → Ajuster prompt si besoin
4. Upload les 65 restantes → Processing automatique

**Option 2: Processing en masse (rapide)**
1. Upload les 100 images d'un coup
2. Attendre ~50-100 minutes
3. Vérifier résultats dans Google Sheets

**Métriques attendues:**
- **Processing time:** ~30-60 secondes/image
- **Total time:** ~50-100 minutes pour 100 images
- **Cost:** ~$1-5 total (Google Gemini API)
- **Success rate:** >95% (based on workflow design)

---

## 🎨 CUSTOMISATION DU PROMPT (OPTIONNEL)

### Prompt actuel (Generic E-commerce):
```
Transform this product photo into a high-quality, studio-style image.
- Background: Remove the original background completely and replace it with a clean, light gray gradient (e.g., #f0f0f0 to #e0e0e0).
- Lighting: Apply soft, diffused, and balanced lighting to eliminate harsh shadows and highlight the product's details. The lighting should feel natural and professional.
- Color & Realism: Perform subtle color correction to enhance vibrancy and ensure colors are true-to-life. Do not oversaturate.
- Integrity: Keep the product's shape, texture, and all original details perfectly intact. Do not add, remove, or alter any part of the product itself. If the product contains any text, especially ensure that the text is readable and identical in the new image.
- Final Look: The result should be a crisp, modern, and professional image suitable for a high-end e-commerce catalog.
```

### Variantes pour Alpha Medical:

**Option 1: Medical White (Clinical look)**
```
Replace background with pure white (#FFFFFF) medical-grade studio background. Apply soft diffused lighting. Preserve all product details exactly. Enhance clarity and sharpness suitable for medical equipment catalog.
```

**Option 2: Clinical Blue (Healthcare look)**
```
Replace background with clean light blue gradient (#E3F2FD to #BBDEFB) suitable for medical products. Soft professional lighting. Preserve product integrity completely. Enhance colors naturally for medical equipment presentation.
```

**Option 3: Luxury Dark (Premium look pour massage chairs)**
```
Replace background with dark gray gradient (#303030 to #202020) for premium medical equipment presentation. Dramatic professional lighting highlighting product features. Perfect product preservation.
```

**Pour changer le prompt:**
1. Ouvrir le workflow dans n8n
2. Cliquer sur "Workflow Configuration" node
3. Modifier la valeur de `text_prompt`
4. Sauvegarder
5. Tester avec 1-2 images
6. Comparer les résultats
7. Choisir le meilleur style

---

## 🐛 TROUBLESHOOTING

### Problème 1: Workflow ne se déclenche pas

**Symptômes:** Image uploadée mais rien ne se passe après 5 min

**Solutions:**
1. Vérifier que le workflow est "Active" (toggle ON)
2. Vérifier Input Folder ID correct dans les triggers
3. Vérifier Google Drive credential valide
4. Tester manuellement: Cliquer "Test Workflow" dans n8n

---

### Problème 2: Erreur dans "Edit Image" node

**Symptômes:** Execution fails au node "Edit Image"

**Solutions:**
1. Vérifier Google Gemini API credential
2. Vérifier quota API pas dépassé (Google AI Studio)
3. Vérifier format image supporté (JPG, PNG)
4. Vérifier taille image < 20MB

---

### Problème 3: Google Sheets pas mis à jour

**Symptômes:** Execution success mais pas de ligne dans Sheets

**Solutions:**
1. Vérifier Sheet ID correct dans Workflow Configuration
2. Vérifier sheet nommé exactement "Photos"
3. Vérifier headers exacts (ligne 1)
4. Vérifier Google Sheets credential = Editor access

---

### Problème 4: Qualité image décevante

**Symptômes:** Image processée mais qualité pas bonne

**Solutions:**
1. Ajuster le text_prompt (voir section Customisation)
2. Tester avec différentes variantes de prompt
3. Vérifier qualité image input (min 1500x1500px recommandé)
4. Essayer Option Medical White ou Clinical Blue

---

## 📊 CHECKLIST RAPIDE

### Avant de commencer:
- [ ] Google Drive folders créés (Input + Output)
- [ ] Folder IDs copiés
- [ ] Google Sheet créé avec onglet "Photos"
- [ ] Headers ajoutés (ligne 1)
- [ ] Sheet ID copié

### Configuration workflow:
- [ ] Workflow ouvert dans n8n
- [ ] "File Created" → Input Folder ID configuré
- [ ] "File Updated" → Input Folder ID configuré
- [ ] "Workflow Configuration" → Sheet ID configuré
- [ ] "Workflow Configuration" → Output Folder ID configuré
- [ ] Tous les credentials vérifiés (6 nodes)
- [ ] MCP Access activé
- [ ] Workflow Active = ON
- [ ] Workflow sauvegardé

### Test:
- [ ] 1 image sélectionnée
- [ ] Image uploadée dans Input folder
- [ ] Attendre 5 minutes
- [ ] Execution Success dans n8n
- [ ] Ligne créée dans Google Sheets
- [ ] Image enhanced dans Output folder
- [ ] Qualité vérifiée et acceptable

---

## 💡 BEST PRACTICES ALPHA MEDICAL

### Recommandations pour images input:

**Optimal:**
- Résolution: 1500x1500px minimum (2000x2000px idéal)
- Format: JPG ou PNG
- Lighting: Peu importe (workflow corrigera)
- Background: Peu importe (workflow remplacera)
- Focus: Produit net et clair

**À éviter:**
- Images très floues
- Résolution < 500x500px
- Fichiers > 20MB
- Formats exotiques (TIFF, RAW)

### Organisation par type de produit:

**Option: Créer sub-folders dans Input:**
```
Alpha Medical - Product Photos Input/
├── Massage Chairs/
├── Therapeutic Devices/
├── Bundles/
└── Accessories/
```

**Puis processing par catégorie:**
1. Upload Massage Chairs → Test → Ajuster prompt
2. Upload Therapeutic Devices → Vérifier
3. Upload Bundles → Vérifier
4. Upload Accessories → Finaliser

---

## 🎯 RÉSUMÉ ULTRA-RAPIDE

**Ce que tu dois faire MAINTENANT (15 min):**

1. **Google Drive** (3 min):
   - Créer "Alpha Medical - Product Photos Input"
   - Créer "Alpha Medical - Product Photos Output"
   - Noter les 2 Folder IDs

2. **Google Sheets** (3 min):
   - Créer "Alpha Medical - Product Image Processing"
   - Onglet "Photos" avec 7 headers
   - Noter Sheet ID

3. **n8n Configuration** (7 min):
   - Ouvrir workflow dans n8n
   - Configurer 2 triggers avec Input Folder ID
   - Configurer Workflow Configuration avec Sheet ID + Output Folder ID
   - Activer MCP Access
   - Activer Workflow
   - Sauvegarder

4. **Test** (10 min):
   - Upload 1 image dans Input folder
   - Attendre 5 min
   - Vérifier Success

**Après test réussi:**
- Upload les 100 produits Alpha Medical
- Processing automatique en ~50-100 minutes
- Cost: ~$1-5 total

---

**Status:** Configuration 90% ready
**Temps requis:** 15 minutes setup + 10 minutes test = 25 minutes total
**Prêt pour:** 100 produits Alpha Medical

**Fichiers créés:**
- `n8n-google-gemini-image-workflow.json` - Workflow JSON backup
- `N8N_ALPHA_MEDICAL_CONFIG_GUIDE.md` - Ce guide
- `N8N_WORKFLOW_IMAGE_PROCESSING.md` - Documentation complète
- `N8N_MCP_CONFIGURATION_GUIDE.md` - MCP integration guide

**Date:** 2025-12-01
**Created by:** Claude Code - Session 68
