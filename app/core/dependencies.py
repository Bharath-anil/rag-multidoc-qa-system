from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStore
from app.core.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

embedding_service = EmbeddingService()
vector_store = VectorStore()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



api_key_header = APIKeyHeader(name="X-User-Id")

def get_current_user(x_user_id: str = Depends(api_key_header)):
    if not x_user_id:
        raise HTTPException(status_code=401, detail="Missing user")

    return x_user_id