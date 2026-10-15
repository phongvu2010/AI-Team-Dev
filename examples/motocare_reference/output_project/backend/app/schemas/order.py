from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class OrderCreateRequest(BaseModel):
    item_id: str = Field(..., min_length=1)
    scheduled_time: str = Field(..., min_length=5)
    notes: Optional[str] = Field(None)

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    item_id: str
    scheduled_time: str
    status: str
    total_amount: float
    notes: Optional[str] = None
