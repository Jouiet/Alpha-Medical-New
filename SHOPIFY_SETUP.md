# Configuration Shopify pour Alpha Medical Care

Ce guide vous explique comment connecter votre store Shopify `azffej-as.myshopify.com` avec votre application Next.js.

## ✅ Configuration actuelle

- **Store Shopify**: `azffej-as.myshopify.com`
- **API Version**: 2025-10 (la plus récente)
- **Cart API**: Nouvelle API implémentée (remplace l'ancienne Checkout API)

## 🔑 Étape 1: Obtenir votre Storefront API Access Token

### Option A: Via le canal Headless (Recommandé)

1. Connectez-vous à votre admin Shopify: https://azffej-as.myshopify.com/admin

2. Allez dans **Sales channels** (Canaux de vente)

3. Recherchez et installez **Headless** depuis l'App Store Shopify si ce n'est pas déjà fait

4. Une fois installé, cliquez sur **Headless** dans votre liste de canaux

5. Cliquez sur **Create storefront** (Créer une vitrine)

6. Donnez un nom à votre storefront (ex: "Alpha Medical Website")

7. Copiez le **Storefront API access token** qui s'affiche

8. Collez-le dans votre fichier `.env.local`:
   ```
   NEXT_PUBLIC_SHOPIFY_STOREFRONT_ACCESS_TOKEN=votre_token_ici
   ```

### Option B: Via une Custom App

1. Allez dans **Settings** > **Apps and sales channels**

2. Cliquez sur **Develop apps**

3. Cliquez sur **Create an app**

4. Donnez un nom (ex: "Alpha Medical Storefront")

5. Dans l'onglet **Configuration**, activez les permissions suivantes pour **Storefront API**:
   - Read products, variants, and collections
   - Read customer tags
   - Read and modify checkouts
   - Read and modify carts

6. Cliquez sur **Install app**

7. Copiez le **Storefront API access token**

8. Collez-le dans `.env.local`

## 🛠️ Étape 2: Configurer vos produits dans Shopify

### Créer des produits dans Shopify Admin

1. Allez dans **Products** > **Add product**

2. Pour chaque produit médical que vous voulez vendre:
   - **Title**: Nom du produit (ex: "Medical Neck Traction Device")
   - **Description**: Description détaillée
   - **Price**: Prix en USD
   - **Images**: Ajoutez les images du produit
   - **Handle**: URL-friendly (ex: "medical-neck-traction-device")
   - **Availability**: Cochez "Available"

### Créer des collections

1. Allez dans **Products** > **Collections** > **Create collection**

2. Créez des collections pour organiser vos produits:
   - Pain Relief
   - Physical Therapy
   - Wellness Equipment
   - Recovery Tools
   - etc.

3. Ajoutez les produits aux collections appropriées

## 🔄 Étape 3: Tester l'intégration

### Test local

1. Redémarrez votre serveur de développement:
   ```bash
   npm run dev
   ```

2. Ouvrez http://localhost:3000

3. Testez les fonctionnalités suivantes:
   - Page produits: `/products`
   - Détails produit: `/products/[handle]`
   - Recherche de produits
   - Ajout au panier
   - Checkout Shopify

### Vérifier les erreurs

Si vous voyez des erreurs dans la console, vérifiez:
- Le token Storefront API est correct
- Le domaine du store est correct: `azffej-as.myshopify.com`
- Vos produits sont publiés et disponibles

## 📦 Fonctionnalités Shopify implémentées

### ✅ API Fonctions disponibles (lib/shopify.ts)

- `getProductsInCollection()` - Récupérer tous les produits
- `getProduct(handle)` - Récupérer un produit par son handle
- `getProductsByCollection(handle)` - Produits d'une collection
- `getAllCollections()` - Toutes les collections
- `searchProducts(query)` - Recherche de produits

### 🛒 Gestion du panier (Cart API 2025-10)

- `createCart()` - Créer un nouveau panier
- `addToCart(cartId, variantId, quantity)` - Ajouter au panier
- `updateCartLine(cartId, lineId, quantity)` - Modifier quantité
- `removeFromCart(cartId, lineId)` - Retirer du panier
- `getCart(cartId)` - Récupérer le panier

## 🚀 Prochaines étapes

### 1. Synchroniser les produits existants

Vous avez déjà 20 produits dans votre site. Vous devez maintenant:

1. Créer ces mêmes produits dans Shopify Admin
2. Utiliser les mêmes handles (slugs) pour garder la cohérence
3. S'assurer que les images et prix correspondent

### 2. Mettre à jour le Context Cart

Le fichier `contexts/CartContext.tsx` utilise actuellement un système local. Il faudra:
- Migrer vers Shopify Cart API
- Stocker le `cartId` dans localStorage
- Utiliser `checkoutUrl` de Shopify pour le paiement

### 3. Connecter le checkout

Dans `/app/checkout/page.tsx`, remplacer Stripe par:
```typescript
const { checkoutUrl } = await getCart(cartId);
window.location.href = checkoutUrl; // Redirige vers Shopify Checkout
```

## 📚 Documentation Shopify

- [Storefront API Reference](https://shopify.dev/docs/api/storefront)
- [Cart API Guide](https://shopify.dev/docs/api/storefront/latest/objects/Cart)
- [GraphQL Explorer](https://shopify.dev/docs/apps/tools/graphiql-admin-api)

## ⚠️ Important

- **Ne committez JAMAIS** votre Storefront API access token sur GitHub
- Le token dans `.env.local` est déjà dans `.gitignore`
- Pour la production, utilisez les variables d'environnement de Vercel

## 🆘 Besoin d'aide?

Si vous rencontrez des problèmes:
1. Vérifiez les logs de la console du navigateur
2. Vérifiez les logs du serveur Next.js
3. Testez vos requêtes dans GraphiQL: https://shopify.dev/docs/apps/tools/graphiql-admin-api
