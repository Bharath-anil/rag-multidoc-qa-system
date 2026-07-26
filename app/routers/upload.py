from fastapi import APIRouter,UploadFile,Depends,HTTPException,BackgroundTasks
from app.services import ingestion_service
from app.core.dependencies import get_db
from app.core.auth import get_current_user
from sqlalchemy.orm import Session
from app.models.document import Document
import uuid
import hashlib
router =APIRouter( tags=["Documents"])

@router.post("/upload",
            summary="Upload PDF document",
            description=(
            "Uploads a PDF document, validates it, stores metadata, "
            "and starts background ingestion for text extraction, "
            "chunking, embedding generation, and Qdrant indexing." ),
            response_description="Document upload started successfully.",)
async def upload_doc(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    document_id = str(uuid.uuid4())

    # read file bytes for hashing
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Maximum allowed file size is 20 MB."
        )

    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # reset pointer after reading
    file.file.seek(0)

    # dedup check
    existing_doc = db.query(Document).filter(
        Document.user_id == user_id,
        Document.file_hash == file_hash,
        Document.is_active == True
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
    background_tasks.add_task(
        ingestion_service.process_file,
        file,
        document_id,
        user_id
    )
    db.refresh(doc)
    return {
        "document_id": document_id,
        "status": "processing",
        "message": "Document upload started."
    }
