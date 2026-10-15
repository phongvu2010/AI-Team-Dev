from pydantic import BaseModel, ConfigDict

class CatalogItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    price: float
    stock_quantity: int
    is_active: bool
