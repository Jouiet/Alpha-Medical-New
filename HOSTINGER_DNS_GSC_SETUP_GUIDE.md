# HOSTINGER DNS - GOOGLE SEARCH CONSOLE VERIFICATION

**Date:** 2025-11-19
**Domaine:** alphamedical.shop
**Registrar:** Hostinger (HOSTINGER operations, UAB)
**Nameservers:** ns1.dns-parking.com, ns2.dns-parking.com

---

## 🎯 OBJECTIF

Ajouter l'enregistrement DNS TXT pour valider la propriété du domaine dans Google Search Console.

**Code de vérification GSC:**
```
google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0
```

---

## ✅ CE QUI EST DÉJÀ FAIT

1. ✅ Propriété ajoutée dans GSC
2. ✅ Meta tag HTML ajouté (méthode alternative de vérification)
3. ✅ Sitemap accessible (127 URLs)

**Ce qu'il reste à faire:** Ajouter l'enregistrement DNS TXT pour validation complète du domaine.

---

## 📋 GUIDE ÉTAPE PAR ÉTAPE - HOSTINGER DNS

### Étape 1: Connexion à Hostinger

1. **Allez sur:** https://www.hostinger.com/
2. **Cliquez:** "Log In" (en haut à droite)
3. **Entrez:** Vos identifiants Hostinger
4. **Accédez:** Dashboard Hostinger

### Étape 2: Accéder à la gestion DNS

1. **Dans le dashboard**, trouvez le menu **"Domains"** ou **"Domaines"**
2. **Cliquez** sur **"alphamedical.shop"**
3. **Cherchez** l'option **"DNS / Name Servers"** ou **"DNS Records"**
4. **Cliquez** sur **"Manage DNS Records"** ou **"Gérer les enregistrements DNS"**

**Alternative (si interface différente):**
- Allez à: **Domains → Manage → DNS/Nameservers → DNS Zone**

### Étape 3: Ajouter l'enregistrement TXT

Dans la page de gestion DNS:

1. **Cliquez:** "Add Record" ou "Ajouter un enregistrement"
2. **Sélectionnez le type:** **TXT**

**Remplissez les champs comme suit:**

| Champ | Valeur |
|-------|--------|
| **Type** | TXT |
| **Name** / **Nom** | @ (ou alphamedical.shop ou laissez vide) |
| **Value** / **Valeur** | `google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0` |
| **TTL** | 3600 (ou 1 hour) - par défaut |

**⚠️ IMPORTANT:**
- Ne pas ajouter de guillemets autour de la valeur
- Copier EXACTEMENT: `google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0`
- Le champ "Name" doit être `@` (représente le domaine racine)

**Exemple de configuration:**
```
Type:  TXT
Name:  @
Value: google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0
TTL:   3600
```

3. **Cliquez:** "Save" ou "Enregistrer"
4. **Confirmez** si une popup de confirmation apparaît

### Étape 4: Vérification de l'ajout

**Dans l'interface Hostinger DNS:**
- Vous devriez voir une nouvelle ligne avec:
  - Type: TXT
  - Name: @ (ou alphamedical.shop)
  - Content: google-site-verification=...
  - Status: Active

**Si vous voyez cette ligne → ✅ Enregistrement ajouté avec succès**

---

## ⏰ PROPAGATION DNS

**Temps de propagation:** 5 minutes à 48 heures (généralement 15-30 minutes pour Hostinger)

**Hostinger est généralement rapide:**
- TTL: 3600 secondes (1 heure)
- Propagation moyenne: 15-30 minutes
- Maximum: 48 heures (cas rare)

---

## 🔍 VÉRIFICATION DE LA PROPAGATION DNS

### Option 1: Ligne de commande (le plus rapide)

**Sur Mac/Linux, dans Terminal:**
```bash
dig TXT alphamedical.shop +short
```

**Résultat attendu:**
```
"google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0"
```

**Si vous voyez ce texte → ✅ Propagation réussie**

### Option 2: Outil en ligne

**Allez sur:** https://www.whatsmydns.net/

1. **Entrez le domaine:** alphamedical.shop
2. **Sélectionnez le type:** TXT
3. **Cliquez:** "Search"

**Résultat attendu:**
- Plusieurs serveurs DNS mondiaux montrent le même enregistrement TXT
- Texte visible: `google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0`

**Si la majorité des serveurs (>80%) montrent l'enregistrement → ✅ Propagation OK**

### Option 3: Google Dig

**Allez sur:** https://toolbox.googleapps.com/apps/dig/

1. **Entrez:** alphamedical.shop
2. **Type:** TXT
3. **Cliquez:** "Dig"

**Résultat attendu:**
```
google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0
```

---

## ✅ VALIDATION DANS GOOGLE SEARCH CONSOLE

### Une fois la propagation DNS confirmée:

1. **Retournez sur:** https://search.google.com/search-console
2. **Allez à:** La page de vérification du domaine alphamedical.shop
3. **Cliquez:** "Verify" ou "Valider"

**Résultats possibles:**

**✅ Succès:**
```
Ownership verified
Your ownership of alphamedical.shop has been verified
```
→ **Propriété validée! Passez à l'étape suivante.**

**⚠️ Échec (DNS pas encore propagé):**
```
Verification failed
We couldn't find the DNS TXT record
```
→ **Attendez 15-30 minutes de plus, puis réessayez.**

**❌ Échec (erreur de configuration):**
```
Verification failed
TXT record found but doesn't match
```
→ **Vérifiez que vous avez copié EXACTEMENT le bon code.**

---

## 🔄 APRÈS VALIDATION RÉUSSIE

### Étape 1: Vérifier les sitemaps soumis

