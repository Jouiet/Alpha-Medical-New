# CRÉER CREDENTIALS GOOGLE OAUTH2 POUR N8N
**Guide Complet - Version 2025**
**Temps:** 15-20 minutes

---

## 🎯 CE QUE TU VAS FAIRE

Tu dois créer des **OAuth2 credentials** dans Google Cloud Console pour que N8N puisse accéder à:
- Google Drive (pour uploader/télécharger files)
- Google Sheets (pour tracking)
- Google Gemini API (pour AI processing)

**Redirect URI N8N:** `https://n8n.srv1168256.hstgr.cloud/rest/oauth2-credential/callback`

---

## PARTIE 1: GOOGLE CLOUD CONSOLE (15 min)

### Étape 1: Créer Projet Google Cloud (3 min)

1. **Ouvre:** https://console.cloud.google.com/

2. **En haut à gauche**, clique sur le **dropdown du projet** (à côté de "Google Cloud")

3. **Dans la popup**, clique **"NEW PROJECT"** (en haut à droite)

4. **Remplis:**
   - **Project name:** `n8n-alpha-medical`
   - **Location:** Organization (laisse par défaut ou "No organization")

5. **Clique:** `CREATE`

6. **Attends** 10-20 secondes (création du projet)

7. **Sélectionne le projet** dans le dropdown (devrait être auto-sélectionné)

---

### Étape 2: Activer Google Drive API (2 min)

1. **Menu hamburger** (☰ en haut à gauche) → **"APIs & Services"** → **"Library"**

2. **Dans la barre de recherche**, tape: `Google Drive API`

3. **Clique** sur **"Google Drive API"** (premier résultat)

4. **Clique** le gros bouton bleu **"ENABLE"**

5. **Attends** 5 secondes (API activation)

---

### Étape 3: Activer Google Sheets API (2 min)

1. **Clique** "Library" dans la navigation de gauche (ou retour avec flèche)

2. **Cherche:** `Google Sheets API`

3. **Clique** sur le résultat

4. **Clique** `ENABLE`

---

### Étape 4: Créer OAuth Consent Screen (5 min)

1. **Menu gauche** → **"OAuth consent screen"**

2. **User Type:**
   - **Sélectionne:** `External`
   - **Clique:** `CREATE`

3. **Page 1/4 - App information:**
   - **App name:** `N8N Alpha Medical Automation`
   - **User support email:** (sélectionne ton email dans dropdown)
   - **App logo:** (optionnel - skip)
   - **Application home page:** (laisse vide)
   - **Application privacy policy:** (laisse vide)
   - **Application terms of service:** (laisse vide)
   - **Authorized domains:** (laisse vide)
   - **Developer contact information - Email:** (ton email)
   - **Clique:** `SAVE AND CONTINUE`

4. **Page 2/4 - Scopes:**
   - **Clique:** `ADD OR REMOVE SCOPES`

   **Dans la popup qui s'ouvre:**
   - Cherche: `Google Drive API`
   - **Coche:** `.../auth/drive` (accès complet Drive)
   - Cherche: `Google Sheets API`
   - **Coche:** `.../auth/spreadsheets` (accès complet Sheets)
   - **Scroll en bas** → Clique `UPDATE`

   - **Retour à la page** → Clique `SAVE AND CONTINUE`

5. **Page 3/4 - Test users:**
   - **Clique:** `+ ADD USERS`
   - **Entre ton email Gmail** (celui que tu utilises)
   - **Clique:** `ADD`
   - **Clique:** `SAVE AND CONTINUE`

6. **Page 4/4 - Summary:**
   - **Vérifie** les infos
   - **Clique:** `BACK TO DASHBOARD`

---

### Étape 5: Créer OAuth Client ID (3 min)

1. **Menu gauche** → **"Credentials"**

2. **En haut**, clique **"+ CREATE CREDENTIALS"**

3. **Sélectionne:** `OAuth client ID`

