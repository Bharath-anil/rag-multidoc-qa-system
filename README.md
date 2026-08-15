# DocuMind

> **Production-Ready Multi-User Retrieval-Augmented Generation (RAG) AI
> Assistant**

DocuMind is a full-stack Retrieval-Augmented Generation (RAG)
application that allows authenticated users to upload PDF documents,
index them into a vector database, and ask AI-powered questions grounded
in their own documents.

## Highlights

-   Multi-user JWT authentication
-   PDF ingestion pipeline
-   Semantic retrieval with Qdrant Cloud
-   Query expansion + hybrid reranking + MMR
-   OpenRouter LLM integration
-   Conversation history
-   Soft delete & recycle bin for documents and conversations
-   Health check endpoint
-   Request logging middleware
-   Dockerized backend
-   React + TypeScript frontend

------------------------------------------------------------------------

## Demo Workflow

PDF Upload
→ Text Extraction
→ Text Cleaning
→ Chunking
→ Embedding Generation
→ Qdrant Vector Storage
→ Semantic Retrieval
→ Hybrid Reranking
→ MMR Diversification
→ OpenRouter LLM
→ Grounded Response

# Architecture

``` text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 │
 ├── Authentication (JWT)
 ├── PDF Upload
 ├── Text Extraction
 ├── Text Cleaning
 ├── Chunking
 ├── Embedding Generation
 ├── Qdrant Storage
 │
 ▼
Question → Query Expansion → Semantic Retrieval
        → Hybrid Reranking → MMR → LLM → Response
```

# Project Structure

```text
DocuMind/
├── app/
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── services/
│
├── frontend/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── lib/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.tsx
│   │   └── main.tsx
│
├── alembic/
├── assets/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

# Tech Stack

## Backend

-   FastAPI
-   SQLAlchemy
-   Alembic
-   PostgreSQL
-   JWT

## Frontend

-   React
-   TypeScript
-   Vite
-   Tailwind CSS
-   shadcn/ui
-   Lucide Icons

## AI

-   sentence-transformers (all-MiniLM-L6-v2)
-   Qdrant Cloud
-   OpenRouter

# Key Engineering Concepts Demonstrated

- Retrieval-Augmented Generation (RAG)
- Vector Databases (Qdrant)
- Semantic Search
- Hybrid Retrieval
- Maximum Marginal Relevance (MMR)
- JWT Authentication & Authorization
- REST API Design
- Database Migrations with Alembic
- Multi-user Data Isolation
- Dockerized Backend
- React State Management
- Production-style Backend Architecture

# Features

  Feature                Status
  ---------------------- --------
  Authentication         ✅
  PDF Upload             ✅
  Semantic Search        ✅
  Hybrid Reranking       ✅
  Conversation History   ✅
  Soft Delete            ✅
  Recycle Bin            ✅
  Restore                ✅
  Health Check           ✅
  Logging Middleware     ✅

# Installation

``` bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

``` bash
cd frontend
npm install
npm run dev
```
# Environment Variables

``` env
DATABASE_URL=
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION=
OPENROUTER_API_KEY=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
# API

  Method   Endpoint
  -------- -------------------------
  POST     /register
  POST     /login
  POST     /upload
  POST     /ask
  GET      /documents
  GET      /documents/deleted
  POST     /documents/{id}/restore
  DELETE   /documents/{id}
  GET      /health

# Design Decisions

- Retrieval quality was prioritized over model size.
- User data is isolated through JWT-based authentication and metadata filtering.
- Qdrant Cloud was chosen for scalable vector storage.
- Modular service architecture improves maintainability and testing.
- Soft delete and recycle-bin workflows prevent accidental data loss.

## Screenshots
The following screenshots demonstrate the complete user workflow from authentication to document querying and conversation management.
### Login
![Login](assets/screenshots/01-login-page.png)

### Dashboard
![Dashboard](assets/screenshots/05-documents-uploaded.png)

### AI Chat
![Chat](assets/screenshots/07-chat-answer-sources.png)

### Recycle Bin
![Recycle Bin](assets/screenshots/08-recycle-bin.png)

### Mobile View
![Mobile View](assets/screenshots/09-mobile-view.png)

# Current Capabilities

- Multi-user document management
- PDF ingestion and processing pipeline
- Semantic document retrieval
- Query expansion and hybrid reranking
- AI-generated grounded answers
- Source-aware responses
- Conversation history management
- Soft delete and restore workflows
- Responsive desktop and mobile interface
- Dockerized backend deployment

# Future Improvements

## Authentication & Security

- Email verification during registration
- Forgot password / password reset via email
- OAuth 2.0 authentication (Google, GitHub)
- Refresh token implementation
- Secure HTTP-only cookie authentication
- HTTPS enforcement
- Rate limiting and request throttling
- Role-based access control (RBAC)
- Secure file validation and upload restrictions
- Audit logging for sensitive operations

---

## AI & Retrieval

- Hybrid BM25 + Vector Search
- Parent-Child Retrieval
- Semantic Chunking
- Contextual Compression
- Metadata-aware Ranking
- Cross-Encoder Reranking
- Streaming AI Responses
- Support for multiple LLM providers
- Conversation memory optimization
- Citation highlighting within answers

---

## Backend & Infrastructure

- Background workers using Celery/RQ
- Redis caching layer
- Asynchronous document ingestion
- Object storage integration (AWS S3 / MinIO)
- Container orchestration with Kubernetes
- CI/CD pipeline with GitHub Actions
- Prometheus & Grafana monitoring
- Distributed tracing with OpenTelemetry
- Database query optimization
- Automated backup and recovery strategy

---

## User Experience

- Fully responsive mobile interface
- Drag-and-drop document uploads
- Upload progress indicators
- Real-time document processing status
- Advanced document filtering and search
- Folder / Workspace organization
- Dark / Light theme support
- Document preview before querying
- Bulk upload support
- Keyboard shortcuts

---

## Document Management

- Support for DOCX, TXT, Markdown and HTML
- OCR support for scanned PDFs
- Version history for uploaded documents
- Permanent delete with retention policy
- Document tagging and categorization
- Batch document operations

---

## Testing & Quality

- Unit tests
- Integration tests
- End-to-end testing

# Engineering Goals

This project was built to simulate a production-ready Retrieval-Augmented Generation (RAG) system rather than a simple AI chatbot. The primary focus was on modular backend architecture, secure multi-user document isolation, scalable retrieval pipelines, maintainable code organization, and a modern full-stack user experience.

The roadmap above reflects production features that would typically be added as the application evolves toward enterprise readiness.