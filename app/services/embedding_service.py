from  sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def embed_chunks(chunks):
    return model.encode(chunks)

def embed_query(question):
    return model.encode([question])[0]
