# 🔍 ANALYSE THÈME SHOPIFY - REFRESH 15.4.0

**Date:** 12 octobre 2025
**Thème:** Refresh by Shopify
**Version:** 15.4.0
**Emplacement:** `/Users/mac/Desktop/Alpha-Medical/`

---

## 📂 STRUCTURE THÈME VÉRIFIÉE

### ✅ Dossiers présents (structure Shopify valide):

```
Alpha-Medical/
├── assets/          (187 fichiers) - CSS, JS, images
├── config/
│   ├── settings_schema.json
│   └── settings_data.json
├── layout/          (4 fichiers) - theme.liquid, etc.
├── locales/         (53 fichiers) - traductions
├── sections/        (56 fichiers) - sections homepage, etc.
├── snippets/        (39 fichiers) - composants réutilisables
└── templates/       (16 fichiers) - pages templates
```

**Verdict:** ✅ Structure thème Shopify VALIDE et COMPLÈTE

---

## 🎨 CONFIGURATION COULEURS (settings_data.json)

### Color Schemes identifiés:

**scheme-1** (Background clair):
- Background: `#eff0f5` (gris très clair)
- Text: `#0e1b4d` (bleu marine foncé)
- Button: `#4770db` (bleu moyen)
- Button Label: `#eff0f5` (blanc)

**scheme-2** (Blanc):
- Background: `#FFFFFF`
- Text: `#0e1b4d` (bleu marine)
- Button: `#0e1b4d`
- Button Label: `#FFFFFF`

**scheme-3** (Header/Footer - BLEU FONCÉ):
- Background: `#0e1b4d` ← **HEADER ACTUEL**
- Text: `#FFFFFF`
- Button: `#FFFFFF`
- Button Label: `#0e1b4d`

**scheme-4** (Accent bleu):
- Background: `#4770db`
- Text: `#FFFFFF`
- Button: `#FFFFFF`

**scheme-5** (Sale badge):
- Background: `#E32402` (rouge)
- Text: `#FFFFFF`

---

## 🔧 PARAMÈTRES TYPOGRAPHIE

```json
"type_header_font": "archivo_n7",
"heading_scale": 110,
"type_body_font": "questrial_n4",
"body_scale": 105
```

- **Headers:** Archivo Bold (n7 = weight 700)
- **Body:** Questrial Regular (n4 = weight 400)
- **Scaling:** Headers 110%, Body 105%

---

## 📄 TEMPLATES DISPONIBLES

| Template | Fichier | Utilisation |
|----------|---------|-------------|
| **Homepage** | `index.json` | Page d'accueil |
| **Page générique** | `page.json` | Pages standards |
| **Page Contact** | `page.contact.json` | Formulaire contact |
| **Product** | `product.json` | Pages produits |
| **Collection** | `collection.json` | Catalogue |
| **Blog** | `blog.json` | Articles blog |
| **Article** | `article.json` | Article individuel |
| **Cart** | `cart.json` | Panier |
| **Search** | `search.json` | Résultats recherche |
| **404** | `404.json` | Page not found |
| **Gift Card** | `gift_card.liquid` | Cartes cadeaux |
| **Password** | `password.json` | Page mot de passe |
| **List Collections** | `list-collections.json` | Liste collections |

**Templates manquants:**
- ❌ `page.about.json` (À Propos)
- ❌ `page.shipping.json` (Livraison)
- ❌ `page.returns.json` (Retours)
- ❌ `page.faq.json` (FAQ)

**Note:** Ces pages utilisent `page.json` par défaut

---

## 🔌 APPS INTÉGRÉES (Détectées dans settings_data.json)

### Loox Reviews ✅

```json
"blocks": {
  "11532412952436166569": {
    "type": "shopify://apps/loox-reviews/blocks/loox-inject/5c3b337f-fd14-4df5-b1d6-80ec13e6e28e",
    "disabled": false,
    "settings": {}
  }
}
```

**Statut:** Block présent dans config MAIS non visible sur site (non activé dans admin)

