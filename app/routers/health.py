from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.services.health_service import health_service

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/",
            summary="Check application health",
            description="Verifies connectivity to PostgreSQL and Qdrant and reports the overall application health status.",
            response_description="Health status returned successfully.",)
def health(db: Session = Depends(get_db)):
    return health_service.get_health_status(db)