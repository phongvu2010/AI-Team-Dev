import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from app.core.config import settings

# Base Declarative Model theo chuẩn SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass

# Tạo Database Engine (Tương thích SQLite file/in-memory và PostgreSQL)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Khởi tạo bảng trong cơ sở dữ liệu."""
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """FastAPI Dependency cung cấp Session cơ sở dữ liệu."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
