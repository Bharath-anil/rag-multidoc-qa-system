from  sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model
    if model is None:
        print("Loading embedding model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")  # lighter
    return model

def embed_chunks(chunks, batch_size=4):
    model = get_model()

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        embeddings = model.encode(batch)

        yield embeddings, batch

def embed_query(question):
    model = get_model()
    return model.encode([question])[0]