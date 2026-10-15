from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.order import OrderModel

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def count_by_scheduled_time(self, scheduled_time: str) -> int:
        stmt = select(func.count()).select_from(OrderModel).where(OrderModel.scheduled_time == scheduled_time)
        return self.db.scalar(stmt) or 0

    def create(self, order_id: str, item_id: str, scheduled_time: str, total_amount: float, notes: str = None) -> OrderModel:
        order = OrderModel(id=order_id, item_id=item_id, scheduled_time=scheduled_time, total_amount=total_amount, notes=notes)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_all(self) -> List[OrderModel]:
        stmt = select(OrderModel).order_by(OrderModel.created_at.desc())
        return list(self.db.scalars(stmt).all())
