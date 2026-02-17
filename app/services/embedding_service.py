from  sentence_transformers import SentenceTransformer
from . import similarity_service

model = SentenceTransformer("all-mpnet-base-v2")


def embed_chunks(chunks):
    embeddings = model.encode(chunks)
    return embeddings

def retrieve_top_k(question, chunks, chunk_embeddings, k=3):
    question_embedding = model.encode([question])[0]

    scores = []
    for i, chunk_embedding in enumerate(chunk_embeddings):
        score = similarity_service.cosine_similarity(question_embedding, chunk_embedding)
        scores.append((score, chunks[i]))

    scores.sort(reverse=True, key=lambda x: x[0])
    return [
    {
        "score": float(score),
        "chunk": chunk
    }
    for score, chunk in scores[:k]
]