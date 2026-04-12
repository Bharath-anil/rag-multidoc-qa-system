from fastapi import APIRouter,UploadFile
from app.services import ingestion_service

router =APIRouter()

@router.post("/upload")
async def upload_doc(file: UploadFile):
    result = ingestion_service.process_file(file)
    return result

