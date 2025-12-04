# ACTIVER LE WORKFLOW GOOGLE GEMINI - GUIDE RAPIDE
## "Enhance Product Photos with Google Gemini AI for E-commerce Catalog"
## Date: 2025-12-01

---

## 🎯 OBJECTIF

Activer l'accès MCP pour que Claude Code puisse voir et exécuter le workflow de traitement d'images.

---

## 📋 ÉTAPE 1: ACTIVER L'ACCÈS MCP (2 minutes)

### Actions dans n8n:

1. **Login:** https://n8n.srv1168256.hstgr.cloud

2. **Ouvrir le workflow:**
   - Aller dans l'onglet "Workflows"
   - Chercher: **"Enhance Product Photos with Google Gemini AI for E-commerce Catalog"**
   - Cliquer pour ouvrir

3. **Activer MCP Access:**
   - Cliquer sur l'icône ⚙️ **"Workflow Settings"** (en haut à droite)
   - Scroller vers le bas jusqu'à la section **"MCP Access"**
   - Toggle **"Enable workflow access in MCP"** → **ON** ✅
   - Cliquer **"Save"**

4. **Activer le workflow:**
   - Toggle **"Active"** en haut → **ON** ✅
   - Sauvegarder

---

## 📋 ÉTAPE 2: VÉRIFIER LA CONFIGURATION (5 minutes)

### Nœuds à vérifier dans le workflow:

**1. Workflow Configuration Node:**
Vérifier/mettre à jour ces valeurs:

```javascript
{
  "google_sheet_id": "VOTRE_GOOGLE_SHEET_ID",
  "dest_folder_id": "VOTRE_OUTPUT_FOLDER_ID",
  "text_prompt": "Transform this product photo into a high-quality, studio-style image..."
}
```

**Comment obtenir ces IDs:**

**A. Google Sheet ID:**
1. Ouvrir Google Sheets: https://sheets.google.com
2. Créer/ouvrir le sheet "Alpha Medical - Product Image Processing"
3. Créer un onglet nommé **"Photos"** (exact)
4. Ajouter les headers en ligne 1:
   ```
   File name | Status | Start Time | End Time | Input File | Output File | Notes
   ```
5. Copier l'URL: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
6. **Sheet ID = la partie entre /d/ et /edit**

