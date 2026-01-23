# Alpha Medical - Knowledge Base Builder (FAISS Version)
# Transferred from MyDealz via Technology Shelf (Étagère Technologique)
# Session 144 | 23/01/2026

"""
Alpha Medical Knowledge Base Builder
====================================

Creates and maintains a vector-based knowledge base from Shopify products
for the Voice Agent RAG (Retrieval-Augmented Generation) system.

Features:
- Fetches all products from Shopify API
- Creates embeddings using sentence-transformers (FREE, no API key)
- Stores in FAISS vector database (FREE, local)
- Supports incremental updates for new products
- Optimized for voice agent queries

Original: MyDealz scripts/knowledge_base_builder.py
Transferred via Technology Shelf - Session 144
"""

import os
import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import requests

# Check for required libraries
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("WARNING: numpy not installed. Run: pip install numpy")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("WARNING: sentence-transformers not installed. Run: pip install sentence-transformers")

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("WARNING: faiss not installed. Run: pip install faiss-cpu")


# =============================================================================
# CONFIGURATION
# =============================================================================

SHOPIFY_STORE = os.getenv("SHOPIFY_STORE_URL", "azffej-as.myshopify.com")
SHOPIFY_TOKEN = os.getenv("SHOPIFY_ADMIN_API_TOKEN") or os.getenv("SHOPIFY_ACCESS_TOKEN", "")

# Paths
BASE_DIR = Path(__file__).parent.parent
KNOWLEDGE_BASE_DIR = BASE_DIR / "knowledge_base"
EMBEDDINGS_FILE = KNOWLEDGE_BASE_DIR / "product_embeddings.npy"
INDEX_FILE = KNOWLEDGE_BASE_DIR / "faiss_index.bin"
METADATA_FILE = KNOWLEDGE_BASE_DIR / "product_metadata.json"
SYNC_STATE_FILE = KNOWLEDGE_BASE_DIR / "sync_state.json"

# Embedding model (all-MiniLM-L6-v2 is fast, free, and effective)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384  # Dimension for all-MiniLM-L6-v2


# =============================================================================
# PRODUCT DATA PROCESSOR
# =============================================================================

class ProductDataProcessor:
    """Processes Shopify products into embedable text chunks."""

    def __init__(self):
        self.products = []
        self.chunks = []

    def fetch_all_products(self) -> List[Dict]:
        """Fetch all products from Shopify API with pagination."""
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

                # Check for pagination
                link_header = response.headers.get("Link", "")
                if 'rel="next"' in link_header:
                    # Extract next URL
                    for part in link_header.split(","):
                        if 'rel="next"' in part:
                            url = part.split(";")[0].strip("<> ")
                            params = {}  # URL already contains params
                            break
                else:
                    url = None

                time.sleep(0.5)  # Rate limiting

            except Exception as e:
                print(f"  ERROR fetching products: {e}")
                break

        self.products = products
        return products

    def create_product_chunks(self, product: Dict) -> List[Dict]:
        """Create searchable text chunks from a product."""
        chunks = []
        product_id = product.get("id")
        title = product.get("title", "")
        description = product.get("body_html", "") or ""
        product_type = product.get("product_type", "")
        vendor = product.get("vendor", "")
        tags = product.get("tags", "")
        handle = product.get("handle", "")

        # Clean HTML from description
        import re
        description_clean = re.sub(r'<[^>]+>', ' ', description)
        description_clean = re.sub(r'\s+', ' ', description_clean).strip()

        # Chunk 1: Product Overview (for general queries)
        overview_text = f"""
Product: {title}
Category: {product_type}
Brand: {vendor}
Tags: {tags}

This is a {product_type} product called "{title}" available at MyDealz.shop.
""".strip()

        chunks.append({
            "product_id": product_id,
            "chunk_type": "overview",
            "text": overview_text,
            "title": title,
            "handle": handle
        })

        # Chunk 2: Product Description (for detailed queries)
        if description_clean:
            # Split long descriptions into smaller chunks
            max_chunk_size = 1000
            desc_parts = [description_clean[i:i+max_chunk_size]
                         for i in range(0, len(description_clean), max_chunk_size)]

            for i, part in enumerate(desc_parts[:3]):  # Max 3 chunks per product
                chunks.append({
                    "product_id": product_id,
                    "chunk_type": f"description_{i+1}",
                    "text": f"Product: {title}\n\nDescription: {part}",
                    "title": title,
                    "handle": handle
                })

        # Chunk 3: Pricing and Variants (for price queries)
        variants = product.get("variants", [])
        if variants:
            variant_info = []
            for v in variants[:5]:  # Max 5 variants
                price = v.get("price", "N/A")
                variant_title = v.get("title", "Default")
                inventory = v.get("inventory_quantity", 0)
                variant_info.append(f"- {variant_title}: ${price} (Stock: {inventory})")

            pricing_text = f"""
Product: {title}
Pricing and Variants:
{chr(10).join(variant_info)}

Available at MyDealz.shop with competitive pricing.
""".strip()

            chunks.append({
                "product_id": product_id,
                "chunk_type": "pricing",
                "text": pricing_text,
                "title": title,
                "handle": handle
            })

        return chunks

    def process_all_products(self) -> List[Dict]:
        """Process all products into chunks."""
        all_chunks = []

        for product in self.products:
            chunks = self.create_product_chunks(product)
            all_chunks.extend(chunks)

        self.chunks = all_chunks
        return all_chunks