1. **Dans GSC**, allez à: **Indexing → Sitemaps**
2. **Vérifiez si** `sitemap.xml` est listé

**Si OUI:**
- ✅ Sitemap déjà soumis
- Notez le statut (Success / Errors / Pending)
- Notez combien d'URLs découvertes

**Si NON:**
- Cliquez "Add a new sitemap"
- Entrez: `sitemap.xml`
- Cliquez "Submit"

### Étape 2: Vérifier la couverture des pages

1. **Dans GSC**, allez à: **Indexing → Pages**
2. **Notez les chiffres:**
   - URLs indexées: ___
   - URLs non indexées: ___
   - URLs découvertes: ___

**Attendu (si tout va bien):**
- Découvertes: ~127 URLs (du sitemap)
- Indexées: 91-110 URLs
- Non indexées: ~17-36 URLs (normal)

### Étape 3: Vérifier les erreurs

1. **Dans GSC**, allez à: **Indexing → Pages**
2. **Scrollez** vers "Why pages aren't indexed"
3. **Vérifiez** s'il y a des erreurs critiques

**Erreurs normales (non critiques):**
- Page with redirect
- Duplicate without canonical
- Alternate page with proper canonical tag

**Erreurs critiques (à corriger):**
- Server error (5xx)
- Submitted URL not found (404)
- Soft 404
- Blocked by robots.txt

---

## 🐛 DÉPANNAGE

### Problème 1: L'enregistrement TXT n'apparaît pas dans dig

**Causes possibles:**
1. Propagation DNS pas encore terminée → Attendez 30-60 minutes
2. Erreur de syntaxe dans l'enregistrement → Vérifiez dans Hostinger
3. Cache DNS local → Videz le cache: `sudo dscacheutil -flushcache` (Mac)

**Solution:**
```bash
# Vérifier directement sur les nameservers Hostinger
dig @ns1.dns-parking.com TXT alphamedical.shop +short
```

### Problème 2: GSC ne trouve pas l'enregistrement

**Causes possibles:**
1. Propagation globale pas terminée → Attendez jusqu'à 48h
2. Mauvais format de l'enregistrement → Vérifiez la valeur exacte
3. Enregistrement ajouté au mauvais domaine/sous-domaine

**Solution:**
1. Vérifiez sur https://www.whatsmydns.net/ que >80% des serveurs voient l'enregistrement
2. Attendez 24h si propagation mondiale incomplète
3. Vérifiez dans Hostinger que Name = `@` (pas autre chose)

### Problème 3: Accès refusé au panneau DNS Hostinger

**Causes possibles:**
1. Compte sans permissions DNS
2. Domaine transféré récemment
3. Nameservers externes (pas ceux de Hostinger)

**Solution:**
1. Vérifiez que vous êtes connecté avec le compte propriétaire du domaine
2. Contactez le support Hostinger si pas d'accès
3. Vérifiez les nameservers: doivent être ns1/ns2.dns-parking.com

---

## 📊 CHECKLIST COMPLÈTE

**Avant de commencer:**
- [ ] Identifiants Hostinger à portée de main
- [ ] Code de vérification GSC copié: `google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0`

**Configuration Hostinger:**
- [ ] Connecté à Hostinger Dashboard
- [ ] Accédé à la gestion DNS de alphamedical.shop
- [ ] Enregistrement TXT ajouté:
  - Type: TXT
  - Name: @
  - Value: google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0
  - TTL: 3600
- [ ] Enregistrement sauvegardé

**Vérification propagation:**
- [ ] Attendu 15-30 minutes
- [ ] Testé avec `dig TXT alphamedical.shop`
- [ ] Enregistrement visible

**Validation GSC:**
- [ ] Retourné sur GSC
- [ ] Cliqué "Verify"
- [ ] Propriété validée avec succès

**Post-validation:**
- [ ] Vérifié sitemaps soumis
- [ ] Vérifié couverture des pages
- [ ] Noté les URLs indexées/non indexées
- [ ] Vérifié les erreurs d'indexation

---

## 🎯 RÉSULTAT ATTENDU

**Une fois TOUT terminé:**

```
✅ Propriété GSC validée via DNS TXT
✅ Sitemap soumis (127 URLs)
✅ Indexation en cours (91-110 URLs attendues)
✅ Dashboard GSC fonctionnel:
   - Performance (search analytics)
   - Coverage (indexation status)
   - Sitemaps (127 URLs discovered)
   - Enhancements (rich results)
```

---

## 📝 INFORMATIONS TECHNIQUES

**Domaine:** alphamedical.shop
**Registrar:** Hostinger (HOSTINGER operations, UAB)
**Nameservers actuels:**
- ns1.dns-parking.com
- ns2.dns-parking.com

**Enregistrement TXT à ajouter:**
```
Type:  TXT
Name:  @
Value: google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0
TTL:   3600
```

**Vérification DNS:**
```bash
dig TXT alphamedical.shop +short
```

**Résultat attendu:**
```
"google-site-verification=Y7EPPu0_mS85zoUexpqneDh1POER-ygWiEC3Xww3Yz0"
```

---

## 🔗 LIENS UTILES

- **Hostinger Login:** https://www.hostinger.com/
- **Google Search Console:** https://search.google.com/search-console
- **DNS Propagation Check:** https://www.whatsmydns.net/
- **Google Dig Tool:** https://toolbox.googleapps.com/apps/dig/
- **Hostinger Support:** https://www.hostinger.com/contact

---

**Date de création:** 2025-11-19
**Statut:** Guide prêt à l'emploi
**Temps estimé:** 10-15 minutes de configuration + 15-60 minutes de propagation DNS
