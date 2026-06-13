from fastapi import APIRouter
from app.services import document_service
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user

router = APIRouter()

@router.get("/documents")
async def get_documents( user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return document_service.get_all_documents(
        user_id,
        db
    )

@router.delete("/documents/{document_id}")
async def delete_document( document_id: str, user_id: str = Depends(get_current_user),db: Session = Depends(get_db)):
    return document_service.delete_document(
        document_id=document_id,
        user_id=user_id,
        db=db
    )


@router.get("/documents/deleted")
async def get_deleted_documents( user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return document_service.get_deleted_documents(
        user_id,
        db
    )

@router.post("/documents/{document_id}/restore")
async def restore_document( document_id: str, user_id: str = Depends(get_current_user),  db: Session = Depends(get_db)):
    return document_service.restore_document(
        document_id,
        user_id,
        db
    )