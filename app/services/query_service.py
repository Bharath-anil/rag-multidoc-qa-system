from .storage import document_store
from . import embedding_service,generation_service

def generate_ans(question:str):

    if not document_store["chunks"]:    
        return {"message": "No document uploaded."}

    question_asked = question
    chunks = document_store["chunks"]
    embedded_data = document_store["embeddings"]
    top_k = embedding_service.retrieve_top_k(question_asked,chunks,embedded_data)
    top_score = top_k[0]["score"]

    if top_score < 0.3:  #Does make sure that LLM does not hallucinate and say non related answers
        return {
            "message": "Question not relevant to document.",
            "top_score": top_score
        }
    top_chunks = [item["chunk"] for item in top_k]

    answer = generation_service.generate_answer(
        question,
        top_chunks
    )

    return {
    "similarity_scores": top_k,
    "answer": answer
    }