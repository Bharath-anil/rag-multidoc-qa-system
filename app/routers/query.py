from fastapi import APIRouter
from app.services import query_service
from app.schemas.request import QuestionRequest
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user

router = APIRouter()
from app.core.config import settings
print("DB URL:", settings.DATABASE_URL)
@router.post("/ask")
async def ask_about_doc(
    payload: QuestionRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return query_service.generate_ans(
        payload.question,
        user_id,
        db,
        payload.document_ids
    )