import os
from pathlib import Path
from . import text_extractor,text_cleaner,chunk_service,embedding_service


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
    retreive_k_elements = embedding_service.retrieve_top_k("What is API layer",chunks,embedded_data)

    return {
    "filename": file_path.name,
    "text_length": len(raw),
    "total_chunks": len(chunks),
    "embedding dimensions ":len(embedded_data[0]),
    "similarity_scores": retreive_k_elements,
    "preview": chunks[0][:500] if chunks else ""
}