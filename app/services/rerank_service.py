from . import similarity_service,keyword_service

def rerank(question,candidate_chunks,question_embedding,model,k=5):

    filtered_chunks = []
    for chunk in candidate_chunks:
        if any(word in chunk.lower() for word in question.lower().split()):
            filtered_chunks.append(chunk)

    if len(filtered_chunks) > 0:
        candidate_chunks = filtered_chunks

    chunk_embeddings = model.encode(candidate_chunks)

    vector_scores = similarity_service.compute_vector_scores(
        question_embedding,
        chunk_embeddings
    )

    keyword_scores = keyword_service.compute_keyword_scores(
        question,
        candidate_chunks
    )

    results = []
    
    for i, chunk in enumerate(candidate_chunks):
        vector_score = vector_scores[i]
        keyword_score = keyword_scores[i]

        score = 0.6 * vector_score + 0.4 * keyword_score

        results.append({
            "score": float(score),
            "chunk": chunk
        })

        results.sort(reverse =True,key=lambda x:x["score"])
    return results[:k]