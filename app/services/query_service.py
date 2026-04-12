from . import (
    generation_service,
    rerank_service,
    query_expansion_service
)
from app.core.dependencies import embedding_service, vector_store
import re
from typing import Optional
from app.storage.user_store import get_user


def extract_top_sentences(question, chunks, top_n=3):
    stopwords = {"what", "is", "the", "a", "an", "of"}
    question_words = set(
        w for w in question.lower().split() if w not in stopwords
    )

    definition_keywords = {"is", "means", "defined", "refers"}

    scored = []

    for chunk in chunks:
        sentences = re.split(r'(?<=[.!?])\s+', chunk)

        for sent in sentences:
            s = sent.strip()
            if len(s) < 30:
                continue

            words = set(s.lower().split())

            # base score
            score = len(question_words & words)

            if any(word in words for word in definition_keywords):
                score += 2

            if score > 0:
                scored.append((score, s))

    scored.sort(reverse=True, key=lambda x: x[0])

    cleaned = []
    for _, s in scored[:top_n]:
        if not s.endswith('.'):
            s += '.'
        cleaned.append(s)

    return cleaned


def build_definition_answer(question, chunk):
    title = chunk.split("\n")[0]
    return f"{title.strip()} is related to {question.lower()}."


def is_code_heavy(text):
    # Only flag actual code patterns
    code_patterns = re.compile(r'(def\s+\w+\s*\(|for\s+\w+\s+in\s+|while\s+\w+\s*[=:<]|import\s+\w+|==|!=|>=|<=)')
    lines = text.split("\n")
    code_lines = sum(1 for l in lines if code_patterns.search(l))
    return code_lines / max(len(lines), 1) > 0.5

def generate_ans(question: str,username:str,document_ids: Optional[list[str]] = None):

    user = get_user(username)
    if not user:
        return {"answer": "User not found", "chunks_used": []}
    allowed_docs = set(user["documents"])

    if document_ids:
        requested = set(document_ids)

        # access control
        if not requested.issubset(allowed_docs):
            return {"answer": "Access denied", "chunks_used": []}

        allowed_docs = requested


    expansion_queries = query_expansion_service.expand_query(question)

    all_candidates = []

    for q in expansion_queries:
        emb = embedding_service.embed_query(q)
        results = vector_store.search(emb, k=5)
        filtered_results = [
            r for r in results
            if r["document_id"] in allowed_docs
        ]

        if document_ids and not filtered_results:
            filtered_results = results
        all_candidates.extend(filtered_results)

    # Dedup + filtering
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

    if not candidate_chunks:
        return {
            "chunks_used": [],
            "answer": "No relevant information found."
        }

    candidate_chunks = [c for c in candidate_chunks if not is_code_heavy(c["text"])]


    if not candidate_chunks:
        return {"chunks_used": [], "answer": "No relevant text found."}

    # Rerank
    question_embedding = embedding_service.embed_query(question)

    reranked = rerank_service.rerank(
        question,
        candidate_chunks,
        question_embedding,
        embedding_service.get_model(),
        k=5
    )

    top_chunks = [item["chunk"] for item in reranked[:5]]

    # Sentence extraction
    # filtered_chunks = extract_top_sentences(question, top_chunks)

    # if not filtered_chunks:
    #     return {
    #     "chunks_used": top_chunks,
    #     "answer": build_definition_answer(question, top_chunks[0])
    #     }

    # filtered_chunks = filtered_chunks[:2]
    context_chunks = top_chunks[:2] 
    answer = generation_service.generate_answer(
        question,
        context_chunks
    )

    # final fallback cleanup
    if not answer or len(answer.split()) < 5:
        answer = " ".join(context_chunks)

    return {
        "chunks_used": top_chunks,
        "answer": answer
    }