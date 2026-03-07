from .storage import document_store
from . import embedding_service,generation_service,vector_store_service 

def generate_ans(question:str,document_id:str):
    if document_id not in document_store:
        return {"message": "Document not found"}
    
    question_embedding = embedding_service.embed_query(question)
    top_chunks = vector_store_service.search(question_embedding, k=5)
    answer = generation_service.generate_answer(
        question,
        top_chunks
    )

    return {
        "chunks_used": top_chunks,
        "answer": answer
    }