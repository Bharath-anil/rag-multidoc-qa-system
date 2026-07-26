from fastapi import APIRouter
from app.services import document_service
from app.core.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.core.auth import get_current_user

router = APIRouter(tags=["Documents"])

@router.get("/documents",
            summary="Retrieve all active documents",
            description="Returns all active documents uploaded by the authenticated user.",
            response_description="List of active documents retrieved successfully.",)
async def get_documents( user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return document_service.get_all_documents(
        user_id,
        db
    )

@router.delete("/documents/{document_id}",
                summary="Delete a document",
                description="Soft deletes a document belonging to the authenticated user.",
                response_description="Document deleted successfully.",
                responses={
                    404: {"description": "Document not found."},
                    403: {"description": "Unauthorized access to document."},
                },)
async def delete_document( document_id: str, user_id: str = Depends(get_current_user),db: Session = Depends(get_db)):
    return document_service.delete_document(
        document_id=document_id,
        user_id=user_id,
        db=db
    )


@router.get("/documents/deleted",
            summary="Retrieve deleted documents",
            description="Returns all soft deleted documents for the authenticated user.",
            response_description="Deleted documents retrieved successfully.",)
async def get_deleted_documents( user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return document_service.get_deleted_documents(
        user_id,
        db
    )

@router.post("/documents/{document_id}/restore",
            summary="Restore a deleted document",
            description="Restores a previously soft deleted document owned by the authenticated user.",
            response_description="Document restored successfully.",
            responses={
                404: {"description": "Document not found."},
            },)
async def restore_document( document_id: str, user_id: str = Depends(get_current_user),  db: Session = Depends(get_db)):
    return document_service.restore_document(
        document_id,
        user_id,
        db
    )