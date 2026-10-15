import uuid
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.repositories.order_repo import OrderRepository
from app.models.order import OrderModel

class OrderService:
    def __init__(self, db: Session):
        self.repo = OrderRepository(db)

    def create_order(self, item_id: str, scheduled_time: str, notes: str = None) -> OrderModel:
        # Kiểm tra Business Rule công suất tối đa theo BR-01
        current_count = self.repo.count_by_scheduled_time(scheduled_time)
        if current_count >= settings.MAX_SLOT_CAPACITY:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Khung giờ {scheduled_time} đã đạt giới hạn tối đa {settings.MAX_SLOT_CAPACITY} yêu cầu. Vui lòng chọn khung giờ khác!"
            )

        order_id = f"ORD_{uuid.uuid4().hex[:8].upper()}"
        return self.repo.create(
            order_id=order_id,
            item_id=item_id,
            scheduled_time=scheduled_time,
            total_amount=150000.0,
            notes=notes
        )

    def list_orders(self) -> List[OrderModel]:
        return self.repo.get_all()
