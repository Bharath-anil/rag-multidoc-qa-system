from . import similarity_service,keyword_service

def rerank(question,candidate_chunks,question_embedding,model,k=5):

    filtered_chunks = []
    texts = [c["text"] for c in candidate_chunks]
    embeddings = [c["embedding"] for c in candidate_chunks]

    filtered = []

    for i, text in enumerate(texts):
        if any(word in text.lower() for word in question.lower().split()):
            filtered.append((text, embeddings[i]))

    if filtered:
        texts = [f[0] for f in filtered]
        embeddings = [f[1] for f in filtered]

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
        score = 0.6 * vector_scores[i] + 0.4 * keyword_scores[i]

        results.append({
            "score": float(score),
            "chunk": texts[i]
        })

    results.sort(reverse =True,key=lambda x:x["score"])
    return results[:k]