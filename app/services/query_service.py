from . import (
    generation_service,
    rerank_service,
    query_expansion_service
)
from app.core.dependencies import embedding_service, vector_store
import re
from sqlalchemy.orm import Session
from app.models.document import Document


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

# filtering coding content 
def is_code_heavy(text):
    # Only flag actual code patterns
    code_patterns = re.compile(r'(def\s+\w+\s*\(|for\s+\w+\s+in\s+|while\s+\w+\s*[=:<]|import\s+\w+|==|!=|>=|<=)')
    lines = text.split("\n")
    code_lines = sum(1 for l in lines if code_patterns.search(l))
    return code_lines / max(len(lines), 1) > 0.5


def generate_ans(question: str,user_id:str,db: Session,document_ids = None):

    docs = db.query(Document).filter(Document.user_id == user_id,Document.is_active == True).all()
    allowed_docs = {str(d.id).strip().lower() for d in docs}

    if document_ids:
        requested = {
            str(doc_id).strip().lower()
            for doc_id in document_ids
        }

        allowed_docs = allowed_docs.intersection(requested)

    expansion_queries = query_expansion_service.expand_query(question)
    all_candidates = []

    for q in expansion_queries:
        emb = embedding_service.embed_query(q)
        results = vector_store.search(emb, k=60)

        for r in results:
            faiss_id = str(r["document_id"]).strip().lower()
            if faiss_id in allowed_docs:
                all_candidates.append(r)

        
    if not all_candidates:
        print("No candidates after filter. Allowed:", allowed_docs)
        return {"answer": "No relevant information found.", "chunks_used": []}
 
    # Dedup + filtering
    unique_chunks = {}

    for item in all_candidates:
        text = item["text"]

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

    is_definition = question.lower().startswith(("what is", "define", "what are"))
    boosted_chunks = []

    for c in candidate_chunks:
        text = c["text"].lower()

        if is_definition:
            if " is " in text or " refers to " in text:
                c["score"] = c.get("score", 0) + 1.2

        boosted_chunks.append(c)

    candidate_chunks = boosted_chunks
    # Rerank
    question_embedding = embedding_service.embed_query(question)

    reranked = rerank_service.rerank(
    question,
    candidate_chunks,
    question_embedding,
    embedding_service.get_model(),
    k=20
    )

    selected = rerank_service.mmr_select(
        reranked,
        question_embedding,
        top_k=5
    )

    top_chunks = [item["text"] for item in selected]

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

