import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "MotoCare_Upgrade API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "prod_safe_super_secret_jwt_key_2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data.db")
    MAX_SLOT_CAPACITY: int = 3  # Giới hạn tối đa 3 xe mỗi khung giờ (BR-01)

settings = Settings()
