import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

def compute_vector_scores(question_embedding, chunk_embeddings):
    scores = []
    for chunk_embedding in chunk_embeddings:
        score = cosine_similarity(
            question_embedding,
            chunk_embedding
        )
        scores.append(score)
    return scores