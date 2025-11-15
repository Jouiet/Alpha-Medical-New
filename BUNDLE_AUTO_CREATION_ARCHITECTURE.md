# ARCHITECTURE - SYSTÈME AUTO-CRÉATION BUNDLES (METAFIELDS)

**Date**: 2025-11-15
**Système**: 10+ Propositions Identiques = Auto-Création Automatique
**Storage**: Shopify Metafields (simple, limité à 100 combinaisons)

---

## WORKFLOW COMPLET

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CLIENT SOUMET PROPOSITION                          │
│   (Sélectionne 3-4 produits via /pages/bundle-creator)              │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│              FRONTEND JAVASCRIPT (bundle-builder-combined.js)        │
│  1. Calcule HASH unique (product_ids triés: "123-456-789")         │
│  2. POST vers Backend API: {product_ids, email, hash}               │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND API (Python/Node.js)                      │
│  1. Reçoit proposition                                               │
│  2. Lit Metafield: page.metafields.bundle_proposals[hash]          │
│  3. Si n'existe pas: Créer {count:1, emails:[email]}               │
│  4. Si existe: Incrémenter count, ajouter email                     │
│  5. Sauvegarder Metafield                                           │
│  6. Si count >= 10: DÉCLENCHER AUTO-CRÉATION ───────┐              │
└──────────────────────────────────────────────────────┼──────────────┘
                                                       │
                                                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│              AUTO-CRÉATION BUNDLE (Backend API)                      │
│  1. Créer produit via Shopify Admin API                             │
│     - Titre: Auto-généré (ex: "Custom Bundle #abc123")              │
│     - Prix: sum(prices) × 0.65 (35% OFF)                            │
│     - Compare_at: sum(prices)                                        │
│     - Tags: bundle, auto-created, proposal-abc123                   │
│  2. Ajouter à collection: 296239169613                              │
│  3. Créer metafield sur bundle: {proposal_hash, customer_emails}   │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│           SHOPIFY FLOW - NOTIFICATIONS AUTOMATIQUES                  │
│  Trigger: Product created avec tag "auto-created"                   │
│  Action:  Envoyer email à tous les 10+ clients                      │
│           (lire emails depuis metafield du bundle)                   │
│  Template: Email prédéfini dans Flow                                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 1. STOCKAGE (METAFIELDS)

### Resource: Page `/pages/bundle-creator`

**Namespace**: `bundle_proposals`
**Key Format**: `hash_{md5}`
**Value Type**: JSON

**Exemple Metafield**:
```json
{
  "key": "hash_a1b2c3d4e5f6",
  "namespace": "bundle_proposals",
  "type": "json",
  "value": {
    "product_ids": [7623055966285, 7623055999053, 7623056031821],
    "product_handles": ["office-worker-essential-kit", "senior-mobility-support", "chronic-pain-starter-kit"],
    "count": 7,
    "emails": [
      "customer1@email.com",
      "customer2@email.com",
      "customer3@email.com",
      "customer4@email.com",
      "customer5@email.com",
      "customer6@email.com",
      "customer7@email.com"
    ],
    "created_at": "2025-11-15T02:30:00Z",
    "updated_at": "2025-11-15T03:45:00Z",
    "bundle_created": false,
    "bundle_id": null
  }
}
```

### HASH Fonction (JavaScript Frontend):

```javascript
function calculateProposalHash(productIds) {
  // Trier IDs par ordre croissant (déterministe)
  const sorted = productIds.slice().sort((a, b) => a - b);

  // Joindre avec "-"
  const string = sorted.join('-');

  // MD5 hash (ou SHA256)
  const hash = md5(string); // Utiliser lib crypto-js

  return `hash_${hash.substring(0, 12)}`;
}

// Exemple:
// productIds: [7623056031821, 7623055966285, 7623055999053]
// sorted: [7623055966285, 7623055999053, 7623056031821]
// string: "7623055966285-7623055999053-7623056031821"
// hash: "hash_a1b2c3d4e5f6"
```

---

## 2. BACKEND API

