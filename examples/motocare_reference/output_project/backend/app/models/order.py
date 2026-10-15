from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.core.database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(50), default="guest_user")
    item_id: Mapped[str] = mapped_column(String(50), nullable=False)
    scheduled_time: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(30), default="CONFIRMED")
    total_amount: Mapped[float] = mapped_column(Float, default=150000.0)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
