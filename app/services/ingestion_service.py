from . import text_extractor,text_cleaner,chunk_service,embedding_service,file_service,vector_store_service
from .storage import document_store
import uuid
def process_file(file):
    document_id = str(uuid.uuid4())
    file_path = file_service.save_file(file)
    raw = text_extractor.extract_text(file_path)
    cleaned = text_cleaner.clean_data(raw)
    chunks = chunk_service.chunk_data(cleaned)
    chunks = [c for c in chunks if "Table of Contents" not in c]
    chunks = [c for c in chunks if len(c) > 150]
    chunks = chunks[:10]
    for embeddings, batch_chunks in embedding_service.embed_chunks(chunks):
        vector_store_service.build_index(embeddings, batch_chunks, document_id)

    return {
    "filename": file_path.name,
    "text_length": len(raw),
    "total_chunks": len(chunks),
    "document_id": document_id,
    
}
