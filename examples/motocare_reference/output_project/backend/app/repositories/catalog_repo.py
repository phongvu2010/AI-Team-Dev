from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.catalog import CatalogItemModel

class CatalogRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_active(self) -> List[CatalogItemModel]:
        stmt = select(CatalogItemModel).where(CatalogItemModel.is_active == True)
        items = list(self.db.scalars(stmt).all())
        if not items:
            # Seed dữ liệu mặc định ban đầu
            defaults = [
                CatalogItemModel(id="item_001", name="Phụ tùng & Dịch vụ Sửa chữa Xe Tiêu chuẩn", price=150000.0, stock_quantity=50),
                CatalogItemModel(id="item_002", name="Phụ tùng & Dịch vụ Sửa chữa Xe Cao cấp", price=225000.0, stock_quantity=30),
            ]
            self.db.add_all(defaults)
            self.db.commit()
            return defaults
        return items
