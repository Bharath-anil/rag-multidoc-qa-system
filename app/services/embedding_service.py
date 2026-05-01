from  sentence_transformers import SentenceTransformer
from app.core.config import settings
class EmbeddingService:
    def __init__(self):
        self.model = None

    def get_model(self):
        if self.model is None:
            print("Loading embedding model...")
            self.model = SentenceTransformer(settings.MODEL_NAME)
        return self.model

    def embed_chunks(self,chunks, batch_size=4):
        model = self.get_model()

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            embeddings = model.encode(batch)

            yield embeddings, batch

    def embed_query(self,question):
        model = self.get_model()
        return model.encode([question])[0]