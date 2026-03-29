from .storage import document_store
from . import (
    embedding_service,
    generation_service,
    vector_store_service,
    rerank_service,
    query_expansion_service
)
import re


def extract_top_sentences(question, chunks, top_n=3):
    stopwords = {"what", "is", "the", "a", "an", "of"}
    question_words = set(
        w for w in question.lower().split() if w not in stopwords
    )

    scored = []

    for chunk in chunks:
        sentences = re.split(r'(?<=[.!?])\s+', chunk)

        for sent in sentences:
            if len(sent.strip()) < 20:
                continue

            words = set(sent.lower().split())
            score = len(question_words & words)

            scored.append((score, sent.strip()))

    scored.sort(reverse=True, key=lambda x: x[0])

    cleaned = []
    for _, s in scored[:top_n]:
        if not s.endswith('.'):
            s += '.'
        cleaned.append(s)

    return cleaned


def generate_ans(question: str, document_id: str =None):

    #Query Expansion
    expansion_queries = query_expansion_service.expand_query(question)

    all_candidates = []

    for q in expansion_queries:
        emb = embedding_service.embed_query(q)
        results = vector_store_service.search(emb, k=8)
        all_candidates.extend(results)

    #Dedup + basic filtering
    unique_chunks = {}

    for item in all_candidates:
        text = item["text"]

        if len(text) < 80:
            continue

        if "table of contents" in text.lower():
            continue

        key = text[:200]

        if key not in unique_chunks:
            unique_chunks[key] = item

    candidate_chunks = list(unique_chunks.values())

    #Safety check
    if not candidate_chunks:
        return {
            "chunks_used": [],
            "answer": "No relevant information found."
        }

    # doc_score = {}
    # for c in candidate_chunks:
    #     doc_score[c["document_id"]] += 1

    #Rerank
    question_embedding = embedding_service.embed_query(question)

    reranked = rerank_service.rerank(
        question,
        candidate_chunks,
        question_embedding,
        embedding_service.model,
        k=5
    )

    top_chunks = [item["chunk"] for item in reranked[:5]]

    #Sentence-level compression
    filtered_chunks = extract_top_sentences(question, top_chunks)

    if not filtered_chunks:
        filtered_chunks = top_chunks[:2]

    filtered_chunks = filtered_chunks[:3]

    #LLM generation
    answer = generation_service.generate_answer(
        question,
        filtered_chunks
    )

    #Fallback
    if not answer or len(answer.split()) < 5:
        answer = filtered_chunks[0]

    return {
        "chunks_used": top_chunks,
        "answer": answer
    }