from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.auth import get_current_user
from app.services import conversation_service
from app.models.conversation import Conversation
from app.schemas.message_request import MessageRequest
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

@router.post("/messages")
async def save_message(payload: MessageRequest,db: Session = Depends(get_db)):
    return conversation_service.save_message(
        payload.conversation_id,
        payload.role,
        payload.content,
        db
    )

@router.get("/messages/{conversation_id}")
async def get_messages( conversation_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db) ):
    conversation = db.query(Conversation).filter( Conversation.id == conversation_id, Conversation.user_id == user_id).first()

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return conversation_service.get_messages(
        conversation_id,
        db
    )

@router.delete("/conversations/{conversation_id}")
async def delete_conversation( conversation_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return conversation_service.delete_conversation(
        conversation_id,
        user_id,
        db
    )


@router.get("/conversation/deleted")
async def get_deleted_documents( user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return conversation_service.get_deleted_conversation(
        user_id,
        db
    )

@router.post("/conversation/{conversation_id}/restore")
async def restore_conversation( conversation_id: str, user_id: str = Depends(get_current_user),  db: Session = Depends(get_db)):
    return conversation_service.restore_conversation(
        conversation_id,
        user_id,
        db
    )