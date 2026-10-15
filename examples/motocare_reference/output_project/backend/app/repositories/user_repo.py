from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import UserModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_phone(self, phone: str) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.phone_number == phone)
        return self.db.scalars(stmt).first()

    def create(self, phone: str, full_name: str, password_hash: str, role: str = "CUSTOMER") -> UserModel:
        user = UserModel(phone_number=phone, full_name=full_name, password_hash=password_hash, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
