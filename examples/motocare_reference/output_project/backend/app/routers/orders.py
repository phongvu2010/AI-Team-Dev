from fastapi import APIRouter, HTTPException, status, Header, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.order import OrderCreateRequest, OrderResponse
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(req: OrderCreateRequest, authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization Header")
    service = OrderService(db)
    order = service.create_order(item_id=req.item_id, scheduled_time=req.scheduled_time, notes=req.notes)
    return order

@router.get("", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.list_orders()
