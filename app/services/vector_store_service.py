import faiss
import numpy as np

index = None
stored_chunks = []

def build_index(embeddings, chunks):
    global index, stored_chunks

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)

    embeddings_np = np.array(embeddings).astype("float32")

    index.add(embeddings_np)

    stored_chunks = chunks


def search(question_embedding, k=20):
    global index, stored_chunks

    query = np.array([question_embedding]).astype("float32")

    distances, indices = index.search(query, k)

    results = []
    for idx in indices[0]:
        results.append(stored_chunks[idx])

    return results