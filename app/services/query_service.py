from .storage import document_store
from . import embedding_service,generation_service,vector_store_service,rerank_service 

def generate_ans(question:str,document_id:str):

    question_embedding = embedding_service.embed_query(question)
    candidate_chunks = vector_store_service.search(question_embedding, k=20)
    candidate_chunks = [
        c["text"]
        for c in candidate_chunks
        if c["document_id"] == document_id
    ]
    reranked = rerank_service.rerank(question,candidate_chunks,question_embedding,embedding_service.model,k=5)
    top_chunks = [item["chunk"]for item in reranked]
    answer = generation_service.generate_answer(
        question,
        top_chunks
    )

    return {
        "chunks_used": top_chunks,
        "answer": answer
    }