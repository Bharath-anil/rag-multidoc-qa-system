from  sentence_transformers import SentenceTransformer
from . import similarity_service,keyword_service

model = SentenceTransformer("all-mpnet-base-v2")


def embed_chunks(chunks):
    embeddings = model.encode(chunks)
    return embeddings

def retrieve_top_k(question, chunks, chunk_embeddings, k=3):
    question_embedding = model.encode([question])[0]

    vector_scores = similarity_service.compute_vector_scores(question_embedding,chunk_embeddings)
    keyword_scores = keyword_service.compute_keyword_scores(question, chunks)
    hybrid_results = []
    for i, chunk in enumerate(chunks):
        vector_score = vector_scores[i]
        keyword_score = keyword_scores[i]

        final_score = 0.7 * vector_score + 0.3 * keyword_score

        hybrid_results.append({
            "score": float(final_score),
            "vector_score": float(vector_score),
            "keyword_score": float(keyword_score),
            "chunk": chunk
        })

    hybrid_results.sort(reverse=True, key=lambda x: x["score"])
    return hybrid_results[:k]
