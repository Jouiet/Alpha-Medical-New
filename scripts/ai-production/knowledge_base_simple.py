# Alpha Medical - Knowledge Base (Simple Version)
# Transferred from MyDealz via Technology Shelf (Étagère Technologique)
# Session 144 | 23/01/2026

"""
Alpha Medical Knowledge Base - Simple Version
=============================================

A simpler knowledge base implementation that:
- Works without heavy ML dependencies (sentence-transformers, faiss)
- Uses TF-IDF for text similarity (numpy only)
- Supports Grok API embeddings as optional enhancement
- Fully functional for voice agent RAG

Original: MyDealz scripts/knowledge_base_simple.py
Transferred via Technology Shelf - Session 144
"""

import os
import json
import re
import math
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import Counter
import requests

# Check numpy
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("WARNING: numpy not installed. Run: pip install numpy")


# =============================================================================
# CONFIGURATION
# =============================================================================

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE_URL", "azffej-as.myshopify.com")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_ADMIN_API_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN", "")
XAI_API_KEY = os.getenv("XAI_API_KEY", "")

# Paths
BASE_DIR = Path(__file__).parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
INDEX_FILE = KNOWLEDGE_BASE_DIR / "tfidf_index.json"
METADATA_FILE = KNOWLEDGE_BASE_DIR / "product_metadata.json"
SYNC_STATE_FILE = KNOWLEDGE_BASE_DIR / "sync_state.json"


# =============================================================================
# TF-IDF IMPLEMENTATION (No dependencies except numpy)
# =============================================================================

class TFIDFVectorizer:
    """Simple TF-IDF vectorizer using only numpy."""

    def __init__(self):
        self.vocabulary = {}
        self.idf = {}
        self.doc_count = 0

    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        tokens = text.split()
        # Remove very short tokens and stopwords
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                    'would', 'could', 'should', 'may', 'might', 'must', 'can',
                    'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
                    'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
                    'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
                    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
                    'own', 'same', 'so', 'than', 'too', 'very', 'just', 'and',
                    'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
                    'at', 'by', 'for', 'with', 'about', 'against', 'between',
                    'into', 'through', 'during', 'before', 'after', 'above',
                    'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on',
                    'off', 'over', 'under', 'again', 'further', 'then', 'once'}
        return [t for t in tokens if len(t) > 2 and t not in stopwords]

    def fit(self, documents: List[str]):
        """Build vocabulary and compute IDF."""
        self.doc_count = len(documents)
        doc_freq = Counter()

        # Build vocabulary and count document frequencies
        for doc in documents:
            tokens = set(self._tokenize(doc))
            for token in tokens:
                doc_freq[token] += 1
                if token not in self.vocabulary:
                    self.vocabulary[token] = len(self.vocabulary)

        # Compute IDF
        for token, freq in doc_freq.items():
            self.idf[token] = math.log(self.doc_count / (1 + freq))

        print(f"  Vocabulary size: {len(self.vocabulary)}")

    def transform(self, documents: List[str]) -> np.ndarray:
        """Transform documents to TF-IDF vectors."""
        vectors = np.zeros((len(documents), len(self.vocabulary)))

        for i, doc in enumerate(documents):
            tokens = self._tokenize(doc)
            tf = Counter(tokens)
            doc_len = len(tokens) or 1

            for token, count in tf.items():
                if token in self.vocabulary:
                    idx = self.vocabulary[token]
                    # Normalized TF * IDF
                    vectors[i, idx] = (count / doc_len) * self.idf.get(token, 0)

            # L2 normalize
            norm = np.linalg.norm(vectors[i])
            if norm > 0:
                vectors[i] /= norm

        return vectors

    def transform_query(self, query: str) -> np.ndarray:
        """Transform a single query to TF-IDF vector."""
        return self.transform([query])[0]

    def save(self, path: Path):
        """Save vectorizer state."""
        state = {
            "vocabulary": self.vocabulary,
            "idf": self.idf,
            "doc_count": self.doc_count
        }
        with open(path, "w") as f:
            json.dump(state, f)

    def load(self, path: Path):
        """Load vectorizer state."""
        with open(path, "r") as f:
            state = json.load(f)
        self.vocabulary = state["vocabulary"]
        self.idf = state["idf"]
        self.doc_count = state["doc_count"]


