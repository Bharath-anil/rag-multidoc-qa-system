from . import text_extractor,text_cleaner,chunk_service,embedding_service,file_service,vector_store_service
from .storage import document_store
import uuid
def process_file(file):
    document_id = str(uuid.uuid4())
    file_path = file_service.save_file(file)
    raw = text_extractor.extract_text(file_path)
    cleaned = text_cleaner.clean_data(raw)
    chunks = chunk_service.chunk_data(cleaned)
    embedded_data = embedding_service.embed_chunks(chunks)
    document_store[document_id] = {
        "chunks": chunks,
        "embeddings": embedded_data
    }  
    vector_store_service.build_index(embedded_data, chunks)
    return {
    "filename": file_path.name,
    "text_length": len(raw),
    "total_chunks": len(chunks),
    "embedding dimensions ":len(embedded_data[0]),
    "document_id": document_id,
    
}
