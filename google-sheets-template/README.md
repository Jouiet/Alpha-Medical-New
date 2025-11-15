# GOOGLE SHEETS TEMPLATES - Bundle Auto-Creation

## IMPORT RAPIDE

### Étape 1: Créer Google Sheet
1. Aller sur Google Sheets: https://sheets.google.com
2. Créer nouveau spreadsheet
3. Nommer: **"Bundle Proposals Auto-Creation"**

### Étape 2: Importer Template PROPOSALS

1. Créer nouvelle sheet, nommer: **PROPOSALS**
2. Copier les colonnes headers:

```
Timestamp | Email | Hash | Product_IDs | Product_Handles | Count | Bundle_Created
```

3. Ou importer `PROPOSALS_TEMPLATE.csv`:
   - File → Import → Upload → PROPOSALS_TEMPLATE.csv
   - Import location: Replace current sheet
   - Separator type: Comma

### Étape 3: Ajouter Formule Count

1. Cliquer cellule **F2** (colonne Count)
2. Entrer formule:
```
=COUNTIF($C$2:$C, C2)
```
3. Cette formule compte automatiquement les proposals avec le même hash

### Étape 4: Créer Sheet BUNDLES_CREATED

1. Créer nouvelle sheet (cliquer + en bas)
2. Nommer: **BUNDLES_CREATED**
3. Copier les colonnes headers:

```
Hash | Bundle_ID | Bundle_Title | Bundle_URL | Created_At | Customer_Count | Customer_Emails
```

4. Ou importer `BUNDLES_CREATED_TEMPLATE.csv`

---

## STRUCTURE FINALE

Votre Google Sheet doit avoir **2 sheets**:

### Sheet 1: PROPOSALS

| Column | Name | Type | Description |
|--------|------|------|-------------|
| A | Timestamp | Date | Auto (Apps Script insère) |
| B | Email | Text | Email du customer |
| C | Hash | Text | Hash unique (ex: hash_a1b2c3d4e5f6) |
| D | Product_IDs | JSON | Array d'IDs (ex: [123,456,789]) |
| E | Product_Handles | JSON | Array de handles (ex: ["knee","ankle"]) |
| F | Count | Formula | =COUNTIF($C$2:$C, C2) |
| G | Bundle_Created | Boolean | FALSE/TRUE (Apps Script update) |

**Note**: Les lignes sont ajoutées automatiquement par Apps Script quand email reçu de Gmail.

### Sheet 2: BUNDLES_CREATED

| Column | Name | Type | Description |
|--------|------|------|-------------|
| A | Hash | Text | Hash de la proposition |
| B | Bundle_ID | Number | Shopify product ID |
| C | Bundle_Title | Text | Titre du bundle créé |
| D | Bundle_URL | Text | URL du bundle |
| E | Created_At | Date | Date de création |
| F | Customer_Count | Number | Nombre de customers (10+) |
| G | Customer_Emails | JSON | Array d'emails notifiés |

**Note**: Les lignes sont ajoutées automatiquement par Apps Script après création bundle.

---

## EXEMPLE DE DONNÉES

### PROPOSALS (après quelques submissions):

```
Timestamp           | Email              | Hash            | Product_IDs        | Product_Handles      | Count | Bundle_Created
2025-11-15 10:30:00 | user1@email.com    | hash_abc123def  | [123,456,789]      | ["knee","ankle","back"] | 1     | FALSE
2025-11-15 11:15:00 | user2@email.com    | hash_abc123def  | [123,456,789]      | ["knee","ankle","back"] | 2     | FALSE
2025-11-15 12:00:00 | user3@email.com    | hash_xyz789ghi  | [111,222,333]      | ["posture","led"]    | 1     | FALSE
...
2025-11-15 15:45:00 | user10@email.com   | hash_abc123def  | [123,456,789]      | ["knee","ankle","back"] | 10    | TRUE
```

**Note**: Quand Count atteint 10, Apps Script crée automatiquement le bundle et update Bundle_Created = TRUE.

### BUNDLES_CREATED (après auto-création):

```
Hash            | Bundle_ID   | Bundle_Title           | Bundle_URL                    | Created_At          | Customer_Count | Customer_Emails
hash_abc123def  | 7623087001  | Custom Bundle #ABC123  | /products/custom-bundle-abc123 | 2025-11-15 15:45:00 | 10             | ["user1@...","user2@..."...]
hash_xyz789ghi  | 7623087002  | Custom Bundle #XYZ789  | /products/custom-bundle-xyz789 | 2025-11-16 10:30:00 | 12             | ["user3@...","user4@..."...]
```

---

## FORMULES IMPORTANTES

### Colonne F (Count) - PROPOSALS Sheet

**Cellule F2**:
```
=COUNTIF($C$2:$C, C2)
```

**Explication**:
- `$C$2:$C` : Plage absolue de la colonne Hash (C) depuis ligne 2 jusqu'à la fin
- `C2` : Hash de la ligne actuelle (relatif)
- Résultat: Nombre de fois que le hash apparaît dans toute la colonne

**Auto-fill**: Quand Apps Script ajoute nouvelle ligne, la formule se copie automatiquement.

---

## PERMISSIONS

### Apps Script Access

Quand vous déployez Apps Script, configurez:
- **Execute as**: Me (votre compte Google)
- **Who has access**: Anyone (pour recevoir webhooks Gmail)

### Sheet Permissions

Le spreadsheet peut rester privé (seulement vous). Apps Script a accès car il s'exécute sous votre compte.

---

## NEXT STEP

Après avoir créé le Google Sheet avec cette structure:

1. ✅ Sheet créé avec 2 tabs: PROPOSALS, BUNDLES_CREATED
2. ✅ Headers ajoutés
3. ✅ Formule Count configurée

→ **Passer à**: Déploiement Apps Script (voir `DEPLOYMENT_GUIDE_COMPLETE.md`)

---

**STATUS**: ✅ TEMPLATES PRÊTS POUR IMPORT