### OPTIONS D'IMPLÉMENTATION:

#### **Option A: Serverless (Vercel/Cloudflare) - RECOMMANDÉ**
- **Avantages**: Gratuit, simple, scalable, HTTPS automatique
- **Stack**: Python (Flask) ou Node.js (Express)
- **Déploiement**: `vercel deploy` ou `wrangler publish`
- **Endpoint**: `https://bundle-api.vercel.app/submit`

#### **Option B: Backend local + ngrok - DEV ONLY**
- **Avantages**: Développement rapide, pas de déploiement
- **Stack**: Python Flask local
- **Exposition**: `ngrok http 5000` → HTTPS URL temporaire
- **Endpoint**: `https://abc123.ngrok.io/submit`

#### **Option C: Shopify App Proxy - AVANCÉ**
- **Avantages**: Intégration native Shopify
- **Requis**: Créer Shopify App complète
- **Endpoint**: `https://alphamedical.shop/apps/bundle-proposals/submit`

**RECOMMANDATION**: **Option A (Vercel)** - Simple, gratuit, production-ready

---

## 3. CODE BACKEND (Python Flask - Vercel)

### `api/submit.py` (Vercel Serverless Function)

```python
from flask import Flask, request, jsonify
import requests
import hashlib
import json
from datetime import datetime

app = Flask(__name__)

# Shopify credentials (from environment variables)
SHOPIFY_DOMAIN = "azffej-as.myshopify.com"
SHOPIFY_TOKEN = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
API_VERSION = "2025-10"
GRAPHQL_URL = f"https://{SHOPIFY_DOMAIN}/admin/api/{API_VERSION}/graphql.json"

HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_TOKEN,
    "Content-Type": "application/json"
}

# Page ID for bundle-creator (get via Shopify API)
BUNDLE_CREATOR_PAGE_ID = "gid://shopify/Page/XXX" # TODO: Get actual ID

@app.route('/api/submit', methods=['POST'])
def submit_proposal():
    """
    Receives bundle proposal, aggregates in Metafields, auto-creates if 10+
    """
    data = request.json

    product_ids = data.get('product_ids', [])
    email = data.get('email', '')
    proposal_hash = data.get('hash', '')

    # Validate
    if not product_ids or not email or not proposal_hash:
        return jsonify({'error': 'Missing required fields'}), 400

    if len(product_ids) < 3 or len(product_ids) > 4:
        return jsonify({'error': 'Must select 3-4 products'}), 400

    # Read existing metafield
    metafield_key = proposal_hash
    metafield = read_metafield(BUNDLE_CREATOR_PAGE_ID, 'bundle_proposals', metafield_key)

    if metafield:
        # Update existing proposal
        value = json.loads(metafield['value'])

        # Check if email already submitted
        if email in value['emails']:
            return jsonify({'error': 'You already submitted this proposal'}), 400

        # Increment count
        value['count'] += 1
        value['emails'].append(email)
        value['updated_at'] = datetime.utcnow().isoformat()

        # Save updated metafield
        update_metafield(metafield['id'], value)

        # Check if threshold reached
        if value['count'] >= 10 and not value.get('bundle_created'):
            # AUTO-CREATE BUNDLE
            bundle_id = create_bundle_auto(product_ids, proposal_hash, value['emails'])

            # Update metafield
            value['bundle_created'] = True
            value['bundle_id'] = bundle_id
            update_metafield(metafield['id'], value)

            return jsonify({
                'success': True,
                'message': 'Bundle auto-created!',
                'count': value['count'],
                'bundle_created': True,
                'bundle_id': bundle_id
            })

        return jsonify({
            'success': True,
            'message': 'Proposal recorded',
            'count': value['count'],
            'remaining': 10 - value['count']
        })

    else:
        # Create new proposal
        value = {
            'product_ids': product_ids,
            'count': 1,
            'emails': [email],
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat(),
            'bundle_created': False,
            'bundle_id': None
        }

        # Create metafield
        create_metafield(BUNDLE_CREATOR_PAGE_ID, 'bundle_proposals', metafield_key, value)

        return jsonify({
            'success': True,
            'message': 'Proposal created',
            'count': 1,
            'remaining': 9
        })


def read_metafield(owner_id, namespace, key):
    """Read metafield via GraphQL"""
    query = """
    query($id: ID!, $namespace: String!, $key: String!) {
      page(id: $id) {
        metafield(namespace: $namespace, key: $key) {
          id
          value
        }
      }
    }
    """

    variables = {"id": owner_id, "namespace": namespace, "key": key}
    response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": query, "variables": variables})

    data = response.json()
    return data.get('data', {}).get('page', {}).get('metafield')


def create_metafield(owner_id, namespace, key, value):
    """Create metafield via GraphQL"""
    mutation = """
    mutation($input: MetafieldsSetInput!) {
      metafieldsSet(metafields: [$input]) {
        metafields {
          id
          key
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "ownerId": owner_id,
            "namespace": namespace,
            "key": key,
            "type": "json",
            "value": json.dumps(value)
        }
    }

    response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": mutation, "variables": variables})
    return response.json()


def update_metafield(metafield_id, value):
    """Update metafield via GraphQL"""
    mutation = """
    mutation($input: MetafieldsSetInput!) {
      metafieldsSet(metafields: [$input]) {
        metafields {
          id
        }
      }
    }
    """

    variables = {
        "input": {
            "id": metafield_id,
            "value": json.dumps(value)
        }
    }

    response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": mutation, "variables": variables})
    return response.json()


def create_bundle_auto(product_ids, proposal_hash, customer_emails):
    """
    Auto-create bundle product via Shopify Admin API
    Returns: bundle product ID
    """
    # Get product details
    products = fetch_products(product_ids)

    # Calculate pricing
    total_price = sum(p['price'] for p in products)
    bundle_price = round(total_price * 0.65, 2)  # 35% OFF

    # Generate title
    bundle_title = f"Custom Bundle #{proposal_hash[5:11].upper()}"

    # Create product
    mutation = """
    mutation($input: ProductInput!) {
      productCreate(input: $input) {
        product {
          id
          title
        }
      }
    }
    """

    variables = {
        "input": {
            "title": bundle_title,
            "vendor": "Alpha Medical",
            "productType": "Bundle",
            "tags": ["bundle", "auto-created", f"proposal-{proposal_hash}"],
            "variants": [{
                "price": str(bundle_price),
                "compareAtPrice": str(total_price),
                "inventoryPolicy": "CONTINUE",
                "inventoryManagement": "SHOPIFY"
            }],
            "metafields": [{
                "namespace": "auto_bundle",
                "key": "proposal_hash",
                "type": "single_line_text_field",
                "value": proposal_hash
            }, {
                "namespace": "auto_bundle",
                "key": "customer_emails",
                "type": "json",
                "value": json.dumps(customer_emails)
            }, {
                "namespace": "auto_bundle",
                "key": "product_ids",
                "type": "json",
                "value": json.dumps(product_ids)
            }]
        }
    }

    response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": mutation, "variables": variables})

    bundle_id = response.json()['data']['productCreate']['product']['id']

    # Add to collection
    add_to_collection(bundle_id, "gid://shopify/Collection/296239169613")

    return bundle_id


def fetch_products(product_ids):
    """Fetch product details for pricing"""
    # Implementation via GraphQL
    pass


def add_to_collection(product_id, collection_id):
    """Add product to collection via GraphQL"""
    # Implementation
    pass


if __name__ == '__main__':
    app.run(debug=True)
```