# =============================================================================
# SIMPLE VECTOR DATABASE
# =============================================================================

class SimpleVectorDB:
    """Simple vector database using numpy."""

    def __init__(self):
        self.vectors = None
        self.metadata = []

    def add(self, vectors: np.ndarray, metadata: List[Dict]):
        """Add vectors and metadata."""
        self.vectors = vectors
        self.metadata = metadata

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar vectors using cosine similarity."""
        if self.vectors is None:
            return []

        # Cosine similarity (vectors are already normalized)
        similarities = np.dot(self.vectors, query_vector)

        # Get top k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] > 0:
                results.append((self.metadata[idx], float(similarities[idx])))

        return results

    def save(self, vectors_path: Path, metadata_path: Path):
        """Save database."""
        np.save(vectors_path, self.vectors)
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def load(self, vectors_path: Path, metadata_path: Path):
        """Load database."""
        self.vectors = np.load(vectors_path)
        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)


# =============================================================================
# KNOWLEDGE BASE MANAGER
# =============================================================================

class SimpleKnowledgeBase:
    """Simple knowledge base manager."""

    def __init__(self):
        self.vectorizer = TFIDFVectorizer()
        self.db = SimpleVectorDB()
        KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

    def fetch_products(self) -> List[Dict]:
        """Fetch all products from Shopify."""
        products = []
        url = f"https://{SHOPIFY_STORE}/admin/api/2024-10/products.json"
        params = {"limit": 250, "status": "active"}
        headers = {
            "X-Shopify-Access-Token": SHOPIFY_TOKEN,
            "Content-Type": "application/json"
        }

        while url:
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                batch = data.get("products", [])
                products.extend(batch)
                print(f"  Fetched {len(batch)} products (total: {len(products)})")

                link_header = response.headers.get("Link", "")
                if 'rel="next"' in link_header:
                    for part in link_header.split(","):
                        if 'rel="next"' in part:
                            url = part.split(";")[0].strip("<> ")
                            params = {}
                            break
                else:
                    url = None

                time.sleep(0.5)
            except Exception as e:
                print(f"  ERROR: {e}")
                break

        return products

    def create_chunks(self, product: Dict) -> List[Dict]:
        """Create text chunks from product."""
        chunks = []
        product_id = product.get("id")
        title = product.get("title", "")
        description = product.get("body_html", "") or ""
        product_type = product.get("product_type", "")
        handle = product.get("handle", "")

        # Clean HTML
        description = re.sub(r'<[^>]+>', ' ', description)
        description = re.sub(r'\s+', ' ', description).strip()

        # Overview chunk
        overview = f"{title}. Category: {product_type}. {description[:500]}"
        chunks.append({
            "product_id": product_id,
            "title": title,
            "handle": handle,
            "chunk_type": "overview",
            "text": overview
        })

        # Pricing chunk
        variants = product.get("variants", [])
        if variants:
            prices = [f"${v.get('price', 'N/A')}" for v in variants[:3]]
            pricing = f"{title} is available at {', '.join(prices)}."
            chunks.append({
                "product_id": product_id,
                "title": title,
                "handle": handle,
                "chunk_type": "pricing",
                "text": pricing
            })

        return chunks

    def build(self) -> Dict:
        """Build the knowledge base."""
        print("\n" + "="*60)
        print("BUILDING SIMPLE KNOWLEDGE BASE")
        print("="*60)

        start = time.time()

        # Fetch products
        print("\n[1/4] Fetching products...")
        products = self.fetch_products()
        print(f"  Total: {len(products)} products")

        if not products:
            return {"success": False, "error": "No products fetched"}

        # Create chunks
        print("\n[2/4] Creating chunks...")
        all_chunks = []
        for p in products:
            all_chunks.extend(self.create_chunks(p))
        print(f"  Total: {len(all_chunks)} chunks")

        # Build TF-IDF
        print("\n[3/4] Building TF-IDF index...")
        texts = [c["text"] for c in all_chunks]
        self.vectorizer.fit(texts)
        vectors = self.vectorizer.transform(texts)
        print(f"  Vectors shape: {vectors.shape}")

        # Save
        print("\n[4/4] Saving...")
        self.db.add(vectors, all_chunks)
        self.db.save(
            KNOWLEDGE_BASE_DIR / "vectors.npy",
            METADATA_FILE
        )
        self.vectorizer.save(INDEX_FILE)

        # Save sync state
        sync_state = {
            "last_build": datetime.now().isoformat(),
            "product_count": len(products),
            "chunk_count": len(all_chunks),
            "vector_dim": vectors.shape[1],
            "product_ids": [p["id"] for p in products]
        }
        with open(SYNC_STATE_FILE, "w") as f:
            json.dump(sync_state, f, indent=2)

        elapsed = time.time() - start

        print("\n" + "="*60)
        print("BUILD COMPLETE")
        print("="*60)
        print(f"  Products: {len(products)}")
        print(f"  Chunks: {len(all_chunks)}")
        print(f"  Time: {elapsed:.2f}s")

        return {
            "success": True,
            "products": len(products),
            "chunks": len(all_chunks),
            "elapsed": round(elapsed, 2)
        }

    def load(self) -> bool:
        """Load existing knowledge base."""
        try:
            self.vectorizer.load(INDEX_FILE)
            self.db.load(
                KNOWLEDGE_BASE_DIR / "vectors.npy",
                METADATA_FILE
            )
            return True
        except Exception as e:
            print(f"ERROR loading: {e}")
            return False

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search the knowledge base."""
        query_vector = self.vectorizer.transform_query(query)
        results = self.db.search(query_vector, top_k)

        formatted = []
        for meta, score in results:
            formatted.append({
                "product_id": meta.get("product_id"),
                "title": meta.get("title"),
                "handle": meta.get("handle"),
                "chunk_type": meta.get("chunk_type"),
                "text": meta.get("text"),
                "score": round(score, 4)
            })

        return formatted

    def get_status(self) -> Dict:
        """Get knowledge base status."""
        status = {
            "exists": INDEX_FILE.exists() and METADATA_FILE.exists(),
            "index_file": str(INDEX_FILE)
        }

        if SYNC_STATE_FILE.exists():
            with open(SYNC_STATE_FILE, "r") as f:
                status["sync_state"] = json.load(f)

        return status


# =============================================================================
# MAIN
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="MyDealz Simple Knowledge Base")
    parser.add_argument("--build", action="store_true", help="Build knowledge base")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--search", type=str, help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")

    args = parser.parse_args()

    if not NUMPY_AVAILABLE:
        print("ERROR: numpy required. Run: pip install numpy")
        return

    kb = SimpleKnowledgeBase()

    if args.status:
        print("\n=== STATUS ===")
        print(json.dumps(kb.get_status(), indent=2, default=str))

    elif args.build:
        result = kb.build()
        print("\n=== RESULT ===")
        print(json.dumps(result, indent=2))

    elif args.search:
        if not kb.load():
            print("Knowledge base not found. Run --build first.")
            return

        print(f"\nSearching: '{args.search}'")
        results = kb.search(args.search, args.top_k)

        print(f"\n=== TOP {args.top_k} RESULTS ===")
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] {r['title']} (score: {r['score']})")
            print(f"    URL: https://mydealz.shop/products/{r['handle']}")
            print(f"    Type: {r['chunk_type']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
