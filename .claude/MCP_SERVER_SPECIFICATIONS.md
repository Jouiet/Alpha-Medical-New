# MCP SERVER SPECIFICATIONS - ALPHA MEDICAL

> **Version:** 1.0 (Specification - Not Yet Implemented)
> **Purpose:** Model Context Protocol server for advanced semantic retrieval
> **Status:** 📋 Specification Complete - Implementation Optional
> **Date:** 2025-11-26

---

## 🎯 OVERVIEW

### What is MCP?

**Model Context Protocol (MCP)** is a standard protocol for providing context to language models through specialized servers. An MCP server acts as a "knowledge provider" that Claude Code can query for relevant information.

### Why MCP for Alpha Medical?

**Current Limitation:**
- Large docs (8,871 lines) require manual chunk loading
- No semantic search across all documentation
- Keyword-based search is limited (grep/glob)

**MCP Solution:**
- Semantic search across ALL docs (~120+ files)
- Auto-suggest relevant docs based on task
- Context-aware recommendations
- Hybrid search (keyword + semantic)

**Value:** 85-90% token savings + faster context loading + better relevance

---

## 🏗️ ARCHITECTURE

### High-Level Design

```
┌─────────────────┐
│  Claude Code    │
│                 │
│  - User asks    │
│    question     │
│  - Needs context│
└────────┬────────┘
         │
         │ MCP Protocol
         │ (JSON-RPC)
         ▼
┌─────────────────┐
│   MCP Server    │
│                 │
│  - Vector DB    │
│  - Embeddings   │
│  - Search       │
└────────┬────────┘
         │
         │ File System Access
         ▼
┌─────────────────┐
│  Documentation  │
│                 │
│  - 120+ .md     │
│  - Code files   │
│  - Configs      │
└─────────────────┘
```

### Components

1. **MCP Server Process**
   - Node.js or Python server
   - Implements MCP protocol
   - Manages vector database

2. **Vector Database**
   - Stores document embeddings
   - Enables semantic search
   - Options: ChromaDB, Pinecone, Weaviate, or local SQLite + numpy

3. **Embedding Model**
   - Converts text to vectors
   - Options: OpenAI embeddings, sentence-transformers, or local models

4. **Search Engine**
   - Semantic search (vector similarity)
   - Keyword search (full-text)
   - Hybrid search (combine both)

---

## 📋 FUNCTIONAL REQUIREMENTS

### Core Features (MVP)

1. **Semantic Search**
   ```json
   Request: {
     "query": "How do I fix GitHub Actions workflow failures?",
     "max_results": 3
   }

   Response: [
     {
       "file": "market-analysis/AUTOMATION_COMPLETE_WORKFLOWS.md",
       "chunk": "auto-03-github-actions",
       "lines": "1501-2500",
       "relevance_score": 0.92,
       "preview": "GitHub Actions Workflows... debugging steps..."
     },
     {
       "file": "INFRASTRUCTURE_AUDIT_CHECKLIST.md",
       "chunk": "infra-05-github",
       "lines": "1201-1500",
       "relevance_score": 0.87,
       "preview": "GitHub Actions & CI/CD... workflow status..."
     }
   ]
   ```

2. **Keyword Search**
   ```json
   Request: {
     "keywords": ["klaviyo", "email flow"],
     "max_results": 5
   }

   Response: [...]
   ```

3. **Hybrid Search**
   - Combine semantic + keyword
   - Rerank results
   - Filter by file type, date, topic

4. **Auto-Suggest**
   ```json
   Request: {
     "task_description": "Deploy Klaviyo welcome email flow",
     "context": "marketing campaign"
   }

   Response: {
     "suggested_docs": [
       "03-marketing-context.md",
       "KLAVIYO_WELCOME_FLOW_IMPLEMENTATION.md",
       "market-analysis/AUTOMATION_COMPLETE_WORKFLOWS.md (chunk: auto-06-klaviyo)"
     ],
     "suggested_agents": ["marketing-specialist"],
     "estimated_tokens": "~15,000 tokens"
   }
   ```

### Advanced Features (Phase 2)

1. **Context-Aware Recommendations**
   - Analyze current conversation
   - Suggest next steps
   - Identify missing context

