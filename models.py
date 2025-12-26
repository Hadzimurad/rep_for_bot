from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from typing import Optional


class Base(DeclarativeBase):
    pass


class Diagnostic(Base):
    __tablename__ = "diagnostics"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    username: Mapped[Optional[str]] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)  # Формат: ДД.ММ.ГГГГ
    time: Mapped[str] = mapped_column(nullable=False)  # Формат: ЧЧ:ММ
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
