from sqlalchemy.orm import Session
from app.models.conversation import Conversation

def create_conversation(user_id:str,db:Session):
    conversation =Conversation(user_id = user_id, title="New Chat")

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def get_conversations( user_id: str, db: Session ):
    return (
        db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.is_active == True
        ).order_by(Conversation.updated_at.desc()).all()
    )