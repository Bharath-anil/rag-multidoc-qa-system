from pydantic import BaseModel
from typing import Optional

class QuestionRequest(BaseModel):
    document_id: Optional[str] = None
    question: str