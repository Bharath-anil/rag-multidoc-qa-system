from  sentence_transformers import SentenceTransformer

model = None

def get_model():
    global model
    if model is None:
        print("Loading embedding model...")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")  # lighter
    return model

def embed_chunks(chunks):
    model = get_model()
    return model.encode(chunks)

def embed_query(question):
    model = get_model()
    return model.encode([question])[0]