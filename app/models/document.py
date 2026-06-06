from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String,primary_key=True)
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id")
    )
    filename: Mapped[str] = mapped_column(String)
    file_hash: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(
        String,
        default="processing"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(
        default=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )