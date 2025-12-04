# SOLUTION: AJOUTER FILTRE POUR ÉVITER BOUCLE INFINIE

## PROBLÈME ACTUEL

Le workflow retraite ses propres outputs en boucle:
```
5-lifestyle.jpg → 5-lifestyle_clean.png → 5-lifestyle_clean_clean.png → ...
```

## POURQUOI?

Les fichiers output (avec "_clean" dans le nom) se retrouvent dans le dossier INPUT 
et sont détectés par les triggers comme de nouveaux fichiers à traiter.

## SOLUTION: AJOUTER UN FILTRE

Modifier le workflow N8N pour ajouter un node "IF" qui vérifie si le fichier 
contient déjà "_clean" dans le nom. Si oui, ignorer.

### ÉTAPES MANUELLES (via interface N8N):

1. Ouvrir workflow: https://n8n.srv1168256.hstgr.cloud/workflow/q0kyXyhCUq5gjmG2

2. Ajouter un node "IF" après "Set File ID":
   - Position: Entre "Set File ID" et "Workflow Configuration"
   - Condition: `{{ $json.input_file_name.includes('_clean') }}`
   - Si TRUE: Ne rien faire (arrêter le workflow)
   - Si FALSE: Continuer normalement

3. Configuration du node IF:
   ```
   Conditions:
     - Value 1: {{ $json.input_file_name }}
     - Operation: contains
     - Value 2: _clean
   
   If TRUE: → Fin (ne rien traiter)
   If FALSE: → Workflow Configuration (traiter normalement)
   ```

4. Sauvegarder et réactiver le workflow

### RÉSULTAT

Le workflow traitera seulement les images originales (sans "_clean" dans le nom)
et ignorera tous les outputs précédents.

## ALTERNATIVE: SUPPRIMER FICHIERS INPUT APRÈS TRAITEMENT

Ajouter un node "Delete File" qui supprime le fichier INPUT après qu'il soit 
traité avec succès. Cela empêche aussi la boucle.

