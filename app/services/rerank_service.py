from . import similarity_service,keyword_service

def rerank(question,candidate_chunks,question_embedding,model,k=5):
    
    texts = [c["text"] for c in candidate_chunks]
    embeddings = [c["embedding"] for c in candidate_chunks]

    vector_scores = similarity_service.compute_vector_scores(
    question_embedding,
    embeddings
    )

    keyword_scores = keyword_service.compute_keyword_scores(
        question,
        texts
    )

    results = []
    
    for i in range(len(texts)):
        base_score = candidate_chunks[i].get("score", 0)
        score = (0.8 * vector_scores[i] + 0.2 * keyword_scores[i]) + base_score

        text = texts[i].lower()

        if any(word in text for word in ["click", "install", "press"]):
            score -= 0.2

        results.append({

            "text": texts[i],
            "embedding": embeddings[i],
            "score": float(score)
        })

    results.sort(reverse =True,key=lambda x:x["score"])
    return results[:k]


# for picking  best chunk 
def mmr_select(chunks, query_embedding, lambda_param=0.7, top_k=5):
    selected = []
    candidates = chunks.copy()

    while candidates and len(selected) < top_k:
        best = None
        best_score = -1

        for c in candidates:
            relevance = similarity_service.cosine_similarity(
                query_embedding,
                c["embedding"]
            )

            diversity = 0
            if selected:
                diversity = max(
                    similarity_service.cosine_similarity(
                        c["embedding"],
                        s["embedding"]
                    )
                    for s in selected
                )

            score = lambda_param * relevance - (1 - lambda_param) * diversity

            if score > best_score:
                best_score = score
                best = c

        selected.append(best)
        candidates.remove(best)

    return selected