from fastapi import APIRouter,HTTPException
from app.services import query_service,conversation_service
from app.schemas.request import QuestionRequest
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.models.conversation import Conversation

router = APIRouter()

@router.post("/ask")
async def ask_about_doc(payload: QuestionRequest,user_id: str = Depends(get_current_user),db: Session = Depends(get_db)):

    conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == payload.conversation_id,
                Conversation.user_id == user_id,
                Conversation.is_active == True
            )
            .first()
        )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    conversation_service.save_message(
        conversation_id=payload.conversation_id,
        role="user",
        content=payload.question,
        db=db
    )

    response = query_service.generate_ans(
        payload.question,
        user_id,
        db,
        payload.document_ids
    )

    conversation_service.save_message(
        conversation_id=payload.conversation_id,
        role="assistant",
        content=response["answer"],
        db=db
    )

    return response