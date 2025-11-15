# Bundle Auto-Creation API - Backend

**Système automatisé d'agrégation et création de bundles**

10+ propositions identiques = Création automatique du bundle

---

## ARCHITECTURE

```
Client → Frontend JS → Vercel API → Shopify Metafields → Auto-création → Shopify Flow
```

---

## DEPLOYMENT (Vercel)

### Prérequis:
- Compte Vercel (gratuit): https://vercel.com
- Vercel CLI: `npm install -g vercel`

### Étapes:

1. **Login Vercel**:
```bash
vercel login
```

2. **Deploy**:
```bash
cd bundle-api
vercel deploy --prod
```

3. **Configure environment variables** (dans Vercel Dashboard):
- `SHOPIFY_DOMAIN`: `azffej-as.myshopify.com`
- `SHOPIFY_ADMIN_ACCESS_TOKEN`: [votre token]
- `BUNDLE_CREATOR_PAGE_GID`: `gid://shopify/Page/108071026765`

4. **Get API URL**:
Après deploy: `https://bundle-api-xxxxx.vercel.app`

---

## API ENDPOINTS

### POST /api/submit
Soumettre proposition de bundle

**Request**:
```json
{
  "product_ids": [7623055966285, 7623055999053, 7623056031821],
  "email": "customer@email.com",
  "hash": "hash_abc123def456"
}
```

**Response (< 10 proposals)**:
```json
{
  "success": true,
  "message": "Proposal recorded! 5 more needed.",
  "count": 5,
  "remaining": 5,
  "bundle_created": false
}
```

**Response (>= 10 proposals - AUTO-CRÉATION)**:
```json
{
  "success": true,
  "message": "Bundle auto-created! You and all proposers will be notified.",
  "count": 10,
  "bundle_created": true,
  "bundle_id": "7623087000000",
  "bundle_title": "Custom Bundle #ABC123",
  "bundle_url": "https://www.alphamedical.shop/products/custom-bundle-abc123"
}
```

### GET /api/health
Health check

**Response**:
```json
{
  "status": "ok",
  "service": "bundle-auto-creation-api",
  "version": "1.0.0"
}
```

---

## TESTING LOCAL

```bash
cd bundle-api

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SHOPIFY_DOMAIN=azffej-as.myshopify.com
export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx
export BUNDLE_CREATOR_PAGE_GID=gid://shopify/Page/108071026765

# Run
python api/submit.py

# Test
curl -X POST http://localhost:5000/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "product_ids": [7623055966285, 7623055999053, 7623056031821],
    "email": "test@example.com",
    "hash": "hash_test123"
  }'
```

---

## WORKFLOW

1. **Client soumet proposition** (3-4 produits)
   - Frontend calcule hash unique
   - POST vers /api/submit

2. **Backend agrège**
   - Lit/crée Metafield sur Page bundle-creator
   - Stocke: {count, emails[], product_ids[]}
   - Incrémente count

3. **Si count >= 10: AUTO-CRÉATION**
   - Créer produit bundle (Shopify Admin API)
   - Prix: 35% discount automatique
   - Tags: auto-created, proposal-{hash}
   - Ajouter à collection 296239169613
   - Metafields: proposal_hash, customer_emails

4. **Shopify Flow notifie clients**
   - Trigger: Product created avec tag "auto-created"
   - Action: Email tous les 10+ clients
   - Template prédéfini dans Flow

---

## MONITORING

### Vercel Dashboard:
- Logs en temps réel
- Analytics (requests, errors)
- Performance metrics

### Shopify:
- Metafields: voir toutes propositions en cours
- Products: filtrer tag "auto-created"
- Flow: logs notifications

---

## LIMITATIONS

- **Metafields**: Max 100 combinaisons uniques
- **Vercel Free**: 100GB bandwidth/month (largement suffisant)
- **API Rate Limits**: Shopify 2 req/s (géré automatiquement)

---

## TROUBLESHOOTING

### Erreur "Missing required fields"
- Vérifier format request JSON
- product_ids doit être array d'integers
- email doit être valide

### Erreur "Failed to create bundle"
- Vérifier SHOPIFY_ADMIN_ACCESS_TOKEN
- Vérifier permissions API (write_products, write_metafields)

### Bundle pas créé après 10+ proposals
- Check logs Vercel
- Vérifier threshold (défaut: 10)
- Check product_ids valides

---

## FILES

```
bundle-api/
├── api/
│   └── submit.py          # Main API endpoint
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
├── .env.example          # Environment template
├── README.md             # This file
└── BUNDLE_CREATOR_PAGE_GID.txt  # Page GID reference
```

---

**STATUS**: ✅ READY FOR DEPLOYMENT