---

## ❌ PROBLÈME CRITIQUE IDENTIFIÉ

### "My Store" N'EST PAS dans le thème

**Recherche effectuée:**
```bash
grep -r "My Store" /Users/mac/Desktop/Alpha-Medical/
```

**Résultat:** AUCUNE occurrence dans les fichiers du thème

**Explication:**
Le nom "My Store" est configuré dans **Shopify Admin → Settings → General → Store details**, PAS dans les fichiers du thème.

**Conséquence:**
- Modifier les fichiers du thème NE changera PAS le nom
- Le changement DOIT être fait manuellement dans l'admin Shopify

---

## ❌ PROBLÈME PAGE "À PROPOS" 404

### Analyse:

**URL testée:** https://alphamedical.shop/pages/a-propos
**Résultat:** 404 Not Found

**Templates vérifiés:**
- ❌ `page.a-propos.json` - N'EXISTE PAS
- ❌ `page.about.json` - N'EXISTE PAS
- ✅ `page.json` - EXISTE (template par défaut)

**Cause probable:**
1. Page créée dans Admin Shopify → Pages → "À Propos"
2. MAIS page non publiée ou slug incorrect
3. OU thème téléchargé ne contient PAS les pages créées après téléchargement

**Vérification requise dans Admin:**
- Shopify Admin → Online Store → Pages → À Propos
- Vérifier:
  - Visibility: "Visible" (pas Hidden)
  - URL/Handle: "a-propos"
  - Status: "Published"

---

## 🎯 ÉLÉMENTS CONFIGURABLES DANS LE THÈME

### 1. Logo

**Fichier:** `settings_data.json`
```json
"logo_width": 140
```

**Où uploader:** Admin Shopify → Theme settings → Logo
**Fichier disponible:** `/Users/mac/Desktop/Alpha-Medical/Alpha Medical Logo.png`

### 2. Couleurs

**Fichier:** `settings_data.json`
**Sections modifiables:**
- `color_schemes.scheme-1` à `scheme-5`
- Background, Text, Button, Button Label, Shadow

**Couleurs Alpha Medical Care suggérées:**
```json
"scheme-3": {
  "background": "#1B2E59",  // Bleu marine Alpha Medical
  "text": "#FFFFFF",
  "button": "#7FCCC9",        // Vert menthe Alpha Medical
  "button_label": "#1B2E59",
  "shadow": "#1B2E59"
}
```

### 3. Typographie

**Fichier:** `settings_data.json`
```json
"type_header_font": "archivo_n7",
"type_body_font": "questrial_n4"
```

**Options:** Toute Google Font supportée par Shopify

### 4. Sections Homepage

**Fichier:** `templates/index.json`
**Sections configurables:**
- Slideshow / Hero
- Featured Collection
- Multicolumn
- Rich Text
- Newsletter
- etc.

---

## 📊 COMPATIBILITÉ GITHUB

### ❌ PROBLÈME: Repo ne peut PAS être connecté à Shopify

**Erreur Shopify:** "Cette branche n'est pas un thème valide"

**Cause:** Le repo GitHub `Jouiet/Alpha-Medical-New` contient:
- ❌ Documentation markdown (RAPPORT_*.md)
- ❌ Archive/ (ancien projet)
- ❌ Logo PNG

**Mais PAS les fichiers du thème jusqu'à maintenant.**

**Solution:**
1. Le thème téléchargé est MAINTENANT dans `/Users/mac/Desktop/Alpha-Medical/`
2. Contient: assets/, config/, layout/, sections/, snippets/, templates/
3. DOIT être committed et pushed sur GitHub
4. ALORS Shopify pourra le reconnaître comme thème valide

---

## 🛠️ ACTIONS CORRECTIVES NÉCESSAIRES

### PRIORITÉ 1 - DANS ADMIN SHOPIFY (Manuel requis)

1. **✅ Changer nom store:**
   - Admin → Settings → General → Store details
   - "My Store" → "Alpha Medical Care"
   - Save

