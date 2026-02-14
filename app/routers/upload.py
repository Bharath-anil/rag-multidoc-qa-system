from fastapi import APIRouter,UploadFile
from app.services import file_service
router =APIRouter()

@router.get("/health")
def health_check():
    return {"status":"Healthy"}


@router.post("/upload")
def upload_doc(file: UploadFile):
    result = file_service.process_file(file)
    return result