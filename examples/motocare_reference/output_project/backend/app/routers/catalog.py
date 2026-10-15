from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.catalog import CatalogItemResponse
from app.repositories.catalog_repo import CatalogRepository

router = APIRouter(prefix="/catalog", tags=["Catalog"])

@router.get("", response_model=List[CatalogItemResponse])
def get_catalog(db: Session = Depends(get_db)):
    repo = CatalogRepository(db)
    return repo.list_active()
