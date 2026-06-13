from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message

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


def save_message( conversation_id: str, role: str, content: str, db: Session ):
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message



def get_messages( conversation_id: str,  db: Session ):
    return (
    db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(
        Message.created_at
    ).all()
)

#delete conversation 
def delete_conversation( conversation_id: str, user_id: str, db: Session ):
    conversation = (
        db.query(Conversation) .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
            Conversation.is_active == True
        ).first()
    )

    if not conversation:
        return {
            "message": "Conversation not found"
        }

    conversation.is_active = False
    db.commit()

    return {
        "message": "Conversation deleted successfully"
    }