4. **Formulaire qui apparaît:**

   - **Application type:** Sélectionne `Web application`

   - **Name:** `N8N Workflow Automation`

   - **Authorized JavaScript origins:** (laisse vide)

   - **Authorized redirect URIs:**
     - **Clique:** `+ ADD URI`
     - **Colle EXACTEMENT:** `https://n8n.srv1168256.hstgr.cloud/rest/oauth2-credential/callback`
     - **⚠️ IMPORTANT:** Vérifie qu'il n'y a PAS d'espace avant/après l'URL

   - **Clique:** `CREATE`

5. **Popup "OAuth client created"** apparaît:

   **📝 COPIE CES 2 VALEURS IMMÉDIATEMENT:**

   - **Your Client ID:** (commence par `XXX-YYY.apps.googleusercontent.com`)
   - **Your Client Secret:** (chaîne aléatoire type `GOCSPX-...`)

   **💾 Sauvegarde-les** dans un fichier texte temporaire ou Notes

6. **Clique:** `OK`

---

## PARTIE 2: CRÉER CREDENTIALS N8N (5 min)

### Credential 1/3: Google Drive OAuth2

1. **Retour N8N:** https://n8n.srv1168256.hstgr.cloud

2. **Menu gauche** → **Credentials** → **+ Add Credential**

3. **Cherche:** `Google Drive OAuth2 API`

4. **Remplis:**
   - **OAuth Redirect URL:** (déjà affiché - ne touche pas)
   - **Client ID:** Colle la valeur copiée de Google Cloud Console
   - **Client Secret:** Colle la valeur copiée de Google Cloud Console
   - **Allowed HTTP Request Domains:** Laisse `All`

5. **Scroll en bas** → **Clique** le bouton **"Sign in with Google"** ou **"OAuth 2.0"**

6. **Popup Google s'ouvre:**
   - **Sélectionne** ton compte Gmail
   - **Tu verras:** "Google hasn't verified this app" ⚠️
   - **C'EST NORMAL** - Clique **"Advanced"** (en bas à gauche)
   - **Clique:** "Go to N8N Alpha Medical Automation (unsafe)" (en bas)
   - **Page permissions** → **Coche** "See, edit, create, and delete all of your Google Drive files"
   - **Clique:** `Continue`

7. **Retour automatique N8N** - Connection réussie ✅

8. **Name:** `Google Drive account`

9. **Clique:** `Save`

---

### Credential 2/3: Google Sheets OAuth2

**Même processus, MÊMES credentials:**

1. **Add Credential** → `Google Sheets OAuth2 API`

2. **Remplis:**
   - **Client ID:** (MÊME valeur que Google Drive)
   - **Client Secret:** (MÊME valeur que Google Drive)

3. **Sign in with Google**

4. **Popup:**
   - Sélectionne compte
   - "Advanced" → "Go to... (unsafe)"
   - Permissions Sheets → `Continue`

5. **Name:** `Google Sheets account`

6. **Save**

---

### Credential 3/3: Google Gemini API

**Différent - Simple API Key:**

1. **Nouvel onglet:** https://aistudio.google.com/app/apikey

2. **Clique:** `Get API key` ou `Create API key`

3. **Sélectionne:** `Create API key in existing project`

4. **Dropdown projet** → Choisis `n8n-alpha-medical`

5. **Clique:** `Create`

6. **Copie la clé** (commence par `AIza...`)

7. **Retour N8N** → **Add Credential** → `Google Gemini (PaLM) API`

8. **Remplis:**
   - **API Key:** Colle la clé copiée

9. **Name:** `Google Gemini API account`

10. **Save**

---

## ✅ VÉRIFICATION

**Dans N8N → Credentials, tu devrais avoir 3 credentials:**

- ✅ `Google Drive account` (OAuth2)
- ✅ `Google Sheets account` (OAuth2)
- ✅ `Google Gemini API account` (API Key)

---

## 🚀 ACTIVER LE WORKFLOW IMAGE PROCESSING

