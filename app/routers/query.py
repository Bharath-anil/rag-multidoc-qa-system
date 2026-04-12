from fastapi import APIRouter
from app.services import query_service
from app.schemas.request import QuestionRequest

router = APIRouter()

@router.post("/ask")
async def ask_about_doc(payload: QuestionRequest):
    return query_service.generate_ans(
        payload.question,
        payload.document_id
    )