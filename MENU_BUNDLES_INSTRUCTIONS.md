# INSTRUCTIONS - AJOUT "BUNDLES" AU MENU PRINCIPAL

**Date**: 2025-11-15
**Action**: Ajouter lien "Bundles" au menu principal
**Durée**: 2 minutes

---

## ÉTAPES (Admin Shopify UI)

1. **Connexion Admin Shopify**
   - URL: https://azffej-as.myshopify.com/admin
   - Section: Online Store → Navigation

2. **Modifier Menu Principal**
   - Cliquer sur **"Main menu"**
   - Cliquer sur **"Add menu item"**

3. **Ajouter Lien Bundles**
   - **Name**: `Bundles`
   - **Link**: `/pages/bundles` (ou chercher "Medical Equipment Bundles" dans les pages)
   - **Position**: Placer après "Catalog" (position #3)

4. **Sauvegarder**
   - Cliquer sur **"Save"**

---

## RÉSULTAT ATTENDU

Menu principal (ordre):
1. Home
2. Catalog
3. **Bundles** ⬅️ NOUVEAU
4. Contact
5. Pain Relief & Recovery
6. Posture & Support
7. Therapy & Wellness
8. Blog

---

## POURQUOI "BUNDLES" APRÈS "CATALOG"?

- **Catalog** = Tous les produits individuels
- **Bundles** = Packages de produits (35% OFF)
- Logique de navigation: voir tous les produits → voir les bundles
- Promotion: Bundles offrent meilleure valeur (35% discount)

---

## ALTERNATIVE: MEGA MENU (Optionnel)

Si vous voulez un sous-menu sous "Bundles":

**Bundles** (parent)
  - Complete Care Bundles → /pages/bundles
  - Build Your Bundle → /pages/bundle-creator

---

## VÉRIFICATION

Après sauvegarde:
1. Visiter https://www.alphamedical.shop
2. Vérifier que "Bundles" apparaît dans le menu
3. Cliquer sur "Bundles" → doit rediriger vers /pages/bundles
4. Vérifier que la page affiche les 15 bundles avec filtres

---

**NOTE**: Les CTAs homepage seront ajoutés automatiquement par script (voir ci-dessous)
