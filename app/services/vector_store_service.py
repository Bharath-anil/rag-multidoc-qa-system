import faiss
import numpy as np
import pickle
import os


class VectorStore:
    def __init__(self):
        self.index = None
        self.stored_chunks = []

    INDEX_FILE = "faiss_index.bin"
    CHUNK_FILE = "chunks.pkl"

    def build_index(self, embeddings, chunks, document_id):
        if self.index is None:
            dimension = len(embeddings[0])
            self.index = faiss.IndexFlatL2(dimension)
            self.stored_chunks = []

        embeddings_np = np.array(embeddings).astype("float32")
        self.index.add(embeddings_np)

        new_chunks = [
                {
                    "text": c,
                    "document_id": str(document_id)  # ✅ EDGE CASE 3: type consistency
                }
                for c in chunks
            ]
        self.stored_chunks.extend(new_chunks)

        self.save_index()


    def save_index(self):
        faiss.write_index(self.index, self.INDEX_FILE)

        with open(self.CHUNK_FILE, "wb") as f:
            pickle.dump(self.stored_chunks, f)  



    def load_index(self):

        if os.path.exists(self.INDEX_FILE):
            self.index = faiss.read_index(self.INDEX_FILE)

            with open(self.CHUNK_FILE, "rb") as f:
                self.stored_chunks = pickle.load(f)
        else:
            print("No existing index found")

    def search(self,question_embedding, k=40):
        if self.index is None or self.index.ntotal == 0:
            return []

        query = np.array([question_embedding]).astype("float32")

        distances, indices = self.index.search(query, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1:
                continue

            results.append({
                "text": self.stored_chunks[idx]["text"],
                "document_id": self.stored_chunks[idx]["document_id"],
                "embedding": self.index.reconstruct(int(idx)),
                "score": float(distances[0][i])
            })
        return results