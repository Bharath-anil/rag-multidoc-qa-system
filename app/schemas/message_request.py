from pydantic import BaseModel

class MessageRequest(BaseModel):
    conversation_id: str
    role: str
    content: str
