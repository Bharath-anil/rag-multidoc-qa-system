from sqlalchemy.orm import Session
from app.models.document import Document

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
    db.commit()
    
    return {
        "message": "Document deleted successfully"
    }