1. **N8N Menu** → **Workflows**

2. **Cherche:** `Enhance Product Photos with Google Gemini AI for E-commerce Catalog`

3. **Ouvre** le workflow

4. **Vérifie** que les nodes ne sont plus rouges (erreurs credentials)

5. **En haut à droite** → Toggle **"Active"** → **ON**

6. **Workflow actif!** ✅

---

## 🧪 TESTER LE WORKFLOW

### Test 1: Upload Image

1. **Va sur Google Drive Input folder:**
   https://drive.google.com/drive/folders/1gs_U0T9ZapXtlrrvzxS9IX0AI9Qllnox

2. **Upload 1 photo** de produit médical

3. **Attends 5 minutes** (workflow check automatiquement toutes les 5 min)

### Test 2: Vérifier Output

1. **Ouvre Output folder:**
   https://drive.google.com/drive/folders/1O1PrZoTDweXQx8ImVLXlJArei9hdvizn

2. **Tu devrais voir:** `filename_clean.jpg`

3. **Ouvre l'image** → Background devrait être gris gradient propre ✅

### Test 3: Vérifier Google Sheet

1. **Ouvre le Sheet:**
   https://docs.google.com/spreadsheets/d/1Q5ujL0LQEz-kgGkg-oMzCutcpUnznpDPpRkqh1hUBUw/edit

2. **Tab "Photos"** devrait avoir 1 ligne:
   - File name: ton fichier
   - Status: "Completed"
   - Start Time: timestamp
   - End Time: timestamp
   - Input File: lien Drive
   - Output File: lien Drive

**Si tout ça marche → Workflow opérationnel!** 🎉

---

## 🐛 TROUBLESHOOTING

### Erreur: "Google hasn't verified this app"
**Normal!** C'est parce que ton app est en "Test mode"
- Clique "Advanced"
- Clique "Go to... (unsafe)"
- Continue

### Erreur: "Redirect URI mismatch"
**Cause:** L'URL de redirect n'est pas exactement la même
**Fix:**
1. Retourne Google Cloud Console → Credentials → Ton OAuth Client ID
2. Vérifie Authorized redirect URIs
3. Doit être EXACTEMENT: `https://n8n.srv1168256.hstgr.cloud/rest/oauth2-credential/callback`
4. Pas d'espace, pas de slash à la fin

### Erreur: "Invalid Client ID"
**Cause:** Client ID ou Secret mal copié
**Fix:**
1. Vérifie qu'il n'y a pas d'espace avant/après
2. Régénère un nouveau secret si nécessaire dans Google Cloud Console

### Workflow reste inactif
**Cause:** Credentials pas assignés aux nodes
**Fix:**
1. Ouvre le workflow
2. Clique chaque node qui utilise Google (Drive, Sheets, Gemini)
3. Dans chaque node, sélectionne le bon credential dans le dropdown
4. Save le workflow

---

## 📝 NOTES IMPORTANTES

**Réutilisation credentials:**
- Les MÊMES Client ID/Secret fonctionnent pour Drive ET Sheets
- Pas besoin de créer 2 OAuth clients différents
- Juste créer 2 credentials N8N qui pointent vers le même OAuth client

**Sécurité:**
- Client Secret = comme un mot de passe
- Ne le partage JAMAIS publiquement
- Ne le commite JAMAIS sur GitHub

**Quotas:**
- Google Drive API: 1 milliard de requêtes/jour (gratuit)
- Google Sheets API: 100 requêtes/100 secondes/user
- Google Gemini API: Varie selon ton plan

---

## ⏱️ TEMPS TOTAL

- Google Cloud Console: **15 min**
- N8N Credentials: **5 min**
- Total: **20 minutes**

Une fois fait, ces credentials sont **réutilisables** pour le Workflow YouTube aussi!

---

**Bon courage! Si tu bloques quelque part, copie-moi le message d'erreur exact.** 🚀
