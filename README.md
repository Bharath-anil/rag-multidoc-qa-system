# Production-Style RAG Backend (FastAPI + FAISS)

##  Overview

Large Language Models often hallucinate when answering questions without grounded context. This project solves that by implementing a **Retrieval-Augmented Generation (RAG)** backend that retrieves relevant document chunks and uses them to generate accurate answers.

This system ingests PDF documents and enables question answering using a structured pipeline:

**Upload → Process → Retrieve → Rerank → Generate**

It is designed with a **production mindset**, focusing on retrieval quality, modular architecture, and evaluation.

---

##  Architecture

```
User Query
→ Query Expansion (LLM + fallback rules)
→ Multi-query Embedding
→ FAISS Retrieval (top-k per query)
→ Merge Results
→ Deduplication
→ Document-level Filtering
→ Hybrid Reranking (Vector + Keyword)
→ Top Chunk Selection
→ Sentence-level Context Compression
→ LLM Answer Generation (FLAN-T5)
→ Fallback Mechanism
```

---

##  Tech Stack

### Backend

* FastAPI

### Embeddings

* sentence-transformers (`all-mpnet-base-v2`)

### Vector Database

* FAISS (`IndexFlatL2`)

### LLM

* transformers (`google/flan-t5-base`)

### Supporting Libraries

* pdfplumber (PDF extraction)
* numpy
* sklearn (TF-IDF for keyword scoring)

---

## Features

* Multi-query retrieval (improves recall)
* Query expansion using LLM + rule-based fallback
* Hybrid reranking (semantic similarity + keyword matching)
* Sentence-level context compression (reduces noise)
* Deduplication and document-level filtering
* FAISS-based fast vector search
* Multi-document support
* Persistent vector index
* Fallback mechanism for weak LLM responses
* Evaluation pipeline for measuring system performance

---

##  System Pipeline

### 1. Ingestion Pipeline

* Upload PDF
* Extract text
* Clean data
* Chunk into overlapping segments
* Generate embeddings
* Store in FAISS index

### 2. Query Pipeline

* Expand user query into multiple search queries
* Embed all queries
* Retrieve top-k chunks per query
* Merge and deduplicate results
* Filter by document
* Rerank using hybrid scoring
* Select top chunks
* Extract key sentences
* Generate answer using LLM
* Apply fallback if answer is weak

---

## Results

* Accuracy: ~60–75% (based on keyword overlap evaluation)
* Improved recall using multi-query retrieval
* Reduced noise using hybrid reranking and sentence filtering
* Better answer grounding due to context compression

### Observations

* Retrieval quality has the highest impact on answer quality
* Chunking strategy directly affects performance
* Query expansion improves recall significantly
* LLM performance is limited by model capability (FLAN-T5)

---

##  How to Run

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start Server

```bash
uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

### Health Check

```
GET /health
```

### Upload Document

```
POST /upload
```

### Ask Question

```
POST /ask
```

Request body:

```json
{
  "question": "What is Windows?",
  "document_id": "optional"
}
```

---

## Example

### Input

```
What is Microsoft Windows?
```

### Output

```
Windows is a graphical operating system developed by Microsoft.
```

---

## 📂 Project Structure

```
app/
├── routers/
│   └── upload.py
├── services/
│   ├── ingestion_service.py
│   ├── query_service.py
│   ├── vector_store_service.py
│   ├── embedding_service.py
│   ├── generation_service.py
│   ├── text_extractor.py
│   ├── text_cleaner.py
│   ├── chunk_service.py
│   ├── rerank_service.py
│   ├── similarity_service.py
│   ├── keyword_service.py
│   ├── query_expansion_service.py
├── storage/
│   └── storage.py
├── evaluate.py
├── test_cases.py
└── main.py
```

---

## 📈 Evaluation

Current evaluation is based on **keyword overlap scoring**:

* Compares generated answer with expected keywords
* Provides a basic accuracy metric

### Limitations

* Does not capture semantic similarity
* Cannot detect partial correctness

---

## 🔮 Future Improvements

* Semantic evaluation using embeddings
* Improved query expansion (NLP + synonyms)
* Adaptive reranking (dynamic weights)
* Semantic chunking instead of fixed sentence chunks
* Stronger LLM (e.g., Mistral, Llama)
* Caching layer for performance
* UI for interaction
* Per-document indexing for better filtering

---

## 🧠 Key Learnings

* Retrieval quality matters more than LLM capability
* Chunking strategy directly impacts performance
* Multi-query retrieval improves recall significantly
* Reranking is critical for precision
* Context compression improves LLM output quality
* Evaluation is essential for iterative improvemen
