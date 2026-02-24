from .storage import document_store
from . import embedding_service,generation_service

def generate_ans(question:str,document_id:str):
    if document_id not in document_store:
        return {"message": "Document not found"}
    
    question_asked = question
    chunks = document_store[document_id]["chunks"]
    embedded_data = document_store[document_id]["embeddings"]
    top_k = embedding_service.retrieve_top_k(question_asked,chunks,embedded_data)
    top_score = top_k[0]["score"]

    if top_score < 0.3:  #Does make sure that LLM does not hallucinate and say non related answers
        return {
            "message": "Not found in the document",
            "top_score": top_score
        }
    top_chunks = [item["chunk"] for item in top_k]

    answer = generation_service.generate_answer(
        question,
        top_chunks
    )

    return {
    "top_score": top_k[0]["score"],
    "top_chunks": top_k,
    "answer": answer
    }