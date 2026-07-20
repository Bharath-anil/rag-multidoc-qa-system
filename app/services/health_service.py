from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.qdrant_vector_store import qdrant_store

class HealthService:
    def check_database(self, db: Session) -> bool:
        try:
            db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False

    def check_qdrant(self) -> bool:
        try:
            qdrant_store.client.get_collection(
                qdrant_store.collection_name
            )
            return True
        except Exception:
            return False

    def get_health_status(self, db: Session):

        database_ok = self.check_database(db)
        qdrant_ok = self.check_qdrant()

        overall_status = (
            "healthy"
            if database_ok and qdrant_ok
            else "unhealthy"
        )

        return {
            "status": overall_status,
            "database": ( "connected"
                if database_ok
                else "disconnected"
            ),
            "qdrant": ( "connected"
                if qdrant_ok
                else "disconnected"
            ),
        }


health_service = HealthService()