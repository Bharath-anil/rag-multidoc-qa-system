from pydantic import BaseModel
from typing import Optional,List

class QuestionRequest(BaseModel):
    document_ids: Optional[List[str]] = None
    question: str
    username: str