---

## 4. FRONTEND MODIFICATION (JavaScript)

### Modifier `assets/bundle-builder-combined.js`:

```javascript
// ADD: Hash calculation function
function calculateProposalHash(productIds) {
  const sorted = productIds.slice().sort((a, b) => a - b);
  const string = sorted.join('-');

  // Simple hash (ou utiliser crypto-js pour MD5)
  let hash = 0;
  for (let i = 0; i < string.length; i++) {
    const char = string.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }

  return `hash_${Math.abs(hash).toString(16).substring(0, 12)}`;
}

// MODIFY: Submission logic
async function submitProposal() {
  const productIds = selectedProducts.map(p => p.id);
  const email = document.getElementById('customer-email').value;
  const hash = calculateProposalHash(productIds);

  // POST vers backend API
  const response = await fetch('https://bundle-api.vercel.app/api/submit', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      product_ids: productIds,
      email: email,
      hash: hash
    })
  });

  const data = await response.json();

  if (data.bundle_created) {
    alert(`🎉 Bundle auto-created! You and ${data.count - 1} others will be notified.`);
  } else {
    alert(`✅ Proposal recorded! ${data.remaining} more needed (${data.count}/10)`);
  }
}
```

---

## 5. SHOPIFY FLOW CONFIGURATION