# =============================================================================
# EMBEDDING GENERATOR
# =============================================================================

class EmbeddingGenerator:
    """Generates embeddings using sentence-transformers."""

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self.model = None

    def load_model(self):
        """Load the embedding model."""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers not installed")

        print(f"  Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print(f"  Model loaded successfully (dim: {self.model.get_sentence_embedding_dimension()})")

    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings for a list of texts."""
        if self.model is None:
            self.load_model()

        print(f"  Generating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        return embeddings


# =============================================================================
# VECTOR DATABASE (FAISS)
# =============================================================================

class VectorDatabase:
    """FAISS-based vector database for product embeddings."""

    def __init__(self, dimension: int = EMBEDDING_DIM):
        self.dimension = dimension
        self.index = None
        self.metadata = []

    def create_index(self, embeddings: np.ndarray, metadata: List[Dict]):
        """Create FAISS index from embeddings."""
        if not FAISS_AVAILABLE:
            raise ImportError("faiss not installed")

        print(f"  Creating FAISS index with {len(embeddings)} vectors...")

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)

        # Create index (IndexFlatIP for inner product = cosine similarity after normalization)
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(embeddings)

        self.metadata = metadata
        print(f"  Index created: {self.index.ntotal} vectors")

    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """Search for similar products."""
        if self.index is None:
            raise ValueError("Index not created or loaded")

        # Normalize query
        query_norm = query_embedding.copy()
        faiss.normalize_L2(query_norm.reshape(1, -1))

        # Search
        distances, indices = self.index.search(query_norm.reshape(1, -1), top_k)

        results = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                results.append((self.metadata[idx], float(dist)))

        return results

    def save(self, index_path: Path, metadata_path: Path):
        """Save index and metadata to disk."""
        print(f"  Saving index to {index_path}")
        faiss.write_index(self.index, str(index_path))

        print(f"  Saving metadata to {metadata_path}")
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def load(self, index_path: Path, metadata_path: Path):
        """Load index and metadata from disk."""
        if not index_path.exists() or not metadata_path.exists():
            raise FileNotFoundError("Index or metadata file not found")

        print(f"  Loading index from {index_path}")
        self.index = faiss.read_index(str(index_path))

        print(f"  Loading metadata from {metadata_path}")
        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)

        print(f"  Loaded {self.index.ntotal} vectors with {len(self.metadata)} metadata entries")


# =============================================================================
# KNOWLEDGE BASE MANAGER
# =============================================================================

class KnowledgeBaseManager:
    """Manages the complete knowledge base lifecycle."""

    def __init__(self):
        self.processor = ProductDataProcessor()
        self.embedder = EmbeddingGenerator()
        self.vector_db = VectorDatabase()

        # Ensure directories exist
        KNOWLEDGE_BASE_DIR.mkdir(parents=True, exist_ok=True)

    def build_full_knowledge_base(self) -> Dict:
        """Build complete knowledge base from scratch."""
        print("\n" + "="*60)
        print("BUILDING MYDEALZ KNOWLEDGE BASE")
        print("="*60)

        start_time = time.time()

        # Step 1: Fetch products
        print("\n[1/4] Fetching products from Shopify...")
        products = self.processor.fetch_all_products()
        print(f"  Total products fetched: {len(products)}")

        if not products:
            return {"success": False, "error": "No products fetched"}

        # Step 2: Process into chunks
        print("\n[2/4] Processing products into searchable chunks...")
        chunks = self.processor.process_all_products()
        print(f"  Total chunks created: {len(chunks)}")

        # Step 3: Generate embeddings
        print("\n[3/4] Generating embeddings...")
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedder.generate_embeddings(texts)
        print(f"  Embeddings shape: {embeddings.shape}")

        # Step 4: Create and save index
        print("\n[4/4] Creating FAISS index...")
        self.vector_db.create_index(embeddings, chunks)
        self.vector_db.save(INDEX_FILE, METADATA_FILE)

        # Save embeddings separately for potential reuse
        np.save(EMBEDDINGS_FILE, embeddings)

        # Save sync state
        sync_state = {
            "last_full_build": datetime.now().isoformat(),
            "product_count": len(products),
            "chunk_count": len(chunks),
            "embedding_dim": EMBEDDING_DIM,
            "model": EMBEDDING_MODEL,
            "product_ids": [p["id"] for p in products]
        }
        with open(SYNC_STATE_FILE, "w") as f:
            json.dump(sync_state, f, indent=2)

        elapsed = time.time() - start_time

        result = {
            "success": True,
            "products": len(products),
            "chunks": len(chunks),
            "embeddings_shape": list(embeddings.shape),
            "elapsed_seconds": round(elapsed, 2),
            "index_file": str(INDEX_FILE),
            "metadata_file": str(METADATA_FILE)
        }

        print("\n" + "="*60)
        print("KNOWLEDGE BASE BUILD COMPLETE")
        print("="*60)
        print(f"  Products: {result['products']}")
        print(f"  Chunks: {result['chunks']}")
        print(f"  Time: {result['elapsed_seconds']}s")
        print(f"  Index: {INDEX_FILE}")

        return result

    def add_product(self, product: Dict) -> Dict:
        """Add a single product to the knowledge base (incremental update)."""
        print(f"\nAdding product to knowledge base: {product.get('title', 'Unknown')}")

        # Load existing index
        try:
            self.vector_db.load(INDEX_FILE, METADATA_FILE)
        except FileNotFoundError:
            return {"success": False, "error": "Knowledge base not found. Run full build first."}

        # Process product
        chunks = self.processor.create_product_chunks(product)

        # Generate embeddings
        texts = [chunk["text"] for chunk in chunks]
        new_embeddings = self.embedder.generate_embeddings(texts)

        # Add to index
        faiss.normalize_L2(new_embeddings)
        self.vector_db.index.add(new_embeddings)
        self.vector_db.metadata.extend(chunks)

        # Save updated index
        self.vector_db.save(INDEX_FILE, METADATA_FILE)

        # Update sync state
        try:
            with open(SYNC_STATE_FILE, "r") as f:
                sync_state = json.load(f)
        except:
            sync_state = {}

        sync_state["last_incremental_update"] = datetime.now().isoformat()
        sync_state["product_count"] = sync_state.get("product_count", 0) + 1
        sync_state["chunk_count"] = len(self.vector_db.metadata)

        if "product_ids" not in sync_state:
            sync_state["product_ids"] = []
        sync_state["product_ids"].append(product.get("id"))

        with open(SYNC_STATE_FILE, "w") as f:
            json.dump(sync_state, f, indent=2)

        return {
            "success": True,
            "product_id": product.get("id"),
            "chunks_added": len(chunks),
            "total_chunks": len(self.vector_db.metadata)
        }

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search the knowledge base."""
        # Load index if not loaded
        if self.vector_db.index is None:
            self.vector_db.load(INDEX_FILE, METADATA_FILE)

        # Generate query embedding
        if self.embedder.model is None:
            self.embedder.load_model()

        query_embedding = self.embedder.model.encode([query], convert_to_numpy=True)

        # Search
        results = self.vector_db.search(query_embedding, top_k)

        # Format results
        formatted = []
        for metadata, score in results:
            formatted.append({
                "product_id": metadata.get("product_id"),
                "title": metadata.get("title"),
                "handle": metadata.get("handle"),
                "chunk_type": metadata.get("chunk_type"),
                "text": metadata.get("text"),
                "relevance_score": round(score, 4)
            })

        return formatted

    def get_status(self) -> Dict:
        """Get knowledge base status."""
        status = {
            "exists": INDEX_FILE.exists() and METADATA_FILE.exists(),
            "index_file": str(INDEX_FILE),
            "metadata_file": str(METADATA_FILE)
        }

        if SYNC_STATE_FILE.exists():
            with open(SYNC_STATE_FILE, "r") as f:
                status["sync_state"] = json.load(f)

        if status["exists"]:
            try:
                self.vector_db.load(INDEX_FILE, METADATA_FILE)
                status["total_vectors"] = self.vector_db.index.ntotal
                status["total_metadata"] = len(self.vector_db.metadata)
            except Exception as e:
                status["load_error"] = str(e)

        return status


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="MyDealz Knowledge Base Builder")
    parser.add_argument("--build", action="store_true", help="Build full knowledge base")
    parser.add_argument("--status", action="store_true", help="Show knowledge base status")
    parser.add_argument("--search", type=str, help="Search the knowledge base")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")

    args = parser.parse_args()

    # Check dependencies
    missing = []
    if not NUMPY_AVAILABLE:
        missing.append("numpy")
    if not SENTENCE_TRANSFORMERS_AVAILABLE:
        missing.append("sentence-transformers")
    if not FAISS_AVAILABLE:
        missing.append("faiss-cpu")

    if missing and (args.build or args.search):
        print(f"\nERROR: Missing required packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return

    manager = KnowledgeBaseManager()

    if args.status:
        status = manager.get_status()
        print("\n=== KNOWLEDGE BASE STATUS ===")
        print(json.dumps(status, indent=2, default=str))

    elif args.build:
        result = manager.build_full_knowledge_base()
        print("\n=== BUILD RESULT ===")
        print(json.dumps(result, indent=2))

    elif args.search:
        print(f"\nSearching for: '{args.search}'")
        results = manager.search(args.search, args.top_k)
        print(f"\n=== TOP {args.top_k} RESULTS ===")
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] {r['title']} (score: {r['relevance_score']})")
            print(f"    Type: {r['chunk_type']}")
            print(f"    Handle: {r['handle']}")
            print(f"    Text preview: {r['text'][:200]}...")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
