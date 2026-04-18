from fastapi import APIRouter,UploadFile,Depends
from app.services import ingestion_service
from app.core.dependencies import get_db,get_current_user
from sqlalchemy.orm import Session
from app.models.document import Document
import uuid
from app.core.config import settings
print("DB URL:", settings.DATABASE_URL)
router =APIRouter()

@router.post("/upload")
async def upload_doc(
    file: UploadFile,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
    ):
    document_id = str(uuid.uuid4())

    result = ingestion_service.process_file(file, document_id)

    doc = Document(id=document_id, user_id=user_id)
    db.add(doc)
    db.commit()

    return {"document_id": document_id, "status": result}