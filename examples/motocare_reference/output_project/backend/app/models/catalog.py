from sqlalchemy import String, Float, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class CatalogItemModel(Base):
    __tablename__ = "catalog_items"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    price: Mapped[float] = mapped_column(Float, default=150000.0)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=100)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