**B. Output Folder ID:**
1. Ouvrir Google Drive: https://drive.google.com
2. Créer un dossier: **"Alpha Medical - Product Photos Output"**
3. Ouvrir le dossier
4. Copier l'URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
5. **Folder ID = la partie après /folders/**

**C. Input Folder ID (pour les triggers):**
1. Créer un dossier: **"Alpha Medical - Product Photos Input"**
2. Copier le Folder ID comme ci-dessus

**2. File Created Trigger:**
- Folder to Watch: [Sélectionner ou coller Input Folder ID]
- Poll Time: Every 5 minutes ✅

**3. File Updated Trigger:**
- Folder to Watch: [Sélectionner ou coller Input Folder ID]
- Poll Time: Every 5 minutes ✅

**4. Credentials:**
Vérifier que tous les nœuds ont les credentials configurés:
- Download Image → Google Drive OAuth2 API ✅
- Save image → Google Drive OAuth2 API ✅
- Create Entry → Google Sheets OAuth2 API ✅
- Update Entry to Done → Google Sheets OAuth2 API ✅
- Update Entry to Error → Google Sheets OAuth2 API ✅
- Edit Image → Google Gemini (PaLM) API ✅

---

## 📋 ÉTAPE 3: VÉRIFIER L'ACCÈS MCP (2 minutes)

### Depuis Claude Code:

Une fois le workflow sauvegardé avec MCP Access activé, je pourrai:

```bash
# Vérifier que je vois le workflow
Can you list the available n8n workflows?
```

**Résultat attendu:**
Je devrais voir le workflow "Enhance Product Photos with Google Gemini AI..."

---

## 🧪 ÉTAPE 4: TEST SIMPLE (10 minutes)

### Préparation:

1. **Sélectionner 1 image de test:**
   - Une photo produit Alpha Medical (massage chair, device, etc.)
   - Format: JPG ou PNG
   - Taille: < 20MB

2. **Upload l'image:**
   - Aller dans Google Drive
   - Ouvrir le dossier "Alpha Medical - Product Photos Input"
   - Upload l'image test

3. **Attendre 5 minutes:**
   - Le trigger poll time est de 5 minutes
   - Le workflow se déclenche automatiquement

4. **Vérifier les résultats:**
   - **n8n Executions:** Voir le log d'exécution (Status = Success ✅)
   - **Google Sheets:** Nouvelle ligne avec Status = "Completed"
   - **Output Folder:** Image enhanced avec nom `{original}_clean.{ext}`

---

## ✅ CRITÈRES DE SUCCÈS

### Test réussi si:
- [ ] Workflow visible via MCP dans Claude Code
- [ ] 1 image uploadée dans Input folder
- [ ] Workflow s'exécute automatiquement après 5 min
- [ ] Execution Status = Success dans n8n
- [ ] Nouvelle ligne dans Google Sheets
- [ ] Image enhanced dans Output folder
- [ ] Qualité de l'image acceptable (background removed, professional lighting)

---

## 🚀 APRÈS LE TEST RÉUSSI

### Batch Processing:

1. **Upload 5 images** → Vérifier traitement
2. **Upload 10 images** → Vérifier consistance
3. **Upload les 100 produits Alpha Medical** → Processing automatique

**Estimated Time:** ~50-100 minutes (automatic)
**Estimated Cost:** ~$1-5 (Google Gemini API)

---

## 📝 CHECKLIST RAPIDE

**Avant de tester:**
- [ ] Workflow "Enhance Product Photos..." ouvert dans n8n
- [ ] MCP Access activé dans Workflow Settings
- [ ] Workflow Active = ON
- [ ] Google Sheet créé avec onglet "Photos" et headers
- [ ] Google Drive folders créés (Input + Output)
- [ ] Google Sheet ID copié et collé dans Workflow Configuration node
- [ ] Output Folder ID copié et collé dans Workflow Configuration node
- [ ] Input Folder ID configuré dans les 2 triggers
- [ ] Tous les credentials configurés (Google Drive, Sheets, Gemini)
- [ ] Workflow sauvegardé

**Pour le test:**
- [ ] 1 image produit sélectionnée
- [ ] Image uploadée dans Input folder
- [ ] Attendre 5 minutes
- [ ] Vérifier n8n Executions
- [ ] Vérifier Google Sheets
- [ ] Vérifier Output folder

---

## 💡 NOTES IMPORTANTES

### Configuration Workflow:

**Text Prompt (déjà configuré dans le workflow):**
```
Transform this product photo into a high-quality, studio-style image.
- Background: Remove the original background completely and replace it with a clean, light gray gradient (e.g., #f0f0f0 to #e0e0e0).
- Lighting: Apply soft, diffused, and balanced lighting to eliminate harsh shadows and highlight the product's details. The lighting should feel natural and professional.
- Color & Realism: Perform subtle color correction to enhance vibrancy and ensure colors are true-to-life. Do not oversaturate.
- Integrity: Keep the product's shape, texture, and all original details perfectly intact. Do not add, remove, or alter any part of the product itself. If the product contains any text, especially ensure that the text is readable and identical in the new image.
- Final Look: The result should be a crisp, modern, and professional image suitable for a high-end e-commerce catalog.
```

**Pour produits médicaux Alpha Medical, variantes possibles:**

**Option Medical White:**
```
Replace background with pure white (#FFFFFF) medical-grade studio background. Apply soft diffused lighting. Preserve all product details exactly. Enhance clarity and sharpness suitable for medical equipment catalog.
```

**Option Clinical Blue:**
```
Replace background with clean light blue gradient (#E3F2FD to #BBDEFB) suitable for medical products. Soft professional lighting. Preserve product integrity completely. Enhance colors naturally for medical equipment presentation.
```

---

## 🔗 DOCUMENTATION COMPLÈTE

- **Architecture complète:** `N8N_WORKFLOW_IMAGE_PROCESSING.md`
- **Plan de test détaillé:** `N8N_IMAGE_WORKFLOW_TEST_PLAN.md`
- **Configuration MCP:** `N8N_MCP_CONFIGURATION_GUIDE.md`

---

**Status:** Workflow existe ✅ | MCP Access à activer ⏳ | Ready to test
**Temps estimé:** 10 minutes setup + 10 minutes test = 20 minutes total
**Prêt pour:** 100 produits Alpha Medical

**Date:** 2025-12-01
**Created by:** Claude Code - Session 68
