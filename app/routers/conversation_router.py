from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.core.auth import get_current_user
from app.services import conversation_service
from app.models.conversation import Conversation
from app.schemas.conversation import MessageRequest
router = APIRouter()


@router.post("/conversations",
            summary="Create a new conversation",
            description="Creates a new conversation for the authenticated user.",
            response_description="Conversation created successfully.",)
async def create_conversation(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return conversation_service.create_conversation(
        user_id,
        db
    )


@router.get("/conversations",
            summary="Retrieve conversations",
            description="Returns all active conversations for the authenticated user.",
            response_description="Conversations retrieved successfully.",)
async def get_conversations( user_id: str = Depends(get_current_user), db: Session = Depends(get_db) ):
    return conversation_service.get_conversations( user_id, db )

@router.post("/messages",
            summary="Save a conversation message",
            description="Stores a user or assistant message in an existing conversation.",
            response_description="Message saved successfully.",)
async def save_message(payload: MessageRequest,db: Session = Depends(get_db)):
    return conversation_service.save_message(
        payload.conversation_id,
        payload.role,
        payload.content,
        payload.sources,
        db
    )

@router.get("/messages/{conversation_id}",
            summary="Retrieve conversation messages",
            description="Returns all messages belonging to the specified conversation.",
            response_description="Conversation messages retrieved successfully.",
            responses={
                404: {"description": "Conversation not found."},
            },)
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

@router.delete("/conversations/{conversation_id}",
            summary="Delete a conversation",
            description="Soft deletes an existing conversation for the authenticated user.",
            response_description="Conversation deleted successfully.",
            responses={
                404: {"description": "Conversation not found."},
            },)
async def delete_conversation( conversation_id: str, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return conversation_service.delete_conversation(
        conversation_id,
        user_id,
        db
    )


@router.get("/conversation/deleted",
            summary="Retrieve deleted conversations",
            description="Returns all soft deleted conversations for the authenticated user.",
            response_description="Deleted conversations retrieved successfully.",)
async def get_deleted_documents( user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return conversation_service.get_deleted_conversation(
        user_id,
        db
    )

@router.post("/conversation/{conversation_id}/restore",
            summary="Restore a deleted conversation",
            description="Restores a previously deleted conversation belonging to the authenticated user.",
            response_description="Conversation restored successfully.",
            responses={
                404: {"description": "Conversation not found."},
            },)
async def restore_conversation( conversation_id: str, user_id: str = Depends(get_current_user),  db: Session = Depends(get_db)):
    return conversation_service.restore_conversation(
        conversation_id,
        user_id,
        db
    )