from app.services.embedding_service import EmbeddingService
from app.core.database import SessionLocal

embedding_service = EmbeddingService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
