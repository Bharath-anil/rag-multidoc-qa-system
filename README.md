# Production-Style Multi-User RAG Backend (FastAPI + Qdrant + PostgreSQL)

## Overview

Large Language Models often hallucinate when answering questions without grounded context. This project solves that by implementing a production-style Retrieval-Augmented Generation (RAG) backend that retrieves relevant document chunks and uses them to generate accurate answers.

This system supports:
- multi-user document isolation
- persistent vector storage
- semantic retrieval
- rerankinggit 
- document lifecycle management

Pipeline:

Upload → Process → Embed → Store → Retrieve → Rerank → Generate

It is designed with a production mindset, focusing on retrieval quality, modular architecture, persistence, and scalability.

---

## Architecture

User Query
→ Query Expansion
→ Multi-query Embedding
→ Qdrant Vector Retrieval
→ User-level Document Filtering
→ Merge Results
→ Deduplication
→ Hybrid Reranking
→ MMR Chunk Selection
→ Context Compression
→ LLM Answer Generation
→ Fallback Handling

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- Alembic

### Database

- PostgreSQL

### Vector Database

- Qdrant Cloud

### Embeddings

- sentence-transformers (all-MiniLM-L6-v2)

### LLM

- OpenRouter API
- openai/gpt-oss-120b:free

### Supporting Libraries

- pdfplumber
- numpy
- scikit-learn
- transformers

---

## Features

### Retrieval Features

- Multi-query retrieval
- Query expansion
- Semantic vector search
- Hybrid reranking
- MMR diversity selection
- Deduplication
- Context compression
- Fallback answer handling

### System Features

- Multi-user document isolation
- Persistent cloud vector storage
- Soft delete document lifecycle
- Metadata-based retrieval filtering
- Batch embedding ingestion
- Modular service architecture
- Production-style API design

---

## System Pipeline

### 1. Ingestion Pipeline

- Upload PDF
- Extract text
- Clean data
- Chunk into overlapping segments
- Generate embeddings
- Store vectors in Qdrant
- Store metadata in PostgreSQL

### 2. Query Pipeline

- Expand user query
- Generate embeddings
- Retrieve chunks from Qdrant
- Filter by active user documents
- Merge and deduplicate results
- Rerank using hybrid scoring
- Select top chunks using MMR
- Compress context
- Generate answer using LLM
- Apply fallback if answer is weak

---

## Current Capabilities

- Persistent vector retrieval
- User-specific document querying
- Metadata filtering
- Semantic retrieval
- Multi-document support
- Cloud-hosted vector database
- Modular backend architecture
- Migration-based database management

---

## How to Run

### 1. Install Dependencies

pip install -r requirements.txt

### 2. Configure Environment Variables

Create a .env file:

DATABASE_URL=your_postgres_url

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=rag_documents

OPENROUTER_API_KEY=your_openrouter_api_key

### 3. Run Migrations

alembic upgrade head

### 4. Start Server

uvicorn app.main:app --reload

---

## API Endpoints

### Health Check

GET /health

### Upload Document

POST /upload

### Ask Question

POST /ask

Request body:

{
  "question": "What is Redis used for?"
}

### Get User Documents

GET /documents

### Soft Delete Document

POST /documents/delete

---

## Example

### Input

What is Redis used for?

### Output

Redis is an in-memory data store commonly used as a distributed cache.

---

## Project Structure

app/
├── core/
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   └── dependencies.py
│
├── models/
│   ├── user.py
│   └── document.py
│
├── routers/
│   ├── upload.py
│   ├── query.py
│   └── documents.py
│
├── services/
│   ├── ingestion_service.py
│   ├── query_service.py
│   ├── qdrant_vector_store.py
│   ├── embedding_service.py
│   ├── generation_service.py
│   ├── rerank_service.py
│   ├── similarity_service.py
│   ├── keyword_service.py
│   ├── query_expansion_service.py
│   ├── chunk_service.py
│   ├── text_cleaner.py
│   └── text_extractor.py
│
├── alembic/
├── main.py
└── requirements.txt

---

## Future Improvements

### Retrieval

- Hybrid BM25 + vector search
- Parent-child retrieval
- Semantic chunking
- Contextual compression

### Infrastructure

- Background ingestion workers
- Async processing pipeline
- Docker deployment
- Redis caching
- Structured logging

### Product Features

- Workspace/folder support
- Per-document querying
- Streaming responses
- Chat memory
- Frontend UI

---

## Key Learnings

- Retrieval quality impacts answer quality more than model size
- Chunking strategy directly affects retrieval precision
- Multi-query retrieval improves recall significantly
- Reranking is critical for precision
- Context compression improves LLM output quality
- Vector databases require metadata indexing strategies
- Persistence architecture matters for scalability
- Multi-user isolation changes retrieval design completely
