# Comment Obtenir Votre Storefront API Token

## Méthode Officielle (Sans Shopify CLI)

### Étape 1: Accéder à votre Admin Shopify

1. Ouvrez https://azffej-as.myshopify.com/admin
2. Connectez-vous avec vos identifiants

### Étape 2: Installer le Canal Headless

1. Dans le menu de gauche, cliquez sur **Settings** (Paramètres)
2. Cliquez sur **Apps and sales channels** (Applications et canaux de vente)
3. Cliquez sur **Shopify App Store**
4. Recherchez "**Headless**"
5. Installez l'app officielle "**Headless**" de Shopify

### Étape 3: Créer un Storefront

1. Une fois installé, allez dans **Sales channels** → **Headless**
2. Cliquez sur **Create storefront**
3. Donnez un nom: "Alpha Medical Next.js"
4. Sélectionnez les permissions:
   - ✅ Read products
   - ✅ Read product listings
   - ✅ Read customer tags
   - ✅ Read and modify checkouts (pour Cart API)

### Étape 4: Copier le Token

1. Shopify affichera votre **Storefront API access token**
2. **COPIEZ-LE IMMÉDIATEMENT** (ne sera plus affiché)
3. Format: commence par `shpat_` ou similaire

### Étape 5: Configurer .env.local

Collez le token dans `/Users/mac/Desktop/Alpha-Medical/.env.local`:

```bash
NEXT_PUBLIC_SHOPIFY_STOREFRONT_ACCESS_TOKEN=shpat_votre_token_ici
```

### Étape 6: Redémarrer le Serveur

```bash
# Dans votre terminal Alpha-Medical
npm run dev
```

### Étape 7: Tester

Ouvrez http://localhost:3000/products

Si vous voyez vos produits Shopify, c'est bon! ✅

## ⚠️ Important

- **NE PARTAGEZ JAMAIS** ce token publiquement
- Il est déjà dans .gitignore (sécurisé)
- Pour production (Vercel), ajoutez-le dans Environment Variables

## Dépannage

### Si vous voyez "Missing credentials":
- Vérifiez que le token est bien dans .env.local
- Pas d'espaces avant/après le token
- Redémarrez le serveur dev

### Si aucun produit n'apparaît:
- Vérifiez que vos produits sont "Available" dans Shopify Admin
- Vérifiez qu'ils sont publiés sur le canal "Headless"

### Si erreur API:
- Vérifiez que le store domain est correct: `azffej-as.myshopify.com`
- Testez avec GraphiQL: https://shopify.dev/docs/apps/tools/graphiql-admin-api
