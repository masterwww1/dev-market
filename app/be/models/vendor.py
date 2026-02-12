"""Vendor model for B2B marketplace."""
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from be.database import Base


class Vendor(Base):
    """Vendor/seller in the B2B marketplace."""

    __tablename__ = "vendors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Vendor(id={self.id}, name={self.name!r})>"