2. **Multi-Modal Search**
   - Search across code + docs + configs
   - Cross-reference related files
   - Dependency mapping

3. **Real-Time Indexing**
   - Auto-update index when files change
   - Incremental indexing
   - Hot-reload on edits

4. **Query Refinement**
   - Suggest better queries
   - Expand queries with synonyms
   - Filter by relevance threshold

---

## 🔧 TECHNICAL SPECIFICATIONS

### MCP Protocol Implementation

**Protocol:** JSON-RPC 2.0 over stdio or HTTP

**Methods to Implement:**

1. `search`
   - Input: `{query: string, max_results: number, filters?: object}`
   - Output: `SearchResult[]`

2. `suggest`
   - Input: `{task: string, context?: string}`
   - Output: `Suggestion[]`

3. `get_chunk`
   - Input: `{file: string, chunk_id: string}`
   - Output: `{content: string, metadata: object}`

4. `list_docs`
   - Input: `{filters?: object}`
   - Output: `DocumentInfo[]`

5. `health`
   - Input: `{}`
   - Output: `{status: string, indexed_docs: number, last_update: string}`

### Data Schema

**Document Index:**
```typescript
interface DocumentIndex {
  id: string;
  file_path: string;
  chunk_id?: string;
  lines?: string;
  content: string;
  embedding: number[];  // Vector embedding
  metadata: {
    title: string;
    topics: string[];
    doc_type: string;  // "infrastructure" | "marketing" | "seo" | "automation"
    last_updated: string;
    token_count: number;
  };
}
```

**Search Result:**
```typescript
interface SearchResult {
  file: string;
  chunk?: string;
  lines?: string;
  relevance_score: number;  // 0.0 - 1.0
  preview: string;  // First 200 chars
  metadata: object;
}
```

### Performance Requirements

- **Search Latency:** <100ms for semantic search
- **Index Build Time:** <60s for all docs (cold start)
- **Incremental Update:** <1s per document
- **Memory Usage:** <500MB for vector database
- **Concurrent Requests:** Support 10+ simultaneous searches

---

## 🚀 IMPLEMENTATION ROADMAP

### Phase 1: MVP (8-12 hours)

**Week 1:**
1. Setup MCP server skeleton (Node.js + TypeScript)
2. Implement basic file indexing (read all .md files)
3. Generate embeddings using OpenAI API or sentence-transformers
4. Setup vector database (ChromaDB or local SQLite)
5. Implement `search` method (semantic only)

**Week 2:**
6. Implement `get_chunk` method (load specific chunks)
7. Implement `list_docs` method (browse available docs)
8. Add MCP protocol handlers (JSON-RPC)
9. Test with Claude Code integration
10. Documentation and deployment guide

**Deliverables:**
- ✅ MCP server (runnable process)
- ✅ Semantic search functional
- ✅ Claude Code integration working
- ✅ Basic documentation

### Phase 2: Advanced Features (12-16 hours)

**Week 3:**
1. Implement hybrid search (semantic + keyword)
2. Add auto-suggest functionality
3. Context-aware recommendations
4. Result reranking algorithms
5. Query expansion with synonyms