### Workflow dans Shopify Flow (Admin UI):

**Trigger**: Product created
**Condition**: Product tags contains "auto-created"

**Action 1**: Get product metafield
- Namespace: `auto_bundle`
- Key: `customer_emails`

**Action 2**: Send email (loop through emails)
- Template: "Your Custom Bundle is Ready!"
- Subject: "🎉 Your Proposed Bundle is Now Available - 35% OFF"
- Body:
```
Hi there,

Great news! Your custom bundle proposal has been created.

You and 9+ other customers requested this exact combination, so we've made it official!

🎁 Bundle: [Bundle Title]
💰 Price: $XXX (was $YYY) - 35% OFF saved
🔗 Shop Now: [Bundle URL]

Thank you for being part of our community-driven product creation!

Best,
Alpha Medical Team
```

---

## 6. LIMITATIONS & CONTRAINTES

### Metafields:
- **Max 100 metafields** par resource (page)
- = Max **100 combinaisons uniques** de propositions
- Si dépassé: ancien système (nécessite base de données externe)

### Backend:
- **Vercel Free Tier**: 100GB bandwidth/month (largement suffisant)
- **Latency**: ~200-500ms par requête (acceptable)

### Scalabilité:
- Si > 100 combinaisons: migrer vers database (Firebase, Supabase)
- Metafields suffisant pour MVP et premiers mois

---

## 7. DÉPLOIEMENT

### Étape 1: Deploy Backend (Vercel)

```bash
# Structure projet
bundle-api/
├── api/
│   └── submit.py
├── requirements.txt
└── vercel.json

# Deploy
cd bundle-api
vercel deploy --prod
```

### Étape 2: Modifier Frontend

```bash
# Update bundle-builder-combined.js
# Add hash calculation
# Change submission endpoint
```

### Étape 3: Upload Frontend vers Shopify

```bash
python3 deploy_bundle_builder_combined.py
```

### Étape 4: Configurer Shopify Flow

```
Admin → Settings → Apps → Shopify Flow
Create workflow (voir section 5)
```

---

## 8. TESTING

### Test 1: Première proposition
1. Sélectionner 3 produits via /pages/bundle-creator
2. Submit
3. Vérifier: Metafield créé avec count=1

### Test 2: Proposition identique
1. Différent email, même 3 produits
2. Submit
3. Vérifier: count=2

### Test 3: Auto-création (10+)
1. Soumettre 10 fois avec emails différents
2. Vérifier: Bundle auto-créé dans Shopify
3. Vérifier: Emails envoyés via Flow

---

## 9. MONITORING

### Dashboard:
- Page metafields: voir toutes les propositions en cours
- Shopify products: filtrer tag "auto-created"
- Email logs (Shopify Flow)

### Métriques:
- Nombre de propositions uniques
- Propositions les plus populaires (count proche de 10)
- Bundles auto-créés par mois

---

## STATUT: ARCHITECTURE DÉFINIE - PRÊT POUR IMPLÉMENTATION

**NEXT STEPS**:
1. Créer backend Vercel (Python Flask)
2. Modifier frontend JavaScript
3. Déployer backend + frontend
4. Configurer Shopify Flow
5. Tester workflow complet

**DURÉE ESTIMÉE**: 4-6 heures (dev + test + deploy)
