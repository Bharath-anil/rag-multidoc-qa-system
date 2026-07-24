from pydantic import BaseModel
from typing import Optional,List

class QuestionRequest(BaseModel):
    conversation_id: str
    document_ids: Optional[List[str]] = None
    question: str