import os
from pathlib import Path
from . import text_extractor,text_cleaner,chunk_service,embedding_service,generation_service


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_file(file):
    file_path = UPLOAD_DIR / file.filename
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    return file_path

def process_file(file):
    file_path = save_file(file)
    raw = text_extractor.extract_text(file_path)
    cleaned = text_cleaner.clean_data(raw)
    chunks = chunk_service.chunk_data(cleaned)
    embedded_data = embedding_service.embed_chunks(chunks)
    question = "What is a docker"
    top_k = embedding_service.retrieve_top_k(
        question,
        chunks,
        embedded_data
    )

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
    "filename": file_path.name,
    "text_length": len(raw),
    "total_chunks": len(chunks),
    "embedding dimensions ":len(embedded_data[0]),
    "similarity_scores": top_k,
    "answer": answer
}