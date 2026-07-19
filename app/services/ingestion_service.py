from . import text_extractor,text_cleaner,chunk_service,embedding_service,file_service
from app.core.dependencies import embedding_service
from app.services.qdrant_vector_store import qdrant_store
from app.core.logger import logger
from fastapi import HTTPException
from app.models.document import Document
from app.core.database import SessionLocal

def process_file(file,document_id,user_id):
    db = SessionLocal()
    try:
        #document_id = str(uuid.uuid4())
        file_path = file_service.save_file(file)

        try:
            raw = text_extractor.extract_text(file_path)
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is corrupted or unreadable."
            )

        if not raw.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text found in the uploaded PDF."
            )

        cleaned = text_cleaner.clean_data(raw)
        chunks = chunk_service.chunk_data(cleaned)
        chunks = [c for c in chunks if "Table of Contents" not in c]
        chunks = [c for c in chunks if len(c) > 40]
        # chunks = chunks[:10]
        for embeddings, batch_chunks in embedding_service.embed_chunks(chunks):

            qdrant_store.add_embeddings(
                embeddings=embeddings,
                chunks=batch_chunks,
                document_id=document_id,
                user_id=user_id,
                filename=file.filename
            )

        doc = db.query(Document).filter(  Document.id == document_id ).first()
        doc.status = "ready"
        db.commit()

        logger.info(f"Processed document: {document_id}")   
        return {
        "filename": file_path.name,
        "text_length": len(raw),
        "total_chunks": len(chunks),
        "document_id": document_id}
    except Exception as e:
        doc = db.query(Document).filter( Document.id == document_id ).first()

        if doc:
            doc.status = "failed"
            db.commit()

        raise
    finally:
        db.close()