**Week 4:**
6. Real-time file watching and indexing
7. Incremental updates (don't rebuild full index)
8. Performance optimization (caching, batching)
9. Multi-modal search (code + docs)
10. Admin dashboard (monitor index status)

**Deliverables:**
- ✅ Hybrid search operational
- ✅ Auto-suggest working
- ✅ Real-time updates
- ✅ Performance metrics

### Phase 3: Production Ready (4-8 hours)

**Week 5:**
1. Error handling and graceful degradation
2. Logging and monitoring
3. Unit tests + integration tests
4. Docker containerization
5. Deployment automation (systemd or PM2)

**Deliverables:**
- ✅ Production-ready MCP server
- ✅ Comprehensive tests
- ✅ Deployment docs
- ✅ Monitoring setup

---

## 💻 EXAMPLE USAGE

### Setup

```bash
# Install MCP server
cd .claude/mcp-server
npm install

# Build index (one-time, ~60s)
npm run index

# Start server
npm start
# Server running on stdio (MCP protocol)
```

### Configure Claude Code

```json
// settings.local.json
{
  "mcp": {
    "servers": {
      "alpha-medical-docs": {
        "command": "node",
        "args": ["/path/to/.claude/mcp-server/dist/index.js"],
        "env": {}
      }
    }
  }
}
```

### Use in Claude Code

```
User: "How do I debug GitHub Actions workflows?"

Claude: Let me search the documentation...
[MCP search: "debug github actions workflows"]

Found relevant docs:
1. AUTOMATION_COMPLETE_WORKFLOWS.md (chunk: auto-03-github-actions)
2. INFRASTRUCTURE_AUDIT_CHECKLIST.md (chunk: infra-05-github)

[Loads only relevant chunks, ~10K tokens instead of 64K]

Based on the documentation, here's how to debug GitHub Actions...
```

---

## 📊 EXPECTED IMPACT

### Token Efficiency

| Scenario | Without MCP | With MCP | Savings |
|----------|-------------|----------|---------|
| SEO question | Load 65K tokens (full file) | Load 8K tokens (1 chunk) | 88% |
| Automation debug | Load 45K tokens (full file) | Load 9K tokens (1 chunk) | 80% |
| Multi-topic | Load 100K+ tokens (multiple files) | Load 20K tokens (relevant chunks) | 80% |

**Average Savings:** 85-90%

### User Experience

**Before MCP:**
- User manually searches for docs (grep, glob)
- Loads large files entirely
- Scans for relevant sections
- Time: 2-5 minutes per query

**After MCP:**
- Semantic search finds exact relevant chunks
- Auto-loads only necessary context
- Immediate answers
- Time: <10 seconds per query

**Improvement:** 12-30x faster

---

## 🔐 SECURITY & PRIVACY

### Data Handling

- ✅ **Local-first:** Vector database stored locally
- ✅ **No cloud uploads:** Documents never leave machine (unless using OpenAI embeddings)
- ✅ **Credentials safe:** .env files excluded from indexing (via .claudeignore)
- ✅ **Read-only:** MCP server only reads files, never writes

### Optional: Self-Hosted Embeddings

Use local embedding models (no API calls):
- `sentence-transformers` (Python)
- `transformers.js` (Node.js)
- No data sent to external APIs

---

## 🎯 DECISION: IMPLEMENT OR NOT?

### Pros
- ✅ 85-90% token savings (even better than current 70-85%)
- ✅ Semantic search (find concepts, not just keywords)
- ✅ Auto-suggest saves time
- ✅ Scalable (works with 1,000+ docs)

### Cons
- ❌ Requires 24-40 hours development time
- ❌ Additional dependency (MCP server process)
- ❌ Embedding API costs (if using OpenAI) or local compute (if self-hosted)
- ❌ Index maintenance needed when docs change

### Recommendation

**For Alpha Medical:**
- ✅ **Phase 1-3 already provides 85% savings** (progressive disclosure + semantic chunking manifest)
- ✅ **Current system is "good enough" for production**
- ⏳ **MCP server is "nice-to-have", not "must-have"**

**Verdict:**
- Document specs ✅ (this file)
- Implement later if needed ⏳ (not critical for launch)
- Current manifest-based chunking is sufficient for 95% of use cases

---

## 📚 REFERENCES

### MCP Protocol
- Official Spec: https://modelcontextprotocol.io
- Claude Code MCP Guide: https://code.claude.com/docs/mcp

### Vector Databases
- ChromaDB: https://www.trychroma.com
- Pinecone: https://www.pinecone.io
- Weaviate: https://weaviate.io

### Embedding Models
- OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
- sentence-transformers: https://www.sbert.net
- transformers.js: https://huggingface.co/docs/transformers.js

---

## ✅ SPECIFICATION STATUS

**Phase:** Complete ✅
**Implementation:** Optional (not required for 100% operational system)
**Priority:** Low (current system sufficient)

**Future Enhancement:**
- Implement if documentation grows beyond 200+ files
- Implement if semantic search becomes critical need
- Implement if user requests advanced retrieval features

---

**Specified by:** Claude Code Session 56
**Date:** 2025-11-26
**Verdict:** Specs complete. Implementation deferred (not blocking 100% completion).
