from fastapi import APIRouter,UploadFile
from app.services import file_service,ingestion_service,query_service
from pydantic import BaseModel
router =APIRouter()

class QuestionRequest(BaseModel):
    document_id:str|None =None
    question:str 


@router.get("/health")
def health_check():
    return {"status":"Healthy"}


@router.post("/upload")
def upload_doc(file: UploadFile):
    result = ingestion_service.process_file(file)
    return result

@router.post("/ask")
def ask_about_doc(payload: QuestionRequest):
    result_data = query_service.generate_ans(payload.question,payload.document_id)
    return result_data