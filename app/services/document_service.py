from sqlalchemy.orm import Session
from app.models.document import Document
from datetime import datetime, UTC, timedelta
from app.services.qdrant_vector_store import qdrant_store

def get_all_documents(user_id:str,db:Session):
    docs = db.query(Document).filter(
        Document.user_id == user_id,
        Document.is_active == True
    ).order_by(Document.created_at.desc()).all()
    return [
        {
            "id": d.id,
            "filename": d.filename,
            "status": d.status,
            "created_at": d.created_at

        } for d in docs
    ]


def delete_document( document_id: str, user_id: str, db: Session ):
    doc = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id,
        Document.is_active == True
    ).first()

    if not doc:
        return {
            "message": "Document not found"
        }
    
    doc.is_active = False
    doc.deleted_at = datetime.now(UTC)
    db.commit()
    
    return {
        "message": "Document deleted successfully"
    }


def get_deleted_documents( user_id: str, db: Session):
    return ( db.query(Document)
        .filter(
            Document.user_id == user_id,
            Document.is_active == False
        ) .all())


def restore_document( document_id: str, user_id: str, db: Session):
    doc = ( db.query(Document)
        .filter(
            Document.id == document_id,
            Document.user_id == user_id,
            Document.is_active == False
        ).first())

    if not doc:
        return {
            "message": "Document not found"
        }

    doc.is_active = True
    doc.deleted_at = None
    db.commit()

    return {
        "message": "Document restored successfully"
    }

def get_expired_deleted_documents(
    days: int,
    db: Session
):
    cutoff = datetime.now(UTC) - timedelta(days=days)

    return (
        db.query(Document)
        .filter(
            Document.is_active == False,
            Document.deleted_at < cutoff
        )
        .all()
    )


def permanently_delete_document(
    document_id: str,
    db: Session
):
    doc = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    if not doc:
        return

    qdrant_store.delete_document_vectors(
        document_id=document_id
    )

    db.delete(doc)
    db.commit()