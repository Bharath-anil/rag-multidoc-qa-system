# Production-Style Multi-User RAG AI Assistant  
(FastAPI + React + Qdrant + PostgreSQL)

---

## Overview

Large Language Models often hallucinate when answering questions without grounded context. This project solves that problem by implementing a production-style Retrieval-Augmented Generation (RAG) AI assistant that retrieves relevant document chunks and generates grounded answers using semantic search and LLM generation.

This system supports:

- Multi-user document isolation
- Persistent vector storage
- Semantic retrieval
- Hybrid reranking
- JWT authentication
- Fullstack frontend integration
- Interactive AI question-answer workflow

Pipeline:

Authentication → Upload → Process → Embed → Store → Retrieve → Rerank → Generate → Render

The project is designed with a production mindset, focusing on modular architecture, scalability, retrieval quality, persistence, and real-world AI application flow.

---

# Architecture

```text
User Authentication
→ JWT Token Generation
→ Protected Frontend Routes
→ PDF Upload
→ Text Extraction
→ Chunking
→ Embedding Generation
→ Qdrant Vector Storage
→ Query Expansion
→ Semantic Retrieval
→ Hybrid Reranking
→ MMR Selection
→ Context Compression
→ LLM Answer Generation
→ React Answer Rendering
```

---

# Tech Stack

## Backend

- FastAPI
- SQLAlchemy
- Alembic
- JWT Authentication

---

## Frontend

- React
- TypeScript
- React Router
- Axios
- Vite

---

## Database

- PostgreSQL

---

## Vector Database

- Qdrant Cloud

---

## Embeddings

- sentence-transformers (`all-MiniLM-L6-v2`)

---

## LLM

- OpenRouter API
- `openai/gpt-oss-120b:free`

---

## Supporting Libraries

- pdfplumber
- numpy
- scikit-learn
- transformers

---

# Features

## Retrieval Features

- Multi-query retrieval
- Query expansion
- Semantic vector search
- Hybrid reranking
- MMR diversity selection
- Deduplication
- Context compression
- Fallback answer handling

---

## Backend Features

- JWT authentication
- Multi-user document isolation
- Persistent cloud vector storage
- Soft delete document lifecycle
- Metadata-based retrieval filtering
- Batch embedding ingestion
- Modular service architecture
- Dockerized backend setup
- Structured logging support

---

## Frontend Features

- User registration
- User login
- JWT token persistence
- Protected frontend routes
- PDF upload interface
- AI question-answer interface
- Loading state handling
- API integration with FastAPI backend
- Dashboard-based workflow

---

# System Pipeline

## 1. Authentication Flow

- User registration
- Password hashing
- JWT token generation
- Protected route validation
- Persistent login state

---

## 2. Ingestion Pipeline

- Upload PDF
- Extract text
- Clean data
- Chunk into overlapping segments
- Generate embeddings
- Store vectors in Qdrant
- Store metadata in PostgreSQL

---

## 3. Query Pipeline

- Expand user query
- Generate embeddings
- Retrieve chunks from Qdrant
- Filter by active user documents
- Merge and deduplicate results
- Rerank using hybrid scoring
- Select top chunks using MMR
- Compress context
- Generate answer using LLM
- Apply fallback handling

---

# Current Capabilities

- Fullstack AI assistant workflow
- Persistent vector retrieval
- User-specific document querying
- Metadata filtering
- Semantic retrieval
- Multi-document support
- Cloud-hosted vector database
- Protected dashboard access
- Interactive upload and ask flow
- Modular backend architecture
- Migration-based database management
- Dockerized backend deployment

---

# How to Run

## 1. Clone Repository

```bash
git clone <repo_url>
cd ai_knowledge_assistant
```

---

## 2. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_postgres_url

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION=rag_documents

OPENROUTER_API_KEY=your_openrouter_api_key

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 4. Run Database Migrations

```bash
alembic upgrade head
```

---

## 5. Start Backend

```bash
uvicorn app.main:app --reload
```

---

## 6. Start Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# API Endpoints

## Health Check

```http
GET /health
```

---

## Register User

```http
POST /register
```

---

## Login User

```http
POST /login
```

---

## Upload Document

```http
POST /upload
```

---

## Ask Question

```http
POST /ask
```

### Request Body

```json
{
  "question": "What is Redis used for?"
}
```

---

## Get User Documents

```http
GET /documents
```

---

## Soft Delete Document

```http
POST /documents/delete
```

---

# Example Workflow

## 1. Register User

Create account using frontend UI.

---

## 2. Login

Receive JWT token and access dashboard.

---

## 3. Upload PDF

PDF gets:
- extracted
- chunked
- embedded
- stored in Qdrant

---

## 4. Ask Question

System retrieves relevant chunks and generates grounded answer.

---

# Example

## Input

```text
What is Redis used for?
```

---

## Output

```text
Redis is an in-memory data store commonly used as a distributed cache.
```

---

# Project Structure

```text
app/
├── core/
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   └── logger.py
│
├── models/
│   ├── user.py
│   └── document.py
│
├── routers/
│   ├── auth.py
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


frontend/
├── src/
│   ├── pages/
│   ├── components/
│   ├── services/
│   ├── App.tsx
│   └── main.tsx
│
├── package.json
└── vite.config.ts
```

---

# Deployment

## Backend

- Dockerized FastAPI application
- PostgreSQL integration
- Qdrant Cloud vector database

---

## Frontend

- React + Vite frontend
- API-driven architecture
- Environment-based API configuration

---

# Security Considerations

## Current Security

- JWT-based authentication
- Password hashing
- User-level document isolation
- Protected frontend routes

---

## Planned Security Improvements

- OAuth2 login providers
- Refresh token rotation
- HTTPS enforcement
- Rate limiting
- File validation
- Secure cookie authentication
- Role-based access control
- Secure document storage

---

# Future Improvements

## Retrieval Improvements

- Hybrid BM25 + vector retrieval
- Parent-child retrieval
- Semantic chunking
- Contextual compression
- Metadata-aware ranking

---

## Infrastructure Improvements

- Background ingestion workers
- Async processing pipeline
- Redis caching
- Streaming responses
- Structured monitoring
- Transaction management
- Query optimization
- Eager loading strategies

---

## Product Improvements

- Chat-style interface
- Real-time ingestion updates
- Document management UI
- Multi-format document ingestion
- Workspace/folder support
- Chat memory
- Markdown rendering
- Streaming AI responses

---

# Key Learnings

- Retrieval quality impacts answer quality more than model size
- Chunking strategy directly affects retrieval precision
- Multi-query retrieval improves recall significantly
- Reranking is critical for precision
- Context compression improves LLM output quality
- Vector databases require metadata indexing strategies
- Persistence architecture matters for scalability
- Multi-user isolation changes retrieval design completely
- Fullstack AI systems require both retrieval quality and UX flow
- Production AI systems require security, persistence, and observability