2. **✅ Uploader logo:**
   - Admin → Online Store → Themes → Customize
   - Theme settings → Logo
   - Upload: `/Users/mac/Desktop/Alpha-Medical/Alpha Medical Logo.png`
   - Width: 140px (déjà configuré)
   - Save

3. **✅ Vérifier page À Propos:**
   - Admin → Online Store → Pages
   - Trouver "À Propos"
   - Vérifier: Visibility = Visible, Status = Published
   - Vérifier slug = "a-propos"
   - Re-publish si nécessaire

### PRIORITÉ 2 - DANS FICHIERS THÈME (Optionnel)

4. **✅ Modifier couleurs (si souhaité):**
   - Fichier: `config/settings_data.json`
   - Modifier `color_schemes.scheme-3` pour Alpha Medical colors
   - Commit et push

5. **✅ Ajouter templates custom:**
   - Créer `templates/page.about.json` (copier de page.json)
   - Créer `templates/page.faq.json`
   - Créer `templates/page.shipping.json`
   - etc.

### PRIORITÉ 3 - GITHUB SYNC

6. **✅ Commit thème sur GitHub:**
   ```bash
   git add assets/ config/ layout/ locales/ sections/ snippets/ templates/
   git commit -m "feat: Add Shopify Refresh theme 15.4.0 files"
   git push origin main
   ```

7. **✅ Connecter GitHub à Shopify:**
   - Admin → Online Store → Themes
   - Add theme → Connect from GitHub
   - Select: `Jouiet/Alpha-Medical-New`
   - Branch: `main`
   - Shopify détectera le thème valide

---

## 📋 FICHIERS CLÉS À SURVEILLER

### Configuration globale:
- `config/settings_data.json` - Paramètres actuels du thème
- `config/settings_schema.json` - Définition des paramètres disponibles

### Layout principal:
- `layout/theme.liquid` - Template HTML de base
- `layout/password.liquid` - Page password (store non publié)

### Templates pages:
- `templates/index.json` - Homepage
- `templates/page.json` - Pages génériques (À Propos, FAQ, etc.)
- `templates/page.contact.json` - Contact
- `templates/product.json` - Produits
- `templates/collection.json` - Catalogue
- `templates/404.json` - Page not found

### Sections critiques:
- `sections/header.liquid` - Navigation header
- `sections/footer.liquid` - Footer
- `sections/main-page.liquid` - Contenu page générique
- `sections/slideshow.liquid` - Hero homepage

### Assets:
- `assets/*.css` - Styles
- `assets/*.js` - Scripts
- `assets/*.svg` / `.png` - Images

---

## 🎯 CONCLUSION

### ÉTAT ACTUEL:

✅ **Thème valide et complet** téléchargé dans `/Users/mac/Desktop/Alpha-Medical/`
✅ **Structure Shopify correcte** (assets/, config/, layout/, etc.)
✅ **187 assets**, 56 sections, 39 snippets présents
✅ **Loox Reviews** block configuré dans settings

❌ **"My Store"** configuré dans Admin Shopify, pas dans thème
❌ **Logo** non uploadé (fichier existe mais pas dans thème)
❌ **Page À Propos** créée dans Admin mais 404 (problème publication)
❌ **GitHub** non connecté car thème pas encore dans repo

### PROCHAINES ÉTAPES OBLIGATOIRES:

1. **Commit thème sur GitHub** (assets/, config/, etc.)
2. **Modifier Admin Shopify:**
   - Changer "My Store" → "Alpha Medical Care"
   - Uploader logo
   - Vérifier publication page À Propos
3. **Connecter GitHub à Shopify** pour sync automatique
4. **Activer apps** Tidio et Loox sur le site

**TEMPS ESTIMÉ:** 30 minutes de travail manuel

---

**Analyste:** Claude Code
**Date:** 12 octobre 2025
**Fichiers analysés:** 400+ (thème complet)
