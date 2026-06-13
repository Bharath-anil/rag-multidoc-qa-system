from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.auth import get_current_user
from app.services import conversation_service

router = APIRouter()

@router.post("/conversations")
async def create_conversation(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return conversation_service.create_conversation(
        user_id,
        db
    )


@router.get("/conversations")
async def get_conversations( user_id: str = Depends(get_current_user), db: Session = Depends(get_db) ):
    return conversation_service.get_conversations( user_id, db )