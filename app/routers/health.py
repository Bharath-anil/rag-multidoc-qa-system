from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.services.health_service import health_service

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
def health(db: Session = Depends(get_db)):
    return health_service.get_health_status(db)