import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column( String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column( String, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column( DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column( DateTime, default=func.now(), onupdate=func.now())
    is_active: Mapped[bool] = mapped_column( default=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime,nullable=True)