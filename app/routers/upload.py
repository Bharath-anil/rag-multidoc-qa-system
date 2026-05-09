from fastapi import APIRouter,UploadFile,Depends
from app.services import ingestion_service
from app.core.dependencies import get_db
from app.core.auth import get_current_user
from sqlalchemy.orm import Session
from app.models.document import Document
import uuid
import hashlib
router =APIRouter()

@router.post("/upload")
async def upload_doc(
    file: UploadFile,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    document_id = str(uuid.uuid4())

    # read file bytes for hashing
    file_bytes = await file.read()

    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # reset pointer after reading
    file.file.seek(0)

    # dedup check
    existing_doc = db.query(Document).filter(
        Document.user_id == user_id,
        Document.file_hash == file_hash
    ).first()

    if existing_doc:
        return {
            "message": "Document already uploaded",
            "document_id": existing_doc.id,
            "status": existing_doc.status
        }

    # create DB row FIRST
    doc = Document(
        id=document_id,
        user_id=user_id,
        filename=file.filename,
        file_hash=file_hash,
        status="processing"
    )

    db.add(doc)
    db.commit()

    try:
        result = ingestion_service.process_file(
            file,
            document_id
        )

        doc.status = "ready"

        db.commit()

        return {
            "document_id": document_id,
            "status": doc.status,
            "result": result
        }

    except Exception as e:
        doc.status = "failed"

        db.commit()

        return {
            "document_id": document_id,
            "status": "failed",
            "error": str(e)
        }