import faiss
import numpy as np
import pickle
import os


index = None
stored_chunks = []

INDEX_FILE = "faiss_index.bin"
CHUNK_FILE = "chunks.pkl"

def build_index(embeddings, chunks,document_id):
    global index, stored_chunks

    if index is None:
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        stored_chunks = []

    embeddings_np = np.array(embeddings).astype("float32")
    index.add(embeddings_np)
    
    new_chunks = [{"text": c, "document_id": document_id} for c in chunks]
    stored_chunks.extend(new_chunks)
    save_index()


def save_index():
    global index, stored_chunks

    faiss.write_index(index, INDEX_FILE)

    with open(CHUNK_FILE, "wb") as f:
        pickle.dump(stored_chunks, f)



def load_index():
    global index, stored_chunks

    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)

        with open(CHUNK_FILE, "rb") as f:
            stored_chunks = pickle.load(f)

        print("Vector store loaded")
        print("Total vectors:", index.ntotal)

    else:
        print("No existing index found")


def search(question_embedding, k=40):
    global index, stored_chunks

    if index is None:
        return []

    query = np.array([question_embedding]).astype("float32")

    distances, indices = index.search(query, k)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "text": stored_chunks[idx]["text"],
            "document_id": stored_chunks[idx]["document_id"],
            "embedding": index.reconstruct(int(idx)),
            "score": float(distances[0][i])
})
    return results